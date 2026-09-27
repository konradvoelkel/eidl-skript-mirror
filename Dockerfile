# Basis-Image **mit Digest** angeheftet. Der Tag `python3.14-nodejs26-slim` heftet nur die
# Minor-Versionen an; Patch-Stand und Debian-Pakete wandern darunter weg (in eipy-skript
# innerhalb eines Tages von Python 3.14.4 auf 3.14.7 und Node 26.1.0 auf 26.10.0).
# Patch-genaue Tags gibt es bei diesem Image nicht, also bleibt der Digest.
#
# Warum das hier zaehlt: Der Image-Bau laeuft automatisch und blockierend, sobald sich das
# Dockerfile aendert. Mit einem wandernden Basis-Image koennte ein Commit aus einem voellig
# unbeteiligten Grund rot werden. Angeheftet bedeutet ein Fehlschlag etwas.
#
# Preis: Sicherheitsaktualisierungen kommen erst beim bewussten Anheben an -- dieselbe
# Pflege-Zusage wie beim mitgelieferten Site-Template in `_site/vendor/`.
#
# Anheben:
#   docker pull nikolaik/python-nodejs:python3.14-nodejs26-slim
#   docker inspect --format '{{index .RepoDigests 0}}' \
#     nikolaik/python-nodejs:python3.14-nodejs26-slim
# Danach den `build-image`-Job von Hand ausloesen (rules: when manual).
#
# Stand 2026-09-27: Python 3.14.7, Node v26.10.0 -- derselbe Digest wie in eipy-skript.
FROM nikolaik/python-nodejs:python3.14-nodejs26-slim@sha256:02488bd4048b3864f785dafcd549f4842a0b10d449f3cf7fa38fbcde1f35812d

# System dependencies. The TeX packages are what `myst build --pdf` needs: latexmk drives
# xelatex, the texlive-* sets cover the packages used by templates/tex/eidl-skript
# (fontspec, hyperref, minted, microtype, ...), texlive-lang-german the hyphenation
# patterns. fonts-dejavu-core provides "DejaVu Sans Mono", which the template sets as the
# monospace font. poppler-utils liefert `pdftotext` fuer die Stichproben in
# devnotes/check_pdf_build.py.
#
# Bewusst **nicht** drin: `imagemagick`. MyST braucht es, um Bilder in Formate zu wandeln,
# die LaTeX lesen kann -- dieses Buch hat aber ausschliesslich PNG und JPG (45 + 2, Stand
# 2026-09-27) und kein einziges SVG. Sollte je ein SVG dazukommen, meldet MyST das auf
# stdout ("To convert .svg images ... you must install inkscape"), und
# check_pdf_build.py liest diese Ausgabe ueber `--myst-log` mit.
RUN apt-get update && apt-get install -y --no-install-recommends \
    procps \
    latexmk \
    texlive-xetex \
    texlive-latex-recommended \
    texlive-latex-extra \
    texlive-fonts-recommended \
    texlive-lang-german \
    fonts-dejavu-core \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

# Seit `code_style: minted` in myst.yml steht, braucht der PDF-Bau die Hilfsanwendung
# `latexminted`: Debians texlive-latex-extra bringt minted **v3** mit, und das holt seine
# Pygments-Stile ueber diesen Helfer statt ueber `pygmentize`. Debian liefert ihn passend
# gebuendelt mit (Symlink /usr/bin/latexminted auf
# .../texmf-dist/scripts/minted/latexminted.py, dazu das Wheel daneben).
#
# Zwei Dinge stehen dem in diesem Image im Weg -- beide 2026-09-26 in eipy-skript im
# Container nachgewiesen, dort vorher 745 Fehler "minted executable is unavailable or
# disabled":
#
# 1. Ein `latexminted` aus PyPI landet in /usr/local/bin, verdeckt Debians Variante -- und
#    0.7.1 verlangt minted.sty >= 3.8.0, waehrend Debian 3.6.0 hat. Deshalb steht es
#    **nicht** in pyproject.toml, und es darf auch nicht dazukommen.
# 2. Der Shebang `#!/usr/bin/env python3` trifft hier /usr/local/bin/python3, also Python
#    3.14 aus dem Basis-Image. Unter 3.14 stirbt die gebuendelte latexminted 0.5.0 in
#    argparse ("ArgParser.__init__() got an unexpected keyword argument 'color'").
#    Debians eigenes python3 fuehrt sie fehlerfrei aus -- daher der feste Shebang.
#
# Gepatcht wird die *echte* Datei, nicht der Symlink: `sed -i` auf /usr/bin/... wuerde den
# Symlink durch eine Kopie ersetzen, und das Skript findet seine Wheels ueber den
# aufgeloesten eigenen Pfad ("failed to find bundled wheels").
#
# `latexminted --version` ist der Selbsttest: Kippt die Paarung bei einem Debian- oder
# Basis-Image-Sprung, scheitert der **Image-Bau** statt des PDF-Laufs.
RUN sed -i '1s|.*|#!/usr/bin/python3|' \
      /usr/share/texlive/texmf-dist/scripts/minted/latexminted.py \
    && latexminted --version > /dev/null

# mystmd global installieren -- **mit angehefteter Version**, passend zur dev-Gruppe in
# pyproject.toml. Die beiden werden gemeinsam angehoben.
RUN npm install -g mystmd@1.10.1

# mystmd hat im LaTeX-Export einen Fehler: Es schreibt Codeblock-Inhalte mit
# `mathMode = true` und setzt dabei vor **jeden Bindestrich ein Leerzeichen**. Aus
# `nvidia-smi` wird `nvidia -smi`, aus `--index-url` wird `- -index -url`. Im HTML
# passiert das nicht, nur im PDF. Details, Nachweis und Reparatur:
# devnotes/patch_myst_tex.py.
#
# Das Skript ist idempotent und scheitert laut, wenn die Stelle nicht mehr da ist -- dann
# hat mystmd sich bewegt (Version ist oben angeheftet), und jemand prueft, ob der Fehler
# behoben ist. Der `myst --version`-Aufruf danach stellt sicher, dass das gepatchte Bundle
# ueberhaupt noch startet.
COPY devnotes/patch_myst_tex.py /tmp/
RUN python3 /tmp/patch_myst_tex.py /usr/local/lib/node_modules/mystmd/dist/myst.cjs \
    && myst --version > /dev/null

# Python-Pakete: **keine**. Der Buch-Bau braucht keines -- `myst build --html` fuehrt die
# Notebooks nicht aus (die Outputs sind gespeichert), und minted v3 holt sein Pygments aus
# dem gebuendelten Wheel des latexminted-Helfers. Die beiden Skripte, die in diesem Image
# laufen (_site/vendor/install_template.py, devnotes/check_pdf_build.py), sind reine
# Standardbibliothek. Die Projektabhaengigkeiten stehen in pyproject.toml/uv.lock und
# gehoeren zur Arbeit am Buch, nicht zu seinem Bau.
