# Erledigt — eidl-skript

Die Erledigt-Historie, am 2026-09-27 aus `TODO.md` herausgelöst. Dort stehen nur noch die
offenen Punkte; hier steht, was erledigt wurde und warum — das erklärt manche Entscheidung,
die sonst willkürlich aussieht.

Datierte Protokolle größerer Umbauten liegen daneben als `build-log-<datum>.md`.

## Nach Themen (aus den Abschnitten von `TODO.md`)

### Inhalt (Skript)

- [x] **Fachliche Durchsicht der Prosafassung**, abgeschlossen am 2026-09-29: alle 27 Kapitel und das
  Glossar auf den drei Achsen A1 (stimmt es), A2 (passt es zu Plan, Folien, Klausur) und A3 (trägt es
  beim Lesen). **Alle 126 Formelblöcke nachgerechnet**, jede Bibliotheksaussage gegen die `.venv`
  geprüft, jede Quelle gegen Modellkarte, arXiv-API oder Verlagsscan. Gefunden und behoben: 31 F,
  8 N, 30 K. Die schwersten waren die, die beim Nachbauen zubeißen und nichts melden — zwei ReLUs,
  die keinen Buckel ergeben können (Kap. 13); `ReLU(x)+ReLU(y)` gegen `ReLU(x+y)` (12); Softmax
  zweimal, im Modell *und* in `CrossEntropyLoss` (14); der DoG-Filter als erste statt zweiter
  Ableitung (20); `nn.Embedding` transponiert (16); BPE ohne Iterationsschritt (19). Dazu die
  Lernrate auf ein Symbol vereinheitlicht (Skript *und* VL-02-Folie) und zwei Markup-Fallen neu in
  `CLAUDE.md`. Protokoll mit Gegenrechnung je Befund: `devnotes/durchsicht/durchsicht-2026-10.md`
  (gitignored). Nachfolger ist der Sprachdurchgang, siehe `TODO.md`.
- [x] **Die Antwortenbox in Kapitel 01** (drei Fragen zum HPCwire-Artikel, im PDF offen): Entscheidung
  Konrad 2026-09-27 — **so lassen**. Es ist kein Vertraulichkeitsproblem, nur ein didaktisches, und die
  Fragen stehen ohnehin direkt darüber.

- [x] Termine, Räume und Verteilung geklärt am 2026-09-24 (Quelle LSF 278733): Vorlesung Mi 12:30–14:00 in
  HS 5E (25.21), 14.10.2026–03.02.2027; Übung Do 10:30–12:00 in 25.22.U1.52, ab der ersten Woche. Material und
  Abgaben über **ILIAS** (Kurs 2165367); Fragen laufen über den Rocket.Chat-Kanal `#eidl-2026` (angelegt
  2026-09-25, Einladungslink ohne Ablauf), inhaltlich wie organisatorisch – kein Forum.
- [x] **Übungsleitung 2026/27: Konrad selbst** (2026-09-24). Elisa Kleinfeld steht in LSF als „begleitend“,
  korrigiert aber nur die Übungsblätter und hält die Übungsgruppe nicht. Die ILIAS-Kursseite nennt – wie
  2025/26 – niemanden namentlich.

### Vorlesungsplan (`kurs-2026-27.md`)

- [x] VL-Tabelle am 2026-09-20 aus dem *Ist* der Aufzeichnungen 2025 neu gebaut (Entscheidung Konrad): jede Woche
  nur, was 2025 in 90 Minuten geschafft wurde; VL 1 ohne Perzeptron, VL 5 = Loss + Gradientenabstieg, VL 6 nur
  Backpropagation, Transformer komplett in VL 10, „Optimierer“ (26) und „Adversarial Attacks“ (27) als Reserve.

### Übungsblätter

- [x] **Lösungsvorschläge aus dem Skript heraus** (2026-09-27, auf Konrads Hinweis): 15 Blöcke aus den
  Blättern 0, 1, 3 und 5 herausgenommen (heute in `uebungen-2025/loesungen/`) — ein Ordner wie
  `transcripts/`, in Sciebo, aber nicht im Repo. Vorher standen sie im veröffentlichten PDF (aufgeklappt, nicht einmal versteckt) und
  auf der Website als aufklappbare Box. PDF jetzt 133 statt 137 Seiten, `grep -c Lösungsvorschlag` = 0.
- [x] **Entschieden am 2026-09-27: `part-exercises/` ganz aus dem TOC**, statt dessen pro Kapitel ein
  kleiner Übungsabschnitt. Die zwölf Blätter liegen in `uebungen-2025/blaetter/` (gitignored, Sciebo),
  die Lösungen daneben. PDF dadurch 110 statt 133 Seiten; `--min-pages` im `build-pdf`-Job auf 100.
- [x] **`notebooks/latent-classifier.ipynb`** hängt seit 2026-09-27 als `downloads:` am Kapitel
  „LLMs benutzen“ (21) statt am früheren Blatt 11; die Kapitel 21 und 27 verweisen darauf.
- [x] **Die 23 Übungsabschnitte sind eingebaut** (2026-09-27): je ein `## Übung` vor der
  „Weiterlesen“-Box, ein bis drei Aufgaben, ein `Tipp:` je Aufgabe, keine Lösung, statt dessen eine
  Antwortprobe. 04, 17, 21 und 22 haben bewusst keinen. Das Vorschlagsdokument
  `uebungen-pro-kapitel.md` ist damit aufgegangen und gelöscht; die Form steht jetzt in `CLAUDE.md`.
  Kapitel 09 hatte schon eine eigene Übungsaufgabe am Ende — die ist in den Abschnitt gewandert.
- [x] **Historie umgeschrieben** (2026-09-27, Konrads Entscheidung — niemand sonst hat eine Kopie des
  Repos). `git filter-repo --path part-exercises/ --invert-paths` über alle 61 Commits, danach
  force-push auf `main`. Damit sind die Lösungsvorschläge auch aus der Vergangenheit des öffentlichen
  Repos verschwunden. Sicherung der alten Historie:
  `~/files/work/__backups/eidl-skript/eidl-skript-vor-history-rewrite-2026-09-27.bundle`.
  **Zu beachten:** GitLab hält die alten Objekte noch eine Weile vor — sie sind über ihre SHA
  erreichbar, bis die Housekeeping-Läufe sie einsammeln. Wer sicher gehen will, stößt in den
  Projekteinstellungen unter *Settings → Repository → Housekeeping* einen Lauf an.
- [x] **Abgabetermine 2026/27 bestätigt (Konrad, 2026-09-24)** und in ILIAS eingetragen: Blatt 0 ohne Abgabe;
  1: 21.10., 2: 28.10., 3: 04.11., 4: 11.11., 5: 18.11., 6: 25.11., 7: 02.12., 8: 09.12., 9: 16.12.2026,
  10: 13.01., 11: 20.01.2027, Probeklausur als Take-Home mit Abgabe 27.01.2027 — jeweils Mittwoch 12:00.
- [x] **[Entscheidung 2026-09-20]** Englische Fassungen (`sheetNN.tex`) fallen weg, solange die Vorlesung deutsch
  ist.

### Klausur

- [x] Termine aus LSF (2026-09-24): **Erstklausur Do 11.02.2027**, LSF-Fenster 8:30–11:30, Hörsäle 5F (25.21)
  und 2D (22.01); **Zweitklausur Mo 15.03.2027**, Fenster 8:30–11:30, Hörsaal 5D (25.21). Geschrieben wird
  jeweils 9:00–10:30 (90 Minuten, Entscheidung Konrad 2026-09-24); so steht es auf der ILIAS-Seite.

### Notebooks

- [x] **Alle 24 Python-Blöcke am 2026-09-24 ausgeführt** (Venv auf `/media/konrad/xtraspace/eidl-venv`, CPU).
  Ergebnis und Korrekturen: `codecheck-2026-09-24.md`. Kurz: `import torch` in „Autograd“ (10) ergänzt,
  Beispieldaten in „Logistische Regression“ (06), Imports + `IMAGESIZE` in „Autoencoder“ (14), `data` aus
  `ASML.csv` in „Faltung und CNNs“ (20), gemessene Wahrscheinlichkeiten in „LLMs benutzen“ (21);
  `ollama`, `pydantic`, `sacremoses` in `pyproject.toml` nachgetragen.
- [x] **[Entscheidung 2026-09-25] Autoencoder-Training (14) bleibt wie es ist.** Mit SGD `lr=1e-2` und
  15 Epochen sinkt der MSE nur von 0.231 auf 0.228, die Rekonstruktion bleibt Matsch – und genau das soll man
  einmal gesehen haben, bevor die Tricks-Liste (mehr Epochen, Lernrate, Adam) danach aufräumt. Gemessene
  Vergleichswerte für den Hörsaal: SGD `lr=1e-1` → 0.072, Adam `lr=1e-3` → 0.019.

### Beamer-Folien (Schritt 4 des Migrationsplans)

- [x] **[Entscheidung 2026-09-20]** Die Folien 2026/27 werden **aus dem Skript heraus neu erzeugt**, nicht aus den
  Google-Slides 2025. Grund: Von neun Unstimmigkeiten, die 2025 im Hörsaal auffielen, waren fünf Folienfehler, die
  das Skript schon richtig hat (Softmax-Minus, BLEU-Mittel, Wasserstein-Wertebereich, Top-k-Vergleichszeichen,
  Softmax-Abstand in „Latente Räume“).
- [x] **Alle 15 Decks stehen** (2026-09-25, `slides/`): ein Deck pro Vorlesungswoche, gebaut aus den Kapiteln
  laut `kurs-2026-27.md`, gemeinsamer Header, Bilder per `\graphicspath` direkt aus `images/`. Alle bauen mit
  `latexmk -lualatex` ohne zu volle Rahmen (14–23 Folien je Deck). Textarm gehalten: die Folie ist der
  Gesprächsanlass, die Ausführung steht in `\note{}`.
- [x] **Durchsicht der Decks 2026-09-25** (`folien-review-2026-09-25.md`), am selben Tag umgesetzt: Schrift
  (Source Sans Pro statt Serifen-Fallback, Mathe kursiv), Frametitle mit Breitenbegrenzung, drei Titel
  gekürzt, Item-Labels als `description`, Blatt-Verweise ohne Nummern („Übungsblatt“), Codezeile VL 3,
  `build.sh`-Glob.
- [x] **VL 1 gegengelesen und nachgezogen** (2026-10-02, `folien-review-vl01-2026-10-02.md`): Ablaufplan in
  Deck-Reihenfolge (Definition vor Semesterplan; Befund A4 für dieses Deck), Notizseite ohne Vorschaubild in
  `\scriptsize` (Befund A5, im Header, gilt für alle Decks), Auflösung der Quizfrage als Folie „Training,
  Validation, Test“ und als Absatz im Kapitel (das Glossar verwies dafür auf ein Kapitel, in dem das Wort
  nicht vorkam), Take-Home-Folie, „Note: nur die Klausur, ohne Hilfsmittel“ auf der Organisatorisches-Folie,
  Folie 2010–2015 mit Halbsätzen und einem lesbaren Bild statt drei Briefmarken, Mark-I-Foto mit deutscher
  Unterschrift und Bildnachweis (`slides/README.md`), „2021 Diffusionsmodelle schlagen GANs“ mit DDPM 2020
  in Notiz und Kapitel, Vibecoding, PyTorch ohne `\texttt`, „dynamisch typisiert“. Im Header `german.sty`
  durch babel ersetzt – vorher trennte kein Deck Silben, das Log sagte es in einer Zeile –, `\emph` in der
  Markenfarbe `#6f59a6`, `pdfsubject`. Die Umfrage-Ansage war falsch: Das ILIAS-Fenster schließt um 13:55,
  die Notiz sagte „bis morgen“. Gegenprobe: 16 Decks bauen, Seitenzahlen unverändert (VL 1: 23 → 25), 0 zu
  volle Rahmen, Sprachprüfungen null, HTML-Bau ohne Warnungen.
- [x] **VL 2 gegengelesen und nachgezogen** (2026-10-02, `folien-review-vl02-2026-10-02.md`): σ gegen τ auf
  zwei Folien und in der Neuron-Abbildung (Wurzel `make_figures.py`, das Bild steht auch im Kapitel und in
  VL 1), neue Folien „XOR, aufgelöst“ (mit dem VL-7-Bild) und „Die fünf Antworten für das Perzeptron“ als
  Take-Home, Bias-Update auf der Drei-Fälle-Folie, Zwei-Panel-Abbildung für die Regel bei der Arbeit, die
  drei Hörsaalfragen von 2025 in den Notizen, Hugging-Face-Ausblick, Iris auf der Blattfolie. Gegenprobe:
  20 → 22 Folien, 0 zu volle Rahmen, Notizenfassung passt, Sprachprüfung null, HTML-Bau ohne Warnungen.
- [x] Dozentennotizen sind in den Decks (2026-09-25): je Folie ein `\note{}` mit den Dialogmustern aus
  `transcripts/*/notiz.md`, dazu auf jeder Titelfolie ein Minuten-Ablaufplan aus der jeweiligen Aufzeichnung.
  Drin sind u.a. der Type-Check (VL 2), die offen gehaltene Zufalls-Frage (VL 5), „Quizfrage nicht auflösen“
  (VL 1), „beim GAN Lab früh aufhören“ (VL 13) und die Vibecoding-Vorbereitung (VL 15).
- [x] Externe Werkzeuge am 2026-09-24 geprüft: TensorFlow Playground (09), Loss Landscape Explorer (08),
  GAN Lab (22), Ollama (21) antworten alle mit 200. Ebenso alle 67 externen Links im Skript – bis auf einen
  toten (`muhark.github.io`, word2vec from scratch), jetzt ersetzt durch das offizielle PyTorch-Tutorial
  „Word Embeddings: Encoding Lexical Semantics“. Der HPCwire-Artikel (01) blockt `curl` mit 403, im Browser
  ist er da. Vor jedem Semester wiederholen.

### ILIAS (Kurs 2026/27, ref_id 2165367)

- [x] Am 2026-09-24 aufgesetzt: Objekte und Seitengestaltung aus dem Kurs 2025/26 (1948423) übernommen
  (Lösungshinweise-Dateien dabei ausgelassen), Kursseite auf 2026/27 umgeschrieben (Ankündigung, Raum und Zeit,
  Themenliste, Material mit Skript-Link, Externe Resourcen inkl. UDL/MML, 19-zeilige Wochentabelle),
  Übungstermine für alle 12 Übungseinheiten gesetzt, Umfragefenster gesetzt,
  Kalender und Neuigkeiten deaktiviert. Der Kurs ist noch **offline**.
- [x] Am 2026-09-25 umgestellt: Absatz „Raum und Zeit“ verlinkt den Rocket.Chat-Kanal `#eidl-2026`
  samt Einladungslink, das Forum-Objekt ist gelöscht (der Block „Foren“ verschwand mit ihm).

### Infrastruktur

- [x] **Abbildungen hingen am System-Python** (2026-10-14). `make_figures.py` lief laut eigenem
  Skriptkopf gegen das System-Python; dessen matplotlib (3.10.9) war eine andere Fassung als die
  in `uv.lock` angeheftete (3.11.2), und ein *unveränderter* Komplettlauf schrieb Abbildungen neu,
  an denen niemand etwas getan hatte — die echte Änderung war vom Fassungsrauschen nicht mehr zu
  trennen. Behoben mit einer Abhängigkeitsgruppe `figures` in `pyproject.toml` (ohne torch, 18
  Pakete) und `matplotlib>=3.11.2,<3.12` auch in den Hauptabhängigkeiten. Aufruf jetzt
  `uv run --only-group figures devnotes/make_figures.py`. Einmalige Neubasierung aller PNGs
  unter der angehefteten Fassung; Gegenprobe: zwei Läufe hintereinander sind byte-gleich.
  (Es waren 29 von 36 — der Lauf brach damals an einem veralteten Pfad ab und erreichte die
  letzten fünf nicht, siehe den Eintrag vom 2026-10-16.)
  Gefunden beim Beschriftungsfehler der GMM-Abbildung (Achse „Pixelwert“, die von −0,5 bis 1,5 lief).
- [x] **Die Seitenzahl-Abweichung ist erklärt, nicht verschwunden** (2026-10-16). Am 2026-10-14
  stand hier, sie sei „von selbst“ weg (lokal wie live 113, Debian habe bei texlive nachgezogen).
  Das war falsch, und `check_doku.py` hat es am Tag darauf gemeldet: Lokal sind es wieder 112.
  Nachgemessen in einem `git worktree` mit eigener `.venv` — derselbe Baum baut mit mystmd 1.10.1
  wie mit 1.11.0 112 Seiten, und auch der Baum vom 2026-10-02, der am 14.10. mit 113 gemessen
  wurde, baut heute 112. Die Ursache ist nicht der Debian-Stand: Diese Maschine benutzt Debians
  texlive überhaupt nicht, sondern eine eigene TeX-Live-2024-Installation unter
  `/usr/local/texlive/2024` (unangetastet seit 2024-06-08, `texlive-latex-extra` steht auf `rc`)
  mit **minted v2.9**, während das Image Debian trixies **minted v3** benutzt. `breaklines` bricht
  dort anders; sichtbar als ein Codeblock der Trainingsschleife auf Seite 28. Die Abweichung
  bleibt also bestehen und ist dokumentiert statt offen: `../CLAUDE.md`, PLAYBOOK §3.8m,
  Messwerte in `build-log-2026-10-15.md`. Was am 14.10. zu der 113 geführt hat, ließ sich nicht
  rekonstruieren — festgehalten ist, was reproduzierbar ist.
- [x] **Abhängigkeiten angehoben** (2026-10-15): mystmd 1.10.1 auf 1.11.0 an **beiden**
  Anheftungen (dev-Gruppe und Dockerfile), dazu numpy, torch, transformers, huggingface-hub 2.x
  und 47 weitere Pakete im Lock. Gleiche Quelle, neue Toolchain, nichts verschoben; die drei
  Patchstellen von `patch_myst_tex.py` gibt es in 1.11.0 noch. Nach dem Push geprüft, dass das
  Image wirklich neu gebaut wurde: `myst.xref.json` der veröffentlichten Seite meldet 1.11.0.
  Protokoll: `build-log-2026-10-15.md`.
- [x] **`make_figures.py` lief nur bis Abbildung 29 von 36** (2026-10-16). `SRC` zeigte auf
  `from_2025/slides` neben dem Buch — ein Ordner aus der Zeit vor den Jahresordnern, der nicht
  mehr existiert. Weil `vl10_asml_convolutions` alphabetisch die dreißigste Abbildung ist, brach
  der Lauf dort mit einem `FileNotFoundError` ab und erreichte die letzten fünf nie; aufgefallen
  ist es erst bei der Gegenprobe zum Upgrade. Jetzt sucht das Skript den Ordner unter beiden
  Namen (`eidl-25/slides` zuerst), liest die Kurstabelle aus dem versionierten
  `notebooks/ASML.csv` statt aus Sciebo (byte-gleich geprüft) und läuft bei fehlendem Material
  **weiter**, nennt am Ende, was fehlte, und endet trotzdem mit Exit 1 — eine Fremddatei
  verschluckt nicht mehr die Abbildungen danach. Gegenprobe: voller Lauf, 36 Abbildungen und
  6 Kopien, `git status images/` leer.
- [x] **`make_figures.py` ist ruff-sauber** (2026-10-16): der ungenutzte `Rectangle`-Import, die
  ungenutzte Rückgabe von `draw_layers` (der andere Aufrufer verwirft sie auch), drei
  `dict()`-Aufrufe als Literale, und das x-Bit gesetzt, weil die Shebang-Zeile es behauptete.
  Gegenprobe: voller Lauf, `git status images/` leer — keine Abbildung ändert sich dadurch.
  **Nicht** `ruff format` laufen lassen: Das ist in diesem Repo keine Konvention (alle zwölf
  Skripte in `devnotes/` würden umgeschrieben, hier allein 474 Zeilen), und eine einzelne
  formatierte Datei macht die Sammlung uneinheitlicher, nicht einheitlicher. Offen bleiben
  dieselben `EXE001` in fünf Geschwisterskripten und ein Dutzend Befunde anderer Klassen,
  siehe `TODO.md`.
- [x] **Der verwaiste Worktree ist weg** (2026-10-16). `.claude/worktrees/silly-archimedes-470c08`
  stand seit dem 2026-10-02 auf `c7db5c4` (detached), 75 MB. Nachgesehen, bevor er gelöscht wurde:
  nichts Geändertes, nichts Unversioniertes, HEAD und Branch `claude/silly-archimedes-470c08`
  vollständig in `main`; an Eigenem lagen dort nur Artefakte — eine `.venv`, `__pycache__` und
  die Beamer-Ausgaben von VL 01 (23 Seiten, Stand 2026-09-30, inzwischen 25) und VL 03, deren
  `.tex` seither um 523 Zeilen weiter ist. Der Branch war merged und ist mit entfernt; zurück
  holen ließe er sich mit `git branch claude/silly-archimedes-470c08 c7db5c4`.
- [x] **`scipy` steht in den Hauptabhängigkeiten** (2026-10-16). Das CNN-Kapitel schreibt
  `from scipy.signal import convolve`; scipy kam nur als Abhängigkeit von gensim und
  scikit-learn mit, in der Gruppe `figures` stand es seit dem 2026-10-14. Jetzt
  `scipy>=1.18,<2` mit Kommentar auf das Kapitel — dieselbe Form wie bei `sacremoses`. An der
  Auflösung ändert sich nichts (1.18.1 war schon installiert).
- [x] GitLab Pages auf „Everyone“ (Konrad, 2026-09-20); aktiv seit dem nächsten Pages-Deploy, geprüft 2026-09-21
  (`curl` → 200, PDF unter `/eidl-skript.pdf` erreichbar).
- [x] PDF-Export in der CI wie bei DS-/EiPy-Skript (2026-09-20): Job `build-pdf` mit `allow_failure`, PDF landet
  unter `public/eidl-skript.pdf` und ist auf `index.md` verlinkt. Dafür TeX Live ins CI-Image und ein eigenes
  Template `templates/tex/eidl-skript/` (plain_latex + amssymb, caption, babel ngerman, A4, HHU-Linkfarbe,
  DejaVu Sans Mono, Kapitel auf neuer Seite). Grund: `plain_latex` ignoriert die `preamble`-Option in `myst.yml`
  stillschweigend, deshalb waren `\mathbb` & Co. bisher undefiniert (248 LaTeX-Fehler, die latexmk durchwinkte).
  Jetzt 0 Fehler, 135 Seiten (A4). Ohne Docker lokal weiterhin `uv run --only-group dev myst build --pdf`.
- [x] **Template-Abgleich mit EiPy — abgeschlossen 2026-09-27.** Beide Bücher haben am selben Tag dasselbe Template
  weiterentwickelt und sind jetzt fast deckungsgleich; der gemeinsame Block steht als Referenz in
  `~/files/work/hhu/PLAYBOOK.md` §3.8i (mit Tabelle, wer was beigesteuert hat). **Von eidl stammen**
  `amssymb`, `caption`, `geometry`/A4 und `\pretocmd{\section}{\clearpage}` — EiPy hat sie übernommen,
  A4 hat dort 447 auf 319 Seiten und 188 auf 67 überlange Zeilen gebracht. Offen sind noch zwei
  Kleinigkeiten in die andere Richtung:
  - ~~`microtype`~~ **erledigt 2026-09-27**, zusammen mit `shorthands=off` an babel. Dabei fiel auf, dass
    der gemeinsame Block bei uns **hinter** `datetime` stand: Auf der Titelseite stand deshalb
    „Saturday 26. September, 2026“. Block nach vorn geschoben, jetzt „27. September 2026“.
  - ~~`Scale=0.872` statt `MatchLowercase`~~ **erledigt 2026-09-27.** Der Faktor ist gerechnet:
    Zeichenvorschub lmmono10 0,5250 em gegen DejaVu 0,60205 em, 0,5250/0,60205 = 0,872. Damit sind die
    Zeichenbreiten identisch, und ein Schriftwechsel ändert keinen einzigen Zeilenumbruch. Nachrechnen
    mit fontTools, wenn die Schrift wechselt.
  - ~~Option `preamble` im eigenen Template deklarieren~~ **erledigt 2026-09-27.** Markenfarbe,
    PDF-Metadaten und `\setminted` stehen jetzt in `options.preamble` in der `myst.yml`, die Option ist
    in `template.yml` deklariert (undeklarierte verwirft jtex kommentarlos). Der Template-Block ist damit
    zwischen den Büchern kopierbar.
- [x] **Emoji im PDF geprüft (2026-09-27).** EiPy hatte 58 Emoji aus `rich`/`textual`- und black-Ausgaben, für
  die keine Schrift im Image eine Glyphe hat; sie fehlten im PDF ersatzlos. Lösung dort: `ucharclasses` +
  `fonts-symbola` (Playbook §3.8b). Ob eidl betroffen ist, sagt der eigene Prüfer — `check_pdf_build.py`
  zählt fehlende Glyphen bereits mit. **Gemessen 2026-09-27: 0 fehlende Glyphen**, lokal und im CI-Image —
  dieses Buch zeigt keine Werkzeugausgaben mit Rahmenzeichen oder Emoji. Hier ist nichts zu tun; der Prüfer
  läuft mit `--max-missing-glyphs 0` weiter und meldet es, falls doch einmal eines dazukommt.
- [x] **Überlange Zeilen: 21 → 9** (2026-09-27). `\usepackage[htt]{hyphenat}` erlaubt Trennung in
  Schreibmaschinenschrift im Fließtext (`torch.backends.mps.is_available()`), dazu 3 em `emergencystretch`
  für die Zeilen, die gar keine Trennstelle haben. Gemessen: ohne beides 17/15 (überlang/zu locker),
  mit 1,5 em 14/15, mit 3 em **9/19** — eine zu lockere Zeile bleibt im Satzspiegel, eine überlange nicht.
- [x] **apt angeheftet** (2026-09-27): `ARG DEBIAN_SNAPSHOT=20260927T000000Z`, die `debian.sources` zeigen
  auf `snapshot.debian.org`, dazu `Acquire::Check-Valid-Until "false"` (ein Snapshot-Release ist
  definitionsgemäß abgelaufen; die Signaturprüfung bleibt). Damit ist der ganze Bau angeheftet — Basis-Image
  per Digest, Debian-Pakete per Zeitstempel, mystmd per Version. Gemessen: vollständiger Bau ohne Cache
  **1 min 29 s**, snapshot.debian.org war nicht der Flaschenhals. Die installierten Versionen stehen als
  Kommentar im Dockerfile; Anheben heißt: Zeitstempel setzen, Image bauen, PDF im Container prüfen, committen.

## Nach Datum

### 2026-10-15/16 (Abhängigkeits-Upgrade)

Auslöser: „Ich denke, wir können mystmd und numpy und ggf. noch mehr updaten.“ Protokoll mit
allen Messwerten: `build-log-2026-10-15.md`. Der Ertrag war nicht das Upgrade — das war
unauffällig —, sondern was beim Prüfen auffiel: eine falsche Erklärung der Seitenzahl-Abweichung
(§3.8m im Playbook), ein Abbildungslauf, der seit der Umbenennung der Jahresordner fünf
Abbildungen nie erreichte, und ein `scipy`, das das Buch benutzt und das Projekt nicht
deklarierte.

### 2026-10-02 (VL-1-Durchsicht vor der ersten Sitzung)

Auslöser: „Sieh die Folien für die erste Sitzung durch.“ Befunde und Umsetzung in
`folien-review-vl01-2026-10-02.md`; die Liste oben unter „Beamer-Folien“ fasst sie zusammen. Zwei
Befunde waren keine Folienfrage: die Umfrage-Ansage gegen das ILIAS-Fenster, und der fehlende
Validation-Split im Kapitel, auf den das Glossar schon verwies. Abends VL 2 nach derselben
Prüfliste (`folien-review-vl02-2026-10-02.md`); der Befund, der über das Deck hinausging, war die
Notation der Neuron-Abbildung (σ statt τ) aus `make_figures.py`.

### 2026-09-27, nachts (Playbook-Durchgang)

Auslöser: Durchsicht von `~/Sciebo/hhu/PLAYBOOK.md` gegen dieses Repo. Protokoll mit Messwerten:
`devnotes/build-log-2026-09-27.md`.

- [x] **Übungsblatt 0 repariert.** Sechs `::: proof` (Pandoc-Stil ohne geschweifte Klammern) waren für MyST
  **Codeblöcke**: Die Beweise standen als roher Markdown-Quelltext im Buch, in HTML wie PDF. Dazu eine
  Schachtelung gleich tiefer `:::`, die eine `##`-Überschrift („Lineare Algebra: Länge“) und eine ganze
  Definition in einen Codeblock verschluckt hat. Jetzt flach, mit deutschen Titeln („Beweis“,
  „Beweisaufgabe“) statt des Konversions-Artefakts „proof“.
- [x] **Übungsblatt 10 repariert.** Fünf Pandoc-Gitter-Tabellen, die die Konversion von 2025 nicht mitgenommen
  hat: drei standen als Fließtext-Wüste im Buch, zwei als Codeblock. Jetzt echte Markdown-Tabellen — auch die
  beiden leeren zum Ausfüllen. Nebenlehre: `a)` ist in CommonMark **kein** Listenmarker, alles vier Leerzeichen
  darunter wird ein Codeblock.
- [x] **Übungsblatt 4**: eingerückter Pseudocode-Block ohne Sprache → Fence mit Sprache `python`.
- [x] **`code_style: minted` wieder an** (am 2026-09-20 entfernt, weil der PDF-Bau brach). Die Ursache war eine
  andere als damals vermutet: drei Codeblöcke **ohne Sprache** ergeben `\begin{minted}[breaklines]{}`, woran
  minted mit „Missing Pygments output“ abbricht. Die drei sind oben repariert, seither 0 Fehler. Dafür braucht
  es im Image den `latexminted`-Helfer von Debian (nicht den aus PyPI!) mit festem Shebang — im Dockerfile
  ausführlich begründet, mit `latexminted --version` als Selbsttest beim Image-Bau.
- [x] **mystmd-Bindestrich-Fehler behoben** (Playbook §3.8g), `devnotes/patch_myst_tex.py`. mystmd escaped
  Codeblöcke als Mathematik und setzte vor jeden Bindestrich ein Leerzeichen: 49 Stellen in 18 Kapiteln, aus
  `nvidia-smi` wurde `nvidia -smi`, aus `--index-url` wurde `- -index -url`. Betrifft `verbatim` genauso wie
  `minted` — die Stelle sitzt im gemeinsamen `code`-Handler. Der PDF-Prüfer hat jetzt zwei `--expect`-Proben
  darauf.
- [x] **`build-pdf` prüft das PDF wirklich** (`devnotes/check_pdf_build.py` aus EiPy): Fehler im
  `-file-line-error`-Format, Abbruch wegen Fehlerflut, fehlende Glyphen, Seitenzahl, Stichproben aus den letzten
  Kapiteln und das MyST-Protokoll auf verschluckte Knoten. Dafür `poppler-utils` ins Image.
- [x] **Site-Template mitgeliefert** (`_site/vendor/`, 13 MB, `@myst-theme/book` 1.3.1 — dieselbe Version, die
  bisher bei jedem Build von GitHub kam, das Aussehen ändert sich also nicht). Playbook §3.4.
- [x] **CI nachgezogen** (Playbook §3.3): Basis-Image per Digest angeheftet, `.dockerignore` als Allowlist,
  `when: never` außerhalb des Default-Branch, Kurz-SHA als zweiter Tag, kaniko-Layer-Cache,
  `devnotes/patch_myst_tex.py` in `changes`, `retry` nur für Runner-Probleme. Dazu
  `devnotes/check_ci_yaml.py` (und `pyyaml` in der dev-Gruppe), weil eine kaputte `.gitlab-ci.yml` sich nicht
  selbst prüfen kann.
- [x] **`downloads:` in `myst.yml`** — das PDF war im `pages`-Job schon dabei, aber im Buch nicht verlinkt.
- [x] **`CLAUDE.md` angelegt**, mit Zeiger aufs Playbook und einem Abschnitt „Markup — die Fallen dieses Repos“,
  in dem die vier Konversions-Artefakte von oben als Regeln stehen.
- [x] **`?“` wurde im PDF zu `?¿`** (von Konrad im PDF gesehen, Seite 54: „Geht das mit neuronalen
  Netzen¿‘). Ursache: MyST schreibt das schließende deutsche Anführungszeichen als zwei Accent-graves,
  und XeLaTeX bildet daraus zusammen mit dem vorangehenden `?` die TeX-Ligatur `¿`. Neun Stellen im Buch.
  `patch_myst_tex.py` klammert die Ersetzung jetzt ein; im PDF 0 Treffer. **Geschwister gegengeprüft
  (nur gelesen, nichts geschrieben):** eipy ist sauber — 0 Treffer im lokalen wie im veröffentlichten PDF,
  die einzige `?“`-Stelle im Repo steht in `devnotes/` und damit nicht im TOC. **ds-skript hat 7 Treffer**
  im veröffentlichten PDF; das ist ein Jupyter Book, also ein anderer Weg zum selben Zeichen. Notiert im
  Playbook, hier nichts zu tun.
- [x] **76 Überschriften standen hinter ihrem eigenen Abschnitt.** `##` wird zu `\paragraph`, und das ist
  in `article` ein run-in-Titel: Folgt eine Merkbox oder ein Codeblock statt eines Absatzes, wandert der
  Titel bis zum nächsten echten Absatz. Am deutlichsten in Blatt 0, wo „Lineare Algebra: Länge“ unter dem
  Länge-Abschnitt stand. `\paragraph` und `\subparagraph` sind im Template jetzt Überschriften auf
  eigener Zeile (vier Zeilen im `\makeatletter`-Block, einzeln rückgängig zu machen). Das ändert das
  Schriftbild aller 979 Zwischenüberschriften — **wenn das nicht gefällt, ist es eine Zeile Arbeit.**
  137 statt 136 Seiten.
- [x] **Template aufgeteilt** (PLAYBOOK §3.8i): Im `template.tex` steht nur noch, was für jedes
  deutschsprachige Skript der Familie gilt; Markenfarbe, PDF-Metadaten und `\setminted` sind in
  `options.preamble` in der `myst.yml` gewandert, die Option ist in `template.yml` deklariert. Dazu
  `\setmonofont{DejaVu Sans Mono}[Scale=0.872]` statt `MatchLowercase` — der Faktor ist aus den
  Zeichenvorschüben gerechnet (lmmono10 0,5250 em zu DejaVu 0,60205 em) und passt die *Breite* an
  statt der x-Höhe. Dazu die Lesezeichen-Einstellungen von hyperref (`bookmarksnumbered`, `breaklinks`).
- [x] Gegenprobe im **echten CI-Image** (lokal mit Docker gebaut, 1,13 GB): `myst build --pdf` plus Prüfer
  laufen durch — 137 Seiten, 0 LaTeX-Fehler, 0 fehlende Glyphen.

### 2026-09-20, zweite Runde (aus der TODO-Liste selbst erledigt)

- [x] `index.md`: Hinweisbox – seit 2026-09-20 abends nur noch die Bitte um Fehlermeldungen (Konrad), kein
  Entwurfs-Disclaimer mehr.
- [x] Alle neun `<!-- TODO Abbildung -->`-Marker aufgelöst: Hugging-Face-Tasks als Tabelle (04); Denoising-AE-Bilder
  aus der Musterlösung 2025 nach `images/vl08-*.png` (14); Faltungsmatrix-Abbildung selbst erzeugt aus
  `notebooks/pallino.jpg` (`images/vl10-faltungsmatrix.png`, 20); CycleGAN, StyleGAN, Transformer Fig. 1, Hubel &
  Wiesel, GRU/LSTM als Links (22, 19, 20, 18). Der Loss-Landscape-Marker war schon beim Split von 08 weg.
- [x] Lehrbuchverweise: „Weiterlesen“-Box (Prince *UDL*, Deisenroth *MML*) am Ende von 17 Kapiteln.
- [x] Glossar zur Klausurvorbereitung (`glossar.md`, TOC-Abschnitt „Anhang“, Link in `README.md`): alle Begriffe aus
  `klausur-abdeckung.md` in ein bis drei Sätzen mit Kapitel-Link.
- [x] „Rezept: ein Anwendungskonzept schreiben“ als Abschnitt am Ende von „Anwendungsbeispiele“ (24), sechs Punkte.
- [x] Blätter 7 bis 10 geprüft: nur Blatt 9 verwies auf „die Vorlesung“, jetzt Kapitel-Link.
- [x] Interpolationsformel $Q(x)$ und $P(x)$ in „Netze von Hand“ (12) nachgerechnet: alle Stützstellen stimmen.
- [x] `notebooks/VL_10_convolutions.ipynb`: `padding=kernel_size // 2` statt `padding=1`, Kommentar korrigiert.
- [x] PDF-Export repariert: `code_style: minted` aus `myst.yml` entfernt (Listings jetzt `verbatim`); fünf
  Mehrbild-`figure`-Direktiven in Einzelfiguren aufgeteilt (06, 12, 14, 15, 23), die in LaTeX „Not in outer par
  mode“ warfen; literale Pfeile „→“ im Fließtext durch `$\to$` ersetzt (sie zwangen LaTeX in den Mathemodus);
  Überschrift „Von Bernoulli zu Multinoulli“. Ergebnis: 0 LaTeX-Fehler, 181 Seiten.

### 2026-09-20, erste Runde (Auswertung der Vorlesungsaufzeichnungen 2025/26)

- [x] 15 Aufzeichnungen transkribiert und je Sitzung `transcripts/<vl>/notiz.md` geschrieben; `transcripts/uebersicht.md`
  und `transcripts/abschlussbericht.md`. `transcripts/` ist in `.gitignore` (Standbilder), liegt nur in Sciebo.
- [x] `devnotes/diskussion-vorlesung-vs-skript.md`: neun Thesen, acht Entscheidungen von Konrad, alle umgesetzt.
- [x] `devnotes/vorschlag-grundlagen.md` (zwölf Snippets) vollständig eingebaut, inklusive Split von „Gradientenabstieg“
  in **Loss-Funktionen und Maximum Likelihood** (07) + **Gradientenabstieg** (08); Kapitel 08–26 → 09–27 umnummeriert
  (`git mv`), alle Links, `myst.yml`, `kurs-2026-27.md` und die Transkript-Notizen angepasst. Wortzahlen danach:
  alle ≤ 2000 außer „Logistische Regression“ (2528) und „Gradientenabstieg“ (2414); beide bewusst so gelassen,
  weil sie je eine ganze Sitzung tragen.
- [x] Vier Kernmomente der Vorlesung 2025 ins Skript: Ein-Sample-Beweis (03), Batch-Bild (05), VAE gegen PCA/EM (15),
  GAN-Regel „früh aufhören“ (22). Plus VAE-Loss in beide Richtungen begründet (15), Sparse-AE-Hinweis auf das
  Addieren des Strafterms (14), Softmax-Vorzeichen-Hinweis (06), CUDA/ROCm-Antworten (01), Zufalls-Absatz zu SGD (08).
- [x] Vertiefungen als aufklappbare Boxen markiert (siehe oben unter „Fachliche Durchsicht (b)“).
- [x] Externe Werkzeuge als „Ausprobieren“-Boxen mit dem, was 2025 daran gezeigt wurde: Playground (09), Loss
  Landscape Explorer (08), GAN Lab (22).
- [x] Tipps zu den Blättern aus den Kapiteln in die Blätter verschoben (Box „Hinweise“ je Blatt), ergänzt um das,
  was 2025 in der Vorlesung dazu gesagt wurde; neue Aufgaben 1/4b, 3/2b, 5/1b mit Lösungsvorschlag.
- [x] Stale VL-Nummern in der Prosa („VL 05/06“, „VL 13“, „VL 15“, „weiter unten“) durch Kapitel-Links ersetzt.
- [x] `README.md`: Satz zu den Rückverweisen auf das DS-Skript.

### 2026-09-17 bis 2026-09-19

- [x] Kursorganisation (Termine, Räume, Prüfung, VL-Tabelle) aus dem Buch in `kurs-2026-27.md` ausgelagert;
  `README.md` ist „Über dieses Skript“ (2026-09-19)
- [x] Notebooks aus dem Buch genommen, Inhalte in die Kapitel übernommen; `notebooks/README.md` erklärt den Stand
  (2026-09-18)
- [x] Kapitelsplits 20 → 26 (Perzeptron, Backprop/Autograd, Aktivierungen/Netze von Hand/Universalität,
  RNN/Transformer, neues Kapitel „Latente Räume geometrisch“) (2026-09-18)
- [x] CI: myst-build nicht mehr von manuellem build-image abhängig (2026-09-18)
- [x] MyST-Projekt aufgesetzt, 15 Kapitel als Prosafassung, Übungsblätter 00–11 per pandoc, GitLab-Remote, CI,
  Pages-Deploy, 35 Abbildungen per matplotlib, Logo/Favicon, Klausur-Abgleich (2026-09-17)
- [x] PDF-Export getestet: 182 Seiten, Mathe und Abbildungen ok (2026-09-17)
- [x] `hidefromsolutions` wird in keinem Blatt verwendet; `latent-classifier.ipynb` in slides/ und exercises/ identisch
  (2026-09-17)
