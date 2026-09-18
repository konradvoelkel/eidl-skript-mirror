---
title: "Neuron und Perzeptron"
short_title: "Neuron und Perzeptron"
---

# Neuron und Perzeptron

## Das Neuron und das Perzeptron

### Das McCulloch-Pitts-Neuron

Das Modell von 1943 ist von der Biologie inspiriert: Ein Neuron bekommt über Dendriten Signale $x_1, \dots, x_n$ von anderen Neuronen, summiert sie gewichtet auf und „feuert“, wenn die Summe eine Schwelle überschreitet. Als Formel: Mit Gewichten $w_1, \dots, w_n \in \mathbb{R}$ ist die *Aktivierung*

$$
\zeta = \sum_{j=1}^n w_j x_j = w \cdot x
$$

und die Ausgabe

$$
y = \sigma(\zeta)
$$

für eine nichtlineare *Aktivierungsfunktion* $\sigma \colon \mathbb{R} \to \mathbb{R}$. Bei McCulloch und Pitts ist $\sigma$ eine Schwellenwertfunktion, die $0$ oder $1$ ausgibt; später wird $\sigma$ die logistische Sigmoidfunktion oder ReLU sein. Die Struktur „Skalarprodukt, gefolgt von einer nichtlinearen Funktion“ ist das Kochrezept, das uns durch die gesamte Vorlesung begleiten wird.

:::{figure} ../images/vl01-neuron.png
:width: 90%

Das McCulloch-Pitts-Neuron: gewichtete Summe der Eingaben, dann eine nichtlineare Aktivierungsfunktion.
:::

### Das Perzeptron

Rosenblatts Beitrag war weniger das Neuron als der *Lernalgorithmus* dafür. Das Perzeptron ist ein Modell zur **binären Klassifikation**: Input sind Stichproben von $(X, Y)$ mit $X \in \mathbb{R}^n$ und $Y \in \{0, 1\}$. Die Parameter des Modells sind ein Gewichtsvektor $w \in \mathbb{R}^n$ und ein Biasterm $b \in \mathbb{R}$. Die Inferenz ist

$$
f(x) = [\, w \cdot x + b > 0 \,],
$$

wobei $[\cdot]$ die Iverson-Klammer ist: $[A] = 1$, wenn die Aussage $A$ wahr ist, sonst $0$. Das Perzeptron ist also ein McCulloch-Pitts-Neuron mit der Schwellenwertfunktion $\sigma(\zeta) = [\zeta + b > 0]$. Man beachte: $f$ ist eine *nichtlineare* Funktion, obwohl im Inneren nur ein Skalarprodukt steht.

Den Bias kann man loswerden, indem man ihn als nulltes Gewicht auffasst: Mit $w_0 := b$ und $x_0 := 1$ ist $w \cdot x + b = \sum_{j=0}^n w_j x_j$. Das ist ein Trick, den wir noch öfter sehen werden. Umgekehrt heißt das: Ein Perzeptron *ohne* Bias kann nur Hyperebenen durch den Ursprung lernen – zwei Klassen, die sich nur mit einer verschobenen Geraden trennen lassen, bleiben ihm verschlossen.

Geometrisch beschreibt die Gleichung $w \cdot x + b = 0$ eine Hyperebene in $\mathbb{R}^n$ (in $\mathbb{R}^2$: eine Gerade), und $f$ gibt an, auf welcher Seite der Hyperebene $x$ liegt. Der Vektor $w$ steht senkrecht auf dieser Hyperebene.

:::{prf:definition} Linear trennbar
Zwei Mengen $A, B \subseteq \mathbb{R}^n$ heißen *linear trennbar*, wenn es $w \in \mathbb{R}^n$ und $b \in \mathbb{R}$ gibt mit
$w \cdot a + b > 0$ für alle $a \in A$ und $w \cdot c + b \le 0$ für alle $c \in B$.
:::

Ein Perzeptron kann also genau die Klassifikationsprobleme lösen, bei denen die beiden Klassen linear trennbar sind – nicht mehr. Das berühmte Gegenbeispiel ist XOR: Die Punkte $(0,0)$ und $(1,1)$ lassen sich nicht durch eine Gerade von $(0,1)$ und $(1,0)$ trennen. Das ist die mathematische Substanz hinter dem AI Winter – und der Grund, warum wir mehrere Neuronen hintereinander schalten werden.

Wie das Perzeptron *trainiert* wird, also wie $w$ und $b$ aus den Daten bestimmt werden, ist Thema des [nächsten Kapitels](03-perzeptron-trainieren.md) und von Übungsblatt 2.

## Was ist ein neuronales Netz?

Ein **Multilayer Perceptron** (MLP) entsteht, indem die Ausgaben von mehreren (verallgemeinerten) Perzeptrons als Eingabe für ein weiteres Perzeptron verwendet werden, welches also eine Schicht (Layer) weiter hinten ist.

:::{figure} ../images/vl01-mlp.png
:width: 90%

Ein Multilayer Perceptron mit 3 Eingaben, einer versteckten Schicht aus 4 Neuronen und einem Ausgabeneuron. Jeder Pfeil ist ein Gewicht.
:::

Formal: Eine Schicht mit $m$ Neuronen, die alle dieselben $n$ Eingaben bekommen, hat eine Gewichtsmatrix $W \in \mathbb{R}^{m \times n}$ und einen Biasvektor $b \in \mathbb{R}^m$ und berechnet

$$
h = \sigma(W x + b),
$$

wobei $\sigma$ komponentenweise angewendet wird. Ein Netz mit $L$ Schichten berechnet dann

$$
h^{(0)} = x, \qquad h^{(k)} = \sigma^{(k)}\!\left(W^{(k)} h^{(k-1)} + b^{(k)}\right) \quad (k = 1, \dots, L), \qquad f(x) = h^{(L)}.
$$

Dabei können die Schichten verschieden groß sein, manche Einträge von $W^{(k)}$ können $0$ sein (fehlende Pfeile), es kann Pfeile rückwärts geben (rekurrente Netze), und es können viele verschiedene nichtlineare Funktionen vorkommen (ReLU, Convolution, Softmax, …). Die Gesamtheit der Einträge aller $W^{(k)}$ und $b^{(k)}$ sind die *Parameter* oder *Gewichte* des Netzes; bei modernen Modellen sind das Milliarden von Zahlen. „Deep“ heißt: $L$ ist groß.

Warum das hintereinanderschalten hilft, sehen wir am XOR-Problem: Mit zwei Perzeptrons in der ersten Schicht, die „$x_1 \lor x_2$“ und „$\lnot(x_1 \land x_2)$“ berechnen, und einem dritten Perzeptron, das deren Ausgaben mit UND verknüpft, ist XOR plötzlich linear trennbar – im Raum der Ausgaben der ersten Schicht.

## Tipps zu Übungsblatt 1

Das erste Blatt wiederholt lineare Algebra: Skalarprodukt, Orthogonalität, Länge und Winkel, und setzt das in NumPy und Matplotlib um. Erinnern Sie sich an die Interpretation des Kosinus eines Winkels als Verhältnis von Seiten im rechtwinkligen Dreieck: Mit Ankathete $a$ und Hypotenuse $b$ ist

$$
\cos(\alpha) = \frac{a}{b}.
$$

Was passiert im Spezialfall $b = 1$? Dann ist $\cos(\alpha) = a$, d.h. der Kosinus ist die Länge der Projektion eines Einheitsvektors auf die Richtung des anderen Schenkels. Genau das steckt in der Formel

$$
\cos(\alpha) = \frac{u \cdot v}{\|u\| \, \|v\|}
$$

für den Winkel zwischen zwei Vektoren $u, v \in \mathbb{R}^n$: Das Skalarprodukt $w \cdot x$ im Perzeptron misst, „wie sehr $x$ in Richtung $w$ zeigt“.
