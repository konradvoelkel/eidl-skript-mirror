---
title: "Recurrent Neural Networks"
short_title: "RNNs"
---

# Recurrent Neural Networks

## Recurrent Neural Networks

### RNNs

Input: ein linearer Strom von Daten, z.B. Text, Audio, Video oder andere Zeitreihen. Output: irgendeine vektorielle oder skalare Größe, z.B. die Vorhersage des nächsten Wortes. Idee: Zum Zeitpunkt $t$ nicht nur die neuen Daten $x_t$, sondern auch die Ergebnisse aus den Daten von $t - 1$ verwenden, um zum Ergebnis zu kommen. Ein rekurrentes Neuron hat einen **hidden state** $h_t$:

$$
h_t = \tau\bigl( W x_t + U h_{t-1} + b \bigr), \qquad y_t = V h_t .
$$

In der „entfalteten Perspektive“ (unrolled) ist ein RNN über $T$ Zeitschritte ein tiefes Netz mit $T$ Schichten, die sich alle dieselben Gewichte $W, U, V$ teilen. Backpropagation funktioniert dann ganz normal (*backpropagation through time*) – mit dem Problem, dass Gradienten über viele Zeitschritte hinweg exponentiell verschwinden oder explodieren, weil immer wieder mit $U$ multipliziert wird. Die Lösung dafür sind LSTMs.

:::{figure} ../images/vl09-rnn-unrolled.png
:width: 90%

Ein rekurrentes Neuron: gefaltet mit der Rückkopplung $U$ (links) und über vier Zeitschritte entfaltet (rechts) – ein tiefes Netz mit geteilten Gewichten.
:::

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

Schaltbilder der Zellen: [LSTM](https://de.wikipedia.org/wiki/Long_short-term_memory) und [GRU](https://en.wikipedia.org/wiki/Gated_recurrent_unit) auf Wikipedia (Abbildungen CC-BY-SA); die Gates sind dort als $\sigma$-Knoten gezeichnet, die elementweise multiplizieren, also genau die stetigen Bitmasken aus dem [Kapitel „Netze von Hand bauen“](../part-lernen/12-netze-von-hand.md).

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

## Übung

Ein RNN mit $h_t = \tanh(w\,x_t + u\,h_{t-1})$, $w = 1$, $u = 0{,}5$, $h_0 = 0$ und der
Eingabefolge $x = (1, 0, 0)$.

1. Berechnen Sie $h_1, h_2, h_3$ (zwei Nachkommastellen genügen).
2. Wiederholen Sie mit $u = 0{,}1$ und mit $u = 0{,}9$. Wie lange „erinnert“ sich das Netz
   jeweils an die 1 vom Anfang?
   *Tipp: Nach dem ersten Schritt ist die Eingabe 0, es bleibt also eine Multiplikation
   mit $u$ pro Schritt.*

*Antwortprobe: Bei (2) fällt einer der drei Verläufe deutlich langsamer ab als die anderen.*
