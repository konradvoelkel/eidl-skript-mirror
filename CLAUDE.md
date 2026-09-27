# CLAUDE.md — Arbeitsanweisungen für dieses Repository

Dieses Repository enthält das Skript zur Vorlesung **„Einführung in Deep Learning“** (EiDL)
im Bachelor Informatik an der Heinrich-Heine-Universität Düsseldorf, gebaut mit
[MyST](https://mystmd.org/), dazu die Beamer-Foliensätze zur Vorlesung. Die Datei
beschreibt, wie in diesem Projekt gearbeitet wird; sie richtet sich an Coding-Agenten und
an Menschen gleichermaßen (`CLAUDE.md` und `AGENTS.md` sind dieselbe Konvention unter
verschiedenen Namen — sollte ein Werkzeug `AGENTS.md` erwarten, genügt ein Symlink).

**CI, Image und Build-Infrastruktur: `~/Sciebo/hhu/PLAYBOOK.md`.** Dort stehen die Regeln,
die für alle drei Bücher (`eipy-skript`, `eidl-skript`, `ds-skript`) gelten — Anheften,
Image-Bau, mitgeliefertes Site-Template, PDF-Verifikation. Diese Datei bleibt beim Buch,
das Playbook bei der Familie. Eine Lehre aus diesem Repo wird am selben Tag dort
eingetragen.

## Was dieses Projekt ist

Ein Lehrbuch für Studierende der Informatik im Bachelor, die das Modul **Data Science**
gehört haben: rudimentäre Python-Kenntnisse, NumPy, lineare Regression werden vorausgesetzt,
Stochastik wird ins [Data-Science-Skript](https://voelkel.pages.cs.uni-duesseldorf.de/ds-skript/)
verlinkt statt wiederholt. Gegliedert nach **Themen, nicht nach Vorlesungswochen** — der
Semesterplan steht getrennt in `kurs-2026-27.md`.

## Bauen und Prüfen

```sh
uv sync                                   # Abhängigkeiten aus pyproject.toml/uv.lock
uv run devnotes/patch_myst_tex.py         # **nach jedem `uv sync`**, sonst ist das PDF kaputt
uv run _site/vendor/install_template.py   # Site-Template bereitlegen (idempotent)
uv run --only-group dev myst build --html # Website nach _build/html
uv run --only-group dev myst build --pdf  # PDF nach exports/eidl-skript.pdf (braucht LaTeX)
uv run devnotes/check_pdf_build.py --min-pages 120   # prüft das gebaute PDF
uv run devnotes/check_ci_yaml.py          # vor jedem Push, wenn .gitlab-ci.yml angefasst wurde
```

`patch_myst_tex.py` repariert einen Fehler im LaTeX-Export von mystmd: Codeblöcke werden
dort als Mathematik escaped, wodurch **vor jedem Bindestrich ein Leerzeichen** landet — aus
`nvidia-smi` wird `nvidia -smi`, aus `--index-url` wird `- -index -url`. Im HTML passiert
das nicht, nur im PDF, und es traf 49 Stellen in 18 Kapiteln. Im CI-Image geschieht der
Patch automatisch (Dockerfile), in einer frisch synchronisierten `.venv` nicht. Das Skript
ist idempotent und scheitert laut, wenn mystmd sich bewegt hat.

Das Site-Template ist **mitgeliefert** (`_site/vendor/book-theme.zip`) und wird von
`install_template.py` an die Stelle entpackt, an der MyST es zwischenspeichert. Ohne diesen
Schritt lädt `myst build` es bei jedem Lauf von einem *wandernden Branch* bei GitHub — das
macht das Aussehen der Seite zu einer unversionierten Abhängigkeit und den Build von einer
Netzverbindung abhängig. Ein lokaler Pfad in `myst.yml` funktioniert für `site.template`
**nicht**; für das tex-Template unter `templates/tex/eidl-skript` funktioniert er sehr wohl,
und deshalb liegt das einfach im Repo. Begründung und Aktualisierungsweg:
`_site/vendor/README.md`.

**Vor jedem Abschluss einer inhaltlichen Änderung**: `myst build --html` laufen lassen und
die Warnungen ansehen. Neue Warnungen sind ein Fehler in der Änderung, nicht
Hintergrundrauschen — insbesondere `Cross-reference target not found` bedeutet einen
kaputten Link. Und **nach dem Push die Pipeline ansehen**, bis zum `pages`-Job: „lokal grün“
und „veröffentlicht“ sind zwei verschiedene Aussagen.

Wichtig zur Ordnerstruktur:

* `_site/` ist **Quellcode** (eigenes CSS, Navbar-Fragmente, und unter `_site/vendor/` das
  mitgelieferte Site-Template).
* `_build/`, `exports/` und `public/` sind **Artefakte** — nie von Hand bearbeiten,
  gitignored.
* `devnotes/` sind Arbeitsnotizen des Autors, nicht Teil des Buchs (nicht im TOC).
  `devnotes/README.md` sagt, welche Datei wofür da ist; `devnotes/TODO.md` ist die eine
  Liste offener Punkte.
* `transcripts/` (Vorlesungsaufzeichnungen 2025/26) ist gitignored und liegt nur in Sciebo.

## Aufbau

| Ordner | Inhalt |
|---|---|
| `part-grundlagen/` | Kapitel 01–05: Was ist Deep Learning, Neuron/Perzeptron, Training, vortrainierte Modelle, Tensoren |
| `part-lernen/` | Kapitel 06–13: logistische Regression, Loss und Maximum Likelihood, Gradientenabstieg, Backprop, Autograd, Aktivierungen, Netze von Hand, universelle Approximation |
| `part-representation-learning/` | Kapitel 14–19: Autoencoder, VAE, word2vec, Graphen, RNN, Transformer |
| `part-architekturen-anwendungen/` | Kapitel 20–27: CNN, LLMs benutzen, GANs, latente Räume, Anwendungen, Destillation, Optimierer, Adversarial Attacks |
| `part-exercises/` | Übungsblätter 0–11 |
| `slides/` | Beamer-Foliensätze VL 01–15 (`build.sh`, gemeinsamer `header.tex`) |
| `images/`, `notebooks/`, `logo/` | Abbildungen, Notebooks aus 2025, Logos |
| `glossar.md` | Klausurbegriffe mit Link ins jeweilige Kapitel |
| `kurs-2026-27.md` | Semesterplan, Termine, Organisatorisches |

Das Inhaltsverzeichnis steht **explizit** in `myst.yml` unter `project.toc`. Eine neue Datei
erscheint erst nach einem Eintrag dort.

## Schreibstil

Der Ton ist knapp und präzise:

* **Deutsch**, Fachbegriffe englisch, wo sie englisch gebräuchlich sind (*Loss*, *Embedding*,
  *Stride*). Keine Eindeutschung um jeden Preis.
* **Keine Adjektiv-Inflation.** Nicht „ein extrem mächtiges, unglaublich flexibles
  Verfahren“, sondern was es tut und wann man es nimmt.
* **Jede Behauptung belegbar.** Formeln nachrechnen, Paper mit Jahr und Titel nennen,
  Bibliotheksversionen prüfen statt erinnern.
* Rechenbeispiele werden **durchgerechnet**, nicht behauptet. Wer eine Zahl ändert, rechnet
  die Folgezahlen nach.
* Vertiefungen, die nicht Vorlesungsstoff sind, stehen in einer aufklappbaren Box
  „Vertiefung: …“ (`:class: dropdown`).

## Markup — die Fallen dieses Repos

Die Übungsblätter und Teile der Prosa sind 2026-09 aus den Beamer-Folien und Pandoc-Quellen
von 2025 konvertiert worden. Die Konversion hat mehrere Dinge liegen lassen, die alle
dieselbe Form haben: **Es sieht im HTML unauffällig aus und ist trotzdem falsch.**

* **`::: name` ohne geschweifte Klammern ist kein Directive, sondern ein Codefence.** MyST
  liest `::: proof` als Codeblock mit der „Sprache“ `proof` — der Beweistext stand dann als
  roher Markdown-Quelltext im Buch. Richtig ist `:::{admonition} Beweis` (gefunden und
  behoben in `eidl2026blatt00.md`, 2026-09-27).
* **Gleich tiefe `:::` schachteln nicht.** Ein `:::{admonition}` innerhalb eines
  `:::{admonition}` schließt das äußere; das nächste `:::` eröffnet einen Codefence, der
  alles bis zum übernächsten verschluckt — in blatt00 waren das eine `##`-Überschrift und
  eine ganze Definition. Innen weniger Doppelpunkte als außen (`::::` außen, `:::` innen)
  oder, besser, gar nicht schachteln.
* **`a)` ist kein Listenmarker.** CommonMark kennt nur `1.` und `1)`. Ein Aufgabenpunkt
  `a)  …` ist also ein gewöhnlicher Absatz, und alles, was darunter vier Leerzeichen
  eingerückt steht, wird ein **Codeblock**. So wurden in blatt10 fünf Tabellen zu
  ASCII-Kunst. Tabellen und Codeblöcke unter `a)`-Punkten gehören in Spalte 0.
* **Ein Codeblock ohne Sprache bricht den PDF-Bau.** Seit `code_style: minted` erzeugt MyST
  daraus `\begin{minted}[breaklines]{}`, und minted bricht mit „Missing Pygments output“ ab.
  Jeder Codeblock bekommt eine Sprache (`python`, `bash`, notfalls `text`). Das ist Absicht:
  Der Fehler ist laut statt still.
* **Kein `→` und keine anderen Unicode-Pfeile im Fließtext.** MyST übersetzt sie nach
  `\rightarrow`, einem Mathe-Modus-Befehl; in einer Tabellenzelle bricht der LaTeX-Lauf daran
  ab, und dann fehlt **alles danach** im PDF, ohne dass das HTML etwas meldet. Schreiben Sie
  „zu“, „wird“, „dann“, „nach“. (In diesem Repo derzeit sauber — bitte so lassen.)
* **Lange Bezeichner im Fließtext laufen in den Rand.** LaTeX sucht in `\texttt` keine
  Trennstelle, also bleibt `torch.backends.mps.is_available()` in einer Zeile. Das
  Template lädt deshalb `hyphenat` mit `htt` und gibt LaTeX 3 em `emergencystretch`
  (überlange Zeilen 21 → 9). Codeblöcke sind davon nicht betroffen, dort trennt
  ohnehin nichts.
* **`?“` wird im PDF zu `?¿`.** MyST übersetzt das schließende deutsche
  Anführungszeichen in die TeX-Schreibweise mit zwei Accent-graves; direkt hinter einem
  Fragezeichen bildet XeLaTeX daraus die Ligatur `¿`. In diesem Buch neunmal, gefunden
  beim Lesen des eigenen PDF. `devnotes/patch_myst_tex.py` repariert das mit; wer die
  `.venv` neu aufsetzt und den Patch vergisst, bekommt es zurück.
* **`##` wird zu `\paragraph`, und `\paragraph` ist in `article` ein run-in-Titel.** Er
  erscheint erst dort, wo der nächste gewöhnliche Absatz beginnt — folgt auf die
  Überschrift sofort eine Merkbox, ein Codeblock oder eine Liste, wandert der Titel an
  dieser vorbei und steht *hinter* seinem eigenen Abschnitt (76 von 979 Überschriften,
  2026-09-27). Das tex-Template macht `\paragraph` und `\subparagraph` deshalb zu
  Überschriften auf eigener Zeile. Wer das rückgängig machen will, löscht dort den
  `\makeatletter`-Block — dann kommen die 76 wandernden Titel zurück.
* **jtex ersetzt seine Marken auch in LaTeX-Kommentaren.** Wer den Namen des
  Import-Platzhalters in einen `%`-Kommentar von `templates/tex/eidl-skript/template.tex`
  schreibt, bekommt den ganzen Import-Block ein zweites Mal in die `.tex` — elf „already
  defined“-Fehler, ein kaputtes PDF, kein Wort im HTML.

## Querverweise

Anker werden explizit gesetzt, als eigene Zeile vor der Überschrift:

```markdown
(backpropagation)=
### Backpropagation
```

Verwiesen wird mit `[Text](#backpropagation)` innerhalb des Projekts (funktioniert über
Dateigrenzen hinweg) oder mit einem relativen Pfad auf eine Datei. Keine absoluten URLs auf
die eigene Pages-Domain.

## Bewusste Entscheidungen — nicht ändern

1. **Gliederung nach Themen, nicht nach Vorlesungswochen.** Der Wochenplan steht in
   `kurs-2026-27.md`, die Folien in `slides/`; das Skript bleibt davon unabhängig.
2. **Die Notebooks aus 2025 sind nicht im TOC.** Ihre Inhalte sind in die Kapitel übernommen
   (siehe `notebooks/README.md`); `latent-classifier.ipynb` hängt als Download an Blatt 11.
3. **Die Kapitel sind nicht gleich lang** und sollen es nicht werden.
4. **Das Image installiert kein einziges Python-Paket.** Der Buch-Bau braucht keines: Die
   Notebooks werden nicht ausgeführt (Outputs sind gespeichert), und minted holt sein
   Pygments aus dem gebündelten Wheel des `latexminted`-Helfers. Die Projektabhängigkeiten
   in `pyproject.toml`/`uv.lock` gehören zur **Arbeit am** Buch, nicht zu seinem Bau. Wer
   sie ins Image zieht, wiederholt einen Fehler, der `eipy-skript` auf 3,5 GB gebracht hat.
5. **Das Template trägt nur Familien-Gemeingut, `myst.yml` das Buchspezifische.** Im
   `templates/tex/eidl-skript/template.tex` steht, was für jedes deutschsprachige Skript
   der Familie gilt (Sprache, A4, Schriften, Überschriften); Markenfarbe, PDF-Metadaten
   und `\setminted` stehen in `options.preamble` in der `myst.yml`. Damit bleibt der
   Template-Block zwischen den Büchern kopierbar (PLAYBOOK §3.8i). Wer dort eine neue
   Option einführt, **deklariert sie in `template.yml`** — jtex verwirft undeklarierte
   Optionen kommentarlos, ohne Warnung und ohne Fehler.
6. **`latexminted` kommt nicht aus PyPI.** Debians texlive liefert minted v3 samt passendem
   Helfer; die PyPI-Fassung verdeckt ihn und verlangt eine neuere `minted.sty`. Steht
   ausführlich im Dockerfile.
7. **Markenfarbe `#6f59a6`** (violett) laut `BRANDING.md`; HHU-Hausfarben bleiben die
   Abbildungsfarben.

## Häufige Fehlerquellen in diesem Repository

* Eine neue Datei angelegt und den `myst.yml`-Eintrag vergessen — sie taucht dann nicht auf.
* Einen Link auf einen Anker gesetzt, den es nicht gibt. Der Build meldet das, der Text sieht
  trotzdem unauffällig aus.
* **PDF-Fehler mit `grep '^! '` zählen.** Latexmk läuft mit `-file-line-error`; Fehlerzeilen
  beginnen dann mit `./datei.tex:419:`. Richtig sind
  `grep -cE '^\./[^:]+\.tex:[0-9]+: '` und `grep -c 'That makes 100 errors'` — und zur
  Gegenprobe die **Seitenzahl** aus `Output written on …` gegen die Erwartung halten.
  `devnotes/check_pdf_build.py` macht all das, zählt zusätzlich `Missing character` (ein
  Zeichen ohne Glyphe fehlt im PDF **ersatzlos**, ohne Fehler und ohne Spur im HTML) und
  liest über `--myst-log` die Ausgabe von MyST auf Knoten, die es gar nicht erst übersetzt
  hat.
* **`.gitlab-ci.yml` geändert und nur die YAML-Syntax geprüft.** Ein `: ` in einem
  unquotierten Skalar macht aus einer Skriptzeile eine Map — die Datei bleibt **valides
  YAML**, GitLab lehnt sie aber ab (`script config should be a string`), und dann läuft
  **kein einziger** Job, auch keine Prüfung. `uv run devnotes/check_ci_yaml.py` vor dem Push.
* **`uv sync` gemacht und den mystmd-Patch vergessen.** Dann sind alle Kommandozeilen im
  lokal gebauten PDF falsch, und zwar unauffällig.
