---
title: "Recurrent Neural Networks"
description: "Recurrent Neural Networks für Text und Zeitreihen: verborgener Zustand, verschwindende Gradienten, Skip Connections, LSTM und GRU, LSTM in PyTorch."
short_title: "RNNs"
---

# Recurrent Neural Networks

## RNNs

Input: ein linearer Strom von Daten, z.B. Text, Audio, Video oder andere Zeitreihen. Output: irgendeine vektorielle oder skalare Größe, z.B. die Vorhersage des nächsten Wortes. Idee: Zum Zeitpunkt $t$ nicht nur die neuen Daten $x_t$, sondern auch die Ergebnisse aus den Daten von $t - 1$ verwenden, um zum Ergebnis zu kommen. Ein rekurrentes Neuron hat einen **hidden state** $h_t$:

$$
h_t = \tau\bigl( W x_t + U h_{t-1} + b \bigr), \qquad y_t = V h_t .
$$

In der „entfalteten Perspektive“ (unrolled) ist ein RNN über $T$ Zeitschritte ein tiefes Netz mit $T$ Schichten, die sich alle dieselben Gewichte $W, U, V$ teilen. Backpropagation funktioniert dann ganz normal (*backpropagation through time*) – mit dem Problem, dass Gradienten über viele Zeitschritte hinweg exponentiell verschwinden oder explodieren, weil immer wieder mit $U$ multipliziert wird. Die Lösung dafür sind LSTMs.

:::{figure} ../images/vl09-rnn-unrolled.png
:width: 90%

Ein rekurrentes Neuron: gefaltet mit der Rückkopplung $U$ (links) und über vier Zeitschritte entfaltet (rechts) – ein tiefes Netz mit geteilten Gewichten.
:::

## Historie: Rekurrente Netze

1982 [Hopfield-Netzwerk](https://hdl.handle.net/10.1073/pnas.79.8.2554) · 1985 [Boltzmann Machine](https://hdl.handle.net/10.1207/s15516709cog0901_7) (Ackley, Hinton, Sejnowski) · 1980er RNNs · 1991 Schmidhubers frühe Attention · 1990er Gated RNNs · 1997 [LSTM](https://hdl.handle.net/10.1162/neco.1997.9.8.1735) (Hochreiter, Schmidhuber) · 2014 [GRUs](https://arxiv.org/abs/1406.1078) (Cho, Bengio et al.) · 2017 [Transformer](https://arxiv.org/abs/1706.03762) (Vaswani et al.).

Im Gegensatz zur *Finite Impulse Response* (FIR) eines CNNs (machen wir noch) ist ein RNN ein *Infinite Impulse Response* (IIR) Signalverarbeiter: Ein Eingabesignal zum Zeitpunkt $t$ kann den Zustand prinzipiell für immer beeinflussen.

## Trick: Skip Connections

Auch bekannt als *Residual Connections*. Anstatt $x^{(m)} = f_\vartheta(x^{(m-1)})$ (z.B. $f$ = MLP) parametrisiere

$$
x^{(m)} = x^{(m-1)} + \operatorname{res}(x^{(m-1)}), \qquad \operatorname{res}(x^{(m-1)}) = f_\vartheta(x^{(m-1)}).
$$

Idee: Jeder Layer ist nah dran an „nichts ändern“ (Identität), und der Gradient hat immer einen direkten Weg (den Term $x^{(m-1)}$) an der Schicht vorbei. Hilft gegen verschwindende oder explodierende Gradienten – in RNNs, in ResNets (daher der Name) und in Transformern.

## Gated RNNs

**GRU** (Gated Recurrent Unit): Der hidden state ist gleichzeitig der Output. Aus Input und altem hidden state wird ein *Kandidat* für den neuen hidden state berechnet, und zwei Gates (Sigmoide, also Werte in $(0, 1)$) steuern: Das *Reset Gate*, wie viel vom alten Zustand in den Kandidaten eingeht, und das *Update Gate*, wie stark der Zustand zum Kandidaten hin aktualisiert wird.

**LSTM** (Long Short-Term Memory): Zusätzlich zum hidden state $h_t$ (= Output, *short term memory*) gibt es einen **cell state** $c_t$ (*long term memory*), der nur durch Addition und komponentenweise Multiplikation verändert wird – eine Art Skip Connection durch die Zeit. Drei Gates (Sigmoide) steuern ihn: *forget* (was aus $c_{t-1}$ gelöscht wird), *input* (was neu hineingeschrieben wird), *output* (was davon in $h_t$ sichtbar wird). Mehr Erklärungen: Shi Yan @ MLReview, *Understanding LSTM and its diagrams*.

Schaltbilder der Zellen: [LSTM](https://de.wikipedia.org/wiki/Long_short-term_memory) und [GRU](https://en.wikipedia.org/wiki/Gated_recurrent_unit) auf Wikipedia (Abbildungen CC-BY-SA); die Gates sind dort als $\sigma$-Knoten gezeichnet, die elementweise multiplizieren, also genau die stetigen Bitmasken aus dem [Kapitel „Netze von Hand bauen“](../part-lernen/12-netze-von-hand.md).

Bill Gates (2018, auf Twitter): „huge milestone in advancing artificial intelligence“ – weil [OpenAI Five](https://openai.com/index/openai-five/) mit LSTMs Dota 2 gewann. Auch mit LSTMs gebaut: [AlphaStar](https://hdl.handle.net/10.1038/s41586-019-1724-z) von Google DeepMind, spielt StarCraft 2 (2019).

## LSTM praktisch

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

`nn.LSTM` bekommt eine Sequenz von Vektoren (z.B. word2vec-Embeddings der Wörter) und liefert die Sequenz der hidden states; darauf ein linearer Layer für die Vorhersage. **Achtung bei den Achsen:** Anders als sonst in PyTorch erwartet `nn.LSTM` voreingestellt `(seq, batch, feature)`, der Batch liegt also auf der *zweiten* Achse (siehe [Kapitel „Tensoren“](../part-grundlagen/05-tensoren.md)). Mit `batch_first=True` im Konstruktor gilt wieder die gewohnte Reihenfolge.

## Am Rande: Konkatenieren vs. Summe

Wenn wir zwei verschiedene Eingabevektoren in einer Schicht verarbeiten wollen, ist es naheliegend, diese zu einem längeren Vektor zu konkatenieren. Oft sehen wir aber im Code stattdessen ein einfaches `+`. Wie kann das funktionieren???

Eine einfachere Frage: Unter welchen Umständen lässt sich für zwei Vektoren $v, w \in \mathbb{R}^n$ aus der Summe $v + w \in \mathbb{R}^n$ wieder das Paar $(v, w)$ rekonstruieren? Probieren Sie explizite Beispiele mit $n = 2$ aus, etwa $v = (3, 0)$ und $w = (1, 1)$. Überlegen Sie hinterher, wie das bei der eigentlichen Frage weiterhilft. (Stichwort: Wenn $v$ und $w$ aus komplementären Unterräumen kommen – oder das Netz lernen kann, sie dort hinzulegen –, verliert die Summe nichts.)

## Übung

Ein RNN mit $h_t = \tanh(w\,x_t + u\,h_{t-1})$, $w = 1$, $u = 0{,}5$, $h_0 = 0$ und der
Eingabefolge $x = (1, 0, 0)$.

1. Berechnen Sie $h_1, h_2, h_3$ (zwei Nachkommastellen genügen).
2. Wiederholen Sie mit $u = 0{,}1$ und mit $u = 0{,}9$. Wie lange „erinnert“ sich das Netz
   jeweils an die 1 vom Anfang?
   *Tipp: Nach dem ersten Schritt ist die Eingabe 0, es bleibt also eine Multiplikation
   mit $u$ pro Schritt.*

*Antwortprobe: Bei (2) fällt einer der drei Verläufe deutlich langsamer ab als die anderen.*

:::{admonition} Weiterlesen
:class: seealso
**Im Kapitel zitiert:**

* Hopfield: [*Neural networks and physical systems with emergent collective computational abilities*](https://hdl.handle.net/10.1073/pnas.79.8.2554), PNAS 1982.
* Ackley, Hinton, Sejnowski: [*A Learning Algorithm for Boltzmann Machines*](https://hdl.handle.net/10.1207/s15516709cog0901_7), Cognitive Science 1985.
* Hochreiter, Schmidhuber: [*Long Short-Term Memory*](https://hdl.handle.net/10.1162/neco.1997.9.8.1735), Neural Computation 1997.
* Cho et al.: [*Learning Phrase Representations using RNN Encoder-Decoder for Statistical Machine Translation*](https://arxiv.org/abs/1406.1078), EMNLP 2014.
* Vaswani et al.: [*Attention Is All You Need*](https://arxiv.org/abs/1706.03762), NeurIPS 2017.
* OpenAI: [*OpenAI Five*](https://openai.com/index/openai-five/), Blog 2018.
* Vinyals et al.: [*Grandmaster level in StarCraft II using multi-agent reinforcement learning*](https://hdl.handle.net/10.1038/s41586-019-1724-z), Nature 2019.

**Zum Ansehen:**

* StatQuest: [*Long Short-Term Memory (LSTM), Clearly Explained*](https://www.youtube.com/watch?v=YCzL96nL7j0), 21 Minuten, 2022 (englisch) – die Gates, die oben nur benannt sind, einzeln durchgerechnet.
:::
