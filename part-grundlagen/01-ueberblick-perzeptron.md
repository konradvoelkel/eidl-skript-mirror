---
title: "VL 01: Überblick und Perzeptron"
short_title: "VL 01"
---

# Überblick und Perzeptron

:::{note} Stand
Erste Prosafassung (aus den Folien von VL 01, WiSe 2025/26). Abbildungen fehlen noch, siehe die `TODO`-Kommentare.
:::

## Was ist eigentlich Deep Learning?

Der Name ist erfreulich ehrlich: *Deep* heißt „viele Ebenen (Layer)“, *Learning* heißt „Training“. Deep Learning ist also das Training von künstlichen neuronalen Netzen mit vielen Ebenen. Was ein künstliches neuronales Netz ist, was eine Ebene ist und was beim Training passiert, ist der Inhalt dieser Vorlesung. Am Ende des Kapitels haben wir zumindest eine erste Definition.

### Was Sie mitbringen sollten

Wir setzen voraus, dass Sie die folgenden Begriffe schon einmal gesehen haben und keine Angst vor ihnen haben: Vektorraum und Vektor, Matrix, Ableitung, Zufallsvariable, und eine grobe Idee davon, was lineare Regression ist. Dazu Grundlagen in Python, idealerweise mit NumPy. Am besten hat man vorher das Modul „Data Science“ bestanden; die Module „Machine Learning“ oder „Data Science 2“ sind *nicht* erforderlich.

### Was wir zusammen lernen

Begriffe wie Gradientenabstieg, Loss-Funktion, Matrizen- und Tensorkalkül, latenter Raum, logistische Regression. Die Grundlagen von PyTorch. Was ein neuronales Netz ist, wie man fertige Modelle benutzt, wie man fertige Modelle verändert, und was die Besonderheiten bei Text und bei Bildern sind.

Der grobe Plan in Stichworten: Geschichte (Perzeptron) – HuggingFace (fertige Modelle) – PyTorch (eigene Modelle) – logistische Regression (Softmax) – Gradientenabstieg und Backpropagation – Sparse Autoencoder und VAE für die Klassifikation von MNIST-Ziffern – NLP mit word2vec und Tokenizern – CNNs für MNIST – GANs (wie DALL-E mini) – LLMs benutzen.

## Wieso Python eine Katastrophe ist

Für maschinelles Lernen ist Python eigentlich völlig ungeeignet, denn es ist

* **single-threaded by default**, mit Garbage Collection und GIL (global interpreter lock), was Multithreading eher erschwert als erleichtert;
* **interpretiert**, nicht direkt auf die Maschine kompiliert, und daher etwas langsam;
* **dynamisch gebunden**, d.h. nicht typesafe, und Typen sind erst zur Laufzeit bekannt, daher aufwändiges Typechecking;
* **nicht maschinennah**, daher ist es schwierig, SIMD-Register und Cachegrößen der spezifischen Hardware zur Optimierung zu nutzen.

## Wieso Python ganz toll ist

Für maschinelles Lernen ist Python perfekt, weil

* **Rapid Prototyping** im schnelllebigen ML-Geschäft erforderlich ist;
* die schwierigen Rechnungen in **C, Rust oder CUDA** durchgeführt werden und Python nur die Funktionsaufrufe macht;
* die Sprache sehr **populär** ist und damit viele gut gewartete Pakete das Datenhandling sehr leicht machen;
* man damit alle **Prinzipien** schnell lernen kann, die man später immer noch in anderen Sprachen implementieren könnte;
* damit trainierte Modelle (die **Gewichte**) unabhängig von Python zur Inferenz verwendet werden können.

Der scheinbare Widerspruch löst sich auf, wenn man Python als *Steuersprache* betrachtet: Die eigentliche Arbeit – Matrixmultiplikationen auf Millionen von Zahlen – passiert in kompiliertem Code, oft auf der GPU. Python sagt nur, welche Operation als nächstes dran ist. Genau das ist die Idee der vektorisierten Programmierung mit NumPy, und PyTorch treibt sie weiter.

:::{admonition} Lesetext zum Einstieg
:class: tip
[How AMD May Get Across the CUDA Moat](https://www.hpcwire.com/2023/10/05/how-amd-may-get-across-the-cuda-moat/) (HPCwire, 2023). Fragen zum Text:

1. Was ist der Unterschied zwischen GPU und SIMD?
2. Wer entwickelt PyTorch?
3. Was ist der Unterschied zwischen CUDA und ROCm?
:::

## Erinnerung: Begriffe aus dem maschinellen Lernen

### Daten und erzeugende Verteilung

Wir haben Datenpunkte $x_1, x_2, \dots, x_N$ mit jeweils $x_i \in \mathbb{R}^n$. Die Grundannahme des maschinellen Lernens ist, dass es eine *erzeugende Verteilung* (die Population) einer Zufallsvariable $X$ gibt, aus der die Datenpunkte als Stichprobe gezogen wurden – und die wir nicht kennen.

Ein **Modell** für $X$ ist eine Beschreibung dieser Verteilung, etwa durch eine Dichtefunktion $p(x)$ oder durch einen *Sampler*, also einen Algorithmus, der neue Stichproben $\tilde{x} \sim X$ erzeugt. Ein solches Modell heißt **generativ**, weil man damit Stichproben generieren kann. Ein klassisches Beispiel ist ein Gaussian Mixture Model, mit dem man etwa ein Bild in Vorder- und Hintergrund segmentieren kann.

<!-- TODO Abbildung: Segmentation with Gaussian mixture models (Scipy Lectures, CC BY) oder eigene matplotlib-Variante -->

### Supervised und Unsupervised

Wenn es zu den Datenpunkten auch (bekannte) **Label** gibt, d.h. nicht nur $x_1, \dots, x_N$, sondern auch $y_1, \dots, y_N$ mit $y_i \in \mathbb{R}^m$, so sprechen wir von **Supervised Learning**. Oft ist $m = 1$ (einfache Regression) oder sogar $y_i \in \{0, 1\}$ (binäre Klassifikation). Ohne Label ist es **Unsupervised Learning**; dazu gehören generative Modelle wie oben, aber auch Clustering und Dimensionsreduktion.

In beiden Fällen unterscheiden wir zwei Phasen:

* **Training**: Input sind die Daten, Output ist ein *gefittetes Modell* (bei uns: ein Satz Zahlen, die Gewichte).
* **Inferenz**: Input sind neue Daten und das gefittete Modell, Output ist die Vorhersage.

### Regression und Klassifikation

**Regression** ist supervised, d.h. es gibt $(x, y)$-Paare. Das Ziel ist ein funktionaler Zusammenhang

$$
Y = f(X) + \varepsilon,
$$

sodass für die Stichprobe $(x_i, y_i)$ der Fehler $\varepsilon$ möglichst klein ausfällt. Bei der linearen Regression ist $f$ affin-linear, $f(x) = w \cdot x + b$.

**Klassifikation** ist der Spezialfall, in dem $Y$ nur endlich viele Werte annimmt, z.B. $Y \in \{0, 1\}$. Man kann Klassifikation als Regression betreiben – man fittet $f$ mit reellen Werten und färbt anschließend nach $f(x) > \tfrac12$ – aber wir werden sehen, dass das nicht die beste Idee ist und die logistische Regression es besser macht.

<!-- TODO Abbildung: two-class demo data (make_blobs, linear trennbar entlang x-Achse) und lineare Regression mit Klasse als abhängiger Variable, Farbe = Vorhersage -->

### Die Kernfrage: Wie gut ist das Modell?

Wie bewerte ich die Güte des Modells, wie bewerte ich den Erfolg der Inferenz? Die Standardantwort ist der **Training-Test-Split**: Man hält einen Teil der Datenpunkte zurück (verwendet ihn nicht im Training), um damit das trainierte Modell zu testen. Die kompliziertere Variante ist die $k$-fold cross validation, bei der man die Daten in $k$ Teile zerlegt und reihum jeden Teil einmal als Testset verwendet.

:::{admonition} Quizfrage
:class: hint
Was kann beim Vergleich verschiedener Modelle und der Optimierung von Hyperparametern mit dem Testset passieren?
:::

## Kurzgeschichte

### Bis 2010

* **1943**: McCulloch und Pitts modellieren ein menschliches Hirnneuron mit elektrischen Schaltkreisen.
* **1958**: Rosenblatt entwirft das **Perzeptron** – und es wurde tatsächlich gebaut: Der *Mark I Perceptron* am Cornell Aeronautical Laboratory war ein frühes System zur Mustererkennung, mit Fotozellen als Eingabe und Potentiometern als Gewichten, die von Elektromotoren nachgestellt wurden.
* Das Perzeptron kann nur linear trennbare Klassen unterscheiden lernen (dazu gleich mehr). Diese Einsicht, prominent im Buch *Perceptrons* von Minsky und Papert (1969), gilt als Auslöser des ersten **AI Winter**. Wie viel an dieser offiziellen Geschichte dran ist, untersucht lesenswert: Olazaran, M. (1996). *A Sociological Study of the Official History of the Perceptrons Controversy.* Social Studies of Science, 26(3), 611–659.
* **1986**: Backpropagation wird (wieder-)erfunden bzw. populär, mehr Schichten werden verwendet.

### 2010–2015

Lesetipp: „The Decade of Deep Learning“ von Leo Gao, [bmk.sh/2019/12/31/The-Decade-of-Deep-Learning](https://bmk.sh/2019/12/31/The-Decade-of-Deep-Learning). Die Highlights für diese Vorlesung:

* **2012** AlexNet – „the paper that sparked the field of Deep Learning“: ein CNN gewinnt die ImageNet-Challenge mit großem Abstand, trainiert auf GPUs.
* **2013** word2vec – Repräsentation von Wörtern als Vektoren in einem latenten Raum.
* **2014** GANs – erstmals „realistische“ Bildgenerierung.

### Nach 2015

Das behandeln wir in dieser Vorlesung nicht mehr (sondern in den darauf aufbauenden Modulen):

* **2017** Transformer, „Attention is all you need“ – die Grundlage für GPT.
* **2020** AlphaFold 2 „löst“ das Proteinfaltungsproblem – Nobelpreis für Chemie 2024.
* **2021** Diffusionsmodelle für realistische Bildgenerierung.
* **2022** Veröffentlichung von ChatGPT; danach RLHF, Copilot, Multimodalität, RAG, Agents, …

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

<!-- TODO Abbildung: schematisches Neuron (x_1..x_5 → ζ = Σ w x → y = σ(ζ)), Grafik CC-BY-SA Whiteknight/Wikimedia oder eigenes TikZ/SVG -->

### Das Perzeptron

Rosenblatts Beitrag war weniger das Neuron als der *Lernalgorithmus* dafür. Das Perzeptron ist ein Modell zur **binären Klassifikation**: Input sind Stichproben von $(X, Y)$ mit $X \in \mathbb{R}^n$ und $Y \in \{0, 1\}$. Die Parameter des Modells sind ein Gewichtsvektor $w \in \mathbb{R}^n$ und ein Biasterm $b \in \mathbb{R}$. Die Inferenz ist

$$
f(x) = [\, w \cdot x + b > 0 \,],
$$

wobei $[\cdot]$ die Iverson-Klammer ist: $[A] = 1$, wenn die Aussage $A$ wahr ist, sonst $0$. Das Perzeptron ist also ein McCulloch-Pitts-Neuron mit der Schwellenwertfunktion $\sigma(\zeta) = [\zeta + b > 0]$. Man beachte: $f$ ist eine *nichtlineare* Funktion, obwohl im Inneren nur ein Skalarprodukt steht.

Den Bias kann man loswerden, indem man ihn als nulltes Gewicht auffasst: Mit $w_0 := b$ und $x_0 := 1$ ist $w \cdot x + b = \sum_{j=0}^n w_j x_j$. Das ist ein Trick, den wir noch öfter sehen werden.

Geometrisch beschreibt die Gleichung $w \cdot x + b = 0$ eine Hyperebene in $\mathbb{R}^n$ (in $\mathbb{R}^2$: eine Gerade), und $f$ gibt an, auf welcher Seite der Hyperebene $x$ liegt. Der Vektor $w$ steht senkrecht auf dieser Hyperebene.

:::{prf:definition} Linear trennbar
Zwei Mengen $A, B \subseteq \mathbb{R}^n$ heißen *linear trennbar*, wenn es $w \in \mathbb{R}^n$ und $b \in \mathbb{R}$ gibt mit
$w \cdot a + b > 0$ für alle $a \in A$ und $w \cdot c + b \le 0$ für alle $c \in B$.
:::

Ein Perzeptron kann also genau die Klassifikationsprobleme lösen, bei denen die beiden Klassen linear trennbar sind – nicht mehr. Das berühmte Gegenbeispiel ist XOR: Die Punkte $(0,0)$ und $(1,1)$ lassen sich nicht durch eine Gerade von $(0,1)$ und $(1,0)$ trennen. Das ist die mathematische Substanz hinter dem AI Winter – und der Grund, warum wir mehrere Neuronen hintereinander schalten werden.

Wie das Perzeptron *trainiert* wird, also wie $w$ und $b$ aus den Daten bestimmt werden, ist Thema des nächsten Kapitels und von Übungsblatt 2.

## Was ist ein neuronales Netz?

Ein **Multilayer Perceptron** (MLP) entsteht, indem die Ausgaben von mehreren (verallgemeinerten) Perzeptrons als Eingabe für ein weiteres Perzeptron verwendet werden, welches also eine Schicht (Layer) weiter hinten ist.

<!-- TODO Abbildung: MLP mit 3 Eingabeneuronen, 4 versteckten, 1 Ausgabeneuron (Folie 27) -->

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

## Tipps zum Übungsblatt

Das erste Blatt wiederholt lineare Algebra: Skalarprodukt, Orthogonalität, Länge und Winkel, und setzt das in NumPy und Matplotlib um. Erinnern Sie sich an die Interpretation des Kosinus eines Winkels als Verhältnis von Seiten im rechtwinkligen Dreieck: Mit Ankathete $a$ und Hypotenuse $b$ ist

$$
\cos(\alpha) = \frac{a}{b}.
$$

Was passiert im Spezialfall $b = 1$? Dann ist $\cos(\alpha) = a$, d.h. der Kosinus ist die Länge der Projektion eines Einheitsvektors auf die Richtung des anderen Schenkels. Genau das steckt in der Formel

$$
\cos(\alpha) = \frac{u \cdot v}{\|u\| \, \|v\|}
$$

für den Winkel zwischen zwei Vektoren $u, v \in \mathbb{R}^n$: Das Skalarprodukt $w \cdot x$ im Perzeptron misst, „wie sehr $x$ in Richtung $w$ zeigt“.
