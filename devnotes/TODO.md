# TODO eidl-skript

Stand: 2026-09-17 (abends). Erledigtes nach unten in „Erledigt“ verschieben.
Punkte mit **[Entscheidung]** brauchen eine Antwort von Konrad; ein Vorschlag steht jeweils dabei.

## Inhalt (Skript)

- [ ] **Fachliche Durchsicht** der Prosafassung, insbesondere der Stellen, die über die Folien 2025 hinausgehen
  (Liste pro Kapitel, Kapitelnamen neu):
  - Perzeptron: Definition vorgezogen, Hyperebenen-Geometrie, XOR über OR/NAND/AND, Perzeptron-Konvergenzsatz (Novikoff), Tabelle verallg. Perzeptron, „ohne Bias nur durch den Ursprung“
  - Was ist DL: Accuracy/Precision/Recall-Absatz (neu, wegen Klausur A2)
  - Tensoren: Rang-0/1/2-Tensoren, `reshape`-Antwort
  - Logistische Regression: $H'(p) = -\operatorname{logit}(p)$, $\tanh(x) = 2\sigma(2x)-1$, Softmax = $\sigma$(Differenz)
  - Gradientenabstieg: Cauchy-Schwarz-Argument, Hinge vs. Perceptron Loss
  - Backpropagation: $\delta_k$-Notation, Faltungs-Backprop-Beispiel (aus Klausur-Set A, neu), Konvolutions-Gradientensumme
  - Aktivierungsfunktionen/Universalität: ELU/Leaky/Swish/GELU-Formeln, explizite $Q(x)$ für $x^2$ (Probe gerechnet), Weierstraß-Bemerkung
  - Autoencoder: KL-Term des Sparse AE, Early Stopping / Data Augmentation (neu)
  - VAE: geschlossene Gauß-KL, `logvar` (neu)
  - word2vec: CBOW-Formel, top-p
  - RepL/Graphen: Message-Passing-Formel
  - Sequenzen: RNN-Rekursion, Attention-Formel, BLEU als geometrisches Mittel
  - CNN: 2D-Faltungsformel, Kanäle, 1×1, Korrelation vs. Faltung, Ausgabegrößen-Formel + Shape-Beispiel (neu)
  - LLMs: LoRA-Parameterzahl, RAG-Skizze
  - GANs: Minimax-Formel, DCGAN, Diffusions-Ablösung
  - Anwendungen: two-tower-Modell
  - Destillation: $T^2$-Faktor
  - Optimierer: Momentum/Adam-Gleichungen; Adversarial: FGSM-Formel, Polysemie-Absatz (aus Ruppik-Folien rekonstruiert)
- [ ] **[Entscheidung] Kapitelschnitt prüfen.** Stand: 26 Kapitel (nach den Splits unten), VL-Nummern nur noch in der Tabelle in `README.md`.
  Bewusst getroffene Schnitte, die man anders setzen könnte (Nummern = alte Zählung vor den Splits):
  - „Vortrainierte Modelle“ (Kap. 3) steht *vor* „Tensoren“ und „Logistische Regression“ – wie 2025. Das Vorstellungsdeck 2026 sieht PyTorch erst nach LogReg/SGD vor. *Vorschlag:* Reihenfolge lassen (die HF-Tour motiviert, warum man das alles lernt), aber im Vortrag Kap. 3 auf eine halbe Sitzung kürzen.
  - „Aktivierungsfunktionen und Universalität“ (Kap. 8) bündelt ReLU & Co., Netze von Hand und die Approximationssätze. *Erledigt durch Split 2* (drei Kapitel).
  - „Backpropagation“ (Kap. 7) enthält jetzt drei Zugänge (Beispielrechnung, Induktion, Berechnungsgraph in PyTorch). *Erledigt durch Split 1* (eigenes Kapitel „Autograd und Berechnungsgraph“).
  - „VAE und latente Räume“ (Kap. 10) referenziert GANs, die erst in Kap. 16 kommen. *Erledigt durch Split 5*: Abschnitt „Latente Räume für Bilder“ ist jetzt Teil von „Latente Räume geometrisch“ nach den GANs.
- [x] **Kapitelsplits** (Entscheidung Konrad 2026-09-18, umgesetzt am selben Tag: Kapitel mit zwei bis drei Themen aufteilen; 20 → 26 Kapitel, Nummern in Dateinamen durchgehend neu):
  - [x] Split 1: „Backpropagation“ → **Backpropagation** (Ziel, Motivation, konkret, Induktion) + **Autograd und Berechnungsgraph** (PyTorch-Teil)
  - [x] Split 2: „Aktivierungsfunktionen und Universalität“ → **Aktivierungsfunktionen** + **Netze von Hand bauen** („Geheimnis lüften“, „Parameter von Hand wählen“) + **Universelle Approximation**
  - [x] Split 3: „Das Perzeptron“ → **Neuron und Perzeptron** (Neuron, Perzeptron, MLP-Definition, Tipps Blatt 1) + **Das Perzeptron trainieren** (Perzeptronregel, verallg. Perzeptron, mehrere Schichten, Tipps Blatt 2)
  - [x] Split 4: „Sequenzen: RNNs und Transformer“ → **RNNs** + **Transformer**
  - [x] Split 5: neues Kapitel **Latente Räume geometrisch** (nach GANs) aus „VAE“ § „Latente Räume für Bilder“ + „word2vec“ § „Wortvektoren geometrisch verstehen“; VAE-Kapitel heißt dann nur noch „Variational Autoencoder“ (Vorwärtsverweis auf GANs entfällt)
  - [x] Alle Dateien neu nummerieren (01–26), `myst.yml`-TOC, VL-Tabelle in `README.md`, Querverweise (`.md`-Links) und Binnenverweise („übernächster Abschnitt“, „siehe oben“, „aus Kapitel 6“ = alte VL-Nummern!) anpassen
  - [x] Build prüfen (keine fehlenden Dateien/Bilder), Wortzahlen je Kapitel danach: alle ≤ ~1 750 außer Logistische Regression (2 263) und Gradientenabstieg (2 061), bewusst nicht gesplittet
- [ ] **Abbildungen**: 35 eingebettet (erzeugt von `make_figures.py`; Bilddateien in `images/`). Noch offen (9 Marker im Text):
  - Hubel & Wiesel (Wikipedia Mads00, CC-BY-SA) – Download + Lizenzhinweis
  - GIMP-Faltungsmatrix – Screenshot selbst machen
  - CycleGAN / StyleGAN-Beispiele – Paper-Figuren; *Vorschlag:* verlinken statt einbetten (Lizenz)
  - HuggingFace-Tasks-Screenshot – *Vorschlag:* durch die Aufzählung im Text ersetzen und Marker löschen
  - Loss Landscape (Li et al.), Amini et al. – *Vorschlag:* verlinken
  - Denoising-AE-Ergebnisbilder MNIST/USPS/Fashion – braucht trainiertes Modell; `blatt08-solution/` hat `denoising-example.png`, `dlae-latent-space.png`, `dlae-loss-curve.png` → übernehmen?
  - GRU/LSTM-Diagramme (Wikipedia, CC-BY-SA) – Download + Lizenzhinweis, oder eigene Zeichnung
  - Transformer Fig. 1 – *Vorschlag:* verlinken
- [ ] Lehrbuchverweise ergänzen (Prince *UDL*: Kap. 3 shallow nets ↔ Universalität, Kap. 4 deep nets, Kap. 6 fitting/SGD, Kap. 7 gradients/backprop, Kap. 10 CNNs, Kap. 12 Transformer, Kap. 15 GANs, Kap. 17 VAE; Deisenroth et al. für Lin. Algebra/Analysis).
- [ ] „Stand“-Hinweisboxen wurden beim Umbau entfernt; ggf. eine allgemeine Box in `index.md` („Entwurf, Stand …“).
- [ ] Formalia (`README.md`): Übungsleitung 2026/27, Räume/Zeiten bestätigen.
- [ ] Glossar für die Klausurvorbereitung (Vorschlag aus `klausur-abdeckung.md`).
- [ ] „Rezept Anwendungskonzept“ in Kap. 17 (Vorschlag aus `klausur-abdeckung.md`).

## Übungsblätter

- [ ] **[Entscheidung] Abgabetermine 2026/27.** 2025 waren es Mittwoche 12:00, wöchentlich ab 22.10.2025, Weihnachtspause 17.12.→14.01.
  *Vorschlag* (eine Woche später als 2025, unter der Annahme Vorlesungsbeginn Mi 14.10.2026): Blatt 0 ohne Abgabe;
  1: 21.10., 2: 28.10., 3: 04.11., 4: 11.11., 5: 18.11., 6: 25.11., 7: 02.12., 8: 09.12., 9: 16.12.2026,
  10: 13.01., 11: 20.01.2027, 12 (Take-Home-Probeklausur): 27.01.2027. Nach Bestätigung per `sed` in `part-exercises/` eintragen.
- [ ] Blatt 12 = Take-Home-Probeklausur anlegen (Grundlage: `../from_2025/exam/exam2025-eidl-probeklausur.tex`).
- [ ] Lösungen: bisher nur die in den `.tex` eingebetteten. Notebook-/Skript-Lösungen liegen in `../from_2025/exercises/blattNN-solution/`.
  *Vorschlag:* nicht ins Skript (öffentlich!), sondern eigenes privates Repo/Ordner; im Skript nur die kurzen Lösungsvorschläge als Dropdown wie jetzt.
- [ ] **[Entscheidung] Englische Fassungen** (`sheetNN.tex`): 2025 gab es alle Blätter zweisprachig. *Vorschlag:* fallen lassen, solange die Vorlesung deutsch ist; sonst gleicher pandoc-Weg (`build_skript_from_2025.py` erweitern).
- [ ] Blätter an neue Kapitelnamen anpassen (Verweise wie „Folien zu Vorlesung 4“ → Kapitelname).

## Klausur

- [x] Aufgabenschatz gegen die Kapitel abgeglichen → `klausur-abdeckung.md` (62/66 Begriffe, 4 fehlende ergänzt).
- [ ] `exam2026-eidl-exam-1/2.tex` (englische Entwürfe vom 20.01.2026) – Status klären: Sind das die Vorlagen für 2026/27?

## Notebooks

- [ ] Notebooks laufen nicht im Build (bewusst; `notebooks/README.md` erklärt das). `ASML.csv` und `pallino.jpg` liegen jetzt im Ordner, `*.gguf` ist per `.gitignore` ausgeschlossen.
- [ ] **[Entscheidung]** Outputs eingecheckt lassen (Stand 2025) oder Notebooks einmal neu ausführen? *Vorschlag:* vor Semesterstart einmal mit aktuellem torch/transformers durchlaufen lassen, dann einchecken.

## Infrastruktur

- [ ] GitLab Pages auf „Everyone“ stellen – **zum Semesterstart, bewusst noch nicht** (https://eidl-skript-131e30.pages.cs.uni-duesseldorf.de/).
- [x] PDF-Export getestet: `uv run --only-group dev myst build --pdf` → `exports/eidl-skript.pdf`, 182 Seiten, Mathe und Abbildungen ok.
- [ ] PDF: Code-Listings ohne Syntax-Highlighting, weil `minted`/`latexminted` auf diesem Rechner einen `ArgParser`-Fehler wirft (Versionskonflikt mit pygments 2.18). *Vorschlag:* `code_style: minted` in `myst.yml` entfernen (dann `verbatim`) oder `pip install --upgrade latexminted`.
- [ ] PDF-Export in die CI aufnehmen und als Download verlinken? (Image bräuchte dann TeX Live – groß.) *Vorschlag:* PDF lokal bauen und bei Bedarf manuell hochladen.
- [ ] `_site/sidebar_footer.md` ist leer, `navbar_end.md` nur „Inhaltsverzeichnis“ – wie bei EiPy (dort auch leer); lassen.
- [ ] Logo: `logo/` enthält die SVGs und Exporte; `site_logo.png` (180 px) und `favicon.ico` (16/32/48) sind daraus erzeugt, `logo_text` in `myst.yml` gesetzt. Für Rocket.Chat `logo/eidl-logo-512.png` verwenden.

## Beamer-Folien (Schritt 4 des Migrationsplans)

- [ ] Erst nach Durchsicht des Skripts: pro Vorlesungswoche ein Beamer-Deck im Stil von `../slides/Einführung in Deep Learning 2026 header.tex` (hhubeamer). Die Tabelle in `README.md` sagt, welche Kapitel(teile) in welche Woche gehören.
- [ ] **[Entscheidung]** Folien aus dem MyST-Quelltext generieren oder von Hand? *Vorschlag:* von Hand in LaTeX, aber Formeln und Abbildungen aus dem Skript übernehmen (`images/` ist direkt `\includegraphics`-tauglich; Formeln 1:1 kopierbar).

## Erledigt

- [x] MyST-Projekt aufgesetzt, Struktur wie EiPy (2026-09-17)
- [x] 15 Kapitel als Prosafassung mit LaTeX-Formeln (2026-09-17)
- [x] Übungsblätter 00–11 per pandoc konvertiert (2026-09-17)
- [x] GitLab-Remote, CI mit kaniko-Image-Build, Pages-Deploy (2026-09-17)
- [x] Abbildungen per matplotlib erzeugt, 35 eingebettet (2026-09-17)
- [x] Kapitel inhaltlich neu geschnitten: 20 Kapitel ohne VL-Nummern, Querverweise angepasst (2026-09-17)
- [x] Logo/Favicon eingebunden (2026-09-17)
- [x] Klausur-Abgleich, fehlende Begriffe ergänzt (2026-09-17)
- [x] `hidefromsolutions` wird in keinem Blatt verwendet – kein Handlungsbedarf (2026-09-17)
- [x] `latent-classifier.ipynb` in slides/ und exercises/ sind identisch (2026-09-17)
