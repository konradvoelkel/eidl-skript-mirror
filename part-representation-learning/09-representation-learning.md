---
title: "VL 09: Representation Learning, RNNs und Transformer"
short_title: "VL 09"
---

# Representation Learning, RNNs und Transformer

:::{note} Stand
Erste Prosafassung (aus den Folien von VL 09, WiSe 2025/26). Abbildungen fehlen noch, siehe die `TODO`-Kommentare.
:::

## Wiederholung: word2vec

Die Semantik eines Wortes ergibt sich durch seine Nutzung in Sätzen. Der unsupervised Machine-Learning-Task (CBOW): Gegeben Text, ersetze ein Wort durch [MASK] und lasse vorhersagen, was [MASK] ist – wie ein Denoising Autoencoder. Die Architektur ist ein Encoder $W \in \mathbb{R}^{K \times N}$ auf One-Hot-Vektoren, Mittelung über den Kontext, ein Decoder $W' \in \mathbb{R}^{N \times K}$ und Softmax. Die Spalten von $W$ sind die Wortvektoren.

## Representation Learning

### Worum geht's?

Gegeben Daten, die einer unbekannten Verteilung folgen, wollen wir *automatisch* Features entwickeln, die spätere Aufgaben mit diesen Daten erleichtern. Spätere Aufgaben können sein: die Verteilung schätzen (um daraus zu sampeln, z.B. Text generieren), Klassifikation (z.B. Spam/Ham), Ähnlichkeit bestimmen (z.B. zwischen zwei Texten).

Oberste Ziele sind eine höhere Modellperformance für die späteren Aufgaben und bessere Generalisierbarkeit. Ein weiteres Ziel ist möglicher **Transfer**: Features, die für eine Aufgabe gelernt wurden, für eine andere nutzen (Beispiel: Übersetzungen – ein Encoder für Englisch, der auch für Französisch etwas taugt).

Wie genau? Zwei Mechanismen haben wir bereits gesehen: Dimensionsreduktion durch „intelligentes Downsampling“ bzw. Kompression (wie beim Autoencoder), und nichtlineare neue Features aus alten Features entwickeln (jede versteckte Schicht tut das).

### Andere Features, die man manuell hinzufügen kann

Representation Learning ist die automatische Variante von *Feature Engineering*. Zwei klassische, handgemachte Beispiele:

* Das **Spektrogramm** einer Audiodatei. So wird eine Waveform-Datei (z.B. eine Unterhaltung, ein Song) in ein Bild umgewandelt, indem die (Kurzzeit-)Fourier-Transformation genutzt wird. Relevant für Sprachsynthese und Spracherkennung.
* Enthält ein Bild horizontale Kanten? Vertikale Kanten? Ecken? Ein Klassifikator für „das Bild enthält ein Haus“ ist leichter zu trainieren, wenn nicht nur Pixelwerte eingehen, sondern auch die Positionen von Ecken und Kanten. Die automatische Variante davon sind **CNNs** (Convolutional Neural Networks), nächstes Kapitel.

## node2vec

### word2vec aus anderer Perspektive

Ein Satz, wie er bei word2vec eingeht, kann als linearer Graph modelliert werden: „Die → Katze → frisst → Mäuse“. Mehrere Sätze können gleiche Wörter enthalten, damit bilden mehrere Sätze größere Graphen mit linearen Teilgraphen: „Der → Hund → frisst → Leckerli“ teilt sich den Knoten „frisst“ mit dem ersten Satz.

Mit diesem Graphen allein lassen sich die Sätze nicht zurückgewinnen, denn „Der Hund frisst Mäuse“ sowie „Die Katze frisst Leckerli“ sind keine ursprünglichen Sätze, aber Pfade im Graphen. Besser wäre ein probabilistisches Modell auf Grundlage des Graphen: für jeden Knoten $x$ eine Wahrscheinlichkeitsverteilung auf den Knoten $y$ mit Kante $x \to y$, abhängig von der vorherigen Kante $z \to x$ (eine Markovkette zweiter Ordnung).

<!-- TODO Abbildung: Satzgraph Die→Katze→frisst→Mäuse, Der→Hund→frisst→Leckerli (Folien 12–17) -->

### Aus anderer Perspektive: von Graphen zu Sätzen

Umgekehrt: Gegeben ein Graph, lassen sich daraus „Sätze“ bilden durch wiederholtes Verfolgen einer ausgehenden Kante. Vereinfachtes probabilistisches Modell auf Grundlage des Graphen: für jeden Knoten $x$ eine Gleichverteilung auf den Knoten $y$ mit Kante $x \to y$, unabhängig von der vorherigen Kante. Das ist ein **Random Walk**.

Beispiel mit einem Graphen aus der Wikipedia: Von „Katze“ führen Links zu „Maus“, „Mäuse“, „Sendung mit der Maus“; von „Maus“ zu „Computermaus“, „Lesk-Algorithmus“ (Wortsinn-Disambiguierung), … Daraus lassen sich endliche Random Walks bilden. Ziel: Verstehe einen Knoten durch seinen Kontext. Beispiel: Haushund und Hausmaus haben gemeinsame eingehende Links.

### node2vec praktisch

Bei **node2vec** (Grover & Leskovec, 2016) haben wir zwei Schritte:

1. Generiere „Sätze“ (Knoten, [Kontext]) durch Random Walks auf dem Graphen.
2. Benutze word2vec-Skip-gram-Training auf den Sätzen.

Schritt 1 ist sehr ressourcenintensiv, kann aber parallelisiert werden. Software dafür: [StellarGraph](https://stellargraph.readthedocs.io/en/stable/demos/link-prediction/node2vec-link-prediction.html) (OK API, nutzt gensim), eine schnelle Implementierung mit Apache Spark ([arXiv:1805.00280](https://arxiv.org/abs/1805.00280)), und als Modul für PyTorch [`torch_geometric.nn.models.Node2Vec`](https://pytorch-geometric.readthedocs.io/en/latest/generated/torch_geometric.nn.models.Node2Vec.html) (siehe auch das [Beispiel](https://github.com/pyg-team/pytorch_geometric/blob/master/examples/node2vec.py)).

Beispielanwendungen: [Recommendations using node2vec](https://www.kaggle.com/code/himj26/recommedations-using-node2vec) – aus einem Netflix-Datensatz werden Serien und Filme sowie deren Genres extrahiert und zu einem bipartiten Graphen Titel → Genre gebaut; nach node2vec kann man zu einem Titel im Latent Space nach ähnlichen Titeln suchen. Ähnlich, mit mehr Klassen von Knoten: [Knowledge graph analysis with node2vec](https://www.kaggle.com/code/ferdzso/knowledge-graph-analysis-with-node2vec).

:::{admonition} Denkaufgabe
:class: hint
Wie könnte *wav2vec* aussehen – word2vec für Audio? Was sind die „Wörter“, was ist der „Kontext“?
:::

### Graph Neural Networks

Etwas anderes: Anstatt die Struktur des Graphen in (Knoten, Kontext)-Paare zu entwickeln, lässt sich die Struktur des Graphen auch direkt im neuronalen Netz nutzen. Beispiel: Ein Graph mit Knoten Kaffee, Tee, Kanne, Tasse, Mühle. Jeder Knoten trägt einen Feature-Vektor, und in jeder Schicht des Netzes aktualisiert jeder Knoten seinen Vektor aus den Vektoren seiner Nachbarn – **Message Passing**:

$$
h_v^{(k+1)} = \tau\Bigl( W^{(k)} h_v^{(k)} + \sum_{u \in N(v)} U^{(k)} h_u^{(k)} \Bigr).
$$

Die Gewichte $W^{(k)}, U^{(k)}$ sind für alle Knoten gleich, sodass das Netz auf Graphen beliebiger Größe funktioniert. Das ist der Grundbaustein von GNNs; wir vertiefen das hier nicht.

<!-- TODO Abbildung: Message Passing auf dem Kaffee/Tee-Graphen (Folie 24) -->

## Recurrent Neural Networks

### RNNs

Input: ein linearer Strom von Daten, z.B. Text, Audio, Video oder andere Zeitreihen. Output: irgendeine vektorielle oder skalare Größe, z.B. die Vorhersage des nächsten Wortes. Idee: Zum Zeitpunkt $t$ nicht nur die neuen Daten $x_t$, sondern auch die Ergebnisse aus den Daten von $t - 1$ verwenden, um zum Ergebnis zu kommen. Ein rekurrentes Neuron hat einen **hidden state** $h_t$:

$$
h_t = \tau\bigl( W x_t + U h_{t-1} + b \bigr), \qquad y_t = V h_t .
$$

In der „entfalteten Perspektive“ (unrolled) ist ein RNN über $T$ Zeitschritte ein tiefes Netz mit $T$ Schichten, die sich alle dieselben Gewichte $W, U, V$ teilen. Backpropagation funktioniert dann ganz normal (*backpropagation through time*) – mit dem Problem, dass Gradienten über viele Zeitschritte hinweg exponentiell verschwinden oder explodieren, weil immer wieder mit $U$ multipliziert wird. Die Lösung dafür sind LSTMs.

<!-- TODO Abbildung: rekurrentes Neuron, gefaltet und entfaltet (Wikipedia, Fdeloche 2017, CC-BY-SA 4.0) -->

### Historie: Rekurrente Netze

1982 Hopfield-Netzwerk · 1985 Boltzmann Machine (Hinton, Sejnowski) · 1980er RNNs · 1991 Schmidhubers frühe Attention · 1990er Gated RNNs · 1997 LSTM (Hochreiter, Schmidhuber) · 2014 GRUs (Cho, Bengio et al.) · 2017 Transformer (Vaswani et al.).

Im Gegensatz zur *Finite Impulse Response* (FIR) eines CNNs (machen wir noch) ist ein RNN ein *Infinite Impulse Response* (IIR) Signalverarbeiter: Ein Eingabesignal zum Zeitpunkt $t$ kann den Zustand prinzipiell für immer beeinflussen.

### Trick: Skip Connections

Auch bekannt als *Residual Connections*. Anstatt $x^{(m)} = f_\vartheta(x^{(m-1)})$ (z.B. $f$ = MLP) parametrisiere

$$
x^{(m)} = x^{(m-1)} + \operatorname{res}(x^{(m-1)}), \qquad \operatorname{res}(x^{(m-1)}) = f_\vartheta(x^{(m-1)}).
$$

Idee: Jeder Layer ist nah dran an „nichts ändern“ (Identität), und der Gradient hat immer einen direkten Weg (den Term $x^{(m-1)}$) an der Schicht vorbei. Hilft gegen verschwindende oder explodierende Gradienten – in RNNs, in ResNets (daher der Name) und in Transformern.

### Gated RNNs

**GRU** (Gated Recurrent Unit): Der hidden state ist gleichzeitig der Output. Aus Input und altem hidden state wird ein *Kandidat* für den neuen hidden state berechnet, und zwei Gates (Sigmoide, also Werte in $(0, 1)$) steuern: Das *Reset Gate*, wie viel vom alten Zustand in den Kandidaten eingeht, und das *Update Gate*, wie stark der Zustand zum Kandidaten hin aktualisiert wird.

**LSTM** (Long Short-Term Memory): Zusätzlich zum hidden state $h_t$ (= Output, *short term memory*) gibt es einen **cell state** $c_t$ (*long term memory*), der nur durch Addition und komponentenweise Multiplikation verändert wird – eine Art Skip Connection durch die Zeit. Drei Gates (Sigmoide) steuern ihn: *forget* (was aus $c_{t-1}$ gelöscht wird), *input* (was neu hineingeschrieben wird), *output* (was davon in $h_t$ sichtbar wird). Mehr Erklärungen: Shi Yan @ MLReview, *Understanding LSTM and its diagrams*.

<!-- TODO Abbildungen: GRU (Wikipedia, Jeblad 2018) und LSTM (Wikipedia, Guillaume Chevalier 2018), beide CC-BY-SA 4.0 -->

Bill Gates (2018): „huge milestone in advancing artificial intelligence“ – weil OpenAI mit LSTMs Dota 2 gewann. Auch mit LSTMs gebaut: AlphaStar von Google DeepMind, spielt StarCraft 2 (2019).

### LSTM praktisch

Mit PyTorch:

```python
import torch.nn as nn

class MyModel(nn.Module):
    def __init__(self, embedding_length, hidden_size, output_size):
        super().__init__()
        self.lstm = nn.LSTM(embedding_length, hidden_size)
        self.label = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        h, (h_n, c_n) = self.lstm(x)
        return self.label(h)
```

`nn.LSTM` bekommt eine Sequenz von Vektoren (z.B. word2vec-Embeddings der Wörter) und liefert die Sequenz der hidden states; darauf ein linearer Layer für die Vorhersage.

### Am Rande: Konkatenieren vs. Summe

Wenn wir zwei verschiedene Eingabevektoren in einer Schicht verarbeiten wollen, ist es naheliegend, diese zu einem längeren Vektor zu konkatenieren. Oft sehen wir aber im Code stattdessen ein einfaches `+`. Wie kann das funktionieren???

Eine einfachere Frage: Unter welchen Umständen lässt sich für zwei Vektoren $v, w \in \mathbb{R}^n$ aus der Summe $v + w \in \mathbb{R}^n$ wieder das Paar $(v, w)$ rekonstruieren? Probieren Sie explizite Beispiele mit $n = 2$ aus, etwa $v = (3, 0)$ und $w = (1, 1)$. Überlegen Sie hinterher, wie das bei der eigentlichen Frage weiterhilft. (Stichwort: Wenn $v$ und $w$ aus komplementären Unterräumen kommen – oder das Netz lernen kann, sie dort hinzulegen –, verliert die Summe nichts.)

## Transformer

### Historie: BLEU (2001)

Um Übersetzungsmodelle zu vergleichen, braucht man ein Maß. Papineni et al. (2001): „Human evaluations of machine translation are extensive but expensive. […] We propose a method of automatic machine translation evaluation that is quick, inexpensive, and language-independent, that correlates highly with human evaluation.“ Die Grundidee: „The closer a machine translation is to a professional human translation, the better it is.“

Der **BLEU-Score** (bilingual evaluation understudy) zwischen 0 und 1 (auch skaliert 0–10 oder 0–100) ist das geometrische Mittel aus den $n$-Gramm-Präzisionsscores der Maschinenübersetzung relativ zu einer menschlichen Referenzübersetzung, multipliziert mit einem Strafterm für abweichende Übersetzungslänge (*brevity penalty*). Die $n$-Gramm-Präzision ist die Anzahl (mit Mehrfachzählung, aber gedeckelt durch die Referenz) der $n$-Gramme, die in der Maschinenübersetzung vorkommen und in der Referenzübersetzung, normiert mit der Anzahl der $n$-Gramme der Maschinenübersetzung. Für BLEU ist $n = 1, 2, 3, 4$ üblich.

### Historie: NeurIPS 2017

Vaswani et al., *Attention is all you need*: „The dominant sequence transduction models are based on complex recurrent or convolutional neural networks in an encoder-decoder configuration. The best performing models also connect the encoder and decoder through an attention mechanism. We propose a new simple network architecture, the Transformer, based solely on attention mechanisms, dispensing with recurrence and convolutions entirely. […] Our model achieves 28.4 BLEU on the WMT 2014 English-to-German translation task, improving over the existing best results, including ensembles by over 2 BLEU. […] a new single-model state-of-the-art BLEU score of 41.8 after training for 3.5 days on eight GPUs.“

Zur Einordnung: WMT = Workshop on Statistical Machine Translation, Task und Datensatz; aktuell WMT23 als Challenge; sacreBLEU als Standard-Implementierung; 41.8 „BLEU“ = 0,418 BLEU. Und das WMT19-Modell aus Kapitel 3 ist genau ein Nachfolger davon.

### Transformer technisch

Der Aufbau (Fig. 1 in „Attention is all you need“): ein **Encoder**-Stapel und ein **Decoder**-Stapel, beide aus identischen Blöcken mit Multi-Head Self-Attention, einem MLP, Residual Connections und Layer-Normalisierung. Anstelle von Rekurrenz bekommt jedes Token eine **Positionskodierung** addiert. Der Kern ist die **Attention**:

$$
\operatorname{Attention}(Q, K, V) = \operatorname{sm}\!\left( \frac{Q K^T}{\sqrt{d_k}} \right) V ,
$$

wobei Queries $Q$, Keys $K$ und Values $V$ lineare Projektionen der Token-Vektoren sind: Jedes Token „fragt“ mit seiner Query alle anderen Tokens, vergleicht sie mit deren Keys (Skalarprodukt, Softmax → Gewichte) und sammelt eine gewichtete Summe ihrer Values ein. Das ist eine Schicht, in der jedes Token von jedem anderen abhängt – ohne Reihenfolge, daher die Positionskodierung – und die vollständig parallel berechnet werden kann. Wir implementieren keine Transformer in dieser Vorlesung; in VL 11 benutzen wir sie.

<!-- TODO Abbildung: Transformer-Architektur (Fig. 1, Vaswani et al. 2017) -->

### Konkrete Modelle mit Transformern

**GPT** (Generative Pretrained Transformer): Trainiert unsupervised auf gigantischen Textmassen (präziser: self-supervised); BPE (Byte Pair Encoding) als Tokenization-Schema; sehr große Modelle (= sehr viele Layer, sehr viele Parameter); gelernte Positionskodierung, begrenzter Kontext; **Decoder-only**: das nächste Token vorhersagen. Varianten: GPT-2, GPT-J, GPT-NeoX, Llama 1/2/3, und nichtöffentlich GPT-3, 3.5, 4, etc.

**Byte Pair Encoding (BPE)**: ein Tokenization-Schema (Gage 1994). BPE baut auf einem Tokenizer auf, meist Token = Byte oder Character. Algorithmus:

1. Sortiere alle möglichen Tokenpaare nach Häufigkeit,
2. verschmelze die zwei häufigsten zu einem neuen Token,
3. Ende, wenn es genug verschiedene Token gibt.

Die Vokabulargröße bei GPT-4s BPE „tiktoken“ ist z.B. 100 256; durchschnittlich entspricht ein Token etwa 4 Bytes. Häufige Wörter werden zu einem Token, seltene in Silben oder Buchstaben zerlegt – das ist die „flexible $n$“-Antwort auf die Tokenisierungsfrage aus dem letzten Kapitel.

**NanoGPT**: Visualisierung und Erklärung, Layer für Layer, von Brendan Bycroft: [bbycroft.net/llm](https://bbycroft.net/llm).

**BERT** (Bidirectional Encoder Representations from Transformers): **Encoder-only** (nicht zwangsläufig generativ); Tokenization auf Subwort-Level (WordPiece); Training mit 2 Tasks: Masked Language Modeling (ähnlich wie bei word2vec, aber mit Kontext in beide Richtungen) und „nächsten Satz vorhersagen“. Bei gleicher Modellgröße besser als GPT für manche Tasks (Klassifikation, Embeddings). Varianten: RoBERTa, ALBERT, DistilBERT.

**ViT** (Vision Transformer, Dosovitskiy et al., „An Image is Worth 16x16 Words“): Das Bild wird grob gerastert in „Patches“ aufgeteilt; jeder Patch (= Token) wird in einen Vektor umgewandelt; Positionskodierung für 2D-Position statt 1D wie bei Text; ansonsten „klassischer“ Transformer. Für Klassifikationsaufgaben manchmal besser als CNNs.

### Implementierung des Transformers

Alexander Rush et al.: *The Annotated Transformer* (updated 2022 edition) – der Artikel „Attention is all you need“ zusammen mit Codeschnipseln und einigen Kommentaren. Für Verrückte oder sehr Interessierte: „I made a transformer by hand (no training!)“ von Theia Vogel, mit sorgfältig von Hand bestimmten Gewichten – die Fortsetzung unseres „Parameter von Hand wählen“ aus Kapitel 7.
