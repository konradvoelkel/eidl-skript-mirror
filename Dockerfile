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

# Der apt-Teil **angeheftet**. Der Digest oben deckt ihn nicht ab: Die Pakete kommen erst
# im `RUN` dazu, also holt `apt-get install texlive-latex-extra` sonst das, was Debian am
# Bautag hat -- und genau daraus entstand in eipy-skript die Differenz zwischen minted v2
# (lokal) und minted v3 (Image), die 745 LaTeX-Fehler und einen Tag Suche gekostet hat.
#
# snapshot.debian.org liefert das Archiv zu einem Zeitpunkt. Das Basis-Image nennt seinen
# eigenen Stand als Kommentar in /etc/apt/sources.list.d/debian.sources (20260918T000000Z);
# hier steht bewusst ein spaeterer, naemlich der, gegen den dieses Image geprueft wurde.
#
# Anheben: Zeitstempel unten setzen, Image bauen, `myst build --pdf` und
# devnotes/check_pdf_build.py im Container laufen lassen, erst dann committen. Die Suiten
# muessen zur Debian-Version des Basis-Images passen (hier trixie = Debian 13).
#
# Stand 2026-09-27 mit diesem Zeitstempel: texlive-latex-extra 2024.20250309-2,
# texlive-lang-german 2024.20250309-1, poppler-utils 25.03.0-5+deb13u4,
# minted.sty v3.6.0 (2025/03/06), latexminted 0.5.0 mit Pygments 2.19.1.
ARG DEBIAN_SNAPSHOT=20260927T000000Z
RUN set -eu; \
    { \
      echo 'Types: deb'; \
      echo "URIs: https://snapshot.debian.org/archive/debian/${DEBIAN_SNAPSHOT}"; \
      echo 'Suites: trixie trixie-updates'; \
      echo 'Components: main'; \
      echo 'Signed-By: /usr/share/keyrings/debian-archive-keyring.pgp'; \
      echo ''; \
      echo 'Types: deb'; \
      echo "URIs: https://snapshot.debian.org/archive/debian-security/${DEBIAN_SNAPSHOT}"; \
      echo 'Suites: trixie-security'; \
      echo 'Components: main'; \
      echo 'Signed-By: /usr/share/keyrings/debian-archive-keyring.pgp'; \
    } > /etc/apt/sources.list.d/debian.sources; \
    # Ein Snapshot-Release ist per Definition abgelaufen -- das ist kein Fehler, sondern
    # der Punkt. Die Signaturpruefung bleibt unangetastet.
    echo 'Acquire::Check-Valid-Until "false";' > /etc/apt/apt.conf.d/99snapshot

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
#
# Seit dem 2026-11-04 kommen die Beamer-Decks dazu (`slides/*.tex`), und die bringen vier
# eigene Anforderungen mit: `texlive-luatex`, weil die Decks mit **LuaLaTeX** gebaut werden
# und nicht mit XeLaTeX wie das Buch; `texlive-pictures` fuer TikZ, das das HHU-Theme
# benutzt; `fonts-adobe-sourcesans3` als Schrift der Decks -- Debian trixie fuehrt genau die
# Fassung 3.052, die auch lokal in ~/.fonts liegt, unter SIL OFL, also ohne jede
# Lizenzfrage -- dazu `fontconfig`, denn luaotfload findet eine Schrift **ueber ihren
# Familiennamen** nur in der fontconfig-Datenbank, und ohne das Paket gibt es keine
# (am 2026-11-04 daran gescheitert: `fc-list: command not found`); und das HHU-Theme selbst, das **nicht** im Repository liegen darf (kein
# Lizenzvermerk, dazu das HHU-Logo) und deshalb unten aus einer Secure File kommt.
# `Acquire::Retries`: snapshot.debian.org antwortet unter Last mit 503 ("No healthy
# backends"), und ein einziges verfehltes .deb reisst den ganzen Bau mit -- am
# 2026-11-04 an `preview-latex-style` passiert, Job 674494. Fuenf Versuche je Paket
# kosten nichts und machen den Bau gegen die Launen des Spiegels unempfindlich.
RUN apt-get -o Acquire::Retries=5 update \
    && apt-get -o Acquire::Retries=5 install -y --no-install-recommends \
    procps \
    latexmk \
    texlive-xetex \
    texlive-luatex \
    texlive-latex-recommended \
    texlive-latex-extra \
    texlive-pictures \
    texlive-fonts-recommended \
    fonts-adobe-sourcesans3 \
    fontconfig \
    texlive-lang-german \
    fonts-dejavu-core \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

# Die fontconfig-Datenbank einmal bauen und **nachsehen, ob die Schrift drin ist**. Das
# Paket liefert 14 OTF nach /usr/share/fonts/opentype/sourcesans3/, aber der Cache, in dem
# luaotfload nach dem Familiennamen sucht, entsteht im Container nicht von selbst: Am
# 2026-11-04 war `fc-list` leer, und `build-slides` meldete die fehlende Schrift, obwohl
# die Dateien da lagen. Schlaegt die Probe fehl, soll der **Image-Bau** scheitern und nicht
# erst der Job, der das Image benutzt.
RUN fc-cache -f > /dev/null \
    && fc-list | grep -q "Source Sans 3" \
    && echo "Schrift da: $(fc-list | grep -c 'Source Sans 3') Schnitte"

# Das HHU-Beamer-Theme. Es liegt **bewusst nicht im Repository**: Es hat keinen
# Lizenzvermerk und keinen Autor, und sein `fig/` enthaelt das HHU-Logo -- ein Markenzeichen,
# dessen Weitergabe nicht uns gehoert. Das Repository wird nach GitHub gespiegelt und waere
# damit oeffentlich; die Registry dieses Projekts ist es nicht. Deshalb kommt das Theme als
# **Secure File dieses Projekts** in den Build-Kontext (siehe `build-image` in
# .gitlab-ci.yml) und von dort in das Image.
#
# Die eckigen Klammern in `hhubeamer.tar.g[z]` sind kein Tippfehler, sondern der uebliche
# Griff fuer ein *optionales* COPY: Fehlt die Datei, trifft das Muster nichts und der Bau
# laeuft weiter, statt mit "file not found" abzubrechen. Dann fehlt das Theme im Image, und
# der Job `build-slides` sagt genau das -- sichtbar, nicht still.
COPY ci/hhubeamer.tar.g[z] /tmp/
RUN set -eu; \
    if [ -f /tmp/hhubeamer.tar.gz ]; then \
      mkdir -p /usr/share/texmf/tex/latex/beamer/themes; \
      tar -xzf /tmp/hhubeamer.tar.gz -C /usr/share/texmf/tex/latex/beamer/themes; \
      rm -f /tmp/hhubeamer.tar.gz; \
      mktexlsr; \
      kpsewhich beamerthemehhubeamer.sty \
        && echo "hhubeamer: eingebaut"; \
    else \
      echo "hhubeamer: nicht im Kontext -- das Image kann keine Decks bauen"; \
    fi

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
RUN npm install -g mystmd@1.11.0

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
