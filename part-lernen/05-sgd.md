---
title: "VL 05: Stochastischer Gradientenabstieg"
short_title: "VL 05"
---

# Stochastischer Gradientenabstieg

:::{note} Stand
Erste Prosafassung (aus den Folien von VL 05, WiSe 2025/26). Abbildungen fehlen noch, siehe die `TODO`-Kommentare.
:::

## Training eines einzelnen Neurons: Was bisher geschah

Wir haben zwei Modelle für ein einzelnes Neuron gesehen, mit gleicher Struktur, aber sehr unterschiedlich beschriebenem Training:

| | Perzeptron | Logistische Regression |
|---|---|---|
| Inferenz | $[\langle w, x \rangle > 0] \in \{0, 1\}$ | $\sigma(\langle w, x \rangle) \in (0, 1)$ |
| Aktivierungsfunktion | „sign“ (Vorzeichen) | $\sigma$ (logistische Sigmoidfunktion) |
| Training | Update-Regel $w_{\text{neu}} = w_{\text{alt}} + \rho\,(y_{\text{true}} - f(x))\,x$ | naiv: finde $w$, sodass der MSE der linearen Regression minimal wird |

Beim Perzeptron kann jedes einzelne neue Paar $(x, y)$ zum Weiterlernen benutzt werden; bei der logistischen Regression wird ein Fehler minimiert. Zwei Fragen drängen sich auf: Wie lernt man bei der logistischen Regression aus einem *einzelnen* neuen Paar $(x, y)$ etwas dazu? Und wird beim Perzeptron eigentlich auch etwas maximiert oder minimiert?

### Neue, einheitliche Perspektive

Die Antwort auf beide Fragen: Jedes Training ist die Minimierung eines **Fehlerterms**, der **Loss-Funktion** $L(x, y; w)$, und die Update-Regel folgt aus der Loss-Funktion. Für die logistische Regression ist der passende Fehlerterm die **binäre Kreuzentropie** (binary cross entropy, BCE):

$$
L_{\text{BCE}}(x, y; w) = -\frac1N \sum_{i=1}^N \Bigl( y_i \log p_i + (1 - y_i) \log(1 - p_i) \Bigr),
\qquad
p_i = P(x_i \text{ in Klasse } 1) = \sigma(\langle w, x_i \rangle) = \frac{e^{\langle w, x_i \rangle}}{1 + e^{\langle w, x_i \rangle}} .
$$

Für das Perzeptron (mit Labels $y_i \in \{-1, +1\}$ statt $\{0, 1\}$, das macht die Formeln kürzer) ist ein Kandidat der **Perceptron Loss**

$$
L_{\text{Perc}}(x, y; w) = \sum_{i=1}^N \max\bigl(0,\, -y_i \operatorname{sign}\langle w, x_i \rangle\bigr),
$$

der einfach die falsch klassifizierten Samples zählt. Die Update-Regel dazu leiten wir weiter unten her.

## Optimieren mit Fehlerterm

Wenn $L(x, y; w) \in \mathbb{R}$ den Fehler eines Modells mit Gewichtsvektor $w$ angibt, dann suchen wir $w$, sodass $L(w) := L(x, y; w)$ minimal wird. Die Daten $x, y$ sind dabei fest, variabel ist $w$.

**Exakt**, wie in der Schule: Extremstellen von $L$ bestimmen.

1. $L'$ bestimmen,
2. $L'(w) = 0$ nach $w$ umstellen,
3. Formel für $w$ ausrechnen (aus den Daten $x, y$),
4. Kandidaten für $w$ ausprobieren – liegt ein Minimum vor?

Für die lineare Regression mit MSE klappt das (die Normalgleichungen). Schaffen wir das immer? Nein: Für die logistische Regression hat $L'(w) = 0$ keine geschlossene Lösung, und für tiefe Netze erst recht nicht.

**Approximativ**, ganz dumm:

1. Zufällig ein $w$ auswählen,
2. $L(w)$ ausrechnen, vergleichen mit dem bisher niedrigsten Wert,
3. Größer? Pech gehabt, weitermachen. Kleiner? Besseres $w$ gefunden!
4. Jetzt ggf. aufhören, wenn $w$ gut genug ist.

**Approximativ, clever**: Wie eben, aber im ersten Schritt $w$ nicht zufällig, sondern *in der Nähe der bisher besten Schätzung* auswählen. Das ist eine lokale Suche, und die Frage ist nur noch, in welche Richtung man von der besten Schätzung aus gehen soll.

## Gradienten

Wir stellen uns für den Moment vor, dass $w \in \mathbb{R}^2$ ist (also die Daten zwei Features haben). Wir stellen uns die $w$-Ebene vor und darauf ein $L(w)$-Gebirge. An jedem Punkt die Frage: Wohin sollen wir gehen, wenn wir runter wollen? Antwort: In die Richtung, wo $L(w)$ am schnellsten kleiner wird, also „nach unten“ – das heißt entlang des negativen **Gradienten** $\operatorname{grad}(L)(w) = L'(w) \in \mathbb{R}^2$.

<!-- TODO Abbildung: Loss-Gebirge über der w-Ebene mit Gradientenabstiegspfad (Folie 11, Quelle Fisseha Berhane; oder eigenes matplotlib-Contour-Plot) -->

### Gradienten konkret

Betrachten wir den MSE für eine lineare Regression:

$$
L(w) = \frac1N \sum_{i=1}^N \bigl( y_i - \langle w, x_i \rangle \bigr)^2 .
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

In welche Richtung $v$ ist die Änderung maximal? Nach Cauchy-Schwarz ist $\langle L'(w), v \rangle \le \|L'(w)\| \, \|v\|$ mit Gleichheit genau dann, wenn $v$ in Richtung $L'(w)$ zeigt. In Richtung $v = L'(w)$ ist die Änderung also maximal, $\langle L'(w), L'(w) \rangle = \|L'(w)\|^2$ – und in Richtung $-L'(w)$ minimal. Der Gradient zeigt bergauf, der negative Gradient bergab.

**Endlich ausrechnen.** Mit der Kettenregel:

$$
\frac{\partial L}{\partial w_1}(w) = \frac1N \sum_{i=1}^N 2\,(y_i - w_1 x_{i1} - w_2 x_{i2})\,(-x_{i1}),
\qquad
\frac{\partial L}{\partial w_2}(w) = \frac1N \sum_{i=1}^N 2\,(y_i - w_1 x_{i1} - w_2 x_{i2})\,(-x_{i2}).
$$

:::{prf:example} Ein Gradientenschritt von Hand
Fiktive Daten: $x_1 = (1, 0)$, $y_1 = 0$, $x_2 = (0, 1)$, $y_2 = 1$, also $N = 2$, und $w_{\text{alt}} = (1, 1)$. Dann ist (der Faktor $\frac{2}{N} = 1$ fällt weg)

$$
\begin{aligned}
\frac{\partial L}{\partial w_1}(w_{\text{alt}}) &= \sum_{i=1}^2 (y_i - x_{i1} - x_{i2})(-x_{i1}) = (0 - 1)(-1) + (1 - 1)(-0) = 1, \\
\frac{\partial L}{\partial w_2}(w_{\text{alt}}) &= \sum_{i=1}^2 (y_i - x_{i1} - x_{i2})(-x_{i2}) = (0 - 1)(-0) + (1 - 1)(-1) = 0,
\end{aligned}
$$

also $L'(w_{\text{alt}}) = (1, 0)$. Der Update-Schritt $w_{\text{neu}} := w_{\text{alt}} - \rho\, L'(w_{\text{alt}})$ mit z.B. $\rho = \tfrac12$ liefert $w_{\text{neu}} = (1, 1) - (\tfrac12, 0) = (\tfrac12, 1)$. Probe: Vorher war $\langle w, x_1 \rangle = 1$ bei $y_1 = 0$, nachher $\tfrac12$ – der Fehler auf dem ersten Sample ist gesunken, der auf dem zweiten unverändert.
:::

<!-- TODO Abbildung: Tafelbild Gradientenabstieg (from_2025/slides/tafelbild-gradientenabstieg.jpg) -->

## Gradientenabstieg

Damit haben wir die sehr clevere Variante der approximativen Minimierung:

1. Sehr clever ein $w$ auswählen, in der Nähe der bisher besten Schätzung:

   $$
   w_{\text{neu}} := w_{\text{alt}} - \rho\, L'(w_{\text{alt}}).
   $$

2. $L(w)$ ausrechnen, vergleichen mit dem bisher niedrigsten Wert,
3. Größer? Pech gehabt, weitermachen (ggf. mit kleinerem $\rho$). Kleiner? Besseres $w$ gefunden!
4. Jetzt ggf. aufhören, wenn $w$ gut genug ist.

Das ist der **Gradientenabstieg**, und $\rho$ ist die **Lernrate** – dieselbe, die wir beim Perzeptron schon hatten. Zu klein, und man braucht ewig; zu groß, und man springt über das Tal hinweg.

Wie so ein Loss-Gebirge für ein echtes neuronales Netz aussieht, zeigen z.B. Li, Xu, Taylor, Studer und Goldstein, *Visualizing the loss landscape of neural nets* (arXiv:1712.09913, 2017), oder interaktiv der [Loss Landscape Explorer](https://losslandscape.com/explorer). Die Landschaften sind nicht konvex, es gibt viele lokale Minima, Sattelpunkte und Plateaus – und trotzdem funktioniert Gradientenabstieg erstaunlich gut.

<!-- TODO Abbildungen: Loss Landscape (Li et al. 2017), Amini et al. 2018 (Folien 28–29) -->

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

### Loss-Funktionen, die wir bisher gesehen haben

Für ein einzelnes Sample mit $y = 1$, aufgetragen gegen den Wert der Entscheidungsfunktion $f(x) = \langle w, x \rangle$:

* **Perceptron Loss** $\max(0, -f(x))$: null, sobald $f(x) > 0$, davor linear.
* **Hinge Loss** $\max(0, 1 - f(x))$: null erst ab $f(x) \ge 1$, verlangt also einen *Sicherheitsabstand* (Margin) – das ist der Loss der Support Vector Machine.
* **BCE Loss** $-\log \sigma(f(x))$: glatt, wird nie exakt null, bestraft auch richtig klassifizierte Samples noch ein bisschen, wenn sie nahe an der Grenze liegen.

<!-- TODO Abbildung: die drei Loss-Kurven L(y=1, f(x)) für f(x) in [-4, 4] (Folie 34) -->

## Take-Home Message

Ein einzelnes Neuron besteht aus einer Aktivierungsfunktion $\tau$ und einem Gewichtsvektor $w$ (den Parametern). Inferenz:

$$
y_{\text{pred}} = \tau(\langle w, x \rangle).
$$

Training, mit Hyperparameter $\rho$, hängt von der Loss-Funktion $L(w)$ ab:

$$
w_{\text{neu}} = w_{\text{alt}} - \rho\, L'(w_{\text{alt}}).
$$

Für binäre Klassifikation nimmt man $\tau = \sigma$ und $L = L_{\text{BCE}}$. Das ist logistische Regression.

## Nicht-stochastischer Gradientenabstieg??

*Gradientenabstieg* ist der Oberbegriff und gleichzeitig die spezifische Bezeichnung für: den ganzen Datensatz einlesen, dabei die Loss-Funktion auswerten und den Gradienten bestimmen, damit die Gewichte anpassen, und erneut den ganzen Datensatz einlesen usw. (auch *Batch Gradient Descent*).

*Stochastischer Gradientenabstieg* (SGD) ist das Anpassen der Gewichte mit einer *Schätzung* des Gradienten aus einem Teildatensatz – meist ist ein einzelnes Sample gemeint. Das ist zufällig gewählt (die Anordnung der Daten wird als zufällig angenommen), daher stochastisch. Der geschätzte Gradient ist verrauscht, aber im Mittel korrekt, und man kommt viel häufiger zu einem Update.

Der Kompromiss ist **Mini-Batch SGD**: Eine kleine, handhabbare Menge von Samples (die *Batch Size*, z.B. 32 oder 64) wird gemeinsam verarbeitet und damit der Gradient approximiert. Das ist, was in der Praxis fast immer gemeint ist, wenn jemand „SGD“ sagt – auch `torch.optim.SGD` aus dem letzten Kapitel weiß nichts davon, wie viele Samples im Batch waren. Ein Durchlauf durch den gesamten Datensatz heißt **Epoche**.

## Ziel für nächste Woche

Verstehen können, was im [TensorFlow Playground](https://playground.tensorflow.org) geschieht: mehrere Neuronen in mehreren Schichten, trainiert mit Gradientenabstieg – wofür wir die Ableitung durch alle Schichten hindurch brauchen.

## Tipps zum Übungsblatt

* Lesen Sie das Kapitel zu Vorlesung 4 nochmal aufmerksam – da sind nützliche Hinweise zu finden, um Aufgabe 3 (Softmax vs. Sigmoid) zu lösen.
* Wenn Sie sich bei Aufgabe 1 (Ableitung von $\sigma$) schwer tun, versuchen Sie zunächst die Rechnung $\sigma(-x) = 1 - \sigma(x)$ aus Vorlesung 4 nachzuvollziehen.
