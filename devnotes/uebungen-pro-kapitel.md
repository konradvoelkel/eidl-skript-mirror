# Vorschlag: ein kleiner Übungsabschnitt je Kapitel

Stand 2026-09-27. Entschieden am selben Tag: `part-exercises/` ist aus dem TOC und aus dem
Repository (siehe `uebungen-2025/README.md`). Die **echten** Blätter werden in TeX gepflegt
und über ILIAS ausgegeben; im Skript stehen statt dessen kleine Übungen zum Mitrechnen beim
Lesen.

Dieses Dokument ist ein **Vorschlag**, kein Beschluss: **23 Abschnitte mit 56 Aufgaben**,
jeweils mit Herkunft (welche Aufgabe von 2025 er variiert) und, wo einschlägig, dem Bezug
zum Klausur-Aufgabenschatz (`klausur-abdeckung.md`).

Der erste Entwurf hatte 27 Abschnitte mit 75 Aufgaben. Ein Viertel ist gestrichen — vier
ganze Abschnitte und neun einzelne Teilaufgaben; die Liste mit den Gründen steht am Ende.
Vier Kapitel (04, 17, 21, 22) haben damit **keinen** Übungsabschnitt, und das ist in Ordnung:
Eine schwache Übung ist schlechter als keine.

## Die Konvention, die ich vorschlage

* **Ein Abschnitt `## Übung` am Kapitelende**, vor „Weiterlesen“, mit Anker
  `(<kapitel>uebung)=`.
* **Ein bis drei Aufgaben**, jede in zwei bis fünf Zeilen. Wer das Kapitel gelesen hat, soll
  sie in fünf bis fünfzehn Minuten mit Papier schaffen — keine Programmieraufgaben, für die
  man eine Umgebung aufsetzt. Die gehören auf die echten Blätter.
* **Mehr Hinweise als auf dem Blatt.** Das ist der Unterschied: Hier liest jemand allein,
  ohne Übungsgruppe. Ein `Tipp:`-Satz je Aufgabe, der den ersten Schritt verrät.
* **Keine Lösungen.** Statt dessen eine *Antwortprobe* — eine nachprüfbare Zahl oder
  Eigenschaft, an der man selbst merkt, ob man richtig liegt („die Summe muss 1 ergeben“,
  „es müssen 8 Kanten sein“). Damit bleibt die Übung selbstkontrollierend, ohne dass die
  Rechnung im Buch steht.
* **Ein Satz Einordnung**, wo die Aufgabe im echten Blatt wiederkommt bzw. was in der
  Klausur daraus wird.

Der Vorschlag hält sich an Stoff, der im jeweiligen Kapitel **steht** — keine Aufgabe
braucht ein späteres Kapitel.

---

## Grundlagen

### 01 — Was ist Deep Learning?

**Vorschlag.** Eine Rechnung; das Kapitel selbst rechnet nichts.

> Ein Rissdetektor findet unter 200 Bauteilen 30 als „rissig“ markierte, davon sind 24
> tatsächlich rissig; insgesamt gibt es 40 rissige Bauteile. Berechnen Sie Precision und
> Recall. Welche der beiden Zahlen würden Sie in der Qualitätssicherung höher gewichten,
> und warum?
> *Antwortprobe: beide Werte liegen zwischen 0,5 und 0,9, und sie sind verschieden.*

**Herkunft.** Neu. **Klausurbezug:** Precision/Recall/mAP steht in `klausur-abdeckung.md`
als **fehlend** markiert — das wäre der Ort, es unterzubringen. Ebenso „Deep Learning =
viele Layer trainieren“ und Object Detection vs. Klassifikation.

### 02 — Neuron und Perzeptron

**Vorschlag.** Die Geometrie-Aufgabe, die 2025 Blatt 1 Aufgabe 4b war — mit den Hinweisen,
die dort in der Übungsgruppe mündlich fielen.

> Sei $w = \binom{3}{4}$ und $b = -5$, also das Perzeptron $x \mapsto [w \cdot x + b > 0]$.
> 1. Berechnen Sie für $x_1 = \binom{4}{2}$, $x_2 = \binom{-1}{0}$ und $x_3 = \binom{3}{-1}$
>    jeweils die Aktivierung $w \cdot x + b$ **und** den vorzeichenbehafteten Abstand zur Geraden.
>    *Tipp: Der Abstand ist die Aktivierung geteilt durch $\|w\|$, und $\|w\| = 5$.*
> 2. Ersetzen Sie $w$ durch $10w$ und $b$ durch $10b$. Was ändert sich an der Geraden, was an
>    den Aktivierungen, was an den Abständen?
>    *Antwortprobe: Genau eine der drei Größen ändert sich.*

**Herkunft.** Blatt 1 Aufgabe 4b, Zahlen unverändert, Teil 3 als Pointe ergänzt.
**Klausurbezug:** „Perzeptron ohne Bias geht nur durch den Ursprung“ — in
`klausur-abdeckung.md` als **fehlend** markiert; Teil 3 ist der natürliche Ort, das als
Zusatzfrage anzuhängen („was passiert mit $b = 0$?“).

### 03 — Das Perzeptron trainieren

**Vorschlag.** Ein Update von Hand, die Variante von Blatt 3 Aufgabe 4 — dort abstrakt,
hier mit Zahlen.

> Gegeben ein Datenpunkt $x = \binom{2}{1}$ mit Label $y = 1$ und ein Perzeptron mit
> $w^{(0)} = \binom{-3}{1}$, also $w^{(0)} \cdot x = -5 < 0$: Das Perzeptron sagt $0$, richtig
> wäre $1$.
> 1. Führen Sie einen Schritt der Perzeptronregel $w^{(1)} = w^{(0)} + r\,(y - f(x))\,x$ mit
>    $r = 0{,}5$ aus.
> 2. Berechnen Sie $w^{(1)} \cdot x$. Um wie viel hat sich die Aktivierung geändert?
>    *Tipp: Rechnen Sie die Differenz einmal allgemein mit der Bilinearität des
>    Skalarprodukts aus — Sie bekommen $r\,\|x\|^2$, unabhängig von $w^{(0)}$.*
> 3. Wie viele solche Schritte braucht es mindestens, bis die Aktivierung positiv wird?
>    *Antwortprobe: eine ganze Zahl, und Sie können sie ausrechnen, ohne zu iterieren.*

**Herkunft.** Blatt 3 Aufgabe 4, mit konkreten Zahlen und dem allgemeinen Argument als Tipp.
**Klausurbezug:** Perzeptron-Konvergenz, Iverson-Klammer.

### 05 — Tensoren

**Vorschlag.** Shapes im Kopf — die Vorübung zu dem, was in der Klausur als
Code-Verständnis kommt.

> 1. Welchen Shape hat das Ergebnis? (a) `torch.zeros(4,3) @ torch.zeros(3,7)`,
>    (b) `x.sum(dim=0)` für `x` mit Shape $(8, 5)$, (c) `x.unsqueeze(1)` für `x` mit Shape
>    $(8,)$, (d) `torch.zeros(4,1) + torch.zeros(1,6)`.
>    *Tipp: Bei (d) hilft die Broadcasting-Regel: Achsen der Länge 1 werden gedehnt.*
> 2. Ein Batch von 32 Graustufenbildern der Größe $28 \times 28$ liegt als Tensor vor.
>    Welchen Shape hat er in PyTorch-Konvention, und welchen nach `nn.Flatten()`?
>    *Antwortprobe: Das Produkt der Shape-Einträge ändert sich bei (2) nicht.*

**Herkunft.** Neu. **Klausurbezug:** „Tensor Rang 0 = Skalar“, `Conv2d`/`MaxPool2d`-Shapes
(A3) — dies ist die Vorübung dazu.

---

## Lernen

### 06 — Logistische Regression

**Vorschlag.** Die Ableitung von $\sigma$, also Blatt 5 Aufgabe 1, mit dem Rechenweg als
Treppe statt als Sprung.

> 1. Zeigen Sie $\sigma(-x) = 1 - \sigma(x)$.
>    *Tipp: Erweitern Sie $\sigma(-x) = \frac{1}{1+e^{x}}$ mit $e^{-x}$.*
> 2. Zeigen Sie $\sigma'(x) = \sigma(x)\,\sigma(-x)$.
>    *Tipp: Quotientenregel, dann mit $1/\sigma(-x)$ multiplizieren und so lange umformen,
>    bis die Definition von $\sigma(x)$ dasteht. Mit Teil 1 ist das dasselbe wie die aus der
>    Literatur bekannte Form $\sigma(x)(1-\sigma(x))$.*
> 3. Wie groß ist $\sigma'(0)$? Und wie groß sind die Odds bei $p = 0{,}5$?
>    *Antwortprobe: Eine der beiden Zahlen ist $1$, die andere nicht.*

**Herkunft.** Blatt 5 Aufgabe 1, um Teil 1 als Zwischenschritt und Teil 3 als Zahlenprobe
ergänzt. **Klausurbezug:** „Sigmoid-Ausgabe als Wahrscheinlichkeit“, „Odds bei $p=0{,}5$
sind 1:1“.

### 07 — Loss-Funktionen und Maximum Likelihood

**Vorschlag.** Blatt 5 Aufgabe 4, aber in zwei Schritten und mit einer Zahlenprobe davor.

> 1. Für $q = (0{,}0\ ,\ 1{,}0)$ (das wahre Label ist 1) und $p = (0{,}2\ ,\ 0{,}8)$:
>    Berechnen Sie $BCE(q,p)$ und $H(q)$.
>    *Tipp: $0 \log 0$ wird als $0$ gelesen. $H(q)$ ist hier besonders einfach.*
> 2. Zeigen Sie allgemein $D(q \Vert p) = BCE(q,p) - H(q)$.
>    *Tipp: Schreiben Sie den Logarithmus des Quotienten als Differenz von Logarithmen und
>    sortieren Sie nach $p$ und $q$.*
> 3. Warum darf man beim Training statt $D(q \Vert p)$ einfach $BCE(q,p)$ minimieren?
>    *Antwortprobe: In Teil 1 muss $D(q\Vert p) = BCE(q,p)$ herauskommen.*

**Herkunft.** Blatt 5 Aufgabe 4, um den Zahlenfall davor ergänzt. **Klausurbezug:**
„Kreuzentropie = NLL = KL (bis auf Entropie)“.

### 08 — Gradientenabstieg

**Vorschlag.** Blatt 3 Aufgabe 2b — eine Rechnung, die alles enthält, was in der Klausur
als A4 wiederkommt.

> Sei $x = (2, -1)$ fest und $L(w) := (1 - w \cdot x)^2$.
> 1. Bestimmen Sie $\frac{\partial L}{\partial w_1}$ und $\frac{\partial L}{\partial w_2}$
>    mit der Kettenregel.
>    *Tipp: Äußere Funktion $u \mapsto u^2$, innere $w \mapsto 1 - w\cdot x$. Die Ableitung
>    von $w \cdot x$ nach $w_j$ ist $x_j$ — mehr steckt nicht dahinter.*
> 2. Werten Sie den Gradienten bei $w = (0,0)$ aus und führen Sie einen Schritt mit
>    Lernrate $\rho = 0{,}1$ aus.
> 3. Berechnen Sie $L$ vor und nach dem Schritt.
>    *Antwortprobe: $L$ muss kleiner geworden sein.*

**Herkunft.** Blatt 3 Aufgabe 2b, um den Schritt und die Probe ergänzt. **Klausurbezug:**
Kettenregel, Lernrate zu groß/zu klein, SGD nutzt nicht den ganzen Datensatz.

### 09 — Backpropagation

**Vorschlag.** Blatt 7 Aufgabe 1 ist mit zwei Layern à zwei Neuronen für eine
Leseübung zu groß. Hier ein Neuron je Layer, dieselbe Mechanik.

> Ein Netz $x \to y = \mathrm{ReLU}(v\,x) \to z = \mathrm{ReLU}(w\,y)$ mit $v = 2$, $w = -1$,
> Eingabe $x = 3$ und Ziel $t = 1$; Loss $L = \tfrac12 (z-t)^2$.
> 1. Forward Pass: Berechnen Sie $y$, $z$ und $L$.
> 2. Berechnen Sie $\frac{\partial L}{\partial w}$ und $\frac{\partial L}{\partial v}$.
>    *Tipp: $\frac{\partial L}{\partial z} = z - t$, die schwache Ableitung von ReLU an der
>    Stelle $a$ ist $[a > 0]$, und der Gradient eines Gewichts ist Eingabe des Neurons mal
>    Ableitung des Fehlers nach seiner Ausgabe.*
> 3. Setzen Sie $w = +1$ und rechnen Sie noch einmal. Was hat sich an
>    $\frac{\partial L}{\partial v}$ qualitativ geändert, und warum?
>    *Antwortprobe: In genau einem der beiden Fälle ist $\frac{\partial L}{\partial v} = 0$.*

**Herkunft.** Blatt 7 Aufgabe 1, auf ein Neuron je Layer verkleinert; Teil 3 zielt auf die
ReLU-Maske. **Klausurbezug:** A4 Backprop-Rechnung, ReLU-Ableitung, Vanishing Gradient.

### 10 — Autograd und Berechnungsgraph

**Vorschlag.** Zwei Fragen, die man am Code beantwortet, ohne ihn auszuführen.

> 1. Ein Modell hat drei Layer. Vor dem Training wird für Layer 1 und 2
>    `requires_grad = False` gesetzt. Welche Tensoren bekommen im Backward Pass einen
>    `.grad`, welche nicht — und wo wird trotzdem noch gerechnet?
>    *Tipp: Der Gradient muss durch Layer 2 hindurch, damit Layer 3 … nein, andersherum.
>    Zeichnen Sie den Graphen und verfolgen Sie die Pfeile rückwärts.*
> 2. Ein Gewicht $k$ wird an drei Stellen im Graphen benutzt (geteilte Gewichte, wie bei
>    einer Faltung). Wie viele Beiträge hat $\frac{\partial L}{\partial k}$, und wie werden
>    sie verrechnet?
>    *Antwortprobe: Bei (1) spart das Einfrieren Speicher, aber nicht jede Rechnung.*

**Herkunft.** Aus dem Kapitel selbst (Abschnitte „Freezing“ und „Geteilte Gewichte“).
**Klausurbezug:** `requires_grad`/Einfrieren/Speicher, Berechnungsgraph/DAG, Transfer
Learning.

### 11 — Aktivierungsfunktionen

**Vorschlag.** Ein totes Neuron zum Anfassen.

> Ein Neuron $x \mapsto \mathrm{ReLU}(w \cdot x + b)$ mit $w = (-1, -1)$ und $b = -3$ sieht
> nur Trainingsdaten mit nichtnegativen Einträgen.
> 1. Zeigen Sie: Die Ausgabe ist für **alle** diese Daten $0$.
> 2. Welchen Wert hat der Gradient nach $w$ und $b$ dann? Was folgt daraus für das Training?
>    *Antwortprobe: Bei (2) ist die Antwort für $w$ und $b$ dieselbe.*

**Herkunft.** Neu, aus „Problem bei ReLU: sterbende Neuronen“. **Klausurbezug:**
Sterbende Neuronen/Swish, ReLU-Ableitung, Vanishing Gradient bei Sigmoid.

### 12 — Netze von Hand bauen

**Vorschlag.** Das Kapitel baut OR, NOR und XOR vor. Die Übung baut eines selbst.

> 1. Geben Sie Gewichte und Bias für ein einzelnes Perzeptron an, das AND auf
>    $\{0,1\}^2$ berechnet. Prüfen Sie alle vier Eingaben nach.
> 2. Bauen Sie NAND aus Ihrem AND, ohne neu zu rechnen.
>    *Tipp: Was macht das Vorzeichenwechseln von $w$ und $b$ mit der Entscheidungsgrenze?*
>    *Antwortprobe: Bei (1) gibt es viele richtige Antworten; alle erfüllen dieselben vier
>    Ungleichungen.*

**Herkunft.** Neu, parallel zu den OR/NOR/XOR-Beispielen des Kapitels.
**Klausurbezug:** Perzeptron ohne Bias, lineare Trennbarkeit.

### 13 — Universelle Approximation

**Vorschlag.** Die Stufe explizit bauen — das Argument des Satzes in Zahlen.

> 1. Geben Sie zwei ReLU-Neuronen und Ausgabegewichte an, deren Summe die Funktion
>    $f(x) = 1$ für $x \in [1,2]$ und $0$ sonst **näherungsweise** darstellt.
>    *Tipp: Zwei steile Rampen an den Stellen $1$ und $2$, die zweite mit umgekehrtem
>    Vorzeichen. Der Steilheitsparameter $h$ bestimmt, wie gut die Näherung ist.*
> 2. Wie viele Neuronen brauchen Sie für eine Treppenfunktion mit $k$ Stufen?
>    *Antwortprobe: Die Antwort auf (2) ist linear in $k$.*

**Herkunft.** Neu, direkt aus dem Beweis in fünf Schritten im Kapitel.
**Klausurbezug:** Universal Approximation.

---

## Representation Learning

### 14 — Autoencoder

**Vorschlag.** Blatt 6 und 8 sind Code-Blätter; die Leseübung ist eine Architekturrechnung.

> Ein Autoencoder für MNIST: $784 \to 128 \to 32 \to 128 \to 784$, alle Layer voll
> verbunden mit Bias.
> 1. Wie viele Parameter hat er? Wie viele davon im Encoder?
>    *Tipp: Ein Layer $n \to m$ hat $n\cdot m + m$ Parameter.*
> 2. Beim Denoising-Autoencoder: Auf welche der beiden Größen — Eingabe oder Zielbild —
>    kommt das Rauschen, und was wäre der Effekt, wenn man es auf die andere legte?
>    *Antwortprobe: Bei (1) liegt das Ergebnis zwischen 200 000 und 250 000.*

**Herkunft.** Neu; Teil 3 ist die Kernaussage des Abschnitts „Denoising Autoencoder“.
**Klausurbezug:** Decoder erhöht Dimension, AE approximiert Identität, AE braucht keine
Label, Denoising-AE (Rauschen auf Input, nicht auf Loss).

### 15 — Variational Autoencoder

**Vorschlag.** Blatt 9 Aufgabe 1 verlangt die Herleitung der KL-Formel — für eine Leseübung
zu lang. Hier der Effekt statt der Herleitung, plus eine Zahl.

> Der variational loss term für eine latente Dimension ist
> $\tfrac12\left(\mu^2 + \sigma^2 - \ln \sigma^2 - 1\right)$.
> 1. Für welches Paar $(\mu, \sigma)$ wird er null? Rechnen Sie nach, dass er dort ein
>    Minimum hat.
>    *Tipp: Leiten Sie nach $\mu$ und nach $\sigma$ getrennt ab.*
> 2. Berechnen Sie den Wert für $(\mu,\sigma) = (2, 1)$ und für $(0\ ,\ 0{,}5)$. Welche der
>    beiden Abweichungen bestraft der Term stärker?
> 3. Der Reparametrisierungstrick schreibt $z = \mu + \sigma\varepsilon$ mit
>    $\varepsilon \sim \mathcal{N}(0,1)$. Warum lässt sich ohne ihn nicht nach $\mu$ und
>    $\sigma$ ableiten?
>    *Antwortprobe: Bei (2) ist genau ein Wert größer als 1.*

**Herkunft.** Blatt 9 Aufgabe 1, Herleitung durch Auswertung ersetzt.
**Klausurbezug:** Reparametrisierungstrick, `logvar` (in `klausur-abdeckung.md` als
**fehlend** markiert — Teil 1 ist der Ort, `logvar` statt $\sigma$ zu erwähnen), Standard-AE
nicht generativ.

### 16 — Wortvektoren: word2vec

**Vorschlag.** Trainingspaare abzählen — daran hängt der Unterschied CBOW/Skip-gram.

> Der Satz „der hund bellt laut im garten“ (6 Token), Fenstergröße $n = 2$.
> 1. Wie viele (Kontext, Zielwort)-Paare erzeugt Skip-gram daraus? Schreiben Sie die Paare
>    für das Zielwort „bellt“ auf.
>    *Tipp: Am Satzanfang und -ende ist das Fenster kleiner.*
> 2. Was ist bei CBOW Eingabe und was Ausgabe — und wie herum ist es bei Skip-gram?
> 3. Der Embedding-Layer für ein Vokabular von 50 000 Wörtern und 300 Dimensionen: Wie viele
>    Parameter, und was steht in Zeile $i$?
>    *Antwortprobe: Bei (3) sind es 15 Millionen.*

**Herkunft.** Neu. **Klausurbezug:** CBOW vs. Skip-gram Richtung, Embedding-Layer für IDs,
Top-k-Sampling.

### 18 — Recurrent Neural Networks

**Vorschlag.** Ein RNN drei Schritte von Hand ausrollen.

> Ein RNN mit $h_t = \tanh(w\,x_t + u\,h_{t-1})$, $w = 1$, $u = 0{,}5$, $h_0 = 0$ und der
> Eingabefolge $x = (1, 0, 0)$.
> 1. Berechnen Sie $h_1, h_2, h_3$ (zwei Nachkommastellen genügen).
> 2. Wiederholen Sie mit $u = 0{,}1$ und mit $u = 0{,}9$. Wie lange „erinnert“ sich das Netz
>    jeweils an die 1 vom Anfang?
>    *Tipp: Nach dem ersten Schritt ist die Eingabe 0, es bleibt also eine Multiplikation
>    mit $u$ pro Schritt.*
>    *Antwortprobe: Bei (2) fällt einer der drei Verläufe deutlich langsamer ab als die
>    anderen.*

**Herkunft.** Neu. **Klausurbezug:** RNN speichert vorherige Schritte, GRU/LSTM,
Vanishing Gradient, LSTM/RNN für Zeitreihen.

### 19 — Transformer

**Vorschlag.** Ein Attention-Schritt mit drei Token und Zahlen, die im Kopf gehen.

> Drei Token mit Query-Key-Skalarprodukten $q \cdot k_1 = 2$, $q \cdot k_2 = 2$,
> $q \cdot k_3 = 0$ und Values $v_1 = 1$, $v_2 = 3$, $v_3 = 10$.
> 1. Berechnen Sie die Attention-Gewichte mit Softmax (ohne Skalierung) und daraus die
>    Ausgabe.
>    *Tipp: Zwei der drei Exponenten sind gleich; $e^2 \approx 7{,}39$.*
> 2. Die Gewichte müssen sich zu 1 summieren — prüfen Sie das nach.
> 3. Warum braucht ein Transformer Positionsembeddings, ein RNN aber nicht?
>    *Antwortprobe: Die Ausgabe liegt näher an 3 als an 10.*

**Herkunft.** Neu, aus „Transformer technisch“. **Klausurbezug:** Softmax summiert zu 1,
Positionsembedding, BERT: Masked LM.

---

## Architekturen und Anwendungen

### 20 — Faltung und Convolutional Neural Networks

**Vorschlag.** Blatt 10 Aufgabe 1 mit einem kürzeren Signal, dazu die Shape-Formel — das
ist der am besten belegte Klausurstoff im ganzen Skript.

> Signal $g = (3, 1, 4, 1, 5)$ an den Stellen $x = 0..4$, Filter
> $f = (\tfrac12, 0, -\tfrac12)$ an den Stellen $-1, 0, 1$.
> 1. Berechnen Sie $(g \ast f)(x)$ für $x = 1, 2, 3$ mit
>    $(g \ast f)(x) = \sum_k g(x-k) f(k)$.
>    *Tipp: Nur drei Summanden je Stelle, und einer davon fällt weg.*
> 2. Berechnen Sie Max-Pooling von $g$ mit Poolgröße 2 und Stride 2.
> 3. Ein $28\times28$-Bild geht durch `Conv2d(1, 16, kernel_size=5)`, dann
>    `MaxPool2d(2)`, dann `Conv2d(16, 16, kernel_size=5)`, dann `MaxPool2d(2)`. Welchen
>    Shape hat die Ausgabe, und wie viele Werte hat sie nach `Flatten`?
>    *Tipp: $\lfloor (n + 2p - k)/s \rfloor + 1$, hier ohne Padding.*
>    *Antwortprobe: Bei (3) kommt $16 \cdot 4 \cdot 4$ heraus — die Zahl taucht in
>    PyTorch-Beispielen ständig auf.*

**Herkunft.** Blatt 10 Aufgabe 1, Signal von 10 auf 5 Stellen gekürzt; Teil 3 ist die in
`klausur-abdeckung.md` als fehlend gemeldete Shape-Rechnung, die inzwischen als Abschnitt
„Ausgabegröße einer Faltungsschicht“ im Kapitel steht. **Klausurbezug:** A3
Code-Verständnis, Stride reduziert Feature Map, $1\times1$-Faltung, Parameter Sharing,
Translationsäquivarianz, Gauß-Kernel glättet.

### 23 — Latente Räume geometrisch

**Vorschlag.** Analogierechnung mit Zahlen statt mit Wörtern — dann sieht man, dass nichts
Magisches passiert.

> Gegeben Embeddings $\text{KÖNIG} = (4,2)$, $\text{MANN} = (3,0)$, $\text{FRAU} = (1,1)$.
> 1. Berechnen Sie $\text{KÖNIG} - \text{MANN} + \text{FRAU}$. Welcher der Vektoren
>    $a = (4,6)$, $b = (2,2)$, $c = (0,4)$ liegt am nächsten — gemessen mit dem Kosinus?
>    *Tipp: Kosinus heißt: normieren, dann Skalarprodukt. Die Längen unterscheiden sich hier
>    deutlich, das Ergebnis mit euklidischem Abstand wäre ein anderes.*
> 2. Interpolieren Sie linear zwischen $\text{MANN}$ und $\text{FRAU}$ in drei Schritten.
>    *Antwortprobe: Bei (1) sind die Antworten für Kosinus und euklidischen Abstand
>    verschieden — das ist der Punkt der Aufgabe.*

**Herkunft.** Neu, aus „Arithmetik im Latent Space“ und „Interpolation und Superposition“.
**Klausurbezug:** Empfehlungssystem im Latent Space, AE vs. VAE.

### 24 — Anwendungsbeispiele

**Vorschlag.** Das „Rezept“ des Kapitels einmal selbst anwenden — das ist Aufgabentyp A2
der Klausur, in klein.

> Ein Verlag möchte eingehende Leserbriefe automatisch an die richtige Redaktion leiten
> (acht Ressorts).
> Gehen Sie die sechs Punkte des Rezepts durch: Was haben wir, was soll herauskommen,
> welches Modell und woher, welcher Loss, womit messen wir Güte, was kann schiefgehen.
> *Tipp: Die Antwort auf „welches Modell und woher“ ist in diesem Kapitel nie „selbst
> trainieren“, solange es ein vortrainiertes gibt.*
> *Antwortprobe: Beim Loss sollte etwas mit „Kreuzentropie“ dastehen, bei der Güte etwas
> anderes als „Accuracy“ — die Ressorts sind ungleich häufig.*

**Herkunft.** Neu, direkt auf „Rezept: ein Anwendungskonzept schreiben“ gemünzt.
**Klausurbezug:** A2 (Müllerkennung, Lagerbestände, Produktbeschreibungen) — derselbe
Aufgabentyp.

### 25 — Destillation

**Vorschlag.** Temperatur ausrechnen, weil das $T^2$ sonst Formelwissen bleibt.

> Ein Lehrermodell gibt für drei Klassen die Logits $(3, 1, 0)$ aus.
> 1. Berechnen Sie die Softmax-Ausgabe bei $T = 1$ und bei $T = 2$ (also mit $z_j / T$ im
>    Exponenten).
>    *Tipp: $e^3 \approx 20{,}1$, $e^{1{,}5} \approx 4{,}48$, $e \approx 2{,}72$,
>    $e^{0{,}5} \approx 1{,}65$.*
> 2. Welche Information steckt in der Ausgabe bei $T = 2$, die bei $T = 1$ fast verschwunden
>    ist? Wie heißt sie im Kapitel?
> 3. Warum wird der Distillation Loss mit $T^2$ multipliziert?
>    *Antwortprobe: Bei beiden Temperaturen summieren sich die drei Werte zu 1, aber der
>    größte ist bei $T=2$ deutlich kleiner.*

**Herkunft.** Neu, aus „Distillation Loss“ und „Dark Knowledge“. **Klausurbezug:**
Speculative Decoding/Destillation, DistilBERT, BERT Masked LM.

### 26 — Optimierer: Momentum, Adam, Muon

**Vorschlag.** Drei Schritte mit und ohne Momentum von Hand — der Unterschied ist an drei
Zahlen zu sehen.

> Eine Funktion mit Gradienten $g_1 = 1$, $g_2 = 1$, $g_3 = 1$ in drei aufeinanderfolgenden
> Schritten (ein langes, flaches Tal), Lernrate $\rho = 0{,}1$.
> 1. Wie weit ist SGD nach drei Schritten gekommen?
> 2. Wie weit kommt Momentum mit $v_t = \beta v_{t-1} + g_t$, $\beta = 0{,}9$ und
>    demselben $\rho$?
>    *Tipp: $v_1 = 1$, $v_2 = 1{,}9$, $v_3 = 2{,}71$ — Sie müssen nur noch aufsummieren.*
> 3. Jetzt wechselt der Gradient das Vorzeichen: $g = (1, -1, 1)$. Was macht Momentum, und
>    warum ist das in einer engen Schlucht erwünscht?
>    *Antwortprobe: Bei (2) ist der zurückgelegte Weg knapp doppelt so lang wie bei (1).*

**Herkunft.** Neu, aus „Das Grundproblem beim SGD“ und „Idee: Momentum“.
**Klausurbezug:** Sattelpunkt, Lernrate zu groß/zu klein.

### 27 — Adversarial Attacks und Polysemie

**Vorschlag.** Ein FGSM-Schritt, drei Pixel.

> Ein Bildausschnitt $x = (0{,}50,\ 0{,}20,\ 0{,}90)$, der Gradient des Loss nach $x$ sei
> $(0{,}03,\ -0{,}07,\ 0{,}01)$, und $\varepsilon = 0{,}02$.
> 1. Berechnen Sie $x' = x + \varepsilon \cdot \operatorname{sign}(\nabla_x L)$.
> 2. Wie groß ist die größte Änderung eines einzelnen Pixels? Wie groß ist sie in
>    8-Bit-Stufen (also mal 255)?
>    *Tipp: Genau deshalb sieht man die Störung nicht.*
> 3. Warum benutzt FGSM nur das **Vorzeichen** des Gradienten und nicht seinen Betrag?
>    *Antwortprobe: Alle drei Pixel ändern sich um denselben Betrag.*

**Herkunft.** Neu, aus „Wie wird's gemacht?“ — im Kapitel als Vertiefung markiert; die
Übung bleibt beim Rechnen und verlangt die Theorie nicht. **Klausurbezug:**
Berechnungsgraph/DAG (die Ableitung nach der *Eingabe*), Manifold-Hypothese.

---

## Was ich dabei nicht entschieden habe

* ~~Ob alle 27 Kapitel einen Abschnitt bekommen.~~ Entschieden: 04, 17, 21 und 22 bekommen
  keinen. 24 bleibt, obwohl es dort nichts zu rechnen gibt — es ist der Aufgabentyp A2 der
  Klausur und damit die einzige Übung, die das ganze Rezept am Stück verlangt. 19 bleibt,
  weil die Attention-Rechnung konkret ist.
* **Ob die Antwortproben reichen.** Alternative wäre ein Anhang „Ergebnisse“ mit nur den
  Endzahlen (nicht den Rechenwegen) — ein eigener TOC-Eintrag, der die Lösungsdiskussion
  nicht wieder aufmacht.
* **Die Vorspann/Abspann-Frage.** In eipy-skript hat jedes Kapitel einen Abspann mit
  Zusammenfassung und drei Kontrollfragen. Wenn eidl das auch bekommt, gehören
  Kontrollfragen und Übung nebeneinander gedacht — sonst steht dreimal dasselbe am
  Kapitelende.
* **Die Zahlen sind nachgerechnet**, alle 27 Abschnitte, und fünf Stellen sind dabei
  gefallen: Bei 02 bleiben beim Skalieren *zwei* Größen unverändert, nicht eine; bei 03 war
  die Aktivierung nach einem einzigen Schritt schon positiv (Startgewicht geändert, jetzt
  drei Schritte); bei 15 lagen *beide* Werte über 1 (zweites Paar geändert); bei 23 war der
  erste Kandidat mit dem Ergebnis identisch, womit Kosinus und euklidischer Abstand
  dieselbe Antwort gaben — genau das, was die Aufgabe zeigen soll, ging so verloren; bei 26
  ist der Weg knapp das Doppelte, nicht mehr als das Doppelte. Wer einen Abschnitt
  übernimmt, rechnet ihn trotzdem noch einmal nach, so wie CLAUDE.md es für Rechenbeispiele
  verlangt — ich habe mit Papier gerechnet, nicht mit NumPy.

---

## Gestrichen, und warum

Der erste Entwurf war zu lang: 75 Aufgaben auf 27 Kapitel, das liest niemand mit. Weg sind
19 — ein Viertel. Wenn Ihnen eine davon fehlt, steht sie hier mit Begründung, und die
Fassung von vorher steht im git-Log dieses Commits.

**Ganze Abschnitte (4, zusammen 10 Aufgaben):**

| Kapitel | Grund |
|---|---|
| 04 Vortrainierte Modelle | Reine Task-Auswahl ohne Rechnung — und 24 macht dieselbe Übung („welches Modell, welcher Loss, welche Metrik“) besser und näher an der Klausur. |
| 17 RepL und Graphen | „Schreiben Sie zwei mögliche Random Walks auf“ hat keine prüfbare Antwort, und Teil 3 ist Abfragen statt Überlegen. |
| 21 LLMs benutzen | Die Speicherrechnung steht im Kapitel schon vorgerechnet, die Top-k-Aufgabe ist eine Normierung. Beides zu nah am Text. |
| 22 GANs | Ein Lückentext und zwei Abfragen — ein Quiz, keine Übung. Von allen Vorschlägen der schwächste. |

**Einzelne Teilaufgaben (9):**

| Kapitel | Weg | Grund |
|---|---|---|
| 01 | Teil 1 | Einsortieren nach supervised/Regression ist Begriffsabfrage; Precision/Recall trägt den Abschnitt allein. |
| 02 | Teil 1 | „Zeichnen Sie die Gerade“ ist eine Anweisung, keine Aufgabe — die Geometrie steckt ohnehin in Teil 2. |
| 05 | Teil 2 | Rang 0 ist ein Einzeiler und steckt schon in der Shape-Frage. |
| 11 | Teil 3 | Welche Aktivierungsfunktion das Problem nicht hat, steht zwei Absätze weiter oben im Kapitel. |
| 12 | Teil 3 | Warum ein einzelnes Perzeptron XOR nicht schafft, führt das Kapitel selbst vor. |
| 13 | Teil 3 | „Was sagt der Satz nicht“ ist Textverständnis, keine Übung. |
| 14 | Teil 2 | Weight Tying kommt im Kapitel nicht vor — die Aufgabe verlangt Stoff von außerhalb. |
| 18 | Teil 3 | Nach Teil 2 ist die Antwort schon gegeben; die Frage wiederholt sie nur. |
| 23 | Teil 3 | AE gegen VAE wird in Kapitel 15 geübt, hier wäre es das zweite Mal. |

**Das Muster dahinter**, falls Sie weiter kürzen wollen: Weg sind die Teile, die man ohne
Rechnen aus dem Kapiteltext beantworten kann, und die, deren Antwort im Abschnitt selbst
schon steht. Übrig bleiben Aufgaben mit einer Zahl am Ende — die kann man falsch haben, und
genau das soll eine Übung können.
