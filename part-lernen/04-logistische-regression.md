---
title: "VL 04: Logistische Regression"
short_title: "VL 04"
---

# Logistische Regression

:::{note} Stand
Erste Prosafassung (aus den Folien von VL 04, WiSe 2025/26). Abbildungen fehlen noch, siehe die `TODO`-Kommentare.
:::

Am Ende des letzten Kapitels hatten wir eine S-förmige Kurve aus dem $\tanh$ gebastelt, aber keine Interpretation dafür. In diesem Kapitel bauen wir die S-Kurve von der Wahrscheinlichkeitsrechnung her auf, und dann fällt die Interpretation von selbst ab.

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

Schon mal irgendwo gesehen? Die Entropie des Bernoulli-Experiments ist

$$
H(p) = -p \ln p - (1 - p) \ln(1 - p),
$$

und ihre Ableitung nach $p$ ist

$$
H'(p) = -\ln p - 1 + \ln(1-p) + 1 = -\operatorname{logit}(p).
$$

Interpretation: Bei Erhöhen von $p$ ist die Abnahme an Informationsgewinn durch $\operatorname{logit}(p)$ gegeben. Entropie misst man in bit (Logarithmus zur Basis 2) oder nat (natürlicher Logarithmus), die Ableitung in *logit*. Zum Beispiel ist $H(0{,}5) = 1 \text{ bit} = 0{,}69 \text{ nat}$.

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

$M$ ist der Maximalwert (die obere Asymptote), $k$ die Steilheit, $\mu$ die Position des Wendepunkts. Das Standardsigmoid steigt monoton von $0$ (für $x \to -\infty$) nach $1$ (für $x \to +\infty$) und hat bei $x = 0$ den Wert $\sigma(0) = \tfrac12$.

<!-- TODO Abbildung: Plot von σ(x) auf [-6, 6] -->

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

Gegeben einen Wert $x \in \mathbb{R}$ gibt $\sigma(x)$ einen Wert $p := \sigma(x) \in (0, 1)$, sodass $x = \operatorname{logit}(p)$. Jeder Wert $x$ lässt sich also als *Logit* auffassen – als logarithmierte Chance –, und $\sigma(x)$ gibt die Wahrscheinlichkeit des Bernoulli-Experiments an, zu der $x$ der Logit-Wert ist. Das ist die Interpretation, die uns im letzten Kapitel gefehlt hat: Eine Zahl zwischen 0 und 1, die aus $\sigma$ kommt, ist eine Wahrscheinlichkeit, wenn die Eingabe ein Logit war.

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

<!-- TODO Abbildung: Ergebnis der linearen Regression (Folie 44) -->

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

Der Rest der Trainingsschleife bleibt identisch. `BCELoss` ist die *binäre Kreuzentropie*, die wir in Blatt 5 mit der Kullback-Leibler-Divergenz in Verbindung bringen: Sie misst, wie weit die vorhergesagte Verteilung $(\sigma(\hat{y}), 1 - \sigma(\hat{y}))$ von der wahren Verteilung $(y, 1 - y)$ entfernt ist.

<!-- TODO Abbildung: Ergebnis der logistischen Regression, S-Kurve durch die 0/1-Daten (Folie 47) -->

## Weg von der 2-Klassen-Gesellschaft: Softmax

### Bernoulli → Multinoulli

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

Softmax verallgemeinert also tatsächlich das Sigmoid, wobei nur die *Differenz* der Logits zählt (Blatt 5).

:::{admonition} Obacht!
:class: warning
Nicht jedes Multiklassen-Klassifikationsproblem schreit nach dem Softmax. Softmax ist dann sinnvoll, wenn $\operatorname{argmax}$ sinnvoll wäre, also wenn sich die Klassen gegenseitig ausschließen (ein Bild zeigt *entweder* eine Katze *oder* einen Hund). Sonst – z.B. bei Tags, von denen mehrere gleichzeitig zutreffen können – nimmt man paarweise binomiale Klassifikation mit Sigmoid, ein $\sigma$ pro Klasse.
:::

## Kurze Erinnerung an die Kettenregel

Für das Training werden wir Ableitungen von verketteten Funktionen brauchen, deshalb zum Abschluss die Kettenregel in der Form, die wir benötigen – für Funktionen zwischen Vektorräumen.

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

## Tipps zum Übungsblatt

Auf Blatt 4 implementieren Sie die logistische Regression in PyTorch, auf Blatt 5 rechnen Sie mit Sigmoid, Softmax und Kreuzentropie.

* Wenn Sie die Trainingsroutine zu kompliziert finden, können Sie anfangen, Test-Cases zu schreiben für das Training aus einer einzelnen Stichprobe (und hierbei z.B. mit den ersten 2 Features des Iris-Datensatzes arbeiten) und diese ans Laufen zu bringen.
* Das Training sollte so ablaufen, dass der Loss dabei sinkt – nicht notwendig strikt monoton, aber im Mittel schon. Wenn das bei Ihnen nicht passiert, ist etwas schief gegangen. Nach einiger Zeit (wenn die Eingabedaten schon mehrmals zum Lernen genutzt wurden) ändert sich der Loss nur noch sehr wenig bis gar nicht. Plotten kann helfen: `losses` gegen `epoch`.
