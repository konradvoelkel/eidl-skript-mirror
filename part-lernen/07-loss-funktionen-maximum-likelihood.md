---
title: "Loss-Funktionen und Maximum Likelihood"
short_title: "Loss und Maximum Likelihood"
---

# Loss-Funktionen und Maximum Likelihood

Dieses Kapitel klärt, *was* beim Training minimiert wird und warum. Das nächste Kapitel klärt, *wie*.

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

der einfach die falsch klassifizierten Samples zählt. Die Update-Regeln zu beiden Loss-Funktionen leiten wir im [nächsten Kapitel](08-gradientenabstieg.md) her.

### Woher kommt die Kreuzentropie? Maximum Likelihood

Die logistische Regression behauptet: $P(Y = 1 \mid X = x) = p(x) := \sigma(\langle w, x \rangle)$. Für einen Datenpunkt $(x, y)$ mit $y \in \{0, 1\}$ ist die Wahrscheinlichkeit des *beobachteten* Labels unter dieser Behauptung

$$
P(Y = y \mid X = x) = \begin{cases} p(x) & y = 1 \\ 1 - p(x) & y = 0 \end{cases}
\;=\; p(x)^{y}\,\bigl(1 - p(x)\bigr)^{1 - y},
$$

wobei die kompakte Schreibweise rechts funktioniert, weil einer der beiden Exponenten $0$ ist und $a^0 = 1$. Für $N$ unabhängig gezogene Datenpunkte multiplizieren sich die Wahrscheinlichkeiten. Die **Likelihood** der Gewichte $w$ ist

$$
\mathcal{L}(w) = \prod_{i=1}^N p(x_i)^{y_i}\,\bigl(1 - p(x_i)\bigr)^{1 - y_i}.
$$

Das Prinzip der **Maximum-Likelihood-Schätzung** ([DS-Skript](https://voelkel.pages.cs.uni-duesseldorf.de/ds-skript/statistische-modelle#maximum-likelihood)): Wähle die Parameter, unter denen die beobachteten Daten am wahrscheinlichsten sind. Ein Produkt aus $N$ Faktoren zwischen $0$ und $1$ ist unhandlich und numerisch schnell $0$; der Logarithmus macht daraus eine Summe, ohne die Lage des Maximums zu ändern, denn $\ln$ ist streng monoton wachsend:

$$
\ln \mathcal{L}(w) = \sum_{i=1}^N \Bigl( y_i \ln p(x_i) + (1 - y_i) \ln\bigl(1 - p(x_i)\bigr) \Bigr).
$$

Maximieren der Log-Likelihood ist Minimieren der negativen Log-Likelihood, und die ist bis auf den Faktor $\frac1N$ genau $L_{\text{BCE}}$. Die binäre Kreuzentropie ist also keine willkürliche Wahl: Sie ist *die* Loss-Funktion, die aus „das Modell sagt Wahrscheinlichkeiten voraus, und wir glauben den Daten“ folgt. Dasselbe Argument mit Gauß-Rauschen $Y = \langle w, X \rangle + \varepsilon$, $\varepsilon \sim \mathcal{N}(0, s^2)$, liefert den MSE als Loss der linearen Regression (Übung: $\ln$ der Gauß-Dichte ist ein quadratischer Term plus Konstante).

:::{prf:example} Maximum Likelihood von Hand
Drei Münzwürfe ergeben Kopf, Kopf, Zahl. Ein Modell ohne Eingabe $x$, nur mit einem Parameter $p = P(\text{Kopf})$, hat Likelihood $\mathcal{L}(p) = p \cdot p \cdot (1 - p)$ und Log-Likelihood $2 \ln p + \ln(1 - p)$. Ableiten und null setzen:

$$
\frac{2}{p} - \frac{1}{1 - p} = 0 \iff 2(1 - p) = p \iff p = \tfrac23 .
$$

Das ist der Anteil der Köpfe, und zugleich der Wert, an dem die binäre Kreuzentropie dieser drei Datenpunkte (mit konstanter Vorhersage $p$) minimal ist. Im DS-Skript steht dieselbe Rechnung ohne Logarithmus ([Welches $p$ passt am besten zu den Daten?](https://voelkel.pages.cs.uni-duesseldorf.de/ds-skript/wichtigste-diskrete-verteilungen#welches-p-passt-am-besten-zu-den-daten)); vergleichen Sie, welche Variante angenehmer ist.
:::

## Optimieren mit Fehlerterm

Wenn $L(x, y; w) \in \mathbb{R}$ den Fehler eines Modells mit Gewichtsvektor $w$ angibt, dann suchen wir $w$, sodass $L(w) := L(x, y; w)$ minimal wird. Die Daten $x, y$ sind dabei fest, variabel ist $w$.

:::{admonition} Ableiten nach den Gewichten, nicht nach den Daten
:class: note
In der Schule wird nach $x$ abgeleitet. Hier ist $x$ eine Konstante (der Datenpunkt) und $w$ die Variable: Wir fragen, wie sich der Fehler ändert, wenn wir *am Modell* drehen, nicht an den Daten. Beides wird vorkommen, denn bei mehreren Schichten ist die Eingabe einer Schicht die Ausgabe der vorigen, und dann brauchen wir auch die Ableitung nach der *Eingabe*, um den Fehler an die vorige Schicht weiterzureichen. Beide Ableitungen desselben Ausdrucks nebeneinander:

| Ausdruck | Ableitung nach $w$ | Ableitung nach $x$ |
|---|---|---|
| $\langle w, x \rangle$ | $x$ | $w$ |
| $\sigma(\langle w, x \rangle)$ | $\sigma'(\langle w, x \rangle)\,x$ | $\sigma'(\langle w, x \rangle)\,w$ |
| $(y - \langle w, x \rangle)^2$ | $-2\,(y - \langle w, x \rangle)\,x$ | $-2\,(y - \langle w, x \rangle)\,w$ |

Die Symmetrie ist kein Zufall: $\langle w, x \rangle$ ist in beiden Argumenten linear. Für Backpropagation heißt das: Wer $\frac{\partial}{\partial w}$ kann, kann auch $\frac{\partial}{\partial x}$, man tauscht nur die Rollen. Und in der Klausur: immer dazuschreiben, *wonach* abgeleitet wird.
:::

**Exakt**, wie in der Schule: Extremstellen von $L$ bestimmen.

1. $L'$ bestimmen,
2. $L'(w) = 0$ nach $w$ umstellen,
3. Formel für $w$ ausrechnen (aus den Daten $x, y$),
4. Kandidaten für $w$ ausprobieren – liegt ein Minimum vor?

Für die lineare Regression mit MSE klappt das (die [Normalgleichungen](https://voelkel.pages.cs.uni-duesseldorf.de/ds-skript/lineare-regression#kleinste-quadrate) aus Data Science). Schaffen wir das immer? Nein: Für die logistische Regression hat $L'(w) = 0$ keine geschlossene Lösung, und für tiefe Netze erst recht nicht.

**Approximativ**, ganz dumm:

1. Zufällig ein $w$ auswählen,
2. $L(w)$ ausrechnen, vergleichen mit dem bisher niedrigsten Wert,
3. Größer? Pech gehabt, weitermachen. Kleiner? Besseres $w$ gefunden!
4. Jetzt ggf. aufhören, wenn $w$ gut genug ist.

**Approximativ, clever**: Wie eben, aber im ersten Schritt $w$ nicht zufällig, sondern *in der Nähe der bisher besten Schätzung* auswählen. Das ist eine lokale Suche, und die Frage ist nur noch, in welche Richtung man von der besten Schätzung aus gehen soll. Das ist der Gradientenabstieg, Thema des nächsten Kapitels.

:::{admonition} Obacht: Bei linear trennbaren Daten hört die logistische Regression nie auf
:class: warning
Zwei Datenpunkte in $\mathbb{R}$: $x = -1$ mit $y = 0$ und $x = +1$ mit $y = 1$, Modell $\sigma(w x)$ ohne Bias. Die BCE ist

$$
L(w) = -\ln\bigl(1 - \sigma(-w)\bigr) - \ln \sigma(w) = -2 \ln \sigma(w)
$$

(wegen $1 - \sigma(-w) = \sigma(w)$). Diese Funktion fällt streng monoton in $w$ und nähert sich $0$ für $w \to \infty$, erreicht es aber nie: Es gibt kein Minimum. Jedes Verfahren, das $L$ verkleinert, schiebt $w$ immer weiter, weil ein steileres Sigmoid (größeres $\|w\|$, siehe [Kapitel „Neuron und Perzeptron“](../part-grundlagen/02-neuron-perzeptron.md)) den Datenpunkten immer mehr Wahrscheinlichkeit gibt. In der Praxis sieht das so aus: Der Loss sinkt und sinkt, die Gewichte wachsen, die Vorhersagen werden „sicherer“, ohne dass sich die Trenngerade noch bewegt. Abhilfe: ein Strafterm für $\|w\|$ (*Regularisierung*, wie bei der Ridge-Regression im [DS-Skript](https://voelkel.pages.cs.uni-duesseldorf.de/ds-skript/lineare-regression#regularisierung); in PyTorch `weight_decay` im Optimierer) oder einfach rechtzeitig aufhören.

Umgekehrt ist das der Vorteil gegenüber dem Perzeptron: Bei *nicht* trennbaren Daten hat die BCE ein Minimum, und die logistische Regression liefert eine sinnvolle Antwort, wo die Perzeptronregel nie terminiert.
:::

## Take-Home Message

Training heißt: eine Loss-Funktion $L(w)$ in den Gewichten minimieren, die Daten sind dabei Konstanten. Die binäre Kreuzentropie ist die negative Log-Likelihood der logistischen Regression, der MSE die der linearen Regression mit Gauß-Rauschen. Exakt lösen kann man das nur in Ausnahmefällen; sonst sucht man lokal, und dafür braucht man die Richtung, in der $L$ am schnellsten fällt.
