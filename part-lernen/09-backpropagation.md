---
title: "Backpropagation"
short_title: "Backpropagation"
---

# Backpropagation

## Ziel

Verstehen können, was im [TensorFlow Playground](https://playground.tensorflow.org) geschieht.

:::{admonition} Ausprobieren: TensorFlow Playground
:class: tip
Wählen Sie den XOR-Datensatz (die vier Quadranten), 2 Hidden Layers zu je 2 Neuronen, Aktivierung `tanh` oder `ReLU`, und setzen Sie die sechs Gewichte *von Hand* (auf eine Verbindung klicken, Wert eintippen), bis die vier Quadranten richtig gefärbt sind. Das geht ([Kapitel „Neuron und Perzeptron“](../part-grundlagen/02-neuron-perzeptron.md) und [„Netze von Hand bauen“](12-netze-von-hand.md)), aber es ist mühsam. Dann Reset und Play. Zu beobachten: Der Gradientenabstieg findet meist *krumme* Gewichte, die trotzdem funktionieren; manche Neuronen sind redundant oder tragen nichts bei; die Lösung hängt von der zufälligen Initialisierung ab, und man kann während des Trainings einzelne Gewichte von Hand editieren und zusehen, wie das Netz sich erholt. Mit einem einzigen Hidden Layer aus vielen Neuronen sieht man, wie die Entscheidungsgrenze aus Stücken zusammengesetzt wird; das ist die Universalität aus dem [Kapitel „Universelle Approximation“](13-universelle-approximation.md).
:::

Genau das Mühsame soll der Gradientenabstieg übernehmen. Dafür brauchen wir den Gradienten der Loss-Funktion nach *allen* Gewichten aller Schichten.

## Training mehrerer Schichten: Motivation

### Beispielsetup 1

Eingabedaten sind eindimensional, ein einzelnes Neuron mit Aktivierungsfunktion $\sigma$ produziert eine Ausgabe, die stecken wir in ein zweites Neuron mit Aktivierungsfunktion $\operatorname{id}$. Also:

$$
y_{\text{pred}} = \bigl\langle w_{\text{zweit}},\, \sigma(\langle w_{\text{erst}}, x \rangle) \bigr\rangle .
$$

:::{figure} ../images/vl06-two-neurons.png
:width: 90%

Beispielsetup 1: zwei Neuronen hintereinander.
:::

Wir planen eine Regression mit $x, y \in \mathbb{R}$, daher nehmen wir den MSE-Loss:

$$
L(x, y; W) = \operatorname{MSE}(y, y_{\text{pred}}) = \sum_{i=1}^N (y_i - y_{\text{pred}, i})^2
\quad\Longrightarrow\quad
L'(W) = \sum_{i=1}^N 2\,(y_i - y_{\text{pred}, i}) \left( -\frac{\partial}{\partial W} y_{\text{pred}, i} \right).
$$

Die Frage ist also nur: Was ist $\frac{\partial}{\partial W} y_{\text{pred}}$, die Ableitung der Netzausgabe nach den Gewichten?

### Vorbereitung

Nehmen wir $W = (w_{\text{erst}}, w_{\text{zweit}})$, so können wir $y_{\text{pred}}$ als Funktion von $W$ auffassen, $y_{\text{pred}}(W) = \langle w_{\text{zweit}}, \sigma(\langle w_{\text{erst}}, x \rangle) \rangle$, und die Ableitung nach $W$ wie zuvor in Komponenten berechnen. Dafür brauchen wir zwei Bausteine:

* Was ist die Ableitung von $\sigma(f(w))$ nach $w$? Kettenregel: $\frac{d}{dw} \sigma(f(w)) = \sigma'(f(w)) \, f'(w)$.
* Was ist die Ableitung von $\langle w, x \rangle$ nach $w$, und von $\langle v, f(w) \rangle$ nach $w$? Es ist $\frac{d}{dw} \langle w, x \rangle = x$ und $\frac{d}{dw} \langle v, f(w) \rangle = \langle v, f'(w) \rangle$.

Damit:

$$
\frac{\partial}{\partial w_{\text{erst}}} y_{\text{pred}}(W) = \bigl\langle w_{\text{zweit}},\, \sigma'(\langle w_{\text{erst}}, x \rangle)\, x \bigr\rangle,
\qquad
\frac{\partial}{\partial w_{\text{zweit}}} y_{\text{pred}}(W) = \sigma(\langle w_{\text{erst}}, x \rangle).
$$

### Die Update-Regeln

Eingesetzt in $L'$ und in die Gradientenabstiegs-Regel $W_{\text{neu}} = W_{\text{alt}} - \rho L'(W_{\text{alt}})$:

$$
w_{\text{zweit,neu}} = w_{\text{zweit,alt}} + \rho \sum_{i=1}^N 2\,\Bigl(y_i - \bigl\langle w_{\text{zweit,alt}}, \sigma(\langle w_{\text{erst,alt}}, x_i \rangle) \bigr\rangle\Bigr)\, \sigma(\langle w_{\text{erst,alt}}, x_i \rangle),
$$

$$
w_{\text{erst,neu}} = w_{\text{erst,alt}} + \rho \sum_{i=1}^N 2\,\Bigl(y_i - \bigl\langle w_{\text{zweit,alt}}, \sigma(\langle w_{\text{erst,alt}}, x_i \rangle) \bigr\rangle\Bigr)\, \bigl\langle w_{\text{zweit,alt}}, \sigma'(\langle w_{\text{erst,alt}}, x_i \rangle)\, x_i \bigr\rangle .
$$

Das funktioniert, aber es ist unübersichtlich – und man sieht schon, dass Teilausdrücke mehrfach vorkommen: der Residuenterm $y_i - y_{\text{pred},i}$ und die Aktivierung $\sigma(\langle w_{\text{erst}}, x_i \rangle)$ der ersten Schicht tauchen in beiden Regeln auf.

### Beispielsetups 2 und 3: mehr Dimensionen, mehr Neuronen

*Setup 2*: Eingabedaten sind zweidimensional, sonst wie oben. Jetzt neu: $w_{\text{erst}} \in \mathbb{R}^2$. An den Formeln ändert sich nichts, die Skalarprodukte sind nur länger.

*Setup 3*: Eingabedaten sind zweidimensional, *zwei* Neuronen mit Aktivierungsfunktion $\sigma$ und Gewichten $u, v \in \mathbb{R}^2$ produzieren Ausgaben, die stecken wir in ein drittes Neuron mit Aktivierungsfunktion $\operatorname{id}$ und Gewichten $w \in \mathbb{R}^2$:

$$
y_{\text{pred}} = \bigl\langle w,\, (\sigma\langle u, x \rangle,\ \sigma\langle v, x \rangle) \bigr\rangle .
$$

### Layer

Mehrere Neuronen, die parallel verarbeitet werden, bilden eine **Schicht** (Layer). Mehrmals lineare Regression ist *multilineare Regression* ist ein **Linear Layer** ist eine Matrix, deren Zeilen die Gewichtsvektoren sind. Schreiben wir also $u, v$ als Zeilen in eine Matrix $A \in \mathbb{R}^{2 \times 2}$ und benutzen $\sigma$ auf Vektoren komponentenweise, so ist

$$
y_{\text{pred}} = \langle w, \sigma(Ax) \rangle = w^T \sigma(Ax).
$$

Die Ableitung nach einem einzelnen Gewicht $u_1 = A_{11}$ ist $\frac{\partial}{\partial u_1} = \frac{\partial}{\partial A_{11}}$, und für die ganze Matrix:

$$
\frac{\partial}{\partial A} y_{\text{pred}} = \frac{\partial}{\partial A} w^T \sigma(Ax) = w^T \frac{\partial}{\partial A} \sigma(Ax) = w^T \sigma'(Ax)\, x,
\qquad
\frac{\partial}{\partial w} y_{\text{pred}} = \frac{\partial}{\partial w} w^T \sigma(Ax) = \sigma(Ax).
$$

(Wobei bei $w^T \sigma'(Ax)\, x$ die Dimensionen passend zu lesen sind: $\sigma'(Ax)$ ist eine Diagonalmatrix, und das Ergebnis ist eine $2 \times 2$-Matrix, deren Eintrag $(j, k)$ gleich $w_j \sigma'((Ax)_j) x_k$ ist.)

**Idee:** Berechne für $y_{\text{pred}}$ gleichzeitig die Daten für den Gradienten. Nach der Kettenregel $\frac{d}{dx} f(g(x)) = f'(g(x))\, g'(x)$ mit $g(x) = \sigma(Ax)$ und $f(z) = w^T z$ berechnen wir zuerst $g$ und $g'$ vom ersten Layer, dann damit den nächsten Layer, usw. bis zum letzten. Die Zwischenergebnisse der Vorwärtsrechnung sind genau das, was die Rückwärtsrechnung braucht.

## Backpropagation konkret

### Beispiel 4: ein Netz mit drei Schichten

Wir betrachten

$$
f(x) = b_3 + W_3 \tanh\bigl(b_2 + W_2 \tanh(b_1 + W_1 x)\bigr)
$$

und schreiben die Vorwärtsrechnung (*forward computation*) schichtweise auf:

$$
\begin{aligned}
z_1 &= x && \text{(input layer)} \\
z_2 &= \tanh(b_1 + W_1 z_1) && \text{(2nd layer)} \\
z_3 &= \tanh(b_2 + W_2 z_2) && \text{(3rd layer)} \\
y_{\text{pred}} &= b_3 + W_3 z_3 && \text{(output layer)} \\
r &= y_{\text{pred}} - y && \text{(residual)} \\
E &= \tfrac12\, r^T r && \text{(squared error)}
\end{aligned}
$$

Der Faktor $\tfrac12$ ist reine Bequemlichkeit, er kürzt sich gleich gegen die $2$ aus der Ableitung des Quadrats.

### Rückwärts differenzieren

Wir verwenden die Notation der Differentiale: $dE$ ist die lineare Änderung von $E$ bei einer infinitesimalen Änderung der Parameter, und $\nabla_b E$ bezeichnet den Gradienten von $E$ nach $b$ (mit der Konvention $dE = \langle \nabla_b E, db \rangle$). Wir arbeiten uns von hinten nach vorn (*backwards differentiation*).

**Output layer.** Es ist

$$
dE = d\bigl(\tfrac12 r^T r\bigr) = \tfrac12 \, d(r^T r) = r^T\, dr = r^T\, dy_{\text{pred}},
$$

denn $y$ ist konstant. Weiter ist $dy_{\text{pred}} = d(b_3 + W_3 z_3) = db_3 + dW_3\, z_3 + W_3\, dz_3$. Für die Ableitung nach $b_3$ betrachten wir nur den ersten Term: $dE = r^T db_3$, also

$$
\nabla_{b_3} E = r .
$$

Für die Ableitung nach $W_3$ ist das Ergebnis

$$
\nabla_{W_3} E = r\, z_3^T .
$$

:::{admonition} Vertiefung: der Spur-Trick
:class: note dropdown
Woher kommt das? Aus $dE = r^T dW_3\, z_3$ soll ein Ausdruck der Form $\langle \nabla_{W_3} E, dW_3 \rangle = \operatorname{tr}\bigl((\nabla_{W_3} E)^T dW_3\bigr)$ werden. Der Skalar $r^T dW_3\, z_3$ ist seine eigene Spur, und die Spur darf zyklisch vertauscht werden: $\operatorname{tr}(r^T dW_3\, z_3) = \operatorname{tr}(z_3 r^T dW_3)$. Der Vergleich mit $\operatorname{tr}\bigl((\nabla_{W_3} E)^T dW_3\bigr)$ liefert $(\nabla_{W_3} E)^T = z_3 r^T$. Wer das nicht mag, rechnet komponentenweise: $\partial E / \partial (W_3)_{jk} = r_j\,(z_3)_k$, dasselbe Ergebnis.
:::

Das ist ein *äußeres Produkt*: Der Gradient nach der Gewichtsmatrix ist Residuum mal Eingabe der Schicht, transponiert – so wie beim einzelnen Neuron der Gradient nach $w$ gleich Fehler mal $x$ war.

**Nächste Schicht.** Jetzt können wir $b_3$ und $W_3$ als Konstanten sehen: $dE = r^T W_3\, dz_3 + \text{irrelevante Terme}$. Mit der Kettenregel gilt $\frac{d}{dz} \tanh(f(z)) = (1 - \tanh(f(z))^2)\, f'(z)$, also

$$
dz_3 = d \tanh(b_2 + W_2 z_2) = (1 - z_3^2) \odot (db_2 + dW_2\, z_2 + W_2\, dz_2),
$$

wobei $z_3^2$ und $\odot$ komponentenweise zu lesen sind. Für $b_2$: $dE = r^T W_3 \operatorname{diag}(1 - z_3^2)\, db_2$, also

$$
\nabla_{b_2} E = (1 - z_3^2) \odot W_3^T r,
\qquad
\nabla_{W_2} E = (\nabla_{b_2} E)\, z_2^T .
$$

**Und noch eine Schicht.** Nach demselben Muster:

$$
\nabla_{b_1} E = (1 - z_2^2) \odot W_2^T (\nabla_{b_2} E),
\qquad
\nabla_{W_1} E = (\nabla_{b_1} E)\, z_1^T .
$$

### Das Muster

Zusammengefasst, mit $\delta_k := \nabla_{b_k} E$ als „Fehlersignal“ der Schicht $k$:

$$
\delta_3 = r, \qquad
\delta_2 = (1 - z_3^2) \odot W_3^T \delta_3, \qquad
\delta_1 = (1 - z_2^2) \odot W_2^T \delta_2,
\qquad
\nabla_{W_k} E = \delta_k\, z_k^T .
$$

Das Fehlersignal wird von Schicht zu Schicht *rückwärts propagiert*: mit der transponierten Gewichtsmatrix multipliziert und mit der Ableitung der Aktivierungsfunktion gewichtet. Man nutzt die Zwischenschritte $z_k$ aus der Vorwärtsrechnung, um den vollen Gradienten effizient zu berechnen – ein Vorwärtsdurchlauf, ein Rückwärtsdurchlauf, fertig. Der Aufwand ist etwa das Doppelte einer Inferenz, unabhängig von der Anzahl der Parameter. Das ist **Backpropagation**, und danach kommt Gradientenabstieg.

Genau das tut `loss.backward()` in PyTorch ([Kapitel „Autograd und Berechnungsgraph“](10-autograd-berechnungsgraph.md)): Beim Vorwärtsrechnen merkt sich jeder Tensor mit `requires_grad`, aus welcher Operation er entstanden ist (der *Berechnungsgraph*), und `backward` läuft diesen Graphen rückwärts ab und schreibt die Gradienten in die `.grad`-Attribute der Parameter. `optimizer.step()` macht dann $W \leftarrow W - \rho \nabla_W E$.

### Matrix-Differentialkalkül: Literaturtipps

Achtung: Das ist nicht notwendig für diese Veranstaltung, das ist weiterführend.

* Thomas P. Minka, *Old and new matrix algebra useful for statistics*, Notes, 2000.
* *The Matrix Cookbook* (Petersen & Pedersen).
* *Matrix derivatives cheat sheet*.
* Wikipedia: *Loss functions for classification*.
* Michael Nielsens Buchkapitel zu Backpropagation (sehr mathematisch): [neuralnetworksanddeeplearning.com/chap2.html](http://neuralnetworksanddeeplearning.com/chap2.html).

## Backpropagation als Induktion

Noch einmal systematisch, als Wiederholung und Zusammenfassung aus der Übung – denn Backpropagation ist Klausurstoff (Aufgabentyp 4), und die Formulierung als Induktion ist die, mit der man jede Architektur erschlägt.

### Warum Backpropagation funktioniert

1. Im **Forward Pass** speichern wir für jede Rechenoperation das Zwischenergebnis und merken uns die Ableitung der einzelnen Rechenoperation und auf welche vorangehenden Ergebnisse wir zurückgreifen müssen (Konstruktion des DAG).
2. Im **Backward Pass** können wir für jede Rechenoperation jeweils nach den Gewichten ableiten, die für diese Operation relevant sind. Wenn wir nach Gewichten ableiten, von denen die vorangegangenen Rechenoperationen abhängen, müssen wir die Kettenregel anwenden. Dazu benötigen wir nur die Ableitung der neuen Rechenoperation (gespeichert im Forward Pass), den Wert der Rechenoperation (gespeichert im Forward Pass) und die Ableitung der vorangegangenen Rechenoperationen.

Mit vollständiger Induktion sehen wir also: Wir können alle Ableitungen berechnen mit *einem* Durchlauf durch den DAG. Insbesondere können wir die Loss-Funktion (das „Ende“ des DAG) nach allen Gewichten ableiten und so den vollständigen Gradienten berechnen.

### Der Induktionsschritt, systematisch

Wir bezeichnen den Input als $x \in \mathcal{X}$. Die „bisherigen Rechenoperationen“ sind eine Abbildung $Y \colon \mathcal{X} \to \mathcal{Y}$, also $y := Y(x; w_Y)$, deren Ableitungen $\frac{dY}{dw_Y}(x; w_Y)$ wir per Induktion kennen. Die „nächste Rechenoperation“ ist eine Abbildung $Z \colon \mathcal{Y} \to \mathcal{Z}$, deren Ableitungen $\frac{dZ}{dy}$ und $\frac{dZ}{dw_Z}$ wir kennen. Die Kettenregel erlaubt uns, $Z(Y(x; w_Y); w_Z)$ nach $w_Y$ abzuleiten:

$$
\frac{d}{dw_Y} Z(Y(x; w_Y); w_Z) = \frac{dZ}{dy}(y; w_Z) \cdot \frac{dY}{dw_Y}(x; w_Y),
\qquad
\frac{d}{dw_Z} Z(Y(x; w_Y); w_Z) = \frac{dZ}{dw_Z}(y; w_Z).
$$

Spezialfälle: Wenn die nächste Rechenoperation der Loss ist, gibt es keine „neuen Gewichte“, dann ist nur die Ableitung nach „bisherigen Gewichten“ relevant. Der Induktionsanfang ist gegeben, indem $Y$ die Identitätsfunktion ist (Ableitung ist $1$). In knapperer Notation, mit Kleinbuchstaben als Funktionsnamen:

$$
\frac{dz}{dw} = \frac{dz}{dy} \cdot \frac{dy}{dw}.
$$

### Nicht konkret genug? Ein weiteres einfaches Beispiel

Wir wählen als Input $x \in \mathcal{X} \subseteq \mathbb{R}^n$. Im Beispiel soll $y := y(x; w) := w \cdot x$ sein, also ein linearer Layer. Die „nächste Rechenoperation“ ist $z \colon \mathbb{R} \to \mathbb{R}$, und zwar $z := z(y) := \operatorname{ReLU}(y) = \max(0, y)$. Die Ableitung nach $y$ ist $[y > 0]$. Aus $\frac{dz}{dw} = \frac{dz}{dy} \cdot \frac{dy}{dw}$ wird also

$$
\frac{dz}{dw} = [y > 0] \cdot x .
$$

Übungsaufgabe: Erweitern Sie den linearen Layer um ein zweites Neuron (also ein weiterer Gewichtsvektor $v \in \mathbb{R}^n$ tritt auf) und erweitern Sie die Berechnung um eine Loss-Funktion $\| z - z_{\text{ground truth}} \|^2$. (Das ist Blatt 7 in Kurzform.)

:::{admonition} Weiterlesen
:class: seealso
Prince, *UDL*, Kap. 7 (Gradients and initialization), dort Backpropagation mit derselben Rückwärts-Notation. Beide Bücher sind frei verfügbar, siehe [Über dieses Skript](../README.md).
:::
