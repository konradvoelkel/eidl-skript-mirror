---
title: "Universelle Approximation"
description: "Das universelle Approximationstheorem, in fünf Schritten bewiesen und im Widget gezeigt. Warum Approximieren nicht Generalisieren heißt: Double Descent."
short_title: "Universalität"
---

# Universelle Approximation

## Universelle Approximation

### Warum neuronale Netze funktionieren

**Universelles Approximationstheorem, grobe Aussage** (wir erinnern uns an das [Kapitel „Netze von Hand bauen“](12-netze-von-hand.md)): Mit neuronalen Netzen (beliebig viele Neuronen, beliebig viele Layer, fully connected, ReLU) lässt sich jede Funktion beliebig gut approximieren. Der Beweis in fünf Schritten:

1. Jede beschränkte messbare Funktion $f \colon E \subseteq \mathbb{R} \to \mathbb{R}$ ist beliebig gut ($\forall \varepsilon > 0$) durch *einfache Funktionen* $g, h$ approximierbar: $g \le f \le h$ und $0 \le h - g < \varepsilon$. Dabei sind einfache Funktionen endliche Linearkombinationen von Indikatorfunktionen messbarer Mengen. (Stetige Funktionen sind integrierbar, integrierbare Funktionen sind messbar.)
2. Eine Funktion $f \colon E \to \mathbb{R}$ (für $E$ messbar) ist messbar genau dann, wenn es eine Folge einfacher Funktionen $f_n$ gibt, die punktweise gegen $f$ konvergieren und $|f_n| \le |f|$ erfüllen. Eine messbare Funktion ist integrierbar, wenn es eine dominierende integrierbare Funktion $h$ gibt, $|f| \le |h|$. Wir können also sagen:

   ```{math}
   :enumerated: false
   \{\text{messbare Funktionen}\} \approx \{\text{interessante Funktionen}\}.
   ```

3. Jede einfache Funktion ist beliebig genau approximierbar durch *Stufenfunktionen*, d.h. endliche Linearkombinationen von Indikatorfunktionen von Intervallen. Also:

   ```{math}
   :enumerated: false
   \{\text{messbare Funktionen}\} \approx \{\text{approximierbar mit Stufenfunktionen}\}.
   ```

4. Eine einzelne Stufe lässt sich mit einem einfachen neuronalen Netz realisieren: Zwei Neuronen mit sehr steilen Sigmoiden an den Intervallgrenzen, mit Gewichten $+h$ und $-h$ in der Ausgabeschicht, ergeben eine Stufe der Höhe $h$ auf dem Intervall (Grafik von Michael Nielsen, Kapitel 4 seines Buchs). Mit ReLUs statt Sigmoiden reichen zwei Neuronen dafür **nicht**: $a\operatorname{ReLU}(x-p) + b\operatorname{ReLU}(x-q)$ ist rechts von beiden Knicken affin mit Steigung $a+b$ und kommt nie auf null zurück – man bekommt eine Rampe mit Plateau, keinen Buckel. Für ein Dreieck über dem Intervall braucht man drei ReLUs, für ein Trapez mit flachem Dach vier.
5. Die leicht zu verstehende Konstruktion mit 2 Hidden Layers bei Michael Nielsen funktioniert auch mit beliebig hoher Ein- und Ausgabedimension, also zur Approximation von Funktionen $\mathbb{R}^n \to \mathbb{R}^n$. Es gibt auch Konstruktionen mit nur 1 Hidden Layer.

Die richtige Frage ist also nie „Geht das mit neuronalen Netzen?“ (Antwort: JA), sondern „*Wie* geht das am *effizientesten* mit neuronalen Netzen?“

:::{figure} ../images/vl11-step-from-sigmoids.png
:width: 90%

Zwei steile Sigmoide mit entgegengesetzten Ausgabegewichten ergeben eine Stufe. Aus Stufen baut man Stufenfunktionen, aus Stufenfunktionen approximiert man alles Messbare.
:::

:::{anywidget} ../widgets/stufe.mjs
{n1: [20, -4, 1], n2: [20, -14, 1]}
:::

### Präzisere Ergebnisse

:::{prf:theorem} Universelle Approximation (Pinkus / Kidger–Lyons)
Sei $E \subseteq \mathbb{R}^d$ eine kompakte (d.h. beschränkte und abgeschlossene) Teilmenge. Sei $\sigma \colon \mathbb{R} \to \mathbb{R}$ eine beliebige stetige Funktion, aber keine affin-lineare Abbildung, die in wenigstens einem Punkt stetig differenzierbar mit Ableitung ungleich $0$ ist. Dann gibt es zu jeder stetigen Funktion $f \colon E \to \mathbb{R}^D$ und jedem $\varepsilon > 0$ ein neuronales Netz $n$ mit Aktivierungen $\sigma$ und endlich vielen hidden Layers, je höchstens $d + D + 2$ groß, mit

$$
\sup_{x \in E} \| n(x) - f(x) \| < \varepsilon .
$$
:::

Also: schmale, aber tiefe Netze reichen. Und noch präziser, mit Aussage über die *Größe*:

:::{prf:theorem} Yarotsky (2017)
Es gibt eine Konstante $c$, sodass gilt: Zu jeder $k$-fach stetig differenzierbaren Funktion $f \colon E \to \mathbb{R}^D$ und jedem $\varepsilon > 0$ gibt es ein neuronales Netz $n$ mit ReLU-Aktivierungen und $c \log(1/\varepsilon)$ vielen hidden Layers, insgesamt etwa $c\, \varepsilon^{-d/k}$ Gewichten und $\sup_{x \in E} \| n(x) - f(x) \| < \varepsilon$.
:::

Der Satz steht in Yarotsky, [*Error bounds for approximations with deep ReLU networks*](https://hdl.handle.net/10.1016/j.neunet.2017.07.002) (Neural Networks 2017). Siehe auch Andreas Thom, *Approximation of functions by neural networks* ([arXiv:1901.10267](https://arxiv.org/abs/1901.10267), 2019). Die Anzahl der Gewichte wächst mit der Eingabedimension $d$ exponentiell (der Fluch der Dimensionalität), aber glattere Funktionen (größeres $k$) brauchen weniger – und die Tiefe wächst nur logarithmisch in der Genauigkeit.

### Neuronale Netze vs. Bäume und Wälder

Umgekehrt lässt sich jedes ReLU-Netz auch als Entscheidungsbaum schreiben: Jedes ReLU-Neuron ist eine Ja/Nein-Entscheidung „$\langle w, x \rangle + b > 0$?“, und die Regionen, in denen alle Entscheidungen feststehen, sind genau die Stücke, auf denen das Netz linear ist (Caglar Aytekin, *Neural Networks are Decision Trees*, [arXiv:2210.05189](https://arxiv.org/abs/2210.05189), 2022). Der Baum ist allerdings exponentiell groß.

## Approximieren heißt nicht generalisieren

Die Sätze oben sagen: Ein ausreichend großes Netz *kann* jede Funktion darstellen. Sie sagen nichts darüber, ob das Training die *richtige* findet. Ein Netz mit mehr Parametern als Trainingsbeispielen kann insbesondere jeden Trainingsdatensatz exakt treffen, samt Rauschen. Nach der Lehre aus dem Data-Science-Skript müsste es dann hoffnungslos overfitten. Moderne Netze haben aber oft viel mehr Parameter als Trainingsbeispiele und generalisieren trotzdem gut. Wie passt das zusammen?

Ein Teil der Antwort ist ein Phänomen namens **Double Descent**, und es lässt sich schon an der polynomialen Regression vollständig verstehen, ganz ohne neuronales Netz.

### Die klassische U-Kurve

Wir nehmen $n = 15$ Punkte $x_i$ gleichverteilt aus $[-1, 1]$ und $y_i = \sin(\pi x_i) + \varepsilon_i$ mit normalverteiltem Rauschen, $\sigma = 0{,}2$. Als Merkmale nehmen wir die ersten $p$ Legendre-Polynome $P_0, \dots, P_{p-1}$ – das sind Polynome vom Grad $0$ bis $p - 1$, die auf $[-1, 1]$ zueinander orthogonal sind; dieselben Funktionen wie bei der [polynomialen Regression im Data-Science-Skript](https://voelkel.pages.cs.uni-duesseldorf.de/ds-skript/lineare-regression#lineare-regression), nur in einer numerisch gutmütigeren Basis. Mit der Designmatrix $A \in \mathbb{R}^{n \times p}$, $A_{ik} = P_k(x_i)$, suchen wir Gewichte $w$ mit $Aw \approx y$ im Sinne kleinster Quadrate.

Gemessen wird der **Testfehler**: der mittlere quadratische Abstand der gelernten Funktion zur wahren Funktion $\sin(\pi x)$ auf ganz $[-1, 1]$. Weil das von den gezogenen Punkten abhängt, wiederholen wir das Ganze für 200 Datensätze und nehmen den Median. Für $p \le n$ sieht man das Bekannte (linke Hälfte der Abbildung): Bei $p = 4$ ist der Testfehler mit $0{,}018$ am kleinsten, danach steigt er, während der Trainingsfehler weiter fällt. Das ist die klassische U-Kurve des Overfittens.

:::{figure} ../images/vl11-double-descent.png
:width: 100%

Links: Trainings- und Testfehler der polynomialen Regression über der Zahl der Merkmale, logarithmisch auf beiden Achsen. Bis $p = n$ die klassische U-Kurve, an der Interpolationsschwelle $p = n$ eine Spitze, dahinter ein zweiter Abstieg – wie tief, hängt von der Basis ab. Rechts: drei Lösungen für denselben Datensatz.
:::

### Die Spitze an der Interpolationsschwelle

Bei $p = n$ ist $A$ quadratisch und (mit Wahrscheinlichkeit $1$) invertierbar. Es gibt dann **genau ein** Polynom vom Grad $n - 1$, das alle Punkte trifft, Rauschen inklusive. Der Trainingsfehler ist null, der Testfehler liegt im Median bei etwa $10^9$.

Der Grund ist lineare Algebra: Die Lösung $w = A^{-1} y$ ist nur so gutartig wie $A^{-1}$. Für unseren ersten Datensatz ist der größte Singulärwert von $A$ etwa $4{,}4$, der kleinste etwa $2{,}5 \cdot 10^{-6}$. Ein Rauschanteil in Richtung des kleinsten Singulärwerts wird also mit $4 \cdot 10^5$ multipliziert. Das Polynom muss durch alle Punkte und schlägt dazwischen wild aus (rote Kurve rechts). Kurz vor und kurz nach $p = n$ ist der Testfehler immer noch riesig (Median $2{,}6 \cdot 10^6$ bei $p = 14$, $10^7$ bei $p = 16$), weil $A$ dort zwar nicht mehr quadratisch, aber immer noch fast singulär ist.

### Der zweite Abstieg

Für $p > n$ hat das Gleichungssystem $Aw = y$ **unendlich viele** Lösungen: Mit einer Lösung $w$ ist auch $w + v$ eine, für jedes $v$ im Kern von $A$ (d.h. $Av = 0$). Alle treffen die Trainingspunkte exakt; wir müssen also *wählen*. Die übliche Wahl ist die Lösung mit **minimaler Norm** $\|w\|$, die die Pseudoinverse liefert, $w^+ = A^+ y$. Sie ist auch der Grenzwert der Ridge-Regression für verschwindende Regularisierung ([Regularisierung im Data-Science-Skript](https://voelkel.pages.cs.uni-duesseldorf.de/ds-skript/lineare-regression#regularisierung)).

Mit dieser Wahl fällt der Testfehler hinter der Spitze wieder: bei $p = 100$ auf $0{,}091$. Das ist der zweite Abstieg. Aber Vorsicht, die Abbildung zeigt zwei Dinge, die man gern unterschlägt:

1. **Ob und wie tief es abwärts geht, hängt von der Basis ab.** Die orange Kurve verwendet dieselben Polynome, nur anders skaliert: $Q_k = \sqrt{2k+1}\, P_k$, sodass alle $Q_k$ im quadratischen Mittel über $[-1, 1]$ die Länge $1$ haben. Für $p \le n$ ist das egal – die Lösung ist eindeutig, und beide Kurven liegen exakt übereinander. Für $p > n$ wählt „minimale Norm“ in den beiden Basen verschiedene Interpolanten. Schreibt man dieselbe Funktion als $\sum_k a_k P_k = \sum_k b_k Q_k$, so ist $a_k = \sqrt{2k+1}\, b_k$, also

   $$
   \|a\|^2 = \sum_k (2k+1)\, b_k^2 .
   $$

   Minimale Norm in der unnormierten Basis bestraft den Grad $k$ also mit dem Gewicht $2k+1$: hohe Grade kosten mehr, und die Lösung wird glatter. Ergebnis bei $p = 100$: $0{,}091$ unnormiert gegen $0{,}43$ orthonormiert. Der zweite Abstieg ist keine Magie, sondern eine **implizite Regularisierung**, versteckt in der Frage, welche Norm man minimiert.
2. **Er muss das klassische Minimum nicht schlagen.** Hier bleibt der zweite Abstieg mit $0{,}091$ deutlich über dem klassischen Optimum $0{,}018$. Die blaue Kurve rechts zeigt, warum: Sie folgt im Großen der Sinuskurve, trifft aber jeden verrauschten Punkt mit einer schmalen Zacke. Bei tiefen Netzen liegt das zweite Minimum dagegen oft *unter* dem ersten – deshalb ist das Phänomen dort so bedeutsam.

### Wer wählt die Lösung? Der Gradientenabstieg

Niemand trainiert ein neuronales Netz mit einer Pseudoinversen. Wer wählt dort unter den vielen Interpolanten aus? Für die kleinsten Quadrate lässt sich das genau beantworten:

:::{prf:proposition} Gradientenabstieg findet die Lösung minimaler Norm
Sei $A \in \mathbb{R}^{n \times p}$ mit $p > n$ und vollem Rang $n$, und $L(w) = \frac{1}{2}\|Aw - y\|^2$. Startet der Gradientenabstieg bei $w_0 = 0$ und konvergiert er gegen eine Lösung von $Aw = y$, dann ist diese Lösung $w^+ = A^+ y$, die mit minimaler Norm.
:::

*Beweis.* Der Gradient ist $\nabla L(w) = A^\top (Aw - y)$, liegt also immer im Bild von $A^\top$, dem von den Zeilen von $A$ aufgespannten Raum $R$. Mit $w_0 = 0$ liegen deshalb alle Iterierten $w_t$ in $R$, und weil $R$ ein Untervektorraum ist, auch ihr Grenzwert $w_\infty$.

$R$ steht senkrecht auf dem Kern $K$ von $A$: Für $Av = 0$ ist $\langle A^\top u, v \rangle = \langle u, Av \rangle = 0$. Aus Dimensionsgründen ($\dim R = n$, $\dim K = p - n$) lässt sich jeder Vektor eindeutig als Summe eines Vektors in $R$ und eines in $K$ schreiben. Jede Lösung von $Aw = y$ hat also die Form $w_\infty + v$ mit $v \in K$, und nach Pythagoras ist $\|w_\infty + v\|^2 = \|w_\infty\|^2 + \|v\|^2$. Die kleinste Norm hat die Lösung mit $v = 0$, also $w_\infty$. $\square$

Die **Initialisierung** entscheidet also mit darüber, wie gut das Ergebnis generalisiert: Ein Start bei $w_0 \ne 0$ landet bei $w^+$ plus dem Anteil von $w_0$, der im Kern liegt. Und die **Parametrisierung** entscheidet mit, wie Punkt 1 oben zeigt: Dieselbe Funktionenklasse in einer anderen Basis führt zu einer anderen Lösung.

### Und bei tiefen Netzen?

Belkin, Hsu, Ma und Mandal haben 2019 in [*Reconciling modern machine-learning practice and the classical bias–variance trade-off*](https://arxiv.org/abs/1812.11118) (PNAS) gezeigt, dass dieselbe Kurve bei Random-Feature-Modellen und neuronalen Netzen auftritt, und den Namen *Double Descent* geprägt. Nakkiran et al. haben sie im selben Jahr in [*Deep Double Descent*](https://arxiv.org/abs/1912.02292) (ICLR 2020) bei CNNs, ResNets und Transformern nachgemessen. Die Kurve zeigt sich dort in drei Formen: über der **Breite** des Netzes, über der **Zahl der Epochen** und – verblüffend – über der **Zahl der Trainingsbeispiele**. In der Nähe der Interpolationsschwelle können mehr Daten das Ergebnis also verschlechtern.

Das Bild aus der polynomialen Regression überträgt sich: Spitze an der Interpolationsschwelle, dahinter entscheidet eine implizite Regularisierung, welche der vielen Interpolanten gewählt wird. Bei einem tiefen Netz ist das aber kein einzelner Satz mehr, sondern das Zusammenspiel von Architektur, Initialisierung und Optimierer, und welche Lösung es genau bevorzugt, ist Gegenstand aktueller Forschung. Die universelle Approximation sagt, dass das Netz die richtige Funktion darstellen *kann*. Dass es sie unter den vielen, die die Trainingsdaten treffen, auch *findet*, ist eine zweite, schwerere Frage.

## Übung

1. Geben Sie zwei Neuronen mit steilen **Sigmoiden** und Ausgabegewichte an, deren Summe
   die Funktion $f(x) = 1$ für $x \in [1,2]$ und $0$ sonst **näherungsweise** darstellt.
   *Tipp: Zwei steile Stufen an den Stellen $1$ und $2$, die zweite mit umgekehrtem
   Vorzeichen. Der Steilheitsparameter $h$ bestimmt, wie gut die Näherung ist.*
2. Mit **ReLUs** statt Sigmoiden reichen zwei Neuronen nicht. Wie viele brauchen Sie für
   ein Dreieck über $[1,2]$, wie viele für ein Trapez mit flachem Dach?
   *Tipp: Sehen Sie sich an, welche Steigung die Summe rechts von allen Knicken hat, und
   was sie sein müsste, damit die Funktion wieder auf $0$ zurückkommt.*
3. Zwei Trainingspunkte, $(x, y) = (-1, 0)$ und $(1, 2)$, und drei Merkmale $1, x, x^2$:
   Gesucht ist $f(x) = w_0 + w_1 x + w_2 x^2$ durch beide Punkte. Bestimmen Sie alle
   Lösungen $w = (w_0, w_1, w_2)$ und darunter die mit minimaler Norm $\|w\|$. Ist es die
   Gerade durch die beiden Punkte?
   *Tipp: Zwei Gleichungen, drei Unbekannte – die Lösungen bilden eine Gerade im
   $\mathbb{R}^3$, und ihre Richtung ist der Kern der Designmatrix. Die Lösung minimaler
   Norm steht senkrecht auf dieser Richtung.*

*Antwortprobe: Die beiden Zahlen in (2) unterscheiden sich um genau eins. In (3) ist
$\|w\|^2 = 3/2$ für die Lösung minimaler Norm und $\|w\|^2 = 2$ für die Gerade.*

:::{admonition} Weiterlesen
:class: seealso
Prince, [*UDL*](https://udlbook.github.io/udlbook/), Kap. 3 (Universal approximation theorem), Kap. 4 (Depth vs. width), Kap. 8 (Measuring performance, dort auch Double Descent) und Kap. 20 (Why does deep learning work?). Das Buch ist frei verfügbar, siehe [Über dieses Skript](../README.md).

**Im Kapitel zitiert:**

* Yarotsky: [*Error bounds for approximations with deep ReLU networks*](https://hdl.handle.net/10.1016/j.neunet.2017.07.002), Neural Networks 2017; frei: [arXiv:1610.01145](https://arxiv.org/abs/1610.01145).
* Thom: [*Approximation of functions by neural networks*](https://arxiv.org/abs/1901.10267), 2019.
* Aytekin: [*Neural Networks are Decision Trees*](https://arxiv.org/abs/2210.05189), 2022.
* Belkin, Hsu, Ma, Mandal: [*Reconciling modern machine-learning practice and the classical bias–variance trade-off*](https://arxiv.org/abs/1812.11118), PNAS 2019.
* Nakkiran, Kaplun, Bansal, Yang, Barak, Sutskever: [*Deep Double Descent: Where Bigger Models and More Data Hurt*](https://arxiv.org/abs/1912.02292), ICLR 2020.
:::
