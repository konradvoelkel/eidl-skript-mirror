---
title: "Aktivierungsfunktionen"
short_title: "Aktivierungsfunktionen"
---

# Aktivierungsfunktionen

## Aktivierungsfunktionen und weitere Layer

Ein Neuron „forward“ ist $\tau\langle w, x \rangle$. Beim Perzeptron ist $\tau = \operatorname{sign}$, bei der logistischen Regression $\tau = \sigma$. Allgemein ist $\tau$ beliebig – aber differenzierbar, sonst funktioniert Backpropagation nicht.

### Neues Ziel: Funktionen lernen

Bisher war das Ziel Klassifikation. Neues Ziel: Das neuronale Netz soll eine Funktion lernen (Regression), und unser Modell von der Funktion ist *stückweise linear*. Welches $\tau$ ist dafür geeignet?

:::{prf:definition} ReLU
Die *Rectified Linear Unit* ist

$$
\operatorname{ReLU}(y) := \max(0, y).
$$

Ein Neuron mit $\tau = \operatorname{ReLU}$ heißt ReLU-Neuron.
:::

**Ableitung** von $\max(0, y)$ nach $y$: Für $y > 0$ ist $\max(0, y) = y$, also ist die Ableitung $1$. Für $y < 0$ ist $\max(0, y) = 0$, also ist die Ableitung $0$. Für $y = 0$ ist die Ableitung nicht definiert – wir *definieren* sie als $0$, das spart Rechnungen. (Dass das erlaubt ist, steckt im Begriff der *schwachen Ableitung*: Sie darf an einzelnen Punkten beliebig sein.)

**Wieso ist ReLU geeignet?** Lineare Abbildung + ReLU ist die Projektion auf einen Halbraum, denn ReLU ist genau die Projektion von $\mathbb{R}$ auf $[0, \infty)$, und ein Halbraum ist eine Seite einer Hyperebene. Ein ReLU-Neuron $\max(0, \langle w, x \rangle + b)$ ist also null auf der einen Seite der Hyperebene $\langle w, x \rangle + b = 0$ und linear ansteigend auf der anderen. Summiert man mehrere solche „Knickfunktionen“ mit Gewichten, bekommt man stückweise lineare Funktionen, deren Knickstellen auf den Hyperebenen liegen – und mit genug Neuronen kann man damit jede stetige Funktion beliebig gut approximieren. Beispiel an der Tafel; im [Kapitel „Netze von Hand bauen“](12-netze-von-hand.md) bauen wir so $x^2$.

:::{figure} ../images/vl06-relu-sum.png
:width: 90%

Links die ReLU, rechts eine gewichtete Summe von drei verschobenen ReLUs: eine stückweise lineare Funktion mit Knicken an den Verschiebungen.
:::

### Layer, nochmal

Mehrere Neuronen, die parallel verarbeitet werden, bilden eine Schicht. Ein **Linear Layer** ist eine Matrix (Zeilen = Gewichtsvektoren) plus Bias. Ein **ReLU Layer** ist eine Schicht, in der jedes Neuron die Aktivierungsfunktion ReLU nutzt, also Linear Layer + komponentenweises ReLU. In PyTorch: `nn.Sequential(nn.Linear(n, m), nn.ReLU())`.

### Problem bei ReLU: sterbende Neuronen

Wenn ein Neuron immer $0$ liefert, weil die Eingabe immer negativ ist, „fließt“ keine Information mehr durch das Neuron während der Backpropagation – die Ableitung ist $0$, also ist $\delta$ für dieses Neuron $0$, also ändern sich seine Gewichte nie wieder. Das Neuron ist tot. Zwei Lösungen:

**Lösung 1**: Statt $\tau = \max(0, y)$ verwende $\tau(y) = f(y)[y < 0] + g(y)[y \ge 0]$ mit passenden $f, g$, sodass auch für $y < 0$ die Ableitung nicht null ist. Mit $f(y) := \alpha(e^y - 1)$ und $g(y) := y$ heißt $\tau$ **ELU** (Exponential Linear Unit); mit $f(y) := 0{,}01\,y$ heißt es Leaky ReLU.

**Lösung 2**: Statt $\max(0, y)$ verwende ein glattes $\tau$, sodass für $y \to -\infty$ gilt $\tau(y) \to 0$ und für $y \to +\infty$ gilt $\tau(y) \to +\infty$, aber ohne harten Knick:

$$
\tau(y) := y\,\sigma(y) \quad \text{(Swish, auch SiLU)}, \qquad
\tau(y) := y\,\Phi(y) \quad \text{(GELU, Gaussian Error Linear Unit)},
$$

wobei $\Phi$ die Verteilungsfunktion der Standardnormalverteilung ist. Beide sind im negativen Bereich nicht strikt null, sondern haben eine kleine Delle unter der Achse, und die Ableitung verschwindet nur asymptotisch. GELU ist heute die Standardwahl in Transformern.

Welche Aktivierungsfunktionen in der Praxis genutzt wurden, listete [paperswithcode.com/methods/category/activation-functions](https://paperswithcode.com/methods/category/activation-functions) (inzwischen nur noch im Internet Archive).

:::{figure} ../images/vl06-activations.png
:width: 90%

Aktivierungsfunktionen im Vergleich. ELU, Swish und GELU sind im negativen Bereich nicht konstant null.
:::

## Übung

Ein Neuron $x \mapsto \mathrm{ReLU}(w \cdot x + b)$ mit $w = (-1, -1)$ und $b = -3$ sieht
nur Trainingsdaten mit nichtnegativen Einträgen.

1. Zeigen Sie: Die Ausgabe ist für **alle** diese Daten $0$.
2. Welchen Wert hat der Gradient nach $w$ und $b$ dann? Was folgt daraus für das Training?

*Antwortprobe: Bei (2) ist die Antwort für $w$ und $b$ dieselbe.*

:::{admonition} Weiterlesen
:class: seealso
Prince, *UDL*, Abschnitt 3.2 (Activation functions) und Kap. 7 (Initialization, sterbende Neuronen). Beide Bücher sind frei verfügbar, siehe [Über dieses Skript](../README.md).
:::
