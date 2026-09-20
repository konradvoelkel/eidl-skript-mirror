---
title: "Tensoren"
short_title: "Tensoren"
---

# Tensoren

## Tensoren in PyTorch

### Tensoren ≈ Arrays

Vier Fragen: Was ist ein Array? Was ist ein Tensor? Was ist ein Array in NumPy? Was ist ein Tensor in Torch?

* Ein **Array** ist eine Sammlung von Daten von gleichem Typ, die fortlaufend im Speicher liegen (können).
* Ein **Tensor** ist, je nachdem, wen man fragt:
  * Physiker: ein Objekt, das sich tensoriell transformiert.
  * Mathematiker: ein Element in einem Tensorproduktraum.
  * Informatiker: ein fancy Wort für Arrays.
* Ein **Tensor in Torch** ist eine Sammlung von Daten von gleichem Typ (dem `dtype`), die fortlaufend im Speicher liegen – und zwar potentiell im GPU-Speicher – optimiert für Gradientenabstiegsmethoden (Attribut `grad`, dazu mehr in den Kapiteln [„Gradientenabstieg“](../part-lernen/08-gradientenabstieg.md) und [„Autograd und Berechnungsgraph“](../part-lernen/10-autograd-berechnungsgraph.md)).

Man kann einen Torch-Tensor aus einem NumPy-Array herstellen, sogar ohne zusätzlichen Speicher zu verbrauchen (`torch.from_numpy` teilt sich den Speicher mit dem Array). Lesen Sie dazu das PyTorch-Tutorial „Tensors“.

### Ausflug: Tensoren in der Mathematik

Der Informatiker hat nicht ganz Unrecht, aber das mathematische Konzept hilft zu verstehen, was `shape` und `reshape` eigentlich bedeuten. Wer den Ausflug überspringen will, kann bei „Ausflug beendet“ weiterlesen.

**Tensorprodukt.** Gegeben Vektorräume $U, V, W$ (z.B. $V = \mathbb{R}^n$ und $W = \mathbb{R}^m$) kann man das Tensorprodukt bilden: $V \otimes W$ ist definiert als ein Vektorraum, sodass es eine 1:1-Korrespondenz gibt

$$
\{\text{bilineare Abbildungen } V \times W \to U\} \longleftrightarrow \{\text{lineare Abbildungen } V \otimes W \to U\}.
$$

Insbesondere gibt es eine bilineare Abbildung $V \times W \to V \otimes W$, $(v, w) \mapsto v \otimes w$. Wenn $v_1, \dots, v_n \in V$ und $w_1, \dots, w_m \in W$ Basen sind, so bilden die $v_i \otimes w_j$ eine Basis von $V \otimes W$; insbesondere ist $\dim(V \otimes W) = n \cdot m$ und $\mathbb{R}^n \otimes \mathbb{R}^m \cong \mathbb{R}^{nm}$.

**Dualraum.** Man kann den Dualraum bilden: $V^\vee := \operatorname{Hom}(V, \mathbb{R})$, die Menge der linearen Abbildungen $V \to \mathbb{R}$, ist ein neuer Vektorraum. Man nennt die Elemente von $V$ *Vektoren*, die Elemente von $V^\vee$ *Kovektoren* oder *Linearformen*. Wenn $v_1, \dots, v_n$ eine Basis von $V$ ist, sind die Linearformen $v_i^\vee := (v_i \cdot \,)$ eine Basis von $V^\vee$. Man sagt, die Elemente von $W \otimes V^\vee$ sind *kovariant* in $W$ und *kontravariant* in $V$; in Einstein-Notation schreibt man Indizes für $W$ unten, für $V^\vee$ oben.

Gegeben $\mathbb{R}^n$ mit der Standardbasis und dem Standardskalarprodukt können wir Vektoren in Kovektoren verwandeln (und zurück) durch Transponieren: Der Spaltenvektor $v \in \mathbb{R}^n$ wird zum Zeilenvektor $v^T \in (\mathbb{R}^n)^\vee$, und die Matrixmultiplikation $v^T w = v \cdot w \in \mathbb{R}$ ist das Skalarprodukt.

**Skalare, Vektoren und Matrizen als Tensoren.** Gegeben einen Vektorraum $V$ lässt sich das iterierte Tensorprodukt $V^{\otimes k} = V \otimes \dots \otimes V$ ($k$ mal) betrachten, mit der Konvention $V^{\otimes 0} = \mathbb{R}$ (denn $V \otimes \mathbb{R} = V$). Eine Matrix $M \in \mathbb{R}^{n \times m}$ lässt sich auffassen als lineare Abbildung $F \colon \mathbb{R}^m \to \mathbb{R}^n$; die Spalten der Matrix sind $F(e_1), \dots, F(e_m)$, die Bilder der Basisvektoren. Für jeden Vektor $v \in \mathbb{R}^m$ ist stets

$$
v = \sum_{i=1}^m (e_i \cdot v) \, e_i,
\qquad\text{also}\qquad
F(v) = \sum_{i=1}^m (e_i \cdot v) \, F(e_i),
$$

und damit

$$
F = \sum_{i=1}^m F(e_i) \, (e_i \cdot \,) = \sum_{i=1}^m F(e_i) \otimes e_i^\vee \;\in\; \mathbb{R}^n \otimes (\mathbb{R}^m)^\vee .
$$

Jedes Element eines Tensorproduktraums wird *Tensor* genannt – also auch Skalare $x \in \mathbb{R} = V^{\otimes 0}$, Vektoren $v \in V = V^{\otimes 1}$ und lineare Abbildungen $F \in \operatorname{Hom}(W, V) = V \otimes W^\vee$. Ein Skalar ist ein Tensor vom Rang 0, ein Vektor vom Rang 1, eine Matrix vom Rang 2. Und was ist $T \in \mathbb{R}^n \otimes \mathbb{R}^m \otimes (\mathbb{R}^p)^\vee \otimes (\mathbb{R}^q)^\vee$ für ein Tensor? Eine bilineare Abbildung $\mathbb{R}^p \times \mathbb{R}^q \to \mathbb{R}^n \otimes \mathbb{R}^m$, zum Beispiel – oder eine lineare Abbildung $\mathbb{R}^p \otimes \mathbb{R}^q \to \mathbb{R}^{n} \otimes \mathbb{R}^m$, oder vier Indizes, je nach Lesart.

**Obacht: lineare Abbildung ≠ Matrix.** Jede Matrix lässt sich als lineare Abbildung interpretieren. Umgekehrt lässt sich, gegeben eine Wahl von Basen, jede lineare Abbildung als Matrix schreiben, die *darstellende Matrix*. Genauso hat der gleiche Vektor $v \in V$ verschiedene darstellende Vektoren $[v]_B \in \mathbb{R}^n$ für verschiedene Basen $B$. Zu einem Tensor $T \in U \otimes V \otimes W$ lässt sich ebenso eine Darstellung finden, wenn man Basen von $U$, $V$ und $W$ wählt: Sie hat zu jedem Tripel von Indizes $(i, j, k)$ ein „Matrixelement“, nämlich den Koeffizienten von $u_i \otimes v_j \otimes w_k$. Das lässt sich dreidimensional darstellen, analog zur zweidimensionalen Darstellung für Matrizen.

**Zurück zu NumPy & Co.** In der Mathematik müssen wir uns zu einem Tensor merken, wie das Tensorprodukt zustande kam, um zu wissen, welche Variablen kovariant und welche kontravariant sind. Wählt man überall Basen, so verschwindet der Unterschied – man sieht nur noch die Koeffizienten. In NumPy arbeiten wir implizit mit Darstellungen in der Standardbasis von $\mathbb{R}^n$. Ist der Shape eines Arrays `a` z.B. `a.shape == (4, 10, 2)`, so bedeutet dies mathematisch gesehen

$$
a \in \mathbb{R}^4 \otimes \mathbb{R}^{10} \otimes \mathbb{R}^2 .
$$

:::{admonition} Quizfrage
:class: hint
Was macht `reshape`?
:::

Antwort: Wegen $\mathbb{R}^n \otimes \mathbb{R}^m \cong \mathbb{R}^{nm}$ hat $\mathbb{R}^4 \otimes \mathbb{R}^{10}$ eine Basis der Form $e_i \otimes e_j$ mit insgesamt $4 \cdot 10 = 40$ Elementen, also ist `a.reshape(-1, 2) == a.reshape(40, 2)` derselbe Tensor, nur mit anderer Klammerung der Faktoren. Reshape ändert keine Daten, nur die Interpretation des Speichers.

**Ausflug beendet.**

**Das Bild, das man sich für PyTorch merken sollte.** Der Shape sagt nur, wie viele Zahlen in jede Richtung gehen, nicht, welche Richtung was bedeutet. Das muss man sich selbst merken, und genau an dieser Stelle entstehen die Fehler, die keinen Fehler werfen, sondern ohne Murren einen sinnlosen Output produzieren (der Autor hat einmal bei einem quadratischen Bild die beiden Achsen vertauscht und lange gesucht). Die Konvention, die überall in PyTorch gilt: Die *erste* Achse ist der Batch. Ein Tensor mit Shape `(32, 784)` sind 32 Datenpunkte mit je 784 Features, eine Zeile pro Datenpunkt. `(32, 28, 28)` sind 32 Bilder, also 32 Matrizen übereinandergestapelt; `(32, 3, 28, 28)` dieselben Bilder mit drei Farbkanälen. `nn.Linear` und fast alle anderen Layer wirken auf die *letzte* Achse und lassen die Batch-Achse in Ruhe. Wer einen Tensor vor sich hat, sollte als Erstes sagen können, welche Achse der Batch ist und was die übrigen Achsen bedeuten; `reshape` und `view` ändern nur die Klammerung, nicht die Bedeutung.
