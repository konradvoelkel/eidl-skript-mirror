---
title: "Autograd und Berechnungsgraph"
short_title: "Autograd"
---

# Autograd und Berechnungsgraph

Im [Kapitel „Backpropagation“](08-backpropagation.md) haben wir Gradienten von Hand rückwärts durch ein Netz gerechnet. PyTorch tut genau dasselbe – automatisch, für beliebige Architekturen, und mit demselben Muster: Zwischenergebnisse im Vorwärtsdurchlauf speichern, Kettenregel im Rückwärtsdurchlauf. Dieses Kapitel schaut hinter die Kulissen von `loss.backward()`.

## Ein Beispiel im Kleinen

Ein Blick darauf, wie PyTorch Backpropagation *tatsächlich* macht (`VL_11_backprop.ipynb`). Wir bauen ein sehr kleines „Netzwerk“:

```python
x = torch.tensor(3.0)                       # Input (Konstante)
w = torch.tensor(2.0, requires_grad=True)   # Gewicht: "Beobachte mich!"
b = torch.tensor(1.0, requires_grad=True)   # Bias
z = w * x     # z = 6
y = z + b     # y = 7
L = y ** 2    # Loss = 49
```

Der **Berechnungsgraph** (ein DAG, directed acyclic graph) entsteht erst beim Ausführen: Jeder Tensor, der aus einer Operation mit einem `requires_grad`-Tensor entstanden ist, trägt eine `grad_fn` (`L.grad_fn` ist `PowBackward0`, davor `AddBackward0`, davor `MulBackward0` und `AccumulateGrad` für die Blätter $w$ und $b$). Die `grad_fn` weiß, wie man die Operation ableitet, und hält Referenzen auf die *saved tensors*, die gespeicherten Zwischenergebnisse – genau die $z_k$ aus dem [Kapitel „Backpropagation“](08-backpropagation.md).

`L.backward()` ist der rekursive Aufruf der Kettenregel, initial mit $\frac{dL}{dL} = 1$:

$$
\frac{dL}{dw} = \frac{dL}{dy} \cdot \frac{dy}{dz} \cdot \frac{dz}{dw} = 2y \cdot 1 \cdot x = 14 \cdot 3 = 42,
\qquad
\frac{dL}{db} = 2y \cdot 1 = 14.
$$

Danach steht das Ergebnis in `w.grad` und `b.grad`. Der Optimizer-Schritt muss unter `torch.no_grad()` passieren, damit der Update selbst nicht Teil des Graphen wird, und die Gradienten müssen danach mit `zero_()` zurückgesetzt werden – sonst *akkumuliert* PyTorch sie beim nächsten `backward()`. Das ist der Grund für `optimizer.zero_grad()` in jeder Trainingsschleife.

**Freezing**: Setzt man `w.requires_grad = False`, so hat `z = w * x` keine `grad_fn` mehr, der Graph ist an dieser Stelle abgeschnitten, und ein Optimizer verändert $w$ nicht mehr, $b$ aber schon. So friert man beim Transfer Learning Schichten eines vortrainierten Modells ein – und spart dabei Speicher, weil für eingefrorene Parameter keine Gradienten gehalten werden.

**Convolution Backprop**: Wie funktioniert Backprop, wenn Gewichte geteilt werden wie bei einem Faltungslayer? Der Kernel `[0.5]` wird über den Input `[1, 2, 3]` geschoben, $o_i = x_i \cdot k$, und der Loss ist $o_1 + o_2 + o_3$. Der Gradient nach $k$ ist die *Summe* der Beiträge aller Positionen, $\frac{dL}{dk} = x_1 + x_2 + x_3 = 6$: Ein geteilter Parameter bekommt die Gradienten aller seiner Verwendungen aufsummiert – im Graphen führen mehrere Kanten zu demselben Blatt.

:::{prf:example} Backpropagation durch Faltung und ReLU von Hand
Ein Neuron führt eine 1D-Faltung gefolgt von ReLU aus: Eingabesignal $x = [2, 0, -1, 4]$, Kernel $k = [k_0, k_1] = [1, -1]$, Bias $b = 0$, „valid“ ohne Padding, Stride 1. Die Pre-Aktivierung an Position $i$ ist $z_i = x_i k_0 + x_{i+1} k_1 + b$, die Ausgabe $a_i = \operatorname{ReLU}(z_i)$.

*Forward:* $z = [2 \cdot 1 + 0 \cdot (-1),\ 0 + (-1)(-1),\ -1 + 4 \cdot (-1)] = [2, 1, -5]$, also $a = [2, 1, 0]$.

*Loss:* $L = \tfrac12 \sum_i (a_i - t_i)^2$ mit Target $t = [1, 2, 0]$, also $\frac{\partial L}{\partial a} = a - t = [1, -1, 0]$.

*Backward nach $k_0$:* Die ReLU-Maske ist $[z_i > 0] = [1, 1, 0]$; nur die Positionen $0$ und $1$ leiten den Gradienten weiter. Da $k_0$ an jeder Position mit $x_i$ multipliziert wird, ist $\frac{\partial z_i}{\partial k_0} = x_i$, und die Beiträge summieren sich:

$$
\frac{\partial L}{\partial k_0} = \sum_i (a_i - t_i)\,[z_i > 0]\,x_i = 1 \cdot 1 \cdot 2 + (-1) \cdot 1 \cdot 0 + 0 = 2 .
$$

*Update* mit Lernrate $\rho = 0{,}1$: $k_0 \leftarrow 1 - 0{,}1 \cdot 2 = 0{,}8$. Analog $\frac{\partial L}{\partial k_1} = 1 \cdot 0 + (-1)(-1) + 0 = 1$.
:::
