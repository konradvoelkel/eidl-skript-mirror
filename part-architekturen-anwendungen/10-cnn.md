---
title: "VL 10: Convolutional Neural Networks"
short_title: "VL 10"
---

# Convolutional Neural Networks

:::{note} Stand
Erste Prosafassung (aus den Folien von VL 10, WiSe 2025/26). Abbildungen fehlen noch, siehe die `TODO`-Kommentare. Der Code ist im Notebook `VL_10_convolutions.ipynb`.
:::

## Motivation zur Faltung

### Bildverarbeitung: it's a blur

Wer schon einmal ein Bild in GIMP oder Photoshop weichgezeichnet hat, hat eine Faltung benutzt: Jeder Pixel wird durch einen gewichteten Mittelwert seiner Nachbarn ersetzt. Und wer Kanten gefunden hat („make a difference“): Das Originalbild minus das weichgezeichnete Bild lässt genau die Stellen übrig, an denen sich benachbarte Pixel stark unterscheiden – die Kanten.

<!-- TODO Abbildungen: Blur-Beispiel, Kantenfindung als Differenz (Folien 3–4) -->

### Das menschliche Auge erkennt Kanten(orientierung)

Hubel & Wiesel (1959) haben in der Sehrinde von Katzen Neuronen gefunden, die auf Balken einer bestimmten *Orientierung* antworten – und auf andere Orientierungen nicht (Reproduktion von Wurtz 1969, in Robert H. Wurtz: „Recounting the impact of Hubel and Wiesel“, J Physiol 2009). Solche Neuronen sind lokale Kantendetektoren: Sie schauen auf einen kleinen Ausschnitt des Gesichtsfelds und reagieren auf ein bestimmtes Muster darin. CNNs sind die technische Umsetzung dieser Idee, und die ersten Schichten eines trainierten CNN sehen tatsächlich aus wie Kantendetektoren verschiedener Orientierung.

<!-- TODO Abbildung: Hubel & Wiesel Neuron-Antwort auf Balkenorientierung (Wikipedia Mads00, CC-BY-SA) -->

### In der Informatik

Abgesehen von CNNs ist die Faltung das zentrale Instrument in der Signalverarbeitung. Das Eindimensionale ist leichter zu verstehen als das Zweidimensionale, damit fangen wir an.

## Eindimensionale Faltung

:::{prf:definition} Diskrete Faltung
Wenn $f \colon [-n, n] \to \mathbb{R}$ und $g \colon [0, N] \to \mathbb{R}$ (auf den ganzen Zahlen), dann ist $f \ast g \colon [0, N] \to \mathbb{R}$ definiert durch

$$
(f \ast g)(x) = \sum_{y = -n}^{n} f(y)\, g(x - y),
$$

wobei der Definitionsbereich von $g$ mit $0$ erweitert wird (*zero padding*).
:::

*Eine* Interpretation: $g$ ist das Signal, $f$ der sogenannte **Filter** (oder Kernel). Der Filter ist kurz ($2n + 1$ Werte), das Signal lang.

### Interpretation der Definition

Da steht ein Skalarprodukt des Vektors $(f(-n), \dots, f(n))$ mit $(g(x + n), \dots, g(x - n))$. Rechnung: Nimm einen $[-n, +n]$-Ausschnitt von $g$, zentriert bei $x$, dann *flippen* (bei $x$ spiegeln) und dann Skalarprodukt mit $f$. Das Flippen ist der Unterschied zwischen Faltung und *Korrelation*; für symmetrische Filter ($f(-y) = f(y)$) ist es egal, und in Deep-Learning-Bibliotheken wird tatsächlich meist die Korrelation berechnet und trotzdem „Convolution“ genannt. Da die Filter gelernt werden, spielt es keine Rolle.

Ein Faltungsfilter ist also ein *Neuron mit $2n + 1$ Gewichten*, das an jeder Position $x$ des Signals dasselbe Skalarprodukt mit dem lokalen Ausschnitt berechnet. Dieselben Gewichte an jeder Position: das heißt **Parameter Sharing**, und es hat zwei Konsequenzen. Erstens hat die Schicht nur $2n + 1$ Parameter, egal wie lang das Signal ist. Zweitens ist die Faltung **translationsäquivariant**: Verschiebt man das Signal, verschiebt sich das Ergebnis genauso.

### Beispiel: ASML-Aktienkurs

Wir möchten ein Signal mit einem Filter falten. Das Signal ist der ASML-Aktienkurs in US-Dollar (closing price adjusted for splits, ein Teildatensatz über 5 Jahre); der Filter ist eine schmale Gaußfunktion (`gaussian_narrow`). Das Ergebnis ist der geglättete Kurs: Die Gaußfunktion ist ein gewichteter gleitender Mittelwert, und je breiter sie ist, desto glatter das Ergebnis. Faltung mit einem Peak (einer diskreten Delta-Funktion) gibt das Signal unverändert zurück; Faltung mit einer Kastenfunktion ist der ungewichtete gleitende Mittelwert; Faltung mit der Differenz zweier Gaußfunktionen (*Difference of Gaussians*, DoG) hebt Änderungen hervor und ist ein Kantendetektor. (Tipp: „DoG filter“ ist kein Snapchat-Filter.)

<!-- TODO Abbildungen: Filterfunktionen (peak, constant, box, gaussian, DoG) und ASML-Kurs gefaltet mit jedem davon (Folien 12–14; Notebook, from_2025/slides/ASML.csv) -->

### Programmierung

Für den Code schauen wir ins Notebook (`VL_10_convolutions.ipynb`): mit `scipy.signal.convolve` für NumPy-Arrays und mit `torch.nn.functional.conv1d` für Tensoren. Bei `conv1d` muss man sich an die Dimensionen gewöhnen: Eingabe und Filter haben den Shape `(batch, channels, length)` bzw. `(out_channels, in_channels, kernel_size)`.

### Das Faltungstheorem

Für zwei stetige Funktionen $f, g$ und die stetige Faltung (Integral statt Summe) gilt für die Fouriertransformation $\mathcal{F}$:

$$
\mathcal{F}(f \ast g) = \mathcal{F}(f) \cdot \mathcal{F}(g),
$$

d.h. Faltung im Ortsraum ist Multiplikation im Frequenzraum. Auch umgekehrt: $\mathcal{F}(f \cdot g) = \mathcal{F}(f) \ast \mathcal{F}(g)$. Das erklärt, warum die Gaußfunktion glättet: Ihre Fouriertransformierte ist wieder eine Gaußfunktion, die hohe Frequenzen (= schnelle Änderungen, Rauschen) dämpft. Kurzer Ausflug in die Fourier-Transformation? Andrew Zisserman, [Lecture 2](https://www.robots.ox.ac.uk/~az/lectures/ia/lect2.pdf).

## Eindimensionales Pooling

### Pooling ≈ Binning

**Binning** = Array in feste disjunkte Blöcke (ohne Überlapp) zerlegen, dann Summe oder Mittelwert bilden. Das ist ungefähr eine Faltung mit einer Kastenfunktion, bei der man aber nur wenige Werte des Ergebnisses verwendet. Wie viel Überlapp es gibt, bestimmt der **Stride** (Schrittlänge).

**Pooling** = Array in feste Blöcke (mit Überlapp) einteilen. **Average-Pooling** = Pooling + Mittelwert der Blöcke. **Max-Pooling** = Pooling + Maximum der Blöcke.

### Pooling-Beispiel

Pooling eines Vektors $(a, b, c, d) \in \mathbb{R}^4$:

* Mit Stride 1 und Poolgröße 2: Pools $[(a, b), (b, c), (c, d)]$.
* Mit Stride 2 und Poolgröße 2: Pools $[(a, b), (c, d)]$; Average-Pooling gibt $[\operatorname{mean}(a, b), \operatorname{mean}(c, d)]$.
* Mit Stride 1 und Poolgröße 3: Pools $[(a, b, c), (b, c, d)]$; Max-Pooling gibt $[\max(a, b, c), \max(b, c, d)]$.

Von 4 Inputs reduzieren wir die Datenmenge also auf 3 oder 2 Outputs, je nach Größe und Stride. Pooling ist Dimensionsreduktion ohne Parameter, und Max-Pooling macht das Netz ein Stück weit *translationsinvariant*: Es ist egal, wo genau im Pool das Maximum lag.

Ein Stride größer als 1 kann man auch direkt bei der Faltung verwenden (*strided convolution*), dann reduziert die Faltung selbst die Dimension.

## Zweidimensionale Faltung

Für Bilder $g \colon [0, N] \times [0, M] \to \mathbb{R}$ (Graustufen) und Filter $f \colon [-n, n]^2 \to \mathbb{R}$:

$$
(f \ast g)(x_1, x_2) = \sum_{y_1 = -n}^{n} \sum_{y_2 = -n}^{n} f(y_1, y_2)\, g(x_1 - y_1, x_2 - y_2).
$$

Ein $3 \times 3$-Filter hat 9 Gewichte, die an jeder Pixelposition dasselbe Skalarprodukt mit der $3 \times 3$-Nachbarschaft bilden. Beispiel mit GIMP: Unter *Filter → Allgemein → Faltungsmatrix* kann man die 9 Werte selbst eintragen und sieht unten den Output der 2D-Faltung – Weichzeichner, Schärfen, Kanten, Relief sind alles nur verschiedene Matrizen.

<!-- TODO Abbildung: GIMP-Faltungsmatrix-Dialog und Ergebnis (Folie 30) -->

Bei Farbbildern hat die Eingabe 3 **Kanäle** (RGB), und ein Filter hat dann Shape $3 \times 3 \times 3$: Er summiert über alle Eingabekanäle. Eine Faltungsschicht mit $C_{\text{out}}$ Filtern erzeugt $C_{\text{out}}$ Ausgabekanäle (*Feature Maps*). Ein $1 \times 1$-Filter schaut nur auf einen Pixel, aber über alle Kanäle – das ist ein linearer Layer pro Pixel und wird benutzt, um die Anzahl der Kanäle zu ändern, ohne die räumlichen Dimensionen anzurühren.

## CNNs

Ein **Convolutional Neural Network** ist ein neuronales Netz, in dem (einige) Schichten Faltungen sind: `nn.Conv1d` bzw. `nn.Conv2d` mit lernbaren Filtergewichten, gefolgt von einer Aktivierungsfunktion, oft gefolgt von Pooling. Typische Architektur für Bildklassifikation: mehrere Blöcke aus Conv → ReLU → MaxPool, wobei die räumliche Auflösung sinkt und die Anzahl der Kanäle steigt, dann *flatten* und ein oder zwei lineare Schichten mit Softmax. Die Faltungsschichten lernen in den frühen Layern allgemeine Merkmale wie Kanten und Ecken, in späteren Layern zusammengesetzte Muster.

Man beachte: Jede Berechnung mit einem Faltungslayer kann auch mit einem linearen (fully connected) Layer durchgeführt werden – die Faltung ist ja linear, also eine Matrix, nur eine sehr spezielle mit vielen Nullen und wiederholten Einträgen. Der Punkt der Faltung ist nicht, dass sie *mehr* kann, sondern dass sie mit viel weniger Parametern das Richtige kann, wenn die Daten lokale, verschiebungsinvariante Struktur haben. Und man muss nicht alle Layer zu Faltungen machen; die letzten Schichten eines CNN sind fast immer linear.

### 1-dimensionale CNNs

Im Notebook: `F.conv1d` mit handgesetzten Filtern (Gauß, DoG) auf dem ASML-Kurs, und die Beobachtung, dass ein gelernter 1D-Filter genau solche Formen annimmt.

### 2-dimensionale CNNs

Im Notebook: `nn.Conv2d` auf einem Foto (`pallino.jpg`) mit verschiedenen $3 \times 3$-Filtern. Weiterführend:

* Animationen von Vincent Dumoulin und Francesco Visin zu Padding, Stride und Dilation: [github.com/vdumoulin/conv_arithmetic](https://github.com/vdumoulin/conv_arithmetic).
* Interaktives MNIST-CNN-Explorationswerkzeug von Adam Harley: [adamharley.com/nn_vis/cnn/2d.html](https://adamharley.com/nn_vis/cnn/2d.html) – man zeichnet eine Ziffer und sieht alle Feature Maps aller Schichten.
* Für Code ins Notebook schauen; das Übungsblatt 10 rechnet Faltungen und Pooling von Hand.
