---
title: "Das Perzeptron"
short_title: "Perzeptron"
---

# Das Perzeptron

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

Wie das Perzeptron *trainiert* wird, also wie $w$ und $b$ aus den Daten bestimmt werden, ist Thema des übernächsten Abschnitts und von Übungsblatt 2.

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

## Das Perzeptron trainieren

Im letzten Kapitel haben wir das Perzeptron als Modell kennengelernt: ein Gewichtsvektor $w \in \mathbb{R}^n$, ein Bias $b \in \mathbb{R}$, und die Inferenz $f(x) = [\, w \cdot x + b > 0 \,]$. Was fehlt, ist das *Lernen*. Bevor wir ein Modell implementieren, sollten wir uns ein paar Fragen stellen, die für jedes Modell in dieser Vorlesung wieder auftauchen werden:

* Was sind die **freien Parameter** (Gewichte) des Modells – welche Variablen ändern sich beim Training?
* Wie soll die **Inferenz** durchgeführt werden?
* Wie funktioniert das **Training**?
  * supervised oder unsupervised?
  * Was genau erlauben wir für Datentypen?
  * Welche Berechnung passt die Gewichte an?
  * Was ist die Zielgröße – wann ist genug trainiert?
  * Welche **Hyperparameter** gibt es, und worauf legen wir sie fest?

Für das Perzeptron beantworten wir sie so.

**Daten und Aufgabe.** Das Perzeptron ist ein Modell zur binären Klassifikation, also Supervised Learning. Input sind Stichproben von $(X, Y)$, wobei $X$ Werte in $\mathbb{R}^n$ hat und $Y \in \{0, 1\}$ die Klasse ist. Die Dimensionalität $n$ der Eingabedaten ist ein Hyperparameter – einer, den wir in der Regel nicht optimieren wollen, weil er von den Daten vorgegeben ist. Ziel ist die Berechnung einer Funktion $f$ mit $Y = f(X) + \varepsilon$ für einen möglichst kleinen Fehler $\varepsilon$.

**Parameter und Inferenz.** Die Parameter sind $n$ Gewichte $w_j$, zusammengefasst zu $w \in \mathbb{R}^n$, und der Bias $b$. Die Inferenz ist

$$
f(x) = [\, w \cdot x + b > 0 \,],
$$

also $f(x) = 1$ genau dann, wenn $\sum_j w_j x_j + b > 0$. Mit dem Trick $w_0 := b$, $x_0 := 1$ von oben schreiben wir im Folgenden einfach $f(x) = [\, w \cdot x > 0 \,]$ und denken uns den Bias als nulltes Gewicht.

**Training: die Perzeptronregel.** Gegeben die bisherigen Gewichte $w$ und ein einzelnes Sample $(x, y)$, setze

$$
w_{\text{neu}} := w + r \cdot (y - f(x)) \, x .
$$

Dabei ist $r > 0$ ein Hyperparameter, die **Lernrate**. Was macht diese Regel?

* Wenn $y = f(x)$, also bei korrekter Klassifikation, ist $y - f(x) = 0$ und damit $w_{\text{neu}} = w$: Nichts passiert.
* Wenn $y = 1$, aber $f(x) = 0$, so ist $w_{\text{neu}} = w + r x$. Dann ist $w_{\text{neu}} \cdot x = w \cdot x + r \, (x \cdot x)$, und weil $x \cdot x > 0$ für alle $x \neq 0$ gilt, ist die Aktivierung für dieses $x$ *gewachsen* – in Richtung der richtigen Entscheidung $f(x) = 1$.
* Wenn $y = 0$, aber $f(x) = 1$, so ist $w_{\text{neu}} = w - r x$, und die Aktivierung *sinkt* entsprechend.

Die Regel schiebt also die Trennhyperebene bei jedem Fehler ein Stück in Richtung des falsch klassifizierten Punkts. Man kann beweisen (Perzeptron-Konvergenzsatz, Novikoff 1962), dass diese Regel nach endlich vielen Fehlern eine trennende Hyperebene findet, *falls* die Daten linear trennbar sind. Falls nicht, terminiert das Verfahren nie von selbst.

**Zielgröße.** Wir messen den Erfolg als Anteil falsch klassifizierter Samples (Fehlerrate), bzw. als Anteil korrekt klassifizierter Samples (Accuracy) auf einem Testset.

**Initialisierung.** Irgendwo muss $w$ anfangen; wir initialisieren $w$ z.B. auf den Vektor $(1, 1, \dots, 1)$. Auch das ist eine Entscheidung mit Konsequenzen, wie wir später sehen werden.

:::{figure} ../images/vl02-perceptron-updates.png
:width: 90%

Die Perzeptronregel bei der Arbeit: Trenngerade $w \cdot x + b = 0$ nach 0, 1, 2 und 3 Epochen über 60 Datenpunkte, Lernrate $r = 0{,}05$.
:::

## Zurück in die Theorie: Wozu das olle Perzeptron?

Moderne neuronale Netze verwenden meist keine Perzeptrons mehr. Beliebter ist die multilineare oder logistische Regression, die ebenfalls gleich strukturierte Eingabedaten annimmt und sehr ähnlich verarbeitet: *Skalarprodukt, gefolgt von einer nichtlinearen Funktion.* Dieses Kochrezept – die gemeinsame Verallgemeinerung – heißt manchmal auch einfach „Perzeptron“.

:::{prf:definition} Verallgemeinertes Perzeptron
Das verallgemeinerte Perzeptron ist ein Regressionsmodell mit Parametern $w \in \mathbb{R}^n$ und Funktion

$$
f(x) = \tau(w \cdot x)
$$

für eine feste *Aktivierungsfunktion* $\tau \colon \mathbb{R} \to \mathbb{R}$.
:::

Die Wahl von $\tau$ bestimmt, welches bekannte Modell wir vor uns haben – und wie man es trainiert:

| Modell | $\tau(a)$ | Training |
|---|---|---|
| Lineare Regression | $\tau(a) = a$ | kleinste Quadrate |
| Perzeptron | $\tau(a) = [a > 0]$ | Perzeptronregel $w_{\text{neu}} := w + r (y - f(x)) x$ |
| „stetiges Perzeptron“ | $\tau(a) = \tanh(a)$ | ? |
| Logistische Regression | $\tau(a) = \sigma(a) = \frac{1}{1 + e^{-a}}$ | ? |

Die letzten beiden Zeilen sind stetige, sogar differenzierbare Versionen der Sprungfunktion $[a > 0]$: $\tanh$ bildet nach $(-1, 1)$ ab, die logistische Sigmoidfunktion $\sigma$ nach $(0, 1)$. Die offene Frage ist die Update-Regel: Wie trainiert man ein verallgemeinertes Perzeptron mit beliebigem $\tau$? Die Antwort – Gradientenabstieg auf einer Loss-Funktion – werden wir in den nächsten Kapiteln eingehend studieren; die Perzeptronregel wird sich dabei als Spezialfall erweisen (Blatt 3).

## Mehrere Schichten

### Warum die Perzeptronregel nicht reicht

Angenommen, $x \in \mathbb{R}^2$ und $v, w \in \mathbb{R}^2$ sind die Gewichte von zwei Perzeptrons,

$$
g(x) = [\, v \cdot x > 0 \,], \qquad f(x) = [\, w \cdot x > 0 \,],
$$

und $z := (g(x), f(x)) \in \{0,1\}^2$ ist der Ergebnisvektor der ersten Schicht. Ein drittes Perzeptron mit Gewichten $u \in \mathbb{R}^2$ berechnet daraus

$$
h(x) = [\, u \cdot z > 0 \,].
$$

Das ist ein Multilayer Perceptron mit einer versteckten Schicht. Die Perzeptronregel sagt uns, wie wir $u$ anpassen, wenn $h(x)$ falsch liegt – aber sie sagt nichts darüber, wie $v$ und $w$ angepasst werden sollten. Welches der beiden Perzeptrons in der ersten Schicht war „schuld“? Die Antwort auf diese Frage heißt **Backpropagation**, und sie funktioniert nur für differenzierbare $\tau$. Das machen wir noch.

### Warum lineare Regression keine Schichten braucht

Man könnte auf die Idee kommen, statt Perzeptrons einfach lineare Regressionen zu stapeln, die haben ja ein bekanntes Trainingsverfahren. Seien also $g(x) = v \cdot x$ und $f(x) = w \cdot x$ zwei lineare Regressionen, $z := (v \cdot x, w \cdot x)$, und $h(x) = u \cdot z$. Dann ist

$$
h(x) = u_1 (v \cdot x) + u_2 (w \cdot x)
= u_1 v_1 x_1 + u_1 v_2 x_2 + u_2 w_1 x_1 + u_2 w_2 x_2
= (u_1 v + u_2 w) \cdot x .
$$

Das ist äquivalent zu einer einzigen linearen Regression mit Gewichtsvektor $u_1 v + u_2 w$. Allgemein: Ein Produkt von Matrizen ist wieder eine Matrix, mehrere lineare Schichten hintereinander sind wieder eine lineare Schicht. Ohne die Nichtlinearität $\tau$ zwischen den Schichten bringt Tiefe gar nichts. Genau deshalb heißt $\tau$ auch *Aktivierungsfunktion* und nicht Dekoration.

## Tipps zu den Übungsblättern

### Blatt 1: Lineare Algebra und NumPy

Das erste Blatt wiederholt lineare Algebra: Skalarprodukt, Orthogonalität, Länge und Winkel, und setzt das in NumPy und Matplotlib um. Erinnern Sie sich an die Interpretation des Kosinus eines Winkels als Verhältnis von Seiten im rechtwinkligen Dreieck: Mit Ankathete $a$ und Hypotenuse $b$ ist

$$
\cos(\alpha) = \frac{a}{b}.
$$

Was passiert im Spezialfall $b = 1$? Dann ist $\cos(\alpha) = a$, d.h. der Kosinus ist die Länge der Projektion eines Einheitsvektors auf die Richtung des anderen Schenkels. Genau das steckt in der Formel

$$
\cos(\alpha) = \frac{u \cdot v}{\|u\| \, \|v\|}
$$

für den Winkel zwischen zwei Vektoren $u, v \in \mathbb{R}^n$: Das Skalarprodukt $w \cdot x$ im Perzeptron misst, „wie sehr $x$ in Richtung $w$ zeigt“.

### Blatt 2: Perzeptron in NumPy

Auf Blatt 2 implementieren Sie ein Perzeptron mit Python und NumPy und werten es aus. Eingabedaten sind $(x, y)$, wobei `x` ein zweidimensionales Array ist (eine Zeile pro Sample, eine Spalte pro Feature); Ausgabe ist die Genauigkeit auf einem Testset nach dem Training.

* Arbeiten Sie direkt mit der Perzeptronregel $w_{\text{neu}} := w + r \cdot (y - f(x)) \, x$ und lassen Sie sich nicht vom verallgemeinerten Perzeptron verwirren.
* Lernrate: $r = 0{,}01$ ist ein guter Startwert.
* Verwenden Sie dieselben Daten mehrmals im Training (mehrere *Epochen*).
* Benutzen Sie Scikit-learn: `sklearn.model_selection.train_test_split` für den Split, `sklearn.datasets.make_blobs` für gut geeignete Übungsdaten, `sklearn.datasets.load_iris` für einen echten Datensatz.
* Komplett lost, Kommilitonen ebenfalls überfordert? Bitte Bescheid sagen.
