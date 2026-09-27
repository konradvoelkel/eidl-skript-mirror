---
title: "Gradientenabstieg"
short_title: "Gradientenabstieg"
---

# Gradientenabstieg

Im [letzten Kapitel](07-loss-funktionen-maximum-likelihood.md) blieb die Frage offen, in welche Richtung man von der bisher besten Schätzung $w$ aus gehen soll, damit die Loss-Funktion kleiner wird. Die Antwort ist der Gradient, und um ihn für verkettete Funktionen auszurechnen, brauchen wir zuerst die Kettenregel.

## Kurze Erinnerung an die Kettenregel

Für das Training werden wir Ableitungen von verketteten Funktionen brauchen, deshalb die Kettenregel in der Form, die wir benötigen: für Funktionen zwischen Vektorräumen.

Für eine Funktion $g \colon \mathbb{R}^n \to \mathbb{R}^m$ an einem Punkt $x_0$ ist die Ableitung $(Dg)(x_0)$ – eine $m \times n$-Matrix, die Jacobi-Matrix – die beste lineare Approximation, also für $x_1$ nah bei $x_0$:

$$
g(x_1) \approx g(x_0) + (Dg)(x_0)\,(x_1 - x_0).
$$

Gegeben eine weitere Funktion $f \colon \mathbb{R}^m \to \mathbb{R}^k$, ebenso

$$
f(y_1) \approx f(y_0) + (Df)(y_0)\,(y_1 - y_0).
$$

Im Spezialfall $y_0 = g(x_0)$, $y_1 = g(x_1)$ setzen wir ein:

$$
\begin{aligned}
f(g(x_1)) &\approx f(g(x_0)) + (Df)(g(x_0))\,\bigl(g(x_1) - g(x_0)\bigr) \\
&\approx f(g(x_0)) + (Df)(g(x_0))\,\bigl(g(x_0) + (Dg)(x_0)(x_1 - x_0) - g(x_0)\bigr) \\
&= f(g(x_0)) + (Df)(g(x_0))\,(Dg)(x_0)\,(x_1 - x_0).
\end{aligned}
$$

Damit ist $(Df)(g(x_0)) \cdot (Dg)(x_0)$ die beste lineare Approximation von $f \circ g$ bei $x_0$. In anderer Notation der gleiche Sachverhalt:

$$
D(f \circ g) = \bigl((Df) \circ g\bigr) \cdot Dg .
$$

Die Ableitung einer Verkettung ist das Matrixprodukt der Ableitungen, ausgewertet an den richtigen Stellen. Das ist bereits die halbe Backpropagation.

**Summe über alle Pfade.** Die Matrixform versteckt einen Fall, der beim Rechnen von Hand oft schiefgeht: Wenn eine Variable auf *mehreren Wegen* in das Ergebnis eingeht, addieren sich die Beiträge. Für $L = u \cdot v$ mit $u = g(w)$ und $v = h(w)$ ist

$$
\frac{dL}{dw} = \frac{\partial L}{\partial u}\,g'(w) + \frac{\partial L}{\partial v}\,h'(w) = v\,g'(w) + u\,h'(w).
$$

Kleinstes Beispiel: $u = w$ und $v = w$, also $L = w^2$. Wer nur einem Pfad folgt, erhält $w$; richtig ist $w + w = 2w$. In einem Netz geht jedes Gewicht der ersten Schicht über *alle* Neuronen der zweiten Schicht in den Loss ein. Backpropagation ist im Kern die Buchhaltung dieser Summe, und die Matrixmultiplikation $(Df)\,(Dg)$ erledigt sie automatisch: Ein Matrixprodukt *ist* eine Summe über Zwischenindizes.

**Numerische Probe.** Ableitungen kann man nachprüfen, ohne sie zu kennen: Für kleines $h$ ist

$$
\frac{L(w + h) - L(w)}{h} \approx L'(w).
$$

Beispiel: $L(w) = (1 - 2w)^2$, also $L'(w) = -4\,(1 - 2w)$ und $L'(1) = 4$. Nachrechnen: $L(1) = 1$, $L(1{,}01) = (1 - 2{,}02)^2 = 1{,}0404$, Differenzenquotient $0{,}0404 / 0{,}01 = 4{,}04$. Diese Probe (*gradient check*) ist der wichtigste Handgriff, wenn eine von Hand hergeleitete Ableitung oder ein selbst geschriebenes `backward` nicht stimmen will. PyTorch hat sie eingebaut: `torch.autograd.gradcheck`.

## Gradienten

Wir stellen uns für den Moment vor, dass $w \in \mathbb{R}^2$ ist (also die Daten zwei Features haben). Wir stellen uns die $w$-Ebene vor und darauf ein $L(w)$-Gebirge. An jedem Punkt die Frage: Wohin sollen wir gehen, wenn wir runter wollen? Antwort: In die Richtung, wo $L(w)$ am schnellsten kleiner wird, also „nach unten“ – das heißt entlang des negativen **Gradienten** $\operatorname{grad}(L)(w) = L'(w) \in \mathbb{R}^2$.

:::{figure} ../images/vl05-loss-landscape.png
:width: 90%

Ein (erfundenes) Loss-Gebirge über der $w$-Ebene mit zwei Gradientenabstiegspfaden von verschiedenen Startpunkten. Beide landen im selben Tal – das ist nicht immer so.
:::

### Gradienten konkret

Betrachten wir den MSE für eine lineare Regression, mit der Notation $x^{(i)}_j$ für Feature $j$ von Datenpunkt $i$ aus dem [Kapitel „Was ist Deep Learning?“](../part-grundlagen/01-was-ist-deep-learning.md):

$$
L(w) = \frac1N \sum_{i=1}^N \bigl( y_i - \langle w, x^{(i)} \rangle \bigr)^2 .
$$

Halte zunächst die Komponente $w_2$ fest und variiere $w_1$. Das gibt eine Funktion in einer Variablen, $w_1 \mapsto L(w_1, w_2)$, und ihre Ableitung gibt die Änderung von $L$ abhängig von $w_1$ an, also die Änderung in Richtung der ersten Koordinate der $w$-Ebene: „Wenn ich einen (infinitesimalen) Schritt nach Osten gehe, wie stark ändert sich $L$ dann?“ Danach $w_1$ festhalten und $w_2$ variieren: ein Schritt nach Norden.

Diese beiden Ableitungen heißen besser **partielle Ableitungen** $\frac{\partial}{\partial w_1} L(w)$ und $\frac{\partial}{\partial w_2} L(w)$, und der Gradient ist der Vektor aus beiden:

$$
L'(w) = \left( \frac{\partial L}{\partial w_1}(w),\ \frac{\partial L}{\partial w_2}(w) \right)
= \frac{\partial L}{\partial w_1}(w)\, e_1 + \frac{\partial L}{\partial w_2}(w)\, e_2 .
$$

Nicht verwechseln: die Ableitung $L'$ (eine Funktion, die jedem $w$ einen Vektor zuordnet) und $L'(w)$, der Gradientenvektor an einem Punkt $w$.

**Richtungsableitung.** Die Änderung in Richtung $e_1$ ist $\langle L'(w), e_1 \rangle = \frac{\partial L}{\partial w_1}(w)$. Die Änderung in Richtung eines beliebigen Einheitsvektors $v$ ist

$$
\langle L'(w), v \rangle = \frac{\partial L}{\partial w_1}(w)\, v_1 + \frac{\partial L}{\partial w_2}(w)\, v_2 .
$$

In welche Richtung $v$ ist die Änderung maximal? Das Skalarprodukt $\langle L'(w), v \rangle$ ist $\|L'(w)\| \cos \alpha$ mit dem Winkel $\alpha$ zwischen $v$ und dem Gradienten, und der Kosinus ist maximal $1$, wenn $v$ in Richtung $L'(w)$ zeigt, und minimal $-1$ in der Gegenrichtung. Der Gradient zeigt bergauf, der negative Gradient bergab.

:::{admonition} Vertiefung: dasselbe mit Cauchy-Schwarz
:class: note dropdown
Ohne Winkel: Nach der Cauchy-Schwarz-Ungleichung ist $\langle L'(w), v \rangle \le \|L'(w)\| \, \|v\|$ mit Gleichheit genau dann, wenn $v$ ein nichtnegatives Vielfaches von $L'(w)$ ist. Für Einheitsvektoren $v$ ist die rechte Seite $\|L'(w)\|$, und sie wird genau in Richtung $v = L'(w) / \|L'(w)\|$ erreicht. Das Argument funktioniert in jeder Dimension, auch dort, wo man sich keinen Winkel mehr vorstellen kann.
:::

**Endlich ausrechnen.** Mit der Kettenregel:

$$
\frac{\partial L}{\partial w_1}(w) = \frac1N \sum_{i=1}^N 2\,\bigl(y_i - w_1 x^{(i)}_1 - w_2 x^{(i)}_2\bigr)\,\bigl(-x^{(i)}_1\bigr),
\qquad
\frac{\partial L}{\partial w_2}(w) = \frac1N \sum_{i=1}^N 2\,\bigl(y_i - w_1 x^{(i)}_1 - w_2 x^{(i)}_2\bigr)\,\bigl(-x^{(i)}_2\bigr).
$$

:::{prf:example} Ein Gradientenschritt von Hand
Fiktive Daten: $x^{(1)} = (1, 0)$, $y_1 = 0$, $x^{(2)} = (0, 1)$, $y_2 = 1$, also $N = 2$, und $w_{\text{alt}} = (1, 1)$. Dann ist (der Faktor $\frac{2}{N} = 1$ fällt weg)

$$
\begin{aligned}
\frac{\partial L}{\partial w_1}(w_{\text{alt}}) &= \sum_{i=1}^2 \bigl(y_i - x^{(i)}_1 - x^{(i)}_2\bigr)\bigl(-x^{(i)}_1\bigr) = (0 - 1)(-1) + (1 - 1)(-0) = 1, \\
\frac{\partial L}{\partial w_2}(w_{\text{alt}}) &= \sum_{i=1}^2 \bigl(y_i - x^{(i)}_1 - x^{(i)}_2\bigr)\bigl(-x^{(i)}_2\bigr) = (0 - 1)(-0) + (1 - 1)(-1) = 0,
\end{aligned}
$$

also $L'(w_{\text{alt}}) = (1, 0)$. Der Update-Schritt $w_{\text{neu}} := w_{\text{alt}} - \rho\, L'(w_{\text{alt}})$ mit z.B. $\rho = \tfrac12$ liefert $w_{\text{neu}} = (1, 1) - (\tfrac12, 0) = (\tfrac12, 1)$. Probe: Vorher war $\langle w, x^{(1)} \rangle = 1$ bei $y_1 = 0$, nachher $\tfrac12$ – der Fehler auf dem ersten Sample ist gesunken, der auf dem zweiten unverändert. Das Minus vor dem Gradienten ist der ganze Unterschied zwischen *descent* und *ascent*: Mit Plus liefe man bergauf.
:::

:::{figure} ../images/vl05-tafelbild-gradientenabstieg.jpg
:width: 90%

Tafelbild zum Gradientenschritt von Hand (WiSe 2025/26).
:::

## Der Algorithmus

Damit haben wir die sehr clevere Variante der approximativen Minimierung:

1. Sehr clever ein $w$ auswählen, in der Nähe der bisher besten Schätzung:

   $$
   w_{\text{neu}} := w_{\text{alt}} - \rho\, L'(w_{\text{alt}}).
   $$

2. $L(w)$ ausrechnen, vergleichen mit dem bisher niedrigsten Wert,
3. Größer? Pech gehabt, weitermachen (ggf. mit kleinerem $\rho$). Kleiner? Besseres $w$ gefunden!
4. Jetzt ggf. aufhören, wenn $w$ gut genug ist.

Das ist der **Gradientenabstieg**, und $\rho$ ist die **Lernrate** – dieselbe, die wir beim Perzeptron schon hatten. Zu klein, und man braucht ewig; zu groß, und man springt über das Tal hinweg.

Wie groß „zu groß“ ist, hängt von den Daten ab, und zwar von jedem Feature einzeln. Für den MSE ist $\frac{\partial L}{\partial w_j} = \frac1N \sum_i 2\,(y_i - \langle w, x^{(i)} \rangle)\,(-x^{(i)}_j)$, also proportional zu den Werten von Feature $j$. Hat Feature 1 Werte um $1$ und Feature 2 Werte um $1000$ (Körpergröße in Metern, Einkommen in Euro), so ist die zweite Gradientenkomponente etwa tausendmal größer als die erste, und die Krümmung des Loss-Gebirges in $w_2$-Richtung ist eine Million mal größer: Das Tal ist eine lange, schmale Schlucht. Eine Lernrate, die in $w_1$-Richtung vernünftig vorankommt, springt in $w_2$-Richtung über die Schlucht hinaus; eine, die dort stabil ist, kriecht in $w_1$-Richtung.

Der einfachste Ausweg ist, alle Features vorher auf Mittelwert $0$ und Standardabweichung $1$ zu bringen (*Standardisierung*, `sklearn.preprocessing.StandardScaler`, und beim Testset mit den Werten aus dem *Trainingsset* skalieren). Dass dieselbe Idee auch *innerhalb* eines Netzes hilft (Batch Normalization, Layer Normalization) und dass Optimierer wie Adam die Lernrate pro Parameter anpassen, sehen wir in späteren Kapiteln; der Grund ist immer dieser.

Wie so ein Loss-Gebirge für ein echtes neuronales Netz aussieht, zeigen z.B. Li, Xu, Taylor, Studer und Goldstein, *Visualizing the loss landscape of neural nets* (arXiv:1712.09913, 2017). Die Landschaften sind nicht konvex, es gibt viele lokale Minima, Sattelpunkte und Plateaus – und trotzdem funktioniert Gradientenabstieg erstaunlich gut.

:::{admonition} Ausprobieren: Loss Landscape Explorer
:class: tip
[losslandscape.com/explorer](https://losslandscape.com/explorer) zeigt echte Loss-Landschaften trainierter Netze als begehbares Gelände, mit einem Gradientenabstiegspfad, den man selbst starten kann. Probieren Sie drei Lernraten: eine so kleine, dass der Pfad im ersten Hang stecken bleibt, eine mittlere, die ins Tal findet, und eine so große, dass der Pfad zwischen den Talwänden hin und her springt oder ganz herausfliegt. Was man daraus mitnimmt: Man kennt die Landschaft im echten Training nicht, man sieht nur den Loss-Wert; der Loss steigt auch mal an, ohne dass etwas kaputt ist; wenn er dauerhaft steigt oder `nan` wird, ist die Lernrate zu groß oder ein Neustart mit anderer Initialisierung fällig; und in der Praxis fängt man mit großer Lernrate an und macht sie später kleiner. Das Bild ist ein trianguliertes Gitter aus wenigen Auswertungen und hängt an den Daten, mit anderen Trainingsdaten sähe dasselbe Netz anders aus.
:::

## Zurück zum Perzeptron

Die neue Perspektive erklärt auch die Perzeptronregel. Der „harte“ Perceptron Loss $\sum_i \max(0, -y_i \operatorname{sign}\langle w, x_i \rangle)$ hat ein Problem: Ableitung?!? Die Funktion ist stückweise konstant, der Gradient ist fast überall $0$. Besser ist der „weiche“ Perceptron Loss ohne das $\operatorname{sign}$:

$$
L_{\text{Perc}}(w) = \sum_{i=1}^N \max\bigl(0,\, -y_i \langle w, x_i \rangle\bigr).
$$

Ein Summand ist $0$, wenn $x_i$ korrekt klassifiziert ist ($y_i \langle w, x_i \rangle > 0$), und sonst $-y_i \langle w, x_i \rangle > 0$, also proportional dazu, *wie weit* auf der falschen Seite $x_i$ liegt. Die (schwache) Ableitung, Blatt 3, ist

$$
L_{\text{Perc}}'(w) = \sum_{i \text{ falsch klassifiziert}} -y_i x_i ,
$$

die Summe über die falsch klassifizierten Samples. Die allgemeine Update-Regel $w_{\text{neu}} = w_{\text{alt}} - \rho\, L'(w)$ liefert für ein einzelnes $(x, y_{\text{true}})$, also $N = 1$:

$$
w_{\text{neu}} = w_{\text{alt}} \pm \rho\, x \quad \text{wenn } x \text{ falsch klassifiziert ist, sonst } w_{\text{neu}} = w_{\text{alt}}.
$$

Das ist exakt die Perzeptronregel. Rosenblatt hat also, ohne es so zu nennen, stochastischen Gradientenabstieg auf dem Perceptron Loss gemacht.

### Und zurück zur logistischen Regression

Für die BCE lohnt sich dieselbe Rechnung, denn sie hat eine Pointe. Für ein einzelnes Sample $(x, y)$ mit Logit $z = \langle w, x \rangle$ und $p = \sigma(z)$ ist

$$
L(z) = -y \ln \sigma(z) - (1 - y) \ln\bigl(1 - \sigma(z)\bigr).
$$

Mit $\sigma' = \sigma(1 - \sigma)$ und der Kettenregel:

$$
\frac{dL}{dz}
= -y\,\frac{\sigma(z)(1 - \sigma(z))}{\sigma(z)} + (1 - y)\,\frac{\sigma(z)(1 - \sigma(z))}{1 - \sigma(z)}
= -y(1 - p) + (1 - y)\,p
= p - y .
$$

Alle Logarithmen und Sigmoide heben sich gegenseitig weg; übrig bleibt der Vorhersagefehler. Mit $\frac{\partial z}{\partial w} = x$ ist der Gradient $(p - y)\,x$, und die Update-Regel lautet

$$
w_{\text{neu}} = w_{\text{alt}} - \rho\,\bigl(\sigma(\langle w_{\text{alt}}, x \rangle) - y\bigr)\,x
= w_{\text{alt}} + \rho\,\bigl(y - f(x)\bigr)\,x .
$$

Das ist buchstäblich die Perzeptronregel aus dem [Kapitel „Das Perzeptron trainieren“](../part-grundlagen/03-perzeptron-trainieren.md), nur mit $f(x) = \sigma(\langle w, x \rangle)$ statt $[\langle w, x \rangle > 0]$: Statt „falsch oder richtig“ zählt jetzt „um wie viel daneben“. Die Formel $p - y$ werden wir bei Backpropagation als Startwert der Rückwärtsrechnung wiedersehen; sie gilt genauso für Softmax mit Kreuzentropie (Blatt 5).

### Loss-Funktionen, die wir bisher gesehen haben

Für ein einzelnes Sample mit $y = 1$, aufgetragen gegen den Wert der Entscheidungsfunktion $f(x) = \langle w, x \rangle$:

* **Perceptron Loss** $\max(0, -f(x))$: null, sobald $f(x) > 0$, davor linear.
* **Hinge Loss** $\max(0, 1 - f(x))$: null erst ab $f(x) \ge 1$, verlangt also einen *Sicherheitsabstand* (Margin) – das ist der Loss der Support Vector Machine.
* **BCE Loss** $-\log \sigma(f(x))$: glatt, wird nie exakt null, bestraft auch richtig klassifizierte Samples noch ein bisschen, wenn sie nahe an der Grenze liegen.

:::{figure} ../images/vl05-loss-curves.png
:width: 90%

Drei Loss-Funktionen für ein Sample der Klasse $y = 1$ in Abhängigkeit vom Wert der Entscheidungsfunktion $f(x)$.
:::

## Take-Home Message

Ein einzelnes Neuron besteht aus einer Aktivierungsfunktion $\tau$ und einem Gewichtsvektor $w$ (den Parametern). Inferenz:

$$
y_{\text{pred}} = \tau(\langle w, x \rangle).
$$

Training, mit Hyperparameter $\rho$, hängt von der Loss-Funktion $L(w)$ ab:

$$
w_{\text{neu}} = w_{\text{alt}} - \rho\, L'(w_{\text{alt}}).
$$

Für binäre Klassifikation nimmt man $\tau = \sigma$ und $L = L_{\text{BCE}}$. Das ist logistische Regression. In echt kennt man die Landschaft nicht und muss die Lernrate ausprobieren.

## Nicht-stochastischer Gradientenabstieg??

*Gradientenabstieg* ist der Oberbegriff und gleichzeitig die spezifische Bezeichnung für: den ganzen Datensatz einlesen, dabei die Loss-Funktion auswerten und den Gradienten bestimmen, damit die Gewichte anpassen, und erneut den ganzen Datensatz einlesen usw. (auch *Batch Gradient Descent*).

*Stochastischer Gradientenabstieg* (SGD) ist das Anpassen der Gewichte mit einer *Schätzung* des Gradienten aus einem Teildatensatz – meist ist ein einzelnes Sample gemeint. Das ist zufällig gewählt (die Anordnung der Daten wird als zufällig angenommen), daher stochastisch. Der geschätzte Gradient ist verrauscht, aber im Mittel korrekt, und man kommt viel häufiger zu einem Update.

Was „im Mittel korrekt“ genau heißt: Der Loss $L(w) = \frac1N \sum_{i=1}^N \ell(x_i, y_i; w)$ ist ein Stichprobenmittel, also eine Schätzung des Erwartungswerts $\mathbb{E}\bigl[\ell(X, Y; w)\bigr]$ über die erzeugende Verteilung aus dem [Kapitel „Was ist Deep Learning?“](../part-grundlagen/01-was-ist-deep-learning.md). *Das* ist die Größe, die wir eigentlich klein haben wollen, denn sie misst den Fehler auf neuen Daten. Der Gradient eines Mini-Batches ist ebenfalls ein Stichprobenmittel; weil der Erwartungswert linear ist, ist sein Erwartungswert der Gradient des vollen Loss. Nach dem Gesetz der großen Zahlen ([DS-Skript](https://voelkel.pages.cs.uni-duesseldorf.de/ds-skript/erwartungswert#erwartungswert-diskret)) liegt das Mittel über viele Batches nahe daran, auch wenn jeder einzelne Batch danebenliegt.

Wo steckt in diesem Verfahren überall Zufall? Im Startvektor, in den Daten, die wir als Stichprobe einer Verteilung modellieren, und in der Reihenfolge, in der die Samples verarbeitet werden. Deshalb liefern zwei Trainingsläufe mit denselben Daten verschiedene Gewichte, und ein Schritt lässt sich nicht sinnvoll rückgängig machen; man kann nur neu starten.

Der Kompromiss ist **Mini-Batch SGD**: Eine kleine, handhabbare Menge von Samples (die *Batch Size*, z.B. 32 oder 64) wird gemeinsam verarbeitet und damit der Gradient approximiert. Das ist, was in der Praxis fast immer gemeint ist, wenn jemand „SGD“ sagt – auch `torch.optim.SGD` aus dem [Kapitel „Logistische Regression“](06-logistische-regression.md) weiß nichts davon, wie viele Samples im Batch waren. Ein Durchlauf durch den gesamten Datensatz heißt **Epoche**.

## Übung

Sei $x = (2, -1)$ fest und $L(w) := (1 - w \cdot x)^2$.

1. Bestimmen Sie $\frac{\partial L}{\partial w_1}$ und $\frac{\partial L}{\partial w_2}$
   mit der Kettenregel.
   *Tipp: Äußere Funktion $u \mapsto u^2$, innere $w \mapsto 1 - w\cdot x$. Die Ableitung
   von $w \cdot x$ nach $w_j$ ist $x_j$ — mehr steckt nicht dahinter.*
2. Werten Sie den Gradienten bei $w = (0,0)$ aus und führen Sie einen Schritt mit
   Lernrate $\rho = 0{,}1$ aus.
3. Berechnen Sie $L$ vor und nach dem Schritt.

*Antwortprobe: $L$ muss kleiner geworden sein.*

:::{admonition} Weiterlesen
:class: seealso
Prince, *UDL*, Kap. 6 (Fitting models: Gradientenabstieg, SGD, Lernrate); Deisenroth et al., *MML*, Kap. 5 (Vector calculus) und 7 (Continuous optimization). Beide Bücher sind frei verfügbar, siehe [Über dieses Skript](../README.md).
:::
