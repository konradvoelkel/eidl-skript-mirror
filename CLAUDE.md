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
uv run --only-group figures devnotes/make_webp.py    # WebP-Fassung je verlinkter Abbildung, ab 700 px auch halb (nach jeder Bildänderung)
uv run devnotes/make_formen_daten.py      # rechnet vor, was torch braucht: Formen-Verteilung (~11 min)
python3 tools/social_card.py --verify                # Vorschaukarte: Maß und Titel (stdlib)
uv run --only-group figures python tools/social_card.py  # Karte neu erzeugen (nur bei Titel-/Farbwechsel)
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
49 Abbildungen neu (dazu 6 Kopien aus dem Material von 2025), ohne dass sich an einer
einzigen etwas Inhaltliches geändert hätte, und
die echte Änderung ist dann nicht mehr von der Fassungsdifferenz zu unterscheiden. Bis zum
2026-10-14 stand im Skriptkopf „System-Python reicht“; dessen matplotlib (3.10.9) war eine
andere als die angeheftete (3.11.2), und genau das ist passiert. Die Gruppe `figures` in
`pyproject.toml` heftet die Fassungen an und enthält **kein** torch, der Lauf kostet also
trotzdem keine Gigabyte. Gegenprobe: zweimal laufen lassen, der zweite Lauf muss
byte-gleich sein.

**Eine Abbildung braucht trotzdem ein trainiertes Netz**, und das ist der Grund für
`devnotes/make_formen_daten.py` (seit 2026-11-13). Es trainiert für die Abbildung
`vl11-stichprobengroesse` im Kapitel „Universelle Approximation“ 50 MLPs – dazu neun
weitere für den Optimierer-Vergleich im Kapitel „Autograd und Berechnungsgraph“ – und legt
das Ergebnis als **versionierte** JSON daneben
(`devnotes/formen-stichprobengroesse.json`); `make_figures.py` zeichnet nur noch daraus
und bleibt damit torch-frei. Die Verteilung selbst steht in `devnotes/formen.py`, reines
NumPy und deshalb auch aus der `figures`-Gruppe heraus benutzbar: Die Beispielbilder in
`vl11-formen-beispiele` kommen aus demselben Code wie die Trainingsdaten und nicht aus
einer Nachzeichnung davon. Die Trennung ist Absicht und keine Umständlichkeit: Sonst
müsste torch in die `figures`-Gruppe, jeder Komplettlauf der Abbildungen würde sieben
Minuten länger dauern, und eine Abbildung hinge an der torch-Fassung statt nur an der
matplotlib-Fassung. Neu erzeugt wird die JSON nur, wenn sich Verteilung oder Budget
ändern — dann mit `uv run devnotes/make_formen_daten.py`, also der Default-Gruppe.

Erwartung eines gesunden Laufs (Stand 2026-11-03, nach den sieben Tafelbildern und dem
Abschnitt „Orthogonale Matrizen“ im Kapitel „Hintergrundwissen Lineare Algebra“ und dem
Rechenbeispiel zur Geradengleichung im Kapitel „Neuron und Perzeptron“ und den zwei
Polyeder-Abbildungen im Kapitel „Aktivierungsfunktionen“ und den Literaturlisten in allen
„Weiterlesen“-Boxen und dem Abschnitt „Approximieren heißt nicht generalisieren“ (Double Descent)
im Kapitel „Universelle Approximation“ und der Vertiefung „Matrizen als Tensoren und die Spur“
im Kapitel „Tensoren“ – und seit dem 2026-11-03 eine Seite mehr, weil in den Kapiteln
„Recurrent Neural Networks“ und „Transformer“ und in „Über dieses Skript“ die doppelte
Titelüberschrift entfiel und die Abschnitte eine Ebene höher stehen (gegen den unveränderten
Baum gemessen: 135); die
fachliche Durchsicht vom 2026-10-15 deckte 27 Kapitel und das Glossar ab, den
Kettenregel-Abschnitt vom 2026-10-20 und diesen Zuwachs nicht; seit dem 2026-11-13 eine Seite
mehr durch den Abschnitt „Mehr Daten oder mehr Epochen?“ samt Abbildung im Kapitel
„Universelle Approximation“ und am selben Tag drei weitere durch den Abschnitt „Autograd bei
der Arbeit“ samt Abbildung im Kapitel „Autograd und Berechnungsgraph“ – jener Abschnitt in 13
wurde dabei um 28 Zeilen kürzer, weil die Verteilung nun in 10 eingeführt wird; seit dem
2026-11-17 vier Seiten mehr: eine durch die Einleitungsabsätze in 20 Kapiteln, eine durch
die Glossarzeile in jeder „Weiterlesen“-Box und drei durch die Herkunftszeile am Ende jedes
Kapitels, abzüglich einer, die beim Nachziehen der Einleitungen und der Startseite am Abend
wieder wegfiel – alles aus den beiden SEO-Audits; seit dem 2026-11-18 eine weitere durch
die Forumszeile am Ende jedes Kapitels; seit dem 2026-11-19 zwei weitere durch den
Abschnitt „Vier Rechnungen mit zwei ReLUs“ in Kapitel 11 und den Richtigstellungskasten
in Kapitel 9): HTML ohne
Warnungen, PDF **155 Seiten A4** lokal, 0 LaTeX-Fehler,
0 fehlende Glyphen, 5 überlange Zeilen. Das veröffentlichte PDF hat am 2026-11-14 **147**
(auf dem Baum `7ccf9c9` gemessen, derselbe wie lokal; am 2026-11-12 waren es **143** gegen
lokal 144, siehe unten). Die `--min-pages`-Untergrenze
soll einen *abgebrochenen* Lauf fangen, nicht eine gewollte Kürzung — sie steht deshalb
deutlich unter der tatsächlichen Seitenzahl, in der CI auf demselben Wert.

**Lokal und CI setzen seit dem 2026-11-17 gleich** — und das ist neu; bis dahin wichen die
beiden PDFs um eine Seite voneinander ab. An dem Tag ist die lokale TeX-Installation von
TeX Live 2024 auf **2026** gehoben worden, und damit lädt auch lokal `minted v3.8.0` statt
`v2.9`. Gegenprobe auf demselben Baum: Das lokal gebaute PDF ist im extrahierten Text
**byte-gleich** mit dem veröffentlichten; gegen die alte Installation unterschieden sich
46 Zeilen, alle davon Umbrüche. Seitenzahl in beiden Fällen 152, überlange Zeilen 5,
0 LaTeX-Fehler, 0 fehlende Glyphen.

Für den Alltag heißt das: **Die lokal gemessene Seitenzahl gilt jetzt auch für die
Veröffentlichung.** Trotzdem bleibt die Regel, die aus der Zeit davor stammt und die
nichts mit der Toolchain zu tun hat: **Die Seitenzahl wird aus dem fertigen PDF gelesen,
nicht aus der Änderungsnotiz übernommen.** Die **142**, die hier und in `devnotes/TODO.md`
bis zum 2026-11-12 stand, ist nie gemessen worden — sie wurde am 2026-11-11 mit der
word2vec-Korrektur eingetragen und war schon beim Eintragen nicht geprüft. Gefunden wurde
das erst, als ein Wächter 17 Stunden lang auf einen Build wartete, der längst durch war:
sein `pgrep`-Muster stand in seiner eigenen Kommandozeile und fand deshalb sich selbst.

### Wie es dazu kam, und was davon zu wissen bleibt

Die Vorgeschichte steht hier, weil sie zweimal falsch erklärt worden ist und weil der
nächste Toolchain-Sprung dieselben Fallen hat.

* **Diese Maschine benutzt nicht das texlive ihrer Distribution** — und die Distribution
  ist **Ubuntu 24.04 LTS**, nicht Debian; bis zum 2026-11-17 stand hier „Debians
  texlive“, und das war an beiden Stellen falsch. Ubuntus Pakete wären auch keine Hilfe:
  `texlive-base 2023.20240207`, also TeX Live **2023**. Die `texlive-*`-Pakete stehen in
  `dpkg` überwiegend auf `rc`; `kpsewhich` kommt trotzdem aus `/usr/bin`, weil das im PATH
  **vor** `/usr/local/bin` steht. Für den Bau ist das ohne Belang — die Engines bringen
  ihre eigene kpathsea mit —, für eine Handprüfung auf der Kommandozeile nicht.
* **minted v2 gegen minted v3** war die Ursache der Abweichung. Bis zum 2026-11-17 lud der
  lokale Lauf `minted 2023/12/18 v2.9`, das CI-Image minted v3; die beiden brechen
  `breaklines` verschieden, und genau das sah man auf Seite 28.
* **Innerhalb eines TeX-Live-Jahrgangs war das nicht zu beheben**, und das sagte `tlmgr`
  selbst: „Local TeX Live (2024) is older than remote repository (2026). Cross release
  updates are only supported with `update-tlmgr-latest --update`.“ Ein einzelnes Paket
  über die Jahresgrenze zu ziehen ist nicht vorgesehen.
* **Deshalb eine frische Installation daneben statt eines Upgrades in place**:
  `/usr/local/texlive/2026`, `scheme-full` ohne Doku- und Quelldateien, 4,9 GB,
  unbeaufsichtigt über ein `-profile`. Die 2024er Installation liegt unangetastet daneben
  — wenn etwas schiefgeht, zeigen die Symlinks mit einem Befehl wieder dorthin.
* **Umgehängt wird mit `tlmgr path add`, nicht mit einzelnen `ln -s`.** In
  `/usr/local/bin` standen **493** Symlinks auf TeX Live 2024, nicht zwei — darunter
  `lualatex`, und das brauchen die Foliensätze (`slides/build.sh` ruft `latexmk
  -lualatex`). Jetzt zeigen 508 auf 2026; die vier, die auf 2024 bleiben, sind
  ConTeXt- und MusiXTeX-Werkzeuge, die TeX Live 2026 nicht mehr mitbringt und die dieses
  Projekt nicht benutzt.
* **`latexminted` braucht lokal keinen Kniff.** TeX Lives eigener Wrapper läuft auf
  Anhieb (`latexminted 0.7.0`, mit Pygments 2.19.2); der Shebang-Patch im Dockerfile gilt
  Debians Paketlayout und nicht dieser Installation.
* **Nachgemessen wurde vor dem Umhängen**, mit dem neuen `bin`-Verzeichnis vorn im PATH
  für einen einzigen Lauf. So steht die alte Toolchain noch, falls das Ergebnis nicht
  taugt. Danach beides gegengeprüft: Buch 152 Seiten, Deck VL 01 41 Seiten und 0 zu volle
  Rahmen — dieselben Zahlen wie unter 2024.

**Die anderen Bücher auf dieser Maschine bauen mit derselben Toolchain.** `ds-skript` und
`eipy-skript` setzen ab jetzt ebenfalls mit TeX Live 2026; ihre lokal notierten
Seitenzahlen stammen aus der Zeit davor und sind beim nächsten Anfassen neu zu messen.

`check_doku.py` prüft die Zahl gegen das **lokale** PDF. Wer die veröffentlichte Zahl
unabhängig davon braucht, holt sie mit dem `curl`-Rezept weiter unten.

Beides ist unabhängig von mystmd: 1.10.1, 1.11.0 und 1.13.0 liefern auf demselben Baum
dieselbe Seitenzahl (1.10.1 gegen 1.11.0 am 2026-10-15 gemessen,
`devnotes/build-log-2026-10-15.md`; 1.13.0 am 2026-11-17, wieder 152 Seiten lokal,
`devnotes/build-log-2026-11-17-theme.md`).

**Die 141 Seiten enthalten zwei Seiten Teilegliederung** (2026-11-04). Vor dem Umbau auf
sechs Teile baute derselbe Baum 138 Seiten, gemessen in einem Worktree auf `4d3434e` mit
derselben `.venv` — die zwei zusätzlichen Seiten sind die zwei neuen Teiltrenner
(„Modelle in der Praxis“, „Ausblick“), nicht neuer Text. Von 136 auf 138 war es davor
schon durch die seitengenauen Folienlinks gewachsen, ohne dass diese Zahl hier nachgezogen
worden wäre.

Am 2026-11-05 ist eine Seite weggefallen, als die Folienzeilen der noch nicht
freigegebenen Decks aus 18 Kapiteln verschwanden (`slides/freigegeben.txt`), und am selben
Tag eine zurückgekommen: die Anhangseite mit den ausgegebenen Übungsblättern. Beide Zahlen
bewegen sich diesen Durchgang über noch, und zwar nach oben – mit jeder Freigabe eines
Decks und mit jedem Blatt, das die Liste länger macht.

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

**Einer der drei Patches sucht mit einem regulären Ausdruck, und das ist Absicht.** Die
Stelle für die Bindestriche steht im minifizierten Bündel als `state.text(nodeN.value,
true)`, und `nodeN` wandert: 1.10.1 und 1.11.0 schrieben `node3`, 1.13.0 schreibt `node4`,
ohne dass sich inhaltlich etwas geändert hätte. Mit einer festen Zeichenkette scheiterte
der Patch beim Fassungssprung, obwohl der Fehler unverändert da war — gefunden am
2026-11-17 beim Upgrade. Anker, Fenster und die Forderung nach genau einem Treffer
bleiben, der Patch scheitert also weiterhin laut, wenn mystmd die Stelle wirklich bewegt.

**Der Patch trifft über den Hardlink den uv-Cache mit — und das verfälscht seine eigene
Meldung.** uv verlinkt Paketdateien aus dem Cache in die `.venv`; `patch_myst_tex.py`
schreibt an Ort und Stelle, also ändert es dieselben Blöcke im Cache. Auf dieser Maschine
liefert deshalb eine **frisch synchronisierte** `.venv` ein schon gepatchtes mystmd, und das
Skript meldet dreimal „bereits gepatcht“ (nachgemessen am 2026-10-16 mit einem Wegwerf-Projekt
auf `mystmd==1.11.0`). Zwei Folgerungen: Der Aufruf bleibt Pflicht — nach einem
`uv cache clean`, in der CI und auf jeder anderen Maschine ist er wieder nötig —, und
**„bereits gepatcht“ ist kein Beleg, dass mystmd den Fehler behoben hat.** Das prüft man
gegen einen frischen Cache, nicht gegen diese `.venv`.

Seit dem 2026-10-16 liegen Cache und venv dieses Projekts auf der zweiten SSD:
`/media/konrad/xtraspace/uv/cache` (global in `~/.config/uv/uv.toml`) und
`/media/konrad/xtraspace/uv/venvs/eidl-skript`, auf das `.venv` als **Symlink** zeigt. Beides
muss auf *derselben* Platte liegen, sonst kann uv nicht mehr hardlinken und kopiert — dann
kostet jede venv ihre volle Größe. `uv run` und `myst` merken davon nichts; wer die Platte
nicht gemountet hat, hat kein Python.

Das Site-Template ist **mitgeliefert** (`_site/vendor/book-theme.zip`, `@myst-theme/book`
1.4.1 seit dem 2026-11-17, davor 1.3.1) und wird von
`install_template.py` an die Stelle entpackt, an der MyST es zwischenspeichert. Ohne diesen
Schritt lädt `myst build` es bei jedem Lauf von einem *wandernden Branch* bei GitHub — das
macht das Aussehen der Seite zu einer unversionierten Abhängigkeit und den Build von einer
Netzverbindung abhängig. Ein lokaler Pfad in `myst.yml` funktioniert für `site.template`
**nicht**; für das tex-Template unter `templates/tex/eidl-skript` funktioniert er sehr wohl,
und deshalb liegt das einfach im Repo. Begründung und Aktualisierungsweg:
`_site/vendor/README.md`; geholt wird seitdem das **Release-Asset** aus
https://github.com/jupyter-book/myst-theme/releases und nicht mehr `main.zip` — ein wandernder Branch hatte schon
einmal eine andere Fassung geliefert als notiert.

**Auf 2.x geht dieses Repo nicht ohne Umbau.** Theme 2.0.0 (2026-11-10) ist ein erklärter
Bruch, und das Dateilayout ändert sich vollständig: zwei Serverbündel statt einem,
Vite-`_assets`-Chunks statt der bisherigen `_shared`-Chunks, `thebe-core.css` in das Hauptstylesheet
eingebacken. **Die Anker in `install_template.py` überleben allerdings** — am 2026-11-18
gemessen: alle 37 greifen, sobald das Anführungszeichen im Muster offen bleibt, denn 2.x
schreibt Zeichenketten in Backticks. Die Arbeit liegt bei den Adressen im Artefakt —
Abbildungen unter `/_public/…` statt `/build/…`, und fünf Skripte in `tools/` setzen die
alte Adresse an 13 Stellen voraus — und bei `dead_css.py`, das ohne den `thebe-core`-`<link>` sein
größtes Ziel verliert. Die Durchsicht der Upstream-Änderungen samt Messwerten steht in
`devnotes/build-log-2026-11-17-theme.md`.

`check_doku.py` vergleicht, was die Dokumentation behauptet, mit dem, was da ist: Pfade,
Kapitel- und Übungszahlen, Seitenzahl, `--min-pages` hier und in der CI, die Vollständigkeit
von `devnotes/README.md`, und die Regeln, die im Buch gelten (keine Blattnummern, keine
Lösungen, keine Unicode-Pfeile, keine zwei gleich benannten Überschriften in einer Datei –
die teilen sich sonst einen Anker, und der zweite Abschnitt ist nicht mehr adressierbar). Er ist entstanden, weil diese Datei an einem einzigen Tag
drei falsche Angaben angesammelt hatte, ohne dass irgendetwas rot geworden wäre. Wer eine
Zahl hier bewusst ändert, ändert sie dort mit — oder der Prüfer meldet sich.

**Vor jedem Abschluss einer inhaltlichen Änderung**: `myst build --html` laufen lassen und
die Warnungen ansehen. Neue Warnungen sind ein Fehler in der Änderung, nicht
Hintergrundrauschen — insbesondere `Cross-reference target not found` bedeutet einen
kaputten Link. Und **nach dem Push nachsehen, dass es auch veröffentlicht wurde**: „lokal
grün“ und „veröffentlicht“ sind zwei verschiedene Aussagen.

**Zuerst: `glab` ist angemeldet.** Die Pipeline-API ist zwar anonym gesperrt
(`/api/v4/projects/voelkel%2Feidl-skript/pipelines` antwortet mit 403), aber ein Token
*liegt* hier — `glab ci list -P 3` und
`glab api "projects/:id/jobs/<id>/trace"` lesen Pipelines und Job-Protokolle. Nicht
abschrecken lassen von `glab auth status`: das meldet „Invalid token provided", weil dem
Token die Berechtigung `User: Read` fehlt und der Endpunkt `user` deshalb 403 gibt — für
Pipelines und Traces genügt es (am 2026-11-16 nachgeprüft: anonym 403, mit `glab` 20
Pipelines). Der direkte Weg ist also der Trace des `pages`-Jobs; die Prüfschritte der
Kette stehen dort namentlich mit ihren Zahlen.

**Zeitstempel statt Inhaltsmarker.** Verläßlich sagt nicht die Seite, ob der Deploy durch
ist, sondern der Vergleich mit der Startzeit des Jobs: liegt `last-modified` davor, ist die
Antwort alt. Nach einem grünen `pages`-Job antwortet die Seite nämlich noch eine Weile mit
dem *vorigen* Deploy, und daran sind zwei Dinge schuld — die Zwischenspeicherung über die
volle URL (`cache-control: max-age=600`, umgehbar mit `?x=$RANDOM`) und eine Verzögerung,
bis die neue Auslieferung bereitsteht, gegen die der Zusatz **nicht** hilft. Am 2026-11-16
beides gemessen, 40 s nach Jobende gab auch die umgangene Anfrage noch den Vorlauf. Der
ETag taugt nicht als Ersatz: er wechselt von Deploy zu Deploy, auch bei bytegleicher Datei.

**Ohne Zugang zur Pipeline** prüft man das **Ergebnis** statt des Laufs:

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

**Und der Wächter braucht `-L`.** Die Kapitelseiten antworten mit **302** auf ihre Adresse ohne
Schrägstrich am Ende und leiten auf die mit weiter — die Regel aus `tools/publish_urls.py`, nach
der jede `<loc>` einen Schrägstrich trägt. Ein `curl -s` ohne `-L` bekommt 94 Byte Weiterleitung, findet den
Marker nie und meldet nach zehn Minuten „nicht veröffentlicht“, obwohl der Deploy längst
durch ist — so am 2026-10-28 geschehen. Also `curl -sL`, und im Zweifel die Bytezahl ansehen:
Eine Seite hat sechsstellig viele, eine Weiterleitung zweistellig. Die Rezepte oben
(`eidl-skript.pdf`, `myst.xref.json`) sind davon nicht betroffen, das sind Dateien.
Dieselbe Falle wie bei den Playlists der Mediathek (Abschnitt „Vorlesungsaufzeichnungen“).

## Veröffentlichungs-Metadaten

Was eine Suchmaschine oder eine Antwortmaschine über dieses Buch erfährt, entsteht
**nicht** beim Bauen, sondern danach: MyST kennt die Adresse der Seite nicht und schreibt
die seines eigenen Dev-Servers in `sitemap.xml` und `robots.txt`, emittiert keinen
Canonical und keine strukturierten Daten. Die Skripte in `tools/` tragen das nach, und
seit dem 2026-11-03 auch das, was die Auslieferung braucht (Kompression, eigene
Herkunft, Layoutsprung; Ports aus ds-skript, ds-en und eipy, PLAYBOOK §3.12). Sie laufen
im `pages`-Job und brauchen **kein einziges Python-Paket**.

| Skript | Was |
|---|---|
| `tools/social_card.py` | Erzeugt und prüft `images/social-card.png` (1200×630). Die Karte ist eingecheckt und steht als `thumbnail:` in `myst.yml` |
| `tools/publish_urls.py` | Echte Adresse in Sitemap und `robots.txt`, jede `<loc>` mit Schrägstrich, `og:image` absolut, ein Canonical je Seite; `--check` prüft das am Artefakt nach |
| `tools/head_meta.py` | `og:url`, `og:site_name`, `og:type`, `og:locale`, `twitter:card`; aus dem `<title>` **der Kapitel** den angehängten Werktitel nehmen, wo er über 60 Zeichen hinausführt (seit dem 2026-11-22, Konrads Entscheidung: neun Seiten, `og:title` bleibt wie MyST es schreibt); den `<title>` **der Landingpage** um „ — Vorlesungsskript, HHU Düsseldorf“ (ohne Jahreszahl, das Skript ist semesterunabhängig; `h1` und `og:title` bleiben der Werktitel); `lang="de"` samt Wächter gegen die Hydration; zu kleine Abbildungen als Vorschaukarte ersetzen; Abbildungen unter der Falz verzögert laden; dazu seit dem 2026-11-22 `og:image:alt`, `twitter:image:alt` und die zwei Maßangaben — **das Maß aus der Bilddatei gelesen**, weil eine große Abbildung als Karte stehen bleiben darf und 1200×630 dann falsch wären; die zwei Hausschriften und — auf den 29 Seiten mit Formeln — die zwei KaTeX-Schriften vorladen (`KaTeX_Math-Italic`, `KaTeX_Main-Regular`): sie werden sonst erst nach dem Stylesheet entdeckt und ruckten die Absätze mit Inline-Mathematik, CLS auf der Destillations-Seite 0,076 statt 0,022 |
| `tools/inject_jsonld.py` | JSON-LD: ein Buchknoten samt den zwei anderen Skripten desselben Autors auf der Landingpage, je ein Kapitelknoten mit Brotkrume auf den 29 übrigen Seiten, und auf der Glossarseite ein `DefinedTermSet` mit den 69 Begriffen — je Begriff die Adresse **seines Kapitels** als `url` (das zuerst genannte) und die Erklärung mit Mathematik im Klartext, `MATHE_ERSATZ` scheitert laut an unbekannten Befehlen. Daten in `tools/structured-data.json` und `tools/sibling-works.json` |
| `tools/dead_css.py` | Nimmt die drei Stylesheets heraus, die das Theme in jede Seite legt und die dieses Buch nicht benutzen kann: `thebe-core.css` (87 kB), `font-awesome.css`, `mpl_widget.css` — alle drei für Jupyter-Ausgaben, und keine der 33 Seiten hat eine. Im Markup **und** im `links()`-Array des Wurzel-Chunks. **Vor `vendor_assets.py`.** Scheitert, sobald eine Seite ausführbar wird |
| `tools/vendor_assets.py`, `tools/check_css_assets.py` | Das KaTeX-Stylesheet des Themes aus `_site/vendor/` statt vom CDN, in HTML **und** JS, samt seinen zwanzig Schriftdateien; die Schriften aus `_site/fonts/` statt von Google. Der Prüfer löst jeden `url()` der eingebundenen Stylesheets auf. Font Awesome und jupyter-matplotlib lagen hier bis zum 2026-11-16, siehe `dead_css.py` |
| `tools/thebe_gate.py` | Lädt `thebe-core` (1,3 MB) nur auf Seiten mit ausführbarem Code, also hier auf keiner. Patcht einen Ausdruck im Client-Bündel und scheitert laut, wenn ein mystmd-Update ihn verschiebt |
| `tools/freshness.py` | `article:modified_time` je Seite und `<lastmod>` je Sitemap-Eintrag, aus `git log` der Quelldatei — **seit dem 2026-11-22 ohne die Commits, die nur die Forums- oder die Herkunftszeile angefaßt haben** (Konrads Entscheidung; vorher sagten 30 von 33 Seiten dasselbe Datum, weil diese Zeilen in einem Zug eingetragen wurden). Dieselbe Funktion versorgt `zitierzeile.py` und `inject_jsonld.py`, sonst stünden auf einer Seite zwei Daten |
| `tools/llms_txt.py` | Der Quelltext jeder Seite als Markdown (`/<slug>.md` und `/<slug>/index.md`, relative Kapitelverweise auf die Seitenadresse umgeschrieben; jede `figure`-Direktive wird zu `![Unterschrift](…/build/…)` mit der Adresse, unter der das Bild wirklich liegt, `anywidget`-Blöcke fallen weg), `<link rel="alternate" type="text/markdown">` im Kopf, `/llms.txt` und `/llms-full.txt`. Google ignoriert `llms.txt`; der Nutzen liegt bei den `.md`-Dateien |
| `tools/image_dims.py`, `tools/outline_reserve.py` | Gegen den Layoutsprung: `width`/`height` an jeder Abbildung samt einem Stylesheet mit allen Bildmaßen, und Platz für die Gliederung, die das Theme erst nach dem Laden füllt. **Unterhalb von `lg` sind es seit dem 2026-11-17 feste 128 px**, passend zu der Deckelung in `_site/custom-style.css` — vorher reservierte der Kasten bis zu 692 px und schob den Einleitungsabsatz unter die Falz |
| `tools/webp.py` | Liefert die Abbildungen als WebP aus statt als PNG und JPG: 7,6 MB werden 2,4 MB. Die Fassungen liegen im Repo (`devnotes/make_webp.py`), das Image baut nichts. Ersetzt den Dateinamen im Markup, im Stylesheet `bildmasse` **und** in der Hydrations-Nutzlast — ein `<picture>` mit PNG-Rückfall überlebt die Hydration nicht. Dazu seit dem 2026-11-17 `srcset="… 1x, … 2x"` für die 53 Abbildungen ab 700 px, die eine halb so breite Fassung daneben haben: ohne Retina-Auflösung 1,04 MB statt 2,37 MB Bildbytes. Das geht als `<picture>`, weil das Theme es aus dem Nutzlastfeld `urlOptimized` selbst rendert — geschrieben wird deshalb Markup **und** Nutzlast, sonst holt der Browser die große Datei nach der Hydration ein zweites Mal. **Nach `image_dims.py`, vor `hydration.py`** |
| `tools/trailing_slash.py` | Kapitellinks mit Schrägstrich (sonst 302), im Markup, in der Hydrations-Nutzlast und in den Seiten-JSON; die Seitenleiste bewusst nicht. Seit dem 2026-11-22 auch mit Fragment oder Query dahinter: Der Schrägstrich kommt **vor** den Rest, aus `/kapitel#abschnitt` wird `/kapitel/#abschnitt` |
| `tools/suchindex.py` | Nimmt den rohen LaTeX-Quelltext aus `myst.search.json`, also aus den Suchausschnitten: MyST legt dort den Text jeder Überschrift samt Abschnitt ab, Mathematik aber **ohne** die `$`-Zeichen. Übersetzt wird mit der Tabelle aus `inject_jsonld.py` plus einer eigenen, der Rest wird abgestreift — ein lauter Abbruch wie beim Glossar wäre hier ein Deploy-Stopper (98 unbekannte Befehle im ganzen Buch). Angefasst wird nur ein Feld mit Backslash, sonst wäre der zweite Lauf nicht wirkungslos. `--check`: kein Backslash mehr im Index |
| `tools/no_css_dialog.py` | Nimmt den Kasten „Site not loading correctly? … `BASE_URL`“ aus jeder Seite. Das Theme legt ihn als `<dialog id="myst-no-css">` an; sichtbar wird er nur ohne Stylesheet, **im Text der Seite steht er aber als erstes** und begrüßt jeden, der die Seite als Text liest, mit einer Deploy-Fehlermeldung. `--check` zählt nach; findet der Lauf gar keinen Kasten, scheitert er (mystmd könnte ihn umbenannt haben) |
| `tools/zitierzeile.py` | Stand und zitierfähige Adresse in die Herkunftszeile der 31 Seiten, die eine haben: aus „frei unter CC BY-SA 4.0." wird „frei unter CC BY-SA 4.0, Stand 18. November 2026. Zitierbar als https://…/backpropagation/." Das Datum kommt aus derselben Funktion wie bei `freshness.py`, also aus `git log` der Quelldatei, und nicht aus einer zweiten Rechnung. Geschrieben wird in Markup **und** Hydrations-Nutzlast (die Zeile ist Fließtext, und den rendert das Theme neu), dazu in die Seiten-JSON, in beide `.md`-Fassungen und abschnittsweise in `llms-full.txt`. **Nach `llms_txt.py`**, sonst fehlt die Angabe in der Markdown-Auslieferung. Nicht angefasst: Startseite und die Seite „Über dieses Skript“ (tragen die Zeile nicht), `myst.search.json` (sonst steht es in jedem Suchausschnitt) und die gehashten Quelltext-Kopien, die MyST unter `_build/html/build` ablegt. Im PDF steht die Zeile ohne Datum und Adresse — dort läuft kein Veröffentlichungsschritt, Konrads Entscheidung vom 2026-11-18 |
| `tools/stable_card.py` | Gibt der Vorschaukarte einen Namen, der nicht bei jedem CI-Lauf wechselt: `public/build/social-card-<hash>.png` → `public/build/social-card.png`, in allen `.html`, `.json`, `.txt` und `.xml` des Artefakts. MyST hasht nach Pfad + mtime + Größe, nicht nach Inhalt. **Nach `llms_txt.py`, vor `image_dims.py`**; im Unterordner und nicht in der Wurzel des Artefakts, damit `hydration.py` die Nutzlast weiter absolut macht |
| `tools/hydration.py` | Hält nach der Hydration zurück, was React ausräumt: Canonical, `og:*`, `twitter:card`, Markdown-`alternate`, `lang`, Titelzusatz, `ld+json` und die zwei Stylesheets; `og:image` dagegen über die Nutzlast, weil das Theme dafür ein Feld rendert. **Letzter Schritt am Kopf.** `--check-rendered` mißt im Browser statt am Artefakt |
| `tools/precompress.py` | `.br` und `.gz` neben jede Textdatei, **als letzter Schritt** des Jobs; `--check` packt jede Kopie aus und vergleicht byteweise |

**Jede Seite außer der Landingpage hat ein eigenes `description:` im Frontmatter**
(seit 2026-11-03; vorher erbten alle 32 die des Buchs aus `myst.yml`). Es ist der Text
unter dem Suchergebnis, die Beschreibung der Vorschaukarte und die `description` des
Kapitels im JSON-LD. Höchstens 155 Zeichen, was im Kapitel steht und mit den Wörtern, nach
denen jemand sucht („Kreuzentropie“, „LSTM“), ohne Werbesprache. Ein neues Kapitel bekommt
eines, sonst meldet sich `check_doku.py`.

**Die Reihenfolge ist nicht beliebig**, und sie steht samt Begründung im `pages`-Job:
`dead_css.py` vor `vendor_assets.py` (dessen Nachbedingung ist, daß jedes vendorierte
Blatt auch eingebunden ist), `vendor_assets.py` vor `thebe_gate.py` (beide ändern dieselben Bündel), `publish_urls.py`
vor `head_meta.py` (og:url bekommt dieselbe URL wie der Canonical), `head_meta.py` vor
`inject_jsonld.py` (liest Karten-URL und Kapiteltitel aus der Seite zurück) und vor
`image_dims.py` (lazy und Maße zusammen), `zitierzeile.py` **nach** `llms_txt.py`
(sonst fehlt die Zitierangabe in der Markdown-Auslieferung), die Prüfläufe danach,
und `precompress.py` **zuletzt** — jede Änderung nach ihm liefert allen Lesern die alte `.br` aus.
Lokal prüfen heißt: `myst build --html`, die Schriften wie im `myst-build`-Job in das
gebaute HTML kopieren, dann die Skriptzeilen des `pages`-Jobs gegen eine **Kopie**
von `_build/html` — sie schreiben in das Verzeichnis hinein.

**Die Hydration scheitert hier, wie in ds-skript — berichtigt am 2026-11-15.** Bis dahin
stand an dieser Stelle das Gegenteil, gemessen am 2026-11-03. Es war falsch, und zwar für
jede Seite. Die Konsole zeigt **React #418 und #423**; #423 heißt, daß React die Wurzel
vollständig neu rendert, und dabei wird `documentElement` mitsamt `<head>` **ersetzt**,
nicht verändert. Nach dem ersten Frame ist deshalb weg, was die Schritte in `tools/`
nachgetragen haben: `lang="de"` (steht dann auf `en`), jeder `ld+json`-Block, der
Canonical, `og:url`/`og:site_name`/`og:type`/`og:locale`, `twitter:card`, der
Markdown-`alternate`, die zwei Stylesheets `bildmasse` und `gliederungsplatz` und der
Titelzusatz der Landingpage; `og:image` steht wieder wurzelrelativ. Zweifach nachgemessen:
im sichtbaren Browserfenster und, unabhängig davon, an Googles eigenem Renderer (Rich
Results Test, „View tested page") — dieser mit dem Befund „No items detected", obwohl
`BreadcrumbList` ein Rich-Result-fähiger Typ ist und im Roh-HTML steht.

Deshalb gibt es `tools/hydration.py` jetzt auch hier — aber **nicht** als Kopie des
dortigen. ds-skripts Wächter beobachtet `document.head`; das wäre hier still wirkungslos,
weil genau dieser Knoten ersetzt wird. Eine Sonde zur Parse-Zeit meldet `headSame: false`,
`headConnected: false`, `deSame: false`. Der Wächter hier hängt an `document` und schlägt
Kopf und Wurzelelement bei jedem Lauf frisch nach. Daran war auch der `lang`-Wächter in
`head_meta.py` gestorben: `langFired: 0`, der Knoten wurde getauscht und nicht mutiert.

**Seit dem 2026-11-22 stimmt diese Mechanik nicht mehr — der Wächter bleibt aber nötig.**
Nachgemessen mit der Pipeline des `pages`-Jobs gegen zwei Kopien des Artefakts, einmal ohne
`hydration.py`, beides im Browser gelesen: Auf sechs von sechs Seiten meldet die Konsole
**keinen React-Fehler mehr**, und ohne Wächter überleben `lang="de"`, der `ld+json`-Block
samt Typen und die zwei Stylesheets `bildmasse` und `gliederungsplatz`. Der Kopf wird also
nicht mehr ersetzt. Verloren gehen nur die `<meta>`- und `<link>`-Tags, die React im Kopf
selbst verwaltet: Canonical, die vier `og:*`, `twitter:card`, der Markdown-`alternate`,
`article:modified_time` und der Titelzusatz der Startseite; `og:image` fällt auf die
wurzelrelative Adresse zurück, und den `myst-no-css`-Kasten legt das Theme neu an. Daß der
Wächter an `document` hängt und Kopf und Wurzel frisch nachschlägt, ist damit Vorsorge statt
Notwendigkeit; welche der beiden Bewegungen vom 2026-11-17 (Theme 1.4.1, mystmd 1.13.0) den
Abbruch behoben hat, ist nicht gemessen. Messwerte und Methode:
`devnotes/build-log-2026-11-22-hydration.md`.

**Wer das Theme oder mystmd anhebt, mißt das neu — am gerenderten DOM, nicht am
Artefakt**: `tools/hydration.py --check-rendered _build/html` (braucht Playwright und
läuft deshalb nicht in der CI). Daß alle Schritte bisher nur das Artefakt prüften, ist der
Grund, aus dem der Verlust zwei Audits lang unentdeckt blieb; Messwerte in
`devnotes/seo-audit-2026-11-15.md`. Und ein Klick auf einen Kapitellink lädt hier das
ganze Dokument neu, er rendert nicht aus der Nutzlast.

**Diese Seite hat zwei Adressen.** Die lesbare Namensraum-URL
https://voelkel.pages.cs.uni-duesseldorf.de/eidl-skript/ antwortet mit 308 auf
https://eidl-skript-131e30.pages.cs.uni-duesseldorf.de/ — GitLabs „unique domain" ist in
diesem Projekt eingeschaltet. **Der generierte Host ist der kanonische** (Konrads
Entscheidung vom 2026-10-19, familienweit): `SITE_ORIGIN`, Canonical, `og:url`, jede
`<loc>`, `url` und der `@id` im JSON-LD nennen ihn. Der `@id` steht als `__SITE__/#work`
in `tools/structured-data.json` und nicht als feste Zeichenkette, damit er nicht von
`SITE_ORIGIN` abdriften kann; die lesbare Adresse bleibt als `sameAs` stehen. Preis:
Der Bezeichner ist ein Hostname, den GitLab vergibt — wird „unique domain" abgeschaltet,
ändern sich die entsprechenden Dateien in vier Repositorien zugleich.

Warum das alles überhaupt nachgerüstet wurde, mit Messwerten:
`devnotes/build-log-2026-10-19.md`. Die Regeln dahinter gelten für alle drei Bücher und
stehen in den Schwesterrepos, aus denen die Skripte stammen (`~/Sciebo/hhu/ds2026/ds-en`,
dort `SEO-NOTES.md`, und `~/Sciebo/hhu/ds2026/ds-skript`).

Wichtig zur Ordnerstruktur:

* `_site/` ist **Quellcode** (eigenes CSS, Navbar-Fragmente, die Fußzeile mit Impressum und
  Datenschutz der HHU (`footer.md`), die Wegweiser unter dem Inhaltsverzeichnis
  (`sidebar_footer.md`: zum Anfang, Über dieses Skript, Glossar und Übungsblätter — auf
  dem Handy stehen sie im aufgeklappten Menü), unter `_site/fonts/` die zwei
  Schriften, unter `_site/vendor/` das mitgelieferte Site-Template und die drei
  Theme-Stylesheets samt Herkunftsnachweis in `PROVENANCE.txt`).
* `_build/`, `exports/` und `public/` sind **Artefakte** — nie von Hand bearbeiten,
  gitignored.
* `tools/` sind die Skripte der **Veröffentlichung** (siehe oben) — sie laufen in der
  CI und schreiben am gebauten HTML, nicht am Buch.
* `devnotes/` sind Arbeitsnotizen des Autors, nicht Teil des Buchs (nicht im TOC).
  `devnotes/README.md` sagt, welche Datei wofür da ist; `devnotes/TODO.md` ist die eine
  Liste offener Punkte.
* `transcripts/` (Vorlesungsaufzeichnungen 2025/26) und `uebungen-2025/` (die zwölf
  Übungsblätter samt Lösungsvorschlägen) sind gitignored und liegen nur in Sciebo. **Was
  hier landet, ist im Netz** — der GitHub-Spiegel unter
  https://github.com/konradvoelkel/eidl-skript-mirror, den der CI-Job `mirror-to-github`
  pusht, ist öffentlich, und daran ändert sich nichts.
  Auf GitLab selbst steht das Repository seit dem 2026-11-17 auf „Only Project Members":
  Blob, Tree und Raw antworten anonym mit 404, anonymes Klonen mit 401, die Projektseite
  und die Pages-Auslieferung bleiben öffentlich. Grund war nicht Geheimhaltung, sondern
  die Suche: Die Quelldatei eines Kapitels stand für „Deep Learning Skript" vor dem
  gesetzten Buch (SEO-Audit vom 2026-11-17, §8b). **Die Regel bleibt deshalb unverändert
  streng** — der Spiegel ist öffentlich, also ist jede committete Datei öffentlich.

## Aufbau

| Ordner | Inhalt |
|---|---|
| `part-grundlagen/` | Kapitel 01–05: Was ist Deep Learning, Neuron/Perzeptron, Training, vortrainierte Modelle, Tensoren; dazu die zwei Hintergrundkapitel (Lineare Algebra, Analysis) **hinter** Kapitel 01, ohne Nummer im Dateinamen, weil sie nicht in der Vorlesungsreihenfolge stehen |
| `part-lernen/` | Kapitel 06–13: logistische Regression, Loss und Maximum Likelihood, Gradientenabstieg, Backprop, Autograd, Aktivierungen, Netze von Hand, universelle Approximation |
| `part-representation-learning/` | Kapitel 14–18: Autoencoder, VAE, word2vec, latente Räume geometrisch, Graphen |
| `part-architekturen-anwendungen/` | Kapitel 19–27: RNN, Transformer, CNN, GANs; LLMs benutzen, Anwendungsbeispiele, Destillation; Optimierer, Adversarial Attacks. **Der Ordner trägt drei Teile des Buchs**, siehe unten |
| `slides/` | Beamer-Foliensätze VL 01–15 (`build.sh`, gemeinsamer `header.tex`); `freigegeben.txt` sagt, welche davon veröffentlicht und verlinkt werden dürfen |
| `images/`, `logo/` | Abbildungen, Logos; dazu `images/social-card.png`, die Vorschaukarte |
| `tools/` | Skripte der Veröffentlichung: Vorschaukarte, Sitemap-URLs, Kopf-Tags, JSON-LD |
| `widgets/` | interaktive Teile der Website (`{anywidget}`, ein ES-Modul ohne Abhängigkeiten je Widget); im PDF fehlen sie, deshalb steht jedes direkt unter etwas, das im PDF dasselbe leistet. Unter einer statischen Abbildung: `drehung.mjs` im Kapitel „Hintergrundwissen Lineare Algebra“, `perzeptron.mjs` im Kapitel „Das Perzeptron trainieren“, `stufe.mjs` im Kapitel „Universelle Approximation“ und `gradientenabstieg.mjs` im Kapitel „Gradientenabstieg“. Unter jeder Aufzeichnungszeile: `mediathek.mjs`, der eingeklappte Player (Abschnitt „Vorlesungsaufzeichnungen“) |
| `notebooks/` | Notebooks aus 2025; nur `latent-classifier.ipynb` hat noch eine Funktion — es hängt als `downloads:` am Kapitel 21 |
| `glossar.md` | Klausurbegriffe mit Link ins jeweilige Kapitel (im TOC, Abschnitt „Anhang“) |
| `blaetter/`, `uebungsblaetter.md` | die **ausgegebenen** Übungsblätter als PDF und die Anhangseite, die sie verlinkt; dass ein PDF hier liegt, ist die Freigabe |
| `kurs-2026-27.md` | Semesterplan, Termine, Organisatorisches — **nicht im TOC**, also nicht Teil des Buchs |
| `uebungen-2025/` | die zwölf Blätter von 2025 samt Lösungen; gitignored, Quelle für neue Übungsabschnitte |

Das Inhaltsverzeichnis steht **explizit** in `myst.yml` unter `project.toc`. Eine neue Datei
erscheint erst nach einem Eintrag dort.

**Sechs Teile, vier Ordner** (seit 2026-11-04): Grundlagen, Lernen, Representation Learning,
Architekturen, Modelle in der Praxis, Ausblick. Die Ordner sind nicht nachgezogen worden —
`part-architekturen-anwendungen/` trägt die letzten drei Teile. Das ist Absicht: Ein Umzug
der Dateien kostet Verweise, und die Teile stehen ohnehin in `myst.yml`, nicht im Pfad.
`devnotes/check_doku.py` zählt die Kapitel über genau diese vier Ordner.

**Die Nummern im Dateinamen folgen der Buchreihenfolge, nicht der Vorlesung.** Wer ein
Kapitel verschiebt, nummeriert die folgenden mit um (am 2026-11-04 für sechs Kapitel
getan: latente Räume von 23 nach 17, Graphen 17 nach 18, RNN 18 nach 19, Transformer 19
nach 20, CNN 20 nach 21, LLMs benutzen 21 nach 23). Billig ist das, weil die Nummer
**nirgends nach außen** sichtbar wird: MyST bildet die Seitenadresse aus dem Dateinamen
*ohne* Nummer und ohne Ordner — das Transformer-Kapitel liegt unter
`https://eidl-skript-131e30.pages.cs.uni-duesseldorf.de/transformer/`, nicht unter einer
Adresse mit Ordner und Nummer. Überschriften tragen keine Nummern, und Querverweise
dürfen keine tragen. Eine *Umbenennung* ändert die Adresse dagegen sehr wohl — am
2026-11-04 genau eine: aus `latente-raeume` wurde `latente-raeume-geometrisch`.

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
* **Keine Pointe am Absatzende.** Kein Nachsatz, der eine Zahl noch einmal in eine Haltung
  übersetzt: „ist also keine Nebensache“, „wer hier am Netz zweifelt, zweifelt an der
  falschen Stelle“, „ist eine Messung und keine Meinung“. Die Messung steht schon da; der
  Nachsatz sagt dem Lesenden bloß, was er davon halten soll, und klingt nach Werbung für
  den eigenen Befund. Am 2026-11-14 zwei solche Stellen im Kapitel „Autograd und
  Berechnungsgraph“ entfernt (Konrads Entscheidung) — und daran gemerkt, dass solche Sätze
  beim Schreiben wie Abschlüsse wirken und deshalb von allein wiederkommen.
* **Jede Behauptung belegbar.** Formeln nachrechnen, Paper mit Jahr und Titel nennen,
  Bibliotheksversionen prüfen statt erinnern.
* Rechenbeispiele werden **durchgerechnet**, nicht behauptet. Wer eine Zahl ändert, rechnet
  die Folgezahlen nach.
* Vertiefungen, die nicht Vorlesungsstoff sind, stehen in einer Box
  `:::{admonition} Vertiefung: …` mit `:class: note dropdown` (derzeit neun; dazu eine
  Antwortenbox in Kapitel 01, zusammen zehn `dropdown`-Boxen).
  **Aufgeklappt wird nur im HTML**: `dropdown` hat im LaTeX-Export keine Wirkung, im PDF
  steht der Inhalt offen da. Für Vertiefungen ist das in Ordnung — für alles, was erst nach
  eigenem Nachdenken gelesen werden soll, ist `dropdown` kein Versteck. Genau daran hingen
  bis zum 2026-09-27 die Lösungsvorschläge der Übungsblätter im PDF.

## Literatur

**Jeder Literaturverweis ist anklickbar, und jedes zitierte Werk steht in der
„Weiterlesen“-Box seines Kapitels.** Entschieden am 2026-11-02, nachdem im
Transformer-Kapitel ein Artikel nur mit Titel und Autorin genannt war – und so rund 50
Werke im ganzen Buch.

* **Im Text** wird der Titel zum Link (bei Kurzzitaten die Angabe „Autor Jahr“). Ziel ist
  die **DOI**, wenn das Werk eine hat – geschrieben als `https://hdl.handle.net/<DOI>`, nicht
  als `doi.org` (Begründung unten); sonst die Adresse, unter der es
  frei abrufbar ist (arXiv-Abstract, Blog, Projektseite). Liegt die DOI-Fassung hinter
  einer Bezahlschranke und gibt es eine freie, kommt sie als „frei: arXiv:…“ dazu.
* **In „Weiterlesen“** steht unter **„Im Kapitel zitiert:“** jedes Werk mit Autoren,
  verlinktem Titel, Ort und Jahr. Ein Kapitel ohne Box bekommt eine, am Ende.
* **Warum nicht `doi.org`:** mystmd macht aus *jedem* Link auf `doi.org` ein Zitat. Es holt
  die Metadaten beim Bauen aus dem Netz, ersetzt im PDF den Linktext durch „Autor [Jahr]“
  und hängt eine Literaturliste an; im HTML bleibt der Text stehen. Am 2026-11-02 stand
  deshalb im veröffentlichten PDF „Hochreiter, Schmidhuber: Hochreiter and Schmidhuber
  [1997]“, im RNN-Zeitstrahl „Hochreiter and Schmidhuber [1997]“ statt „LSTM“, und es war
  drei Seiten länger als lokal – wo das Netz fehlte und 24-mal „?“ stand. Einen Schalter
  dagegen gibt es nicht (`transformLinkedDOIs` in mystmd 1.11). DOIs sind Handles:
  `hdl.handle.net` leitet auf dasselbe Ziel weiter, und mystmd lässt den Link in Ruhe.
  Wer das Zitatsystem von MyST doch will, entscheidet das für das ganze Buch – und macht
  den Bau von `doi.org` abhängig.
* **Kennungen werden nicht aus dem Gedächtnis eingetragen**, sondern gegen den Titel
  geprüft: arXiv über `export.arxiv.org/api/query?id_list=…`, DOIs über `doi.org` mit
  `Accept: application/vnd.citationstyles.csl+json`. Am 2026-11-02 so für 50 Kennungen.
* `check_doku.py` meldet eine Zeile mit „et al.“ oder „arXiv:“ ohne Link und jede DOI-
  oder arXiv-Adresse, die nicht auch in „Weiterlesen“ steht. Was keine dieser Formen hat
  („Gage 1994“), fängt er nicht.
* **Fremde Abbildungen:** Eine Lizenzangabe auf Wikimedia Commons ist eine Behauptung des
  Hochladenden. Das klassische Hubel-Wiesel-Bild steht dort als „Own work“, ist aber
  erkennbar aus einem Lehrbuch gescannt – deshalb ist es nachgezeichnet
  (`vl10_hubel_wiesel` in `make_figures.py`) statt übernommen.

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
* **Eine Bildunterschrift mit Mathematik braucht ein `:alt:`.** MyST bildet den Alt-Text
  aus der Unterschrift; steht dort `$w \cdot x + b = 0$`, liest ein Screenreader
  „backslash cdot“. Am 2026-11-17 waren so 20 Alt-Texte im gebauten HTML. Jede `figure`,
  deren Unterschrift Mathematik enthält, trägt deshalb ein `:alt:` mit einer
  Klartextbeschreibung — und zwar eine, die *das Bild* beschreibt, nicht die Unterschrift
  wiederholt; die steht ohnehin daneben.
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
* **Die Kästen sind `<div>` und nicht `<aside>`, und das ist ein Patch am Theme.**
  `_site/vendor/install_template.py` ersetzt seit dem 2026-11-17 in beiden Bündeln
  `aside` durch `div` — aber nur im else-Zweig der drei Ternäre, die im if-Zweig
  `details` rendern (Admonition und die zwei `prf`-Fassungen). Grund: `<aside>` heißt „am
  Rande verwandt“, und gängige Textextraktoren werfen es weg; gemessen fielen damit 94 von
  97 Kästen aus dem extrahierten Text, darunter sämtliche Definitionen der beiden
  Hintergrundkapitel. Nach dem Umbau kommen sie an (`hintergrundwissen-analysis` 736 auf
  1420 Wörter). Wer die Stelle sucht: Das Muster hängt an `"details"`, nicht an `"aside"` —
  das Wort steht dutzendfach in Tag-Listen fremder Bibliotheken.

  **Seit dem 2026-11-18 trägt die Admonition dazu `role="note"`** (dritter Audit, §3): Der
  Umbau hatte den Kästen ihre Rolle im Barrierefreiheitsbaum genommen, sie erschienen als
  `generic ''`. `<aside>` trug `complementary` — eine Landmarke, und 97 Landmarken in einem
  Buch sind ebenfalls schlecht; `role="note"` ist die Rolle eines Merkkastens und keine
  Landmarke. Gezählt im Artefakt: **51 `role="note"` plus 10 `<details>` gleich 61
  Admonition-Kästen.** Die Extraktion ändert sich dadurch nicht, an sieben Seiten
  gegengeprüft (buchweit 52.012 Wörter, Differenz zur Messung ohne Rolle: null).

  **Die beiden `prf`-Fassungen bekommen die Rolle ausdrücklich nicht.** `role="note"` heißt
  in ARIA „parenthetic or ancillary to the main content"; eine Definition oder ein Satz ist
  in einem Lehrbuch der Hauptinhalt, die Rolle wäre dort falsch — und zwar für 47 der 108
  Kästen. Richtig wäre `role="group"` mit einem Namen aus der Kopfzeile, das verlangt aber
  eine `id` am Titel, die das Theme nicht vergibt. Unterschieden werden die drei Ternäre an
  der Form ihres Props-Objekts: Admonition `{className:…}`, `prf` `{id:…}`, in beiden
  Bündeln 1 und 2.
* **`{prf:…}`-Kästen heißen auf Englisch.** mystmd und das Site-Template schreiben den
  Kastennamen aus dem `kind`: „Example 1“, „Theorem 2“, im HTML wie im PDF, ohne Rücksicht
  auf die Sprache. Repariert an zwei Stellen, beide als Patch, der laut scheitert, wenn sich
  die Quelle bewegt: `devnotes/patch_myst_tex.py` (Abschnitt 3, die `\newtheorem`-Namen im
  PDF) und `_site/vendor/install_template.py` (der Kastenkopf im Template, im Bündel für
  den Server *und* in dem für den Browser – sonst schreibt die Hydration das Englische
  zurück). **Wer einen dieser Texte ändert, löscht vorher
  `_build/templates/site/myst/book-theme`**: Das Skript hält sich an seinem eigenen
  Prüftext für erledigt, und das zwischengespeicherte Template trägt noch den alten
  deutschen Text – es meldet dann „Bedientext nicht gefunden – Template bewegt?“,
  obwohl sich nichts bewegt hat. In der CI wird ohnehin frisch entpackt. Wer die `.venv` neu aufsetzt oder das Template neu entpackt, bekommt beides von
  den Skripten wieder; wer sie überspringt, hat „Example“ zurück. Gegenprobe:
  `pdftotext exports/eidl-skript.pdf - | grep -cE '^(Example|Theorem) [0-9]'` muss 0 sein.
  Dasselbe Skript übersetzt seit dem 2026-11-02 die **Bedienung** des Templates (Suche,
  Sprunglinks, Download-Menü, Kopierknöpfe, Screenreader-Beschriftungen; Liste `BEDIENUNG`).
  Jede Ersetzung ist ein Muster *mit Kontext*, weil dieselben Wörter im Code auch
  Bezeichner sind („Search“ ist im Suchdialog ein Zustand), und muss im Server- und im
  Browser-Bündel gleich oft vorkommen. Ein Template-Update, das eine Stelle verschiebt,
  lässt das Skript scheitern statt halb englisch weiterzubauen.
* **jtex ersetzt seine Marken auch in LaTeX-Kommentaren.** Wer den Namen des
  Import-Platzhalters in einen `%`-Kommentar von `templates/tex/eidl-skript/template.tex`
  schreibt, bekommt den ganzen Import-Block ein zweites Mal in die `.tex` — elf „already
  defined“-Fehler, ein kaputtes PDF, kein Wort im HTML.

## Der Vorspann eines Kapitels

**Jedes Kapitel öffnet mit einem Einleitungsabsatz** (seit 2026-11-17, Audit §6.1/§4.1),
und zwar vor allem anderen. Die Reihenfolge im Vorspann ist:

1. `# Überschrift`
2. **Einleitungsabsatz**, zwei bis vier Sätze: was die Sache *ist* (eine Definition, kein
   Vorgeplänkel), dann was in diesem Kapitel damit geschieht.
3. optional eine kursive Zeile **`*Setzt voraus: …*`** mit Links auf die ein bis drei
   Kapitel, ohne die es nicht geht. Nur dort, wo es echte Voraussetzungen gibt — eine
   leere Pflichtzeile in jedem Kapitel wäre Formular, kein Hinweis. **16 der 29 Kapitel
   tragen eine** (seit dem 2026-11-18; vorher zehn, die sechs neuen aus §7 des dritten
   Audits). Verlinkt wird nur nach *hinten*: Ein Kapitel, das später im Buch steht, ist
   keine Voraussetzung, auch wenn die Einleitung es nennt — Kapitel 17 nennt GANs, und das
   ist Kapitel 22. Wo die Sache schärfer ist als das Kapitel, wird sie genannt („das
   Skalarprodukt und die Geradengleichung aus dem …"). Am Handy ist diese Zeile zudem der
   **einzige** Weiterweg aus dem ersten Bildschirm: Das Backprop-Kapitel hat dort 25 Links,
   davon drei auf andere Kapitel — genau die drei aus dieser Zeile.
4. Aufzeichnungszeile und Player, dann die Folienzeile (beides nur, wenn freigegeben).
5. die erste `##`-Überschrift.

Begründung aus dem Audit: Auf 20 von 29 Kapiteln folgte der Überschrift unmittelbar ein
`##` oder der Aufzeichnungsblock. Wer über eine Suchmaschine mitten im Buch ankommt — der
Normalfall für die Queries, die dieses Buch gewinnen kann —, las als erstes
„Historie: BLEU (2001)“ oder „Tensoren in PyTorch“ und erfuhr nirgends, worin er steckt;
bei „Autoencoder“ stand die Definition unter der Überschrift „Loss-Funktion“. Der Absatz
ist zugleich die Passage, die eine Antwortmaschine zitieren kann, und er steht **über**
dem Video, weil die ersten Wörter der Seite die Sache nennen sollen und nicht das Medium.

**Keine Nummern im Vorspann**, auch nicht „Kapitel 9 von 29“ oder „Teil 2“: Dieselbe
Regel wie bei Querverweisen (siehe unten) — die Nummern verschieben sich, zuletzt am
2026-11-04 für sechs Kapitel. Wo das Kapitel in der Folge steht, sagen die Seitenleiste,
das aufgeklappte Menü und, wo es sich anbietet, der erste Satz („Im letzten Kapitel …“).

`devnotes/check_doku.py` prüft Punkt 2 und die Reihenfolge; `devnotes/folienlinks.py`
hängt die Folienzeile ans Ende des Vorspanns.

## Das Ende eines Kapitels

Nach dem letzten Abschnitt, in dieser Reihenfolge: der Übungsabschnitt (wo es einen gibt),
die „Weiterlesen“-Box, dann zwei kursive Zeilen.

1. **Die Forumszeile** (seit 2026-11-18): „Frage zu diesem Kapitel?“ mit einem Link auf
   `https://hai.konradvoelkel.com/eidl/f/kapitel/<kennung>/`, dazu in einem Halbsatz, wer
   fragen und wer mitlesen kann. Die Kennung ist die **Seitenadresse des Kapitels** — aus
   `09-backpropagation.md` wird `backpropagation`. Das Forum ist hAInrich2
   (`~/files/work/__drafts/hainrich2`); es kennt genau diese 29 Kennungen, und sein Bau
   scheitert, wenn eine davon nicht mehr zum Skript passt. `check_doku.py` prüft hier die
   Gegenrichtung: genau ein Forumslink je Kapitel, und die Kennung darin gleich der
   Seitenadresse. Ein Tippfehler fiele sonst nirgends auf.
2. **Die Herkunftszeile**: Werktitel, Gattung, Autor, Lizenz im Klartext und der Link auf
   „Über dieses Skript“ (Punkt 1 des zweiten Audits). **Stand und zitierfähige Adresse
   trägt `tools/zitierzeile.py` beim Veröffentlichen nach** (seit 2026-11-18), nicht die
   Quelle: Die Adresse darf dort nicht stehen (keine absoluten URLs auf die eigene
   Domain), und das Datum soll sich nicht von Hand pflegen lassen müssen. Im PDF fehlt
   beides deshalb.

Die vier Seiten außerhalb der Kapitel — Startseite, Glossar, „Über dieses Skript“,
Übungsblätter — bekommen **keine** Forumszeile; dafür gibt es drüben keine Seite.
**Die Herkunftszeile tragen `glossar.md` und `uebungsblaetter.md` dagegen seit dem
2026-11-18** (dritter Audit, §4): Dort stand die Lizenz nirgends im Text, und das Glossar
ist mit gut 2.100 extrahierten Wörtern und seinem `DefinedTermSet` die Seite, die eine
Antwortmaschine am ehesten begriffsweise zitiert. Die Links sind dort wurzelrelativ
(`index.md`, `README.md`) und nicht `../`, und die Zeile beginnt mit „Dieses Glossar“ bzw.
„Diese Seite“ statt „Dieses Kapitel“. Startseite und „Über dieses Skript“ brauchen sie
nicht — die eine *ist* das Werk, die andere erklärt es.

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

## Vorlesungsaufzeichnungen

Die Aufzeichnungen liegen in der HHU-Mediathek, **eine Playlist je Durchgang**. Der Kanal
„Einführung in Deep Learning“ (Kanal 194) mischt die Jahrgänge und wird nirgends mehr verlinkt
(Entscheidung Konrad, 2026-10-20 — dieselbe im Skript, in ILIAS und auf der Website);
2024/25 wird nicht mehr beworben. Verlinkt sind genau zwei Playlists, der laufende
Durchgang zuerst: `README.md` (Abschnitt „Vorlesungsaufzeichnungen“) und
`kurs-2026-27.md` nennen sie, dieselben Adressen stehen in `../ilias/runs/ws2026-27.yaml`
unter `external:`.

**Je Vorlesung eine Zeile im Kapitel**, im Vorspann unter dem Einleitungsabsatz (siehe
„Der Vorspann eines Kapitels“ weiter unten; bis zum 2026-11-17 stand sie direkt unter der
`#`-Überschrift), nach dem Muster des Data-Science-Skripts
(`~/Sciebo/hhu/ds2026/ds-skript`, dort `erwartungswert.md`):

```markdown
[Vorlesungsaufzeichnung VL 1: Überblick](https://media.hhu.de/video/einfuehrung-in-deep-learning-202627-vl-1-ueberblick/<hash>)

:::{anywidget} ../widgets/mediathek.mjs
{url: 'https://media.hhu.de/video/einfuehrung-in-deep-learning-202627-vl-1-ueberblick/<hash>'}
:::
```

* **Darunter der eingeklappte Player** (seit 2026-11-03, `widgets/mediathek.mjs`): ein
  Kasten „Aufzeichnung hier abspielen“, erst der Klick lädt den Player der Mediathek
  (`/media/embed?key=…&chapters=true`, mit derselben Startzeit `t`). Wer nur liest, lädt
  nichts von `media.hhu.de`; im PDF steht die Linkzeile allein. Die Adresse steht damit
  zweimal im Kapitel, **Zeichen für Zeichen gleich** — `check_doku.py` prüft das und
  meldet auch eine Linkzeile ohne Player darunter.
* Welches Kapitel zu welcher Sitzung gehört, sagt die Tabelle in `kurs-2026-27.md`. Deckt
  eine Sitzung zwei Kapitel ab, bekommt jedes seine Zeile; beginnt das Thema mitten im
  Video, kommt `?t=<sekunden>` an die Adresse (so macht es das DS-Skript).
* **Nachgetragen wird, sobald die Aufzeichnung in der Playlist auftaucht**, in der Regel in
  der Woche nach der Sitzung. **Zum selben Handgriff gehört die Freigabe des Decks**: die
  Nummer in `slides/freigegeben.txt` eintragen und `python3 devnotes/folienlinks.py
  --schreiben` laufen lassen, dann steht die Folienzeile im Kapitel und das PDF
  unter der Adresse `vlNN.pdf` im Ordner `folien` der Website. Vorher ist beides absichtlich nicht da – ein Deck wird veröffentlicht, wenn
  es durchgesehen ist, nicht wenn es gebaut ist.
  **Vorher die Decks neu bauen** (`cd slides && ./build.sh`): `folienlinks.py` zählt die
  Seiten im **lokal gebauten** PDF, der `pages`-Job im CI baut aber aus der Quelle. Ein altes
  lokales PDF schreibt deshalb still falsche Bereiche in *alle* freigegebenen Kapitel — am
  2026-11-18 wurde VL 5 so von „S. 2–20 / 21–34" auf „2–14 / 15–21" gesetzt, weil das lokale
  Deck noch der Stand vom 04.11. ohne die Reveals war. `--check` im CI hätte es gemeldet,
  der lokale Lauf nicht.
* **Und das ausgegebene Übungsblatt**: `blattNN.pdf` aus `../exercises/` nach `blaetter/`
  kopieren und die Zeile in `uebungsblaetter.md` ergänzen, sobald das Blatt in ILIAS
  ausgegeben ist. Gebaut wird es dort mit `./build.sh blattNN`; **nie** die
  Lösungsfassung mitkopieren. `check_doku.py` prüft beides. Dieselbe Adresse gehört in die Wochentabelle in ILIAS
  (`../ilias/runs/ws2026-27.yaml`, `schedule.weeks[].material`) — ein Arbeitsschritt, zwei
  Stellen. **Und dazu Kapitelmarken in der Mediathek** (seit 2026-11-02 fester Teil dieses
  Schritts): rund 8–12 je 90 Minuten, eine je Folienblock bzw. `##`-Abschnitt, Titel nach
  den Folientiteln. Setzen kann sie nur Konrad eingeloggt, unter
  `https://media.hhu.de/webplayer/formchapters/key/<hash>` (eine Marke je Absenden,
  Sprache Deutsch, Zeit `HH:MM:SS`) — vorbereitet wird die Liste, eingetragen erst nach
  Konrads Freigabe. Die Zeiten werden **gemessen, nicht geschätzt**: Video in 480p von
  `https://media.hhu.de/getMedium/<hash>.mp4?format=480p` nach
  `/media/konrad/xtraspace/eidl-videos/2026/`, Kontaktbögen mit einem Bild alle 30 s zum
  Zuordnen, dann die Bilddifferenz im Titelband alle 5 s für die Sekunde des Wechsels
  (OCR der Folientitel taugt nicht). Die Marke liegt auf dem ersten Bild der neuen Folie,
  und ein `?t=` im Kapitel nennt dieselbe Sekunde wie die passende Marke. Die
  Vorschaubilder der Kapitelleiste stammen aus einem Raster von etwa einem Bild pro
  Minute und zeigen oft noch die vorige Folie — das lässt sich nicht wegschieben. Ein
  eingebetteter Player zeigt die Marken nur mit `&chapters=true` in der Embed-Adresse.
  **Ebenso Untertitel** (seit 2026-11-02, zuerst VL 3): faster-whisper large-v3 mit
  Wortzeitstempeln, geschnitten auf höchstens 84 Zeichen und 7 s je Untertitel, dann eine
  Bereinigung durch Opus, die nur korrigiert (Fachbegriffe, Rechtschreibung, Füllwörter)
  und Zeiten und Anzahl erhält — geprüft per Skript, Änderungen als Vorher-nachher-Liste
  an Konrad, hochgeladen erst nach seinem Ja über `/webPlayerSubtitles/upload/key/<hash>`
  (`.srt` oder `.vtt`, Sprache Deutsch). Die Mediathek bricht die Zeilen selbst neu um.
  **Vorher auf ganze Sekunden runden** (`untertitel_ganze_sekunden.py`): Die Mediathek
  verdirbt ab Minute 1 die Millisekunden, und kurze Untertitel bekommen dann Anfang gleich
  Ende — bis zum 2026-11-02 waren so 11 bis 21 je Video unsichtbar. Geprüft wird an der
  ausgelieferten VTT, und zwar an den Zeiten, nicht nur an Text und Anzahl (PLAYBOOK §3.13).
  Die Whisper-GPU teilt sich die Maschine mit Ollama; ist sie belegt, warten. **Und die
  Gegenrichtung:** In der Beschreibung des Videos je behandeltes Kapitel ein Link auf die
  Kapitelseite (beim zweiten Kapitel einer Sitzung mit „ab Minute n“), im Autorenfeld der
  Name als Link auf `https://www.konradvoelkel.com`; dazu Thumbnail im Kursdesign. Der
  ganze Ablauf, für alle Kurse: `~/Sciebo/hhu/PLAYBOOK.md` §3.13.
* **Die fünf SEO-Felder des Formulars** (`/media/edit/key/<hash>`: „SEO URL Titel“ und die
  vier Meta-Tag-Felder) sind nicht kosmetisch, und sie waren bis zum 2026-11-04 bei allen
  Videos leer. Geprüft und erzeugt wird das mit `devnotes/mediathek_seo.py`; im Docstring
  steht, was am 2026-11-04 an VL 1 gemessen wurde. Kurz:
  * **„SEO URL Titel“ (`media[slug]`) muß von Hand nachgezogen werden**: Der Vorschlag der
    Mediathek **löscht** Umlaute statt sie umzuschreiben („einfhrung“). Dieselbe Löschung
    steckt unverbesserlich in der `video:description` des Sitemaps („berblick ber die
    Vorlesung“) — die ist Sache der Mediathek. Der Slug ist die Adresse, die die Mediathek
    selbst als `<video:player_loc>` ins Sitemap schreibt, also die, die Google Video kennt;
    gleichzeitig hat die Videoseite **kein Canonical**, und *jeder* Slug mit dem richtigen
    Hash liefert dieselbe Seite. Deshalb immer dieselbe Schreibweise verlinken. Ein Tippfehler
    im Titel wandert in den Slug, und eine Titelkorrektur zieht den Slug **nicht** mit (VL 4,
    2026-11-04: Titel „2025/26“ berichtigt, Slug blieb `…-202526-…`).
  * **`meta_description` ist der Ertrag**: Ist das Feld leer, füllt die Seite
    `<meta name="description">` aus der Beschreibung **samt escapeten HTML-Tags** — der
    Suchtreffer-Text beginnt mit „<p>“. Hinein gehört das `description:` aus dem Frontmatter
    des Kapitels, das die Aufzeichnung verlinkt (80–155 Zeichen, von `check_doku.py` geprüft).
  * `meta_author` und `meta_copyright` füllen, die Tags fehlen sonst ganz. `meta_keywords`
    **ersetzt** die Hausliste der Mediathek, ergänzt sie nicht — Tag und Hausbegriffe also
    mitnehmen. `meta_title` landet nur in `<meta name="title">`, das Suchmaschinen nicht
    lesen; der `<title>` kommt weiter aus `media[title]`.
* **Die Adresse wird nicht geraten.** Sie steht in der Playlist selbst oder in der
  Titelsuche <https://media.hhu.de/search/title/Einf%C3%BChrung+in+Deep+Learning+2026/>.
  Zwei Eigenheiten der Mediathek: Playlist-Adressen antworten mit **302** und landen beim
  ersten Video der Liste, eine Prüfung läuft also mit `curl -sIL` und nicht ohne `-L`; und
  Playlists sind nirgends auffindbar (die Kanalseite verlinkt keine, die Titelsuche liefert
  nur einzelne Videos) — eine weitere Playlist-Adresse muss Konrad schicken.

## Übungen

Jedes Kapitel, dem eine sinnvolle Aufgabe zuzuordnen ist, endet mit einem Abschnitt
`## Übung` **vor** der „Weiterlesen“-Box. 23 der 29 Kapitel haben einen; 04, 17, 21 und 22
haben bewusst keinen, weil eine schwache Übung schlechter ist als keine, und die beiden
Hintergrundkapitel keinen, weil ihre Aufgaben auf den Übungsblättern stehen. Die Form:

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
   Lösungsvorschlägen, die damit veröffentlicht waren.
   **Seit dem 2026-11-05 liegt das fertige PDF eines Blatts trotzdem auf der Website**
   (`blaetter/`, verlinkt von `uebungsblaetter.md` im Anhang) — und zwar erst, wenn das
   Blatt in ILIAS ausgegeben ist. Das ist kein Rückschritt, sondern genau die Trennung,
   um die es ging: Gepflegt wird weiter nur die TeX-Quelle, im Buch steht keine zweite
   Fassung der Aufgaben, und die Lösungen bleiben draußen. Die TeX-Quellen enthalten sie
   (der Wrapper schaltet sie ein) und dürfen deshalb **nicht** ins Repository; was hinein
   darf, ist das gebaute Blatt-PDF. `.gitignore` und `check_doku.py` sichern das doppelt. Seit dem 2026-09-27 sind sie aus dem
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
* **Den Buchtitel in `myst.yml` geändert und die Vorschaukarte vergessen.** Die Karte
  ist ein eingechecktes PNG; sie zeigt den alten Titel weiter, bis jemand sie neu
  erzeugt. `tools/social_card.py --verify` meldet das (es liest den Titel aus dem
  tEXt-Block der PNG) und läuft deshalb im `myst-build`-Job.
* **`SITE_ORIGIN` geändert und die Schwesterrepos vergessen.** Der `@id` folgt
  `SITE_ORIGIN` von selbst — aber `ds-en`, `ds-skript` und `konradvoelkel.com` nennen
  dieses Buch bei demselben `@id`, und der muss derselbe bleiben, sonst beschreiben die
  vier Seiten zwei Werke statt eines.
* **Eine Abbildung mit unlesbarem Text eingecheckt.** Buchbau, PDF-Prüfung und
  Byte-Vergleich sehen keine Bildinhalte: Das Autoencoder-Schema hatte vom 2026-09-17 bis
  zum 2026-11-02 drei übereinanderliegende Überschriften und Pfeile durch „Encoder“ und
  „Decoder“, und nichts wurde rot. Ursache war `set_aspect("equal")` in `draw_layers`, das
  die Zeichenfläche nach dem Netz statt nach `figsize` formt. Seitdem prüft `save()` in
  `make_figures.py` jede Abbildung (Textabstände, Pfeile durch Text, Text in seiner Form,
  Panel-Titel) und endet bei einem Befund mit Fehlercode. Die erste Runde samt Durchsicht
  von Hand fand Mängel in 19 weiteren Abbildungen. **Was sie nicht sieht** (Text in Markern, Legende über der
  wichtigen Stelle, Abbildungen von außerhalb wie Notebook- und Paper-Bilder), sieht nur, wer
  **jede geänderte PNG einmal öffnet** – das gehört zu jeder Änderung an einer Abbildung,
  genauso wie der Blick auf die Foliensätze, die dieselbe PNG einbinden (`grep -l <name>
  slides/*.tex`, dann `slides/build.sh`).
* **`uv sync` gemacht und den mystmd-Patch vergessen.** Dann sind alle Kommandozeilen im
  lokal gebauten PDF falsch, und zwar unauffällig.
