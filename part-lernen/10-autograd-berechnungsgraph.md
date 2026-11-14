---
title: "Autograd und Berechnungsgraph"
description: "Wie PyTorch Gradienten selbst berechnet: Berechnungsgraph, Freezing, geteilte Gewichte – und ein ganzes Training darauf, mit Generator und DataLoader."
short_title: "Autograd"
---

# Autograd und Berechnungsgraph

Im [Kapitel „Backpropagation“](09-backpropagation.md) haben wir Gradienten von Hand rückwärts durch ein Netz gerechnet. PyTorch tut genau dasselbe – automatisch, für beliebige Architekturen, und mit demselben Muster: Zwischenergebnisse im Vorwärtsdurchlauf speichern, Kettenregel im Rückwärtsdurchlauf. Dieses Kapitel schaut hinter die Kulissen von `loss.backward()`.

## Ein Beispiel im Kleinen

Ein Blick darauf, wie PyTorch Backpropagation *tatsächlich* macht. Wir bauen ein sehr kleines „Netzwerk“:

```python
import torch

x = torch.tensor(3.0)                       # Input (Konstante)
w = torch.tensor(2.0, requires_grad=True)   # Gewicht: "Beobachte mich!"
b = torch.tensor(1.0, requires_grad=True)   # Bias
z = w * x     # z = 6
y = z + b     # y = 7
L = y ** 2    # Loss = 49
```

Der **Berechnungsgraph** (ein DAG, directed acyclic graph) entsteht erst beim Ausführen: Jeder Tensor, der aus einer Operation mit einem `requires_grad`-Tensor entstanden ist, trägt eine `grad_fn`, und man kann den Graphen von hinten nach vorn ablaufen:

```python
print(L.grad_fn)                                    # <PowBackward0>
print(L.grad_fn.next_functions[0][0])               # <AddBackward0>
print(L.grad_fn.next_functions[0][0].next_functions)
# ((<MulBackward0>, 0), (<AccumulateGrad>, 0))  -- z, und das Blatt b
```

Die `grad_fn` weiß, wie man die Operation ableitet, und hält Referenzen auf die *saved tensors*, die gespeicherten Zwischenergebnisse – genau die $z_k$ aus dem [Kapitel „Backpropagation“](09-backpropagation.md). `AccumulateGrad` sind die Blätter des Graphen, die Parameter $w$ und $b$; die topologische Sortierung ist implizit.

`L.backward()` ist der rekursive Aufruf der Kettenregel, initial mit $\frac{dL}{dL} = 1$:

$$
\frac{dL}{dw} = \frac{dL}{dy} \cdot \frac{dy}{dz} \cdot \frac{dz}{dw} = 2y \cdot 1 \cdot x = 14 \cdot 3 = 42,
\qquad
\frac{dL}{db} = 2y \cdot 1 = 14.
$$

```python
L.backward()
print(w.grad, b.grad)   # tensor(42.), tensor(14.)
```

Danach steht das Ergebnis in `w.grad` und `b.grad`. Ein Schritt Gradientenabstieg von Hand, das ist alles, was `optimizer.step()` tut:

```python
lr = 0.01
with torch.no_grad():        # sonst würde der Update selbst Teil des Graphen
    w -= lr * w.grad         # 2.0 - 0.01 * 42 = 1.58
    b -= lr * b.grad         # 1.0 - 0.01 * 14 = 0.86
    w.grad.zero_()           # sonst wird beim nächsten backward() akkumuliert
    b.grad.zero_()
```

Der Optimizer-Schritt muss unter `torch.no_grad()` passieren, damit der Update selbst nicht Teil des Graphen wird, und die Gradienten müssen danach mit `zero_()` zurückgesetzt werden – sonst *akkumuliert* PyTorch sie beim nächsten `backward()`. Das ist der Grund für `optimizer.zero_grad()` in jeder Trainingsschleife.

## Warum rückwärts?

`backward()` läuft den Graphen von der Loss-Funktion zu den Blättern, nicht umgekehrt. Das
ist keine Willkür. Automatisches Differenzieren kann in beide Richtungen laufen, und der
Unterschied liegt darin, was ein Durchlauf liefert:

* **Forward-Mode** schiebt eine Richtung von den Eingängen nach vorn. Ein Durchlauf gibt
  die Ableitung *aller* Ausgaben nach *einer* Eingabe – eine Spalte der Jacobi-Matrix.
* **Reverse-Mode**, also die Backpropagation, zieht eine Richtung vom Ausgang zurück. Ein
  Durchlauf gibt die Ableitung *einer* Ausgabe nach *allen* Eingaben – eine Zeile.

Für $f \colon \mathbb{R}^n \to \mathbb{R}^m$ braucht man demnach $n$ Durchläufe
vorwärts oder $m$ rückwärts, jeder davon in der Größenordnung einer Funktionsauswertung.
Welche Richtung billiger ist, hängt also nur am Verhältnis von $n$ und $m$:

:::{admonition} Faustregel
:class: tip
* $n \gg m$: **Reverse-Mode**. Beim Training ist $n$ die Zahl der Parameter – Millionen –
  und $m = 1$, weil der Loss eine einzelne Zahl ist. Ein Rückwärtsdurchlauf liefert alle
  Gradienten.
* $m \gg n$: **Forward-Mode**. Etwa die Sensitivitätsanalyse einer Kurve
  $\gamma \colon \mathbb{R} \to \mathbb{R}^m$: ein Parameter hinein, viele Werte
  heraus. Ein Vorwärtsdurchlauf liefert alles.
:::

Deep Learning liegt am äußersten Ende des ersten Falls, mit $m = 1$ gegen Millionen von
Parametern. Deshalb heißt das Verfahren hier Backpropagation und nicht Forwardpropagation.

:::{admonition} Vertiefung: Pushforward und Pullback
:class: note dropdown
Differentialgeometrisch sind die beiden Richtungen nicht dasselbe Objekt in zwei
Laufrichtungen, sondern zwei verschiedene Objekte. Der Forward-Mode schiebt
*Tangentialvektoren* nach vorn: Aus einer Richtung $v$ am Eingang wird $df_x(v)$, der
**Pushforward**. Die Backpropagation zieht *Kovektoren* zurück, also 1-Formen: Aus $\omega$
am Ausgang wird $df_x^{*}(\omega)$, der **Pullback**.

Darin steckt der Grund für die Asymmetrie. Am Ausgang steht mit $dL$ bereits eine skalare
1-Form, ein einziges Element des Kotangentialraums – es gibt genau ein Objekt
zurückzuziehen. Vorwärts müsste man statt dessen eine ganze Basis des $n$-dimensionalen
Tangentialraums durchschieben, einen Vektor nach dem anderen.
:::

## Freezing

Setzt man `w.requires_grad = False`, so hat `z = w * x` keine `grad_fn` mehr, der Graph ist an dieser Stelle abgeschnitten:

```python
w.requires_grad = False
z = w * x
print(z.grad_fn)             # None  -- Blatt abgeschnitten
print((z + b).grad_fn)       # <AddBackward0>  -- b wird weiter beobachtet
```

Ein Optimizer verändert $w$ nicht mehr, $b$ aber schon. So friert man beim Transfer Learning Schichten eines vortrainierten Modells ein – und spart dabei Speicher, weil für eingefrorene Parameter keine Gradienten gehalten werden.

## Geteilte Gewichte: Backprop durch eine Faltung

Wie funktioniert Backprop, wenn Gewichte geteilt werden wie bei einem Faltungslayer? Eine (1D-)Faltung schiebt einen kurzen Gewichtsvektor, den *Kernel*, über die Eingabe und bildet an jeder Position dasselbe Skalarprodukt mit dem Ausschnitt darunter; ausführlich im [Kapitel „Faltung und Convolutional Neural Networks“](../part-architekturen-anwendungen/21-faltung-cnn.md). Hier reicht der kleinste Fall: Der Kernel `[0.5]` wird über den Input `[1, 2, 3]` geschoben, $o_i = x_i \cdot k$, und der Loss ist $o_1 + o_2 + o_3$:

```python
x = torch.tensor([1.0, 2.0, 3.0])
k = torch.tensor([0.5], requires_grad=True)
o1, o2, o3 = x[0] * k, x[1] * k, x[2] * k   # von Hand, wie nn.Conv1d
loss = o1 + o2 + o3
loss.backward()
print(k.grad)                # tensor([6.])
```

Der Gradient nach $k$ ist die *Summe* der Beiträge aller Positionen, $\frac{dL}{dk} = x_1 + x_2 + x_3 = 6$: Ein geteilter Parameter bekommt die Gradienten aller seiner Verwendungen aufsummiert – im Graphen führen mehrere Kanten zu demselben Blatt.

:::{prf:example} Backpropagation durch Faltung und ReLU von Hand
Ein Neuron führt eine 1D-Faltung gefolgt von ReLU aus: Eingabesignal $x = [2, 0, -1, 4]$, Kernel $k = [k_0, k_1] = [1, -1]$, Bias $b = 0$, ohne Auffüllen am Rand (der Kernel bleibt ganz im Signal) und mit Schrittweite 1. Die Pre-Aktivierung an Position $i$ ist $z_i = x_i k_0 + x_{i+1} k_1 + b$, die Ausgabe $a_i = \operatorname{ReLU}(z_i)$.

*Forward:* $z = [2 \cdot 1 + 0 \cdot (-1),\ 0 + (-1)(-1),\ -1 + 4 \cdot (-1)] = [2, 1, -5]$, also $a = [2, 1, 0]$.

*Loss:* $L = \tfrac12 \sum_i (a_i - t_i)^2$ mit Target $t = [1, 2, 0]$, also $\frac{\partial L}{\partial a} = a - t = [1, -1, 0]$.

*Backward nach $k_0$:* Die ReLU-Maske ist $[z_i > 0] = [1, 1, 0]$; nur die Positionen $0$ und $1$ leiten den Gradienten weiter. Da $k_0$ an jeder Position mit $x_i$ multipliziert wird, ist $\frac{\partial z_i}{\partial k_0} = x_i$, und die Beiträge summieren sich:

$$
\frac{\partial L}{\partial k_0} = \sum_i (a_i - t_i)\,[z_i > 0]\,x_i = 1 \cdot 1 \cdot 2 + (-1) \cdot 1 \cdot 0 + 0 = 2 .
$$

*Update* mit Lernrate $\rho = 0{,}1$: $k_0 \leftarrow 1 - 0{,}1 \cdot 2 = 0{,}8$. Analog $\frac{\partial L}{\partial k_1} = 1 \cdot 0 + (-1)(-1) + 0 = 1$.
:::

## Autograd bei der Arbeit: Dreiecke gegen Quadrate

Bisher war der Graph winzig und die Daten waren einzelne Zahlen. Dieser Abschnitt setzt
dieselbe Maschinerie einmal ganz ein: ein Netz, das $32 \times 32$-Graustufenbilder in zwei
Klassen sortiert, mit der Trainingsschleife aus dem [Kapitel „Logistische
Regression“](06-logistische-regression.md) und ohne eine einzige von Hand ausgerechnete
Ableitung. Alles, was zwischen `loss` und `w.grad` passiert, ist das, was oben in diesem
Kapitel steht.

Ungewöhnlich sind dabei die Daten: Sie liegen in keinem Ordner. Statt eines Datensatzes
geben wir die **Verteilung** an, aus der er stammt, und ziehen daraus, so oft wir wollen.

### Die Verteilung

Zwei Klassen, Dreiecke und Quadrate. Gezogen werden nicht Pixel, sondern die erzeugenden
Größen:

```python
phi = rng.uniform(0, 2 * np.pi)          # Drehung
flaeche = rng.uniform(60, 220)           # Fläche in Pixeln, für beide Klassen gleich

# Quadrat: damit sind die vier Ecken auf dem Umkreis schon festgelegt.
radius = np.sqrt(flaeche / 2)            # Seite durch Wurzel aus 2
winkel = phi + np.arange(4) * (np.pi / 2) + np.pi / 4

# Dreieck: drei Bögen auf dem Umkreis, die sich zu 360 Grad addieren.
# Der Radius ist hier beliebig, skaliert wird hinterher auf `flaeche`.
boegen = np.deg2rad(56 + (360 - 3 * 56) * rng.dirichlet([1, 1, 1]))
winkel = phi + np.cumsum(boegen)
```

Jedes Dreieck liegt auf seinem Umkreis, ist also durch drei Bögen festgelegt, die sich zu
$360^\circ$ addieren; der Innenwinkel an einer Ecke ist der halbe gegenüberliegende Bogen. Die
Schranke von $56^\circ$ je Bogen hält damit jeden Innenwinkel über $28^\circ$ – ohne sie entstehen
Splitter, die wie ein Strich aussehen und keine erkennbare Klasse mehr haben. Dazu kommen
Strichstärke, Füllung oder nur Umriss, Hintergrundhelligkeit und, in der Hälfte der Fälle,
vertauschte Polarität; die Lage ist gleichverteilt über alle Positionen, in denen die Form
ganz ins Bild passt. Gezeichnet wird über die vorzeichenbehaftete Distanzfunktion des
Polygons, womit Antialiasing und Strichstärke aus derselben Rechnung fallen.

:::{figure} ../images/vl11-formen-beispiele.png
:width: 100%

Je acht Ziehungen aus den beiden Klassen. Bei *gleicher Fläche* wirken die Dreiecke größer –
diese Nebenwirkung wird gleich noch wichtig.
:::

Warum der Aufwand, wo ein paar hundert gezeichnete Bilder schneller gegangen wären? Weil wir
damit drei Dinge bekommen, die ein Ordner voller Bilder nicht hergibt: beliebig viele frische
Beispiele, zu jedem Bild die erzeugenden Größen exakt – und die Möglichkeit, dem Netz
Abkürzungen gezielt zu verbauen.

**Diese letzte Möglichkeit ist der wichtigste Teil.** Ein selbst erzeugter Datensatz enthält
leicht ein Merkmal, das die Klasse verrät, ohne dass die Form dafür gesehen werden müsste.
Hier wäre das die Fläche: Ein Dreieck und ein Quadrat *gleichen Umfangs* unterscheiden sich
in der Fläche deutlich, und „Tinte zählen“ wäre schon die halbe Antwort. Deshalb wird die
Fläche vorgegeben und für beide Klassen gleich gezogen. Ob das reicht, ist eine Messung –
ein lineares Modell auf ein paar handgebauten Merkmalen sagt es:

| Merkmal | Genauigkeit |
|---|---|
| Tintenmenge | $0{,}544$ |
| mittlere Helligkeit | $0{,}494$ |
| Bounding-Box (Höhe, Breite, Fläche) | $0{,}677$ |
| Füllgrad in der Bounding-Box | $0{,}561$ |
| alle vier zusammen | $0{,}707$ |
| lineares Modell auf den 1024 Rohpixeln | $0{,}506$ |

Die Tinte trägt nicht mehr ($0{,}544$ gegen $0{,}5$ beim Raten), die grobe Formstatistik
aber durchaus: Die Bounding-Box eines Dreiecks ist bei gleicher Fläche größer, und das sieht
man der Abbildung oben an. $0{,}707$ ist damit die Höhe, über die ein Netz erst einmal
kommen muss, bevor man sagen darf, es habe etwas über *Formen* gelernt. Dass ein lineares
Modell auf den Rohpixeln bei $0{,}506$ bleibt, liegt an der zufälligen Lage: Ein einzelnes
Pixel sagt nichts, wenn die Form überall sein kann.

### Ein Generator als Datenquelle

Eine Verteilung hat kein Ende. Es gibt also keine Liste, kein `len`, keinen letzten Index –
und damit ist ein **Generator** das Naheliegende, eine Funktion, die mit `yield` Werte
herausgibt und zwischen zwei Werten stehen bleibt:

```python
def formen_strom(cfg, seed, chunk=256):
    """Unendlich viele Beispiele, eines nach dem anderen."""
    rng = np.random.default_rng(seed)
    while True:
        x, y = zieh_bilder(cfg, rng, chunk)   # (chunk, 32, 32) und (chunk,)
        yield from zip(x, y)
```

Gezogen wird in Blöcken, weil NumPy Vektoren mag, herausgegeben wird einzeln: `yield from`
gibt die Werte eines anderen iterierbaren Objekts einen nach dem anderen weiter. Der
Zustand – `rng` und die Position im Block – lebt zwischen zwei Aufrufen in der Funktion
selbst; genau das macht einen Generator aus. Speicher kostet das nichts, auch nicht nach
einer Million Bildern.

Generatoren sind in Python die einfachste Form der **Koroutine**: einer Funktion, die
angehalten und später an derselben Stelle fortgesetzt wird, statt von vorn bis hinten
durchzulaufen. Wer schon `async def` gesehen hat, hat dieselbe Idee in ihrer großen
Ausführung gesehen; hier genügt die kleine.

### `IterableDataset` und `DataLoader`

PyTorch kennt zwei Sorten von Datensätzen. Ein `Dataset` hat eine Länge und wird über
Indizes gelesen (`__len__` und `__getitem__`) – das ist der übliche Fall mit einem Ordner
voller Dateien. Ein `IterableDataset` hat beides nicht und liefert statt dessen einen
Iterator; für einen Strom ohne Ende ist das die passende Sorte:

```python
from torch.utils.data import DataLoader, IterableDataset, get_worker_info

class Formen(IterableDataset):
    def __init__(self, cfg, seed=0):
        self.cfg, self.seed = cfg, seed

    def __iter__(self):
        info = get_worker_info()                     # None, wenn ohne Worker geladen wird
        wid = 0 if info is None else info.id
        for x, y in formen_strom(self.cfg, self.seed + 9973 * wid):
            yield torch.from_numpy(x), int(y)

loader = DataLoader(Formen(cfg), batch_size=128, num_workers=4)
```

Der `DataLoader` stapelt die einzelnen Beispiele zu Batches der Form `(128, 32, 32)` und
lässt sie, mit `num_workers=4`, in vier Hintergrundprozessen vorbereiten, während das Netz
noch am vorigen Batch rechnet. Das ist hier kein Luxus: Ein Bild zu ziehen und zu rendern
kostet mehr Zeit als der Gradientenschritt, der es verarbeitet.

:::{admonition} Die Falle mit den Workern
:class: warning
Die drei Zeilen mit `get_worker_info()` sehen nach Buchhaltung aus, sind aber der Kern.
`num_workers=4` startet vier **Prozesse**, und jeder bekommt eine Kopie des Datensatzes –
mitsamt `self.seed`. Ohne die Unterscheidung zieht jeder Prozess dieselbe Folge: Das Netz
sieht jedes Bild viermal, die effektive Datenmenge ist ein Viertel der erwarteten.

Auffallen tut das nicht. Es gibt keinen Fehler, keine Warnung, und der Loss sinkt ganz
normal weiter – nur eben auf weniger Daten, als auf dem Papier stehen. Die Übung am
Kapitelende rechnet den Fall einmal durch; vermeiden lässt er sich nur, indem man bei jedem
`IterableDataset` als Erstes fragt, was passiert, wenn es **mehrfach** läuft.
:::

### Die Trainingsschleife

Und nun das Netz. Es ist ein MLP: Das Bild wird zu einem Vektor der Länge $1024$
ausgerollt, dann zwei versteckte Schichten mit $256$ und $128$ Neuronen, dann zwei Ausgaben
für die zwei Klassen. (`nn.Sequential` reiht Schichten hintereinander, `nn.ReLU` ist die
Aktivierungsfunktion dazwischen – beides im [Kapitel
„Aktivierungsfunktionen“](11-aktivierungsfunktionen.md); hier genügt, dass ohne eine solche
Funktion zwischen den Schichten das ganze Netz wieder nur eine lineare Abbildung wäre.)

```python
modell = nn.Sequential(nn.Flatten(),
                       nn.Linear(32 * 32, 256), nn.ReLU(),
                       nn.Linear(256, 128), nn.ReLU(),
                       nn.Linear(128, 2))
opt = torch.optim.Adam(modell.parameters(), lr=1e-3)
verlust = nn.CrossEntropyLoss()

for schritt, (xb, yb) in enumerate(loader, start=1):
    opt.zero_grad()                        # Gradienten von letztem Mal weg
    verlust(modell(xb), yb).backward()     # Graph bauen und rückwärts gehen
    opt.step()                             # ein Schritt Gradientenabstieg
    if schritt == 3000:
        break
```

Das sind dieselben Zeilen wie im Kapitel „Logistische Regression“, mit einem Unterschied:
Die Schleife läuft nicht über Epochen, sondern über Schritte, und sie hört auf, weil wir
sie anhalten. Über einen unendlichen Strom kann man nicht „einmal durchgehen“. Wer schon
einmal eine Trainingsschleife gesehen hat, vermisst hier auch das Mischen der Daten: Bei
frisch gezogenen Beispielen gibt es nichts zu mischen, die Reihenfolge ist von sich aus
zufällig.

Nach diesen $3000$ Schritten – $384\,000$ gesehene Bilder, jedes genau einmal – liegt das
Netz auf $10\,000$ frischen Bildern bei einer Genauigkeit von $0{,}922$ (Median aus fünf
Läufen). Gemessen an den $0{,}707$ von oben hat es also tatsächlich etwas über Formen
gelernt und nicht bloß Tinte gezählt. Keine Ableitung wurde dafür hingeschrieben:
`backward()` liefert in jedem Schritt die Gradienten für alle $295\,554$ Parameter, und an
jedem Knoten des Graphen steht dabei genau die Rechnung, die im [Kapitel
„Backpropagation“](09-backpropagation.md) von Hand gemacht wurde.

:::{admonition} Warum hier `Adam` steht und nicht `SGD`
:class: note
`torch.optim.Adam` ist eine Verfeinerung des Gradientenabstiegs, die jedem Parameter eine
eigene, mitlaufend angepasste Schrittweite gibt; das [Kapitel
„Optimierer“](../part-architekturen-anwendungen/26-optimierer.md) rechnet sie aus. Der
Unterschied ist an dieser Aufgabe nicht kosmetisch: Mit demselben Budget, demselben Netz und
demselben Strom kommt einfaches `SGD` auf $0{,}606$ (Lernrate $0{,}01$) oder auf $0{,}763$
(Lernrate $0{,}1$, und das mit Werten zwischen $0{,}688$ und $0{,}807$ über drei Läufe),
gegen $0{,}922$ mit `Adam`.
:::

Die Verteilung bleibt uns erhalten: Im [Kapitel „Universelle
Approximation“](13-universelle-approximation.md) wird sie benutzt, um eine Frage zu
beantworten, die nur mit beliebig vielen Daten überhaupt zu stellen ist – ob ein Netz
lieber mehr verschiedene Bilder sehen oder länger auf denselben üben sollte.

## Übung

1. Ein Modell hat drei Layer. Vor dem Training wird für Layer 1 und 2
   `requires_grad = False` gesetzt. Welche Tensoren bekommen im Backward Pass einen
   `.grad`, welche nicht – und wo wird trotzdem noch gerechnet?
   *Tipp: Zeichnen Sie den Graphen und verfolgen Sie die Pfeile rückwärts, von der
   Loss-Funktion zu den Blättern. Fragen Sie sich bei jedem Layer: Muss der Gradient hier
   überhaupt noch hindurch, damit weiter vorne etwas ankommt?*
2. Ein Gewicht $k$ wird an drei Stellen im Graphen benutzt (geteilte Gewichte, wie bei
   einer Faltung). Wie viele Beiträge hat $\frac{\partial L}{\partial k}$, und wie werden
   sie verrechnet?
3. Im `Formen`-Datensatz oben wird die Zeile mit `get_worker_info()` vergessen, der
   `DataLoader` läuft mit `num_workers=4` und das Training über $3000$ Schritte zu je
   $128$ Beispielen. Wie viele *verschiedene* Bilder sieht das Netz dann – und woran
   würden Sie es im Training merken?
   *Tipp: Jeder Worker-Prozess bekommt eine Kopie des Datensatzes, also auch von
   `self.seed`, und der `DataLoader` nimmt die Batches reihum von den Workern entgegen.*

*Antwortprobe: Bei (1) spart das Einfrieren Speicher, aber nicht jede Rechnung; bei (3)
ist die Genauigkeit auf frischen Bildern das Einzige, was den Unterschied überhaupt
zeigt.*
