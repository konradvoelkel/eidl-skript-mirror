---
title: "Einführung in Deep Learning"
---

Dieses Skript begleitet die Vorlesung mit Übung „Einführung in Deep Learning“ im Bachelor Informatik an der HHU Düsseldorf, Wintersemester 2026/27. Es führt vom einzelnen Neuron über Gradientenabstieg und Backpropagation bis zu Autoencodern, Transformern und großen Sprachmodellen, mit durchgerechneten Beispielen und Code in PyTorch.

Vorausgesetzt wird, was das Modul Data Science vermittelt: Python mit NumPy und die Idee der linearen Regression. Die nötige lineare Algebra und Analysis stehen in zwei Hintergrundkapiteln, die Stochastik im [Data-Science-Skript](https://voelkel.pages.cs.uni-duesseldorf.de/ds-skript/). Lernziele, Aufzeichnungen und Literatur stehen unter [Über dieses Skript](README.md). Fast jedes Kapitel endet mit einer kurzen Übung samt Antwortprobe; die Übungsblätter gibt es in ILIAS.

{button}`Das ganze Skript als PDF </eidl-skript.pdf>`

:::{note} Hinweis
Wenn Sie Fehler finden oder etwas unklar ist, freue ich mich über eine Nachricht – Konrad Völkel. Am einfachsten als [Issue auf GitHub](https://github.com/konradvoelkel/eidl-skript-mirror/issues).
:::

## Inhalt

### Grundlagen

- [Was ist Deep Learning?](part-grundlagen/01-was-ist-deep-learning.md) – Begriffe, Python als Werkzeug, eine kurze Geschichte
- [Hintergrundwissen Lineare Algebra](part-grundlagen/hintergrundwissen-lineare-algebra.md) – Vektoren, Skalarprodukt, Matrizen
- [Hintergrundwissen Analysis](part-grundlagen/hintergrundwissen-analysis.md) – Gradient, Kettenregel, Jacobi- und Hesse-Matrix
- [Neuron und Perzeptron](part-grundlagen/02-neuron-perzeptron.md) – gewichtete Summe mit Schwelle, die trennende Gerade
- [Das Perzeptron trainieren](part-grundlagen/03-perzeptron-trainieren.md) – die Lernregel, zum Ausprobieren im Widget
- [Vortrainierte Modelle verwenden](part-grundlagen/04-vortrainierte-modelle.md) – Hugging Face, Tasks, Rechnen auf der GPU
- [Tensoren](part-grundlagen/05-tensoren.md) – Arrays in NumPy und PyTorch

### Lernen

- [Logistische Regression](part-lernen/06-logistische-regression.md) – Sigmoid, Logit, Softmax
- [Loss-Funktionen und Maximum Likelihood](part-lernen/07-loss-funktionen-maximum-likelihood.md) – die Kreuzentropie hergeleitet
- [Gradientenabstieg](part-lernen/08-gradientenabstieg.md) – Lernrate und Mini-Batches, mit Widget
- [Backpropagation](part-lernen/09-backpropagation.md) – Gradienten von Hand, Schicht für Schicht
- [Autograd und Berechnungsgraph](part-lernen/10-autograd-berechnungsgraph.md) – wie PyTorch ableitet
- [Aktivierungsfunktionen](part-lernen/11-aktivierungsfunktionen.md) – ReLU, GELU und Verwandte
- [Netze von Hand bauen](part-lernen/12-netze-von-hand.md) – OR, NOR und XOR aus Perzeptrons
- [Universelle Approximation](part-lernen/13-universelle-approximation.md) – das Theorem und Double Descent

### Representation Learning

- [Autoencoder](part-representation-learning/14-autoencoder.md) – Lernen ohne Label
- [Variational Autoencoder](part-representation-learning/15-variational-autoencoder.md) – der Autoencoder als probabilistisches Modell
- [Wortvektoren: word2vec](part-representation-learning/16-word2vec.md) – Embeddings aus dem Kontext
- [Representation Learning und Graphen](part-representation-learning/17-representation-learning-graphen.md) – node2vec und Graph Neural Networks
- [Recurrent Neural Networks](part-representation-learning/18-rnn.md) – Sequenzen, LSTM und GRU
- [Transformer](part-representation-learning/19-transformer.md) – Self-Attention mit Query, Key und Value

### Architekturen und Anwendungen

- [Faltung und Convolutional Neural Networks](part-architekturen-anwendungen/20-faltung-cnn.md) – Faltung, Pooling, CNNs
- [LLMs benutzen](part-architekturen-anwendungen/21-llms-benutzen.md) – große Sprachmodelle per API und lokal
- [Generative Adversarial Networks](part-architekturen-anwendungen/22-gans.md) – Generator gegen Diskriminator
- [Latente Räume geometrisch](part-architekturen-anwendungen/23-latente-raeume.md) – Arithmetik und Interpolation im latenten Raum
- [Anwendungsbeispiele](part-architekturen-anwendungen/24-anwendungsbeispiele.md) – Chatbot, E-Mails klassifizieren, Empfehlungssystem
- [Destillation](part-architekturen-anwendungen/25-destillation.md) – kleine Netze lernen von großen
- [Optimierer: Momentum, Adam, Muon](part-architekturen-anwendungen/26-optimierer.md) – was über SGD hinausgeht
- [Adversarial Attacks und Polysemie](part-architekturen-anwendungen/27-adversarial-attacks-polysemie.md) – Netze täuschen, mehrdeutige Wörter

### Anhang

- [Glossar zur Klausurvorbereitung](glossar.md) – die Klausurbegriffe, je mit Link ins Kapitel
