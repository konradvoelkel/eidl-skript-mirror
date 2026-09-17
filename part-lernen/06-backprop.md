---
title: "VL 06: Backpropagation"
short_title: "VL 06"
---

# Backpropagation

:::{note} Stand
Erste Prosafassung (aus den Folien von VL 06, WiSe 2025/26). Abbildungen fehlen noch, siehe die `TODO`-Kommentare.
:::

## Ziel für heute

Verstehen können, was im [TensorFlow Playground](https://playground.tensorflow.org) geschieht. Als Aufwärmübung: Setzen Sie dort die Gewichte von Hand, mit 2 Hidden Layers zu je 2 Neuronen, um das XOR-Problem zu lösen. Das geht (Kapitel 1), aber es ist mühsam – und genau das Mühsame soll der Gradientenabstieg übernehmen. Dafür brauchen wir den Gradienten der Loss-Funktion nach *allen* Gewichten aller Schichten.

## Training mehrerer Schichten: Motivation

### Beispielsetup 1

Eingabedaten sind eindimensional, ein einzelnes Neuron mit Aktivierungsfunktion $\sigma$ produziert eine Ausgabe, die stecken wir in ein zweites Neuron mit Aktivierungsfunktion $\operatorname{id}$. Also:

$$
y_{\text{pred}} = \bigl\langle w_{\text{zweit}},\, \sigma(\langle w_{\text{erst}}, x \rangle) \bigr\rangle .
$$

<!-- TODO Abbildung: x → [w_erst] → σ → [w_zweit] → y_pred -->

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

Für die Ableitung nach $W_3$: $dE = r^T dW_3\, z_3 = \operatorname{tr}(r^T dW_3\, z_3) = \operatorname{tr}(z_3 r^T dW_3)$ – der Trick ist, dass die Spur zyklisch vertauscht werden darf – also

$$
\nabla_{W_3} E = r\, z_3^T .
$$

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

Genau das tut `loss.backward()` in PyTorch: Beim Vorwärtsrechnen merkt sich jeder Tensor mit `requires_grad`, aus welcher Operation er entstanden ist (der *Berechnungsgraph*), und `backward` läuft diesen Graphen rückwärts ab und schreibt die Gradienten in die `.grad`-Attribute der Parameter. `optimizer.step()` macht dann $W \leftarrow W - \rho \nabla_W E$.

### Matrix-Differentialkalkül: Literaturtipps

Achtung: Das ist nicht notwendig für diese Veranstaltung, das ist weiterführend.

* Thomas P. Minka, *Old and new matrix algebra useful for statistics*, Notes, 2000.
* *The Matrix Cookbook* (Petersen & Pedersen).
* *Matrix derivatives cheat sheet*.
* Wikipedia: *Loss functions for classification*.
* Michael Nielsens Buchkapitel zu Backpropagation (sehr mathematisch): [neuralnetworksanddeeplearning.com/chap2.html](http://neuralnetworksanddeeplearning.com/chap2.html).

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

**Ableitung** von $\max(0, y)$ nach $y$: Für $y > 0$ ist $\max(0, y) = y$, also ist die Ableitung $1$. Für $y < 0$ ist $\max(0, y) = 0$, also ist die Ableitung $0$. Für $y = 0$ ist die Ableitung nicht definiert – wir *definieren* sie als $0$, das spart Rechnungen. (Dass das erlaubt ist, ist genau der Inhalt von Blatt 3: schwache Ableitungen dürfen an einzelnen Punkten beliebig sein.)

**Wieso ist ReLU geeignet?** Lineare Abbildung + ReLU ist die Projektion auf einen Halbraum, denn ReLU ist genau die Projektion von $\mathbb{R}$ auf $[0, \infty)$, und ein Halbraum ist eine Seite einer Hyperebene. Ein ReLU-Neuron $\max(0, \langle w, x \rangle + b)$ ist also null auf der einen Seite der Hyperebene $\langle w, x \rangle + b = 0$ und linear ansteigend auf der anderen. Summiert man mehrere solche „Knickfunktionen“ mit Gewichten, bekommt man stückweise lineare Funktionen, deren Knickstellen auf den Hyperebenen liegen – und mit genug Neuronen kann man damit jede stetige Funktion beliebig gut approximieren. Beispiel an der Tafel; im nächsten Kapitel bauen wir so von Hand $x^2$.

<!-- TODO Abbildung: ReLU-Graph; Summe von drei ReLUs als stückweise lineare Funktion -->

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

<!-- TODO Abbildung: ReLU, ELU, Swish, GELU im Vergleich (Folie 46) -->

## Autoencoder

### Im Kontrast zu unserem bisherigen Vorgehen

Bisher haben wir ein Neuron oder ein neuronales Netz zur Klassifikation oder Regression verwendet: Eine nicht bekannte Funktion $f$, für die wir manche Werte kennen (Label $y = f(x)$ für Trainingsdaten $(x, y)$), wollen wir mit dem Modell „schätzen“. Was, wenn wir keine Label haben?

### Herleitung zur abstrakten Idee

Ohne Label müssen wir den Output des neuronalen Netzes anders bewerten. Wie Erfolg messen? Welches Ziel ist im Training noch sinnvoll?

Ein mögliches Ziel: **Transformation der Eingabe in ein anderes Koordinatensystem** (Feature Extraction). Das kann man rückgängig machen – und messen, wie gut das klappt. Abstrakt: $f$ ist nicht bekannt, aber $g \circ f$ ist bekannt, nämlich $g(f(x)) = x$. Hier heißt $f$ **Encoder** und $g$ **Decoder**, und $g \circ f$ soll die Identität sein.

Das allein wäre trivial ($f = g = \operatorname{id}$). Interessant wird es mit einer Einschränkung: **Dimensionsreduktion**. Versuche, die Dimensionalität zu reduzieren ohne Informationsverlust – transformiere die Eingabe in ein *kleineres* Koordinatensystem, sodass man es trotzdem rückgängig machen kann. Der Encoder $f \colon \mathbb{R}^n \to \mathbb{R}^k$ mit $k \ll n$ muss dann lernen, was an den Daten wesentlich ist.

### Loss-Funktion

Trainingsziel: Output so ähnlich wie möglich zum Input (**Rekonstruktion**). Vergleiche Input mit Output, z.B. über die mittlere quadratische Abweichung der Pixelwerte:

$$
L(x; f, g) = \frac1N \sum_{i=1}^N \bigl\| x_i - g(f(x_i)) \bigr\|^2 .
$$

Der Autoencoder ist also ein neuronales Netz mit einem „Flaschenhals“ in der Mitte, trainiert mit MSE zwischen Ein- und Ausgabe – und die Label sind die Eingaben selbst. Man nennt das auch *self-supervised*.

<!-- TODO Abbildung: Autoencoder schematisch (Michaela Massi 2019, CC-BY-SA 4.0) -->

Im Vergleich zur Dimensionsreduktion mit PCA: Ist der Autoencoder linear (keine Aktivierungsfunktionen), so findet er denselben Unterraum wie PCA. Mit Nichtlinearitäten kann er gekrümmte Strukturen in den Daten erfassen, die PCA verfehlt, und rekonstruiert z.B. Bilder bei gleicher Dimension des Flaschenhalses deutlich besser.

<!-- TODO Abbildung: Rekonstruktion Autoencoder vs. PCA (Michaela Massi 2019) -->

## Tipps zum Übungsblatt

Auf Blatt 6 lesen Sie einen Autoencoder-Quelltext und formulieren Fragen dazu. Benutzen Sie zur Formulierung der Fragen sowie zur Beantwortung *keine* generative KI – sonst lernen Sie genau das nicht: wie man anhand der offiziellen Dokumentation prüfen kann, ob die KI-Antwort korrekt ist. Ziel ist nicht die „richtige Lösung“, sondern der Erwerb der Kompetenz, Deep-Learning-Quelltexte kritisch zu lesen.
