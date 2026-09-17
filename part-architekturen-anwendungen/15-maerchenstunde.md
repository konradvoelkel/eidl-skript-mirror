---
title: "VL 15: Märchenstunde: Optimierer, Adversarial Attacks, Polysemie"
short_title: "VL 15"
---

# Märchenstunde: Optimierer, Adversarial Attacks, Polysemie

:::{warning} Rohfassung
Dieses Kapitel ist eine automatische Transkription der Folien von VL 15 aus dem WiSe 2025/26
(`from_2025/slides/Einführung in Deep Learning 2025_26 VL 15_ Märchenstunde.pdf`), Folie für Folie in der Originalreihenfolge.
Formeln und Abbildungen sind dabei größtenteils verloren gegangen; der Text ist noch nicht überarbeitet.
:::

## Ein Märchen über Optimierung

<!-- Folie 2 -->

## Adam oder was?

<!-- Folie 3 -->
Wir haben die Grundidee des stochastischen Mini-Batch Gradientenabstieg gelernt,
und dann gesagt: in PyTorch klappt Adam oft besser als SGD.
Aber was steckt dahinter?

## Das Grundproblem beim SGD

<!-- Folie 4 -->
Die Daten x1,...,xN modellieren wir als Stichprobe einer Zufallsvariable X
Verteilung von X ist unbekannt, Stichprobe hat Sampling-Bias.
Am liebsten möchten wir N → ∞ haben,
Damit aus Stichprobe die Verteilung von X genau geschätzt werden kann.

<!-- Folie 5 -->
Die Daten x1,...,xN modellieren wir als Stichprobe einer Zufallsvariable X
Verteilung von X ist unbekannt, Stichprobe hat Sampling-Bias.
Am liebsten möchten wir N → ∞ haben,
Damit aus Stichprobe die Verteilung von X genau geschätzt werden kann.
Für eine Stichprobe können wir den Loss ausrechnen.
Idealisiert für eine “unendlich große Stichprobe” wäre das der Erwartungswert der
Loss-Funktion unter der Verteilung von X - der “eigentlich richtige Loss”.

<!-- Folie 6 -->
Die Daten x1,...,xN modellieren wir als Stichprobe einer Zufallsvariable X
Verteilung von X ist unbekannt, Stichprobe hat Sampling-Bias.
Player:
◼
◼
◼
Der Erwartungswert der Loss-Funktion unter der Verteilung von X (unbekannt)
Ein Schätzwert für diesen Erwartungswert, berechnet aus einer großen Stichprobe
(Bester Schätzwert, wenn Stichprobe = alle Daten, die man kriegen kann)
Ein schlechter, aber billiger Schätzwert, berechnet aus einem Mini-Batch

<!-- Folie 7 -->
Die Daten x1,...,xN modellieren wir als Stichprobe einer Zufallsvariable X
Verteilung von X ist unbekannt, Stichprobe hat Sampling-Bias.
Player:
◼
◼
◼
Der Erwartungswert der Loss-Funktion unter der Verteilung von X (unbekannt)
Ein Schätzwert für diesen Erwartungswert, berechnet aus einer großen Stichprobe
(Bester Schätzwert, wenn Stichprobe = alle Daten, die man kriegen kann)
Ein schlechter, aber billiger Schätzwert, berechnet aus einem Mini-Batch
Pro Minibatch wird der Loss grob abgeschätzt und damit Gradienten berechnet,
die also auch “nur so grob geschätzt” sind.

<!-- Folie 8 -->
Verständnisfrage:
(Warum) kann der Loss von einem Minibatch zum nächsten steigen,
wenn wir stochastischen Gradientenabstieg verwenden?
Haben wir nicht gelernt, dass Gradientenabstieg den Loss senken muss?

## Idee: Momentum

<!-- Folie 9 -->
Wir schätzen den “wahren Loss” und damit den eigentlich interessanten Gradienten aus
jedem Minibatch neu.
Die Schätzung wird besser, wenn die Batchsize steigt.
Kann man auch Informationen aus dem vorherigen Minibatch nutzen,
um einen ähnlichen Effekt zu erzielen?

<!-- Folie 10 -->
Wir schätzen den “wahren Loss” und damit den eigentlich interessanten Gradienten aus
jedem Minibatch neu.
Die Schätzung wird besser, wenn die Batchsize steigt.
Kann man auch Informationen aus dem vorherigen Minibatch nutzen,
um einen ähnlichen Effekt zu erzielen?
Könnte z.B. Gradientenschätzungen von je 5 Batches mitteln,
Erhalte damit bessere Schätzung.
→ Was ist das praktische Problem, mit diesem Ansatz?

<!-- Folie 11 -->
Wir schätzen den “wahren Loss” und damit den eigentlich interessanten Gradienten aus
jedem Minibatch neu.
Idee: Gradienten sind ein bisschen ähnlich, wenn man sich nicht so weit weg bewegt im
“Loss Landscape”.

<!-- Folie 12 -->
Wir schätzen den “wahren Loss” und damit den eigentlich interessanten Gradienten aus
jedem Minibatch neu.
Idee: Gradienten sind ein bisschen ähnlich, wenn man sich nicht so weit weg bewegt im
“Loss Landscape”.
Idee: Statt Mittelwert der letzten 5 Gradienten, verwende gewichtetes Mittel.
Visuelle Metapher: zeigt der Pfeil (Gradient) in eine Richtung, geht es nächstes Mal auf
jeden Fall auch ein bisschen weiter in diese Richtung (Impulserhaltung).

## Idee: Adaptive Lernrate

<!-- Folie 13 -->
Der zweite Bestandteil von Adam (=Adaptive Moment Estimation) ist der adaptive Teil:
Zusätzlich zu einer Heuristik zur besseren Schätzung der Gradienten der Lossfunktion,
berechne die Quadrate - die Varianz des Gradienten.

<!-- Folie 14 -->
Der zweite Bestandteil von Adam (=Adaptive Moment Estimation) ist der adaptive Teil:
Zusätzlich zu einer Heuristik zur besseren Schätzung der Gradienten der Lossfunktion,
berechne die Quadrate - die Varianz des Gradienten.
Ändert sich der Gradient stark, gehe kleine Schritte (das Loss-Landscape ist steil).
Ändert sich der Gradient wenig, gehe große Schritte (das Loss-Landscape is flach).
Diese Technik kommt von RMSProp (Root Mean Square Propagation).

## Adam oder was?

<!-- Folie 15 -->
Wir haben die Grundidee des stochastischen Mini-Batch Gradientenabstieg gelernt,
und dann gesagt: in PyTorch klappt Adam oft besser als SGD.
Dahinter steckt eine adaptive Lernrate, abhängig von der Varianz der Gradienten, einzeln
für jedes Gewicht, sowie die Impuls-Heuristik zur verbesserten Gradientenschätzung.
Wo geht das schief?

<!-- Folie 16 -->
Wir haben die Grundidee des stochastischen Mini-Batch Gradientenabstieg gelernt,
und dann gesagt: in PyTorch klappt Adam oft besser als SGD.
Dahinter steckt eine adaptive Lernrate, abhängig von der Varianz der Gradienten, einzeln
für jedes Gewicht, sowie die Impuls-Heuristik zur verbesserten Gradientenschätzung.
Wo geht das schief?
Wenn die Lernrate nicht stark genug abgesenkt wird,
findet die Optimierung nie das lokale Optimum und oszilliert darum herum.

## Adam oder Muon?

<!-- Folie 17 -->
Die Grundidee “wir rechnen clever eine bessere Schätzung/Heuristik für Gradienten aus”
kann man noch weiter treiben.
Idee: ein linearer Layer im neuronalen Netz lässt sich als Operator betrachten,
also als Abbildung (die Matrixmultiplikation). Behandle die Gewichte nicht isoliert!

<!-- Folie 18 -->
Die Grundidee “wir rechnen clever eine bessere Schätzung/Heuristik für Gradienten aus”
kann man noch weiter treiben.
Idee: ein linearer Layer im neuronalen Netz lässt sich als Operator betrachten,
also als Abbildung (die Matrixmultiplikation). Behandle die Gewichte nicht isoliert!
Idee: statt mit der Varianz zu reskalieren wie bei Adam,
“orthogonalisiere” das Update ← das ist etwas schwieriger zu verstehen.
Erinnerung: eine Matrix A hat eine Singulärwertzerlegung A = UDV, wobei U und V
orthogonale Matrizen sind (bestimmte Koordinatensysteme) und D eine Diagonalmatrix.
Wenn die Einträge von D entweder 0 oder 1 sind, ist A selbst orthogonal.

## Muon?

<!-- Folie 19 -->
Idee: “orthogonalisiere” das Update
Wir berechnen erst wie bei SGD den Gradienten der Loss-Funktion, hier genannt A.
Update-Formel: Wneu := Walt - ρ A
Erinnerung: eine Matrix A hat eine Singulärwertzerlegung A = UDV, wobei U und V
orthogonale Matrizen sind (bestimmte Koordinatensysteme) und D eine Diagonalmatrix.
Wenn die Einträge von D entweder 0 oder 1 sind, ist A selbst orthogonal.
“Orthogonal machen” durch A = UDV berechnen und Aortho := UDorthoV mit Dortho,i:=[Di>0]
ist leider teuer: SVD ist aufwändig.

## Muon

<!-- Folie 20 -->
Idee: “orthogonalisiere” das Update mit der Brechstange
Wir berechnen erst wie bei SGD den Gradienten der Loss-Funktion, hier genannt A.
Zutaten:
◼
◼
◼
◼
Wenn A = UDV die Singulärwertzerlegung ist,
dann ist f(A) = U f(D) V für ein Polynom f.
Approximiere die Funktion [x > 0] mit einem Polynom f kleinen Grades. (NewtonSchulz)
Oha: g(x) := f(f(f(f(f(x))))) approximiert [x > 0] auch ganz gut.
(NewtonSchulz5)
Berechne Aoha := g(A), hoffe dass es nah dran ist an Aortho.
Update Wneu := Walt - ρ Aoha
Jordan, Keller et al. Muon: An optimizer for hidden layers in neural networks. 2024.

## Wieso so kompliziert?

<!-- Folie 21 -->
Genau genommen liegt der Gradient der Loss-Funktion an einem Punkt des
Gewichtsraums im Kotangentialraum des Graphen der Loss-Funktion.
Um einen Vektor aus dem Gewichtsraum daraus zu machen, müssen wir “dualisieren”.

<!-- Folie 22 -->
Genau genommen liegt der Gradient der Loss-Funktion an einem Punkt des
Gewichtsraums im Kotangentialraum des Graphen der Loss-Funktion.
Um einen Vektor aus dem Gewichtsraum daraus zu machen, müssen wir “dualisieren”.
Dabei kann man verschiedene Geometrien betrachten:
◼
Die euklidische Geometrie, einfach ℝn, dann kann man die Zahlen, die man
ausrechnet, wie gehabt als Vektor in ℝn auffassen.

<!-- Folie 23 -->
Genau genommen liegt der Gradient der Loss-Funktion an einem Punkt des
Gewichtsraums im Kotangentialraum des Graphen der Loss-Funktion.
Um einen Vektor aus dem Gewichtsraum daraus zu machen, müssen wir “dualisieren”.
Dabei kann man verschiedene Geometrien betrachten:
◼
◼
Die euklidische Geometrie, einfach ℝn, dann kann man die Zahlen, die man
ausrechnet, wie gehabt als Vektor in ℝn auffassen.
Die riemannsche Geometrie die durch die Fisher-Informationsmatrix gegeben ist
“Natural Gradient” - Die Fisher-Matrix ist die zweite Ableitung der relativen Entropie.

<!-- Folie 24 -->
Genau genommen liegt der Gradient der Loss-Funktion an einem Punkt des
Gewichtsraums im Kotangentialraum des Graphen der Loss-Funktion.
Um einen Vektor aus dem Gewichtsraum daraus zu machen, müssen wir “dualisieren”.
Dabei kann man verschiedene Geometrien betrachten:
◼
◼
◼
Die euklidische Geometrie, einfach ℝn, dann kann man die Zahlen, die man
ausrechnet, wie gehabt als Vektor in ℝn auffassen.
Die riemannsche Geometrie die durch die Fisher-Informationsmatrix gegeben ist
“Natural Gradient” - Die Fisher-Matrix ist die zweite Ableitung der relativen Entropie.
Verschiedene andere sogenannte affine Geometrien das ist ein aktives Forschungsgebiet in der Optimierungstheorie.
Stichwort Informationsgeometrie
Z.B. Derun Zhou, Keisuke Yano, Mahito Sugiyama: Dual Riemannian Newton
Method on Statistical Manifolds 2025, https://arxiv.org/pdf/2511.11318

## Ein Märchen über Adversarial Attacks

<!-- Folie 25 -->

## Adversarial Attacks

<!-- Folie 26 -->
Definition
Die gezielte Manipulation des Inputs
eines Machine-Learning-Modells
um ein spezifisch falsches Ergebnis
oder ein unerwartetes Verhalten zu produzieren.
Die Manipulation ist häufig nicht direkt für Menschen zu erkennen.

<!-- Folie 27 -->
Beispiel
Die gezielte Manipulation des Inputs
eines Bildklassifikators
um eine spezifisch falsche Klasse zu produzieren.

<!-- Folie 28 -->
Beispiel
Die gezielte Manipulation des Inputs
eines Bildklassifikators
um eine spezifisch falsche Klasse zu produzieren.
Also: wir stecken einen weißen Hai rein,
aber “die KI” sagt “Goldfisch” dazu. Reingelegt!

## Aus der Abschlussarbeit “Das Dimpled Manifold Model als

<!-- Folie 29 -->
Erklärung für die Existenz und die Eigenschaften von
Adversarial Examples” von N.Wieczorek (BA, HHU 2023)

## Adversarial Attacks

<!-- Folie 30 -->
Theorie
Wir betrachten den Eingaberaum “Menge aller Bilddateien”
sowie die Eingabemenge “Menge aller Trainingsbilder”.
Das Modell lernt Entscheidungsgrenzen im Eingaberaum,
um Klassenlabel zu vergeben.
Hypothese: Nahe der Entscheidungsgrenze liegen
adversarial examples.

<!-- Folie 31 -->
Wie wird’s gemacht?
Mit Gradientenabstiegsmethoden sucht man,
ausgehend von einem Bild eines weißen Hais,
Richtungen, die die Klassifikation ändern,
ohne besonders viel am Bild zu ändern.
Anders als sonst:
SGD im Eingaberaum, nicht im Gewichtsraum.

## Aus der Abschlussarbeit

<!-- Folie 32 -->
“Das Dimpled Manifold
Model als Erklärung für
die Existenz und die
Eigenschaften von
Adversarial Examples”
von N.Wieczorek (BA,
HHU 2023)

## Sharif et. al. 2016 “Accessorize to a Crime:

<!-- Folie 33 -->
Real and Stealthy Attacks on State-of-the-Art Face Recognition”

## Heise Newsticker 2.2.2026

<!-- Folie 34 -->
https://www.heise.de/news/Manip
ulierte-Strassenschilder-Wenn-da
s-autonome-Auto-Fussgaenger-u
mfaehrt-11162744.html

## Ein Märchen über Polysemie

<!-- Folie 35 -->
[Folien von Ben Ruppik, TDA im
Master AI&Data Science Juni 2025]
