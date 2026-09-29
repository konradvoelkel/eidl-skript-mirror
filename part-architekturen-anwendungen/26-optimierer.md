---
title: "Optimierer: Momentum, Adam, Muon"
short_title: "Optimierer"
---

# Optimierer: Momentum, Adam, Muon

## Adam oder was?

Wir haben die Grundidee des stochastischen Mini-Batch-Gradientenabstiegs gelernt und dann gesagt: In PyTorch klappt Adam oft besser als SGD. Aber was steckt dahinter?

### Das Grundproblem beim SGD

Die Daten $x_1, \dots, x_N$ modellieren wir als Stichprobe einer Zufallsvariable $X$. Die Verteilung von $X$ ist unbekannt, und die Stichprobe hat Sampling-Bias. Am liebsten möchten wir $N \to \infty$ haben, damit aus der Stichprobe die Verteilung von $X$ genau geschätzt werden kann. Für eine Stichprobe können wir den Loss ausrechnen; idealisiert für eine „unendlich große Stichprobe“ wäre das der Erwartungswert der Loss-Funktion unter der Verteilung von $X$ – der „eigentlich richtige Loss“. Es gibt also drei Player:

* Der Erwartungswert $\mathbb{E}_X[L(X; w)]$ der Loss-Funktion unter der Verteilung von $X$ (unbekannt).
* Ein Schätzwert für diesen Erwartungswert, berechnet aus einer großen Stichprobe: $\frac1N \sum_i L(x_i; w)$. Bester Schätzwert, wenn Stichprobe = alle Daten, die man kriegen kann.
* Ein schlechter, aber billiger Schätzwert, berechnet aus einem Mini-Batch $B$: $\frac{1}{|B|} \sum_{i \in B} L(x_i; w)$.

Pro Mini-Batch wird der Loss grob abgeschätzt und damit werden Gradienten berechnet, die also auch „nur so grob geschätzt“ sind.

:::{admonition} Verständnisfrage
:class: hint
(Warum) kann der Loss von einem Mini-Batch zum nächsten *steigen*, wenn wir stochastischen Gradientenabstieg verwenden? Haben wir nicht gelernt, dass Gradientenabstieg den Loss senken muss?
:::

### Idee: Momentum

Wir schätzen den „wahren Loss“ und damit den eigentlich interessanten Gradienten aus jedem Mini-Batch neu. Die Schätzung wird besser, wenn die Batch Size steigt. Kann man auch Informationen aus dem vorherigen Mini-Batch nutzen, um einen ähnlichen Effekt zu erzielen? Man könnte z.B. die Gradientenschätzungen von je 5 Batches mitteln und erhielte damit eine bessere Schätzung. Das praktische Problem mit diesem Ansatz: Man müsste 5 Gradienten (jeder so groß wie das Modell) speichern, und man bekäme nur alle 5 Batches ein Update.

Idee: Gradienten sind ein bisschen ähnlich, wenn man sich nicht so weit weg bewegt im Loss Landscape. Statt des Mittelwerts der letzten 5 Gradienten verwende ein *exponentiell gewichtetes* Mittel, das sich mit einem einzigen Vektor mitführen lässt:

$$
m_t := \beta_1 m_{t-1} + (1 - \beta_1)\, g_t, \qquad w_{t+1} := w_t - \rho\, m_t,
$$

mit $g_t$ dem Gradienten des aktuellen Batches und typischerweise $\beta_1 = 0{,}9$. Visuelle Metapher: Zeigt der Pfeil (Gradient) in eine Richtung, geht es nächstes Mal auf jeden Fall auch ein bisschen weiter in diese Richtung – Impulserhaltung, daher **Momentum**. Rauschen in wechselnden Richtungen mittelt sich heraus, konsistente Richtungen verstärken sich.

### Idee: Adaptive Lernrate

Der zweite Bestandteil von **Adam** (= Adaptive Moment Estimation) ist der adaptive Teil: Zusätzlich zu einer Heuristik zur besseren Schätzung der Gradienten der Loss-Funktion berechne die Quadrate – das mittlere Gradientenquadrat, also das *zweite Moment* (nicht die Varianz; dafür müsste man noch $m_t^2$ abziehen), ebenfalls als exponentiell gewichtetes Mittel, komponentenweise:

$$
v_t := \beta_2 v_{t-1} + (1 - \beta_2)\, g_t^2, \qquad w_{t+1} := w_t - \rho\, \frac{m_t}{\sqrt{v_t} + \epsilon},
$$

mit typischerweise $\beta_2 = 0{,}999$ und $\epsilon = 10^{-8}$ gegen Division durch null. Sind die Gradienten einer Koordinate durchweg groß, wird der Schritt dort gedämpft; sind sie durchweg klein, wird er verstärkt. Im Ergebnis ist $m_t / \sqrt{v_t}$ von der Größenordnung $1$, jeder Parameter macht also Schritte der Größenordnung $\rho$ – unabhängig davon, wie groß seine Gradienten absolut sind. Diese Technik kommt von RMSProp (Root Mean Square Propagation). Der Effekt ist eine **Lernrate pro Gewicht**: Gewichte mit selten großen Gradienten (z.B. Embeddings seltener Wörter) bekommen dadurch relativ größere Schritte.

### Adam oder was?

Dahinter steckt also eine adaptive Lernrate, abhängig von der bisherigen Größe der Gradienten, einzeln für jedes Gewicht, sowie die Impuls-Heuristik zur verbesserten Gradientenschätzung. (Adam korrigiert außerdem die Schätzungen $m_t$, $v_t$ in den ersten Schritten für den Bias durch die Initialisierung mit null.) Wo geht das schief? Wenn die Lernrate nicht stark genug abgesenkt wird, findet die Optimierung nie das lokale Optimum und oszilliert darum herum. Deshalb kombiniert man Adam in der Praxis mit einem *Learning Rate Schedule*, der $\rho$ im Laufe des Trainings verkleinert.

### Adam oder Muon?

Die Grundidee „wir rechnen clever eine bessere Schätzung bzw. Heuristik für Gradienten aus“ kann man noch weiter treiben. Idee: Ein linearer Layer im neuronalen Netz lässt sich als *Operator* betrachten, also als Abbildung (die Matrixmultiplikation). Behandle die Gewichte einer Matrix nicht isoliert, sondern als Ganzes! Und statt mit der Varianz zu reskalieren wie bei Adam, **orthogonalisiere** das Update – das ist etwas schwieriger zu verstehen.

Erinnerung: Eine Matrix $A$ hat eine Singulärwertzerlegung $A = U D V$, wobei $U$ und $V$ orthogonale Matrizen sind (bestimmte Koordinatensysteme) und $D$ eine Diagonalmatrix mit den Singulärwerten. Wenn die Einträge von $D$ entweder $0$ oder $1$ sind, ist $A$ selbst (semi-)orthogonal.

**Muon**: Wir berechnen erst wie bei SGD den Gradienten der Loss-Funktion nach einer Gewichtsmatrix, hier genannt $A$; die Update-Formel wäre $W_{\text{neu}} := W_{\text{alt}} - \rho A$. „Orthogonal machen“ durch $A = UDV$ berechnen und $A_{\text{ortho}} := U D_{\text{ortho}} V$ mit $D_{\text{ortho}, i} := [D_i > 0]$ ist leider teuer: Die SVD ist aufwändig. Also mit der Brechstange:

* Wenn $A = UDV$ die Singulärwertzerlegung ist, dann ist $f(A) = U f(D) V$ für ein Polynom $f$ (in $A$ und $A^T A$).
* Approximiere die Funktion $[x > 0]$ auf $(0, 1]$ mit einem Polynom $f$ kleinen Grades (Newton-Schulz-Iteration).
* Oha: $g(x) := f(f(f(f(f(x)))))$ approximiert $[x > 0]$ auch ganz gut (*NewtonSchulz5*).
* Berechne $A_{\text{oha}} := g(A)$ – nur Matrixmultiplikationen, die auf der GPU billig sind – und hoffe, dass es nah dran ist an $A_{\text{ortho}}$.
* Update $W_{\text{neu}} := W_{\text{alt}} - \rho A_{\text{oha}}$.

Jordan, Keller et al.: *Muon: An optimizer for hidden layers in neural networks* (2024). Alle Richtungen im Gewichtsraum bekommen dadurch denselben Schritt, nicht nur die mit großem Singulärwert – Richtungen, die der Gradient „vernachlässigt“, werden mitgezogen.

### Wieso so kompliziert?

Genau genommen liegt der Gradient der Loss-Funktion an einem Punkt des Gewichtsraums im *Kotangentialraum* des Graphen der Loss-Funktion – er ist eine Linearform, die Änderungsrichtungen Zahlen zuordnet ([Kapitel „Tensoren“](../part-grundlagen/05-tensoren.md): Kovektoren!). Um einen Vektor aus dem Gewichtsraum daraus zu machen, mit dem wir einen Schritt gehen können, müssen wir „dualisieren“. Dabei kann man verschiedene Geometrien betrachten:

* Die **euklidische Geometrie**, einfach $\mathbb{R}^n$ mit dem Standardskalarprodukt; dann kann man die Zahlen, die man ausrechnet, wie gehabt als Vektor in $\mathbb{R}^n$ auffassen. Das ist SGD.
* Die **Riemannsche Geometrie**, die durch die Fisher-Informationsmatrix gegeben ist – der *Natural Gradient* (Amari). Die Fisher-Matrix ist die zweite Ableitung der relativen Entropie; Schritte werden so gemessen, wie stark sich die *Ausgabeverteilung* des Modells ändert, nicht die Gewichte.
* Verschiedene andere sogenannte affine Geometrien; das ist ein aktives Forschungsgebiet in der Optimierungstheorie, Stichwort **Informationsgeometrie**. Z.B. Derun Zhou, Keisuke Yano, Mahito Sugiyama: *Dual Riemannian Newton Method on Statistical Manifolds* (2025), [arXiv:2511.11318](https://arxiv.org/abs/2511.11318).

Adam und Muon sind in diesem Bild billige Näherungen an eine bessere Geometrie des Gewichtsraums.

## Übung

Eine Funktion mit Gradienten $g_1 = 1$, $g_2 = 1$, $g_3 = 1$ in drei aufeinanderfolgenden
Schritten (ein langes, flaches Tal), Lernrate $\rho = 0{,}1$.

1. Wie weit ist SGD nach drei Schritten gekommen?
2. Wie weit kommt Momentum mit $v_t = \beta v_{t-1} + g_t$, $\beta = 0{,}9$ und
   demselben $\rho$? Das ist die Form, die `torch.optim.SGD(momentum=0.9)` benutzt; sie
   unterscheidet sich von der Fassung oben im Kapitel um den Faktor $(1 - \beta)$, der
   dort das Mittel normiert. Mit der Kapitelfassung käme entsprechend ein Zehntel heraus.
   *Tipp: $v_1 = 1$, $v_2 = 1{,}9$, $v_3 = 2{,}71$ — Sie müssen nur noch aufsummieren.*
3. Jetzt wechselt der Gradient das Vorzeichen: $g = (1, -1, 1)$. Was macht Momentum, und
   warum ist das in einer engen Schlucht erwünscht?

*Antwortprobe: Bei (2) ist der zurückgelegte Weg knapp doppelt so lang wie bei (1).*

:::{admonition} Weiterlesen
:class: seealso
Prince, *UDL*, Abschnitte 6.3 und 6.4 (Momentum, Adam); Deisenroth et al., *MML*, Kap. 7 (Continuous optimization). Beide Bücher sind frei verfügbar, siehe [Über dieses Skript](../README.md).
:::
