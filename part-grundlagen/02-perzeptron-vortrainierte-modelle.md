---
title: "VL 02: Perzeptron in der Praxis, vortrainierte Modelle"
short_title: "VL 02"
---

# Perzeptron in der Praxis, vortrainierte Modelle

:::{warning} Rohfassung
Dieses Kapitel ist eine automatische Transkription der Folien von VL 02 aus dem WiSe 2025/26
(`from_2025/slides/Einführung in Deep Learning 2025_26 VL 02_ Perzeptron, Vortrainierte Modelle.pdf`), Folie für Folie in der Originalreihenfolge.
Formeln und Abbildungen sind dabei größtenteils verloren gegangen; der Text ist noch nicht überarbeitet.
:::

## Wie war das mit dem Perzeptron?

<!-- Folie 2 -->

## In die Praxis

<!-- Folie 3 -->
Wir implementieren ein Perzeptron (Blatt 2)
Als Aufwärmübung. Zu klärende Fragen:
◼ Was sind die freien Parameter (Gewichte) des Modells
(welche Variablen ändern sich beim Training)?
◼ Wie soll Inferenz durchgeführt werden?
◼ Wie funktioniert das Training?
…

<!-- Folie 4 -->
Wir implementieren ein Perzeptron (Blatt 2)
Als Aufwärmübung. Zu klärende Fragen:
◼ Was sind die freien Parameter (Gewichte) des Modells
(welche Variablen ändern sich beim Training)?
◼ Wie soll Inferenz durchgeführt werden?
◼ Wie funktioniert das Training?
◼
◼
◼
◼
◼
supervised/unsupervised?
was genau erlauben wir für Datentypen?
welche Berechnung zur Anpassung der Gewichte?
was ist die Zielgröße (wann ist genug trainiert)?
welche Hyperparameter gibt es
und worauf legen wir sie fest?

<!-- Folie 5 -->
Wir implementieren ein Perzeptron (Blatt 2)
Das Perzeptron ist ein Modell zur binären Klassifikation,
d.h. Supervised Learning,
Input sind Stichproben von (X,Y),
wobei X Werte in ℝn hat und Y ∊ {0,1} die Klasse ist.
Dabei ist das n, also die Dimensionalität der Eingabedaten,
ein Hyperparameter (den wir i.d.R. nicht optimieren wollen).
Ziel ist die Berechnung einer Funktion f(X) mit Y = f(X) + ε.

<!-- Folie 6 -->
Wir implementieren ein Perzeptron (Blatt 2)
Das Perzeptron ist ein Modell zur binären Klassifikation,
d.h. Supervised Learning,
Input sind Stichproben von (X,Y),
wobei X Werte in ℝn hat und Y ∊ {0,1} die Klasse ist.
Die Parameter des Modells sind n Gewichte wj bzw.
ein Gewichtsvektor w ∊ ℝn.
Inferenz geht so: f(x) = [ w · x > 0 ] (Iversen-Bracket),
also ist f(x) = 1 wenn ∑jwjxj > 0 ist. Das f ist eine nichtlineare Funktion!

<!-- Folie 7 -->
Wir implementieren ein Perzeptron (Blatt 2)
Das Perzeptron ist ein Modell zur binären Klassifikation,
Input sind Stichproben von (X,Y) mit X ∊ ℝn, Y ∊ {0,1}.
Die Parameter des Modells sind ein Gewichtsvektor w ∊ ℝn.
Inferenz geht so: f(x) = [ w · x > 0 ]
Training = Anpassung der Gewichte:
Gegeben bisherige Gewichte w und ein einzelnes Sample (x,y) setze
wneu := w + r · (y - f(x))x.
Dabei ist r ein Hyperparameter, die Lernrate.

<!-- Folie 8 -->
Wir implementieren ein Perzeptron (Blatt 2)
Das Perzeptron ist ein Modell zur binären Klassifikation,
Input sind Stichproben von (X,Y) mit X ∊ ℝn, Y ∊ {0,1}.
Die Parameter des Modells sind ein Gewichtsvektor w ∊ ℝn.
Inferenz geht so: f(x) = [ w · x > 0 ]
Training: Gegeben bisherige Gewichte w und ein einzelnes Sample (x,y)
wneu := w + r · (y - f(x))x.
Wenn y = f(x), also bei korrekter Klassifikation, so ist wneu = w
Wenn y ≠ f(x), so ist wneu = w + rx oder wneu = w - rx (je nach Klasse y)
Erinnerung: x · x > 0 gilt immer außer für x = 0.

<!-- Folie 9 -->
Wir implementieren ein Perzeptron (Blatt 2)
Das Perzeptron ist ein Modell zur binären Klassifikation,
Input sind Stichproben von (X,Y) mit X ∊ ℝn, Y ∊ {0,1}.
Die Parameter des Modells sind ein Gewichtsvektor w ∊ ℝn.
Inferenz geht so: f(x) = [ w · x > 0 ]
Training: Gegeben bisherige Gewichte w und ein einzelnes Sample (x,y)
wneu := w + r · (y - f(x))x.
Das Ziel messen wir in Anteil falsch klassifizierter Samples.
Wir initialisieren w z.B. auf den Vektor (1,1,...,1).

<!-- Folie 10 -->
Wir implementieren ein Perzeptron (Blatt 2)
Das Perzeptron ist ein Modell zur binären Klassifikation,
Input sind Stichproben von (X,Y) mit X ∊ ℝn, Y ∊ {0,1}.
Die Parameter des Modells sind ein Gewichtsvektor w ∊ ℝn
und der Biasterm b ∊ ℝ.
Inferenz geht so: f(x) = [ w · x + b > 0 ]
Training: Gegeben bisherige Gewichte w, b und ein einzelnes Sample (x,y)
wneu := w + r · (y - f(x))x und bneu := b + r · (y - f(x))
Aber wir kennen das schon: mit w0 := b und x0 := 1 ist alles wie zuvor.

<!-- Folie 11 -->
Wir implementieren ein Perzeptron (Blatt 2)
Übungsaufgabe:
Ein Perzeptron mit Python&Numpy implementieren und auswerten
Eingabedaten: (x,y) wobei x ein zweidimensionaler Array ist
Ausgabe: Genauigkeit auf einem Testset (nach Training).

<!-- Folie 12 -->
Wir implementieren ein Perzeptron (Blatt 2)
Übungsaufgabe:
Ein Perzeptron mit Python&Numpy implementieren und auswerten
Eingabedaten: (x,y) wobei x ein zweidimensionaler Array ist
Ausgabe: Genauigkeit auf einem Testset (nach Training).
Tipp: Lernrate 0.01
Tipp 2: die selben Daten mehrmals verwenden im Training
Tipp 3: zum Üben hier gut geeignet: scikit-learn’s datasets.make_blobs

<!-- Folie 13 -->
Wir implementieren ein Perzeptron (Blatt 2)
Übungsaufgabe:
Ein Perzeptron mit Python&Numpy implementieren und auswerten
Eingabedaten: (x,y) wobei x ein zweidimensionaler Array ist
Ausgabe: Genauigkeit auf einem Testset (nach Training).
Komplett lost? Kommilitonen ebenfalls überfordert?
Bitte Bescheid sagen und ggf. das hier lesen (ist aber ugly code):
github.com/nandesh553/100-Days-of-Deep-Learning/blob/main/Day%207%20-%20Perceptrons%20from%20scratch%20using%20NumPy.ipynb

## Zurück in die Theorie

<!-- Folie 14 -->
Wozu das olle Perzeptron?
Moderne neuronale Netze verwenden meist keine Perzeptrons mehr.
Beliebter ist stattdessen die Multilineare oder Logistische Regression,
die ebenfalls gleich strukturierte Eingabedaten annimmt und sehr
ähnlich verarbeitet:
Skalarprodukt, gefolgt von einer nichtlinearen Funktion.
Dieses “Kochrezept” (die gemeinsame Verallgemeinerung) heißt
manchmal auch einfach “Perzeptron”.
Offene Frage: wie trainiert man ein “verallgemeinertes Perzeptron”?

## Wie geht’s weiter mit dem Perzeptron?

<!-- Folie 15 -->
Training des verallgemeinerten Perzeptrons
Das verallgemeinerte Perzeptron ist ein Regressionsmodell mit
Funktion
f(x) = τ(w · x)
Spezialfall
Lineare Regression: τ(a) = a
Perzeptron:
τ(a) = [a > 0]

<!-- Folie 16 -->
Training des verallgemeinerten Perzeptrons
Das verallgemeinerte Perzeptron ist ein Regressionsmodell mit
Funktion
f(x) = τ(w · x)
Spezialfall
Training
Lineare Regression: τ(a) = a
kleinste Quadrate
Perzeptron:
τ(a) = [a > 0] Perzeptronregel
wneu := w + r · (y - f(x))x

<!-- Folie 17 -->
Training des verallgemeinerten Perzeptrons
Das verallgemeinerte Perzeptron ist ein Regressionsmodell mit
Funktion
f(x) = τ(w · x)
Spezialfall
Lineare Regression: τ(a) = a
Perzeptron:
τ(a) = [a > 0]
Stetige Version:
τ(a) = tanh(a), hyperbolischer Tangens
Logistische Reg.:
τ(a) = σ(a), logistische Sigmoidfunktion

<!-- Folie 18 -->
Training des verallgemeinerten Perzeptrons
Das verallgemeinerte Perzeptron ist ein Regressionsmodell mit
Funktion
f(x) = τ(w · x)
Spezialfall
Lineare Regression: τ(a) = a
Perzeptron:
τ(a) = [a > 0]
Stetige Version:
τ(a) = tanh(a), hyperbolischer Tangens
Logistische Reg.:
τ(a) = σ(a), logistische Sigmoidfunktion
Update-Regel?
wneu = ???

<!-- Folie 19 -->
Training des verallgemeinerten Perzeptrons
Das verallgemeinerte Perzeptron ist ein Regressionsmodell mit
Funktion
f(x) = τ(w · x)
Spezialfall
Lineare Regression: τ(a) = a
Perzeptron:
τ(a) = [a > 0]
Stetige Version:
τ(a) = tanh(a), hyperbolischer Tangens
Logistische Reg.:
τ(a) = σ(a), logistische Sigmoidfunktion
→ werden wir noch eingehend studieren

<!-- Folie 20 -->
Training des Mehrschichten-Perzeptrons (MLP)
Das verallgemeinerte Perzeptron ist ein Regressionsmodell mit
Funktion
f(x) = τ(w · x)
Angenommen, x ∊ ℝ2 und v,w ∊ ℝ2 sind die Gewichte von zwei
Perzeptrons:
x1
g(x) = [v · x > 0]
x2
f(x) = [w · x > 0]

<!-- Folie 21 -->
Training des Mehrschichten-Perzeptrons (MLP)
Das verallgemeinerte Perzeptron ist ein Regressionsmodell mit
Funktion
f(x) = τ(w · x)
Angenommen, x ∊ ℝ2 und v,w ∊ ℝ2 sind die Gewichte von zwei
Perzeptrons und z := (g(x), f(x)) ist der Ergebnisvektor.
x1
g(x) = [v · x > 0]
h(x) = [u · z > 0]
x2
f(x) = [w · x > 0]
Perzeptron-Updateregel nur für 1 Perzeptron (hier: h bzw u)

<!-- Folie 22 -->
Training des Mehrschichten-Perzeptrons (MLP)
Das verallgemeinerte Perzeptron ist ein Regressionsmodell mit
Funktion
f(x) = τ(w · x)
Angenommen, x ∊ ℝ2 und v,w ∊ ℝ2 sind die Gewichte von zwei
Perzeptrons und z := (g(x), f(x)) ist der Ergebnisvektor.
x1
g(x) = [v · x > 0]
h(x) = [u · z > 0]
x2
f(x) = [w · x > 0]
→ Multilayer-Training? Backpropagation! … machen wir noch.

<!-- Folie 23 -->
Training der Mehrschichten-Linearen Regression
Die lineare Regression ist ein Regressionsmodell mit Funktion
f(x) = w · x
Angenommen, x ∊ ℝ2 und v,w ∊ ℝ2 sind die Gewichte von zwei
lin.Reg. und z := (v · x, w · x) ist der Ergebnisvektor.
x1
g(x) = v · x
h(x) = u · z = u1(v · x)+u2(w · x)
x2
f(x) = w · x

<!-- Folie 24 -->
Training der Mehrschichten-Linearen Regression
Die lineare Regression ist ein Regressionsmodell mit Funktion
f(x) = w · x
Angenommen, x ∊ ℝ2 und v,w ∊ ℝ2 sind die Gewichte von zwei
lin.Reg. und z := (v · x, w · x) ist der Ergebnisvektor.
x1
g(x) = v · x
h(x) = u · z = u1(v · x)+u2(w · x)
x2
f(x) = w · x
=
u1v1x1+u1v2x2+u2w1x1+u2w2x2
= (u1v+u2w) · x
→ äquivalent zu einer einzigen linearen Regression

## Vortrainierte Modelle verwenden; Orientierung

<!-- Folie 25 -->

## Tasks

<!-- Folie 26 -->
Was tun mit Deep Learning?
Wenn wir für eine Aufgabe ein vortrainiertes
Modell verwenden wollen,
müssen wir wissen, welches Modell
geeignet sein kann.
→ Wir schauen bei Hugging Face
huggingface.co/models
huggingface.co/tasks
“The Hugging Face Hub hosts many models
for a variety of machine learning tasks.”

<!-- Folie 29 -->

## Hugging Face … ?

<!-- Folie 30 -->
Surfen Sie ruhig weiter auf HuggingFace.co. Hier ein paar Fakten:
◼
◼
◼
HF verdient Geld mit gehosteter Inferenz
HF lockt Entwickler an mit guter Infrastruktur wie
◼ Libraries (z.B. transformers, diffusers, gradio),
◼ Hosting (git repos, models, spaces),
◼ Dokumentation
für Finetuning (Nachtrainieren von vortrainierten Modellen).
HF ist ein privates Unternehmen aus New York City, gegründet 2016,
Heute (bzw. Ende 2023) mit ca. 4.5 Mrd. $ bewertet

## Zum neuen Übungsblatt

<!-- Folie 31 -->
Tipps für Blatt 2
◼ Arbeiten Sie direkt mit der Perzeptronregel
wneu := w + r · (y - f(x))x
und lassen Sie sich nicht vom verallgemeinerten Perzeptron verwirren.
◼ Benutzen Sie Scikit-learn:
◼ sklearn.model_selection.train_test_split
◼ sklearn.datasets.make_blobs
◼
sklearn.datasets.load_iris
