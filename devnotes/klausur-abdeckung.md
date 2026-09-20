# Abdeckung des Klausur-Aufgabenschatzes 2025/26 durch das Skript

Stand: 2026-09-17, automatischer Abgleich (Stichwortsuche, `devnotes/klausur-abdeckung.md` wird nicht automatisch aktualisiert).
Quelle: `../from_2025/exam/exam2025-eidl-aufgabenschatz.tex` – 49 MC-Aussagen (A1), 3 Anwendungskonzepte (A2),
5 Code-Verständnis-Sets (A3), 3 Backprop-Rechnungen (A4), 4 gruppierte MC-Sets (A5).

Die Kapitelnamen in der Tabelle beziehen sich auf den Stand vom 2026-09-17 (20 Kapitel). Seit den Kapitelsplits
am 2026-09-18 gilt: „Perzeptron“ → Neuron und Perzeptron / Perzeptron trainieren; „Backprop“ → Backpropagation /
Autograd; „Aktivierung/Univ.“ → Aktivierungsfunktionen / Netze von Hand / Universelle Approximation;
„RNN/Transformer“ → RNNs / Transformer; „VAE“ (latente Räume) und „word2vec“ (Geometrie) → Latente Räume geometrisch.

Seit 2026-09-20 gibt es zusätzlich „Loss-Funktionen und Maximum Likelihood“ (Kapitel 07, Split von „Gradientenabstieg“);
die Kapitel*namen* in der Tabelle gelten unverändert, die Dateinummern ab „Backpropagation“ sind um eins höher.

Die vier beim ersten Abgleich fehlenden Begriffe (Perzeptron ohne Bias, Early Stopping/Data Augmentation,
Precision/Recall, `logvar`) wurden am 2026-09-17 in die Kapitel eingearbeitet.

| Klausurbegriff | Kapitel |
|---|---|
| Softmax summiert zu 1 | RNN/Transformer |
| Berechnungsgraph / DAG | Adversarial, Backprop |
| Vanishing Gradient (Sigmoid vs ReLU) | GANs, Aktivierung/Univ. |
| 1×1-Faltung ändert Kanäle | CNN |
| Faltung = spezieller linearer Layer | CNN, RepL/Graphen |
| Translationsäquivarianz | CNN |
| Reparametrisierungstrick | VAE |
| ReLU-Ableitung | Aktivierung/Univ. |
| Sterbende Neuronen / Swish | Aktivierung/Univ. |
| Perzeptron ohne Bias nur durch Ursprung | **fehlt** |
| Wasserstein / Mode Collapse | GANs |
| CBOW vs Skip-gram Richtung | word2vec |
| Parameter Sharing | CNN |
| Diskriminator schätzt P(echt) | GANs |
| Generator bekommt Rauschen, keine Daten | GANs |
| Empfehlungssystem im Latent Space | Anwendungen |
| BERT-Embeddings als Features | LLMs |
| requires_grad / Einfrieren / Speicher | Backprop |
| Tensor Rang 0 = Skalar | Tensoren |
| Decoder erhöht Dimension | Autoencoder |
| BERT: Masked LM, nicht next token | Destillation, RNN/Transformer |
| Dropout | Aktivierung/Univ., Autoencoder |
| Stride reduziert Feature Map | CNN |
| Autoencoder komprimiert Bilder | Destillation, Gradientenabstieg, Autoencoder, RepL/Graphen |
| Standard-AE nicht generativ / VAE generativ | Autoencoder, VAE |
| LSTM/RNN für Zeitreihen | RNN/Transformer |
| SGD nutzt nicht den ganzen Datensatz | Gradientenabstieg |
| Ollama / quantisierte LLMs lokal | LLMs |
| Gauß-Kernel glättet | CNN |
| Transfer Learning | Backprop, Aktivierung/Univ. |
| AE approximiert Identität | GANs, Destillation, Backprop, Aktivierung/Univ., Autoencoder, RNN/Transformer |
| AE braucht keine Label | Destillation, Was ist DL, Autoencoder |
| Sigmoid-Ausgabe als Wahrscheinlichkeit | LogReg |
| CNN frühe Layer: Kanten | CNN |
| Average Pooling zur Dimensionsreduktion | CNN |
| Over-/Underfitting | Autoencoder |
| Deep Learning = viele Layer trainieren | Was ist DL |
| Odds bei p=0.5 sind 1:1 | LogReg |
| Positionsembedding (gelernt oder fest) | RNN/Transformer |
| Denoising AE: Rauschen auf Input, nicht Loss | Autoencoder |
| L2-Regularisierung / Weight Decay | Autoencoder |
| Early Stopping | **fehlt** |
| Data Augmentation | LLMs |
| Batch Normalization | Aktivierung/Univ., Autoencoder |
| Sattelpunkt | Gradientenabstieg |
| Lernrate zu groß / zu klein | Gradientenabstieg, Autoencoder |
| Object Detection / YOLO / Segmentierung | Was ist DL, Vortrainierte |
| Precision / Recall / mAP | **fehlt** |
| COCO / ImageNet Pretraining | Was ist DL, Vortrainierte |
| Kombinierter Loss (CE + Box-Regression) | Vortrainierte |
| GRU / LSTM | RNN/Transformer |
| Embedding-Layer für IDs | LLMs, word2vec |
| Multimodal / Encoder-Decoder | Destillation, Was ist DL |
| Finetuning | LLMs, GANs, Destillation, Vortrainierte, word2vec |
| Conv2d/MaxPool2d Shapes (16*6*6) | CNN |
| logvar im VAE | **fehlt** |
| Hinge Loss | Gradientenabstieg |
| Kreuzentropie = NLL = KL (bis auf Entropie) | LogReg, Autoencoder |
| Sequenzielle Daten: RNN speichert vorherige Schritte | RNN/Transformer |
| Speculative decoding / Destillation | LLMs, Destillation, Vortrainierte |
| Universal approximation | Aktivierung/Univ. |
| Perzeptron-Konvergenz | Perzeptron |
| Iverson-Klammer | Perzeptron |
| Kettenregel | Gradientenabstieg, Backprop, VAE |
| Temperatur-Sampling | Destillation, word2vec |
| Top-k Sampling | word2vec |

## Beobachtungen

- **A2 Anwendungskonzept** (Müllerkennung, Lagerbestände, Produktbeschreibungen) verlangt Wissen, das im Skript nur
  gestreift wird: Object Detection vs. Klassifikation (Kapitel „Vortrainierte Modelle“ nennt YOLOS, aber keinen
  Box-Regressions-Loss), Precision/Recall/mAP (jetzt in Kapitel 1), Zeitreihen-Vorverarbeitung (Aggregation,
  Normalisierung), multimodale Encoder-Decoder. Vorschlag: einen Abschnitt „Rezept für ein Anwendungskonzept“
  im Kapitel „Anwendungsbeispiele“ ergänzen, der genau diese Checkliste (Architektur → Daten → Loss → Metrik →
  Risiken) durchgeht – das ist der Aufgabentyp, und die drei Beispiele im Kapitel folgen ihm bereits implizit.
- **A3 Code-Verständnis** setzt `nn.Conv2d`/`nn.MaxPool2d`-Shape-Rechnung voraus (`16 * 6 * 6` bei 28×28-Eingabe).
  Das Skript erklärt Faltung und Pooling, aber rechnet keine Ausgabegrößen vor. Vorschlag: im CNN-Kapitel einen
  Absatz „Ausgabegröße einer Faltungsschicht“ mit der Formel $\lfloor (n + 2p - k)/s \rfloor + 1$ und dem
  Beispiel 28 → 24 → 12 → 8 → 4 (bzw. 6) ergänzen. Ebenso `nn.Flatten`/`nn.Unflatten`.
- **A4 Backprop & Update** (1D-Faltung + ReLU, Gradient nach Kernelgewicht): Das Kapitel „Backpropagation“ enthält
  jetzt das Notebook-Beispiel zu geteilten Gewichten (Summe der Beiträge), aber keine durchgerechnete Aufgabe mit
  ReLU-Maske. Vorschlag: das Set-A-Beispiel ($x=[2,0,-1,4]$, $k=[1,-1]$) als `prf:example` ins Kapitel.
- **A5 gruppierte MC**: Data Augmentation, Early Stopping, Sattelpunkte, Softmax vs. Sigmoid bei Multi-Label –
  alle nun im Skript, aber verstreut. Ein kurzes Glossar am Ende wäre für die Klausurvorbereitung hilfreich.
