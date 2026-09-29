---
title: "Das Perzeptron trainieren"
short_title: "Perzeptron trainieren"
---

# Das Perzeptron trainieren

## Das Perzeptron trainieren

Im [letzten Kapitel](02-neuron-perzeptron.md) haben wir das Perzeptron als Modell kennengelernt: ein Gewichtsvektor $w \in \mathbb{R}^n$, ein Bias $b \in \mathbb{R}$, und die Inferenz $f(x) = [\, w \cdot x + b > 0 \,]$. Was fehlt, ist das *Lernen*. Bevor wir ein Modell implementieren, sollten wir uns ein paar Fragen stellen, die für jedes Modell in dieser Vorlesung wieder auftauchen werden:

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

also $f(x) = 1$ genau dann, wenn $\sum_j w_j x_j + b > 0$. Mit dem Trick $w_0 := b$, $x_0 := 1$ aus dem letzten Kapitel schreiben wir im Folgenden einfach $f(x) = [\, w \cdot x > 0 \,]$ und denken uns den Bias als nulltes Gewicht.

**Training: die Perzeptronregel.** Gegeben die bisherigen Gewichte $w$ und ein einzelnes Sample $(x, y)$, setze

$$
w_{\text{neu}} := w + \rho \cdot (y - f(x)) \, x .
$$

Dabei ist $\rho > 0$ ein Hyperparameter, die **Lernrate**. Was macht diese Regel?

* Wenn $y = f(x)$, also bei korrekter Klassifikation, ist $y - f(x) = 0$ und damit $w_{\text{neu}} = w$: Nichts passiert.
* Wenn $y = 1$, aber $f(x) = 0$, so ist $w_{\text{neu}} = w + \rho x$. Dann ist $w_{\text{neu}} \cdot x = w \cdot x + \rho \, (x \cdot x)$, und weil $x \cdot x > 0$ für alle $x \neq 0$ gilt, ist die Aktivierung für dieses $x$ *gewachsen* – in Richtung der richtigen Entscheidung $f(x) = 1$.
* Wenn $y = 0$, aber $f(x) = 1$, so ist $w_{\text{neu}} = w - \rho x$, und die Aktivierung *sinkt* entsprechend.

Warum funktioniert das nicht nur für einen Schritt, sondern irgendwann sicher? Für ein festes Sample $(x, y)$ mit $y = 1$, das nach $k$ Updates immer noch falsch klassifiziert ist, gilt wegen der Bilinearität des Skalarprodukts

$$
w^{(k)} \cdot x = w^{(0)} \cdot x + k\, \rho\, \|x\|^2 ,
$$

und dieser Wert wird für großes $k$ irgendwann positiv, egal wie schlecht $w^{(0)}$ war. Geometrisch: Jedes Update addiert ein Vielfaches von $x$ zu $w$, dreht $w$ also Schritt für Schritt *in Richtung* $x$ (bei $y = 0$ von $x$ weg), und die Entscheidungsgrenze, die senkrecht auf $w$ steht, dreht sich mit, bis $x$ auf der richtigen Seite liegt. Das ist die eine Rechnung, die man zu diesem Kapitel einmal selbst auf Papier gemacht haben sollte. Natürlich kann ein Update für $x$ ein anderes Sample $x'$ auf die falsche Seite schieben; dass sich das nicht endlos wiederholt, ist die Aussage des Konvergenzsatzes.

Die Regel schiebt also die Trennhyperebene bei jedem Fehler ein Stück in Richtung des falsch klassifizierten Punkts. Falls die Daten linear trennbar sind, findet sie nach endlich vielen Fehlern eine trennende Hyperebene; falls nicht, terminiert das Verfahren nie von selbst.

:::{admonition} Vertiefung: der Perzeptron-Konvergenzsatz
:class: note dropdown
(Novikoff 1962.) Seien die Label als $y_i \in \{-1, +1\}$ kodiert. Angenommen, es gibt einen Einheitsvektor $w^*$ und eine *Margin* $\gamma > 0$ mit $y_i\,(w^* \cdot x_i) \ge \gamma$ für alle $i$, und alle Datenpunkte erfüllen $\|x_i\| \le R$. Dann macht die Perzeptronregel mit Start $w^{(0)} = 0$ höchstens $R^2 / \gamma^2$ Fehler, unabhängig von der Lernrate, der Dimension $n$ und der Anzahl $N$ der Datenpunkte.

Beweisidee: Bei jedem Fehler wächst $w \cdot w^*$ um mindestens $\rho\gamma$, nach $k$ Fehlern also auf mindestens $k \rho \gamma$. Gleichzeitig wächst $\|w\|^2$ bei jedem Fehler um höchstens $\rho^2 R^2$, denn $\|w + \rho y x\|^2 = \|w\|^2 + 2 \rho y\,(w \cdot x) + \rho^2 \|x\|^2$, und der mittlere Term ist bei einem Fehler nicht positiv. Nach $k$ Fehlern ist also $\|w\| \le \rho R \sqrt{k}$. Mit Cauchy-Schwarz $w \cdot w^* \le \|w\|$ folgt $k \rho \gamma \le \rho R \sqrt{k}$, also $k \le R^2 / \gamma^2$. Das Verfahren nutzt die Margin, ohne sie zu kennen.
:::

**Zielgröße.** Wir messen den Erfolg als Anteil falsch klassifizierter Samples (Fehlerrate), bzw. als Anteil korrekt klassifizierter Samples (Accuracy) auf einem Testset.

**Initialisierung.** Irgendwo muss $w$ anfangen; wir initialisieren $w$ z.B. auf den Vektor $(1, 1, \dots, 1)$. Auch das ist eine Entscheidung mit Konsequenzen, wie wir später sehen werden.

:::{figure} ../images/vl02-perceptron-updates.png
:width: 90%

Die Perzeptronregel bei der Arbeit: Trenngerade $w \cdot x + b = 0$ nach 0, 1, 2 und 3 Epochen über 60 Datenpunkte, Lernrate $\rho = 0{,}05$.
:::

## Zurück in die Theorie: Wozu das olle Perzeptron?

Moderne neuronale Netze verwenden meist keine Perzeptrons mehr. Beliebter ist die multiple lineare oder die logistische Regression, die ebenfalls gleich strukturierte Eingabedaten annimmt und sehr ähnlich verarbeitet: *Skalarprodukt, gefolgt von einer nichtlinearen Funktion.* Dieses Kochrezept – die gemeinsame Verallgemeinerung – heißt manchmal auch einfach „Perzeptron“.

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
| Perzeptron | $\tau(a) = [a > 0]$ | Perzeptronregel $w_{\text{neu}} := w + \rho (y - f(x)) x$ |
| „stetiges Perzeptron“ | $\tau(a) = \tanh(a)$ | ? |
| Logistische Regression | $\tau(a) = \sigma(a) = \frac{1}{1 + e^{-a}}$ | ? |

Die letzten beiden Zeilen sind stetige, sogar differenzierbare Versionen der Sprungfunktion $[a > 0]$: $\tanh$ bildet nach $(-1, 1)$ ab, die logistische Sigmoidfunktion $\sigma$ nach $(0, 1)$. Die offene Frage ist die Update-Regel: Wie trainiert man ein verallgemeinertes Perzeptron mit beliebigem $\tau$? Die Antwort – Gradientenabstieg auf einer Loss-Funktion – werden wir in den nächsten Kapiteln eingehend studieren; die Perzeptronregel wird sich dabei als Spezialfall erweisen.

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

Das ist ein Multilayer Perceptron mit einer versteckten Schicht. Die Perzeptronregel sagt uns, wie wir $u$ anpassen, wenn $h(x)$ falsch liegt – aber sie sagt nichts darüber, wie $v$ und $w$ angepasst werden sollten. Welches der beiden Perzeptrons in der ersten Schicht war „schuld“? Die Antwort auf diese Frage heißt **Backpropagation**, und sie braucht ein $\tau$, das sich ableiten lässt. Die Sprungfunktion des Perzeptrons tut das nicht; ReLU dagegen wird überall benutzt, obwohl sie bei $0$ einen Knick hat (siehe [Kapitel „Aktivierungsfunktionen“](../part-lernen/11-aktivierungsfunktionen.md)). Das machen wir noch.

### Warum lineare Regression keine Schichten braucht

Man könnte auf die Idee kommen, statt Perzeptrons einfach lineare Regressionen zu stapeln, die haben ja ein bekanntes Trainingsverfahren. Seien also $g(x) = v \cdot x$ und $f(x) = w \cdot x$ zwei lineare Regressionen, $z := (v \cdot x, w \cdot x)$, und $h(x) = u \cdot z$. Dann ist

$$
h(x) = u_1 (v \cdot x) + u_2 (w \cdot x)
= u_1 v_1 x_1 + u_1 v_2 x_2 + u_2 w_1 x_1 + u_2 w_2 x_2
= (u_1 v + u_2 w) \cdot x .
$$

Das ist äquivalent zu einer einzigen linearen Regression mit Gewichtsvektor $u_1 v + u_2 w$. Allgemein: Ein Produkt von Matrizen ist wieder eine Matrix, mehrere lineare Schichten hintereinander sind wieder eine lineare Schicht. Ohne die Nichtlinearität $\tau$ zwischen den Schichten bringt Tiefe gar nichts. Genau deshalb heißt $\tau$ auch *Aktivierungsfunktion* und nicht Dekoration.

## Übung

Gegeben ein Datenpunkt $x = \binom{2}{1}$ mit Label $y = 1$ und ein Perzeptron mit
$w^{(0)} = \binom{-3}{1}$, also $w^{(0)} \cdot x = -5 < 0$: Das Perzeptron sagt $0$, richtig
wäre $1$.

1. Führen Sie einen Schritt der Perzeptronregel $w^{(1)} = w^{(0)} + \rho\,(y - f(x))\,x$ mit
   $\rho = 0{,}5$ aus.
2. Berechnen Sie $w^{(1)} \cdot x$. Um wie viel hat sich die Aktivierung geändert?
   *Tipp: Rechnen Sie die Differenz einmal allgemein mit der Bilinearität des
   Skalarprodukts aus — Sie bekommen $\rho\,\|x\|^2$, unabhängig von $w^{(0)}$.*
3. Wie viele solche Schritte braucht es mindestens, bis die Aktivierung positiv wird?

*Antwortprobe: eine ganze Zahl, ohne Iteration ausrechenbar. Machen Sie die Gegenprobe mit
einem Schritt weniger – dort muss die Aktivierung noch $\le 0$ sein, denn in
$[\,w \cdot x > 0\,]$ steht ein echtes Größerzeichen.*

:::{admonition} Weiterlesen
:class: seealso
Prince, *UDL*, Kap. 3 (Shallow neural networks) und 4 (Deep neural networks) für das Stapeln von Schichten. Das Buch ist frei verfügbar, siehe [Über dieses Skript](../README.md).
:::
