# CLAUDE.md — Arbeitsanweisungen für dieses Repository

Dieses Repository enthält das Skript zur Vorlesung **„Einführung in Deep Learning“** (EiDL)
im Bachelor Informatik an der Heinrich-Heine-Universität Düsseldorf, gebaut mit
[MyST](https://mystmd.org/), dazu die Beamer-Foliensätze zur Vorlesung. Die Datei
beschreibt, wie in diesem Projekt gearbeitet wird; sie richtet sich an Coding-Agenten und
an Menschen gleichermaßen (`CLAUDE.md` und `AGENTS.md` sind dieselbe Konvention unter
verschiedenen Namen — sollte ein Werkzeug `AGENTS.md` erwarten, genügt ein Symlink).

**Wo was steht.** Diese Datei: wie hier gearbeitet wird. `devnotes/TODO.md`: was offen ist,
mit Einstieg für einen frischen Durchgang ganz oben. `devnotes/build-log-<datum>.md`: datierte
Protokolle größerer Umbauten, mit Messwerten. `devnotes/README.md`: was sonst in `devnotes/`
liegt.

**CI, Image und Build-Infrastruktur: `~/Sciebo/hhu/PLAYBOOK.md`.** Dort stehen die Regeln,
die für alle drei Bücher (`eipy-skript`, `eidl-skript`, `ds-skript`) gelten — Anheften,
Image-Bau, mitgeliefertes Site-Template, PDF-Verifikation. Diese Datei bleibt beim Buch,
das Playbook bei der Familie. Eine Lehre aus diesem Repo wird am selben Tag dort
eingetragen. **Für die Foliensätze gilt dasselbe mit `~/Sciebo/hhu/PLAYBOOK-folien.md`**
(seit 2026-10-02): Header, Bau, Notizenfassung, Prüfliste vor dem Upload nach ILIAS; was
nur dieses Repo betrifft, steht in `slides/README.md`.

## Was dieses Projekt ist

Ein Lehrbuch für Studierende der Informatik im Bachelor, die das Modul **Data Science**
gehört haben: rudimentäre Python-Kenntnisse, NumPy, lineare Regression werden vorausgesetzt,
Stochastik wird ins [Data-Science-Skript](https://voelkel.pages.cs.uni-duesseldorf.de/ds-skript/)
verlinkt statt wiederholt. Gegliedert nach **Themen, nicht nach Vorlesungswochen** — der
Semesterplan steht getrennt in `kurs-2026-27.md`.

## Bauen und Prüfen

```sh
uv sync                                   # Abhängigkeiten aus pyproject.toml/uv.lock
uv run --no-project devnotes/patch_myst_tex.py       # **nach jedem `uv sync`**, sonst ist das PDF kaputt
uv run --no-project _site/vendor/install_template.py # Site-Template bereitlegen (idempotent)
uv run --only-group dev myst build --html # Website nach _build/html
uv run --only-group dev myst build --pdf  # PDF nach exports/eidl-skript.pdf (braucht LaTeX)
uv run --no-project devnotes/check_pdf_build.py --min-pages 100  # prüft das gebaute PDF
uv run --only-group dev devnotes/check_ci_yaml.py    # vor jedem Push, wenn .gitlab-ci.yml angefasst wurde
uv run --no-project devnotes/check_doku.py           # prüft diese Datei und devnotes/ gegen das Repo
uv run --only-group figures devnotes/make_figures.py # Abbildungen nach images/ (nie mit System-Python)
```

**`--no-project` ist kein Schmuck.** Vier der fünf Skripte hier brauchen nur die
Standardbibliothek; ohne den Schalter synchronisiert `uv run` vorher die ganze
Default-Gruppe – torch, triton, scipy, rund ein Gigabyte – für ein Skript, das `re` und
`pathlib` importiert. Im eingerichteten Arbeitsverzeichnis merkt man das nicht, in einem
frischen Klon oder Worktree schon. Die CI ruft dieselben Skripte deshalb schlicht mit
`python3` auf. Einzige Ausnahme ist `check_ci_yaml.py`: Es braucht `pyyaml` und damit die
dev-Gruppe.

**Für `make_figures.py` gilt das Gegenteil, und zwar aus demselben Grund.** Es braucht
matplotlib, numpy, scipy, scikit-learn — und weil seine Ausgabe, die PNGs in `images/`,
**versioniert** ist, braucht es jedes Mal *dieselbe* Fassung davon. matplotlib ändert
zwischen Minor-Fassungen den Satz; ein Komplettlauf mit einer anderen Fassung schreibt alle
34 Abbildungen neu, ohne dass sich an einer einzigen etwas Inhaltliches geändert hätte, und
die echte Änderung ist dann nicht mehr von der Fassungsdifferenz zu unterscheiden. Bis zum
2026-10-14 stand im Skriptkopf „System-Python reicht“; dessen matplotlib (3.10.9) war eine
andere als die angeheftete (3.11.2), und genau das ist passiert. Die Gruppe `figures` in
`pyproject.toml` heftet die Fassungen an und enthält **kein** torch, der Lauf kostet also
trotzdem keine Gigabyte. Gegenprobe: zweimal laufen lassen, der zweite Lauf muss
byte-gleich sein.

Erwartung eines gesunden Laufs (Stand 2026-10-14, nach der fachlichen Durchsicht
aller 27 Kapitel und des Glossars): HTML ohne Warnungen, PDF **113 Seiten A4**, 0 LaTeX-Fehler, 0 fehlende
Glyphen, 5 überlange Zeilen. Die `--min-pages`-Untergrenze
soll einen *abgebrochenen* Lauf fangen, nicht eine gewollte Kürzung — sie steht deshalb
deutlich unter der tatsächlichen Seitenzahl, in der CI auf demselben Wert.

**Die Abweichung zwischen lokal und CI ist weg (2026-10-14).** Vom 2026-09-29 bis dahin
stand hier: lokal 112 Seiten, veröffentlicht 113, erste Abweichung auf Seite 29 mitten in
einem Codeblock — also der *Satz*, nicht der Inhalt. Als Ursache war die Toolchain
vermutet: Das CI-Image heftet texlive über einen Debian-Snapshot an, diese Maschine hat,
was Debian gerade liefert, und `minted` brach eine Codezeile eine Spalte anders um. Das
hat sich bestätigt — Debian ist nachgezogen, und der lokale Bau liefert jetzt dieselben
**113 Seiten** wie die CI. Nachgemessen am 2026-10-14 in einem `git worktree` auf
unverändertem HEAD, eben damit die Zahl nicht einer gleichzeitigen Änderung zugeschrieben
wird. Wer die veröffentlichte Zahl braucht, holt sie mit dem `curl`-Rezept weiter unten.

Die Lehre daran ist nicht die Zahl, sondern die Methode: **Eine Seitenzahl, die sich
„von selbst“ ändert, gehört gegen einen unveränderten Baum gemessen, bevor man sie der
eigenen Änderung zuschreibt** — oder man schreibt eine Toolchain-Bewegung in die
Änderungsnotiz und sucht den Fehler später an der falschen Stelle.

`patch_myst_tex.py` repariert zwei Fehler im LaTeX-Export von mystmd. Der erste: Codeblöcke werden
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

`check_doku.py` vergleicht, was die Dokumentation behauptet, mit dem, was da ist: Pfade,
Kapitel- und Übungszahlen, Seitenzahl, `--min-pages` hier und in der CI, die Vollständigkeit
von `devnotes/README.md`, und die Regeln, die im Buch gelten (keine Blattnummern, keine
Lösungen, keine Unicode-Pfeile). Er ist entstanden, weil diese Datei an einem einzigen Tag
drei falsche Angaben angesammelt hatte, ohne dass irgendetwas rot geworden wäre. Wer eine
Zahl hier bewusst ändert, ändert sie dort mit — oder der Prüfer meldet sich.

**Vor jedem Abschluss einer inhaltlichen Änderung**: `myst build --html` laufen lassen und
die Warnungen ansehen. Neue Warnungen sind ein Fehler in der Änderung, nicht
Hintergrundrauschen — insbesondere `Cross-reference target not found` bedeutet einen
kaputten Link. Und **nach dem Push nachsehen, dass es auch veröffentlicht wurde**: „lokal
grün“ und „veröffentlicht“ sind zwei verschiedene Aussagen.

**Wie man das nachsieht, ohne Zugang zur Pipeline.** Das GitLab-Projekt ist öffentlich
lesbar, die Pipeline-API aber nicht (`/api/v4/projects/voelkel%2Feidl-skript/pipelines`
antwortet mit 403), und ein Token liegt hier nicht. Wer keinen Browser-Zugang hat, prüft
deshalb das **Ergebnis** statt des Laufs:

```sh
U=https://eidl-skript-131e30.pages.cs.uni-duesseldorf.de
curl -s -o /tmp/live.pdf $U/eidl-skript.pdf && pdfinfo /tmp/live.pdf | grep Pages
curl -s $U/myst.xref.json | python3 -c 'import json,sys
d=json.load(sys.stdin)["references"]; print(sum(1 for r in d if r.get("kind")=="page"), "Seiten")'
```

Ein Deploy braucht nach dem Push typischerweise zwei bis fünf Minuten, mit Image-Bau länger.
**Auf einen Inhaltsmarker warten, nicht auf die Prüfsumme** — zwischendurch laufen Pipelines
durch, die ein byte-verschiedenes, inhaltsgleiches PDF erzeugen. Und der Marker darf keinen
Zeilenumbruch enthalten können: `pdftotext` zerlegt lange Sätze, ein Wächter auf „Praktisch
heißt das“ wäre am 2026-09-27 nie fertig geworden. Eine Seitenzahl oder ein einzelnes Wort
ist der bessere Marker.

Wichtig zur Ordnerstruktur:

* `_site/` ist **Quellcode** (eigenes CSS, Navbar-Fragmente, und unter `_site/vendor/` das
  mitgelieferte Site-Template).
* `_build/`, `exports/` und `public/` sind **Artefakte** — nie von Hand bearbeiten,
  gitignored.
* `devnotes/` sind Arbeitsnotizen des Autors, nicht Teil des Buchs (nicht im TOC).
  `devnotes/README.md` sagt, welche Datei wofür da ist; `devnotes/TODO.md` ist die eine
  Liste offener Punkte.
* `transcripts/` (Vorlesungsaufzeichnungen 2025/26) und `uebungen-2025/` (die zwölf
  Übungsblätter samt Lösungsvorschlägen) sind gitignored und liegen nur in Sciebo. **Das
  Repository ist öffentlich** — was hier landet, ist im Netz.

## Aufbau

| Ordner | Inhalt |
|---|---|
| `part-grundlagen/` | Kapitel 01–05: Was ist Deep Learning, Neuron/Perzeptron, Training, vortrainierte Modelle, Tensoren |
| `part-lernen/` | Kapitel 06–13: logistische Regression, Loss und Maximum Likelihood, Gradientenabstieg, Backprop, Autograd, Aktivierungen, Netze von Hand, universelle Approximation |
| `part-representation-learning/` | Kapitel 14–19: Autoencoder, VAE, word2vec, Graphen, RNN, Transformer |
| `part-architekturen-anwendungen/` | Kapitel 20–27: CNN, LLMs benutzen, GANs, latente Räume, Anwendungen, Destillation, Optimierer, Adversarial Attacks |
| `slides/` | Beamer-Foliensätze VL 01–15 (`build.sh`, gemeinsamer `header.tex`) |
| `images/`, `logo/` | Abbildungen, Logos |
| `notebooks/` | Notebooks aus 2025; nur `latent-classifier.ipynb` hat noch eine Funktion — es hängt als `downloads:` am Kapitel 21 |
| `glossar.md` | Klausurbegriffe mit Link ins jeweilige Kapitel (im TOC, Abschnitt „Anhang“) |
| `kurs-2026-27.md` | Semesterplan, Termine, Organisatorisches — **nicht im TOC**, also nicht Teil des Buchs |
| `uebungen-2025/` | die zwölf Blätter von 2025 samt Lösungen; gitignored, Quelle für neue Übungsabschnitte |

Das Inhaltsverzeichnis steht **explizit** in `myst.yml` unter `project.toc`. Eine neue Datei
erscheint erst nach einem Eintrag dort.

## Schreibstil

Der Ton ist knapp und präzise:

* **Deutsch**, Fachbegriffe englisch, wo sie englisch gebräuchlich sind (*Loss*, *Embedding*,
  *Stride*). Keine Eindeutschung um jeden Preis.
* **Englische Stämme mit deutscher Flexion bleiben stehen** — das ist entschieden, nicht
  Versehen: `sampeln` (nicht *samplen*), `finetunen`/`gefinetunt`, `fittet`/`gefittet`,
  `labeln`/`gelabelte`, `overfittet`, `flippen`, `quantisierte`, `Tokenisiere`. Gezählt am
  2026-09-29: 300 Vorkommen in 54 Formen. Eine Eindeutschung („feinabstimmen“) wäre
  schlechter, und `sampeln` ist die Form, die der Duden führt. **Nicht neu verhandeln.**
* **Der Gedankenstrich ist der Halbgeviertstrich `–` mit Spatien.** Der Geviertstrich `—`
  ist die englische Form. **Gilt für alles, was veröffentlicht wird:** die Kapitel,
  `glossar.md`, `index.md` und die Foliensätze (dort ist `--` der Halbgeviertstrich und
  `---` der Geviertstrich), dazu `BRANDING.md` und `slides/README.md`. Am 2026-09-29
  ersetzt: 14 im Buch, 316 in den Decks. `sprachpruefliste.py` und `folienpruefliste.py`
  halten Buch und Folien auf null, samt `--` als ASCII-Notbehelf im Fließtext.

  **Nicht** betroffen sind die Arbeitsnotizen: diese Datei und `devnotes/` benutzen den
  Geviertstrich seit Anfang an (59 Stellen am 2026-09-29) und behalten ihn. Wer das
  ändern will, ändert es als eigene Entscheidung, nicht als Nebenwirkung — und dann in
  einem Rutsch.
* **Vor „und“ und „oder“ steht in einer Aufzählung kein Komma.** Auch nicht bei
  nachgetragenen Gliedern („… sein oder ReLU.“) — am 2026-09-29 für alle zehn Stellen so
  entschieden. `devnotes/grammatikpruefung.py` meldet Rückfälle (`KOMMA_VOR_UND_ODER`).
* **`z.B.`, `d.h.`, `i.d.R.` ohne Leerzeichen**, wie im ganzen Buch (94 Stellen). Und die
  vier Stellen mit `?!?`, `??`, `!!`, `???` sind Absicht — dort soll der Text wachrütteln.
* **Keine Adjektiv-Inflation.** Nicht „ein extrem mächtiges, unglaublich flexibles
  Verfahren“, sondern was es tut und wann man es nimmt.
* **Jede Behauptung belegbar.** Formeln nachrechnen, Paper mit Jahr und Titel nennen,
  Bibliotheksversionen prüfen statt erinnern.
* Rechenbeispiele werden **durchgerechnet**, nicht behauptet. Wer eine Zahl ändert, rechnet
  die Folgezahlen nach.
* Vertiefungen, die nicht Vorlesungsstoff sind, stehen in einer Box
  `:::{admonition} Vertiefung: …` mit `:class: note dropdown` (derzeit sechs; dazu eine
  Antwortenbox in Kapitel 01, zusammen sieben `dropdown`-Boxen).
  **Aufgeklappt wird nur im HTML**: `dropdown` hat im LaTeX-Export keine Wirkung, im PDF
  steht der Inhalt offen da. Für Vertiefungen ist das in Ordnung — für alles, was erst nach
  eigenem Nachdenken gelesen werden soll, ist `dropdown` kein Versteck. Genau daran hingen
  bis zum 2026-09-27 die Lösungsvorschläge der Übungsblätter im PDF.

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
  Template lädt deshalb `hyphenat` mit `htt` und gibt LaTeX 3 em `emergencystretch`; am Tag
  der Änderung brachte das 21 → 9 überlange Zeilen, aktuell sind es 5. Codeblöcke sind davon
  nicht betroffen, dort trennt ohnehin nichts.
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
* **Zwei Währungs-`$` in einer Datei öffnen Mathemodus.** Ein einzelnes `$` am Zeilenende
  lässt MyST als Text stehen (`\$` in der `.tex`), zwei aber paart es zu Inline-Mathematik —
  und dann meldet der HTML-Bau `unicodeTextInMathMode` für jeden Umlaut dazwischen, während
  der Satz im PDF in Mathe-Kursive erscheint. Passiert beim Einfügen einer zweiten Geldsumme
  in ein Kapitel, das schon eine hat (2026-09-27 in `04-vortrainierte-modelle.md`).
  Abhilfe: „US-Dollar“ ausschreiben, wie in Kapitel 20.
* **jtex ersetzt seine Marken auch in LaTeX-Kommentaren.** Wer den Namen des
  Import-Platzhalters in einen `%`-Kommentar von `templates/tex/eidl-skript/template.tex`
  schreibt, bekommt den ganzen Import-Block ein zweites Mal in die `.tex` — elf „already
  defined“-Fehler, ein kaputtes PDF, kein Wort im HTML.

## Querverweise

Verwiesen wird mit einem **relativen Pfad auf die Datei**, in der Form
`[Kapitel „Neuron und Perzeptron“](../part-grundlagen/02-neuron-perzeptron.md)`. Keine
absoluten URLs auf die eigene Pages-Domain, und keine Nummern: weder Kapitel- noch
Blattnummern, die sich jedes Semester verschieben (dieselbe Regel hält `slides/README.md`
für die Folien fest — beim Herausnehmen der Übungsblätter am 2026-09-27 liefen fünfzehn
solche Verweise ins Leere).

Explizite Anker (`(name)=` vor der Überschrift, Verweis mit `[Text](#name)`) benutzt dieses
Repository **nicht** — die Überschriften bekommen ihre Anker von MyST. Wer damit anfängt,
fängt für das ganze Buch an, nicht für ein Kapitel.

## Übungen

Jedes Kapitel, dem eine sinnvolle Aufgabe zuzuordnen ist, endet mit einem Abschnitt
`## Übung` **vor** der „Weiterlesen“-Box. 23 der 27 Kapitel haben einen; 04, 17, 21 und 22
haben bewusst keinen, weil eine schwache Übung schlechter ist als keine. Die Form:

* **Ein bis drei Aufgaben**, mit Papier in fünf bis fünfzehn Minuten zu schaffen. Keine
  Programmieraufgaben — die gehören auf die echten Übungsblätter (TeX, ILIAS).
* **Ein `Tipp:` je Aufgabe**, der den ersten Schritt verrät. Hier liest jemand allein.
* **Keine Lösung.** Statt dessen eine *Antwortprobe* als letzter Absatz: eine nachprüfbare
  Zahl oder Eigenschaft („die Summe muss 1 ergeben“, „genau eine der drei Größen ändert
  sich“), an der man selbst merkt, ob man richtig liegt.
* **Zahlen werden nachgerechnet**, nicht geschätzt — beim ersten Entwurf stimmten fünf
  Antwortproben nicht.

## Bewusste Entscheidungen — nicht ändern

1. **Die Übungsblätter gehören nicht ins Skript.** Sie werden in TeX gepflegt und über
   ILIAS ausgegeben; im Buch standen sie in einer zweiten, veraltenden Fassung — samt
   Lösungsvorschlägen, die damit veröffentlicht waren. Seit dem 2026-09-27 sind sie aus dem
   TOC und aus dem Repository (`uebungen-2025/`, gitignored). Ins Skript kommt statt dessen
   pro Kapitel ein kleiner Übungsabschnitt: Varianten der echten Aufgaben, mit mehr
   Hinweisen, **ohne Lösung** — statt dessen eine nachprüfbare Antwortprobe. Die Form steht
   oben unter „Übungen“; das Material von 2025, aus dem sie entstanden sind, liegt in
   `uebungen-2025/` (gitignored).
2. **Gliederung nach Themen, nicht nach Vorlesungswochen.** Der Wochenplan steht in
   `kurs-2026-27.md`, die Folien in `slides/`; das Skript bleibt davon unabhängig.
3. **Die Notebooks aus 2025 sind nicht im TOC.** Ihre Inhalte sind in die Kapitel übernommen
   (siehe `notebooks/README.md`); `latent-classifier.ipynb` hängt seit 2026-09-27 als
   `downloads:` am Kapitel „LLMs benutzen“ (21) und ist das einzige mit noch aktiver Rolle.
4. **Die Kapitel sind nicht gleich lang** und sollen es nicht werden.
5. **Das Image installiert kein einziges Python-Paket.** Der Buch-Bau braucht keines: Die
   Notebooks werden nicht ausgeführt (Outputs sind gespeichert), und minted holt sein
   Pygments aus dem gebündelten Wheel des `latexminted`-Helfers. Die Projektabhängigkeiten
   in `pyproject.toml`/`uv.lock` gehören zur **Arbeit am** Buch, nicht zu seinem Bau. Wer
   sie ins Image zieht, wiederholt einen Fehler, der `eipy-skript` auf 3,5 GB gebracht hat.
6. **Das Template trägt nur Familien-Gemeingut, `myst.yml` das Buchspezifische.** Im
   `templates/tex/eidl-skript/template.tex` steht, was für jedes deutschsprachige Skript
   der Familie gilt (Sprache, A4, Schriften, Überschriften); Markenfarbe, PDF-Metadaten
   und `\setminted` stehen in `options.preamble` in der `myst.yml`. Damit bleibt der
   Template-Block zwischen den Büchern kopierbar (PLAYBOOK §3.8i). Wer dort eine neue
   Option einführt, **deklariert sie in `template.yml`** — jtex verwirft undeklarierte
   Optionen kommentarlos, ohne Warnung und ohne Fehler.
7. **`latexminted` kommt nicht aus PyPI.** Debians texlive liefert minted v3 samt passendem
   Helfer; die PyPI-Fassung verdeckt ihn und verlangt eine neuere `minted.sty`. Steht
   ausführlich im Dockerfile.
8. **Markenfarbe `#6f59a6`** (violett) laut `BRANDING.md`; HHU-Hausfarben bleiben die
   Abbildungsfarben.

## Häufige Fehlerquellen in diesem Repository

* **Eine Lösung in einen Übungsabschnitt geschrieben.** Sie steht dann im veröffentlichten
  PDF und auf der Website — `:class: dropdown` wirkt im LaTeX-Export nicht. Gegenprobe vor
  dem Push:

  ```sh
  grep -rn --include='*.md' -oE 'Lösungsvorschlag|(Übungs)?[Bb]latt ?[0-9]+' part-*
  ```

  muss leer bleiben (der zweite Teil fängt Verweise auf Blattnummern ab, die es nicht mehr
  gibt).
* **Eine Gegenprobe mit Kontext links und rechts geschrieben.** `grep -oE '.{25}X.{25}'`
  findet einen Treffer **nicht**, wenn er am Zeilenende steht — die 25 Zeichen danach fehlen
  ja. So haben drei Blatt-Verweise zwei Prüfungen überlebt und standen im veröffentlichten
  PDF. Ohne Kontextbreite suchen, dann mit `-o` nur den Treffer ausgeben.
* **Ein Umbau-Skript aus der Entstehungszeit wiederbeleben.** `build_skript_from_2025.py` und
  `restructure.py` haben am 2026-09-17 die erste Fassung erzeugt und geschnitten; sie sind am
  2026-09-27 gelöscht worden, weil ein zweiter Lauf das Repo zurückgedreht hätte —
  `part-exercises/` samt Lösungen neu anlegen bzw. die heutigen Kapitel mit einer alten
  Fassung überschreiben. In der Historie stehen sie noch (`git log -- devnotes/`). Wer so
  etwas Neues schreibt: nicht ins Repo legen, oder mit einer Sperre versehen.
* Eine neue Datei angelegt und den `myst.yml`-Eintrag vergessen — sie taucht dann nicht auf.
* **Einen relativen Link auf eine Datei gesetzt, die es nicht (mehr) gibt.** Der HTML-Build
  meldet `Cross-reference target not found`; im PDF sieht der Text unauffällig aus.
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
  **kein einziger** Job, auch keine Prüfung. `uv run --only-group dev devnotes/check_ci_yaml.py` vor dem Push.
* **`uv sync` gemacht und den mystmd-Patch vergessen.** Dann sind alle Kommandozeilen im
  lokal gebauten PDF falsch, und zwar unauffällig.
