---
title: "Logistische Regression"
short_title: "Logistische Regression"
---

# Logistische Regression

Im ersten Abschnitt basteln wir eine S-förmige Kurve aus dem $\tanh$, haben aber keine Interpretation dafür. Danach bauen wir die S-Kurve von der Wahrscheinlichkeitsrechnung her auf, und dann fällt die Interpretation von selbst ab.

## Lineare Regression zur Klassifikation

Wenn wir an Regression denken, dann oft an eine Regressionsgerade in einem $x$-$y$-Plot, bei dem auf der $x$-Achse die unabhängige Variable (der *Regressor*) und auf der $y$-Achse die abhängige Variable (der *Regressand*) aufgetragen ist. Bei der Klassifikation ist der Regressand die Klasse, $y \in \{0, 1\}$.

Schauen wir uns das Schritt für Schritt an, für einen eindimensionalen Regressor $x \in \mathbb{R}$ mit zwei Klassen, deren $x$-Werte sich überlappen:

1. Im eindimensionalen Plot liegen alle Punkte der Klasse 0 auf der Höhe $y = 0$ und alle Punkte der Klasse 1 auf $y = 1$.
2. Die lineare Regression fittet eine Gerade $\hat{y} = w x + b$ durch diese Punktwolke. Die Gerade nimmt Werte in ganz $\mathbb{R}$ an, auch weit außerhalb von $[0, 1]$.
3. **Harte Klassifikation**: Wir entscheiden für Klasse 1, wenn $\hat{y} > \tfrac12$. Die Entscheidungsgrenze ist der Punkt $x^*$ mit $w x^* + b = \tfrac12$; die vorhergesagte Klasse als Funktion von $x$ ist eine Sprungfunktion.
4. Für einen zweidimensionalen Regressor $x \in \mathbb{R}^2$ wird aus der Geraden eine Regressionshyperebene über der $(x_1, x_2)$-Ebene, und die Entscheidungsgrenze $\{ w \cdot x + b = \tfrac12 \}$ ist eine Gerade in der $(x_1, x_2)$-Ebene – genau wie beim Perzeptron.

:::{figure} ../images/vl03-linreg-classification-1d.png
:width: 90%

Lineare Regression zur Klassifikation, eindimensionaler Regressor: Regressionsgerade durch die 0/1-Daten, harte Klassifikation mit Entscheidungsgrenze $x^*$, und die $\tanh$-Variante.
:::

:::{figure} ../images/vl03-linreg-classification-2d.png
:width: 90%

Zweidimensionaler Regressor: Die Entscheidungsgrenze ist eine Gerade, die Regressionsfunktion eine Ebene.
:::

### S-Förmigkeit herstellen

Die Sprungfunktion $[\hat{y} > \tfrac12]$ ist unbefriedigend: Sie ist nicht differenzierbar, und sie verrät nicht, wie *sicher* die Entscheidung ist. Anstelle von $[\hat{y} > \tfrac12]$ könnte man $[\tanh(\hat{y}) > 0]$ verwenden; $\tanh$ liegt zwischen $-1$ und $+1$. Um zwischen $0$ und $1$ zu landen, kann man z.B.

$$
\tfrac12 \left( \tanh(\hat{y}) + 1 \right)
$$

nutzen. Das liefert eine S-förmige Kurve, die glatt von 0 nach 1 übergeht. Aber: Die Interpretation einer Zahl zwischen 0 und 1 als *Wahrscheinlichkeit* ist damit noch unklar. Genau das klärt das nächste Kapitel mit der logistischen Regression.

## Wahrscheinlichkeiten und Chancen (Odds)

### Chancen für ein Bernoulli-Experiment

Angenommen, wir haben ein Bernoulli-Experiment (Münzwurf) mit Parameter $p \in (0, 1)$ – zur Vereinfachung mit $p \neq 0$ und $p \neq 1$. Die **Wahrscheinlichkeit** (probability) für Erfolg ist $P(\text{Erfolg}) = p$. Die **Chancen** (odds) für Erfolg sind $p : (1-p)$.

Beispiel: Einen Standardwürfel (D6) rollen und gucken, ob es eine 6 ist. Dann ist $P(D = 6) = \tfrac16 = p$ die Wahrscheinlichkeit, und $1 : 5 = \tfrac15$ sind die Chancen für eine 6; $5 : 1 = 5$ sind die Chancen für eine Nicht-6. Als Formel:

$$
\operatorname{odds}(D = 6) = \frac{P(D = 6)}{P(D \neq 6)} = \frac{1/6}{5/6} = \frac15 .
$$

Allgemein rechnet man von Wahrscheinlichkeiten zu Odds und zurück über

$$
\operatorname{odds}(p) = \frac{p}{1 - p}, \qquad p = \frac{\operatorname{odds}}{1 + \operatorname{odds}} .
$$

### Die Skala für Odds

Wahrscheinlichkeiten liegen immer in $[0, 1]$. Wie sieht die Skala für Odds aus?

* Wenn $p = \tfrac12$, so ist $1 - p = \tfrac12$, also $\operatorname{odds}(p) = 1$.
* Wenn $0 < p < \tfrac12$, so ist $1 > 1 - p > \tfrac12$, also $0 < \operatorname{odds}(p) = \frac{p}{1-p} < \frac{p}{1/2} = 2p < 1$. Damit ist $\operatorname{odds}(p) \in [0, 1)$.
* Wenn $1 > p > \tfrac12$, so ist $0 < 1 - p < \tfrac12$, also $1 < 2p < \operatorname{odds}(p) < \frac{1}{1-p} < \infty$. Damit ist $\operatorname{odds}(p) \in (1, \infty)$.

Die Fälle $p < \tfrac12$ und $p > \tfrac12$ sind symmetrisch, d.h. Erfolg und Misserfolg sind äquivalent – aber $\operatorname{odds}(p) \in [0, \infty)$ ist *nicht* symmetrisch: $[0, 1)$ ist beschränkt, $(1, \infty)$ ist unbeschränkt. Die Odds für eine 6 sind $\tfrac15$, die Odds für eine Nicht-6 sind $5$.

Beachte: Logarithmieren rettet die Symmetrie. Es ist

$$
\ln\left(\frac{p}{1-p}\right) = \ln(p) - \ln(1-p),
$$

und damit $\ln(1 : 5) = -\ln(5 : 1)$. Die Werte liegen in $(-\infty, +\infty)$.

### Logistic Unit

:::{prf:definition} Logit
Für $p \in (0, 1)$ ist

$$
\operatorname{logit}(p) := \ln \operatorname{odds}(p) = \ln \frac{p}{1-p} = \ln p - \ln(1 - p).
$$
:::

Schon mal irgendwo gesehen? Im Data-Science-Skript haben wir den *Informationsgehalt* (die Überraschung) eines Ereignisses mit Wahrscheinlichkeit $p$ als $-\log p$ definiert und die *Entropie* als erwartete Überraschung ([Informationsgehalt](https://voelkel.pages.cs.uni-duesseldorf.de/ds-skript/erwartungswert#informationsgehalt), [Entropie](https://voelkel.pages.cs.uni-duesseldorf.de/ds-skript/erwartungswert#entropie)). Der Logarithmus steht dort aus einem Grund, der uns noch oft nützen wird: Für unabhängige Ereignisse multiplizieren sich die Wahrscheinlichkeiten, und $\log$ macht daraus eine Summe. Zwei Überraschungen addieren sich. Ein fairer Münzwurf ist $1$ bit Überraschung, eine 6 beim Würfeln $\log_2 6 \approx 2{,}58$ bit, beides zusammen $3{,}58$ bit.

Für das Bernoulli-Experiment ist die Entropie

$$
H(p) = -p \ln p - (1 - p) \ln(1 - p),
$$

und ihre Ableitung nach $p$ ist

$$
H'(p) = -\ln p - 1 + \ln(1-p) + 1 = -\operatorname{logit}(p)
$$

(im DS-Skript: [Die binäre Entropiefunktion](https://voelkel.pages.cs.uni-duesseldorf.de/ds-skript/wichtigste-diskrete-verteilungen#die-bin-re-entropiefunktion), dort mit $\log_2$ und kleinem $h$). Interpretation: Bei Erhöhen von $p$ ist die Abnahme an Informationsgewinn durch $\operatorname{logit}(p)$ gegeben. Entropie misst man in bit ($\log_2$) oder nat ($\ln$), die Ableitung in *logit*. Zum Beispiel ist $H(0{,}5) = 1 \text{ bit} = 0{,}69 \text{ nat}$.

## Logistische Sigmoidfunktion

### Allgemeine S-Förmigkeit

Sigma $\approx$ S, Sigmoid $\approx$ S-förmig.

:::{prf:definition} Logistische Funktion
Die *allgemeine logistische Funktion* (aka allgemeine Sigmoidfunktion) mit Parametern $M, k, \mu$ ist gegeben als Funktion in $x$:

$$
S(x; M, k, \mu) = \frac{M}{1 + e^{-k(x - \mu)}} .
$$

Das *Standardsigmoid* ist

$$
\sigma(x) = S(x; M = 1, k = 1, \mu = 0) = \frac{1}{1 + e^{-x}} .
$$
:::

$M$ ist der Maximalwert (die obere Asymptote), $k$ die Steilheit, $\mu$ die Position des Wendepunkts. Bei $\sigma(w \cdot x + b)$ übernimmt $\|w\|$ die Rolle von $k$, siehe [Kapitel „Neuron und Perzeptron“](../part-grundlagen/02-neuron-perzeptron.md): Die Länge von $w$ bestimmt, wie steil die Wahrscheinlichkeit mit dem Abstand zur Entscheidungsgrenze wächst. Das Standardsigmoid steigt monoton von $0$ (für $x \to -\infty$) nach $1$ (für $x \to +\infty$) und hat bei $x = 0$ den Wert $\sigma(0) = \tfrac12$.

:::{figure} ../images/vl04-sigmoid.png
:width: 90%

Das Standardsigmoid $\sigma$, der Tangens hyperbolicus als umskaliertes Sigmoid, und die Ableitung $\sigma' = \sigma(1-\sigma)$ mit Maximum $\tfrac14$ bei $0$.
:::

### Symmetrie

Es gilt

$$
\sigma(-x) = \frac{1}{1 + e^{x}} = \frac{e^{-x}}{e^{-x} + 1} = \frac{1 + e^{-x} - 1}{1 + e^{-x}} = 1 - \sigma(x),
$$

also $\sigma(-x) = 1 - \sigma(x)$: Der Graph ist punktsymmetrisch um $(0, \tfrac12)$.

### Andere Sigmoidfunktionen: Tangens hyperbolicus

Die Parameter $M$ und $k$ sind Skalierungsfaktoren. Möchte man die Skala des Standardsigmoids von $[0, 1]$ auf z.B. $[-1, 1]$ bringen, so nimmt man $2\sigma(x) - 1$, und mit $k = 2$:

$$
2\sigma(2x) - 1 = \frac{2}{1 + e^{-2x}} - 1 = \frac{1 - e^{-2x}}{1 + e^{-2x}} = \frac{e^{x} - e^{-x}}{e^{x} + e^{-x}} = \tanh(x).
$$

Der Tangens hyperbolicus ist also nur ein umskaliertes Standardsigmoid, $\tanh(x) = 2\sigma(2x) - 1$.

### Ableitung

Wir benötigen später die Ableitung der Sigmoidfunktion. Eventuell bekannt ist $\tanh'(x) = 1 - \tanh^2(x)$. Ähnlich gilt

$$
\sigma'(x) = \sigma(x)\,\bigl(1 - \sigma(x)\bigr) = \sigma(x)\,\sigma(-x).
$$

Der Beweis mit der Quotientenregel ist Aufgabe auf Blatt 5. Bemerkenswert daran: Die Ableitung lässt sich aus dem Funktionswert berechnen, ohne $e^{-x}$ noch einmal auszuwerten – das ist beim Training praktisch.

## Sigmoid und Logit

Wir haben zwei Funktionen:

$$
\sigma \colon \mathbb{R} \to (0, 1), \qquad \operatorname{logit} \colon (0, 1) \to \mathbb{R}.
$$

Also lassen sich beide Verkettungen bilden, $\sigma \circ \operatorname{logit} \colon (0, 1) \to (0, 1)$ und $\operatorname{logit} \circ \sigma \colon \mathbb{R} \to \mathbb{R}$. Was haben die Funktionen miteinander zu tun?

Für $p \in (0, 1)$ ist

$$
\sigma(\operatorname{logit}(p)) = \frac{1}{1 + e^{-\ln\frac{p}{1-p}}} = \frac{1}{1 + \frac{1-p}{p}} = \frac{p}{p + 1 - p} = p.
$$

Für $x \in \mathbb{R}$ ist – erst $\sigma(x)$ mit $e^x$ erweitern, dann $\ln$ anwenden und $\ln(e^x) = x$ nutzen –

$$
\operatorname{logit}(\sigma(x)) = \ln \frac{\sigma(x)}{1 - \sigma(x)} = \ln \frac{\frac{e^x}{e^x + 1}}{\frac{1}{e^x + 1}} = \ln e^x = x.
$$

Wir haben gesehen: $\sigma$ und $\operatorname{logit}$ sind Inverse zueinander,

$$
\sigma \circ \operatorname{logit} = \operatorname{id}_{(0,1)}, \qquad \operatorname{logit} \circ \sigma = \operatorname{id}_{\mathbb{R}}.
$$

Darum nennt man $\sigma$ als Inverse von $\operatorname{logit}$ auch **expit**.

### Wie interpretieren wir das?

Gegeben einen Wert $x \in \mathbb{R}$ gibt $\sigma(x)$ einen Wert $p := \sigma(x) \in (0, 1)$, sodass $x = \operatorname{logit}(p)$. Jeder Wert $x$ lässt sich also als *Logit* auffassen – als logarithmierte Chance –, und $\sigma(x)$ gibt die Wahrscheinlichkeit des Bernoulli-Experiments an, zu der $x$ der Logit-Wert ist. Das ist die Interpretation, die uns im ersten Abschnitt gefehlt hat: Eine Zahl zwischen 0 und 1, die aus $\sigma$ kommt, ist eine Wahrscheinlichkeit, wenn die Eingabe ein Logit war.

## Logistische Regression

Alle Zutaten sind bereit, jetzt wird gekocht. Die lineare Regression spuckt $\hat{y}$-Werte aus, die in ganz $\mathbb{R}$ liegen. Wenn $y = 0$ und $y = 1$ zu den zwei Klassen korrespondieren, so fassen wir $\hat{y} = w \cdot x + b$ als Logit auf, und die Werte $\sigma(\hat{y})$ geben die Wahrscheinlichkeit an, in Klasse 1 zu liegen. Wenn $\sigma(\hat{y}) > \tfrac12$, so entscheiden wir für Klasse 1 – und weil $\sigma$ monoton mit $\sigma(0) = \tfrac12$ ist, ist das dasselbe wie $\hat{y} > 0$.

:::{prf:definition} Logistische Regression
Die logistische Regression ist das verallgemeinerte Perzeptron mit $\tau = \sigma$, also das Modell

$$
f(x) = \sigma(w \cdot x + b) = P(Y = 1 \mid X = x).
$$
:::

In Scikit-Learn wird in der logistischen Regression unterschieden zwischen `predict` und `predict_proba`. Wenn $\hat{y}$ der durch lineare Regression vorhergesagte Wert an einem Punkt $x$ ist, so gilt

$$
\texttt{predict\_proba}(x) = \sigma(\hat{y}), \qquad \texttt{predict}(x) = [\, \sigma(\hat{y}) > \tfrac12 \,].
$$

### Lineare Regression in PyTorch

In PyTorch macht man eine lineare Regression so:

```python
import torch
import torch.nn as nn

class LinearRegression(nn.Module):
    def __init__(self, input_dim, output_dim):
        super(LinearRegression, self).__init__()
        self.linear = nn.Linear(input_dim, output_dim)

    def forward(self, x):
        return self.linear(x)
```

Ein Modell ist eine Unterklasse von `nn.Module`; im Konstruktor werden die Bausteine mit Parametern angelegt (hier eine einzige lineare Schicht `nn.Linear`, das ist $x \mapsto Wx + b$), und `forward` beschreibt die Inferenz. Das Training:

```python
import numpy as np

x = np.linspace(0, 10, 50)                      # irgendein eindimensionaler Datensatz
y = 2.5 * x + 1.0 + np.random.normal(0, 1, 50)  # verrauschte Gerade

model = LinearRegression(1, 1)
criterion = nn.MSELoss()
optimizer = torch.optim.SGD(model.parameters(), lr=0.01)

inputs = torch.from_numpy(x.reshape(-1, 1).astype("float32")).requires_grad_()
labels = torch.from_numpy(y.reshape(-1, 1).astype("float32"))

number_of_epochs = 100
losses = np.arange(number_of_epochs, dtype="float32")

for epoch in range(number_of_epochs):
    optimizer.zero_grad()
    outputs = model(inputs)
    loss = criterion(outputs, labels)
    loss.backward()
    optimizer.step()
    losses[epoch] = loss.item()

y_pred = model(inputs).data.numpy()
```

Die fünf Zeilen in der Schleife sind *die* Trainingsschleife von PyTorch, die uns in allen weiteren Kapiteln begleitet: Gradienten auf null setzen, Vorwärtsrechnung, Loss berechnen, Gradienten rückwärts berechnen (`backward`), Parameter anpassen (`step`). Was `criterion` (die Loss-Funktion, hier der mittlere quadratische Fehler MSE) und `optimizer` (hier stochastischer Gradientenabstieg SGD mit Lernrate $0{,}01$) genau tun, klären die nächsten beiden Kapitel.

:::{figure} ../images/vl04-lin-vs-log-regression.png
:width: 90%

Dieselben 0/1-Daten, einmal mit linearer Regression (MSE-Loss) und einmal mit logistischer Regression (BCE-Loss) gefittet.
:::

### Logistische Regression in PyTorch

Für die logistische Regression ändern sich genau zwei Zeilen: Die Aktivierungsfunktion in `forward`

```python
class LogisticRegression(nn.Module):
    def __init__(self, input_dim, output_dim):
        super(LogisticRegression, self).__init__()
        self.linear = nn.Linear(input_dim, output_dim)

    def forward(self, x):
        return torch.sigmoid(self.linear(x))  # <---
```

und die Loss-Funktion:

```python
model = LogisticRegression(1, 1)
criterion = nn.BCELoss()  # <---
optimizer = torch.optim.SGD(model.parameters(), lr=0.01)
```

Der Rest der Trainingsschleife bleibt identisch. `BCELoss` ist die *binäre Kreuzentropie*: die erwartete Überraschung, wenn man mit den vorhergesagten Wahrscheinlichkeiten $(\sigma(\hat{y}), 1 - \sigma(\hat{y}))$ rechnet, die Wahrheit aber $(y, 1 - y)$ ist. Sie ist bis auf eine Konstante die Kullback-Leibler-Divergenz aus dem [DS-Skript](https://voelkel.pages.cs.uni-duesseldorf.de/ds-skript/relative-entropie) (dort $H(p \Vert r)$ geschrieben); den genauen Zusammenhang rechnen Sie auf Blatt 5 nach. Woher diese Loss-Funktion *kommt*, klärt das nächste Kapitel.

## Weg von der 2-Klassen-Gesellschaft: Softmax

### Von Bernoulli zu Multinoulli

Von binomial (2 Klassen) zu multinomial ($K$ Klassen): Anstelle eines einzelnen $\hat{y}$-Werts der linearen Regression, der uns mit $\sigma$ die Wahrscheinlichkeit für Klasse 1 angibt, benötigen wir nun einen Vektor der Länge $K$, der sich auf $1$ aufsummiert. Für $K = 2$ erwarten wir den Vektor $(\sigma(\hat{y}), 1 - \sigma(\hat{y}))$.

Wenn wir die Klasse **one-hot** kodieren, also Vektoren der Länge $K$ mit einer $1$ an Stelle $k$ und sonst Nullen als Labels verwenden, dann liefert multinomiale lineare Regression – eine Matrix $W \in \mathbb{R}^{K \times n}$ statt eines Vektors $w$ – Vorhersagevektoren $v = Wx + b \in \mathbb{R}^K$. Die Entscheidung für Klasse $k \in \{1, \dots, K\}$ fällt, wenn der Eintrag des Vektors an Index $k$ am größten ist, $\operatorname{argmax}_j v_j = k$. Gesucht ist, analog zu $\sigma$, ein „soft argmax“.

:::{prf:definition} Softmax
Die Softmax-Funktion $\operatorname{sm} \colon \mathbb{R}^K \to \Delta^K$ ist komponentenweise gegeben durch

$$
\operatorname{sm}_j(v) = \frac{e^{v_j}}{\sum_{k=1}^K e^{v_k}} .
$$

Dabei ist $\Delta^K$ die Teilmenge von $[0, 1]^K$ mit $\sum_j v_j = 1$, der *Wahrscheinlichkeitssimplex*.
:::

Man darf sich das zweistufig vorstellen: Im ersten Schritt wird der Vektor $v$ komponentenweise exponenziert (alle Einträge werden positiv, und die Reihenfolge bleibt erhalten), im zweiten Schritt wird der Vektor normiert, sodass die Summe $1$ ist. Für den Fall $K = 2$ mit $v = (x, y)$ können wir leicht einsehen, dass

$$
\operatorname{sm}_1(v) = \frac{e^x}{e^x + e^y} = \frac{1}{1 + e^{y - x}} = \sigma(x - y),
$$

Softmax verallgemeinert also tatsächlich das Sigmoid, wobei nur die *Differenz* der Logits zählt (Blatt 5). Obacht beim Vergleich mit $\sigma$: In der Softmax-Formel steht *kein* Minus im Exponenten. Das Minus in $\sigma(x) = 1/(1 + e^{-x})$ entsteht erst beim Kürzen für $K = 2$, wie eben gerechnet. Die Probe, dass $\operatorname{sm}(v)$ wirklich eine Wahrscheinlichkeitsverteilung ist: Alle Einträge sind positiv, und die Summe ist $\sum_j e^{v_j} \big/ \sum_k e^{v_k} = 1$.

:::{admonition} Obacht!
:class: warning
Nicht jedes Multiklassen-Klassifikationsproblem schreit nach dem Softmax. Softmax ist dann sinnvoll, wenn $\operatorname{argmax}$ sinnvoll wäre, also wenn sich die Klassen gegenseitig ausschließen (ein Bild zeigt *entweder* eine Katze *oder* einen Hund). Sonst – z.B. bei Tags, von denen mehrere gleichzeitig zutreffen können – nimmt man paarweise binomiale Klassifikation mit Sigmoid, ein $\sigma$ pro Klasse.
:::

:::{admonition} Obacht: $e^x$ und $\ln$ am Computer
:class: warning
In `float32` ist $e^{89}$ bereits `inf`, und $\sigma(-100) = 1/(1 + e^{100})$ wird zu $1/\texttt{inf} = 0$ gerundet. Wer dann die Kreuzentropie selbst ausschreibt, berechnet $\ln 0 = -\infty$ und $0 \cdot (-\infty) = \texttt{nan}$; der Loss ist `nan`, und ab dem nächsten Schritt sind es alle Gewichte auch. Ähnlich beim Softmax: $e^{v_j}$ läuft über, sobald ein Logit größer als etwa $88$ ist.

Abhilfe ist immer dieselbe: nie erst $e^x$ und dann $\ln$ berechnen, sondern beides algebraisch zusammenfassen. Zum Beispiel ist $\ln \sigma(z) = -\ln(1 + e^{-z})$, und für $z < 0$ schreibt man das als $z - \ln(1 + e^{z})$, dann ist der Exponent nie groß. Beim Softmax darf man von allen $v_k$ das Maximum abziehen, ohne das Ergebnis zu ändern (*log-sum-exp-Trick*). PyTorch hat das eingebaut: `nn.BCEWithLogitsLoss` und `nn.CrossEntropyLoss` nehmen die *Logits* entgegen, nicht die Wahrscheinlichkeiten, und rechnen stabil. (`nn.BCELoss` auf Wahrscheinlichkeiten fängt $\ln 0$ mit einem Trick ab, indem es den Logarithmus bei $-100$ abschneidet. Das verhindert `nan`, ist aber ein Pflaster, keine Lösung.) Für Blatt 4 heißt das: Wenn Ihr Loss `nan` wird, ist meist das die Ursache, nicht ein Fehler in Ihrer Trainingsschleife.
:::

:::{admonition} Weiterlesen
:class: seealso
Prince, *UDL*, Kap. 5 (Loss functions), dort die logistische Regression als Maximum-Likelihood-Modell; Deisenroth et al., *MML*, Kap. 6 (Probability). Beide Bücher sind frei verfügbar, siehe [Über dieses Skript](../README.md).
:::
