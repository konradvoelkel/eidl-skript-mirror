# TODO eidl-skript

Stand: 2026-09-20 (spät abends). Erledigtes steht unten unter „Erledigt“, nach Datum. Punkte mit **[Entscheidung]**
brauchen eine Antwort von Konrad; ein Vorschlag steht jeweils dabei. Überblick über alle Dateien in `devnotes/`:
`devnotes/README.md`.

Aktueller Stand des Skripts: 27 Kapitel (01–27) plus Glossar. HTML-Build ohne Warnungen
(`uv run --only-group dev myst build --html`), PDF-Export ohne LaTeX-Fehler, 135 Seiten A4
(`uv run --only-group dev myst build --pdf` → `exports/eidl-skript.pdf`, gitignored; in der CI als `build-pdf`).

## Inhalt (Skript)

- [ ] **Fachliche Durchsicht** der Prosafassung. Zwei Sorten von Stellen:
  - *(a) Stoff, der in der Vorlesung 2026/27 vorkommen soll* (steht im Plan in `kurs-2026-27.md` oder wird in der
    Klausur gefragt): Hyperebenen-Geometrie und Abstand (02), Ein-Sample-Argument für die Perzeptronregel (03),
    Batch-Bild für Tensoren (05), Numerik-Box zu `exp`/`log` (06), Maximum Likelihood → BCE und Gradient $p - y$
    (07/08), Summe über Pfade und numerische Probe (08), Feature-Skalierung (08), Erwartungswert-Absatz zu SGD (08),
    Playground-Box (09), VAE-Fragenbox (15), GAN-Lab-Box mit Regel „früh aufhören“ (22), CBOW-Formel (16),
    Ausgabegrößen-Formel und Shape-Beispiel (20), Minimax-Formel (22), Reparametrisierung (15), $T^2$-Faktor (25),
    Antwortbox zu GPU/SIMD, PyTorch, CUDA/ROCm (01), Rezept Anwendungskonzept (24), Glossar (`glossar.md`).
  - *(b) Vertiefungen*, als aufklappbare Box „Vertiefung: …“ markiert und nicht Vorlesungsstoff:
    Konvergenzsatz (03), Cauchy-Schwarz (08), Spur-Trick (09), Message-Passing-Formel (17), Wasserstein-Dualität (22),
    FGSM (27). Nur auf Korrektheit prüfen, nicht auf Didaktik.
  - Konkrete Prüfaufträge: Encoder mit oder ohne Sigmoid in „Autoencoder“ (14) entscheiden (Skript: ohne, mit
    Hinweis „man kann auch“; Vorlesung 2025: mit – der Verweis auf 2025 steht seit 2026-09-21 nicht mehr im Text); die neuen Lösungsvorschläge zu Blatt 1 Aufgabe 4b, Blatt 3 Aufgabe 2b und Blatt 5
    Aufgabe 1b gegenrechnen; die „Weiterlesen“-Boxen (17 Kapitel) auf passende UDL/MML-Kapitelnummern prüfen.
- [ ] **Abbildungen**, verbleibende Wünsche (alle `<!-- TODO Abbildung -->`-Marker sind seit 2026-09-20 aufgelöst,
  entweder durch eigene Bilder, Bilder aus den Musterlösungen 2025 oder Links): Hubel & Wiesel und GRU/LSTM sind
  nur verlinkt (Wikipedia, CC-BY-SA); wer sie einbetten will, lädt die Dateien nach `images/` und ergänzt den
  Lizenzhinweis in der Bildunterschrift.
- [ ] „Rezept Anwendungskonzept“ (24) ist geschrieben; die 2025 angekündigte Klausurfrage „wie trainiert man das
  Netz für das Empfehlungssystem“ ist dort noch nicht als ausformulierte Aufgabe, nur als Absatz im Beispiel.
- [ ] Zeitreihen / Aktienkurs-Beispiel (2025 gewünscht, nicht geliefert): bewusst zurückgestellt, sprengt den Rahmen.
  `notebooks/ASML.csv` liegt bereit, falls „RNNs“ (18) später ein Beispiel bekommen soll.
- [x] Termine, Räume und Verteilung geklärt am 2026-09-24 (Quelle LSF 278733): Vorlesung Mi 12:30–14:00 in
  HS 5E (25.21), 14.10.2026–03.02.2027; Übung Do 10:30–12:00 in 25.22.U1.52, ab der ersten Woche. Material und
  Abgaben über **ILIAS** (Kurs 2165367); Fragen laufen über den Rocket.Chat-Kanal `#eidl-2026` (angelegt
  2026-09-25, Einladungslink ohne Ablauf), inhaltlich wie organisatorisch – kein Forum.
- [x] **Übungsleitung 2026/27: Konrad selbst** (2026-09-24). Elisa Kleinfeld steht in LSF als „begleitend“,
  korrigiert aber nur die Übungsblätter und hält die Übungsgruppe nicht. Die ILIAS-Kursseite nennt – wie
  2025/26 – niemanden namentlich.

## Vorlesungsplan (`kurs-2026-27.md`)

- [x] VL-Tabelle am 2026-09-20 aus dem *Ist* der Aufzeichnungen 2025 neu gebaut (Entscheidung Konrad): jede Woche
  nur, was 2025 in 90 Minuten geschafft wurde; VL 1 ohne Perzeptron, VL 5 = Loss + Gradientenabstieg, VL 6 nur
  Backpropagation, Transformer komplett in VL 10, „Optimierer“ (26) und „Adversarial Attacks“ (27) als Reserve.
- [ ] **[Entscheidung]** Die Reserve-Kapitel 26/27 ganz aus dem Plan nehmen oder als 16. Termin (Fragestunde vor
  der Klausur) einplanen? *Vorschlag:* 15 Termine wie 2025, Reserve nur, wenn eine Woche ausfällt.

## Übungsblätter

- [ ] **[Entscheidung] Punkte und Bestehensgrenzen** der Blätter 1, 3, 5 nach den neuen Aufgaben 4b, 2b, 1b
  anpassen (*Vorschlag:* je +1 Punkt, Bestehensgrenze bleibt „die Hälfte“).
- [x] **Abgabetermine 2026/27 bestätigt (Konrad, 2026-09-24)** und in ILIAS eingetragen: Blatt 0 ohne Abgabe;
  1: 21.10., 2: 28.10., 3: 04.11., 4: 11.11., 5: 18.11., 6: 25.11., 7: 02.12., 8: 09.12., 9: 16.12.2026,
  10: 13.01., 11: 20.01.2027, Probeklausur als Take-Home mit Abgabe 27.01.2027 — jeweils Mittwoch 12:00.
- [ ] Die Zeile „N Punkte, Abgabe bis …“ je Blatt wieder eintragen (ist seit 2026-09-20 draußen); die Termine
  stehen jetzt fest, die Punkte hängen an der Entscheidung oben. Die Notiz „Übungsaufgaben von 2025, werden ggf.
  noch angepasst …“ bleibt, bis das Blatt wirklich angepasst ist.
- [ ] **[Entscheidung vertagt]** Blatt 6 (Iris-Autoencoder) wird nach dem neuen Wochenplan eine Woche *vor* der
  Autoencoder-Vorlesung ausgegeben (AE ist jetzt VL 8 statt VL 7, CNNs VL 11, LLMs VL 12). Optionen: Blätter 6/7
  in der Ausgabe tauschen, Blatt 6 anpassen, oder so lassen (Skript-Kapitel steht online). Bei der
  Blatt-Überarbeitung ansehen; in ILIAS ist vorerst die unveränderte Reihenfolge eingetragen.
- [ ] Blatt 12 = Take-Home-Probeklausur anlegen (Grundlage: `../eidl-25/exam/`, Probeklausur 2025).
- [ ] Lösungen: bisher nur die in den Blättern eingebetteten Dropdowns. Notebook-/Skript-Lösungen liegen in
  `~/Sciebo/hhu/eidl-25/exercises/blattNN-solution/`. *Vorschlag:* nicht ins Skript (öffentlich!), sondern eigenes
  privates Repo/Ordner.
- [x] **[Entscheidung 2026-09-20]** Englische Fassungen (`sheetNN.tex`) fallen weg, solange die Vorlesung deutsch
  ist.

## Klausur

- [x] Termine aus LSF (2026-09-24): **Erstklausur Do 11.02.2027**, LSF-Fenster 8:30–11:30, Hörsäle 5F (25.21)
  und 2D (22.01); **Zweitklausur Mo 15.03.2027**, Fenster 8:30–11:30, Hörsaal 5D (25.21). Geschrieben wird
  jeweils 9:00–10:30 (90 Minuten, Entscheidung Konrad 2026-09-24); so steht es auf der ILIAS-Seite.
- [ ] `exam2026-eidl-exam-1/2.tex` (englische Entwürfe vom 20.01.2026 in `../eidl-25/exam/`) – Status klären:
  Vorlagen für 2026/27?
- Keine weiteren Klausuransagen aus den Aufzeichnungen übernehmen (Entscheidung Konrad 2026-09-20).

## Notebooks

- [ ] `latent-classifier.ipynb` ist das einzige verbleibende Notebook mit Funktion (Download auf der Blatt-11-Seite).
  Vor Semesterstart mit aktuellem torch/transformers durchlaufen lassen (bert-medium-Download, `ipywidgets` für die
  Saliency-Zelle) und Outputs neu einchecken.
- [x] **Alle 24 Python-Blöcke am 2026-09-24 ausgeführt** (Venv auf `/media/konrad/xtraspace/eidl-venv`, CPU).
  Ergebnis und Korrekturen: `codecheck-2026-09-24.md`. Kurz: `import torch` in „Autograd“ (10) ergänzt,
  Beispieldaten in „Logistische Regression“ (06), Imports + `IMAGESIZE` in „Autoencoder“ (14), `data` aus
  `ASML.csv` in „Faltung und CNNs“ (20), gemessene Wahrscheinlichkeiten in „LLMs benutzen“ (21);
  `ollama`, `pydantic`, `sacremoses` in `pyproject.toml` nachgetragen.
- [x] **[Entscheidung 2026-09-25] Autoencoder-Training (14) bleibt wie es ist.** Mit SGD `lr=1e-2` und
  15 Epochen sinkt der MSE nur von 0.231 auf 0.228, die Rekonstruktion bleibt Matsch – und genau das soll man
  einmal gesehen haben, bevor die Tricks-Liste (mehr Epochen, Lernrate, Adam) danach aufräumt. Gemessene
  Vergleichswerte für den Hörsaal: SGD `lr=1e-1` → 0.072, Adam `lr=1e-3` → 0.019.
- [ ] Torch aus `uv sync` ist der cu130-Build, der NVIDIA-Treiber hier ist 12.9 → `torch.cuda.is_available()`
  ist False, alles läuft auf der CPU. Vor Demos im Hörsaal entweder Treiber aktualisieren oder einen
  passenden Torch-Build pinnen.

## Beamer-Folien (Schritt 4 des Migrationsplans)

- [x] **[Entscheidung 2026-09-20]** Die Folien 2026/27 werden **aus dem Skript heraus neu erzeugt**, nicht aus den
  Google-Slides 2025. Grund: Von neun Unstimmigkeiten, die 2025 im Hörsaal auffielen, waren fünf Folienfehler, die
  das Skript schon richtig hat (Softmax-Minus, BLEU-Mittel, Wasserstein-Wertebereich, Top-k-Vergleichszeichen,
  Softmax-Abstand in „Latente Räume“).
- [x] **Alle 15 Decks stehen** (2026-09-25, `slides/`): ein Deck pro Vorlesungswoche, gebaut aus den Kapiteln
  laut `kurs-2026-27.md`, gemeinsamer Header, Bilder per `\graphicspath` direkt aus `images/`. Alle bauen mit
  `latexmk -lualatex` ohne zu volle Rahmen (14–23 Folien je Deck). Textarm gehalten: die Folie ist der
  Gesprächsanlass, die Ausführung steht in `\note{}`.
- [ ] Decks inhaltlich gegenlesen und im Hörsaal erproben; Folien-PDFs in ILIAS hochladen (die kopierten
  Dateien dort sind noch die von 2025/26).
- [x] Dozentennotizen sind in den Decks (2026-09-25): je Folie ein `\note{}` mit den Dialogmustern aus
  `transcripts/*/notiz.md`, dazu auf jeder Titelfolie ein Minuten-Ablaufplan aus der jeweiligen Aufzeichnung.
  Drin sind u.a. der Type-Check (VL 2), die offen gehaltene Zufalls-Frage (VL 5), „Quizfrage nicht auflösen“
  (VL 1), „beim GAN Lab früh aufhören“ (VL 13) und die Vibecoding-Vorbereitung (VL 15).
- [x] Externe Werkzeuge am 2026-09-24 geprüft: TensorFlow Playground (09), Loss Landscape Explorer (08),
  GAN Lab (22), Ollama (21) antworten alle mit 200. Ebenso alle 67 externen Links im Skript – bis auf einen
  toten (`muhark.github.io`, word2vec from scratch), jetzt ersetzt durch das offizielle PyTorch-Tutorial
  „Word Embeddings: Encoding Lexical Semantics“. Der HPCwire-Artikel (01) blockt `curl` mit 403, im Browser
  ist er da. Vor jedem Semester wiederholen.

## ILIAS (Kurs 2026/27, ref_id 2165367)

Textfassung von Seite und Objektbaum: `../ilias/` (analog zu `ds2-26/ilias/`), Workflow in
`../ilias/README.md`, aktueller Durchlauf in `../ilias/runs/ws2026-27.yaml`.

- [x] Am 2026-09-24 aufgesetzt: Objekte und Seitengestaltung aus dem Kurs 2025/26 (1948423) übernommen
  (Lösungshinweise-Dateien dabei ausgelassen), Kursseite auf 2026/27 umgeschrieben (Ankündigung, Raum und Zeit,
  Themenliste, Material mit Skript-Link, Externe Resourcen inkl. UDL/MML, 19-zeilige Wochentabelle),
  Übungstermine für alle 12 Übungseinheiten gesetzt, Umfragefenster gesetzt,
  Kalender und Neuigkeiten deaktiviert. Der Kurs ist noch **offline**.
- [x] Am 2026-09-25 umgestellt: Absatz „Raum und Zeit“ verlinkt den Rocket.Chat-Kanal `#eidl-2026`
  samt Einladungslink, das Forum-Objekt ist gelöscht (der Block „Foren“ verschwand mit ihm).
- [ ] Vorlesungsfolien 2026/27 als neue Versionen der kopierten Dateien hochladen (aktuell liegen dort die
  Folien von 2025/26) – hängt an den Beamer-Decks.
- [ ] Zusatzmaterial aktualisieren: „EiDL-Klausur-2024“ durch die Erstklausur 2025/26 ersetzen, Probeklausur
  und Blatt 0 / Sheet 0 prüfen.
- [ ] Kurs online schalten, wenn die Blätter und die erste Foliensitzung stehen.

## Infrastruktur

- [x] GitLab Pages auf „Everyone“ (Konrad, 2026-09-20); aktiv seit dem nächsten Pages-Deploy, geprüft 2026-09-21
  (`curl` → 200, PDF unter `/eidl-skript.pdf` erreichbar).
- [x] PDF-Export in der CI wie bei DS-/EiPy-Skript (2026-09-20): Job `build-pdf` mit `allow_failure`, PDF landet
  unter `public/eidl-skript.pdf` und ist auf `index.md` verlinkt. Dafür TeX Live ins CI-Image und ein eigenes
  Template `templates/tex/eidl-skript/` (plain_latex + amssymb, caption, babel ngerman, A4, HHU-Linkfarbe,
  DejaVu Sans Mono, Kapitel auf neuer Seite). Grund: `plain_latex` ignoriert die `preamble`-Option in `myst.yml`
  stillschweigend, deshalb waren `\mathbb` & Co. bisher undefiniert (248 LaTeX-Fehler, die latexmk durchwinkte).
  Jetzt 0 Fehler, 135 Seiten (A4). Ohne Docker lokal weiterhin `uv run --only-group dev myst build --pdf`.
- `_site/sidebar_footer.md` leer, `navbar_end.md` nur „Inhaltsverzeichnis“ – wie bei EiPy; lassen.
- Logo: `logo/` enthält SVGs und Exporte; für Rocket.Chat `logo/eidl-logo-512.png`.

## Erledigt

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
