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
y = \tau(\zeta)
$$

für eine nichtlineare *Aktivierungsfunktion* $\tau \colon \mathbb{R} \to \mathbb{R}$. Bei McCulloch und Pitts ist $\tau$ eine Schwellenwertfunktion, die $0$ oder $1$ ausgibt; später wird $\tau$ die logistische Sigmoidfunktion $\sigma$ sein, oder ReLU. Diese Rollenverteilung gilt im ganzen Buch: $\tau$ ist eine beliebige Aktivierungsfunktion, $\sigma$ immer die logistische Sigmoidfunktion. Die Struktur „Skalarprodukt, gefolgt von einer nichtlinearen Funktion“ ist das Kochrezept, das uns durch die gesamte Vorlesung begleiten wird.

:::{figure} ../images/vl01-neuron.png
:width: 90%

Das McCulloch-Pitts-Neuron: gewichtete Summe der Eingaben, dann eine nichtlineare Aktivierungsfunktion.
:::

### Das Perzeptron

Rosenblatts Beitrag war weniger das Neuron als der *Lernalgorithmus* dafür. Das Perzeptron ist ein Modell zur **binären Klassifikation**: Input sind Stichproben von $(X, Y)$ mit $X \in \mathbb{R}^n$ und $Y \in \{0, 1\}$. Die Parameter des Modells sind ein Gewichtsvektor $w \in \mathbb{R}^n$ und ein Biasterm $b \in \mathbb{R}$. Die Inferenz ist

$$
f(x) = [\, w \cdot x + b > 0 \,],
$$

wobei $[\cdot]$ die Iverson-Klammer ist: $[A] = 1$, wenn die Aussage $A$ wahr ist, sonst $0$. Das Perzeptron ist also ein McCulloch-Pitts-Neuron mit der Schwellenwertfunktion $\tau(\zeta) = [\zeta + b > 0]$. Man beachte: $f$ ist eine *nichtlineare* Funktion, obwohl im Inneren nur ein Skalarprodukt steht.

Den Bias kann man loswerden, indem man ihn als nulltes Gewicht auffasst: Mit $w_0 := b$ und $x_0 := 1$ ist $w \cdot x + b = \sum_{j=0}^n w_j x_j$. Das ist ein Trick, den wir noch öfter sehen werden. Umgekehrt heißt das: Ein Perzeptron *ohne* Bias kann nur Hyperebenen durch den Ursprung lernen – zwei Klassen, die sich nur mit einer verschobenen Geraden trennen lassen, bleiben ihm verschlossen.

Geometrisch beschreibt die Gleichung $w \cdot x + b = 0$ eine Hyperebene $H$ in $\mathbb{R}^n$ (in $\mathbb{R}^2$: eine Gerade), und $f$ gibt an, auf welcher Seite von $H$ der Punkt $x$ liegt. Der Vektor $w$ steht senkrecht auf $H$: Für zwei Punkte $x, x' \in H$ ist

$$
w \cdot (x - x') = (w \cdot x + b) - (w \cdot x' + b) = 0 - 0 = 0,
$$

also ist $w$ orthogonal zu jeder Richtung *innerhalb* von $H$.

Mehr noch: Die Aktivierung $w \cdot x + b$ misst, *wie weit* $x$ von $H$ entfernt ist. Sei $\tilde{w} = w / \|w\|$ der normierte Normalenvektor. Jeder Punkt lässt sich zerlegen als $x = x_H + d\,\tilde{w}$ mit einem Punkt $x_H \in H$ (dem Lotfußpunkt) und einer Zahl $d \in \mathbb{R}$. Dann ist

$$
w \cdot x + b = (w \cdot x_H + b) + d\,(w \cdot \tilde{w}) = 0 + d\,\|w\|,
\qquad\text{also}\qquad
d = \frac{w \cdot x + b}{\|w\|}.
$$

Das ist der **vorzeichenbehaftete Abstand** von $x$ zur Hyperebene: positiv auf der Seite, in die $w$ zeigt, negativ auf der anderen, null auf $H$. Die Aktivierung eines Neurons ist nichts anderes als dieser Abstand, multipliziert mit $\|w\|$.

:::{prf:example} Abstand zur Trenngeraden
Sei $w = (3, 4)$ und $b = -5$, also $\|w\| = 5$ und $H = \{ x \in \mathbb{R}^2 : 3x_1 + 4x_2 = 5 \}$. Der Punkt $(1, \tfrac12)$ liegt auf $H$, denn $3 + 2 - 5 = 0$. Der Punkt $(3, 4)$ hat Aktivierung $9 + 16 - 5 = 20$ und damit Abstand $20/5 = 4$. Der Punkt $(-1, 0)$ hat Aktivierung $-3 - 5 = -8$ und Abstand $-8/5$: andere Seite.
:::

Daraus folgt eine Beobachtung, die uns bei der logistischen Regression wieder begegnen wird. Multipliziert man $w$ und $b$ mit derselben Zahl $c > 0$, so ändert sich weder $H$ noch die Entscheidung $[w \cdot x + b > 0]$, aber die Aktivierung wird um den Faktor $c$ skaliert. Die *Richtung* von $w$ legt fest, *was* klassifiziert wird; die *Länge* von $w$ legt fest, wie schnell die Aktivierung mit dem Abstand wächst. Für das Perzeptron ist die Länge egal. Sobald wir statt der Sprungfunktion eine glatte Aktivierungsfunktion verwenden, ist sie es nicht mehr: Für die logistische Sigmoidfunktion $\sigma$ ist $\sigma(c \cdot 20)$ bei $c = 10$ praktisch $1$, bei $c = 0{,}01$ nur knapp über $\tfrac12$. Dieselbe Trenngerade, ganz andere „Sicherheit“.

:::{prf:definition} Linear trennbar
Zwei Mengen $A, B \subseteq \mathbb{R}^n$ heißen *linear trennbar*, wenn es $w \in \mathbb{R}^n$ und $b \in \mathbb{R}$ gibt mit
$w \cdot a + b > 0$ für alle $a \in A$ und $w \cdot a' + b \le 0$ für alle $a' \in B$.
:::

Ein Perzeptron kann also genau die Klassifikationsprobleme lösen, bei denen die beiden Klassen linear trennbar sind – nicht mehr. Das berühmte Gegenbeispiel ist XOR: Die Punkte $(0,0)$ und $(1,1)$ lassen sich nicht durch eine Gerade von $(0,1)$ und $(1,0)$ trennen. Das ist die mathematische Substanz hinter dem AI Winter – und der Grund, warum wir mehrere Neuronen hintereinander schalten werden.

Wie das Perzeptron *trainiert* wird, also wie $w$ und $b$ aus den Daten bestimmt werden, ist Thema des [nächsten Kapitels](03-perzeptron-trainieren.md); auf einem Übungsblatt implementieren Sie es dann selbst.

## Was ist ein neuronales Netz?

Ein **Multilayer Perceptron** (MLP) entsteht, indem die Ausgaben von mehreren (verallgemeinerten) Perzeptrons als Eingabe für ein weiteres Perzeptron verwendet werden, welches also eine Schicht (Layer) weiter hinten ist.

:::{figure} ../images/vl01-mlp.png
:width: 90%

Ein Multilayer Perceptron mit 3 Eingaben, einer versteckten Schicht aus 4 Neuronen und einem Ausgabeneuron. Jeder Pfeil ist ein Gewicht.
:::

Formal: Eine Schicht mit $m$ Neuronen, die alle dieselben $n$ Eingaben bekommen, hat eine Gewichtsmatrix $W \in \mathbb{R}^{m \times n}$ und einen Biasvektor $b \in \mathbb{R}^m$ und berechnet

$$
h = \tau(W x + b),
$$

wobei $\tau$ komponentenweise angewendet wird.

Wie liest man $Wx$? Die $i$-te Komponente von $Wx$ ist das Skalarprodukt der $i$-ten *Zeile* von $W$ mit $x$. Die Zeilen von $W$ (in NumPy `W[i, :]`) sind also die Gewichtsvektoren der $m$ Neuronen, und $Wx + b$ berechnet $m$ Aktivierungen auf einmal, mit dem vorigen Abschnitt: $m$ skalierte Abstände zu $m$ Hyperebenen. Als Bild in $\mathbb{R}^2$: Jedes Neuron der ersten Schicht zeichnet eine Gerade in die Eingabeebene, und der Vektor $h$ sagt für jede dieser Geraden, auf welcher Seite $x$ liegt und wie weit weg. Das XOR-Beispiel unten ist genau das: zwei Geraden, dann eine Entscheidung im Raum der beiden Seiten-Informationen.

In PyTorch speichert `nn.Linear(n, m)` die Matrix als `weight` mit Shape `(m, n)`, eine Zeile pro Neuron, und `bias` mit Shape `(m,)`.

Ein Netz mit $L$ Schichten berechnet dann

$$
h^{(0)} = x, \qquad h^{(k)} = \tau^{(k)}\!\left(W^{(k)} h^{(k-1)} + b^{(k)}\right) \quad (k = 1, \dots, L), \qquad f(x) = h^{(L)}.
$$

Dabei können die Schichten verschieden groß sein, manche Einträge von $W^{(k)}$ können $0$ sein (fehlende Pfeile), es kann Pfeile rückwärts geben (rekurrente Netze), und es können viele verschiedene nichtlineare Funktionen vorkommen (ReLU, Convolution, Softmax, …). Die Gesamtheit der Einträge aller $W^{(k)}$ und $b^{(k)}$ sind die *Parameter* oder *Gewichte* des Netzes; bei modernen Modellen sind das Milliarden von Zahlen. „Deep“ heißt: $L$ ist groß.

Warum das hintereinanderschalten hilft, sehen wir am XOR-Problem: Mit zwei Perzeptrons in der ersten Schicht, die „$x_1 \lor x_2$“ und „$\lnot(x_1 \land x_2)$“ berechnen, und einem dritten Perzeptron, das deren Ausgaben mit UND verknüpft, ist XOR plötzlich linear trennbar – im Raum der Ausgaben der ersten Schicht.

## Übung

Sei $w = \binom{3}{4}$ und $b = -5$, also das Perzeptron $x \mapsto [w \cdot x + b > 0]$.

1. Berechnen Sie für $x_1 = \binom{4}{2}$, $x_2 = \binom{-1}{0}$ und $x_3 = \binom{3}{-1}$
   jeweils die Aktivierung $w \cdot x + b$ **und** den vorzeichenbehafteten Abstand zur Geraden.
   *Tipp: Der Abstand ist die Aktivierung geteilt durch $\|w\|$, und $\|w\| = 5$.*
2. Ersetzen Sie $w$ durch $10w$ und $b$ durch $10b$. Was ändert sich an der Geraden, was an
   den Aktivierungen, was an den Abständen?

*Antwortprobe: Genau eine der drei Größen ändert sich.*

:::{admonition} Weiterlesen
:class: seealso
Prince, *UDL*, Kap. 3 (Shallow neural networks); Deisenroth et al., *MML*, Kap. 3 (Analytic geometry: Skalarprodukt, Winkel, Projektion). Beide Bücher sind frei verfügbar, siehe [Über dieses Skript](../README.md).
:::
