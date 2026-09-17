---
title: "VL 07: Handgemachte Netze und Autoencoder"
short_title: "VL 07"
---

# Handgemachte Netze und Autoencoder

:::{warning} Rohfassung
Dieses Kapitel ist eine automatische Transkription der Folien von VL 07 aus dem WiSe 2025/26
(`from_2025/slides/Einführung in Deep Learning 2025_26 VL 07_ Autoencoder.pdf`), Folie für Folie in der Originalreihenfolge.
Formeln und Abbildungen sind dabei größtenteils verloren gegangen; der Text ist noch nicht überarbeitet.
:::

## Handgemachte Netze

<!-- Folie 2 -->

## Das Geheimnis um Deep Learning lüften

<!-- Folie 3 -->
Warum (wie genau) funktioniert Deep Learning so gut?
Zutaten (bisher):
◼
◼
◼
Das einzelne Neuron = Skalarprodukt + Aktivierungsfunktion
Gradientenabstieg: lernen in Richtung der Ableitung einer Loss-Funktion
Backpropagation: clever Ableitung berechnen für tiefe Netze

<!-- Folie 4 -->
Warum (wie genau) funktioniert Deep Learning so gut?
Zutaten:
◼
◼
◼
◼
◼
◼
Das einzelne Neuron = Skalarprodukt + Aktivierungsfunktion
Gradientenabstieg: lernen in Richtung der Ableitung einer Loss-Funktion
Backpropagation: clever Ableitung berechnen für tiefe Netze
Sinnvolle Loss-Funktionen festlegen:
← Heute!
Regression mit MSE und (binäre) Klassifikation mit (B)CE, BCE vs NLL, DKL
Architekturen neben einfachen MLPs wie z.B. Autoencoder
← Heute!
Damit auch Representation Learning, Transfer Learning
Regularisierung und Tricks gegen verschwindende Gradienten
← Heute!

<!-- Folie 5 -->
Warum (wie genau) funktioniert Deep Learning so gut?
Zutaten:
◼
◼
◼
◼
◼
◼
◼
◼
Das einzelne Neuron = Skalarprodukt + Aktivierungsfunktion
Gradientenabstieg: lernen in Richtung der Ableitung einer Loss-Funktion
Backpropagation: clever Ableitung berechnen für tiefe Netze
Sinnvolle Loss-Funktionen festlegen:
← Heute!
Regression mit MSE und (binäre) Klassifikation mit (B)CE, BCE vs NLL, DKL
Architekturen neben einfachen MLPs wie z.B. Autoencoder
← Heute!
Damit auch Representation Learning, Transfer Learning
Regularisierung und Tricks gegen verschwindende Gradienten
← Heute!
Hyperparameter wählen/optimieren,
alles hängt von den Daten ab…
Elementare Funktionen sind leicht approximierbar
← jetzt kurz

## Parameter von Hand wählen

<!-- Folie 6 -->
Easy mode: Boolesche Variablen
x,y ∊ {0, 1} = {FALSE, TRUE}
f : ℝ2 → ℝ,
f(x,y) := x OR y
Also f(0,0)=0, f(1,0)=1, f(0,1)=1, f(1,1)=1
Welches neuronale Netz berechnet als Inferenz/Forward die Funktion f?

<!-- Folie 7 -->
Easy mode: Boolesche Variablen
x,y ∊ {0, 1} = {FALSE, TRUE}
f : ℝ2 → ℝ,
f(x,y) := x OR y
Also f(0,0)=0, f(1,0)=1, f(0,1)=1, f(1,1)=1
Welches neuronale Netz berechnet als Inferenz/Forward die Funktion f?
Idee: schreibe die Funktion f als
Verkettung von gewichteten Summen (=Skalarprodukte)
und Aktivierungsfunktionen (z.B. [x > 0] oder ReLU(x):=max(0,x))

<!-- Folie 8 -->
Easy mode: Boolesche Variablen
x,y ∊ {0, 1} = {FALSE, TRUE}
f : ℝ2 → ℝ,
f(x,y) := x OR y
Also f(0,0)=0, f(1,0)=1, f(0,1)=1, f(1,1)=1
Welches neuronale Netz berechnet als Inferenz/Forward die Funktion f?
Idee: schreibe die Funktion f als
Verkettung von gewichteten Summen (=Skalarprodukte)
und Aktivierungsfunktionen (z.B. [x > 0] oder ReLU(x):=max(0,x))
Idee: interpoliere OR, d.h. Entscheide, was z.B. f(0.5, 0) sein soll.
Idee: extrapoliere OR, d.h. Entscheide, was z.B. f(-1, 2) sein soll.

<!-- Folie 9 -->
Easiest mode: eindimensional
x ∊ ℝ mit der Interpretation (x ≤ 0)=FALSE, (x ≥ 1)=TRUE
n : ℝ → ℝ,n(x) := NOT x
Also n(0)=1, n(1)=0, allgemeiner n(x) ≤ 0 falls x ≥ 1
Welches neuronale Netz berechnet als Inferenz/Forward die Funktion n?

<!-- Folie 10 -->
Easiest mode: eindimensional
x ∊ ℝ mit der Interpretation (x ≤ 0)=FALSE, (x ≥ 1)=TRUE
n : ℝ → ℝ,n(x) := NOT x
Also n(0)=1, n(1)=0, allgemeiner n(x) ≤ 0 falls x ≥ 1
Welches neuronale Netz berechnet als Inferenz/Forward die Funktion n?
n(x) = 1 - x
erfüllt die Eigenschaft, NOT zu inter/extrapolieren.
Neuronales Netz: 1 Neuron, Gewicht w = -1, Bias b = +1, Aktivierungsfunktion id.

<!-- Folie 11 -->
Zurück zu OR
x,y ∊ ℝ mit der Interpretation (x ≤ 0)=FALSE, (x ≥ 1)=TRUE
f : ℝ2 → ℝ,
f(x,y) := x OR y
Also f(0,0)=0, f(1,0)=1, f(0,1)=1, f(1,1)=1
Welches neuronale Netz berechnet als Inferenz/Forward die Funktion f?
Ansatz: f(x,y) = x+y
leider f(1,1)=2 ≠ 1

<!-- Folie 12 -->
Zurück zu OR
x,y ∊ ℝ mit der Interpretation (x ≤ 0)=FALSE, (x ≥ 1)=TRUE
f : ℝ2 → ℝ,
f(x,y) := x OR y
Also f(0,0)=0, f(1,0)=1, f(0,1)=1, f(1,1)=1
Welches neuronale Netz berechnet als Inferenz/Forward die Funktion f?
Ansatz: f(x,y) = [x+y > 0]
Ein Neuron, Gewichtsvektor (1, 1), kein Bias (bzw. Bias b=0),
Aktivierungsfunktion ist [x > 0] mit Werten in 0,1

## x,y ∊ ℝ mit der Interpretation

<!-- Folie 13 -->
(x ≤ 0)=F=FALSE,
(x > 0)=T=TRUE

## Parameter von Hand wählen

<!-- Folie 14 -->
Zurück zu OR
x,y ∊ ℝ mit der Interpretation (x ≤ 0)=FALSE, (x > 0)=TRUE
f : ℝ2 → ℝ,
f(x,y) := x OR y
Also f(0,0)=0, f(1,0)=1, f(0,1)=1, f(1,1)=1
Welches neuronale Netz berechnet als Inferenz/Forward die Funktion f?
Ansatz: f(x,y) = [x+y > 0]
Ein Neuron, Gewichtsvektor (1, 1), kein Bias (bzw. Bias b=0),
Aktivierungsfunktion ist [x > 0] mit Werten in 0,1
oder die softere Variante f(x,y) := x+y oder 𝜎(x+y)
Besser: f(x,y) := ReLU(x) + ReLU(y)

<!-- Folie 15 -->
Komplizierteres aus Einfachem:
x,y ∊ ℝ mit der Interpretation (x ≤ 0)=F=FALSE, (x > 0)=T=TRUE
g : ℝ2 → ℝ,
g(x,y) := x NOR y
g(F,F)=T, g(F,T)=F, g(T,F)=F, g(T,T)=F
Welches neuronale Netz berechnet als Inferenz/Forward die Funktion g?

## x,y ∊ ℝ mit der Interpretation

<!-- Folie 16 -->
(x ≤ 0)=F=FALSE,
(x > 0)=T=TRUE

## Parameter von Hand wählen

<!-- Folie 17 -->
Komplizierteres aus Einfachem:
x,y ∊ ℝ mit der Interpretation (x ≤ 0)=F=FALSE, (x > 0)=T=TRUE
g : ℝ2 → ℝ,
g(x,y) := x NOR y
g(F,F)=T, g(F,T)=F, g(T,F)=F, g(T,T)=F
Welches neuronale Netz berechnet als Inferenz/Forward die Funktion g?
NOR = NOT OR, also g(x,y) = n(f(x,y)) für ein f, welches OR implementiert, z.B.
f(x,y) := ReLU(x) + ReLU(y) und n(x) := 1 - x
⇒ g(x,y) := 1 - (ReLU(x) + ReLU(y)),
also:
erste Schicht Gewicht (1, 1), Bias 0 und ReLU,
zweite Schicht Gewicht -1, Bias 1 und id.

## x,y ∊ ℝ mit der Interpretation

<!-- Folie 18 -->
(x ≤ 0)=F=FALSE,
(x > 0)=T=TRUE

<!-- Folie 19 -->
(x ≤ 0)=F=FALSE,
(x > 0)=T=TRUE

## Parameter von Hand wählen

<!-- Folie 20 -->
Weiter so?
x,y ∊ ℝ mit der Interpretation (x ≤ 0)=F=FALSE, (x > 0)=T=TRUE
f : ℝ2 → ℝ,
f(x,y) := x XOR y
Welches neuronale Netz berechnet als Inferenz/Forward die Funktion f?

## x,y ∊ ℝ mit der Interpretation

<!-- Folie 21 -->
(x ≤ 0)=F=FALSE,
(x > 0)=T=TRUE

## Parameter von Hand wählen

<!-- Folie 22 -->
Weiter so?
x,y ∊ ℝ mit der Interpretation (x ≤ 0)=F=FALSE, (x > 0)=T=TRUE
f : ℝ2 → ℝ,
f(x,y) := x XOR y
Welches neuronale Netz berechnet als Inferenz/Forward die Funktion f?
Die “Region” XOR in der Ebene, also die Punkte (x,y) mit XOR(x,y) > 0
ist der Schnitt von NAND(x,y) > 0 mit OR(x,y) > 0
XOR(x,y) = AND( NAND(x,y), OR(x,y) )
⇒ Mit 4 Hidden Layer zu je 4 Neuronen müsste es klappen

## Gradientenabstieg/Backprop findet auch diese Approximation mit 3 Hidden Layer:

<!-- Folie 23 -->

## Gradientenabstieg/Backprop findet auch diese Approximation mit 2 Hidden Layer:

<!-- Folie 24 -->

## Take-Home Message

<!-- Folie 25 -->
Wir haben gesehen:
Boolesche Funktionen lassen sich mit neuronalen Netzen darstellen/approximieren,
D.h. es gibt Gewichte sodass die resultierende Funktion tut, was sie soll.
Also kann auch Optimierung diese idealen Gewichte finden.
Aus elementaren Funktionen lassen sich komplexe verknüpfen,
neuronale Netze können aber auch “Abkürzungen” nehmen,
und Platz verschwenden (überflüssige Neuronen).

## Parameter von Hand wählen

<!-- Folie 26 -->
Arithmetik
Wie können wir z.B.
mit einem neuronalen Netz berechnen / approximieren?

<!-- Folie 27 -->
Arithmetik
Wie können wir z.B.
mit einem neuronalen Netz berechnen / approximieren?
Einfachere Probleme, die wir nicht lösen können:

## Auf [-3, +3] approximieren wir x²

<!-- Folie 28 -->
mit einer stückweise linearen Funktion
an ganzzahligen Stützstellen

<!-- Folie 29 -->
mit einer stückweise linearen Funktion
an ganzzahligen Stützstellen
(Symmetrie ignoriert - geht das besser?)

<!-- Folie 30 -->
mit einer stückweise linearen Funktion
an ganzzahligen Stützstellen

## Parameter von Hand wählen

<!-- Folie 31 -->
Arithmetik
Wenn x2 gut approximiert werden kann, dann auch xy über die
Polarisationsidentität:

<!-- Folie 32 -->
Arithmetik
Wenn x2 gut approximiert werden kann, dann auch xy über die
Polarisationsidentität:
Damit setzen wir für eine Approximation Q der Quadratfunktion:

## Take-Home Message

<!-- Folie 33 -->
Wir haben gesehen:
Funktionen lassen sich mit neuronalen Netzen darstellen/approximieren.

<!-- Folie 34 -->
Wir haben gesehen:
Funktionen lassen sich mit neuronalen Netzen darstellen/approximieren.
Mit LUT und Interpolation sind beliebig gute Näherungen auf beschränkten
Definitionsbereichen möglich → so rechnet auch die GPU z.B. Sinus aus.
Außerhalb der Stützstellen wird die Approximation beliebig schlecht
⇒ Neuronale Netze interpolieren gut, extrapolieren schlecht.

## Zeit für eine Pause?

<!-- Folie 35 -->

## Autoencoder

<!-- Folie 36 -->

<!-- Folie 37 -->
Wie letztes Mal bereits …
Das Autoencoder-Layout
Regression,
Input: Vektor x der Länge D
Encoder: reduziert in mehreren Schichten
von Dimension D auf Dimension L
Decoder: erhöht in mehreren Schichten von
Dimension L auf Dimension D
Input/Output im “Datenraum”
(bei Bildern: “Pixelraum”, pixel space)
Flaschenhals-Hidden Layer, Dimension L
“Latenter Raum”, latent space
(Grafik mit NN-SVG erstellt)

## Anwendungsbeispiel

<!-- Folie 38 -->
MNIST
28x28 Graustufen-Bilder
handgeschriebener Ziffern 0-9 (mit Label)

<!-- Folie 39 -->
MNIST
28x28 Graustufen-Bilder
handgeschriebener Ziffern 0-9
Mögliche Tasks:
◼
◼
◼
◼
Unsupervised Kompression der Bilder
Unsupervised neue Bilder generieren
Supervised Klassifikation
Supervised neue Bilder mit
vorgegebener Ziffer generieren

<!-- Folie 40 -->
MNIST
28x28 Graustufen-Bilder
handgeschriebener Ziffern 0-9
Mögliche Tasks:
◼
◼
◼
◼
Unsupervised Kompression der Bilder
Unsupervised neue Bilder generieren
Supervised Klassifikation
Supervised neue Bilder mit
vorgegebener Ziffer generieren
Kompression:
Autoencoder = Encoder + Decoder,
Encoder ist der Kompressor
Neue Bilder generieren:
Verteilung der Punkte im latenten Raum
modellieren, sampeln, dekodieren.

<!-- Folie 41 -->
MNIST
28x28 Graustufen-Bilder
handgeschriebener Ziffern 0-9
Mögliche Tasks:
◼
Unsupervised Kompression der Bilder
◼
Supervised Klassifikation
Heute:
◼
◼
Accuracy erhöhen
Overfitten vermeiden

<!-- Folie 42 -->
MNIST
28x28 Graustufen-Bilder
handgeschriebener Ziffern 0-9
Variationsmöglichkeiten:
◼
◼
◼
Daten modifizieren (putzen?)
Modellarchitektur (tiefer?)
Trainings-Hyperparameter
(wie genau wird gelernt?)
Heute:
◼
◼
Accuracy erhöhen
Overfitten vermeiden

## Code-Beispiel, Modell-Architektur

<!-- Folie 43 -->
Visualisierung mit Netron und
torch.save(model, 'model.pth')

## Code-Beispiel, Training

<!-- Folie 44 -->

## Tricks zur Verbesserung des Trainings

<!-- Folie 45 -->

## Tricks beim Training

<!-- Folie 46 -->
◼
Mehr Epochen trainieren!

<!-- Folie 47 -->
◼
Mehr Epochen trainieren!
◼
◼
Lernrate anpassen - statt lr=1e3 mal mit lr=1e2 probieren!
Die Gewichte können zu groß werden, dann kann man eine L2-Regularisierung
nutzen, den Weight Decay (als Parameter für den Optimierer, wie die Lernrate).
weight_decay=1e-5

<!-- Folie 48 -->
◼
Mehr Epochen trainieren!
◼
◼
Lernrate anpassen - statt lr=1e3 mal mit lr=1e2 probieren!
Die Gewichte können zu groß werden, dann kann man eine L2-Regularisierung
nutzen, den Weight Decay (als Parameter für den Optimierer, wie die Lernrate).
weight_decay=1e-5
SGD kann sehr langsam sein. Es gibt eine ganze Reihe von Tricks wie z.B. eine
adaptive Lernrate und cleveres Mitteln über mehrere Batches hinweg, die in Adam
implementiert sind.
◼

<!-- Folie 49 -->
◼
Mehr Epochen trainieren!
◼
◼
Lernrate anpassen - statt lr=1e3 mal mit lr=1e2 probieren!
Die Gewichte können zu groß werden, dann kann man eine L2-Regularisierung
nutzen, den Weight Decay (als Parameter für den Optimierer, wie die Lernrate).
weight_decay=1e-5
SGD kann sehr langsam sein. Es gibt eine ganze Reihe von Tricks wie z.B. eine
adaptive Lernrate und cleveres Mitteln über mehrere Batches hinweg, die in Adam
implementiert sind.
Oft ist I/O oder die CPU ein Bottleneck beim Laden der Daten.
Im Konstruktor des DataLoaders mit anderen batch_sizes experimentieren
(im Zweifel mehr, bis Out of Memory).
Mehrere CPU-Kerne zum Laden der Daten nutzen:
num_workers=8
◼
◼
◼

## Label Autoencoder

<!-- Folie 50 -->

## Label Klassifikator

<!-- Folie 51 -->
Supervised: Klassifikator
Ein “klassischer” Klassifikator-Ansatz:
Encoder vom Autoencoder
Linearer Layer auf 10 Dimensionen
Softmax
Zur “harten” Klassifikation noch ein argmax
dahinter hängen.

<!-- Folie 52 -->
Supervised: Klassifikator
Ein “klassischer” Klassifikator-Ansatz:
Encoder vom Autoencoder
Linearer Layer auf 10 Dimensionen
Softmax
Zur “harten” Klassifikation noch ein argmax
dahinter hängen.
Loss-Funktion:
Negative log likelihood
= Kreuzentropie
≘ Kullback-Leibler-Divergenz
zwischen echten Labels
und Vorhersage
“classification loss”
(Im Gegensatz zum “reconstruction loss”)

## Label Autoencoder

<!-- Folie 53 -->
Supervised: Klassifikator
Encoder vom Autoencoder
Linearer Layer auf 10 Dimensionen
Softmax
Daneben Decoder vom Autoencoder
Loss-Funktion:
reconstruction_loss
+
classification_loss
Input: Bild
Output: Rekonstruktion, Label-Vorhersage

## Tricks zur Erhöhung der Accuracy

<!-- Folie 55 -->

## Tricks bei der Modellarchitektur

<!-- Folie 56 -->
◼
Mehr Layer!

<!-- Folie 57 -->
◼
Mehr Layer!
◼
Dem Problem sterbender Neuronen entgegen wirken mit anderen
Aktivierungsfunktionen als ReLU, z.B. dem Swish (in Pytorch SiLU).

<!-- Folie 58 -->
◼
Mehr Layer!
◼
Dem Problem sterbender Neuronen entgegen wirken mit anderen
Aktivierungsfunktionen als ReLU, z.B. dem Swish (in Pytorch SiLU).
◼
Dropout-Layer:
Zufällig ein paar Einträge des eingehenden Vektors auf 0 setzen.
Verhindert zu starke Konzentration auf einige wenige Neuronen.

<!-- Folie 59 -->
◼
Mehr Layer!
◼
Dem Problem sterbender Neuronen entgegen wirken mit anderen
Aktivierungsfunktionen als ReLU, z.B. dem Swish (in Pytorch SiLU).
◼
Dropout-Layer:
Zufällig ein paar Einträge des eingehenden Vektors auf 0 setzen.
Verhindert zu starke Konzentration auf einige wenige Neuronen.
◼
Batch Normalization Layer:
Nach jedem Batch den Output des vorigen Layers auf eine Normalverteilung
normieren. Die Transformation (Skalierung und Translation) auf eine andere
Normalverteilung als Standard sind erlernbare Gewichte dieses Layers.
→ theoretisch etwas kompliziert (wieso es nützt), praktisch sehr nützlich
