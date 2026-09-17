---
title: "VL 10: Convolutional Neural Networks"
short_title: "VL 10"
---

# Convolutional Neural Networks

:::{warning} Rohfassung
Dieses Kapitel ist eine automatische Transkription der Folien von VL 10 aus dem WiSe 2025/26
(`from_2025/slides/Einführung in Deep Learning 2025_26 VL 10_ Convolution (CNN).pdf`), Folie für Folie in der Originalreihenfolge.
Formeln und Abbildungen sind dabei größtenteils verloren gegangen; der Text ist noch nicht überarbeitet.
:::

## Motivation zur Faltung

<!-- Folie 2 -->

<!-- Folie 3 -->
Bildverarbeitung: it’s a blur

<!-- Folie 4 -->
Bildverarbeitung: make a difference (Kanten finden)
-
=

<!-- Folie 5 -->
Das menschliche Auge erkennt Kanten(orientierung)
Antwort eines Neurons auf Balken unterschiedlicher Orientierung,
Grafik von Hubel & Wiesel (1959)
Reproduktion von Wurtz (1969) →
aus Robert H Wurtz: “Recounting the impact of Hubel and Wiesel” J Physiol.
2009 Jun 15;587(Pt 12):2817–2823. doi: 10.1113/jphysiol.2009.170209
← Grafik von Wikipedia Nutzer
“Mads00”, CC-BY-SA

<!-- Folie 6 -->
In der Informatik
Abgesehen von CNN = Convolutional Neural Networks
ist Faltung zentrales Instrument in der Signalverarbeitung.
Das (1D) ist auch leichter zu verstehen (als 2D),
damit fangen wir an.

## Eindimensionale Faltung

<!-- Folie 7 -->

## 1-Dimensionale Konvolution

<!-- Folie 8 -->
Definition (diskret)

<!-- Folie 9 -->
Definition (diskret)

<!-- Folie 10 -->
Definition (diskret)

<!-- Folie 11 -->
Interpretation der Definition
Da steht ein Skalarprodukt des Vektors (f(-n),...,f(n))
mit (g(x+n),...,g(x-n)).
Rechnung: nimm einen [-n,+n]-Ausschnitt von g, zentriert bei x,
dann flippen (bei x spiegeln) und dann Skalarprodukt mit f.

<!-- Folie 12 -->
Interpretation der Definition
Wir möchten jetzt das Signal rechts
mit einem Filter falten.
Der Filter:

<!-- Folie 13 -->
Interpretation der Definition
Wir möchten jetzt das Signal rechts
mit einem Filter falten.
Der Filter:

<!-- Folie 14 -->
Interpretation der Definition
Zum direkten Vergleich nochmal untereinander:
Achtung: die
Skalen sind hier
ungünstig
beschriftet.

## Noch mehr Faltungen

<!-- Folie 15 -->

## 1-Dimensionale Konvolution

<!-- Folie 16 -->
Programmierung
Für den Code schauen wir ins
Notebook (VL10-convolutions)

<!-- Folie 17 -->
Das Faltungstheorem
Für zwei stetige Funktionen f,g und die stetige Faltung (Integral statt
Summe) gilt für die Fouriertransformation F:
D.h. Faltung im Ortsraum ist Multiplikation im Frequenzraum.
Auch:

<!-- Folie 18 -->
Das Faltungstheorem
Kurzer Ausflug in die
Fourier-Transformation?
www.robots.ox.ac.uk/~az/le
ctures/ia/lect2.pdf

## 1-Dimensionales Pooling

<!-- Folie 19 -->

<!-- Folie 20 -->
Pooling ≈ Binning
Binning = Array in feste disjunkte Blöcke
(ohne Überlapp) zerlegen
+ Summe/Mittelwert bilden

<!-- Folie 21 -->
Pooling ≈ Binning
Binning = Array in feste disjunkte Blöcke
(ohne Überlapp) zerlegen
+ Summe/Mittelwert bilden
≈ Faltung mit einer Kastenfunktion,
nur wenige Werte verwenden.

<!-- Folie 22 -->
Pooling ≈ Binning
Binning = Array in feste disjunkte Blöcke
(ohne Überlapp) zerlegen
+ Summe/Mittelwert bilden
≈ Faltung mit einer Kastenfunktion,
nur wenige Werte verwenden.
Wie viel Überlapp =: stride (Schrittlänge)

<!-- Folie 23 -->
Pooling ≈ Binning
Binning = Array in feste disjunkte Blöcke
(ohne Überlapp) zerlegen
+ Summe/Mittelwert bilden
≈ Faltung mit einer Kastenfunktion,
nur wenige Werte verwenden.
Wie viel Überlapp =: stride (Schrittlänge)
Pooling = Array in feste Blöcke
(mit Überlapp) einteilen
Average-Pooling = Pooling
+ Mittelwert der Blöcke
Max-Pooling = Pooling
+ Maximum der Blöcke

<!-- Folie 24 -->
Pooling-Beispiel
Pooling eines Vektors (a,b,c,d)
Mit Schrittlänge (stride) 1 und Poolgröße 2
Pools: [ (a,b), (b,c), (c,d) ]

<!-- Folie 25 -->
Pooling-Beispiel
Pooling eines Vektors (a,b,c,d)
Mit Schrittlänge (stride) 1 und Poolgröße 2
Pools: [ (a,b), (b,c), (c,d) ]
Mit Schrittlänge 2, Poolgröße 2:
Pools: [ (a,b), (c,d) ]

<!-- Folie 26 -->
Pooling-Beispiel
Pooling eines Vektors (a,b,c,d)
Mit Schrittlänge (stride) 1 und Poolgröße 2
Pools: [ (a,b), (b,c), (c,d) ]
Mit Schrittlänge 2, Poolgröße 2:
Pools: [ (a,b), (c,d) ]
Mit Schrittlänge 1, Poolgröße 3:
Pools: [ (a,b,c), (b,c,d) ]

<!-- Folie 27 -->
Pooling-Beispiel
Pooling eines Vektors (a,b,c,d)∊ℝ4
Mit Schrittlänge (stride) 1 und Poolgröße 2
Pools: [ (a,b), (b,c), (c,d) ]
Von 4 Inputs reduzieren wir die
Datenmenge also auf 3 oder 2 Outputs,
Je nach Größe und Stride.
Mit Schrittlänge 2, Poolgröße 2:
Pools: [ (a,b), (c,d) ]
Mit Schrittlänge 1, Poolgröße 3:
Pools: [ (a,b,c), (b,c,d) ]

<!-- Folie 28 -->
Pooling-Beispiel
Pooling eines Vektors (a,b,c,d)∊ℝ4
Mit Schrittlänge (stride) 1 und Poolgröße 2
Pools: [ (a,b), (b,c), (c,d) ]
Von 4 Inputs reduzieren wir die
Datenmenge also auf 3 oder 2 Outputs,
Je nach Größe und Stride.
Mit Schrittlänge 2, Poolgröße 2:
Pools: [ (a,b), (c,d) ]
Average-Pooling:
Output: [ mean(a,b), mean(c,d) ]
Mit Schrittlänge 1, Poolgröße 3:
Pools: [ (a,b,c), (b,c,d) ]
Max-Pooling:
Output: [ max(a,b,c), max(b,c,d) ]

## 2-Dimensionale Konvolution

<!-- Folie 29 -->

<!-- Folie 30 -->
Beispiel mit GIMP (≈Photoshop)
Unten: Output der 2D Faltung

## CNNs

<!-- Folie 31 -->

## 1-Dimensionale CNNs

<!-- Folie 32 -->
→später ins Notebook schauen
Tipp: “Dog filter” = “DoG filter” = Difference-of-Gaussians filter ist kein Snapchat Filter.

## 2-Dimensionale CNNs

<!-- Folie 33 -->
→Animationen von Vincent Dumoulin, Francesco Visin
github.com/vdumoulin/conv_arithmetic
→Interaktives MNIST-CNN-Explorationswerkzeug von Adam Harley
https://adamharley.com/nn_vis/cnn/2d.html
→Für Code ins Notebook schauen!
