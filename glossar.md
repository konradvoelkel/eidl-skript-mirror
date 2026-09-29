---
title: "Glossar zur Klausurvorbereitung"
short_title: "Glossar"
---

# Glossar zur Klausurvorbereitung

Die Begriffe, die in Klausuraufgaben vorkommen, je in ein bis drei Sätzen, mit Link zum Kapitel. Das Glossar ersetzt nicht die Kapitel; es ist zum Abhaken gedacht: Wer einen Eintrag liest und nicht erklären kann, warum er stimmt, liest das Kapitel.

## Grundbegriffe

**Deep Learning** ist das Training künstlicher neuronaler Netze mit vielen Schichten. Es ist ein Teilgebiet des maschinellen Lernens und orthogonal zur Frage supervised, unsupervised oder reinforcement. [Was ist Deep Learning?](part-grundlagen/01-was-ist-deep-learning.md)

**Training und Inferenz.** Training: Daten rein, gefittetes Modell (Gewichte) raus. Inferenz: neue Daten und Gewichte rein, Vorhersage raus. [Was ist Deep Learning?](part-grundlagen/01-was-ist-deep-learning.md)

**Train-Test-Split, Validation-Split.** Testdaten werden zurückgehalten, um die Güte zu messen. Wer Hyperparameter nach dem Testset wählt, overfittet indirekt darauf; dafür spaltet man vom Trainingsset ein Validation-Set ab. [Was ist Deep Learning?](part-grundlagen/01-was-ist-deep-learning.md)

**Accuracy, Precision, Recall.** Accuracy ist der Anteil richtiger Vorhersagen und bei unbalancierten Klassen irreführend. Precision: Anteil der als positiv vorhergesagten, die wirklich positiv sind. Recall: Anteil der wirklich positiven, die gefunden wurden. [Was ist Deep Learning?](part-grundlagen/01-was-ist-deep-learning.md)

**Over- und Underfitting.** Overfitting: gut auf Trainings-, schlecht auf Testdaten, das Modell hat auswendig gelernt. Underfitting: schon auf Trainingsdaten schlecht. Gegenmittel gegen Overfitting sind Regularisierung, Early Stopping, Data Augmentation, Dropout. [Autoencoder](part-representation-learning/14-autoencoder.md)

**Generatives Modell.** Ein Modell für eine Wahrscheinlichkeitsverteilung, als Dichte oder als Sampler. Generieren heißt aus dieser Verteilung samplen. [Was ist Deep Learning?](part-grundlagen/01-was-ist-deep-learning.md)

## Neuron, Perzeptron, Netz

**Iverson-Klammer.** $[A] = 1$, wenn $A$ wahr ist, sonst $0$. Das Perzeptron ist $f(x) = [w \cdot x + b > 0]$. [Neuron und Perzeptron](part-grundlagen/02-neuron-perzeptron.md)

**Perzeptron ohne Bias** kann nur Hyperebenen durch den Ursprung lernen. Der Bias lässt sich als nulltes Gewicht mit konstanter Eingabe $1$ schreiben. [Neuron und Perzeptron](part-grundlagen/02-neuron-perzeptron.md)

**Linear trennbar.** Zwei Klassen, die eine Hyperebene trennt. Nur solche kann ein einzelnes Perzeptron lernen; XOR ist das Gegenbeispiel. [Neuron und Perzeptron](part-grundlagen/02-neuron-perzeptron.md)

**Perzeptronregel und Konvergenz.** $w_{\text{neu}} = w + \rho\,(y - f(x))\,x$. Bei linear trennbaren Daten findet die Regel nach endlich vielen Fehlern eine trennende Hyperebene; sonst terminiert sie nie. [Das Perzeptron trainieren](part-grundlagen/03-perzeptron-trainieren.md)

**Verallgemeinertes Perzeptron.** Skalarprodukt, dann Aktivierungsfunktion $\tau$: lineare Regression ($\tau = \operatorname{id}$), Perzeptron (Sprung), logistische Regression ($\tau = \sigma$). [Das Perzeptron trainieren](part-grundlagen/03-perzeptron-trainieren.md)

**Warum Schichten ohne Nichtlinearität nichts bringen.** Ein Produkt von Matrizen ist eine Matrix; gestapelte lineare Regressionen sind eine lineare Regression. [Das Perzeptron trainieren](part-grundlagen/03-perzeptron-trainieren.md)

**Tensor.** Für uns ein mehrdimensionales Array. Die Zahl der Achsen heißt *Stufe* oder, englisch, *rank*: Rang 0 ist ein Skalar, Rang 1 ein Vektor, Rang 2 eine Matrix (nicht zu verwechseln mit dem Rang einer Matrix aus der linearen Algebra). Die erste Achse ist in PyTorch fast immer der Batch – außer bei `nn.RNN`, `nn.LSTM`, `nn.GRU` und `nn.Transformer`, die voreingestellt `(seq, batch, feature)` erwarten. `reshape` ändert nur die Klammerung, nicht die Daten. [Tensoren](part-grundlagen/05-tensoren.md)

## Logistische Regression und Loss

**Odds und Logit.** $\operatorname{odds}(p) = p/(1-p)$, bei $p = \tfrac12$ also $1{:}1$. $\operatorname{logit}(p) = \ln \operatorname{odds}(p)$, die Umkehrfunktion von $\sigma$. [Logistische Regression](part-lernen/06-logistische-regression.md)

**Sigmoid.** $\sigma(x) = 1/(1 + e^{-x})$, Werte in $(0, 1)$, $\sigma(-x) = 1 - \sigma(x)$, $\sigma' = \sigma(1 - \sigma)$. Die Ausgabe ist eine Wahrscheinlichkeit, wenn die Eingabe ein Logit ist. [Logistische Regression](part-lernen/06-logistische-regression.md)

**Softmax.** $\operatorname{sm}_j(v) = e^{v_j} / \sum_k e^{v_k}$, ohne Minus im Exponenten; summiert zu $1$, verallgemeinert $\sigma$ auf $K$ Klassen, nur Differenzen der Logits zählen. Für sich nicht ausschließende Klassen (Tags) stattdessen ein Sigmoid pro Klasse. [Logistische Regression](part-lernen/06-logistische-regression.md)

**Kreuzentropie, NLL, KL-Divergenz.** Die Kreuzentropie ist die negative Log-Likelihood des Modells und unterscheidet sich von der KL-Divergenz nur um die Entropie der wahren Verteilung, die nicht von den Gewichten abhängt. [Loss-Funktionen und Maximum Likelihood](part-lernen/07-loss-funktionen-maximum-likelihood.md)

**Maximum Likelihood.** Wähle die Gewichte, unter denen die Daten am wahrscheinlichsten sind. Liefert BCE für die logistische und MSE für die lineare Regression mit Gauß-Rauschen. [Loss-Funktionen und Maximum Likelihood](part-lernen/07-loss-funktionen-maximum-likelihood.md)

**Hinge Loss.** $\max(0, 1 - f(x))$ für $y = 1$: verlangt einen Sicherheitsabstand, der Loss der Support Vector Machine. Der Perceptron Loss ist $\max(0, -f(x))$. [Gradientenabstieg](part-lernen/08-gradientenabstieg.md)

## Gradientenabstieg

**Gradient und Update.** Der Gradient zeigt bergauf; $w_{\text{neu}} = w_{\text{alt}} - \rho\, L'(w_{\text{alt}})$ geht bergab. Beim Ableiten immer sagen, wonach: nach $w$, die Daten sind Konstanten. [Gradientenabstieg](part-lernen/08-gradientenabstieg.md)

**Kettenregel.** Die Ableitung einer Verkettung ist das Matrixprodukt der Jacobi-Matrizen. Geht eine Variable auf mehreren Pfaden ein, addieren sich die Beiträge. [Gradientenabstieg](part-lernen/08-gradientenabstieg.md)

**Lernrate.** Zu klein: ewig langsam. Zu groß: springt über das Tal, Loss steigt oder wird `nan`. Hängt von der Skalierung der Features ab, deshalb standardisieren. [Gradientenabstieg](part-lernen/08-gradientenabstieg.md)

**SGD, Mini-Batch, Epoche.** SGD schätzt den Gradienten aus einem Teil der Daten statt aus allen; der Schätzer ist verrauscht, aber im Mittel korrekt. Ein Mini-Batch sind einige Dutzend Samples, eine Epoche ein Durchlauf durch alle Daten. Der Loss darf von Batch zu Batch steigen. [Gradientenabstieg](part-lernen/08-gradientenabstieg.md)

**Sattelpunkt.** Ein Punkt mit Gradient null, der in einer Richtung Minimum und in einer anderen Maximum ist. In hohen Dimensionen häufiger als lokale Minima; Momentum hilft, ihn zu verlassen. [Optimierer](part-architekturen-anwendungen/26-optimierer.md)

**Momentum, Adam.** Momentum mittelt Gradienten über Schritte, Adam passt zusätzlich die Lernrate pro Gewicht an die bisherige Größe der Gradienten an (mittleres Gradientenquadrat). Faustregel im Kurs: Adam statt SGD. [Optimierer](part-architekturen-anwendungen/26-optimierer.md)

## Backpropagation und Autograd

**Backpropagation.** Kettenregel plus Buchführung: im Forward Pass Zwischenergebnisse merken, dann rückwärts Schicht für Schicht das Fehlersignal mit der transponierten Gewichtsmatrix und der Ableitung der Aktivierung weiterreichen. Aufwand etwa das Doppelte einer Inferenz. [Backpropagation](part-lernen/09-backpropagation.md)

**Berechnungsgraph, DAG.** PyTorch baut beim Vorwärtsrechnen einen gerichteten azyklischen Graphen der Operationen; `backward` läuft ihn rückwärts ab und schreibt Gradienten in `.grad`. Die Eingabe ist nur ein weiteres Blatt, deshalb geht Gradientenabstieg auch im Eingaberaum. [Autograd und Berechnungsgraph](part-lernen/10-autograd-berechnungsgraph.md)

**`requires_grad`, Einfrieren.** Nur Tensoren mit `requires_grad` bekommen Gradienten und kosten Speicher für den Graphen. Ein vortrainiertes Modell einfrieren heißt, seine Parameter davon auszunehmen und nur den Kopf zu trainieren. [Autograd und Berechnungsgraph](part-lernen/10-autograd-berechnungsgraph.md)

**Geteilte Gewichte.** Kommt ein Gewicht an mehreren Stellen vor (Faltung, rekurrente Netze), ist sein Gradient die Summe der Beiträge aller Stellen. [Autograd und Berechnungsgraph](part-lernen/10-autograd-berechnungsgraph.md)

## Aktivierungsfunktionen und Universalität

**ReLU und ihre Ableitung.** $\max(0, x)$ mit schwacher Ableitung $[x > 0]$. Billig, kein Sättigen im Positiven. [Aktivierungsfunktionen](part-lernen/11-aktivierungsfunktionen.md)

**Vanishing Gradient.** Sigmoid hat Ableitung höchstens $\tfrac14$; über viele Schichten multipliziert verschwindet der Gradient. ReLU vermeidet das im Positiven. [Aktivierungsfunktionen](part-lernen/11-aktivierungsfunktionen.md)

**Sterbende Neuronen, Swish, GELU.** Ein ReLU-Neuron mit negativer Aktivierung für alle Daten bekommt nie wieder einen Gradienten. Leaky ReLU, Swish (SiLU) und GELU lassen im Negativen ein kleines Signal durch. [Aktivierungsfunktionen](part-lernen/11-aktivierungsfunktionen.md)

**Universelle Approximation.** Ein Netz mit einer versteckten Schicht kann jede stetige Funktion auf einem beschränkten Bereich beliebig gut annähern, aus Treppen- oder Knickfunktionen. Sagt nichts darüber, ob der Gradientenabstieg die Gewichte findet, und nichts über Extrapolation. [Universelle Approximation](part-lernen/13-universelle-approximation.md)

**Dropout, Batch Normalization.** Dropout setzt im Training zufällig Aktivierungen auf null, gegen Overfitting. Batch Normalization normiert die Ausgabe einer Schicht über den Batch auf Mittelwert null und Varianz eins, mit lernbarer Rückskalierung. [Autoencoder](part-representation-learning/14-autoencoder.md)

## Autoencoder und latente Räume

**Autoencoder.** Encoder von $D$ auf $L \ll D$ Dimensionen, Decoder zurück, Loss ist die Rekonstruktion (MSE). Approximiert die Identität durch einen Flaschenhals, braucht keine Label, komprimiert. Der Decoder erhöht die Dimension. Linear ist er PCA. [Autoencoder](part-representation-learning/14-autoencoder.md)

**Standard-AE ist nicht generativ, VAE schon.** Der klassische Autoencoder lässt Löcher im latenten Raum; der VAE zwingt die Codes zur Standardnormalverteilung, danach kann man samplen und dekodieren. [Variational Autoencoder](part-representation-learning/15-variational-autoencoder.md)

**Denoising AE.** Rauschen auf die *Eingabe*, Loss gegen das *saubere* Bild. [Autoencoder](part-representation-learning/14-autoencoder.md)

**Sparse AE.** Strafterm, der die mittlere Aktivierung jeder latenten Dimension klein hält; muss zum Loss addiert werden. [Autoencoder](part-representation-learning/14-autoencoder.md)

**Weight Decay, L2-Regularisierung.** $\lambda \|W\|^2$ zum Loss, zieht Gewichte Richtung null; in PyTorch ein Parameter des Optimierers. [Autoencoder](part-representation-learning/14-autoencoder.md)

**Early Stopping, Data Augmentation.** Aufhören, wenn der Testloss wieder steigt; Trainingsdaten durch labelerhaltende Transformationen vervielfachen. [Autoencoder](part-representation-learning/14-autoencoder.md)

**Reparametrisierungstrick.** Statt aus $\mathcal{N}(\mu_x, \sigma_x^2)$ zu samplen, sample $\varepsilon \sim \mathcal{N}(0, 1)$ und setze $y = \mu_x + \sigma_x \varepsilon$; dann ist $\varepsilon$ eine Konstante und der Gradient fließt durch $\mu_x$ und $\sigma_x$. [Variational Autoencoder](part-representation-learning/15-variational-autoencoder.md)

**`logvar`.** Der Encoder gibt $\ln \sigma_x^2$ aus statt $\sigma_x$, damit kein Ausgang auf positive Werte eingeschränkt werden muss. [Variational Autoencoder](part-representation-learning/15-variational-autoencoder.md)

**Latent Space, Manifold-Hypothese.** Die Daten liegen nahe einer niedrigdimensionalen gekrümmten Fläche; der latente Raum parametrisiert sie. Gerade Linien zwischen Codes können die Fläche verlassen: Interpolation gut, Extrapolation schlecht. [Latente Räume geometrisch](part-architekturen-anwendungen/23-latente-raeume.md)

## Text, Graphen, Sequenzen

**word2vec: CBOW und Skip-gram.** CBOW sagt aus dem Kontext das Wort voraus, Skip-gram aus dem Wort den Kontext. Die eine Gewichtsmatrix ist das Embedding. [word2vec](part-representation-learning/16-word2vec.md)

**Embedding-Layer.** Eine Lookup-Tabelle, die einer ID (Wort, Item, Nutzer) einen gelernten Vektor zuordnet, `nn.Embedding`. [word2vec](part-representation-learning/16-word2vec.md)

**Temperatur- und Top-k-Sampling.** Beim Generieren die Logits durch $T$ teilen (klein: gieriger, groß: zufälliger) oder nur unter den $k$ wahrscheinlichsten Token samplen. [Latente Räume geometrisch](part-architekturen-anwendungen/23-latente-raeume.md)

**node2vec.** Random Walks auf einem Graphen erzeugen „Sätze“, darauf word2vec. So bekommen Knoten Vektoren, etwa Items eines Empfehlungssystems. [Representation Learning und Graphen](part-representation-learning/17-representation-learning-graphen.md)

**RNN, GRU, LSTM.** Ein rekurrentes Netz verarbeitet eine Sequenz Schritt für Schritt und trägt einen Zustand mit, deshalb geeignet für Zeitreihen. LSTM und GRU steuern mit Gates, was in den Zustand geschrieben und gelesen wird, gegen verschwindende Gradienten über lange Sequenzen. [RNNs](part-representation-learning/18-rnn.md)

**Transformer, Attention.** Kein rekurrentes Netz: Jedes Token vergleicht seine Query mit den Keys aller anderen und mischt deren Values, alles parallel. Positionsinformation kommt über ein Positionsembedding, gelernt oder fest. [Transformer](part-representation-learning/19-transformer.md)

**BERT und GPT.** BERT ist ein Encoder, trainiert mit maskierten Wörtern (Masked Language Model), liefert kontextabhängige Embeddings, die man als Features klassifizieren kann. GPT ist ein Decoder, trainiert auf das nächste Token. [Transformer](part-representation-learning/19-transformer.md)

## Faltung und CNNs

**Faltung.** An jeder Stelle ein Skalarprodukt des Filters mit einem gespiegelten Ausschnitt des Signals. Ein Faltungslayer ist ein spezieller linearer Layer mit vielen Nullen und geteilten Gewichten. [Faltung und CNNs](part-architekturen-anwendungen/20-faltung-cnn.md)

**Parameter Sharing, Translationsäquivarianz.** Derselbe Filter an jeder Position: wenige Parameter, und ein verschobenes Bild gibt eine verschobene Feature Map. [Faltung und CNNs](part-architekturen-anwendungen/20-faltung-cnn.md)

**Ausgabegröße.** $\lfloor (n + 2p - k)/s \rfloor + 1$ für Eingabe $n$, Padding $p$, Kernel $k$, Stride $s$. Stride und Pooling verkleinern die Feature Map. Vor dem linearen Kopf `Flatten`. [Faltung und CNNs](part-architekturen-anwendungen/20-faltung-cnn.md)

**Pooling.** Max- oder Average-Pooling verkleinert ohne Parameter und macht das Netz robust gegen kleine Verschiebungen. [Faltung und CNNs](part-architekturen-anwendungen/20-faltung-cnn.md)

**1×1-Faltung.** Ändert die Kanalzahl, nicht die räumliche Größe: eine lineare Abbildung pro Pixel. [Faltung und CNNs](part-architekturen-anwendungen/20-faltung-cnn.md)

**Gauß-Kernel.** Glättet (Tiefpass). Frühe CNN-Schichten lernen von selbst Kanten- und Balkendetektoren. [Faltung und CNNs](part-architekturen-anwendungen/20-faltung-cnn.md)

## Vortrainierte Modelle, LLMs, Destillation

**Transfer Learning, Finetuning.** Ein auf großen Daten (ImageNet, COCO) vortrainiertes Modell als Startpunkt: Features einfrieren und nur den Kopf trainieren, oder alle Gewichte mit kleiner Lernrate nachtrainieren. [Vortrainierte Modelle](part-grundlagen/04-vortrainierte-modelle.md), [LLMs benutzen](part-architekturen-anwendungen/21-llms-benutzen.md)

**Object Detection, Segmentierung.** Detection liefert Klassen mit Bounding Boxes, der Loss kombiniert Klassifikation und Box-Regression; Segmentierung liefert pro Pixel eine Klasse. [Vortrainierte Modelle](part-grundlagen/04-vortrainierte-modelle.md)

**Lokale LLMs, Quantisierung.** Mit Ollama oder llama.cpp laufen Modelle mit wenigen Milliarden Parametern in 4-Bit-Quantisierung auf der CPU. Ein LLM liefert eine Verteilung über dem Vokabular, die man auslesen, als Vektor weiterverarbeiten oder per Constrained Generation einschränken kann. [LLMs benutzen](part-architekturen-anwendungen/21-llms-benutzen.md)

**Destillation.** Ein kleines Schülernetz lernt per Regression die (mit Temperatur aufgeweichten) Ausgaben eines großen Lehrers, nicht nur die harten Labels. Speculative Decoding nutzt ein kleines Modell zum Vorschlagen und das große zum Prüfen. [Destillation](part-architekturen-anwendungen/25-destillation.md)

**Multimodal, Encoder-Decoder.** Ein Modell mit Encoder für die eine Modalität und Decoder für die andere (Bild zu Text, Text zu Bild); die Verbindung läuft über einen gemeinsamen latenten Raum. [Vortrainierte Modelle](part-grundlagen/04-vortrainierte-modelle.md)

## GANs

**Generator und Diskriminator.** Der Generator bekommt Rauschen, nie Daten, und sieht die Daten nur über den Gradienten des Diskriminators. Der Diskriminator schätzt die Wahrscheinlichkeit, dass ein Sample echt ist. Beide werden abwechselnd mit Backpropagation trainiert. [GANs](part-architekturen-anwendungen/22-gans.md)

**Mode Collapse, Wasserstein.** Mode Collapse: der Generator produziert nur noch wenige Varianten. Wasserstein-GANs ersetzen die Kreuzentropie durch eine Transportdistanz mit einem Kritiker, der reelle Zahlen ausgibt; das gibt auch bei nicht überlappenden Verteilungen einen Gradienten. [GANs](part-architekturen-anwendungen/22-gans.md)

## Anwendungen

**Empfehlungssystem im Latent Space.** Items als Vektoren, sodass gemeinsam gekaufte Items nahe liegen (word2vec auf Kauflisten, node2vec, Two-Tower); empfohlen wird, was nahe an den bisherigen Items liegt. [Anwendungsbeispiele](part-architekturen-anwendungen/24-anwendungsbeispiele.md)

**Anwendungskonzept.** Was haben wir, was soll rauskommen, welches Modell und woher, welcher Loss, womit messen wir Güte, was kann schiefgehen. [Anwendungsbeispiele](part-architekturen-anwendungen/24-anwendungsbeispiele.md)

**Adversarial Example.** Eine für Menschen unsichtbare Änderung der Eingabe, die die Klassifikation kippt; gefunden per Gradientenabstieg im Eingaberaum. [Adversarial Attacks und Polysemie](part-architekturen-anwendungen/27-adversarial-attacks-polysemie.md)
