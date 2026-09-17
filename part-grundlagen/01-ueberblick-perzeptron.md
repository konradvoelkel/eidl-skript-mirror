---
title: "VL 01: Überblick und Perzeptron"
short_title: "VL 01"
---

# Überblick und Perzeptron

:::{warning} Rohfassung
Dieses Kapitel ist eine automatische Transkription der Folien von VL 01 aus dem WiSe 2025/26
(`from_2025/slides/Einführung in Deep Learning 2025_26 VL 01_ Überblick, Perzeptron.pdf`), Folie für Folie in der Originalreihenfolge.
Formeln und Abbildungen sind dabei größtenteils verloren gegangen; der Text ist noch nicht überarbeitet.
:::

## Formales (mehr dazu in ILIAS)

<!-- Folie 2 -->
Übungsbetrieb + Prüfung
Jede Woche Mittwochs 12:30 ist Vorlesung in 5E,
Jede Woche Donnerstags 10:30 ist Übung in 25.22.U1.52.
Es gibt jede Woche ein Übungsblatt, das man einreichen kann.
Zur Prüfung zugelassen ist, wer 8 von 11 Blättern bestanden hat.
In der Übung besprechen wir die Aufgaben von der Vorwoche,
manchmal Anwesenheitsaufgaben, diskutieren offene Fragen
und Tipps zum aktuellen Übungsblatt.
Kommunikation im ILIAS-Forum für organisatorisches sowie
inhaltliches - nicht per E-Mail!

## Voraussetzungen

<!-- Folie 3 -->
Das bitte mitbringen:
Das lernen wir zusammen:
◼
◼
◼
Begriffe
◼
◼
◼
◼
◼
Vektorraum, Vektor
Matrix
Ableitung
Zufallsvariable
Grobe Idee von
Linearer Regression
Grundlagen Python
(ideal wäre Numpy)
Am besten vorher “Data Science”
bestehen. Die VLen “Machine Learning”
oder “Data Science 2” sind nicht
erforderlich.
◼
◼
◼
◼
◼
Begriffe, u.a.
◼
◼
◼
◼
Gradientenabstieg, Loss-Funktion
Matrizenkalkül, Tensorkalkül
Latenter Raum
Logistische Regression
Grundlagen PyTorch
Was ist ein neuronales Netz
Wie benutzt man fertige Modelle
Wie verändert man fertige Modelle
Was sind die Besonderheiten bei
◼
◼
Text
Bildern

## Erwartungen und Wünsche

<!-- Folie 4 -->

## Inhalte

<!-- Folie 5 -->
Der grobe Plan:
◼
◼
◼
◼
◼
◼
◼
◼
◼
◼
Geschichte (Perzeptron)
HuggingFace (fertige Modelle)
PyTorch (eigene Modelle)
Logistische Regression (Softmax)
Gradientenabstieg,
Backpropagation
Sparse Autoencoder, VAE
für MNIST Ziffern-Klassifikation
NLP: Word2Vec, Tokenizer
CNNs für MNIST Klassifikation
GANs (wie DALL-E mini)
LLMs benutzen, Vibe Coding
The Mark I Perceptron, an early pattern recognition
system, at the Cornell Aeronautical Laboratory.
Logistische Funktion,
Plot von Nutzer Hagman der dt. Wikipedia

## Was ist jetzt Deep Learning?

<!-- Folie 6 -->
Deep = Viele Ebenen (Layer)
Learning = Training
Also:
Training von künstlichen neuronalen Netzen mit vielen Ebenen.

## Wieso Python eine Katastrophe ist

<!-- Folie 7 -->
Für Machine Learning ist Python eigentlich völlig ungeeignet, denn es ist
◼ Single-Threaded by default, mit Garbage Collection und GIL (global
interpreter lock), was Multithreading eher erschwert als erleichtert

<!-- Folie 8 -->
Für Machine Learning ist Python eigentlich völlig ungeeignet, denn es ist
◼ Single-Threaded by default, mit Garbage Collection und GIL (global
interpreter lock), was Multithreading eher erschwert als erleichtert;
◼ Interpretiert, nicht direkt auf die Maschine kompiliert,
und daher etwas langsam

<!-- Folie 9 -->
Für Machine Learning ist Python eigentlich völlig ungeeignet, denn es ist
◼ Single-Threaded by default, mit Garbage Collection und GIL (global
interpreter lock), was Multithreading eher erschwert als erleichtert;
◼ Interpretiert, nicht direkt auf die Maschine kompiliert,
und daher etwas langsam;
◼ Dynamisch gebunden, d.h. nicht typesafe und Typen sind erst zur
Laufzeit bekannt, daher aufwändiges Typechecking

<!-- Folie 10 -->
Für Machine Learning ist Python eigentlich völlig ungeeignet, denn es ist
◼ Single-Threaded by default, mit Garbage Collection und GIL (global
interpreter lock), was Multithreading eher erschwert als erleichtert;
◼ Interpretiert, nicht direkt auf die Maschine kompiliert,
und daher etwas langsam;
◼ Dynamisch gebunden, d.h. nicht typesafe und Typen sind erst zur
Laufzeit bekannt, daher aufwändiges Typechecking;
◼ Nicht maschinennah, daher ist es schwierig, SIMD-Register- und
Cachegrößen der spezifischen Hardware zur Optimierung zu nutzen.

## Wieso Python ganz toll ist

<!-- Folie 11 -->
Für Machine Learning ist Python perfekt, weil
◼ Rapid Prototyping im schnelllebigen ML-Geschäft erforderlich ist

<!-- Folie 12 -->
Für Machine Learning ist Python perfekt, weil
◼ Rapid Prototyping im schnelllebigen ML-Geschäft erforderlich ist;
◼ Schwierige Rechnungen in C/Rust/CUDA durchgeführt werden,
und Python nur die Funktionsaufrufe durchführt

<!-- Folie 13 -->
Für Machine Learning ist Python perfekt, weil
◼ Rapid Prototyping im schnelllebigen ML-Geschäft erforderlich ist;
◼ Schwierige Rechnungen in C/Rust/CUDA durchgeführt werden,
und Python nur die Funktionsaufrufe durchführt;
◼ Die Sprache sehr populär ist und damit viele gut gewartete Pakete das
Datenhandling sehr leicht machen

<!-- Folie 14 -->
Für Machine Learning ist Python perfekt, weil
◼ Rapid Prototyping im schnelllebigen ML-Geschäft erforderlich ist;
◼ Schwierige Rechnungen in C/Rust/CUDA durchgeführt werden,
und Python nur die Funktionsaufrufe durchführt;
◼ Die Sprache sehr populär ist und damit viele gut gewartete Pakete das
Datenhandling sehr leicht machen;
◼ Man damit alle Prinzipien schnell lernen kann, die später immer noch in
anderen Sprachen implementiert werden könnten

<!-- Folie 15 -->
Für Machine Learning ist Python perfekt, weil
◼ Rapid Prototyping im schnelllebigen ML-Geschäft erforderlich ist;
◼ Schwierige Rechnungen in C/Rust/CUDA durchgeführt werden,
und Python nur die Funktionsaufrufe durchführt;
◼ Die Sprache sehr populär ist und damit viele gut gewartete Pakete das
Datenhandling sehr leicht machen;
◼ Man damit alle Prinzipien schnell lernen kann, die später immer noch in
anderen Sprachen implementiert werden könnten;
◼ Damit trainierte Deep-Learning-Modelle (Gewichte) unabhängig von
Python zur Inferenz verwendet werden können.

## Wiederholung / Erinnerung

<!-- Folie 16 -->
Begriffe aus dem maschinellen Lernen
◼
Training-Test Split
◼
Supervised
/ Unsupervised
◼
Klassifikation
/ Regression
◼
Generatives Modell

## Kernfrage im maschinellen Lernen:

<!-- Folie 17 -->
Wie bewerte ich die Güte des Modells,
Wie bewerte ich den Erfolg der Inferenz?
Erinnerung
Training-Test-Split
Wenn man einen Teil der Datenpunkte
zurückhält (nicht im Training verwendet),
um damit das trainierte Modell zu testen.
Quizfrage:
Was kann beim Vergleich verschiedener
Modelle und der Optimierung von
Hyperparametern mit dem Testset passieren?
Kompliziertere Variante:
k-fold cross validation

## Erinnerung

<!-- Folie 18 -->
Generatives Modell
Wenn es Datenpunkte
x1, x2, …, xn mit jeweils xi∊ℝn
Oben: eine Anwendung
Quelle: Scipy Lectures (CC BY)
gibt, so gibt es eine erzeugende Verteilung
(Population) einer Zufallsvariable X,
die wir nicht kennen.
Ein Modell für X besteht z.B. aus einer
Dichtefunktion oder aus einem Sampler.
Generativ,
weil man Stichproben generieren kann.

<!-- Folie 19 -->
Training
Supervised Learning
Input:
Daten
Wenn es (bekannte) Label gibt,
d.h. nicht nur Datenpunkte
x1, x2, …, xn mit jeweils xi∊ℝn
sondern auch
y1, y2, …, yn mit jeweils yi∊ℝm
Inferenz
Input:
Daten +
gefittetes
Modell
oftmals m=1 (einfache Regression)
oder sogar yi∊{0, 1} (Klassifikation)

## Anwendung

<!-- Folie 20 -->
Erinnerung
Y ∊ {0,1}
Regression
Supervised, d.h. es gibt (x,y)-Paare.
Ziel: ein funktionaler Zusammenhang
Ergebnis
f(X) als
Farbe
Y = f(X) + ε
sodass für die Stichprobe x,y
möglichst kleiner Fehler ε auftritt.

## Beispieltext mit Begriffen, die wir lernen

<!-- Folie 21 -->
https://www.hpcwire.com/2023/10/05/how
-amd-may-get-across-the-cuda-moat/
Fragen zu dem Text:
1. Was ist der Unterschied GPU/SIMD?
2. Wer entwickelt PyTorch?
3. Was ist der Unterschied CUDA/ROCm?

## Kurzgeschichte

<!-- Folie 22 -->
Bis 2010
◼ 1943: McCulloch-Pitts modellieren ein
menschliches Hirnneuron,
mit elektrischen Schaltkreisen
◼ 1958: Rosenblatt entwirft das
Perzeptron, es wurde gebaut.
kann nur linear trennbare Klassen
lernen zu unterscheiden, daher
AI WINTER
◼ 1986: Backpropagation wird erfunden,
mehr Schichten werden verwendet
Grafik CC-BY-SA
von Wikimedia
Nutzer Whiteknight

<!-- Folie 23 -->
Zum Perzeptron
Empfehlung:
Olazaran, M. (1996). A Sociological
Study of the Official History of the
Perceptrons Controversy. Social
Studies of Science, 26(3), 611–659.

<!-- Folie 24 -->
2010 -- 2015
“The Decade of Deep Learning” von Leo Gao - Lesempfehlung!
bmk.sh/2019/12/31/The-Decade-of-Deep-Learning
Highlights für diese Vorlesung:
◼ 2012 AlexNet “the paper that sparked the field of Deep Learning”
◼ 2013 word2vec, Repräsentation von Worten im latenten Raum
◼ 2014 GANs, erstmals “realistische” Bildgenerierung

<!-- Folie 25 -->
Nach 2015
Das behandeln wir in dieser Vorlesung nicht mehr:
◼ 2017 Transformers “Attention is all you need”
→ Grundlage für GPT
◼ 2020 AlphaFold 2 ‘löst’ das Proteinfaltungsproblem
→ Nobelpreis Chemie 2024
◼ 2021 Diffusionsmodelle für realistische Bildgenerierung
◼ 2022 Veröffentlichung von ChatGPT
→später RLHF, Copilot, Multimodalität, RAG, Agents, …

## Was ist ein neuronales Netz?

<!-- Folie 26 -->
MLP = Multilayer Perceptron
Die Ausgaben von mehreren (verallgemeinerten) Perzeptrons
werden als Eingabe für ein weiteres Perzeptron verwendet
(welches also eine Schicht (Layer) weiter hinten ist).

<!-- Folie 27 -->
MLP = Multilayer Perceptron
Die Ausgaben von mehreren (verallgemeinerten) Perzeptrons
werden als Eingabe für ein weiteres Perzeptron verwendet
(welches also eine Schicht (Layer) weiter hinten ist).
Dabei können die Schichten
verschieden groß sein,
manche Pfeile 0,
manche Pfeile rückwärts,
und viele verschiedene
nichtlineare Funktionen usw.
(ReLu, Convolution, SoftMax, …)

## Zum neuen Übungsblatt

<!-- Folie 28 -->
Tipps für Blatt 1
◼ Erinnern Sie sich an die Interpretation vom Kosinus eines Winkels
als Verhältnis von Seiten in einem rechtwinkligen Dreieck:
)
e
s
u
ten
b
𝛼
o
p
y
(H
cos(𝛼) = a / b
•
a (Ankathete)
◼ Was passiert im Spezialfall b=1 ?
