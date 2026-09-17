# TODO eidl-skript

Stand: 2026-09-17. Erledigtes nach unten in „Erledigt“ verschieben.

## Inhalt (Skript)

- [ ] **Fachliche Durchsicht** der Prosafassung, insbesondere der Stellen, die über die Folien 2025 hinausgehen:
  - VL 01: Perzeptron-Definition vorgezogen, Hyperebenen-Geometrie, XOR über OR/NAND/AND
  - VL 02: Perzeptron-Konvergenzsatz (Novikoff), Tabelle verallg. Perzeptron
  - VL 03: Rang-0/1/2-Tensoren, `reshape`-Antwort
  - VL 04: $H'(p) = -\operatorname{logit}(p)$, $\tanh(x) = 2\sigma(2x)-1$, Softmax = $\sigma$(Differenz)
  - VL 05: Cauchy-Schwarz-Argument für die Gradientenrichtung, Hinge vs. Perceptron Loss
  - VL 06: $\delta_k$-Notation, ELU/Leaky/Swish/GELU-Formeln
  - VL 07: explizite ReLU-Interpolation $Q(x)$ für $x^2$ (Probe gerechnet), Weierstraß-Bemerkung
  - VL 08: KL-Term des Sparse AE, geschlossene Form der Gauß-KL, CBOW-Formel
  - VL 09: Message-Passing-, RNN-, Attention-Formel; BLEU als geometrisches Mittel
  - VL 10: 2D-Faltungsformel, Kanäle, 1×1-Faltung, Korrelation vs. Faltung
  - VL 11: Konvolutions-Backprop-Summe, LoRA-Parameterzahl, RAG-Skizze
  - VL 12: Minimax-Formel, DCGAN-Hinweis, Diffusion-Ablösung
  - VL 13: top-p, two-tower-Modell
  - VL 14: $T^2$-Faktor im Distillation Loss
  - VL 15: Momentum/Adam-Updategleichungen, FGSM-Formel, Polysemie-Absatz (aus Ruppik-Folien rekonstruiert)
- [ ] **Abbildungen** – 62 Stellen `<!-- TODO Abbildung -->`, Liste in `abbildungen-todo.txt`.
  Vorhandene Bilddateien in `../from_2025/slides/` (Tafelbilder, XOR-Playground, Bolukbasi Fig. 7, Arvanitidis Fig. 1, convolutions.png, asml.png); Rest per matplotlib neu erzeugen oder aus Google Slides exportieren.
- [ ] **Kapitelstruktur**: Reihenfolge laut Vorstellungsdeck 2026 (LogReg/SGD/Backprop *vor* PyTorch) – Kapitel 03 nach hinten?
- [ ] VL 06/07-Grenze neu ziehen (AE-Einführung am Ende von 06 vs. handgemachte Netze am Anfang von 07).
- [ ] VL 08 entlasten: word2vec/NLP-Teil nach VL 09 verschieben?
- [ ] Lehrbuchverweise ergänzen (Prince *UDL* Kapitel pro Thema; Deisenroth et al. für Mathe).
- [ ] „Stand“-Hinweisboxen am Kapitelanfang entfernen, sobald ein Kapitel durchgesehen ist.
- [ ] Formalia-Kapitel (`README.md`): Übungsleitung 2026/27, Räume/Zeiten bestätigen.

## Übungsblätter

- [ ] Abgabetermine 2026/27 eintragen (aktuell noch 2025-Daten mit Hinweis).
- [ ] Blätter an neue Kapitelreihenfolge anpassen; Blatt 12 = Take-Home-Probeklausur anlegen.
- [ ] Lösungen: bisher nur die in den `.tex` eingebetteten; Notebook-/Skript-Lösungen aus `../from_2025/exercises/blattNN-solution/` einbinden oder verlinken.
- [ ] Englische Fassungen (`sheetNN.tex`) – konvertieren oder fallen lassen?
- [ ] `hidefromsolutions`-Inhalte prüfen (werden vom Generator verworfen).

## Klausur

- [ ] Aufgabenschatz (`../from_2025/exam/exam2025-eidl-aufgabenschatz.tex`) gegen die Kapitel abgleichen: Deckt das Skript jede MC-Aussage ab? (Zuordnung in `migrationsplan.md`.)
- [ ] `exam2026-eidl-exam-1/2.tex` (englische Entwürfe) – Status klären.

## Notebooks

- [ ] `notebooks/` laufen nicht im Build (`jupyter: true` ist nur Thebe); entscheiden: ausgeführte Outputs einchecken oder `--execute` mit Python-Image.
- [ ] Datenabhängigkeiten: `ASML.csv`, `pallino.jpg`, MNIST-Download, Qwen-GGUF (491 MB, nicht ins Repo).
- [ ] `latent-classifier.ipynb` liegt doppelt vor (slides/ und exercises/), Version vergleichen.

## Infrastruktur

- [ ] GitLab Pages auf „Everyone“ stellen – **zum Semesterstart, bewusst noch nicht** (Site: https://eidl-skript-131e30.pages.cs.uni-duesseldorf.de/).
- [ ] PDF-Export (`myst build --pdf`) testen; LaTeX-Preamble aus EiPy übernommen, ungetestet.
- [ ] `_site/sidebar_footer.md` ist leer, `navbar_end.md` nur „Inhaltsverzeichnis“ – wie bei EiPy füllen?
- [ ] Ggf. Google Search Console Verification-Datei wieder in CI aufnehmen (wurde entfernt).

## Beamer-Folien (Schritt 4 des Migrationsplans)

- [ ] Erst nach Durchsicht des Skripts: pro Kapitel ein Beamer-Deck im Stil von `../slides/Einführung in Deep Learning 2026 header.tex` (hhubeamer).
- [ ] Entscheiden, ob Folien aus dem MyST-Quelltext generiert werden (myst → LaTeX-Export) oder von Hand.

## Erledigt

- [x] MyST-Projekt aufgesetzt, Struktur wie EiPy (2026-09-17)
- [x] 15 Kapitel als Prosafassung mit LaTeX-Formeln (2026-09-17)
- [x] Übungsblätter 00–11 per pandoc konvertiert (2026-09-17)
- [x] GitLab-Remote, CI mit kaniko-Image-Build, Pages-Deploy (2026-09-17)
