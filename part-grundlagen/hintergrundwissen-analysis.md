---
title: "Hintergrundwissen Analysis"
short_title: "Hintergrundwissen Analysis"
---

# Hintergrundwissen Analysis

Training heißt ableiten: Der Gradient sagt, wohin ein Schritt gehen soll, und die
Kettenregel verteilt ihn über die Schichten. Dieses Kapitel stellt die Begriffe bereit,
die dafür gebraucht werden, von der partiellen Ableitung bis zur Jacobi-Matrix, und
erklärt, was man tut, wenn eine Funktion einen Knick hat.

Wie das [Kapitel zur linearen Algebra](hintergrundwissen-lineare-algebra.md) ein
Nachschlagekapitel. Wie der Gradient *benutzt* wird, steht im
[Kapitel „Gradientenabstieg“](../part-lernen/08-gradientenabstieg.md); hier steht, was er
ist.

## Partielle Ableitung

:::{prf:definition} Partielle Ableitung
Sei $f \colon \mathbb{R}^n \to \mathbb{R}$ und $a \in \mathbb{R}^n$. Die partielle
Ableitung von $f$ nach der $j$-ten Variablen an der Stelle $a$ ist

$$
\frac{\partial f}{\partial x_j}(a) := \lim_{h \to 0} \frac{f(a + h\,e_j) - f(a)}{h},
$$

sofern der Grenzwert existiert. Man hält also alle Komponenten bis auf die $j$-te fest und
leitet die verbleibende Funktion einer Variablen ganz gewöhnlich ab.
:::

:::{prf:example} Partielle Ableitungen
Für $f(x_1, x_2) = x_1^2 + 3 x_1 x_2$ ist
$\frac{\partial f}{\partial x_1} = 2x_1 + 3x_2$ und
$\frac{\partial f}{\partial x_2} = 3x_1$. An der Stelle $a = (1, 2)^\top$ sind das $8$
und $3$.
:::

## Richtungsableitung und Gradient

Die partiellen Ableitungen messen die Änderung entlang der Koordinatenachsen. Eine
beliebige Richtung geht genauso.

:::{prf:definition} Richtungsableitung
Für einen Einheitsvektor $u \in \mathbb{R}^n$ ist die Richtungsableitung von $f$ in
Richtung $u$ an der Stelle $a$

$$
D_u f(a) := \lim_{h \to 0} \frac{f(a + h u) - f(a)}{h} .
$$

Für $u = e_j$ ist das die $j$-te partielle Ableitung.
:::

:::{prf:definition} Gradient
Der Gradient von $f \colon \mathbb{R}^n \to \mathbb{R}$ an der Stelle $a$ ist der Vektor
der partiellen Ableitungen,

$$
\nabla f(a) := \left( \frac{\partial f}{\partial x_1}(a), \dots,
\frac{\partial f}{\partial x_n}(a) \right)^\top \in \mathbb{R}^n .
$$
:::

Beide Begriffe hängen zusammen: Ist $f$ differenzierbar, so gilt
$D_u f(a) = \nabla f(a) \cdot u$ – bewiesen unten im Abschnitt „Die Kettenregel“, sobald
der dafür nötige Ableitungsbegriff da ist. Die Richtungsableitung ist also ein
Skalarprodukt, und
damit ist sofort klar, welche Richtung die steilste ist. Nach Cauchy-Schwarz ist
$|D_u f(a)| \leq \|\nabla f(a)\|$, mit Gleichheit genau für
$u = \nabla f(a) / \|\nabla f(a)\|$:

> Der Gradient zeigt in die Richtung des steilsten Anstiegs, und seine Länge ist die
> Steigung in dieser Richtung.

Das ist die Rechtfertigung für den Gradientenabstieg: Wer absteigen will, geht entgegen
dem Gradienten.

:::{prf:example} Steilste Richtung
Für $f$ wie oben ist $\nabla f(1, 2) = (8, 3)^\top$. In Richtung $e_1$ steigt $f$ mit
$8$, in Richtung $e_2$ mit $3$, am steilsten in Richtung
$(8, 3)^\top / \sqrt{73}$ mit der Steigung $\sqrt{73} \approx 8{,}544$.
:::

## Die Ableitung als beste lineare Näherung

Für Funktionen zwischen Vektorräumen ist die Ableitung keine Zahl mehr, sondern eine
lineare Abbildung, also eine Matrix.

:::{prf:definition} Ableitung und Jacobi-Matrix
$g \colon \mathbb{R}^n \to \mathbb{R}^m$ heißt differenzierbar in $a$, wenn es eine
lineare Abbildung $(Dg)(a) \colon \mathbb{R}^n \to \mathbb{R}^m$ gibt mit

$$
g(a + h) = g(a) + (Dg)(a)\,h + r(h), \qquad
\frac{\|r(h)\|}{\|h\|} \longrightarrow 0 \text{ für } h \to 0 .
$$

Die zugehörige Matrix heißt Jacobi-Matrix; ihre Einträge sind die partiellen Ableitungen
der Komponentenfunktionen,

$$
\bigl((Dg)(a)\bigr)_{ij} = \frac{\partial g_i}{\partial x_j}(a)
\qquad (i = 1, \dots, m,\; j = 1, \dots, n),
$$

sie hat also $m$ Zeilen und $n$ Spalten.
:::

Der Rest $r$ verschwindet schneller als $h$ selbst: Die Jacobi-Matrix ist die *beste*
lineare Näherung an $g$ in der Nähe von $a$. Für $m = 1$ ist sie die Zeile
$\nabla f(a)^\top$ – Gradient und Ableitung sind dieselbe Information, einmal als Spalte
und einmal als Zeile geschrieben.

:::{prf:example} Jacobi-Matrix
Für $g(x_1, x_2) = (x_1 x_2,\; x_1 + x_2^2)^\top$ ist

$$
(Dg)(x) = \begin{pmatrix} x_2 & x_1 \\ 1 & 2x_2 \end{pmatrix},
\qquad
(Dg)(1, 2) = \begin{pmatrix} 2 & 1 \\ 1 & 4 \end{pmatrix}.
$$
:::

## Die Kettenregel

In dieser Sprache ist die Kettenregel ein Matrixprodukt.

:::{prf:theorem} Kettenregel
Sei $g \colon \mathbb{R}^n \to \mathbb{R}^m$ differenzierbar in $a$ und
$f \colon \mathbb{R}^m \to \mathbb{R}^k$ differenzierbar in $g(a)$. Dann ist $f \circ g$
differenzierbar in $a$, und

$$
D(f \circ g)(a) = (Df)\bigl(g(a)\bigr) \cdot (Dg)(a) .
$$

Die Ableitung einer Verkettung ist das Produkt der Ableitungen, ausgewertet an den
richtigen Stellen. Die Formate passen: $(Df)(g(a))$ ist $k \times m$, $(Dg)(a)$ ist
$m \times n$, das Produkt $k \times n$.
:::

Für $n = m = k = 1$ sind alle drei Matrizen Zahlen, und übrig bleibt die Kettenregel aus
der Schule, $(f \circ g)'(a) = f'(g(a)) \, g'(a)$. Warum das Matrixprodukt die richtige
Verallgemeinerung ist, wird im
[Kapitel „Gradientenabstieg“](../part-lernen/08-gradientenabstieg.md) hergeleitet: Man
setzt die beiden linearen Näherungen ineinander ein. Dort steht auch der Fall, der beim
Rechnen von Hand am häufigsten schiefgeht – eine Variable, die auf mehreren Wegen ins
Ergebnis eingeht. Die Kettenregel ist der Kern der Backpropagation.

### Die Richtungsableitung ist ein Skalarprodukt

Damit lässt sich die Behauptung von oben beweisen. Der Trick ist, die Richtung zu einer
Funktion *einer* Variablen zu machen. Statt $f$ auf ganz $\mathbb{R}^n$ zu betrachten,
läuft man die Gerade durch $a$ in Richtung $u$ entlang und leitet nach dem Laufparameter
ab.

:::{prf:theorem} Richtungsableitung und Gradient
Ist $f \colon \mathbb{R}^n \to \mathbb{R}$ differenzierbar in $a$, so existiert für jeden
Einheitsvektor $u$ die Richtungsableitung $D_u f(a)$, und es gilt

$$
D_u f(a) = \nabla f(a) \cdot u .
$$
:::

:::{prf:proof}
Sei $\gamma \colon \mathbb{R} \to \mathbb{R}^n$ die Gerade durch $a$ in Richtung $u$,

$$
\gamma(h) := a + h u .
$$

$\gamma$ ist affin, ihre beste lineare Näherung ist sie selbst, also ist
$(D\gamma)(h) = u$ für jedes $h$ – eine $n \times 1$-Matrix, nämlich die Spalte $u$.

Setze $\varphi := f \circ \gamma \colon \mathbb{R} \to \mathbb{R}$, also
$\varphi(h) = f(a + hu)$ und $\varphi(0) = f(a)$. Die Richtungsableitung ist nach
Definition nichts anderes als die gewöhnliche Ableitung von $\varphi$ an der Stelle $0$:

$$
D_u f(a) = \lim_{h \to 0} \frac{f(a + hu) - f(a)}{h}
         = \lim_{h \to 0} \frac{\varphi(h) - \varphi(0)}{h}
         = \varphi'(0) .
$$

Nun ist $\gamma$ differenzierbar in $0$ mit $\gamma(0) = a$ und $f$ differenzierbar in $a$,
die Kettenregel ist also anwendbar und liefert

$$
\varphi'(h) = (Df)\bigl(\gamma(h)\bigr) \cdot (D\gamma)(h)
            = \nabla f\bigl(\gamma(h)\bigr)^\top u .
$$

Dabei wurde benutzt, dass die Ableitung einer Funktion nach $\mathbb{R}$ die Zeile
$\nabla f^\top$ ist. An der Stelle $h = 0$ steht damit

$$
D_u f(a) = \varphi'(0) = \nabla f(a)^\top u = \nabla f(a) \cdot u ,
$$

und das war die Behauptung. Nebenbei ist mitbewiesen, dass die Richtungsableitung
überhaupt existiert: Sie ist die Ableitung einer nach der Kettenregel differenzierbaren
Funktion einer Variablen.
:::

**Die Voraussetzung ist keine Zierde.** Dass die partiellen Ableitungen existieren,
genügt *nicht* – dann steht zwar ein Gradient da, aber die Formel kann falsch sein. Für

$$
f(x, y) := \frac{x^2 y}{x^4 + y^2} \quad \text{für } (x,y) \neq (0,0), \qquad f(0,0) := 0
$$

rechnet man für einen Einheitsvektor $u = (\alpha, \beta)^\top$ und $h \neq 0$ nach:

$$
\frac{f(h\alpha, h\beta) - f(0,0)}{h}
= \frac{1}{h} \cdot \frac{h^3 \alpha^2 \beta}{h^4\alpha^4 + h^2\beta^2}
= \frac{\alpha^2 \beta}{h^2 \alpha^4 + \beta^2} .
$$

Für $\beta \neq 0$ geht das gegen $\alpha^2/\beta$, für $\beta = 0$ ist der Bruch konstant
null. *Alle* Richtungsableitungen existieren also. Insbesondere ist
$\frac{\partial f}{\partial x}(0,0) = 0$ (das ist $\alpha = 1, \beta = 0$) und
$\frac{\partial f}{\partial y}(0,0) = 0$ (das ist $\alpha = 0$), also
$\nabla f(0,0) = (0,0)^\top$. Für $u = \tfrac{1}{\sqrt2}(1,1)^\top$ ist aber

$$
D_u f(0,0) = \frac{\alpha^2}{\beta} = \frac{1/2}{1/\sqrt2} = \frac{1}{\sqrt2}
\neq 0 = \nabla f(0,0) \cdot u .
$$

Die Formel gilt also wirklich erst, wenn $f$ im Sinne der obigen Definition
differenzierbar ist – und das ist mehr, als die Existenz der partiellen Ableitungen
hergibt.

## Zweite Ableitungen: die Hesse-Matrix

:::{prf:definition} Hesse-Matrix
Für $f \colon \mathbb{R}^n \to \mathbb{R}$ mit zweiten partiellen Ableitungen ist die
Hesse-Matrix an der Stelle $a$

$$
H_f(a) := \left( \frac{\partial^2 f}{\partial x_i \, \partial x_j}(a) \right)_{i,j}
\in \mathbb{R}^{n \times n} .
$$
:::

Sind die zweiten Ableitungen stetig, ist $H_f$ symmetrisch (Satz von Schwarz). Sie
beschreibt die Krümmung. Der Gradient sagt nur, in welche Richtung es abwärts geht; die
Hesse-Matrix sagt zusätzlich, wie stark sich diese Richtung ändert, und unterscheidet an
einem kritischen Punkt Minimum, Maximum und Sattelpunkt.

Im Deep Learning kommt sie trotzdem kaum vor, und der Grund ist eine Abschätzung: $n$ ist
hier die Zahl der Parameter. Schon ein kleines Netz mit einer Million Parametern hätte
eine Hesse-Matrix mit $10^{12}$ Einträgen, in `float32` also vier Terabyte. Deshalb
arbeiten die Optimierer dieses Buchs mit Verfahren *erster* Ordnung und schätzen Krümmung
höchstens billig und implizit, über Momentum und adaptive Lernraten
([Kapitel „Optimierer“](../part-architekturen-anwendungen/26-optimierer.md)).

## Schwache Ableitung

ReLU hat bei $0$ einen Knick, und dort existiert die Ableitung nicht: Die einseitigen
Grenzwerte des Differenzenquotienten sind verschieden, es gibt keine Tangente. Dasselbe
gilt für den Betrag $|x|$. Trainiert wird trotzdem, und der Begriff, der das rechtfertigt,
ist der folgende.

:::{prf:definition} Schwache Ableitung
$g \colon \mathbb{R} \to \mathbb{R}$ heißt schwache Ableitung von
$f \colon \mathbb{R} \to \mathbb{R}$, wenn für alle $a < b$ gilt

$$
\int_a^b g(x) \, dx = f(b) - f(a).
$$
:::

Verlangt wird also nur die Eigenschaft, die eine gewöhnliche Ableitung im Hauptsatz hat.
Wo $f$ differenzierbar ist, stimmt jede schwache Ableitung mit $f'$ überein; an einzelnen
Stellen dagegen ist sie **nicht eindeutig**, denn ein Integral ändert sich nicht, wenn man
den Wert an endlich vielen Stellen ändert.

:::{prf:example} Der Betrag
$f(x) = |x|$ hat als schwache Ableitung die Vorzeichenfunktion $\operatorname{sign}$ mit
$\operatorname{sign}(0) = 0$. Dass gerade $0$ dort steht, ist Konvention, nicht Rechnung:
Jeder andere Wert an dieser einen Stelle täte es auch.
:::

Genau diese Freiheit nutzt ein Framework bei ReLU: Es gibt die Ableitung auf beiden Seiten
des Knicks zurück und legt sich an der Knickstelle auf einen Wert fest. Dass die Wahl
praktisch folgenlos ist, liegt daran, dass eine einzelne Stelle beim Lernen aus endlich
vielen Datenpunkten fast nie exakt getroffen wird. Die Konsequenzen für die Wahl der
Aktivierungsfunktion stehen im
[Kapitel „Aktivierungsfunktionen“](../part-lernen/11-aktivierungsfunktionen.md).

:::{admonition} Weiterlesen
:class: seealso
Deisenroth et al., *MML*, Kap. 5 (Vector calculus: partielle Ableitungen, Gradienten,
Jacobi- und Hesse-Matrix). Frei verfügbar, siehe
[Über dieses Skript](../README.md).
:::
