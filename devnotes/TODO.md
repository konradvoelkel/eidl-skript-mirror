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
    Hinweis; Vorlesung 2025: mit); die neuen Lösungsvorschläge zu Blatt 1 Aufgabe 4b, Blatt 3 Aufgabe 2b und Blatt 5
    Aufgabe 1b gegenrechnen; die „Weiterlesen“-Boxen (17 Kapitel) auf passende UDL/MML-Kapitelnummern prüfen.
- [ ] **Abbildungen**, verbleibende Wünsche (alle `<!-- TODO Abbildung -->`-Marker sind seit 2026-09-20 aufgelöst,
  entweder durch eigene Bilder, Bilder aus den Musterlösungen 2025 oder Links): Hubel & Wiesel und GRU/LSTM sind
  nur verlinkt (Wikipedia, CC-BY-SA); wer sie einbetten will, lädt die Dateien nach `images/` und ergänzt den
  Lizenzhinweis in der Bildunterschrift.
- [ ] „Rezept Anwendungskonzept“ (24) ist geschrieben; die 2025 angekündigte Klausurfrage „wie trainiert man das
  Netz für das Empfehlungssystem“ ist dort noch nicht als ausformulierte Aufgabe, nur als Absatz im Beispiel.
- [ ] Zeitreihen / Aktienkurs-Beispiel (2025 gewünscht, nicht geliefert): bewusst zurückgestellt, sprengt den Rahmen.
  `notebooks/ASML.csv` liegt bereit, falls „RNNs“ (18) später ein Beispiel bekommen soll.
- [ ] Formalia (`kurs-2026-27.md`, bewusst nicht im Buch): Übungsleitung 2026/27, Räume/Zeiten bestätigen;
  Verteilung an die Studierenden klären (ILIAS/Rocket.Chat?).

## Vorlesungsplan (`kurs-2026-27.md`)

- [x] VL-Tabelle am 2026-09-20 aus dem *Ist* der Aufzeichnungen 2025 neu gebaut (Entscheidung Konrad): jede Woche
  nur, was 2025 in 90 Minuten geschafft wurde; VL 1 ohne Perzeptron, VL 5 = Loss + Gradientenabstieg, VL 6 nur
  Backpropagation, Transformer komplett in VL 10, „Optimierer“ (26) und „Adversarial Attacks“ (27) als Reserve.
- [ ] **[Entscheidung]** Die Reserve-Kapitel 26/27 ganz aus dem Plan nehmen oder als 16. Termin (Fragestunde vor
  der Klausur) einplanen? *Vorschlag:* 15 Termine wie 2025, Reserve nur, wenn eine Woche ausfällt.

## Übungsblätter

- [ ] **[Entscheidung] Punkte und Bestehensgrenzen** der Blätter 1, 3, 5 nach den neuen Aufgaben 4b, 2b, 1b
  anpassen (*Vorschlag:* je +1 Punkt, Bestehensgrenze bleibt „die Hälfte“).
- [ ] **[Entscheidung] Abgabetermine 2026/27.** 2025 waren es Mittwoche 12:00, wöchentlich ab 22.10.2025,
  Weihnachtspause 17.12.→14.01. *Vorschlag* (eine Woche später als 2025, unter der Annahme Vorlesungsbeginn Mi
  14.10.2026): Blatt 0 ohne Abgabe; 1: 21.10., 2: 28.10., 3: 04.11., 4: 11.11., 5: 18.11., 6: 25.11., 7: 02.12.,
  8: 09.12., 9: 16.12.2026, 10: 13.01., 11: 20.01.2027, 12 (Take-Home-Probeklausur): 27.01.2027. Die Zeile
  „N Punkte, Abgabe bis …“ ist seit 2026-09-20 aus allen Blättern raus (Konrad); nach Bestätigung je Blatt neu
  eintragen. Die Notiz je Blatt lautet jetzt „Übungsaufgaben von 2025, werden ggf. noch angepasst …“ und bleibt,
  bis das Blatt wirklich angepasst ist.
- [ ] Blatt 12 = Take-Home-Probeklausur anlegen (Grundlage: `../eidl-25/exam/`, Probeklausur 2025).
- [ ] Lösungen: bisher nur die in den Blättern eingebetteten Dropdowns. Notebook-/Skript-Lösungen liegen in
  `~/Sciebo/hhu/eidl-25/exercises/blattNN-solution/`. *Vorschlag:* nicht ins Skript (öffentlich!), sondern eigenes
  privates Repo/Ordner.
- [x] **[Entscheidung 2026-09-20]** Englische Fassungen (`sheetNN.tex`) fallen weg, solange die Vorlesung deutsch
  ist.

## Klausur

- [ ] `exam2026-eidl-exam-1/2.tex` (englische Entwürfe vom 20.01.2026 in `../eidl-25/exam/`) – Status klären:
  Vorlagen für 2026/27?
- Keine weiteren Klausuransagen aus den Aufzeichnungen übernehmen (Entscheidung Konrad 2026-09-20).

## Notebooks

- [ ] `latent-classifier.ipynb` ist das einzige verbleibende Notebook mit Funktion (Download auf der Blatt-11-Seite).
  Vor Semesterstart mit aktuellem torch/transformers durchlaufen lassen (bert-medium-Download, `ipywidgets` für die
  Saliency-Zelle) und Outputs neu einchecken.
- [ ] Code-Beispiele in den Kapiteln (CNN, LLMs, Autograd, Autoencoder) sind aus den Notebooks übernommen, aber nicht
  erneut ausgeführt – bei der fachlichen Durchsicht einmal laufen lassen (`uv sync` installiert torch, groß).

## Beamer-Folien (Schritt 4 des Migrationsplans)

- [x] **[Entscheidung 2026-09-20]** Die Folien 2026/27 werden **aus dem Skript heraus neu erzeugt**, nicht aus den
  Google-Slides 2025. Grund: Von neun Unstimmigkeiten, die 2025 im Hörsaal auffielen, waren fünf Folienfehler, die
  das Skript schon richtig hat (Softmax-Minus, BLEU-Mittel, Wasserstein-Wertebereich, Top-k-Vergleichszeichen,
  Softmax-Abstand in „Latente Räume“).
- [ ] Pro Vorlesungswoche ein Beamer-Deck im Stil von `../slides/Einführung in Deep Learning 2026 header.tex`
  (hhubeamer), Zuordnung laut Tabelle in `kurs-2026-27.md`. Formeln und `images/` sind 1:1 übernehmbar.
- [ ] Dozentennotizen je Deck: die Dialogmuster, die 2025 getragen haben und bewusst *nicht* im Skript stehen
  (Type-Check-Argument, Gegenbeispiel „Eingabe 100“ bei Netzen von Hand, die 20 Minuten offen gehaltene Frage „wo
  steckt Zufall“, das Anwendungsbeispiel als Spiel). Quelle: `transcripts/*/notiz.md`, Abschnitt „Beobachtungen“.
- [ ] Externe Werkzeuge sind im Skript verlinkt und werden in der Vorlesung benutzt, solange sie existieren:
  TensorFlow Playground (09), Loss Landscape Explorer (08), GAN Lab (22), Ollama/llama.cpp (21). Vor jedem Semester
  einmal anklicken.

## Infrastruktur

- [ ] GitLab Pages auf „Everyone“ gestellt (Konrad, 2026-09-20), aber https://eidl-skript-131e30.pages.cs.uni-duesseldorf.de/
  leitete direkt danach noch auf die GitLab-Anmeldung um. Nach dem nächsten Pipeline-Lauf prüfen (`curl -sI` muss
  200 statt 302 auf `…/auth` liefern); sonst Settings → General → Visibility → „Pages: Everyone“ nochmal
  kontrollieren.
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
