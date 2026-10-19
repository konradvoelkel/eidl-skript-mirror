# Was das Skript an Mathematik still voraussetzt (2026-10-19)

Befundnotiz, kein Plan. Entstanden aus Konrads Frage, worauf das Skript stillschweigend
aufbaut; das Ergebnis sind die beiden Kapitel
`part-grundlagen/hintergrundwissen-lineare-algebra.md` und
`part-grundlagen/hintergrundwissen-analysis.md`, beide am selben Tag geschrieben. Sie
stehen **nach** Kapitel 01 und tragen deshalb keine Nummer: Die erste Vorlesung braucht
keine Mathematik, ab der zweiten wird sie gebraucht, und dort laufen die ersten beiden
Übungsblätter.

## Methode

Alle 28 Kapitel in Lesereihenfolge nach Notation und Begriffen durchsucht (reguläre
Ausdrücke je Begriff), dazu `glossar.md` und die Übungsblätter 2026 in
`~/Sciebo/hhu/eidl-26/exercises/`. Gezählt wurde, in wie vielen Kapiteln ein Begriff
vorkommt und ab welchem; geprüft wurde von Hand, ob er dort eingeführt oder benutzt wird.

## Was das Buch selbst sauber einführt

Das ist der Teil, der beim Nachrüsten **nicht** gedoppelt werden darf:

* **Notation des Skalarprodukts** – Kapitel 01 legt `w · x` und `⟨w, x⟩` als gleichbedeutend fest.
* **Hyperebene, Normalenvektor, vorzeichenbehafteter Abstand** – Kapitel 02, vollständig
  hergeleitet, mit Zahlenbeispiel. Die beste mathematische Passage des Buchs.
* **Partielle Ableitung und Gradient** – Kapitel 08, anschaulich („ein Schritt nach Osten“).
* **Kettenregel in Matrixform, Summe über alle Pfade, numerischer Gradient-Check** – ebenfalls 08.
* **Standardisierung der Features samt Testset-Falle** – 08. **One-Hot** – 06.
* **Stochastik** wird verlinkt statt wiederholt: zehn Verweise ins Data-Science-Skript aus
  den Kapiteln 06, 07, 08 und 15.

## Was still vorausgesetzt war

| Begriff | ab Kapitel | Befund vor dem 2026-10-19 |
|---|---|---|
| `‖w‖`, euklidische Norm, Orthogonalität | 02 | benutzt, nirgends definiert, kein Glossareintrag |
| Matrixprodukt, Transponieren, Shapes | 05 | `Wx` zeilenweise erklärt (02), transponiert an sechs Stellen ohne Einführung |
| Jacobi-Matrix, „beste lineare Approximation“ | 08 | eine Zeile, danach trägt sie die Backpropagation |
| Logarithmusregeln, argmax | 06/07 | vorausgesetzt, genau dort, wo Maximum Likelihood kippt |
| kompakt, Supremum, Dichtheit | 13 | „kompakt“ in Klammern erklärt, der Rest gesetzt |
| Dichte, `N(μ,σ²)`, KL in geschlossener Form | 15 | ein Verweis ins DS-Skript, der Rest gesetzt |
| gleitende Mittel, Bias-Korrektur | 26 | gesetzt (Adam) |
| Broadcasting | 05 | steht **nur als Tipp in einer Übungsaufgabe** |
| Seeds, Determinismus | – | kommt im ganzen Buch nicht vor |
| Fairness, Verzerrung | – | kommt im ganzen Buch nicht vor |

Davon deckt das neue Kapitel die ersten beiden Zeilen ab, zusammen mit Winkel und
Normalisierung. Der Rest ist offen und steht in `TODO.md`.

## Die Übungsblätter, gegengelesen

Blatt 0 (2026, gleichlautend 2025): Hadamard-Produkt, Skalarprodukt mit Definition und
den drei Eigenschaften als **Beweisaufgaben**, Orthogonalität, Länge, Normalisierung,
„Einträge eines Einheitsvektors liegen in [−1, 1]“. Blatt 1: Winkel, NumPy, Matplotlib.

Zwei Dinge daran sind wichtig:

1. **Matrixprodukt und Transponieren stehen auf keinem der Blätter**, Transponieren nur
   als Notation `vᵀ` in einem Nebensatz. Die Lücke im Buch war also auch dort keine
   Wiederholung, sondern fehlte schlicht überall.
2. Die Definitionen sind dort richtig gesetzt; das Kapitel übernimmt sie **ohne die
   Beweise**, weil die Beweisaufgaben auf dem Blatt ihren Zweck behalten sollen. Das Buch
   nennt die drei Eigenschaften und sagt, dass sie in zwei Zeilen nachzurechnen sind.

**Ein Fehler auf dem Blatt**, beim Abgleich gefunden: In `blatt00.tex` steht im Satz zur
Länge `\Vert \lambda v \Vert = \lambda \Vert v \Vert`, die Lösung beweist korrekt
`|\lambda|`. Ohne Betrag ist die Aussage für negatives λ falsch. Das Kapitel schreibt es
mit Betrag; das Blatt liegt in einem anderen Repo und ist nicht angefasst.

## Was bewusst nicht ins Kapitel kam

* **Numerik als eigenes Thema** (Fließkomma, log-sum-exp, Überlauf, Seeds). Konrads
  Entscheidung vom 2026-10-19: nur als Nebenbemerkung. Im Kapitel sind es zwei – der
  Wurzelvergleich und die Division durch `‖v‖ = 0`.
* **Die Konstruktion eines orthogonalen Vektors** in der Ebene, weil genau das auf dem
  Blatt die Aufgabe ist.
* **Eigenwerte, Determinanten, quadratische Formen.** Im ganzen Buch kommen sie nicht vor
  (Singulärwerte genau einmal, Kapitel 26). Sie gehören zum Data-Science-Skript, nicht
  hierher.
