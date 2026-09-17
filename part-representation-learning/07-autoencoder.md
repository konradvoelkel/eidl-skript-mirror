---
title: "VL 07: Handgemachte Netze und Autoencoder"
short_title: "VL 07"
---

# Handgemachte Netze und Autoencoder

:::{note} Stand
Erste Prosafassung (aus den Folien von VL 07, WiSe 2025/26). Abbildungen fehlen noch, siehe die `TODO`-Kommentare.
:::

## Das Geheimnis um Deep Learning lüften

Warum – und wie genau – funktioniert Deep Learning so gut? Die Zutaten, die wir bisher haben:

* Das einzelne Neuron = Skalarprodukt + Aktivierungsfunktion.
* Gradientenabstieg: Lernen in Richtung der Ableitung einer Loss-Funktion.
* Backpropagation: clever die Ableitung berechnen für tiefe Netze.

Was noch fehlt, und was wir in diesem und den nächsten Kapiteln angehen:

* Sinnvolle Loss-Funktionen festlegen: Regression mit MSE, (binäre) Klassifikation mit (B)CE; BCE vs. NLL vs. $D_{KL}$. *(heute)*
* Architekturen neben einfachen MLPs, wie z.B. Autoencoder – und damit auch Representation Learning und Transfer Learning. *(heute)*
* Regularisierung und Tricks gegen verschwindende Gradienten. *(heute)*
* Hyperparameter wählen und optimieren; alles hängt von den Daten ab …
* Und ganz grundsätzlich: Elementare Funktionen sind leicht approximierbar. *(jetzt kurz)*

## Parameter von Hand wählen

Bevor wir Netze trainieren, überzeugen wir uns davon, dass die gesuchten Gewichte überhaupt *existieren*: Wir bauen kleine Netze von Hand. Das Notebook dazu ist `nn-by-hand.ipynb`.

### Easy mode: Boolesche Variablen

Seien $x, y \in \{0, 1\} = \{\text{FALSE}, \text{TRUE}\}$ und $f \colon \mathbb{R}^2 \to \mathbb{R}$, $f(x, y) := x \text{ OR } y$, also $f(0,0) = 0$, $f(1,0) = 1$, $f(0,1) = 1$, $f(1,1) = 1$. Welches neuronale Netz berechnet als Inferenz die Funktion $f$?

Idee: Schreibe $f$ als Verkettung von gewichteten Summen (= Skalarprodukten) und Aktivierungsfunktionen (z.B. $[x > 0]$ oder $\operatorname{ReLU}(x) := \max(0, x)$). Dabei müssen wir OR *interpolieren* – entscheiden, was z.B. $f(0{,}5, 0)$ sein soll – und *extrapolieren* – entscheiden, was z.B. $f(-1, 2)$ sein soll. Denn ein neuronales Netz ist auf ganz $\mathbb{R}^2$ definiert, nicht nur auf den vier Ecken.

### Easiest mode: eindimensional

Sei $x \in \mathbb{R}$ mit der Interpretation $(x \le 0) = \text{FALSE}$, $(x \ge 1) = \text{TRUE}$, und $n \colon \mathbb{R} \to \mathbb{R}$, $n(x) := \text{NOT } x$. Also $n(0) = 1$, $n(1) = 0$, allgemeiner $n(x) \le 0$ falls $x \ge 1$. Die Funktion

$$
n(x) = 1 - x
$$

erfüllt die Eigenschaft, NOT zu inter- und extrapolieren. Als neuronales Netz: 1 Neuron, Gewicht $w = -1$, Bias $b = +1$, Aktivierungsfunktion $\operatorname{id}$.

### Zurück zu OR

Ansatz: $f(x, y) = x + y$. Leider ist $f(1, 1) = 2 \neq 1$. Besser: $f(x, y) = [x + y > 0]$ – ein Neuron mit Gewichtsvektor $(1, 1)$, Bias $b = 0$ und Aktivierungsfunktion $[\,\cdot > 0]$ mit Werten in $\{0, 1\}$. Dafür ändern wir die Interpretation leicht zu $(x \le 0) = \text{F}$, $(x > 0) = \text{T}$. Softere Varianten sind $f(x, y) := x + y$ oder $\sigma(x + y)$; und noch besser, weil es Negatives sauber abschneidet:

$$
f(x, y) := \operatorname{ReLU}(x) + \operatorname{ReLU}(y).
$$

<!-- TODO Abbildung: Heatmap von ReLU(x)+ReLU(y) auf [-1,2]^2 mit den vier Booleschen Ecken markiert (Folie 13) -->

### Komplizierteres aus Einfachem: NOR

Sei $g(x, y) := x \text{ NOR } y$, also $g(\text{F}, \text{F}) = \text{T}$ und sonst $\text{F}$. NOR = NOT OR, also $g(x, y) = n(f(x, y))$ für ein $f$, welches OR implementiert. Mit $f(x, y) := \operatorname{ReLU}(x) + \operatorname{ReLU}(y)$ und $n(x) := 1 - x$:

$$
g(x, y) := 1 - \bigl(\operatorname{ReLU}(x) + \operatorname{ReLU}(y)\bigr).
$$

Als Netz: erste Schicht mit Gewichten $(1, 1)$, Bias $0$ und ReLU (zwei Neuronen, eines pro Eingabe – oder eines mit Gewichtsvektor $(1,1)$, wenn man die ReLU vor die Summe zieht), zweite Schicht mit Gewicht $-1$, Bias $1$ und $\operatorname{id}$.

### Weiter so? XOR

Sei $f(x, y) := x \text{ XOR } y$. Die „Region“ XOR in der Ebene, also die Punkte $(x, y)$ mit $\text{XOR}(x, y) > 0$, ist der Schnitt von $\text{NAND}(x, y) > 0$ mit $\text{OR}(x, y) > 0$:

$$
\text{XOR}(x, y) = \text{AND}\bigl(\text{NAND}(x, y),\ \text{OR}(x, y)\bigr).
$$

Setzt man das mit den obigen Bausteinen zusammen, so müsste es mit 4 Hidden Layers zu je 4 Neuronen klappen. Gradientenabstieg mit Backpropagation findet allerdings auch Approximationen mit 3 Hidden Layers – und mit 2 Hidden Layers (siehe die Bilder `krude-xor-approximation.png` aus dem TensorFlow Playground).

<!-- TODO Abbildungen: XOR-Region; Playground-Lösungen mit 3 bzw. 2 Hidden Layers (from_2025/slides/krude-xor-approximation*.png) -->

### Take-Home Message

Boolesche Funktionen lassen sich mit neuronalen Netzen darstellen bzw. approximieren, d.h. es gibt Gewichte, sodass die resultierende Funktion tut, was sie soll. Also kann auch Optimierung diese idealen Gewichte finden. Aus elementaren Funktionen lassen sich komplexe verknüpfen; neuronale Netze können aber auch „Abkürzungen“ nehmen und Platz verschwenden (überflüssige Neuronen).

### Arithmetik

Wie können wir z.B. $f(x, y) := x^3 + x y^2 - 3y$ mit einem neuronalen Netz berechnen oder approximieren? Einfachere Probleme, die wir dafür zuerst lösen müssen: $f(x, y) := xy$ und $f(x) := x^2$.

**Auf $[-3, +3]$ approximieren wir $x^2$** mit einer stückweise linearen Funktion an ganzzahligen Stützstellen. Die Interpolation durch die Punkte $(k, k^2)$ für $k = -3, \dots, 3$ hat auf $[k, k+1]$ die Steigung $2k + 1$, also an jeder inneren Stützstelle einen Knick, bei dem die Steigung um $2$ wächst – und jeder Knick ist eine ReLU:

$$
Q(x) = 9 - 5\,\operatorname{ReLU}(x + 3) + \sum_{k=-2}^{2} 2\,\operatorname{ReLU}(x - k).
$$

Probe: $Q(0) = 9 - 15 + 2(2 + 1) = 0$ und $Q(3) = 9 - 30 + 2(5 + 4 + 3 + 2 + 1) = 9$. Das ist ein Netz mit einer versteckten Schicht aus 6 ReLU-Neuronen (Gewicht $1$, Bias $-k$ für $k = -3, \dots, 2$) und einer linearen Ausgabeschicht mit Gewichten $(-5, 2, 2, 2, 2, 2)$ und Bias $9$. Die Symmetrie $x^2 = (-x)^2$ haben wir dabei ignoriert – geht das besser? Mit $|x|$ als erster Schicht halbiert sich die Anzahl der Knicke.

<!-- TODO Abbildung: x² und stückweise lineare Interpolation an ganzzahligen Stützstellen (Folien 28–30) -->

**Wenn $x^2$ gut approximiert werden kann, dann auch $xy$** über die Polarisationsidentität:

$$
\frac{(x + y)^2 - (x - y)^2}{4} = \frac{x^2 + 2xy + y^2 - x^2 + 2xy - y^2}{4} = xy .
$$

Damit setzen wir für eine Approximation $Q$ der Quadratfunktion

$$
\operatorname{MUL}(x, y) := \tfrac14 Q(x + y) - \tfrac14 Q(x - y),
$$

und $x + y$ sowie $x - y$ sind lineare Schichten. Mit MUL und Addition bekommen wir alle Polynome, und damit (Weierstraß) alle stetigen Funktionen auf beschränkten Bereichen.

### Take-Home Message

Funktionen lassen sich mit neuronalen Netzen darstellen bzw. approximieren. Mit einer Lookup-Table (LUT) und Interpolation sind beliebig gute Näherungen auf *beschränkten* Definitionsbereichen möglich – so rechnet auch die GPU z.B. den Sinus aus. Außerhalb der Stützstellen wird die Approximation beliebig schlecht: **Neuronale Netze interpolieren gut, extrapolieren schlecht.**

## Autoencoder

### Das Autoencoder-Layout

Wie letztes Mal bereits: Ein Autoencoder ist eine Regression mit Input $x$, einem Vektor der Länge $D$. Der **Encoder** reduziert in mehreren Schichten von Dimension $D$ auf Dimension $L$, der **Decoder** erhöht in mehreren Schichten von Dimension $L$ zurück auf Dimension $D$. Input und Output liegen im „Datenraum“ (bei Bildern: „Pixelraum“, pixel space); die Flaschenhals-Schicht der Dimension $L$ ist der **latente Raum** (latent space).

<!-- TODO Abbildung: Autoencoder-Layout, mit NN-SVG erstellt (Folie 37) -->

### Anwendungsbeispiel: MNIST

MNIST besteht aus $28 \times 28$ Graustufen-Bildern handgeschriebener Ziffern 0–9, mit Label; 60 000 Trainings- und 10 000 Testbilder. Mögliche Tasks:

* Unsupervised: Kompression der Bilder. Autoencoder = Encoder + Decoder, der Encoder ist der Kompressor.
* Unsupervised: neue Bilder generieren. Die Verteilung der Punkte im latenten Raum modellieren, sampeln, dekodieren – dazu mehr im nächsten Kapitel (VAE).
* Supervised: Klassifikation.
* Supervised: neue Bilder mit vorgegebener Ziffer generieren.

Heute: Kompression und Klassifikation, mit den Zielen *Accuracy erhöhen* und *Overfitten vermeiden*. Variationsmöglichkeiten dafür gibt es an drei Stellen: die Daten modifizieren (putzen?), die Modellarchitektur (tiefer?), und die Trainings-Hyperparameter (wie genau wird gelernt?).

### Code-Beispiel: Modell-Architektur

Ein Autoencoder in PyTorch ist ein `nn.Module` mit zwei `nn.Sequential`-Blöcken. Schematisch:

```python
class Autoencoder(nn.Module):
    def __init__(self, latent_dim=12):
        super().__init__()
        self.encoder = nn.Sequential(
            nn.Linear(IMAGESIZE**2, 256), nn.ReLU(True),
            nn.Linear(256, 64), nn.ReLU(True),
            nn.Linear(64, latent_dim),
        )
        self.decoder = nn.Sequential(
            nn.Linear(latent_dim, 64), nn.ReLU(True),
            nn.Linear(64, 256), nn.ReLU(True),
            nn.Linear(256, IMAGESIZE**2), nn.Sigmoid(),
        )

    def forward(self, x):
        latent = self.encoder(x)
        return latent, self.decoder(latent)
```

Das Sigmoid am Ende des Decoders sorgt dafür, dass die Ausgabe wie Pixelwerte in $[0, 1]$ liegt. Die Architektur lässt sich mit [Netron](https://netron.app) visualisieren, nachdem man das Modell mit `torch.save(model, 'model.pth')` gespeichert hat.

### Code-Beispiel: Training

```python
IMAGESIZE = 28
transform_mnist = transforms.Compose([
    transforms.ToTensor(),
    transforms.Lambda(lambda x: x.view(-1)),   # 28x28 -> 784
])
mnist_data = datasets.MNIST(root='./data', train=True, download=True,
                            transform=transform_mnist)
data_loader = DataLoader(dataset=mnist_data, batch_size=512,
                         num_workers=8, shuffle=True)

model = Autoencoder(latent_dim=12).to(device)
reconstruction_criterion = nn.MSELoss()
optimizer = optim.SGD(model.parameters(), lr=1e-2)

for epoch in range(15):
    for img, labels in data_loader:
        img = img.to(device)
        latent, reconstructed = model(img)
        reconstruction_loss = reconstruction_criterion(reconstructed, img)
        loss = reconstruction_loss
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
```

Neu gegenüber Kapitel 4 sind `Dataset` und `DataLoader`: Der Datensatz liefert einzelne Samples (hier mit einer `transform`, die das Bild in einen Vektor der Länge 784 verwandelt), der Loader fasst sie zu zufällig gemischten Mini-Batches zusammen. Die Trainingsschleife selbst ist dieselbe wie immer, nur dass das Label das Bild selbst ist.

### Tricks beim Training

* **Mehr Epochen trainieren!**
* **Lernrate anpassen** – statt `lr=1e-3` mal mit `lr=1e-2` probieren.
* Die Gewichte können zu groß werden, dann kann man eine **L2-Regularisierung** nutzen, den *Weight Decay* (als Parameter für den Optimierer, wie die Lernrate): `weight_decay=1e-5`. Das addiert $\lambda \|W\|^2$ zum Loss und zieht die Gewichte bei jedem Schritt ein wenig Richtung null.
* SGD kann sehr langsam sein. Es gibt eine ganze Reihe von Tricks wie z.B. eine adaptive Lernrate und cleveres Mitteln über mehrere Batches hinweg, die in **Adam** implementiert sind: `optim.Adam(model.parameters(), lr=1e-3)`. Dazu mehr in VL 15.
* Oft ist I/O oder die CPU ein Bottleneck beim Laden der Daten. Im Konstruktor des `DataLoader` mit anderen `batch_size`s experimentieren (im Zweifel mehr, bis Out of Memory), und mehrere CPU-Kerne zum Laden der Daten nutzen: `num_workers=8`.

## Label Autoencoder

### Supervised: Klassifikator

Ein „klassischer“ Klassifikator-Ansatz auf Basis des Autoencoders: Encoder vom Autoencoder, dann ein linearer Layer auf 10 Dimensionen, dann Softmax. Zur „harten“ Klassifikation noch ein $\operatorname{argmax}$ dahinter hängen.

Loss-Funktion: **Negative Log-Likelihood** = Kreuzentropie $\mathrel{\hat=}$ Kullback-Leibler-Divergenz zwischen echten Labels und Vorhersage (Blatt 5). Das ist der *classification loss*, im Gegensatz zum *reconstruction loss*. In PyTorch: `nn.CrossEntropyLoss()`, das Softmax und NLL in einem Schritt (numerisch stabiler) berechnet und direkt auf die Logits angewendet wird.

### Label Autoencoder

Warum nicht beides? Encoder vom Autoencoder, darauf ein linearer Layer auf 10 Dimensionen mit Softmax – und *daneben* der Decoder vom Autoencoder. Input ist ein Bild, Output sind Rekonstruktion und Label-Vorhersage, und die Loss-Funktion ist

$$
L = \text{reconstruction\_loss} + \text{classification\_loss}.
$$

Der Encoder muss jetzt einen latenten Raum finden, der *beides* kann: das Bild rekonstruieren und die Ziffer erkennen. Die Rekonstruktion wirkt dabei wie eine Regularisierung des Klassifikators – der latente Raum darf nichts Wichtiges wegwerfen.

<!-- TODO Abbildung: Label-Autoencoder-Architektur (Folie 54) -->

### Tricks bei der Modellarchitektur

* **Mehr Layer!**
* Dem Problem sterbender Neuronen entgegenwirken mit anderen Aktivierungsfunktionen als ReLU, z.B. dem **Swish** (in PyTorch `nn.SiLU`).
* **Dropout-Layer**: Zufällig ein paar Einträge des eingehenden Vektors auf $0$ setzen (`nn.Dropout(0.3)` setzt 30 % auf null, nur während des Trainings). Verhindert zu starke Konzentration auf einige wenige Neuronen und wirkt gegen Overfitting.
* **Batch-Normalization-Layer** (`nn.BatchNorm1d`): Nach jedem Batch den Output des vorigen Layers auf eine Normalverteilung normieren, d.h. Mittelwert abziehen und durch die Standardabweichung teilen, beides über den Batch berechnet. Die Transformation (Skalierung und Translation) auf eine andere Normalverteilung als die Standardnormalverteilung sind erlernbare Gewichte dieses Layers. Theoretisch etwas kompliziert (wieso es nützt), praktisch sehr nützlich.
