---
title: "Netze von Hand bauen"
short_title: "Netze von Hand"
---

# Netze von Hand bauen

## Das Geheimnis um Deep Learning lüften

Warum – und wie genau – funktioniert Deep Learning so gut? Die Zutaten, die wir bisher haben:

* Das einzelne Neuron = Skalarprodukt + Aktivierungsfunktion.
* Gradientenabstieg: Lernen in Richtung der Ableitung einer Loss-Funktion.
* Backpropagation: clever die Ableitung berechnen für tiefe Netze.

Was noch fehlt, und was wir in diesem und den nächsten Kapiteln angehen:

* Sinnvolle Loss-Funktionen festlegen: Regression mit MSE, (binäre) Klassifikation mit (B)CE; BCE vs. NLL vs. $D_{KL}$.
* Architekturen neben einfachen MLPs, wie z.B. Autoencoder – und damit auch Representation Learning und Transfer Learning ([Kapitel „Autoencoder“](../part-representation-learning/14-autoencoder.md) und folgende).
* Regularisierung und Tricks gegen verschwindende Gradienten ([Kapitel „Aktivierungsfunktionen“](11-aktivierungsfunktionen.md), Dropout und Batch-Normalisierung im Autoencoder-Kapitel).
* Hyperparameter wählen und optimieren; alles hängt von den Daten ab …
* Und ganz grundsätzlich: Elementare Funktionen sind leicht approximierbar – das jetzt, zuerst von Hand (dieses Kapitel), dann als Satz ([Kapitel „Universelle Approximation“](13-universelle-approximation.md)).

## Parameter von Hand wählen

Bevor wir Netze trainieren, überzeugen wir uns davon, dass die gesuchten Gewichte überhaupt *existieren*: Wir bauen kleine Netze von Hand.

### Easy mode: Boolesche Variablen

Seien $x, y \in \{0, 1\} = \{\text{FALSE}, \text{TRUE}\}$ und $f \colon \mathbb{R}^2 \to \mathbb{R}$, $f(x, y) := x \text{ OR } y$, also $f(0,0) = 0$, $f(1,0) = 1$, $f(0,1) = 1$, $f(1,1) = 1$. Welches neuronale Netz berechnet als Inferenz die Funktion $f$?

Idee: Schreibe $f$ als Verkettung von gewichteten Summen (= Skalarprodukten) und Aktivierungsfunktionen (z.B. $[x > 0]$ oder $\operatorname{ReLU}(x) := \max(0, x)$). Dabei müssen wir OR *interpolieren* – entscheiden, was z.B. $f(0{,}5, 0)$ sein soll – und *extrapolieren* – entscheiden, was z.B. $f(-1, 2)$ sein soll. Denn ein neuronales Netz ist auf ganz $\mathbb{R}^2$ definiert, nicht nur auf den vier Ecken.

### Easiest mode: eindimensional

Sei $x \in \mathbb{R}$ mit der Interpretation $(x \le 0) = \text{FALSE}$, $(x \ge 1) = \text{TRUE}$, und $n \colon \mathbb{R} \to \mathbb{R}$, $n(x) := \text{NOT } x$. Also $n(0) = 1$, $n(1) = 0$, allgemeiner $n(x) \le 0$ falls $x \ge 1$. Die Funktion

$$
n(x) = 1 - x
$$

erfüllt die Eigenschaft, NOT zu inter- und extrapolieren. Als neuronales Netz: 1 Neuron, Gewicht $w = -1$, Bias $b = +1$, Aktivierungsfunktion $\operatorname{id}$.

### Zurück zu OR

Ansatz: $f(x, y) = x + y$. Leider ist $f(1, 1) = 2 \neq 1$. Besser: $f(x, y) = [x + y > 0]$ – ein Neuron mit Gewichtsvektor $(1, 1)$, Bias $b = 0$ und Aktivierungsfunktion $[\,\cdot > 0]$ mit Werten in $\{0, 1\}$. Dafür ändern wir die Interpretation leicht zu $(x \le 0) = \text{F}$, $(x > 0) = \text{T}$. Softere Varianten sind $f(x, y) := x + y$ oder $\sigma(x + y)$; und noch besser, weil es Negatives sauber abschneidet:

$$
f(x, y) := \operatorname{ReLU}(x) + \operatorname{ReLU}(y).
$$

:::{figure} ../images/vl07-or-nor-heatmap.png
:width: 90%

OR und NOR als Funktionen auf ganz $\mathbb{R}^2$: Die vier Booleschen Ecken sind markiert, die schwarze Linie ist die Nullstellenmenge.
:::

### Komplizierteres aus Einfachem: NOR

Sei $g(x, y) := x \text{ NOR } y$, also $g(\text{F}, \text{F}) = \text{T}$ und sonst $\text{F}$. NOR = NOT OR, also $g(x, y) = n(f(x, y))$ für ein $f$, welches OR implementiert. Mit $f(x, y) := \operatorname{ReLU}(x) + \operatorname{ReLU}(y)$ und $n(x) := 1 - x$:

$$
g(x, y) := 1 - \bigl(\operatorname{ReLU}(x) + \operatorname{ReLU}(y)\bigr).
$$

Als Netz: erste Schicht mit Gewichten $(1, 1)$, Bias $0$ und ReLU (zwei Neuronen, eines pro Eingabe – oder eines mit Gewichtsvektor $(1,1)$, wenn man die ReLU vor die Summe zieht), zweite Schicht mit Gewicht $-1$, Bias $1$ und $\operatorname{id}$.

### Weiter so? XOR

Sei $f(x, y) := x \text{ XOR } y$. Die „Region“ XOR in der Ebene, also die Punkte $(x, y)$ mit $\text{XOR}(x, y) > 0$, ist der Schnitt von $\text{NAND}(x, y) > 0$ mit $\text{OR}(x, y) > 0$:

$$
\text{XOR}(x, y) = \text{AND}\bigl(\text{NAND}(x, y),\ \text{OR}(x, y)\bigr).
$$

Setzt man das mit den obigen Bausteinen zusammen, so müsste es mit 4 Hidden Layers zu je 4 Neuronen klappen. Gradientenabstieg mit Backpropagation findet allerdings auch Approximationen mit 3 Hidden Layers – und mit 2 Hidden Layers (siehe die Bilder `krude-xor-approximation.png` aus dem TensorFlow Playground).

:::{figure}
:width: 90%

![](../images/vl07-xor-region.png)
![](../images/vl07-xor-playground-3hidden.png)
![](../images/vl07-xor-playground-2hidden.png)

Oben: XOR als Schnitt von NAND und OR. Unten: Vom Gradientenabstieg gefundene Approximationen im TensorFlow Playground mit 3 bzw. 2 versteckten Schichten.
:::

### Take-Home Message

Boolesche Funktionen lassen sich mit neuronalen Netzen darstellen bzw. approximieren, d.h. es gibt Gewichte, sodass die resultierende Funktion tut, was sie soll. Also kann auch Optimierung diese idealen Gewichte finden. Aus elementaren Funktionen lassen sich komplexe verknüpfen; neuronale Netze können aber auch „Abkürzungen“ nehmen und Platz verschwenden (überflüssige Neuronen).

### Arithmetik

Wie können wir z.B. $f(x, y) := x^3 + x y^2 - 3y$ mit einem neuronalen Netz berechnen oder approximieren? Einfachere Probleme, die wir dafür zuerst lösen müssen: $f(x, y) := xy$ und $f(x) := x^2$.

**Auf $[-3, +3]$ approximieren wir $x^2$** mit einer stückweise linearen Funktion an ganzzahligen Stützstellen. Die Interpolation durch die Punkte $(k, k^2)$ für $k = -3, \dots, 3$ hat auf $[k, k+1]$ die Steigung $2k + 1$, also an jeder inneren Stützstelle einen Knick, bei dem die Steigung um $2$ wächst – und jeder Knick ist eine ReLU:

$$
Q(x) = 9 - 5\,\operatorname{ReLU}(x + 3) + \sum_{k=-2}^{2} 2\,\operatorname{ReLU}(x - k).
$$

Probe: $Q(0) = 9 - 15 + 2(2 + 1) = 0$ und $Q(3) = 9 - 30 + 2(5 + 4 + 3 + 2 + 1) = 9$. Das ist ein Netz mit einer versteckten Schicht aus 6 ReLU-Neuronen (Gewicht $1$, Bias $-k$ für $k = -3, \dots, 2$) und einer linearen Ausgabeschicht mit Gewichten $(-5, 2, 2, 2, 2, 2)$ und Bias $9$. Die Symmetrie $x^2 = (-x)^2$ haben wir dabei ignoriert – geht das besser? Der Betrag ist selbst ein kleines Netz, $|x| = \operatorname{ReLU}(x) + \operatorname{ReLU}(-x)$ (zwei Neuronen mit Gewichten $1$ und $-1$, dann ein Neuron mit Gewichtsvektor $(1, 1)$), und damit reicht die Interpolation auf $[0, 3]$:

$$
P(x) = |x| + 2\operatorname{ReLU}(|x| - 1) + 2\operatorname{ReLU}(|x| - 2).
$$

Das sind nur noch 3 Neuronen in der Interpolationsschicht – dafür ist das Netz tiefer, weil $|x|$ zwei Schichten vorweg kostet. Weniger Neuronen pro Schicht gegen mehr Schichten: ein Tausch, den wir noch öfter sehen werden.

In der Praxis könnte man PyTorch auch direkt bitten, $x^2$ oder $xy$ *exakt* zu berechnen (Stichwort *Gates*, etwa in LSTMs), auch wenn man damit das reine MLP verlässt. Der Haken: Im Allgemeinen weiß man vorher nicht, ob man $x^2$ braucht, um die gesuchte Funktion gut zu approximieren.

:::{figure} ../images/vl07-square-interpolation.png
:width: 90%

$x^2$ auf $[-3, 3]$ und die stückweise lineare Interpolation $Q(x)$ an ganzzahligen Stützstellen, ein Netz mit 6 ReLU-Neuronen.
:::

**Wenn $x^2$ gut approximiert werden kann, dann auch $xy$** über die Polarisationsidentität:

$$
\frac{(x + y)^2 - (x - y)^2}{4} = \frac{x^2 + 2xy + y^2 - x^2 + 2xy - y^2}{4} = xy .
$$

Damit setzen wir für eine Approximation $Q$ der Quadratfunktion

$$
\operatorname{MUL}(x, y) := \tfrac14 Q(x + y) - \tfrac14 Q(x - y),
$$

und $x + y$ sowie $x - y$ sind lineare Schichten. Mit MUL und Addition bekommen wir alle Polynome, und damit (Weierstraß) alle stetigen Funktionen auf beschränkten Bereichen.

### Take-Home Message

Funktionen lassen sich mit neuronalen Netzen darstellen bzw. approximieren. Mit einer Lookup-Table (LUT) und Interpolation sind beliebig gute Näherungen auf *beschränkten* Definitionsbereichen möglich – so rechnet auch die GPU z.B. den Sinus aus. Außerhalb der Stützstellen wird die Approximation beliebig schlecht: **Neuronale Netze interpolieren gut, extrapolieren schlecht.**
