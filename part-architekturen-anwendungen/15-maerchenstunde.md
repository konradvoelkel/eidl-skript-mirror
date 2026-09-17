---
title: "VL 15: Märchenstunde"
short_title: "VL 15"
---

# Märchenstunde: Optimierer, Adversarial Attacks, Polysemie

:::{note} Stand
Erste Prosafassung (aus den Folien von VL 15, WiSe 2025/26). Abbildungen fehlen noch, siehe die `TODO`-Kommentare.
:::

Drei Märchen zum Abschluss – Themen, die über die Vorlesung hinausgehen, aber mit dem Gelernten schon verständlich sind.

## Ein Märchen über Optimierung: Adam oder was?

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

Der zweite Bestandteil von **Adam** (= Adaptive Moment Estimation) ist der adaptive Teil: Zusätzlich zu einer Heuristik zur besseren Schätzung der Gradienten der Loss-Funktion berechne die Quadrate – die Varianz des Gradienten, ebenfalls als exponentiell gewichtetes Mittel, komponentenweise:

$$
v_t := \beta_2 v_{t-1} + (1 - \beta_2)\, g_t^2, \qquad w_{t+1} := w_t - \rho\, \frac{m_t}{\sqrt{v_t} + \epsilon},
$$

mit typischerweise $\beta_2 = 0{,}999$ und $\epsilon = 10^{-8}$ gegen Division durch null. Ändert sich der Gradient stark, gehe kleine Schritte (das Loss Landscape ist steil). Ändert sich der Gradient wenig, gehe große Schritte (das Loss Landscape ist flach). Diese Technik kommt von RMSProp (Root Mean Square Propagation). Der Effekt ist eine **Lernrate pro Gewicht**: Gewichte mit selten großen Gradienten (z.B. Embeddings seltener Wörter) bekommen größere Schritte.

### Adam oder was?

Dahinter steckt also eine adaptive Lernrate, abhängig von der Varianz der Gradienten, einzeln für jedes Gewicht, sowie die Impuls-Heuristik zur verbesserten Gradientenschätzung. (Adam korrigiert außerdem die Schätzungen $m_t$, $v_t$ in den ersten Schritten für den Bias durch die Initialisierung mit null.) Wo geht das schief? Wenn die Lernrate nicht stark genug abgesenkt wird, findet die Optimierung nie das lokale Optimum und oszilliert darum herum. Deshalb kombiniert man Adam in der Praxis mit einem *Learning Rate Schedule*, der $\rho$ im Laufe des Trainings verkleinert.

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

Genau genommen liegt der Gradient der Loss-Funktion an einem Punkt des Gewichtsraums im *Kotangentialraum* des Graphen der Loss-Funktion – er ist eine Linearform, die Änderungsrichtungen Zahlen zuordnet (Kapitel 3: Kovektoren!). Um einen Vektor aus dem Gewichtsraum daraus zu machen, mit dem wir einen Schritt gehen können, müssen wir „dualisieren“. Dabei kann man verschiedene Geometrien betrachten:

* Die **euklidische Geometrie**, einfach $\mathbb{R}^n$ mit dem Standardskalarprodukt; dann kann man die Zahlen, die man ausrechnet, wie gehabt als Vektor in $\mathbb{R}^n$ auffassen. Das ist SGD.
* Die **Riemannsche Geometrie**, die durch die Fisher-Informationsmatrix gegeben ist – der *Natural Gradient* (Amari). Die Fisher-Matrix ist die zweite Ableitung der relativen Entropie; Schritte werden so gemessen, wie stark sich die *Ausgabeverteilung* des Modells ändert, nicht die Gewichte.
* Verschiedene andere sogenannte affine Geometrien; das ist ein aktives Forschungsgebiet in der Optimierungstheorie, Stichwort **Informationsgeometrie**. Z.B. Derun Zhou, Keisuke Yano, Mahito Sugiyama: *Dual Riemannian Newton Method on Statistical Manifolds* (2025), [arXiv:2511.11318](https://arxiv.org/pdf/2511.11318).

Adam und Muon sind in diesem Bild billige Näherungen an eine bessere Geometrie des Gewichtsraums.

## Ein Märchen über Adversarial Attacks

### Definition

Die gezielte Manipulation des Inputs eines Machine-Learning-Modells, um ein spezifisch falsches Ergebnis oder ein unerwartetes Verhalten zu produzieren. Die Manipulation ist häufig nicht direkt für Menschen zu erkennen.

Beispiel: die gezielte Manipulation des Inputs eines Bildklassifikators, um eine spezifisch falsche Klasse zu produzieren. Also: Wir stecken einen weißen Hai rein, aber „die KI“ sagt „Goldfisch“ dazu. Reingelegt!

### Theorie

Wir betrachten den Eingaberaum „Menge aller Bilddateien“ ($[0, 1]^{3 \cdot H \cdot W}$) sowie die Eingabemenge „Menge aller Trainingsbilder“. Das Modell lernt Entscheidungsgrenzen im Eingaberaum, um Klassenlabel zu vergeben. Hypothese: Nahe der Entscheidungsgrenze liegen *adversarial examples* – und da die Trainingsbilder nur auf einer winzigen Teilmenge des Eingaberaums liegen (Manifold-Hypothese), verläuft die Entscheidungsgrenze fast überall dicht an jedem Bild vorbei, nur in Richtungen, die „aus der Mannigfaltigkeit heraus“ zeigen und für Menschen wie Rauschen aussehen.

Das ist die These der Bachelorarbeit „Das Dimpled Manifold Model als Erklärung für die Existenz und die Eigenschaften von Adversarial Examples“ von N. Wieczorek (HHU 2023), nach Shamir et al. 2021: Die Entscheidungsgrenze schmiegt sich wie eine Folie mit kleinen Dellen (*dimples*) an die Datenmannigfaltigkeit an.

<!-- TODO Abbildung: Dimpled Manifold (aus der BA Wieczorek 2023) -->

### Wie wird's gemacht?

Mit Gradientenabstiegsmethoden sucht man, ausgehend von einem Bild eines weißen Hais, Richtungen, die die Klassifikation ändern, ohne besonders viel am Bild zu ändern:

$$
x_{\text{adv}} := x + \epsilon \cdot \operatorname{sign}\bigl(\nabla_x L(f(x), y_{\text{Ziel}})\bigr)
$$

(Fast Gradient Sign Method, Goodfellow et al. 2014) oder iterativ mit kleinen Schritten. Anders als sonst: Gradientenabstieg im **Eingaberaum**, nicht im Gewichtsraum – Backpropagation liefert $\nabla_x$ genauso wie $\nabla_w$, denn im DAG ist $x$ nur ein weiteres Blatt.

Dass das nicht nur mit Pixeln funktioniert: Sharif et al. 2016, *Accessorize to a Crime: Real and Stealthy Attacks on State-of-the-Art Face Recognition* – eine bedruckte Brillenfassung lässt ein Gesichtserkennungssystem eine andere Person erkennen. Und aus dem Heise-Newsticker vom 2.2.2026: [Manipulierte Straßenschilder: Wenn das autonome Auto Fußgänger umfährt](https://www.heise.de/news/Manipulierte-Strassenschilder-Wenn-das-autonome-Auto-Fussgaenger-umfaehrt-11162744.html).

## Ein Märchen über Polysemie

(Folien von Ben Ruppik, aus der Vorlesung *Topological Data Analysis* im Master AI & Data Science, Juni 2025; siehe `from_2025/slides/2025-06-09 TDA guest lecture Ben Ruppik.pdf`.)

**Manifold Hypothesis**: High-dimensional data lies on or near a low-dimensional structure called a *manifold*. Das ist die Annahme hinter allem, was wir über latente Räume gesagt haben: Der Autoencoder findet die Parametrisierung der Mannigfaltigkeit, der VAE glättet sie, word2vec legt Wörter auf eine Mannigfaltigkeit, auf der Richtungen Bedeutung haben.

**Problems with the Manifold Hypothesis**: Sometimes data does *not* have a low-dimensional structure and cannot be effectively mapped onto a lower-dimensional space – wegen Rauschen, oder wegen zu weniger Samples, sodass die zugrundeliegende Struktur nicht geschätzt werden kann. Und manchmal ist die Struktur zwar niedrigdimensional, aber keine Mannigfaltigkeit: Zwei Kurven, die sich kreuzen, haben am Schnittpunkt keine eindeutige Tangente.

Genau das passiert bei **Polysemie**: Ein Wort wie „Maus“ (Tier, Computermaus) oder „Bank“ (Sitzgelegenheit, Geldinstitut) hat mehrere Bedeutungen, die in verschiedenen Kontexten vorkommen. Im Embedding-Raum eines kontextabhängigen Modells (BERT) liegen die Vorkommen von „Maus“ auf mehreren „Ästen“, die sich an einem Punkt treffen – eine *Singularität* der Datenmannigfaltigkeit. Topologische Datenanalyse (persistent homology, lokale Dimension) kann solche Singularitäten finden und damit polyseme Wörter *ohne Wörterbuch* aus den Embeddings entdecken. word2vec mit einem Vektor pro Wort kann das prinzipiell nicht: Es muss alle Bedeutungen in einen Punkt mitteln.

<!-- TODO Abbildungen: Manifold-Hypothese, Problemfälle (Rauschen, Kreuzung), Polysemie-Beispiel (Folien 36–41, Ben Ruppik) -->

Damit schließt sich der Kreis zur Kernfrage aus Kapitel 8: Welche Struktur finden wir im Latent Space? Manchmal eine schöne Mannigfaltigkeit – und manchmal etwas Interessanteres.
