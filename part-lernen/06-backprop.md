---
title: "VL 06: Backpropagation"
short_title: "VL 06"
---

# Backpropagation

:::{warning} Rohfassung
Dieses Kapitel ist eine automatische Transkription der Folien von VL 06 aus dem WiSe 2025/26
(`from_2025/slides/Einführung in Deep Learning 2025_26 VL 06_ Backprop.pdf`), Folie für Folie in der Originalreihenfolge.
Formeln und Abbildungen sind dabei größtenteils verloren gegangen; der Text ist noch nicht überarbeitet.
:::

## Ziel für heute

<!-- Folie 2 -->
Ziel: Verstehen können, was dort geschieht:
TensorFlow Playground
https://playground.tensorflow.org
Übungsaufgabe:
Setzen Sie
Gewichte von Hand
mit 2 Hidden Layer
zu je 2 Neuronen,
um das XOR
Problem zu lösen

## Training mehrerer Schichten:

<!-- Folie 3 -->
Backpropagation (Motivation)

## Backpropagation

<!-- Folie 4 -->
Beispielsetup 1
Eingabedaten sind eindimensional,
ein einzelnes Neuron mit Aktivierungsfunktion 𝜎 produziert Ausgabe,
die stecken wir in ein zweites Neuron mit Aktivierungsfunktion id.
x
werst
𝜎
wzweit
ypred

<!-- Folie 5 -->
Beispielsetup 1
Eingabedaten sind eindimensional,
ein einzelnes Neuron mit Aktivierungsfunktion 𝜎 produziert Ausgabe,
die stecken wir in ein zweites Neuron mit Aktivierungsfunktion id.
Also: ypred = 〈wzweit, 𝜎(〈werst, x〉)〉
x
werst
𝜎
wzweit
ypred

<!-- Folie 6 -->
Beispielsetup 1
Eingabedaten sind eindimensional,
ein einzelnes Neuron mit Aktivierungsfunktion 𝜎 produziert Ausgabe,
die stecken wir in ein zweites Neuron mit Aktivierungsfunktion id.
Also: ypred = 〈wzweit, 𝜎(〈werst, x〉)〉
x
werst
𝜎
wzweit
ypred
Wir planen eine Regression mit x,y ∊ ℝ, daher nehmen wir den MSE Loss:
L(x,y; w) = MSE(y,ypred) = Σi=1..N (yi-ypred,i)2

<!-- Folie 7 -->
Beispielsetup 1
Eingabedaten sind eindimensional,
ein einzelnes Neuron mit Aktivierungsfunktion 𝜎 produziert Ausgabe,
die stecken wir in ein zweites Neuron mit Aktivierungsfunktion id.
Also: ypred = 〈wzweit, 𝜎(〈werst, x〉)〉
x
werst
𝜎
wzweit
ypred
Wir planen eine Regression mit x,y ∊ ℝ, daher nehmen wir den MSE Loss:
L(x,y; w) = MSE(y,ypred) = Σi=1..N (yi-ypred,i)2 → L’(w) = Σi=1..N 2(yi-ypred,i)(-d/dw ypred,i)

<!-- Folie 8 -->
Beispielsetup 1
Eingabedaten sind eindimensional,
ein einzelnes Neuron mit Aktivierungsfunktion 𝜎 produziert Ausgabe,
die stecken wir in ein zweites Neuron mit Aktivierungsfunktion id.
Also: ypred = 〈wzweit, 𝜎(〈werst, x〉)〉
x
werst
𝜎
wzweit
ypred
ypred’ = ?
Wir planen eine Regression mit x,y ∊ ℝ, daher nehmen wir den MSE Loss:
L(x,y; w) = MSE(y,ypred) = Σi=1..N (yi-ypred,i)2 → L’(w) = Σi=1..N 2(yi-ypred,i)(-d/dw ypred,i)

## Backpropagation preparation

<!-- Folie 9 -->
Beispielsetup 1
Nehmen wir W = (werst, wzweit), können wir ypred als Funktion von W auffassen:
ypred(W) = 〈wzweit, 𝜎(〈werst, x〉)〉
Ableitung nach W wie zuvor berechnet in Komponenten.
Was ist die Ableitung von 𝜎(f(w)) nach w?
Was ist die Ableitung von 〈w, f(x)〉 nach w oder x?

<!-- Folie 10 -->
Beispielsetup 1
Nehmen wir W = (werst, wzweit), können wir ypred als Funktion von W auffassen:
ypred(W) = 〈wzweit, 𝜎(〈werst, x〉)〉
Ableitung nach W wie zuvor berechnet in Komponenten.
d/dwerst ypred(W) =
Was ist die Ableitung von 𝜎(f(w)) nach w?
Kettenregel: d/dw 𝜎(f(w)) =
Was ist die Ableitung von 〈w, f(x)〉 nach w oder x?
d/dw 〈w,x〉 = ? und d/dw 〈v, f(w)〉 = ?

<!-- Folie 11 -->
Beispielsetup 1
Nehmen wir W = (werst, wzweit), können wir ypred als Funktion von W auffassen:
ypred(W) = 〈wzweit, 𝜎(〈werst, x〉)〉
Ableitung nach W wie zuvor berechnet in Komponenten.
d/dwerst ypred(W) =
Was ist die Ableitung von 𝜎(f(w)) nach w?
Kettenregel: d/dw 𝜎(f(w)) = 𝜎’(f(w)) f’(w)
Was ist die Ableitung von 〈w, f(x)〉 nach w oder x?
d/dw 〈w,x〉 = x und d/dw 〈v, f(w)〉 = 〈v, f’(w)〉

<!-- Folie 12 -->
Beispielsetup 1
Nehmen wir W = (werst, wzweit), können wir ypred als Funktion von W auffassen:
ypred(W) = 〈wzweit, 𝜎(〈werst, x〉)〉
Ableitung nach W wie zuvor berechnet in Komponenten.
d/dwerst ypred(W) = 〈 wzweit, 𝜎’(〈werst, x〉)x 〉
d/dwzweit ypred(W) = 𝜎(〈werst, x〉)
Kettenregel: d/dw 𝜎(f(w)) = 𝜎’(f(w)) f’(w)
d/dw 〈w,x〉 = x und d/dw 〈v, f(w)〉 = 〈v, f’(w)〉

## Backpropagation

<!-- Folie 13 -->
Beispielsetup 1
ypred = 〈wzweit, 𝜎(〈werst, x〉)〉
x
werst
𝜎
wzweit
ypred
L(x,y; w) = MSE(y,ypred) = Σi=1..N (yi-ypred,i)2
L’(w) = Σi=1..N 2(yi-ypred,i)(-d/dw ypred,i)
d/dwerst ypred(W) = 〈 wzweit, 𝜎’(〈werst, x〉)x 〉
d/dwzweit ypred(W) = 𝜎(〈werst, x〉)
wzweit, neu = wzweit, alt - ρ Σi=1..N 2(yi-ypred,i)(-𝜎(〈werst,alt, x〉))

<!-- Folie 14 -->
Beispielsetup 1
ypred = 〈wzweit, 𝜎(〈werst, x〉)〉
x
werst
𝜎
ypred
wzweit
L(x,y; w) = MSE(y,ypred) = Σi=1..N (yi-ypred,i)2
L’(w) = Σi=1..N 2(yi-ypred,i)(-d/dw ypred,i)
d/dwerst ypred(W) = 〈 wzweit, 𝜎’(〈werst, x〉)x 〉
d/dwzweit ypred(W) = 𝜎(〈werst, x〉)
wzweit, neu = wzweit, alt + ρ Σi=1..N 2(yi-〈wzweit,alt, 𝜎(〈werst,alt, x〉)〉)(𝜎(〈werst,alt,
x〉))

<!-- Folie 15 -->
Beispielsetup 1
ypred = 〈wzweit, 𝜎(〈werst, x〉)〉
x
werst
𝜎
wzweit
ypred
L(x,y; w) = MSE(y,ypred) = Σi=1..N (yi-ypred,i)2
L’(w) = Σi=1..N 2(yi-ypred,i)(-d/dw ypred,i)
d/dwerst ypred(W) = 〈 wzweit, 𝜎’(〈werst, x〉)x 〉
d/dwzweit ypred(W) = 𝜎(〈werst, x〉)
werst, neu = werst, alt + ρ Σi=1..N 2(yi-〈wzweit,alt, 𝜎(〈werst,alt, x〉)〉)(〈 wzweit,alt, 𝜎’(〈werst,alt,
x〉)x 〉)

<!-- Folie 16 -->
Beispielsetup 2
Eingabedaten sind zweidimensional,
ein einzelnes Neuron mit Aktivierungsfunktion 𝜎 produziert Ausgabe,
die stecken wir in ein zweites Neuron mit Aktivierungsfunktion id.
Also: ypred = 〈wzweit, 𝜎(〈werst, x〉)〉
Jetzt neu: werst ∊ ℝ2
x1
werst
𝜎
wzweit
ypred
x2

<!-- Folie 17 -->
Beispielsetup 3
Eingabedaten sind zweidimensional,
zwei Neuronen mit Aktivierungsfunktion 𝜎 produzieren Ausgabe,
die stecken wir in ein drittes Neuron mit Aktivierungsfunktion id.
Also: ypred = 〈w, (𝜎〈u, x〉, 𝜎〈v, x〉)〉
x1
u
𝜎
w
Jetzt neu: u,v,w ∊ ℝ2
x2
v
ypred
𝜎

## Layer

<!-- Folie 18 -->
Mehrere Neuronen, die parallel verarbeitet
werden, bilden eine Schicht (Layer).
Mehrmals Lineare Regression
= Multilineare Regression
= “Linear Layer”
= 1 Matrix, Zeilen sind Gewichtsvektoren

## Backpropagation

<!-- Folie 19 -->
Beispielsetup 3
Eingabedaten sind zweidimensional,
zwei Neuronen mit Aktivierungsfunktion 𝜎 produzieren Ausgabe,
die stecken wir in ein drittes Neuron mit Aktivierungsfunktion id.
Also: ypred = 〈w, (𝜎〈u, x〉, 𝜎〈v, x〉)〉
= 〈w, 𝜎Ax〉
x1
u
𝜎
w
x2
v
ypred
𝜎
(Schreibe u,v als Zeilen in eine Matrix A
und benutze 𝜎 auf Vektoren komponentenweise.)

<!-- Folie 20 -->
Beispielsetup 3
ypred = 〈w, (𝜎〈u, x〉, 𝜎〈v, x〉)〉
= 〈w, 𝜎Ax〉 = wT𝜎Ax (Schreibe u,v als Zeilen in eine Matrix A und benutze 𝜎 auf Vektoren
komponentenweise.)
u1 = A11 also
d/du1 = d/dA11
x1
u
𝜎
w
d/dA ypred
T
= d/dA w 𝜎Ax
=?
x2
v
ypred
𝜎

<!-- Folie 21 -->
Beispielsetup 3
ypred = 〈w, (𝜎〈u, x〉, 𝜎〈v, x〉)〉
= 〈w, 𝜎Ax〉 = wT𝜎Ax (Schreibe u,v als Zeilen in eine Matrix A und benutze 𝜎 auf Vektoren
komponentenweise.)
u1 = A11 also
d/du1 = d/dA11
x1
u
𝜎
w
d/dA ypred
T
= d/dA w 𝜎Ax
= wT d/dA 𝜎Ax
= wT 𝜎’(Ax) x
x2
v
ypred
𝜎

<!-- Folie 22 -->
Beispielsetup 3
ypred = 〈w, (𝜎〈u, x〉, 𝜎〈v, x〉)〉
= 〈w, 𝜎Ax〉 = wT𝜎Ax (Schreibe u,v als Zeilen in eine Matrix A und benutze 𝜎 auf Vektoren
komponentenweise.)
u1 = A11 also
d/du1 = d/dA11
x1
u
𝜎
w
d/dA ypred
d/dw ypred
T
= d/dA w 𝜎Ax
= wT d/dA 𝜎Ax
= wT 𝜎’(Ax) x
= d/dw wT𝜎Ax = 𝜎Ax
x2
v
ypred
𝜎

<!-- Folie 23 -->
Beispielsetup 3
ypred = wT𝜎Ax
d/dA ypred = wT 𝜎’(Ax) x
d/dw ypred = d/dw wT𝜎Ax = 𝜎Ax
x1
u
𝜎
w
x2
v
ypred
𝜎
Idee: berechne für ypred gleichzeitig Daten für den Gradienten.
Kettenregel: d/dw f(g(x)) = f’(g(x)) g’(x)
mit g(x) = 𝜎Ax und f(x) = wTx
Also zuerst g(w) und g’(w) berechnen vom ersten Layer,
dann damit den nächsten Layer (usw.) bis zum letzten.

## Training mehrerer Schichten:

<!-- Folie 24 -->
Backpropagation (Konkret)

## Backpropagation

<!-- Folie 25 -->
Beispiel 4
f(x) = b3 + W3tanh(b2 + W2tanh(b1 + W1x))
z1 = x
z2 = tanh(b1 + W1z1)
z3 = tanh(b2 + W2z2)
ypred =
b3 + W3z3
(input layer)
(2nd layer)
(3rd layer)
(output layer)
r
E
(residual)
(squared error)
= ypred - y
= ½ r Tr

<!-- Folie 26 -->
Beispiel 4: forward computation
backwards differentiation
f(x) = b3 + W3tanh(b2 + W2tanh(b1 + W1x))
dE = d ½ rTr = ½ d rTr = rT dr = rT dypred
z1 = x
z2 = tanh(b1 + W1z1)
z3 = tanh(b2 + W2z2)
ypred =
b3 + W3z3
(input layer)
(2nd layer)
(3rd layer)
(output layer)
r
E
(residual)
(squared error)
= ypred - y
= ½ r Tr

<!-- Folie 27 -->
Beispiel 4: forward computation
backwards differentiation
f(x) = b3 + W3tanh(b2 + W2tanh(b1 + W1x))
dE = d ½ rTr = ½ d rTr = rT dr = rT dypred
z1 = x
z2 = tanh(b1 + W1z1)
z3 = tanh(b2 + W2z2)
ypred =
b3 + W3z3
(input layer)
(2nd layer)
(3rd layer)
(output layer)
r
E
(residual)
(squared error)
= ypred - y
= ½ r Tr
dypred = d( b3 + W3z3 ) = db3 + dW3z3
So ∇b3E = r

<!-- Folie 28 -->
Beispiel 4: forward computation
backwards differentiation
f(x) = b3 + W3tanh(b2 + W2tanh(b1 + W1x))
dE = d ½ rTr = ½ d rTr = rT dr = rT dypred
z1 = x
z2 = tanh(b1 + W1z1)
z3 = tanh(b2 + W2z2)
ypred =
b3 + W3z3
(input layer)
(2nd layer)
(3rd layer)
(output layer)
r
E
(residual)
(squared error)
= ypred - y
= ½ r Tr
dypred = d( b3 + W3z3 ) = db3 + dW3z3
So ∇b3E = r
und ∇W3E = rz3T
(trace cyclic permutation trick)

<!-- Folie 29 -->
Beispiel 4: forward computation
backwards differentiation
f(x) = b3 + W3tanh(b2 + W2tanh(b1 + W1x))
dE = d ½ rTr = ½ d rTr = rT dr = rT dypred
dypred = d( b3 + W3z3 ) = db3 + dW3z3
∇b3E = r, ∇W3E = rz3T
z1 = x
z2 = tanh(b1 + W1z1)
z3 = tanh(b2 + W2z2)
ypred =
b3 + W3z3
(input layer)
(2nd layer)
(3rd layer)
(output layer)
r
E
(residual)
(squared error)
= ypred - y
= ½ r Tr
Next layer:
kann b3 und W3 als Konstanten sehen,
dE = rT dW3z3 + irrelevant terms
Mit der Kettenregel gilt
d/dz tanh(f(z)) = (1-tanh(f(z))2)f’(z)

<!-- Folie 30 -->
Beispiel 4: forward computation
backwards differentiation
f(x) = b3 + W3tanh(b2 + W2tanh(b1 + W1x))
dE = d ½ rTr = ½ d rTr = rT dr = rT dypred
dypred = d( b3 + W3z3 ) = db3 + dW3z3
∇b3E = r, ∇W3E = rz3T
z1 = x
z2 = tanh(b1 + W1z1)
z3 = tanh(b2 + W2z2)
ypred =
b3 + W3z3
(input layer)
(2nd layer)
(3rd layer)
(output layer)
r
E
(residual)
(squared error)
= ypred - y
= ½ r Tr
Mit der Kettenregel gilt
d/dz tanh(f(z)) = (1-tanh(f(z))2)f’(z)
Next layer:
kann b3 und W3 als Konstanten sehen,
dE = rT dW3z3 + irrelevant terms
dz3 = dtanh(b2+W2z2) = (1-z32)(db2+dW2z2)
so ∇b2E = (1-z32)W3Tr

<!-- Folie 31 -->
Beispiel 4: forward computation
backwards differentiation
f(x) = b3 + W3tanh(b2 + W2tanh(b1 + W1x))
dE = d ½ rTr = ½ d rTr = rT dr = rT dypred
dypred = d( b3 + W3z3 ) = db3 + dW3z3
z1 = x
z2 = tanh(b1 + W1z1)
z3 = tanh(b2 + W2z2)
ypred =
b3 + W3z3
r
E
= ypred - y
= ½ r Tr
(input layer)
(2nd layer)
(3rd layer)
(output layer)
(residual)
(squared error)
Mit der Kettenregel gilt
d/dz tanh(f(z)) = (1-tanh(f(z))2)f’(z)
∇b3E = r,
∇b2E = (1-z32)W3Tr,
∇W3E = rz3T
∇W2E = ∇b2E z2T
∇b1E = (1-z22)W2Tr∇b2E, ∇W1E = ∇b1E z1T
nutze Zwischenschritte zi aus forward um
vollen Gradienten effizient zu berechnen
→ gradient descent

## Matrix-Differenzialkalkül

<!-- Folie 32 -->
Literaturtips
(Achtung: das ist nicht notwendig für diese Veranstaltung, das ist weiterführend)
◼
◼
◼
◼
◼
Thomas P. Minka. Old and new matrix algebra useful for statistics, December 2000.
Notes.
The Matrix Cookbook
Matrix derivatives cheat sheet
Loss functions for classification - Wikipedia
Michael Nielsen’s Buchkapitel zu Backpropagation (sehr mathematisch)
http://neuralnetworksanddeeplearning.com/chap2.html

## Aktivierungsfunktionen und

<!-- Folie 33 -->
weitere Layer

## Aktivierungsfunktionen

<!-- Folie 34 -->
Ein Neuron “forward”: 𝜏〈w, x〉
Perzeptron: 𝜏 = sign
Logistische Regression: 𝜏 = 𝜎
𝜏 beliebig, aber differenzierbar!

<!-- Folie 35 -->
Ein Neuron “forward”: 𝜏〈w, x〉
Perzeptron: 𝜏 = sign
Logistische Regression: 𝜏 = 𝜎
𝜏 beliebig, aber differenzierbar!
Neues Ziel:
neuronales Netz soll Funktion
lernen (Regression);
Modell von der Funktion:
Stückweise linear.
Welches 𝜏 ist geeignet?

<!-- Folie 36 -->
Ein Neuron “forward”: 𝜏〈w, x〉
NEU:
Perzeptron: 𝜏 = sign
Logistische Regression: 𝜏 = 𝜎
ReLU = Rectified Linear Unit
ReLU(y) := max(0, y)
“ReLU Neuron”
𝜏 beliebig, aber differenzierbar!
Ableitung?

<!-- Folie 37 -->
Ableitung von max(0, y) nach y:
Für y > 0 ist max(0, y) = y,
also Ableitung dy/dy = 1.
ReLU = Rectified Linear Unit
ReLU(y) := max(0, y)
“ReLU Neuron”
Für y < 0 ist max(0, y) = 0,
Also Ableitung 0.
Für y = 0 ist die Ableitung nicht definiert.

<!-- Folie 38 -->
Ableitung von max(0, y) nach y:
Für y > 0 ist max(0, y) = y,
also Ableitung dy/dy = 1.
ReLU = Rectified Linear Unit
ReLU(y) := max(0, y)
“ReLU Neuron”
Für y < 0 ist max(0, y) = 0,
Also Ableitung 0.
Für y = 0 definieren wir die Ableitung als 0, das spart Rechnungen.

<!-- Folie 39 -->
Wieso ist ReLU geeignet?
Ziel:
neuronales Netz soll Funktion
lernen (Regression);
Modell von der Funktion:
Stückweise linear.
ReLU = Rectified Linear Unit
ReLU(y) := max(0, y)

<!-- Folie 40 -->
Wieso ist ReLU geeignet?
Lineare Abbildung + ReLU
ist die
Projektion auf einen Halbraum,
denn ReLU ist genau
Projektion auf einen Halbraum.
(Halbraum = eine Seite einer Hyperebene)
Ziel:
neuronales Netz soll Funktion
lernen (Regression);
Modell von der Funktion:
Stückweise linear.
ReLU = Rectified Linear Unit
ReLU(y) := max(0, y)
← Beispiel an der Tafel!

## Layer

<!-- Folie 41 -->
Mehrere Neuronen, die parallel verarbeitet
werden, bilden eine Schicht (Layer).
Mehrmals Lineare Regression
= Multilineare Regression
= Linear Layer
= 1 Matrix, Zeilen sind Gewichtsvektoren
ReLU Layer
= Schicht, in der jedes Neuron die
Aktivierungsfunktion ReLU nutzt
= Linear Layer + ReLU

## Aktivierungsfunktionen

<!-- Folie 42 -->
Problem bei ReLU:
Sterbende Neuronen.
Dann “fließt” keine Information mehr durch
das Neuron während der Backpropagation,
wenn ein Neuron immer 0 liefert, weil die
Eingabe immer negativ ist.

<!-- Folie 43 -->
Problem bei ReLU:
Sterbende Neuronen.
Lösung 1:
Statt 𝜏 = max(0, y) verwende
𝜏 = f(y)[y < 0] +g(y)[y ≥ 0] mit passenden f,g
Dann “fließt” keine Information mehr durch
das Neuron während der Backpropagation,
wenn ein Neuron immer 0 liefert, weil die
Eingabe immer negativ ist.

<!-- Folie 44 -->
Problem bei ReLU:
Sterbende Neuronen.
Dann “fließt” keine Information mehr durch
das Neuron während der Backpropagation,
wenn ein Neuron immer 0 liefert, weil die
Eingabe immer negativ ist.
Lösung 1:
Statt 𝜏 = max(0, y) verwende
𝜏 = f(y)[y < 0] +g(y)[y ≥ 0] mit passenden f,g
z.B. f(y) := α(ey-1) und g(y) := y
Dann heißt 𝜏 auch ELU
(Exponential Linear Unit)

<!-- Folie 45 -->
Problem bei ReLU:
Sterbende Neuronen.
Dann “fließt” keine Information mehr durch
das Neuron während der Backpropagation,
wenn ein Neuron immer 0 liefert, weil die
Eingabe immer negativ ist.
Lösung 2:
Statt 𝜏 = max(0, y) verwende
𝜏 sodass für y →-∞ gilt: 𝜏(y) → 0
und für y → +∞ gilt: 𝜏(y) → +∞
z.B. 𝜏(y) := y*𝜎(y) “Swish”
oder 𝜏(y) := y*Φ(y) “GELU”
(Gaussian error linear unit)
Welche Aktivierungsfunktionen wurden
genutzt? (→Internet Archive)
paperswithcode.com/methods/category/activation-functions

## Autoencoder

<!-- Folie 47 -->

## Autoencoder schematisch

<!-- Folie 48 -->
Grafik von Michaela Massi,
2019 (CC-BY-SA 4.0 International)

## Autoencoder

<!-- Folie 49 -->
Im Kontrast zu unserem bisherigen Vorgehen
Bisher: ein Neuron oder ein neuronales
Netz zur Klassifikation/Regression, also:
Eine nicht bekannte Funktion f,
für die wir manche Werte kennen
( Label y=f(x) für Trainingsdaten (x,y) )
wollen wir “schätzen” mit dem Modell.

<!-- Folie 50 -->
Im Kontrast zu unserem bisherigen Vorgehen
Bisher: ein Neuron oder ein neuronales
Netz zur Klassifikation/Regression, also:
Eine nicht bekannte Funktion f,
für die wir manche Werte kennen
( Label y=f(x) für Trainingsdaten (x,y) )
wollen wir “schätzen” mit dem Modell.
Was, wenn wir
keine Label haben?

<!-- Folie 51 -->
Herleitung zur abstrakten Idee
Ohne Label müssen wir den Output des
neuronalen Netzes anders bewerten.
Was, wenn wir
keine Label haben?
→ Wie Erfolg messen?
→ Welches Ziel ist im
Training noch sinnvoll?

<!-- Folie 52 -->
Herleitung zur abstrakten Idee
Mögliches Ziel:
Ohne Label müssen wir den Output des
neuronalen Netzes anders bewerten.
→ Wie Erfolg messen?
→ Welches Ziel ist im
Training noch sinnvoll?
Transformation der
Eingabe in ein anderes
Koordinatensystem
(Feature Extraction)

<!-- Folie 53 -->
Herleitung zur abstrakten Idee
Mögliches Ziel:
Ohne Label müssen wir den Output des
neuronalen Netzes anders bewerten.
→ Wie Erfolg messen?
→ Welches Ziel ist im
Training noch sinnvoll?
Transformation der
Eingabe in ein anderes
Koordinatensystem
(Feature Extraction)
→ kann man rückgängig
machen, messen, wie gut.

<!-- Folie 54 -->
Herleitung zur abstrakten Idee
Abstrakt:
f ist nicht bekannt,
aber g◦f ist bekannt
d.h. g(f(x)) = x
hier: f = Encoder,
g = Decoder
→
g◦f = Identität

<!-- Folie 55 -->
Dimensionsreduktion
Ziel:
Idee:
Versuche, Dimensionalität
zu reduzieren ohne
Informationsverlust.
Transformation der
Eingabe in ein kleineres
Koordinatensystem
(Feature Extraction)
→ kann man rückgängig
machen, messen, wie gut.

## Loss-Funktion:

<!-- Folie 56 -->
Vergleiche Input mit Output,
mittlere quadratische
Abweichung der Pixelwerte
Trainingsziel:
Output so ähnlich wie möglich
zum Input (Rekonstruktion).
Autoencoder schematisch
Grafik von Michaela Massi,
2019 (CC-BY-SA 4.0 International)

## Rekonstruktion mit einem Autoencoder im

<!-- Folie 57 -->
Vergleich zu Dimensionsreduktion mit PCA
Grafik von Michaela Massi,
2019 (CC-BY-SA 4.0 International)

## Zum neuen Übungsblatt

<!-- Folie 58 -->
Tipps für Blatt 6
Benutzen Sie zur Formulierung der Fragen sowie zur Beantwortung
keine generative KI -- sonst lernen Sie genau das nicht: wie man
anhand der offiziellen Dokumentation prüfen kann, ob die KI-Antwort
korrekt ist.
Ziel ist nicht die “richtige Lösung” sondern der Erwerb der Kompetenz,
Deep Learning Quelltexte kritisch zu lesen
