# Migrationsplan EiDL 2025/26 → 2026/27

Stand: 2026-09-17

## Ausgangslage

- Die Folien aus 2025/26 liegen nur als Google-Slides-Exporte (PDF) vor, siehe `../from_2025/slides/`.
- Übungsblätter (LaTeX, `../from_2025/exercises/`) und Klausuren (LaTeX, `../from_2025/exam/`) sind vollständig als Quelltext vorhanden.
- Das neue Modul-Vorstellungsdeck (`../slides/`) ist bereits im üblichen LaTeX-Beamer-Stil (hhubeamer, Source Sans Pro).

## Migrationspfad

1. **Skript aufsetzen** (dieses Projekt, MyST wie `eipy-skript`) und die Inhalte der 15 Vorlesungen in Reihenfolge festhalten.
   Erledigt als automatische Transkription der Folien (Folie für Folie, `<!-- Folie N -->`-Marker), erzeugt durch
   ein Skript aus den PDFs. Formeln (Unicode-Mathe aus Google Slides) und Abbildungen müssen von Hand nachgezogen werden.
2. **Inhalt überarbeiten**: Text in eigene Worte bringen, Formeln in LaTeX setzen, Abbildungen ersetzen/neu erzeugen (matplotlib),
   Redundanzen aus inkrementellen Folien (Overlays) zusammenfassen. Dabei sicherstellen, dass alles enthalten ist, was
   Übungsblätter und Klausur-Aufgabenschatz voraussetzen (siehe Tabelle unten).
3. **Übungsblätter** anpassen (`part-exercises/`, bereits per pandoc konvertiert; Abgabetermine noch aus 2025).
4. **Danach** neue Beamer-Decks aus dem Skript ableiten, Themenfolge wie bisher, Header aus `../slides/Einführung in Deep Learning 2026 header.tex`.

## Zuordnung Vorlesung ↔ Kapitel ↔ Übungsblatt ↔ Klausur

| VL | Kapitel | Blatt (2025) | Klausur-Aufgabenschatz (Bezug) |
|----|---------|--------------|--------------------------------|
| 01 | `part-grundlagen/01-ueberblick-perzeptron.md` | 00 (Lin. Algebra: Skalarprodukt, Orthogonalität, Länge), 01 (Winkel, NumPy, Matplotlib) | A1 MC: Perzeptron ohne Bias |
| 02 | `part-grundlagen/02-perzeptron-vortrainierte-modelle.md` | 02 (Perzeptron in NumPy) | A2 Anwendungskonzept (Transfer Learning) |
| 03 | `part-grundlagen/03-pytorch-tensoren.md` | 03 (verallg. Perzeptron, schwache Ableitung), 04 (PyTorch) | A1 MC: `requires_grad`, Tensor-Rang; A3 Code-Verständnis |
| 04 | `part-lernen/04-logistische-regression.md` | 05 (Sigmoid, Softmax, Kreuzentropie) | A1 MC: Odds, Sigmoid, Softmax |
| 05 | `part-lernen/05-sgd.md` | — | A1 MC: SGD; A4 Update-Schritt |
| 06 | `part-lernen/06-backprop.md` | 07 (Backprop von Hand, 2×2 ReLU) | A4 Backpropagation & Update; A1 MC: vanishing gradient, ReLU-Ableitung |
| 07 | `part-representation-learning/07-autoencoder.md` | 06 (Autoencoder) | A1 MC: Swish/sterbende Neuronen, AE ≈ Identität, Dropout |
| 08 | `part-representation-learning/08-latent-space-vae.md` | 08 (Denoising/Label-AE MNIST), 09 (VAE, Frenzel) | A1 MC: Reparameterization Trick, Denoising AE, word2vec CBOW/Skip-Gram |
| 09 | `part-representation-learning/09-representation-learning.md` | — | A1 MC: BERT Masked LM, RNN/LSTM, Positionsembedding |
| 10 | `part-architekturen-anwendungen/10-cnn.md` | 10 (Faltung, Filter, Pooling) | A1 MC: 1×1-Faltung, Äquivarianz, Parameter-Sharing, Stride, Gauß-Kernel |
| 11 | `part-architekturen-anwendungen/11-llms-benutzen.md` | 11 (BERT latent classifier) | A1 MC: Ollama/quantisierte LLMs; A3 Code-Verständnis |
| 12 | `part-architekturen-anwendungen/12-gans.md` | — | A1 MC: Diskriminator, Generator-Input, WGAN/Mode Collapse |
| 13 | `part-architekturen-anwendungen/13-latent-spaces-anwendungen.md` | — | A1 MC: Empfehlungssystem im Latent Space; A2 Anwendungskonzept |
| 14 | `part-architekturen-anwendungen/14-destillation.md` | — | A5 gruppierte MC |
| 15 | `part-architekturen-anwendungen/15-maerchenstunde.md` | 12 = Take-Home-Probeklausur | — |

Klausurformat 2025/26: 6 Aufgaben, 55 Punkte, 90 Minuten, keine Hilfsmittel; Aufgabentypen laut
`../from_2025/exam/exam2025-eidl-aufgabenschatz.tex`: (1) Multiple Choice W/F, (2) Anwendungskonzept,
(3) Code-Verständnis, (4) Backpropagation & Update, (5) gruppierte Multiple Choice, jeweils in Sets A–D.
Entwürfe für 2026 (englisch, amsart): `exam2026-eidl-exam-1.tex`, `exam2026-eidl-exam-2.tex`.

## Offene Punkte / Ideen

- Im Vorstellungsdeck 2026 ist die geplante Reihenfolge leicht anders als 2025: Logistische Regression und SGD/Backprop
  *vor* PyTorch. Entscheiden, ob Kapitel 03 (PyTorch) nach hinten wandert.
- VL 08 war 2025 mit 85 Folien überladen (AE-Varianten + VAE + word2vec + NLP); ggf. word2vec/NLP in Kapitel 09 verschieben.
- VL 06 endet bereits mit Autoencoder-Einführung, VL 07 beginnt mit „handgemachten Netzen" (Universalität) – Kapitelgrenzen neu ziehen.
- Lehrbuchbezug: Prince, *Understanding Deep Learning* (Kapitel pro Thema referenzieren), Deisenroth et al. für Mathe-Grundlagen.
- Notebooks (`notebooks/`) laufen noch nicht im Build (`jupyter: true` ohne Kernel-Setup); Datensätze (MNIST) nicht im Repo.
- Englische Übungsblätter (`sheetNN.tex`) sind nicht konvertiert; bei Bedarf gleicher Weg über pandoc.
