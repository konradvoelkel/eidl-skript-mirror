---
title: "VL 02: Perzeptron in der Praxis, vortrainierte Modelle"
short_title: "VL 02"
---

# Perzeptron in der Praxis, vortrainierte Modelle

:::{note} Stand
Erste Prosafassung (aus den Folien von VL 02, WiSe 2025/26). Abbildungen fehlen noch, siehe die `TODO`-Kommentare.
:::

## Wie war das mit dem Perzeptron?

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

also $f(x) = 1$ genau dann, wenn $\sum_j w_j x_j + b > 0$. Mit dem Trick $w_0 := b$, $x_0 := 1$ aus dem letzten Kapitel schreiben wir im Folgenden einfach $f(x) = [\, w \cdot x > 0 \,]$ und denken uns den Bias als nulltes Gewicht.

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

<!-- TODO Abbildung: make_blobs-Daten in R^2 mit Trenngerade w·x + b = 0 vor und nach einigen Perzeptron-Updates -->

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

## Vortrainierte Modelle verwenden: Orientierung

### Was tun mit Deep Learning?

Bevor wir selbst Modelle trainieren, lohnt sich ein Blick darauf, was es schon gibt. Wenn wir für eine Aufgabe ein vortrainiertes Modell verwenden wollen, müssen wir wissen, welches Modell geeignet sein kann. Dafür schauen wir bei **Hugging Face**: [huggingface.co/models](https://huggingface.co/models) listet Modelle, [huggingface.co/tasks](https://huggingface.co/tasks) sortiert sie nach Aufgabe („The Hugging Face Hub hosts many models for a variety of machine learning tasks.“). Die Task-Seiten sind ein guter Einstieg, um das Vokabular zu lernen: Was ist Image Classification, Object Detection, Token Classification, Text Generation, …? Einen systematischen Rundgang machen wir im nächsten Kapitel.

<!-- TODO Abbildung: Screenshot huggingface.co/tasks (Folien 27–28) oder Liste der Task-Kategorien -->

### Hugging Face … ?

Surfen Sie ruhig weiter auf huggingface.co. Hier ein paar Fakten zur Einordnung:

* HF verdient Geld mit gehosteter Inferenz.
* HF lockt Entwickler an mit guter Infrastruktur: Libraries (z.B. `transformers`, `diffusers`, `gradio`), Hosting (git-Repositories für Modelle, Datensätze und „Spaces“) und Dokumentation – insbesondere für **Finetuning**, das Nachtrainieren von vortrainierten Modellen.
* HF ist ein privates Unternehmen aus New York City, gegründet 2016, Ende 2023 mit ca. 4,5 Mrd. $ bewertet.

Mit anderen Worten: Der Hub ist ein kommerzielles Angebot, aber die Modelle und Libraries darauf sind größtenteils offen, und für uns ist er die bequemste Art, an Gewichte zu kommen.

## Tipps zum Übungsblatt

Auf Blatt 2 implementieren Sie ein Perzeptron mit Python und NumPy und werten es aus. Eingabedaten sind $(x, y)$, wobei `x` ein zweidimensionales Array ist (eine Zeile pro Sample, eine Spalte pro Feature); Ausgabe ist die Genauigkeit auf einem Testset nach dem Training.

* Arbeiten Sie direkt mit der Perzeptronregel $w_{\text{neu}} := w + r \cdot (y - f(x)) \, x$ und lassen Sie sich nicht vom verallgemeinerten Perzeptron verwirren.
* Lernrate: $r = 0{,}01$ ist ein guter Startwert.
* Verwenden Sie dieselben Daten mehrmals im Training (mehrere *Epochen*).
* Benutzen Sie Scikit-learn: `sklearn.model_selection.train_test_split` für den Split, `sklearn.datasets.make_blobs` für gut geeignete Übungsdaten, `sklearn.datasets.load_iris` für einen echten Datensatz.
* Komplett lost, Kommilitonen ebenfalls überfordert? Bitte Bescheid sagen.
