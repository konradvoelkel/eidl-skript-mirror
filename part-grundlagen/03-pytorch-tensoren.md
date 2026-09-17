---
title: "VL 03: PyTorch Basics und Tensoren"
short_title: "VL 03"
---

# PyTorch Basics und Tensoren

:::{note} Stand
Erste Prosafassung (aus den Folien von VL 03, WiSe 2025/26). Abbildungen fehlen noch, siehe die `TODO`-Kommentare.
:::

## Vortrainierte Modelle verwenden: Orientierung

Wenn wir für eine Aufgabe ein vortrainiertes Modell verwenden wollen, müssen wir wissen, welches Modell geeignet sein kann. Auf [huggingface.co/tasks](https://huggingface.co/tasks) sind die Modelle nach *Tasks* sortiert. Wir gehen exemplarisch einige davon durch – nicht, um die Modelle zu verstehen, sondern um das Vokabular zu lernen und ein Gefühl dafür zu bekommen, was heute „von der Stange“ geht.

### Tasks in Computer Vision

* **Depth Estimation**: Von einem Bild für jeden Pixel bei $(x, y)$ auch eine $z$-Koordinate schätzen. Beispiel: Intels *Dense Prediction Transformer* (DPT) von 2022, ein Vision Transformer.
* **Image Classification**: Von einem Bild sagen, was es ist. Beispiel: Microsofts *ResNet* (CNN, 2016), trainiert auf ImageNet – gibt zu einem Foto „Igel“ zurück.
* **Object Detection**: Von einem Bild sagen, was drauf ist, mit Bounding Boxes. Beispiel: *YOLOS* (NeurIPS 2021), trainiert auf ImageNet und COCO – findet in Bild #7781 des COCO-Datensatzes „Cat, Banana, Chair“.
* **Image Segmentation**: Auf einem Bild für jedes erkannte Objekt die Umrisse finden, das Bild also aufteilen. Beispiel: Nvidias *Segformer* (2021), trainiert auf ImageNet, COCO und ADE20k.
* **Image-to-Image**: Ein Bild als Input, ein Bild als Output, z.B. historische Fotos einfärben. Beispiel: Renato Sortinos *ColorizeNet*, ein Finetune von ControlNet / Stable Diffusion 2.1 auf bearbeitetem COCO.
* **Unconditional Image Generation**: Nur ein Bild als Output, z.B. ein Katzenbild (je nach Datenbasis). Beispiel: Googles *DDPM* (2020), Denoising Diffusion Probabilistic Models.
* **Zero-Shot Image Classification**: Von einem Bild sagen, was es ist – ohne dass für die Klassen gelabelte Daten vorlagen. Beispiel: OpenAIs *CLIP-ViT* (2021), Contrastive Language-Image Pretrained Vision Transformer, dem man die Kandidaten als Text gibt („a photo of a car“).

Zur Einordnung des Vokabulars: **Zero-Shot** heißt ohne gelabelte Daten für die neue Aufgabe, **One-Shot** (oder Single-Shot) mit einem gelabelten Sample, **Few-Shot** mit einigen wenigen gelabelten Samples.

### Tasks in NLP

Wir betrachten nur einen Teil der NLP-Tasks:

* **Text Classification**: Texten ein Genre, eine Stimmung (Sentiment) o.ä. zuordnen. Beispiel: *DistilBERT* (2019), self-supervised trainiert mit BERT (Bidirectional Encoder Representations from Transformers) als Lehrer – zur Destillation kommen wir in VL 14.
* **Token Classification**: Named Entity Recognition (NER) oder Part-of-Speech (PoS) Tagging, also jedem Wort ein Label geben. Beispiel: *flair ner-german* (2020) von der HU Berlin.
* **Summarization**: Zu einem Text (Satz oder Dokument) eine kurze Zusammenfassung schreiben. Beispiel: Facebooks *BART* (2019), Bidirectional and Auto-Regressive Transformers.
* **Fill-Mask**: Einen Lückentext füllen. Beispiel: wieder *DistilBERT* – das ist nämlich genau die Aufgabe, mit der BERT-artige Modelle vortrainiert werden.

## Vortrainierte Modelle verwenden: Praktisch

### Beispiel: Übersetzen mit WMT19

Wir übersetzen von Englisch nach Deutsch mit Facebooks WMT19-Modell, nach der Anleitung von Hugging Face:

```python
from transformers import FSMTForConditionalGeneration, FSMTTokenizer

mname = "facebook/wmt19-en-de"
tokenizer = FSMTTokenizer.from_pretrained(mname)
model = FSMTForConditionalGeneration.from_pretrained(mname)

input = "I am not sure if deep learning is really for me."
input_ids = tokenizer.encode(input, return_tensors="pt")
outputs = model.generate(input_ids)
decoded = tokenizer.decode(outputs[0], skip_special_tokens=True)
print(decoded)
# Ich bin mir nicht sicher, ob Deep Learning wirklich etwas für mich ist.
```

Das Muster ist typisch für alle Modelle auf dem Hub: Ein **Tokenizer** verwandelt Text in Zahlen (`input_ids`, als PyTorch-Tensor, daher `return_tensors="pt"`), das **Modell** verwandelt Zahlen in Zahlen, und der Tokenizer verwandelt das Ergebnis zurück in Text. `from_pretrained` lädt die Gewichte beim ersten Aufruf aus dem Hub herunter und cached sie lokal.

### Auf der GPU rechnen

Um auf der GPU mit CUDA zu rechnen, müssen Modell *und* Eingabedaten dorthin verschoben werden:

```python
model = FSMTForConditionalGeneration.from_pretrained(mname).to("cuda")
input_ids = tokenizer.encode(input, return_tensors="pt").to("cuda")
```

Der übliche Workflow, damit der Code auch ohne GPU läuft:

```python
import torch

device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
model.to(device)
```

Alternativ kann die `accelerate`-Library von HF auch dynamisch Teile des Modells auf die GPU legen und andere Teile im Hauptspeicher belassen, um sehr große Modelle zu nutzen.

### Was zuvor geschah: Installation

`pip install 'transformers[torch]'` in der Shell (oder `!pip install ...` in einem Notebook) installiert `transformers` und PyTorch. Das allein installiert noch kein CUDA, d.h. alle Rechnungen finden auf der CPU mit dem Hauptspeicher statt – das ist intern „device 0“ vom Typ `cpu`.

Für CUDA (Ubuntu Linux auf NVIDIA-Hardware) prüft man zuerst, was da ist:

```bash
lspci | grep -i nvidia
nvidia-smi
```

`nvidia-smi` zeigt die Treiberversion und die maximale CUDA-Version, die die GPU bzw. der Treiber unterstützt (z.B. 11.4); `nvcc --version` zeigt die installierte CUDA-Toolkit-Version (z.B. 10.1). Die installierte Version darf kleiner sein als die maximale – das passt dann. Anschließend PyTorch mit passendem CUDA-Build installieren:

```bash
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu129
```

Hat es geklappt? Python-Interpreter auf und `torch.cuda.is_available()` sollte `True` liefern. Auf AMD-GPUs heißt das Ganze ROCm statt CUDA, aber der Python-Befehl ist derselbe; auf macOS 12.3+ gibt es Beschleunigung über MPS (`torch.backends.mps.is_available()`).

Und noch davor: eine virtuelle Umgebung im Arbeitsordner anlegen, damit die Installation nicht das System-Python verändert:

```bash
python -m venv .env
source .env/bin/activate
```

und erst *danach* mit `pip` fleißig installieren. Oder entspannt `uv` benutzen, das Umgebung und Pakete in einem Schritt verwaltet.

### Alternative: Google Colab

Wer nicht lokal installieren will oder keine GPU hat: [Google Colab](https://colab.research.google.com/notebooks/intro.ipynb) bietet Jupyter-Notebooks mit (begrenzter) GPU-Zeit im Browser. Ein neues Notebook gibt es unter [colab.research.google.com/#create=true](http://colab.research.google.com/#create=true); die Hugging-Face-Dokumentation ist als Colab-Notebooks verfügbar, z.B. die [Task Summary](https://colab.research.google.com/github/huggingface/notebooks/blob/main/transformers_doc/en/task_summary.ipynb).

## PyTorch Basics: Tensoren

### Tensoren ≈ Arrays

Vier Fragen: Was ist ein Array? Was ist ein Tensor? Was ist ein Array in NumPy? Was ist ein Tensor in Torch?

* Ein **Array** ist eine Sammlung von Daten von gleichem Typ, die fortlaufend im Speicher liegen (können).
* Ein **Tensor** ist, je nachdem, wen man fragt:
  * Physiker: ein Objekt, das sich tensoriell transformiert.
  * Mathematiker: ein Element in einem Tensorproduktraum.
  * Informatiker: ein fancy Wort für Arrays.
* Ein **Tensor in Torch** ist eine Sammlung von Daten von gleichem Typ (dem `dtype`), die fortlaufend im Speicher liegen – und zwar potentiell im GPU-Speicher – optimiert für Gradientenabstiegsmethoden (Attribut `grad`, dazu mehr in VL 05/06).

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

## Lineare Regression zur Klassifikation

Wenn wir an Regression denken, dann oft an eine Regressionsgerade in einem $x$-$y$-Plot, bei dem auf der $x$-Achse die unabhängige Variable (der *Regressor*) und auf der $y$-Achse die abhängige Variable (der *Regressand*) aufgetragen ist. Bei der Klassifikation ist der Regressand die Klasse, $y \in \{0, 1\}$.

Schauen wir uns das Schritt für Schritt an, für einen eindimensionalen Regressor $x \in \mathbb{R}$ mit zwei Klassen, deren $x$-Werte sich überlappen:

1. Im eindimensionalen Plot liegen alle Punkte der Klasse 0 auf der Höhe $y = 0$ und alle Punkte der Klasse 1 auf $y = 1$.
2. Die lineare Regression fittet eine Gerade $\hat{y} = w x + b$ durch diese Punktwolke. Die Gerade nimmt Werte in ganz $\mathbb{R}$ an, auch weit außerhalb von $[0, 1]$.
3. **Harte Klassifikation**: Wir entscheiden für Klasse 1, wenn $\hat{y} > \tfrac12$. Die Entscheidungsgrenze ist der Punkt $x^*$ mit $w x^* + b = \tfrac12$; die vorhergesagte Klasse als Funktion von $x$ ist eine Sprungfunktion.
4. Für einen zweidimensionalen Regressor $x \in \mathbb{R}^2$ wird aus der Geraden eine Regressionshyperebene über der $(x_1, x_2)$-Ebene, und die Entscheidungsgrenze $\{ w \cdot x + b = \tfrac12 \}$ ist eine Gerade in der $(x_1, x_2)$-Ebene – genau wie beim Perzeptron.

<!-- TODO Abbildungen (Folien 54–62): Regressionsgerade auf 0/1-Daten; harte Klassifikation; 2D-Regressor mit Entscheidungsgrenze; 3D-Regressionshyperebene; 1D-Fall mit Sprungfunktion und S-Kurve -->

### S-Förmigkeit herstellen

Die Sprungfunktion $[\hat{y} > \tfrac12]$ ist unbefriedigend: Sie ist nicht differenzierbar, und sie verrät nicht, wie *sicher* die Entscheidung ist. Anstelle von $[\hat{y} > \tfrac12]$ könnte man $[\tanh(\hat{y}) > 0]$ verwenden; $\tanh$ liegt zwischen $-1$ und $+1$. Um zwischen $0$ und $1$ zu landen, kann man z.B.

$$
\tfrac12 \left( \tanh(\hat{y}) + 1 \right)
$$

nutzen. Das liefert eine S-förmige Kurve, die glatt von 0 nach 1 übergeht. Aber: Die Interpretation einer Zahl zwischen 0 und 1 als *Wahrscheinlichkeit* ist damit noch unklar. Genau das klärt das nächste Kapitel mit der logistischen Regression.

## Tipps zum Übungsblatt

Auf Blatt 3 geht es um das verallgemeinerte Perzeptron und um *schwache Ableitungen*, damit wir später auch Funktionen mit Knick (wie $|x|$ oder ReLU) ableiten können.

* Das Beispiel mit der Betragsfunktion ist wichtig. Versuchen Sie zu verstehen, dass die veränderte Vorzeichenfunktion „quatschi“ mit $\operatorname{quatschi}(x) = \operatorname{sign}(x)$ für $x \neq 0$ und $\operatorname{quatschi}(0) := 100$ ebenfalls eine schwache Ableitung der Betragsfunktion ist.
* Lassen Sie sich nicht von Integralen einschüchtern, denn um die geht es „in Wirklichkeit“ nicht. Aber Integrale haben eine besondere Eigenschaft, die hier zur Geltung kommt – gerade bei dem Beispiel oben: Der Wert an einem einzelnen Punkt spielt keine Rolle.
* Wir brauchen das später beim Gradientenabstieg und bei Backpropagation.
