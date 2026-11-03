---
title: "Hintergrundwissen Lineare Algebra"
description: "Vektoren, Skalarprodukt, Norm, Winkel, Orthogonalität und Matrizen: die lineare Algebra, auf der Neuronen, Schichten und Backpropagation aufbauen."
short_title: "Hintergrundwissen LA"
---

# Hintergrundwissen Lineare Algebra

Im Inneren eines Neurons steckt ein Skalarprodukt, in einer Schicht eine Matrix, in der
Backpropagation ein Matrixprodukt. Dieses Kapitel stellt die Begriffe bereit, auf denen
der Rest des Buchs aufbaut, und legt die Schreibweisen fest.

Ein Nachschlagekapitel, kein Lehrgang: Wer aus der linearen Algebra kommt, überfliegt es.
Die Eigenschaften, die unten ohne Beweis stehen, sind in zwei, drei Zeilen nachzurechnen.

## Vektoren

:::{prf:definition} Vektor
Ein reeller Vektor der Dimension $d \in \mathbb{N}$ ist ein Tupel von $d$ reellen Zahlen,
den *Komponenten* $v_i \in \mathbb{R}$, geschrieben als Spalte:

$$
v = \begin{pmatrix} v_1 \\ \vdots \\ v_d \end{pmatrix} \in \mathbb{R}^d .
$$

Es ist $v = w$, wenn $v_i = w_i$ für alle $i$ gilt.
:::

Das hochgestellte $\top$ ist das *Transponieren*: Es vertauscht Zeilen und Spalten, aus der
Spalte $v$ wird die Zeile $v^\top = (v_1, \dots, v_d)$. Die *Standardbasisvektoren*
$e_1, \dots, e_d$ haben eine $1$ in einer Komponente und sonst Nullen.

:::{admonition} Spalte, Zeile und was NumPy daraus macht
:class: note
`np.array([1.0, 2.0])` hat die Shape `(2,)` – weder Zeile noch Spalte, und `v.T` tut
nichts. Erst `v.reshape(2, 1)` ist die Spalte. Das ist der häufigste Grund dafür, dass
eine Rechnung auf dem Papier stimmt und im Code eine Shape zu viel hat; siehe
[Kapitel „Tensoren“](05-tensoren.md).
:::

## Hadamard-Produkt und Skalarprodukt

:::{prf:definition} Hadamard-Produkt
Das Hadamard-Produkt von $v, w \in \mathbb{R}^d$ ist der Vektor
$v \odot w \in \mathbb{R}^d$ mit $(v \odot w)_i := v_i w_i$, also die komponentenweise
Multiplikation.
:::

:::{prf:definition} Skalarprodukt
Das Skalarprodukt von $v, w \in \mathbb{R}^d$ ist die Zahl

$$
v \cdot w := \sum_{i=1}^d (v \odot w)_i = \sum_{i=1}^d v_i w_i \;\in\; \mathbb{R}.
$$
:::

Wie im [Kapitel „Was ist Deep Learning?“](01-was-ist-deep-learning.md) festgelegt, sind
$v \cdot w$ und $\langle v, w \rangle$ dasselbe; unten kommt mit $v^\top w$ eine dritte
Schreibweise dazu.

:::{prf:example} Skalarprodukt
Für $v = \binom{2}{0}$ und $w = \binom{1}{3}$ ist $v \odot w = \binom{2}{0}$ und
$v \cdot w = 2 \cdot 1 + 0 \cdot 3 = 2$. Mit den Standardbasisvektoren liest man
Komponenten aus: $e_1 \cdot \binom{x}{y} = x$.
:::

Drei Eigenschaften benutzt das Buch, ohne sie jedes Mal zu nennen. Das Skalarprodukt ist

* **symmetrisch**: $v \cdot w = w \cdot v$,
* **bilinear**: $(\lambda u + \mu v) \cdot w = \lambda (u \cdot w) + \mu (v \cdot w)$, und
  ebenso im zweiten Argument,
* **positiv definit**: $v \cdot v \geq 0$, mit $v \cdot v = 0$ nur für den Nullvektor.

Die Bilinearität trägt den Konvergenzbeweis im
[Kapitel „Das Perzeptron trainieren“](03-perzeptron-trainieren.md), die positive
Definitheit den nächsten Abschnitt.

## Länge und Normalisierung

:::{prf:definition} Länge
Die Länge ($2$-Norm) von $v \in \mathbb{R}^d$ ist
$\|v\| := \sqrt{v \cdot v} = \sqrt{v_1^2 + \dots + v_d^2}$.
:::

Dass unter der Wurzel nichts Negatives steht, ist die positive Definitheit; in
$\mathbb{R}^2$ ist es der Satz des Pythagoras. Es gilt $\|v\| = 0$ nur für den Nullvektor,
und $\|\lambda v\| = |\lambda| \, \|v\|$ – mit Betrag, denn eine Länge ist nie negativ.

:::{prf:example} Länge
$\left\| \binom{2}{0} \right\| = 2$ und
$\left\| \binom{3}{4} \right\| = \sqrt{9 + 16} = 5$. Standardbasisvektoren haben Länge $1$.
:::

:::{prf:definition} Normalisierung
Für $v \neq 0$ ist $\tilde{v} := v / \|v\|$ die Normalisierung von $v$; sie hat Länge $1$.
Vektoren der Länge $1$ heißen *Einheitsvektoren*.
:::

Damit zerfällt jeder Vektor in Richtung und Länge, $v = \|v\| \, \tilde{v}$, und mit ihm
das Skalarprodukt:

$$
v \cdot w = \|v\| \, \|w\| \; \bigl(\tilde{v} \cdot \tilde{w}\bigr).
$$

:::{figure} ../images/la-normalisierung.png
:width: 60%

Normalisieren schiebt jeden Vektor auf den Einheitskreis: $\tilde{v}$ und $\tilde{w}$
zeigen in dieselben Richtungen wie $v$ und $w$, der Winkel $\theta$ zwischen ihnen bleibt.
:::

Der zweite Faktor hängt nur von den Richtungen ab und bekommt im nächsten Abschnitt einen
Namen. Nebenbei: Aus $1 = v_1^2 + \dots + v_d^2$ folgt $-1 \leq v_i \leq 1$, normalisierte
Embeddings liefern also gutmütige Zahlen.

:::{admonition} Obacht: Wurzeln kosten, Nullen stören
:class: warning
Zum Vergleichen zweier Längen braucht man keine Wurzel: $\|v\| < \|w\|$ gilt genau dann,
wenn $v \cdot v < w \cdot w$. Und `v / np.linalg.norm(v)` ist für $v = 0$ eine Division
durch null – in echten Daten kommt der Nullvektor häufiger vor, als man denkt.
:::

## Winkel

:::{prf:definition} Winkel
Für $v, w \neq 0$ ist der Winkel $\theta \in [0, \pi]$ zwischen ihnen festgelegt durch

$$
\cos \theta = \frac{v \cdot w}{\|v\| \, \|w\|} = \tilde{v} \cdot \tilde{w}.
$$
:::

Mit $w = e_1$ wird die Definition zur Schulgeometrie. Der Nullpunkt, der Punkt $v$ und
sein Lotfußpunkt $v_1 e_1$ auf der $x$-Achse bilden ein rechtwinkliges Dreieck. Seine
Hypotenuse ist $v$ selbst, mit Länge $\|v\|$. Die Ankathete an $\theta$ liegt auf der
$x$-Achse und hat (für spitzes $\theta$) die Länge $v_1$. Also ist

$$
\cos \theta = \frac{\text{Ankathete}}{\text{Hypotenuse}} = \frac{v_1}{\|v\|}
= \frac{v \cdot e_1}{\|v\| \, \|e_1\|},
$$

genau die Definition oben. Für Einheitsvektoren ist der Nenner $1$, und
$\cos \theta = v \cdot e_1 = v_1$ ist die $x$-Koordinate des Punktes $v$ auf dem
Einheitskreis; in der Ebene ist $\sin \theta = v_2$ die Länge der Gegenkathete.

:::{figure} ../images/la-einheitskreis.png
:width: 50%

Für einen Einheitsvektor $v$ hat die Hypotenuse die Länge $1$, und $\cos \theta = v \cdot e_1$
ist die Länge der Ankathete: die erste Komponente von $v$, die Strecke, die $v$ auf die
$x$-Achse wirft.
:::

Dass der Bruch zwischen $-1$ und $1$ liegt, also überhaupt ein Kosinus sein kann, ist die
Ungleichung von Cauchy und Schwarz: $|v \cdot w| \leq \|v\| \, \|w\|$.

:::{prf:example} Winkel
Für $v = \binom{2}{0}$ und $w = \binom{1}{3}$ ist $v \cdot w = 2$, $\|v\| = 2$ und
$\|w\| = \sqrt{10} \approx 3{,}162$, also $\cos \theta = 1/\sqrt{10} \approx 0{,}316$ und
$\theta \approx 71{,}6^\circ$.
:::

Ist nur einer der beiden Vektoren normalisiert, bleibt eine Länge übrig:
$v \cdot \tilde{w} = \|v\| \cos \theta$. Das ist die *Projektion* von $v$ auf die Richtung
von $w$, die Länge des Schattens, den $v$ auf die Gerade durch $w$ wirft – mit
Vorzeichen, negativ, sobald der Winkel stumpf ist. Dass ein Schatten nie länger ist als der
Vektor selbst, ist die Ungleichung von Cauchy und Schwarz im Bild.

:::{figure} ../images/la-projektion.png
:width: 90%

Das Skalarprodukt mit einem Einheitsvektor ist eine Schattenlänge mit Vorzeichen. Links
ist $\theta$ spitz, rechts stumpf.
:::

Der Kosinus misst Ähnlichkeit der *Richtungen*, unabhängig von den Längen. Als
**Kosinusähnlichkeit** ist er das Standardmaß für Embeddings, etwa im
[Kapitel „word2vec“](../part-representation-learning/16-word2vec.md) und im
[Kapitel „Latente Räume“](../part-architekturen-anwendungen/23-latente-raeume.md).

## Orthogonalität

:::{prf:definition} Orthogonalität
$v, w \in \mathbb{R}^d$ heißen orthogonal, geschrieben $v \perp w$, wenn $v \cdot w = 0$ ist.
:::

Für Vektoren ungleich null ist das der Fall $\cos \theta = 0$, also ein rechter Winkel;
die Standardbasisvektoren sind paarweise orthogonal. Daran hängt die Geometrie des
Neurons: Der Gewichtsvektor steht senkrecht auf der Trennebene, und die Aktivierung misst
den Abstand zu ihr. Ausgerechnet wird das im
[Kapitel „Neuron und Perzeptron“](02-neuron-perzeptron.md).

Ohne Bias geht die Trennebene durch den Nullpunkt: Alle $x$ mit $w \cdot x = 0$ stehen
senkrecht auf $w$, und das Vorzeichen von $w \cdot x$ sagt, auf welcher Seite ein Punkt
liegt.

:::{figure} ../images/la-halbebenen.png
:width: 50%

Die Gerade $w \cdot x = 0$ steht senkrecht auf $w$ und teilt die Ebene in zwei Hälften.
Auf der Seite, in die $w$ zeigt, ist $w \cdot x > 0$, auf der anderen negativ.
:::

## Matrizen

:::{prf:definition} Matrix
Eine reelle Matrix mit $m$ Zeilen und $n$ Spalten ist ein Schema
$A = (a_{ij}) \in \mathbb{R}^{m \times n}$ mit Einträgen $a_{ij} \in \mathbb{R}$; der
erste Index zählt die Zeilen, der zweite die Spalten. Ein Vektor aus $\mathbb{R}^d$ ist
der Spezialfall $\mathbb{R}^{d \times 1}$.
:::

Die Angabe $m \times n$ heißt im Code *Shape*. Sie mitzuführen ist die halbe Miete: Die
meisten Fehler beim Rechnen mit Netzen sind Shape-Fehler.

:::{prf:definition} Matrix mal Vektor
Für $A \in \mathbb{R}^{m \times n}$ und $x \in \mathbb{R}^n$ ist $Ax \in \mathbb{R}^m$ mit
$(Ax)_i = \sum_{j=1}^n a_{ij} x_j$: Die $i$-te Komponente ist das Skalarprodukt der
$i$-ten *Zeile* von $A$ mit $x$.
:::

:::{prf:example} Matrix mal Vektor
$A = \begin{pmatrix} 1 & 2 & 0 \\ 0 & 1 & 3 \end{pmatrix} \in \mathbb{R}^{2 \times 3}$ und
$x = (2, 1, 4)^\top$ ergeben
$Ax = \binom{2 + 2 + 0}{0 + 1 + 12} = \binom{4}{13} \in \mathbb{R}^2$.
:::

So liest man eine Schicht: In $Wx + b$ mit $W \in \mathbb{R}^{m \times n}$ steht in jeder
Zeile der Gewichtsvektor eines Neurons, und $Wx + b$ berechnet $m$ Aktivierungen auf
einmal. Eine Matrix *ist* eine lineare Abbildung $\mathbb{R}^n \to \mathbb{R}^m$.

Welche, liest man an den Spalten ab: $Ae_j$ ist die $j$-te Spalte von $A$. Weil jedes
$x = x_1 e_1 + \dots + x_n e_n$ ist, legen die Bilder der Standardbasisvektoren schon
alles fest, $Ax = x_1 \, Ae_1 + \dots + x_n \, Ae_n$.

:::{figure} ../images/la-lineare-abbildung.png
:width: 90%

Was eine $2 \times 2$-Matrix mit dem Gitter macht: Das Einheitsquadrat geht auf das
Parallelogramm aus den Spalten $Ae_1$ und $Ae_2$. Eine Drehung (Mitte) erhält rechte
Winkel und Flächen, eine allgemeine Matrix (rechts) nicht.
:::

:::{prf:definition} Matrix mal Matrix
Für $A \in \mathbb{R}^{m \times n}$ und $B \in \mathbb{R}^{n \times k}$ ist
$AB \in \mathbb{R}^{m \times k}$ mit $(AB)_{i\ell} = \sum_{j=1}^n a_{ij} b_{j\ell}$.
:::

Die Shape-Regel steht in der Definition: $(m \times n) \cdot (n \times k)$ ergibt
$m \times k$, die inneren Zahlen müssen übereinstimmen und fallen weg. Passen sie nicht,
ist das Produkt nicht definiert; $AB$ und $BA$ sind verschieden, oft ist nur eines von
beiden definiert. Inhaltlich ist das Produkt die **Verkettung** der Abbildungen: erst $B$,
dann $A$. Daran hängt die Backpropagation, denn die Ableitung einer Verkettung ist das
Produkt der Ableitungen
([Kapitel „Gradientenabstieg“](../part-lernen/08-gradientenabstieg.md)).

:::{prf:definition} Transponieren
Die Transponierte von $A \in \mathbb{R}^{m \times n}$ ist
$A^\top \in \mathbb{R}^{n \times m}$ mit $(A^\top)_{ij} = a_{ji}$: Zeilen werden Spalten.
:::

Drei Regeln, die das Buch braucht: $(A^\top)^\top = A$; $(AB)^\top = B^\top A^\top$, die
Reihenfolge dreht sich also um; und $v \cdot w = v^\top w$, denn eine Zeile mal eine
Spalte ist eine $1 \times 1$-Matrix. Die zweite Regel ist der Grund, warum in der
Backpropagation ständig transponierte Gewichtsmatrizen auftauchen: vorwärts $W$, rückwärts
$W^\top$.

:::{prf:example} Produkt und Transponierte
Mit $A$ wie oben und
$B = \begin{pmatrix} 1 & 0 \\ 2 & 1 \\ 1 & 3 \end{pmatrix} \in \mathbb{R}^{3 \times 2}$ ist

$$
AB = \begin{pmatrix} 5 & 2 \\ 5 & 10 \end{pmatrix} \in \mathbb{R}^{2 \times 2},
\qquad
(AB)^\top = \begin{pmatrix} 5 & 5 \\ 2 & 10 \end{pmatrix} = B^\top A^\top .
$$

$BA$ ist ebenfalls definiert, aber $3 \times 3$ – schon die Shape zeigt, dass die
Reihenfolge zählt.
:::

:::{admonition} Zeilen statt Spalten: die Konvention im Code
:class: note
Auf dem Papier ist ein Datenpunkt eine Spalte, und eine Schicht rechnet $Wx$. In NumPy und
PyTorch liegt ein Batch als Matrix der Shape `(N, n)` vor, ein Datenpunkt je *Zeile*, und
dieselbe Schicht rechnet `X @ W.T + b`. Beide Konventionen beschreiben dasselbe;
transponiert ist genau der Unterschied. Wer eine Formel aus dem Buch in Code übersetzt und
eine Shape-Fehlermeldung bekommt, hat meist diesen Wechsel vor sich und keinen
Rechenfehler.
:::

## Orthogonale Matrizen

:::{prf:definition} Orthogonale Matrix
Eine Matrix $A \in \mathbb{R}^{d \times d}$ heißt orthogonal, wenn $A^\top A = I$ ist;
dabei ist $I$ die Einheitsmatrix mit Einsen auf der Diagonale und Nullen sonst.
:::

Der Eintrag $(A^\top A)_{ij}$ ist das Skalarprodukt der $i$-ten mit der $j$-ten Spalte von
$A$. Orthogonal heißt also: Die Spalten haben Länge $1$ und stehen paarweise senkrecht
aufeinander. $A^\top$ macht $A$ rückgängig, $A^\top (Ax) = x$. In der Ebene sind das genau
die Drehungen um den Nullpunkt und die Spiegelungen an Geraden durch ihn.

Orthogonale Matrizen ändern kein Skalarprodukt. Mit $v \cdot w = v^\top w$ und
$(Av)^\top = v^\top A^\top$ ist

$$
v \cdot w = v^\top w = v^\top A^\top A \, w = (Av)^\top (Aw) = (Av) \cdot (Aw),
$$

und mit dem Skalarprodukt bleiben Längen und Winkel erhalten. Beim Rechnen mit zwei
Vektoren darf man deshalb annehmen, dass einer von ihnen auf der positiven $x$-Achse
liegt.

:::{figure} ../images/la-drehung.png
:width: 80%

Eine Drehung $A$ bringt $v$ auf die positive $x$-Achse. Der Winkel $\theta$ zwischen den
beiden Vektoren bleibt derselbe, und mit ihm das Skalarprodukt.
:::

:::{anywidget} ../widgets/drehung.mjs
{v: [1.6, 1.9], w: [-1.2, 1.5]}
:::

:::{prf:example} Eine Ebene im Raum flachlegen
Die Vektoren $v = (1, 2, 2)^\top$ und $w = (5, 4, -2)^\top$ spannen eine Ebene im
$\mathbb{R}^3$ auf. Gesucht ist eine orthogonale Matrix, die diese Ebene auf die
$x$-$y$-Ebene $\{z = 0\}$ dreht. Ihre Zeilen sind

* $u_1 = v / \|v\| = \tfrac{1}{3} (1, 2, 2)^\top$;
* $u_2$: von $w$ den Anteil in Richtung $u_1$ abziehen und normalisieren,
  $w - (w \cdot u_1) \, u_1 = (5, 4, -2)^\top - (1, 2, 2)^\top = (4, 2, -4)^\top$, also
  $u_2 = \tfrac{1}{3} (2, 1, -2)^\top$;
* $n = \tfrac{1}{3} (-2, 2, -1)^\top$, senkrecht auf $u_1$ und $u_2$ und damit auf der
  ganzen Ebene.

Das ergibt

$$
A = \frac{1}{3} \begin{pmatrix} 1 & 2 & 2 \\ 2 & 1 & -2 \\ -2 & 2 & -1 \end{pmatrix},
\qquad
Av = \begin{pmatrix} 3 \\ 0 \\ 0 \end{pmatrix},
\qquad
Aw = \begin{pmatrix} 3 \\ 6 \\ 0 \end{pmatrix},
$$

und $A^\top A = I$ rechnet man nach. Die dritte Komponente von $Av$ und $Aw$ ist
$n \cdot v = n \cdot w = 0$, die Bilder liegen also in $\{z = 0\}$. Die Probe:
$v \cdot w = 5 + 8 - 4 = 9$ und $(Av) \cdot (Aw) = 3 \cdot 3 + 0 \cdot 6 + 0 \cdot 0 = 9$;
ebenso $\|v\| = 3 = \|Av\|$ und $\|w\| = \sqrt{45} = \|Aw\|$. Den Winkel liest man jetzt
in der Ebene ab: $\cos \theta = 9 / (3 \sqrt{45}) = 1/\sqrt{5}$, also
$\theta \approx 63{,}4^\circ$.
:::

:::{figure} ../images/la-ebene-r3.png
:width: 100%

Das Beispiel im Bild: $v$ und $w$ spannen eine schräge Ebene auf, $n$ steht senkrecht auf
ihr. $A$ dreht die Ebene in die $x$-$y$-Ebene und $n$ auf $e_3$; danach lässt sich alles
flach zeichnen.
:::

Für Embeddings heißt das: Dreht man alle Embeddings mit derselben orthogonalen Matrix,
ändern sich weder Längen noch Kosinusähnlichkeiten. Ein Verfahren, das nur Skalarprodukte
von Embeddings benutzt – das [Kapitel „word2vec“](../part-representation-learning/16-word2vec.md)
beschreibt eines –, ist invariant unter solchen Transformationen.

:::{admonition} Weiterlesen
:class: seealso
Deisenroth et al., [*MML*](https://mml-book.github.io/), Kap. 2 (Linear algebra) und Kap. 3 (Analytic geometry:
Skalarprodukt, Winkel, Projektion). Frei verfügbar, siehe
[Über dieses Skript](../README.md).
:::
