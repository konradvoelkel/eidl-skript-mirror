---
title: "VL 04: Logistische Regression"
short_title: "VL 04"
---

# Logistische Regression

:::{warning} Rohfassung
Dieses Kapitel ist eine automatische Transkription der Folien von VL 04 aus dem WiSe 2025/26
(`from_2025/slides/Einführung in Deep Learning 2025_26 VL 04_ Logistische Regression.pdf`), Folie für Folie in der Originalreihenfolge.
Formeln und Abbildungen sind dabei größtenteils verloren gegangen; der Text ist noch nicht überarbeitet.
:::

## Wahrscheinlichkeiten und

<!-- Folie 2 -->
Chancen (Odds)

## Chancen (Odds)

<!-- Folie 3 -->
Für ein Bernoulli-Experiment (Münzwurf)
Angenommen, wir haben ein Bernoulli-Experiment mit Parameter 𝑝∈(0,1),
zur Vereinfachung mit p≠0 und p≠1.
Die Wahrscheinlichkeit (probability) für Erfolg ist P(Erfolg) = 𝑝,
Die Chancen (odds) für Erfolg sind 𝑝 : 1-𝑝.

<!-- Folie 4 -->
Für ein Bernoulli-Experiment (Münzwurf)
Angenommen, wir haben ein Bernoulli-Experiment mit Parameter 𝑝∈(0,1),
zur Vereinfachung mit p≠0 und p≠1.
Die Wahrscheinlichkeit (probability) für Erfolg ist P(Erfolg) = 𝑝,
Die Chancen (odds) für Erfolg sind 𝑝 : 1-𝑝.
Beispiel für ein Bernoulli-Experiment:
Standardwürfel (D6) rollen und gucken, ob es eine 6 ist.
P(D = 6) = ⅙ = p (Wahrscheinlichkeit) und
1 : 5 = ⅕ sind die Chancen für eine 6.

<!-- Folie 5 -->
Für ein Bernoulli-Experiment (Münzwurf)
Beispiel für ein Bernoulli-Experiment:
Standardwürfel (D6) rollen und gucken, ob es eine 6 ist.
P(D = 6) = ⅙ = p (Wahrscheinlichkeit) und
1 : 5 = ⅕ sind die Chancen für eine 6.
5 : 1 = 5 sind die Chancen für eine Nicht-6.
odds(D = 6) = P(D = 6) / P(D ≠ 6) = ⅙ / ⅚ = ⅕

<!-- Folie 6 -->
Probability → Odds → Probability
Standardwürfel (D6) rollen und gucken, ob es eine 6 ist.
P(D = 6) = ⅙ = p (Wahrscheinlichkeit) und Chancen
odds(D = 6) = P(D = 6) / P(D ≠ 6) = ⅙ / ⅚ = ⅕
Allgemein:

<!-- Folie 7 -->
Skala für Odds
Wenn p = ½ ist, so ist 1-p = ½, also
odds(p) = p / (1-p) = 1

<!-- Folie 8 -->
Skala für Odds
Wahrscheinlichkeiten liegen immer in [0, 1].
Wenn 0 < p < ½ ist, so ist 1 > 1-p > ½, also
0 < odds(p) = p / (1-p) < p / ½ = 2p < 1
Damit also odds(p) ∈ [0, 1)

<!-- Folie 9 -->
Skala für Odds
Wahrscheinlichkeiten liegen immer in [0, 1].
Wenn 1 > p > ½ ist, so ist 0 < 1-p < ½, also
1 < 2p < odds(p) = p / (1-p) < 1 / (1-p) < ∞
Damit also odds(p) ∈ (1, ∞)

<!-- Folie 10 -->
Skala für Odds
Wahrscheinlichkeiten liegen immer in [0, 1],
Die Fälle p < ½ und p > ½ sind symmetrisch,
d.h. Erfolg und Mißerfolg sind äquivalent.
odds(p) ∈ [0, ∞) ist nicht symmetrisch!
[0,1) ist beschränkt, (1, ∞) ist unbeschränkt.

<!-- Folie 11 -->
Skala für Odds
[0,1) ist beschränkt, (1, ∞) ist unbeschränkt.
Beachte: Logarithmieren rettet die Symmetrie.
log( p / 1-p ) = log(p) - log(1-p)
Damit ist log( 1 : 5 ) = - log( 5 : 1).
Die Werte liegen in (-∞, +∞).

<!-- Folie 12 -->
Logistic Unit
Definition:

<!-- Folie 13 -->
Logistic Unit
Definition:
Schonmal irgendwo gesehen?

<!-- Folie 14 -->
Logistic Unit
Definition:
Entropie des Bernoulli-Experiments ist
H(p) = -p*log(p) - (1-p)*log(1-p)

<!-- Folie 15 -->
Logistic Unit
Definition:
Interpretation:
Bei Erhöhen von p ist die Abnahme an
Informationsgewinn durch logit(p) gegeben.

<!-- Folie 16 -->
Entropie misst man in
bit/nat,
Die Ableitung in logit.

<!-- Folie 17 -->
H(0.5) = 1 bit = 0.69 nat
Entropie misst man in
bit/nat,
Die Ableitung in logit.

## Logistische Sigmoidfunktion

<!-- Folie 18 -->

<!-- Folie 19 -->
Allgemeine S-Förmigkeit
Sigma ≈ S
Sigmoid ≈ S-förmig
Definition:
Die allgemeine logistische Funktion
(aka allgemeine Sigmoidfunktion)
mit Parametern M, k, μ ist gegeben als Funktion in x:

<!-- Folie 20 -->
Allgemeine S-Förmigkeit
Definition:
Die allgemeine logistische Funktion
(aka allgemeine Sigmoidfunktion)
mit Parametern M, k, μ ist gegeben als Funktion in x:
Das Standardsigmoid ist

<!-- Folie 21 -->
Plot:

<!-- Folie 22 -->
Symmetrie:

<!-- Folie 23 -->
Symmetrie:
Also: 𝜎(−𝑥) = 1−𝜎(𝑥).

<!-- Folie 24 -->
Andere Sigmoidfunktion:
Die Parameter M und k sind Skalierungsfaktoren.
Möchte man die Skala des Standardsigmoids von [0,1]
auf z.B. [-1, 1] bringen:

<!-- Folie 25 -->
Andere Sigmoidfunktion: tangens hyperbolicus
Die Parameter M und k sind Skalierungsfaktoren.
Möchte man die Skala des Standardsigmoids von [0,1]
auf z.B. [-1, 1] bringen:
=

<!-- Folie 26 -->
Ableitung
Wir benötigen später die Ableitung der Sigmoidfunktion.
Evtl. bekannt ist tanh’(x) = 1 - tanh²(x). Ähnlich:

## Sigmoid und Logit

<!-- Folie 27 -->

## Sigmoidfunktion und Logit

<!-- Folie 28 -->
Was haben die Funktionen miteinander zu tun?
𝜎 : ℝ → (0, 1)
logit : (0, 1) → ℝ
Also:
𝜎 ⚬ logit : (0,1) → (0,1)
logit ⚬ 𝜎 : ℝ → ℝ

<!-- Folie 29 -->
Was haben die Funktionen miteinander zu tun?
𝜎 : ℝ → (0, 1)
logit : (0, 1) → ℝ
Also:
𝜎 ⚬ logit : (0,1) → (0,1)
logit ⚬ 𝜎 : ℝ → ℝ

<!-- Folie 30 -->
Was haben die Funktionen miteinander zu tun?
Für p ∊ (0, 1) ist

<!-- Folie 31 -->
Was haben die Funktionen miteinander zu tun?
Für p ∊ (0, 1) ist

<!-- Folie 32 -->
Was haben die Funktionen miteinander zu tun?
Für x ∊ ℝ ist

<!-- Folie 33 -->
Was haben die Funktionen miteinander zu tun?
Für x ∊ ℝ ist
Erst 𝜎(x) mit ex
erweitern, dann ln
anwenden und
ln(ex)=x nutzen.

<!-- Folie 34 -->
Was haben die Funktionen miteinander zu tun?
Für x ∊ ℝ ist

<!-- Folie 35 -->
Was haben die Funktionen miteinander zu tun?
Für x ∊ ℝ ist

<!-- Folie 36 -->
Was haben die Funktionen miteinander zu tun?
Wir haben gesehen, 𝜎 und logit sind Inverse zueinander:
𝜎 ⚬ logit = id : (0,1) → (0,1)
logit ⚬ 𝜎 = id : ℝ → ℝ

<!-- Folie 37 -->
Was haben die Funktionen miteinander zu tun?
Wir haben gesehen, 𝜎 und logit sind Inverse zueinander:
𝜎 ⚬ logit = id : (0,1) → (0,1)
logit ⚬ 𝜎 = id : ℝ → ℝ
Darum nennt man 𝜎 als Inverse von logit auch expit.
Wie interpretieren wir diesen Zusammenhang?

## Sigmoid ist Umkehrfunktion zu Logit

<!-- Folie 38 -->
Wie interpretieren wir das?
Gegeben einen Wert x ∊ ℝ
gibt 𝜎(x) einen Wert p := 𝜎(x) ∊ (0, 1)
sodass x = logit(p).
Jeder Wert x lässt sich also als logits auffassen
und 𝜎(x) gibt die Wahrscheinlichkeit des
Bernoulli-Experiments an, zu der x der logit-Wert ist.

## Logistische Regression

<!-- Folie 39 -->

<!-- Folie 40 -->
Alle Zutaten bereit: jetzt wird gekocht
Die Lineare Regression spuckt y-Werte aus, die in ganz ℝ liegen.
Wenn y=0 und y=1 zu den zwei Klassen korrespondieren, so
geben die Werte 𝜎(y) Wahrscheinlichkeiten an, in Klasse 1 zu
liegen.
Wenn 𝜎(y) > ½, so entscheiden wir für Klasse 1.

<!-- Folie 41 -->
Alle Zutaten bereit: jetzt wird gekocht
In Scikit-Learn wird in der logistischen Regression unterschieden
zwischen predict und predict_proba.
Wenn ypred der durch lineare Regression vorhergesagte Wert
an einem Punkt x ist, so gilt
predict_proba(x) = 𝜎(ypred)
predict(x) = [ 𝜎(ypred) > ½ ].

## Lineare Regression in PyTorch

<!-- Folie 42 -->
Alle Zutaten bereit: jetzt wird gekocht
In PyTorch macht man eine lineare Regression so:

<!-- Folie 43 -->
Alle Zutaten bereit: jetzt wird gekocht

<!-- Folie 44 -->

## Logistische Regression in PyTorch

<!-- Folie 45 -->
Alle Zutaten bereit: jetzt wird gekocht
In PyTorch macht man eine logistische Regression so:

<!-- Folie 46 -->
Alle Zutaten bereit: jetzt wird gekocht

<!-- Folie 47 -->

## Weg von der

<!-- Folie 48 -->
2-Klassen-Gesellschaft: Softmax

## Multiklassen-Regression

<!-- Folie 49 -->
Bernoulli → Multinoulli
Binomial (2 Klassen) → Multinomial (K Klassen)
Anstelle eines einzelnen y-Werts der linearen Regression,
der uns mit 𝜎 die Wahrscheinlichkeit für Klasse 1 angibt,
benötigen wir nun einen Vektor der Länge K,
der sich auf 1 aufsummiert.
Für K=2 erwarten wir den Vektor (𝜎(y), 1 - 𝜎(y)).

<!-- Folie 50 -->
Bernoulli → Multinoulli
Binomial (2 Klassen) → Multinomial (K Klassen)
Wenn wir die Klasse one-hot kodieren,
also Vektoren der Länge K als Labels verwenden,
dann liefert multinomiale lineare Regression
Vorhersagevektoren der Länge K.
Entscheidung für Klasse k ∊ {1, …, K} wenn
Der Eintrag des Vektors an Index k am größten ist (argmax=k).

<!-- Folie 51 -->
Bernoulli → Multinoulli
Wenn wir die Klasse one-hot kodieren,
dann liefert multinomiale lineare Regression
Vorhersagevektoren der Länge K.
Entscheidung für Klasse k ∊ {1, …, K} wenn
Der Eintrag des Vektors an Index k am größten ist (argmax=k).
Gesucht: Analog zu 𝜎 ein “soft argmax”.

<!-- Folie 52 -->
Bernoulli → Multinoulli
Definition:
Die softmax-Funktion
Ist komponentenweise gegeben durch
Dabei ist 𝚫K die Teilmenge von [0, 1]K mit Σvj=1.

<!-- Folie 53 -->
Bernoulli → Multinoulli
Die softmax-Funktion ist komponentenweise gegeben durch
Man darf sich das zweistufig vorstellen:
Im ersten Schritt wird der Vektor v komponentenweise exponiert,
im zweiten Schritt der Vektor normiert.

<!-- Folie 54 -->
Bernoulli → Multinoulli
Die softmax-Funktion ist komponentenweise gegeben durch
Für den Fall K=2 mit v=(x,y) können wir leicht einsehen, dass
𝜎(v)1 = 1 / (1 + ey-x)

<!-- Folie 55 -->
Obacht!
Nicht jedes Multiklassen-Klassifikationsproblem schreit nach dem
Softmax!
Softmax ist dann sinnvoll, wenn argmax sinnvoll wäre,
also wenn sich die Klassen gegenseitig ausschließen.
Sonst: paarweise Binomiale Klassifikation (mit Sigmoid).

## Kurze Erinnerung an die

<!-- Folie 56 -->
Kettenregel

## Erinnerung an die Kettenregel

<!-- Folie 57 -->
The chain rule
Für eine Funktion g: ℝn → ℝm an einem Punkt x0,
Die Ableitung (Dg)(x0) ist die beste
lineare Approximation, also für x1 nah bei
x0
g(x1) ≈ g(x0) + (Dg)(x0) (x1 - x0)

<!-- Folie 58 -->
The chain rule
Für eine Funktion g: ℝn → ℝm an einem Punkt x0,
Die Ableitung (Dg)(x0) ist die beste
lineare Approximation, also für x1 nah bei
x0
g(x1) ≈ g(x0) + (Dg)(x0) (x1 - x0)
Gegeben eine weitere Funktion f: ℝm → ℝk
f(y1) ≈ f(y0) + (Df)(y0) (y1 - y0)
Spezialfall y0=g(x0), y1=g(x1)

<!-- Folie 59 -->
The chain rule
Für eine Funktion g: ℝn → ℝm an einem Punkt x0,
Die Ableitung (Dg)(x0) ist die beste
lineare Approximation, also für x1 nah bei
x0
f(g(x1)) ≈ f(g(x0)) + (Df)g(x0) (g(x1) - g(x0))
≈ f(g(x0)) + (Df)g(x0) (g(x0) + (Dg)(x0) (x1 - x0) - g(x0))
≈ f(g(x0)) + (Df)g(x0) (Dg)(x0) (x1 - x0)
g(x1) ≈ g(x0) + (Dg)(x0) (x1 - x0)
Gegeben eine weitere Funktion f: ℝm → ℝk
f(y1) ≈ f(y0) + (Df)(y0) (y1 - y0)
Spezialfall y0=g(x0), y1=g(x1)

<!-- Folie 60 -->
The chain rule
Für eine Funktion g: ℝn → ℝm an einem Punkt x0,
Die Ableitung (Dg)(x0) ist die beste
lineare Approximation, also für x1 nah bei
x0
f(g(x1)) ≈ f(g(x0)) + (Df)g(x0) (g(x1) - g(x0))
≈ f(g(x0)) + (Df)g(x0) (g(x0) + (Dg)(x0) (x1 - x0) - g(x0))
≈ f(g(x0)) + (Df)g(x0) (Dg)(x0) (x1 - x0)
g(x1) ≈ g(x0) + (Dg)(x0) (x1 - x0)
Damit ist (Df)g(x0) (Dg)(x0)
die beste lineare Approximation
von fg bei x0
Gegeben eine weitere Funktion f: ℝm → ℝk
f(y1) ≈ f(y0) + (Df)(y0) (y1 - y0)
In anderer Notation der gleiche Sachverhalt:
D(fg) = (Df)g Dg
Spezialfall y0=g(x0), y1=g(x1)

## Zum neuen Übungsblatt

<!-- Folie 61 -->
Tipps für Blatt 4
Wenn Sie die Trainingsroutine zu kompliziert finden, können Sie
anfangen Test-Cases zu schreiben für das Training aus einer einzelnen
Stichprobe (und hierbei z.B. mit den ersten 2 Features des
Iris-Datensatz arbeiten) und diese ans Laufen zu bringen.
Das Training sollte so ablaufen, dass der Loss dabei sinkt - nicht
notwendig strikt monoton, aber im Mittel schon. Wenn das bei Ihnen
nicht passiert, ist etwas schief gegangen. Nach einiger Zeit (wenn die
Eingabedaten schon mehrmals zum Lernen genutzt wurden) ändert
sich der Loss nur noch sehr wenig bis gar nicht. Plotten kann beim
Debuggen hilfreich sein.
