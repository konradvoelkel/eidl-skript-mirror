---
title: "VL 05: Stochastischer Gradientenabstieg"
short_title: "VL 05"
---

# Stochastischer Gradientenabstieg

:::{warning} Rohfassung
Dieses Kapitel ist eine automatische Transkription der Folien von VL 05 aus dem WiSe 2025/26
(`from_2025/slides/Einführung in Deep Learning 2025_26 VL 05_ SGD.pdf`), Folie für Folie in der Originalreihenfolge.
Formeln und Abbildungen sind dabei größtenteils verloren gegangen; der Text ist noch nicht überarbeitet.
:::

## Training eines einzelnen Neurons:

<!-- Folie 2 -->
Gradientenabstieg

## Training eines einzelnen Neurons

<!-- Folie 3 -->
Was bisher geschah
Perzeptron
[〈w,v〉 > 0] = “sign”(〈w,v〉) ∊ {0, 1}
Aktivierungsfunktion:
“sign” (Vorzeichen)
Training: Update-Regel:
wneu= walt + ρ(ytrue - “sign”(〈w,v〉))x

<!-- Folie 4 -->
Was bisher geschah
Perzeptron
[〈w,v〉 > 0] = “sign”(〈w,v〉) ∊ {0, 1}
Aktivierungsfunktion:
“sign” (Vorzeichen)
Training: Update-Regel:
wneu= walt + ρ(ytrue - “sign”(〈w,v〉))x
Logistische Regression
𝜎(〈w,v〉)
Aktivierungsfunktion:
𝜎 (Logistische Sigmoidfunktion)
Training (naiv): finde w sodass MSE von
linearer Regression minimal.

<!-- Folie 5 -->
Was bisher geschah
Perzeptron
[〈w,v〉 > 0] = “sign”(〈w,v〉) ∊ {0, 1}
Aktivierungsfunktion:
“sign” (Vorzeichen)
Training: Update-Regel:
wneu= walt + ρ(ytrue - “sign”(〈w,v〉))x
Logistische Regression
𝜎(〈w,v〉)
Aktivierungsfunktion:
𝜎 (Logistische Sigmoidfunktion)
Training (naiv): finde w sodass MSE von
linearer Regression minimal.
Jedes einzelne neue Paar (x,y) kann zum
weiterlernen benutzt werden.
Fehler wird minimiert.
Wie aus einem einzelnen neuen Paar (x,y)
etwas dazu lernen?
Wird beim Lernen etwas
maximiert/minimiert?

<!-- Folie 6 -->
Neue, einheitliche Perspektive
Perzeptron
Logistische Regression
Aktivierungsfunktion:
sign (Vorzeichen +1 oder -1)
Training: Update-Regel:
wneu= walt + ρ(ytrue - sign(〈w,x〉))x
Aktivierungsfunktion:
𝜎 (Logistische Sigmoidfunktion)
Training: Update-Regel:
wneu= walt + ρ( ?? ytrue ?? w ?? x ?? )
Fehlerterm (=Loss-Funktion):
Kandidat Perceptron Hinge Loss:
LHinge(x,y; w) = Σi=1..N max(0, -yisign〈w,xi〉)
Fehlerterm (=Loss-Funktion):
Binary cross entropy loss:
LBCE(x,y; w) = - 1/N Σi=1..N yi log pi
pi = P(xi in Klasse 1) = e〈w,xi〉/ (1 + e〈w,xi〉)

## Optimieren mit Fehlerterm

<!-- Folie 7 -->
Wenn L(x,y; w) ∊ ℝ den Fehler eines Modells mit Gewichtsvektor w angibt,
dann suchen wir w sodass L(w) = L(x,y; w) minimal wird.
Extremstellen von L bestimmen:
◼
◼
◼
◼
L’ bestimmen
L’(w) = 0 nach w umstellen
Formel für w ausrechnen (aus den Daten x,y)
Kandidaten für w ausprobieren
(liegt ein Minimum vor?)

<!-- Folie 8 -->
Wenn L(x,y; w) ∊ ℝ den Fehler eines Modells mit Gewichtsvektor w angibt,
dann suchen wir w sodass L(w) = L(x,y; w) minimal wird.
Extremstellen von L bestimmen:
◼
◼
◼
◼
Schaffen wir das immer?
L’ bestimmen
L’(w) = 0 nach w umstellen
Formel für w ausrechnen (aus den Daten x,y)
Kandidaten für w ausprobieren
(liegt ein Minimum vor?)

<!-- Folie 9 -->
Wenn L(x,y; w) ∊ ℝ den Fehler eines Modells mit Gewichtsvektor w angibt,
dann suchen wir w sodass L(w) = L(x,y; w) minimal wird.
Approximative Extremstellen von L bestimmen:
◼
◼
◼
◼
Zufällig ein w auswählen
L(w) ausrechnen, vergleichen mit letztem niedrigstem Wert
Größer? Pech gehabt, weitermachen.
Kleiner? Besseres w gefunden!
Jetzt ggf. aufhören, wenn w gut genug ist.

<!-- Folie 10 -->
Wenn L(x,y; w) ∊ ℝ den Fehler eines Modells mit Gewichtsvektor w angibt,
dann suchen wir w sodass L(w) = L(x,y; w) minimal wird.
Clever approximative Extremstellen von L bestimmen:
◼
◼
◼
◼
Zufällig Clever ein w auswählen, in der Nähe der bisher besten Schätzung
L(w) ausrechnen, vergleichen mit letztem niedrigstem Wert
Größer? Pech gehabt, weitermachen.
Kleiner? Besseres w gefunden!
Jetzt ggf. aufhören, wenn w gut genug ist.

## Quelle: Fisseha Berhane

<!-- Folie 11 -->
https://datascience-enthusiast.com/DL/Optimization_methods.html

## Gradienten

<!-- Folie 12 -->
Wenn L(x,y; w) ∊ ℝ den Fehler eines Modells mit Gewichtsvektor w angibt,
dann suchen wir w sodass L(w) = L(x,y; w) minimal wird.
Wir stellen uns (für den Moment) vor, dass w ∊ ℝ2 ist (also die Daten 2 Features haben).
Wir stellen uns die w-Ebene vor, darauf ein L(w)-Gebirge.
An jedem Punkt die Frage: wohin sollen wir gehen, wenn wir runter wollen?

<!-- Folie 13 -->
Wenn L(x,y; w) ∊ ℝ den Fehler eines Modells mit Gewichtsvektor w angibt,
dann suchen wir w sodass L(w) = L(x,y; w) minimal wird.
Wir stellen uns (für den Moment) vor, dass w ∊ ℝ2 ist (also die Daten 2 Features haben).
Wir stellen uns die w-Ebene vor, darauf ein L(w)-Gebirge.
An jedem Punkt die Frage: wohin sollen wir gehen, wenn wir runter wollen?
Antwort: In die Richtung, wo L(w) am schnellsten kleiner wird, also “nach unten”.

<!-- Folie 14 -->
Wenn L(x,y; w) ∊ ℝ den Fehler eines Modells mit Gewichtsvektor w angibt,
dann suchen wir w sodass L(w) = L(x,y; w) minimal wird.
Wir stellen uns (für den Moment) vor, dass w ∊ ℝ2 ist (also die Daten 2 Features haben).
Wir stellen uns die w-Ebene vor, darauf ein L(w)-Gebirge.
An jedem Punkt die Frage: wohin sollen wir gehen, wenn wir runter wollen?
Antwort: In die Richtung, wo L(w) am schnellsten kleiner wird, also “nach unten”.
D.h. entlang des Gradienten grad(L)(w) = L’(w) ∊ ℝ2

## Gradienten - Konkret

<!-- Folie 15 -->
Wenn wir den MSE für eine lineare Regression betrachten:
L(w) = 1/N Σi=1..N (yi - 〈w,xi〉)2
Halte (zunächst) Komponente w2 fest und variiere w1
→ Funktion in einer Variablen L(w1)
Ableitung L’(w1) gibt Änderung von L abhängig von w1 an,
also Änderung in Richtung der ersten Koordinate der w-Ebene.
“Wenn ich einen (infinitesimalen) Schritt nach Osten gehe, wie stark ändert sich L dann?”

<!-- Folie 16 -->
Wenn wir den MSE für eine lineare Regression betrachten:
L(w) = 1/N Σi=1..N (yi - 〈w,xi〉)2
Halte (danach) Komponente w1 fest und variiere w2
→ Funktion in einer Variablen L(w2)
Ableitung L’(w2) gibt Änderung von L abhängig von w2 an,
also Änderung in Richtung der zweiten Koordinate der w-Ebene.
“Wenn ich einen (infinitesimalen) Schritt nach Norden gehe, wie stark ändert sich L dann?”

<!-- Folie 17 -->
Wenn wir den MSE für eine lineare Regression betrachten:
L(w) = 1/N Σi=1..N (yi - 〈w,xi〉)2
L’(w1) und L’(w2) heißen besser
d/dw1 L(w) und d/dw2 L(w)
und L’(w) = ( d/dw1 L(w), d/dw2 L(w) )
Nicht verwechseln: Ableitung L’ (eine Funktion)
und L’(w), der Gradientenvektor an einem Punkt w.

<!-- Folie 18 -->
Wenn wir den MSE für eine lineare Regression betrachten:
L(w) = 1/N Σi=1..N (yi - 〈w,xi〉)2
L’(w) = ( d/dw1 L(w), d/dw2 L(w) )
= d/dw1L(w) e1 + d/dw2L(w) e2
Änderung in Richtung e1 ausrechnen:
〈L’(w), e1〉 = d/dw1L(w)

<!-- Folie 19 -->
Wenn wir den MSE für eine lineare Regression betrachten:
L(w) = 1/N Σi=1..N (yi - 〈w,xi〉)2
L’(w) = ( d/dw1 L(w), d/dw2 L(w) )
= d/dw1L(w) e1 + d/dw2L(w) e2
Änderung in Richtung v ausrechnen:
〈L’(w), v〉 = d/dw1L(w) v1 + d/dw2L(w) v2

<!-- Folie 20 -->
Wenn wir den MSE für eine lineare Regression betrachten:
L(w) = 1/N Σi=1..N (yi - 〈w,xi〉)2
L’(w) = ( d/dw1 L(w), d/dw2 L(w) )
= d/dw1L(w) e1 + d/dw2L(w) e2
In welche Richtung v ist die Änderung maximal?
〈L’(w), v〉 = d/dw1L(w) v1 + d/dw2L(w) v2

<!-- Folie 21 -->
Wenn wir den MSE für eine lineare Regression betrachten:
L(w) = 1/N Σi=1..N (yi - 〈w,xi〉)2
L’(w) = ( d/dw1 L(w), d/dw2 L(w) )
= d/dw1L(w) e1 + d/dw2L(w) e2
In Richtung v=L’(w) ist die Änderung maximal:
〈L’(w), L’(w)〉 = || L’(w) ||2

<!-- Folie 22 -->
Wenn wir den MSE für eine lineare Regression betrachten:
L(w) = 1/N Σi=1..N (yi - 〈w,xi〉)2
L’(w) = ( d/dw1 L(w), d/dw2 L(w) )
= d/dw1L(w) e1 + d/dw2L(w) e2
Endlich Ausrechnen:
d/dw1L(w) = 1/N Σi=1..N 2(yi - w1xi1 - w2xi2)(-xi1)
d/dw2L(w) = 1/N Σi=1..N 2(yi - w1xi1 - w2xi2)(-xi2)

<!-- Folie 23 -->
Wenn wir den MSE für eine lineare Regression betrachten:
L(w) = 1/N Σi=1..N (yi - 〈w,xi〉)2
L’(w) = ( d/dw1 L(w), d/dw2 L(w) ) = d/dw1L(w) e1 + d/dw2L(w) e2
d/dw1L(w) = 1/N Σi=1..N 2(yi - w1xi1 - w2xi2)(-xi1)
d/dw2L(w) = 1/N Σi=1..N 2(yi - w1xi1 - w2xi2)(-xi2)
Fiktive Daten: x1 = (1,0), y1=0, x2 = (0,1), y2=1, N=2
walt = (1,1)

<!-- Folie 24 -->
Wenn wir den MSE für eine lineare Regression betrachten:
L(w) = 1/N Σi=1..N (yi - 〈w,xi〉)2
L’(w) = ( d/dw1 L(w), d/dw2 L(w) ) = d/dw1L(w) e1 + d/dw2L(w) e2
d/dw1L(w) = 1/N Σi=1..N 2(yi - w1xi1 - w2xi2)(-xi1)
d/dw2L(w) = 1/N Σi=1..N 2(yi - w1xi1 - w2xi2)(-xi2)
Fiktive Daten: x1 = (1,0), y1=0, x2 = (0,1), y2=1, N=2,
walt = (1,1)
d/dw1L(walt) = Σi=1..2(yi - xi1 - xi2)(-xi1) = (0-1)(-1) + (1-1)(-0) = 1
d/dw2L(walt) = Σi=1..2(yi - xi1 - xi2)(-xi2) = (0-1)(-0) + (1-1)(-1) = 0

<!-- Folie 26 -->
Wenn wir den MSE für eine lineare Regression betrachten:
L(w) = 1/N Σi=1..N (yi - 〈w,xi〉)2
L’(w) = ( d/dw1 L(w), d/dw2 L(w) ) = d/dw1L(w) e1 + d/dw2L(w) e2
Fiktive Daten: x1 = (1,0), y1=0, x2 = (0,1), y2=1, N=2,
walt = (1,1)
L’(w) = (1,0)
wneu := walt - ρ L’(w)
mit z.B. ρ=½ also wneu = (1,1) - (½,0) = (½, 1)

## Optimieren mit Fehlerterm

<!-- Folie 27 -->
Wenn L(x,y; w) ∊ ℝ den Fehler eines Modells mit Gewichtsvektor w angibt,
dann suchen wir w sodass L(w) = L(x,y; w) minimal wird.
Sehr clever approximative Extremstellen von L bestimmen:
◼
Sehr clever ein w auswählen, in der Nähe der bisher besten Schätzung:
wneu := walt - ρ L’(walt)
◼
◼
◼
“Gradientenabstieg”
L(w) ausrechnen, vergleichen mit letztem niedrigstem Wert
Größer? Pech gehabt, weitermachen.
Kleiner? Besseres w gefunden!
Jetzt ggf. aufhören, wenn w gut genug ist.

## Quelle: Amini, Alexander & Soleimany, Ava

<!-- Folie 28 -->
& Karaman, Sertac & Rus, Daniela. (2018).
Spatial Uncertainty Sampling for
End-to-End Control.

## Quelle: Li, Hao, Zheng Xu, Gavin

<!-- Folie 29 -->
Taylor, Christoph Studer, and Tom
Goldstein. "Visualizing the loss
landscape of neural nets." arXiv
preprint arXiv:1712.09913 (2017).

## Interaktiv:

<!-- Folie 30 -->
Loss Landscape Explorer
https://losslandscape.com/explorer

## Training eines einzelnen Neurons

<!-- Folie 31 -->
Neue, einheitliche Perspektive
Perzeptron
Aktivierungsfunktion:
sign (Vorzeichen +1 oder -1)
Training: Update-Regel:
wneu= walt + ρ(ytrue - sign(〈w,x〉))x
Fehlerterm (=Loss-Funktion):
Kandidat Perceptron Hinge Loss:
LHinge(x,y; w) = Σi=1..N max(0, -yisign〈w,xi〉)
Ableitung?!?

<!-- Folie 32 -->
Neue, einheitliche Perspektive
Perzeptron
Aktivierungsfunktion:
sign (Vorzeichen +1 oder -1)
Training: Update-Regel:
wneu= walt + ρ(ytrue - sign(〈w,x〉))x
Fehlerterm (=Loss-Funktion):
“hard” Perceptron Loss:
LHinge(x,y; w) = Σi=1..N max(0, -yisign〈w,xi〉)
Besser: “soft” Perceptron Loss:
LHinge(x,y; w) = Σi=1..N max(0, -yi〈w,xi〉)
LHinge’(w) = Σi=1..N -yixi max(0, -yi〈w,xi〉) / (-yi〈w,xi〉)
= Summe falsch klassifizierter

<!-- Folie 33 -->
Neue, einheitliche Perspektive
Perzeptron
Aktivierungsfunktion:
sign (Vorzeichen +1 oder -1)
Training: Update-Regel:
wneu= walt + ρ(ytrue - sign(〈w,x〉))x
Fehlerterm (=Loss-Funktion):
“hard” Perceptron Loss:
LHinge(x,y; w) = Σi=1..N max(0, -yisign〈w,xi〉)
Besser: “soft” Perceptron Loss:
LHinge(x,y; w) = Σi=1..N max(0, -yi〈w,xi〉)
Allgemeine Update-Regel:
wneu = walt - ρ L’(w)
Für einzelnes (x, ytrue) also N=1 und
wneu = walt ± ρ x wenn x falsch klassifiziert.
LHinge’(w) = Σi=1..N -yixi max(0, -yi〈w,xi〉) / (-yi〈w,xi〉)
= Summe falsch klassifizierter

## Loss-Funktionen

<!-- Folie 34 -->
Die wir bisher gesehen haben:

## Training eines einzelnen Neurons

<!-- Folie 35 -->
Take-Home Message
Ein einzelnes Neuron besteht aus
◼
◼
einer Aktivierungsfunktion τ,
einem Gewichtsvektor w (Parameter).
Inferenz:
ypred = τ(〈w,x〉)
Für binäre Klassifikation:
τ=𝜎
L(w) = LBCE(w)
Das ist logistische Regression.
Training (mit Hyperparameter ρ):
Das kommt auf die Loss-Funktion L(w) an:
wneu = walt - ρ L’(walt)

## Nicht-Stochastischer Gradientenabstieg??

<!-- Folie 36 -->
Gradientenabstieg ist der Oberbegriff
und gleichzeitig auch die spezifische
Bezeichnung für:
Den ganzen Datensatz einlesen, dabei die
Loss-Funktion auswerten und den
Gradienten bestimmen. Damit Gewichte
anpassen und erneut den ganzen
Datensatz einlesen usw.
Stochastischer Gradientenabstieg ist das
Anpassen der Gewichte mit einer
Schätzung des Gradienten aus einem
Teildatensatz, meist ist ein einzelnes
Sample gemeint. Das ist zufällig gewählt
(die Anordnung der Daten wird als zufällig
angenommen), daher stochastisch.
Kompromiss Mini-Batch SGD:
Eine kleine, handhabbare Menge von
Samples wird gemeinsam verarbeitet,
damit dann der Gradient approximiert.

## Ziel für nächste Woche

<!-- Folie 37 -->
Ziel: Verstehen können, was dort geschieht:
TensorFlow Playground
https://playground.tensorflow.org

## Zum neuen Übungsblatt

<!-- Folie 38 -->
Tipps für Blatt 5
Lesen Sie die Folien zu Vorlesung 4 nochmal aufmerksam - da sind
nützliche Hinweise zu finden, um Aufgabe 3 zu lösen.
Wenn Sie sich bei Aufgabe 1 schwer tun,
versuchen Sie zunächst die Rechnung 𝜎(−𝑥) = 1−𝜎(𝑥) aus Vorlesung 4
nachzuvollziehen.
