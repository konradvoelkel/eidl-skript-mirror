---
title: "VL 03: PyTorch Basics und Tensoren"
short_title: "VL 03"
---

# PyTorch Basics und Tensoren

:::{warning} Rohfassung
Dieses Kapitel ist eine automatische Transkription der Folien von VL 03 aus dem WiSe 2025/26
(`from_2025/slides/Einführung in Deep Learning 2025_26 VL 03_ PyTorch Basics, Tensoren.pdf`), Folie für Folie in der Originalreihenfolge.
Formeln und Abbildungen sind dabei größtenteils verloren gegangen; der Text ist noch nicht überarbeitet.
:::

## Vortrainierte Modelle verwenden; Orientierung

<!-- Folie 2 -->

## Tasks

<!-- Folie 3 -->
Was tun mit Deep Learning?
Wenn wir für eine Aufgabe ein vortrainiertes
Modell verwenden wollen,
müssen wir wissen, welches Modell
geeignet sein kann.
→ Wir schauen bei Hugging Face
huggingface.co/models
huggingface.co/tasks
“The Hugging Face Hub hosts many models
for a variety of machine learning tasks.”

## Tasks in Computer Vision

<!-- Folie 4 -->
Exemplarisch erstmal das

<!-- Folie 5 -->
Von einem Bild für jeden Pixel bei (x,y)
auch eine z-Koordinate schätzen
Beispiel: Intel’s Dense Prediction Transformer (DPT) von 2022
(ein Vision Transformer)

<!-- Folie 6 -->
Von einem Bild sagen, was es ist
Beispiel: Microsoft’s ResNet CNN von 2016
Trainiert auf ImageNet
Igel

<!-- Folie 7 -->
Von einem Bild sagen, was drauf ist
Beispiel: YOLOS von 2021 (NeurIPS)
Trainiert auf ImageNet und COCO
Cat, Banana,
Chair
#7781 from
COCO dataset

<!-- Folie 8 -->
Beispiel: Nvidia’s Segformer von 2021
Trainiert auf ImageNet, COCO und ADE20k
Auf einem Bild für jedes erkannte
Objekt Umrisse finden (das Bild
segmentieren = aufteilen)
Cat, Banana,
Chair
#7781 from
COCO dataset

<!-- Folie 9 -->
Ein Bild als Input, ein Bild als Output
z.B. historische Photos einfärben
Beispiel: Renato Sortino’s ColorizeNet
Finetune von ControlNet / Stable Diffusion 2.1
auf bearbeitetem COCO

<!-- Folie 10 -->
Ein Bild als Output
z.B. ein Katzenbild (je nach Datenbasis)
Beispiel: Google’s DDPM (2020)
(Denoising Diffusion Probabilistic Models)

<!-- Folie 11 -->
Beispiel: OpenAI’s CLIP-ViT (2021)
Contrastive Language-Image Pretrained Vision Transformer
Von einem Bild sagen, was es ist
(z.B. ein Foto von einem Auto)
Zero-Shot = ohne gelabelte Daten

<!-- Folie 12 -->
Beispiel: OpenAI’s CLIP-ViT (2021)
Contrastive Language-Image Pretrained Vision Transformer
Von einem Bild sagen, was es ist
(z.B. ein Foto von einem Auto)
Zero-Shot = ohne gelabelte Daten

<!-- Folie 13 -->
vgl. Single-Shot / One-Shot = ein gelabeltes Sample,
Few-Shot = einige wenige gelabelte Samples
Beispiel: OpenAI’s CLIP-ViT (2021)
Contrastive Language-Image Pretrained Vision Transformer
Von einem Bild sagen, was es ist
(z.B. ein Foto von einem Auto)
Zero-Shot = ohne gelabelte Daten

## Tasks

<!-- Folie 14 -->

## Tasks in NLP

<!-- Folie 15 -->
Wir betrachten
einen Teil der
NLP-Tasks

<!-- Folie 16 -->
Texten ein Genre oder eine Stimmung
o.ä. zuordnen
Beispiel: DistilBERT (2019)
Self-supervised trainiert mit BERT
(Bidirectional Encoder
Representations from
Transformers) als Lehrer

<!-- Folie 17 -->
Beispiel: flair ner-german (2020)
von der HU Berlin
Named Entity
Recognition (NER)
oder Part-of-Speech
(PoS) tagging

<!-- Folie 18 -->
Zu einem Text (Satz oder
Dokument o.ä.) eine kurze
Zusammenfassung schreiben
Beispiel: Facebook’s BART (2019)
(Bidirectional and Auto-Regressive
Transformers)

<!-- Folie 19 -->
Einen Lückentext füllen
Beispiel: DistilBERT (2019) wieder!

## Vortrainierte Modelle verwenden; Praktisch

<!-- Folie 20 -->

## Beispiel: Vortrainiertes Modell verwenden

<!-- Folie 21 -->
Wir übersetzen von Englisch nach Deutsch mit Facebook’s WMT19
Nach der Anleitung von Hugging Face:
from transformers import FSMTForConditionalGeneration, FSMTTokenizer
mname = "facebook/wmt19-en-de"
tokenizer = FSMTTokenizer.from_pretrained(mname)
model = FSMTForConditionalGeneration.from_pretrained(mname)
input = "I am not sure if deep learning is really for me."
input_ids = tokenizer.encode(input, return_tensors="pt")
outputs = model.generate(input_ids)
decoded = tokenizer.decode(outputs[0], skip_special_tokens=True)
print(decoded) # Ich bin mir nicht sicher, ob Deep Learning wirklich etwas für mich ist.

<!-- Folie 22 -->
Wir übersetzen von Englisch nach Deutsch mit Facebook’s WMT19
Auf der GPU mit CUDA rechnen:
from transformers import FSMTForConditionalGeneration, FSMTTokenizer
mname = "facebook/wmt19-en-de"
tokenizer = FSMTTokenizer.from_pretrained(mname)
model = FSMTForConditionalGeneration.from_pretrained(mname).to("cuda")
input = "I am not sure if deep learning is really for me."
input_ids = tokenizer.encode(input, return_tensors="pt").to("cuda")
outputs = model.generate(input_ids)
decoded = tokenizer.decode(outputs[0], skip_special_tokens=True)
print(decoded) # Ich bin mir nicht sicher, ob Deep Learning wirklich etwas für mich ist.

<!-- Folie 23 -->
Wir übersetzen von Englisch nach Deutsch mit Facebook’s WMT19
Was zuvor geschah:
$ pip install 'transformers[torch]'
in der Shell, oder in einem Notebook:
!pip install 'transformers[torch]'
Das allein installiert noch kein CUDA,
d.h. alle Rechnungen (mit PyTorch) finden auf der CPU mit dem Hauptspeicher statt,
das ist intern “device 0”.

<!-- Folie 24 -->
Wir übersetzen von Englisch nach Deutsch mit Facebook’s WMT19
Üblicher Workflow:
import torch
device = torch.device("cuda")
if torch.cuda.is_available()
else torch.device("cpu")
model.to(device)
Alternativ kann die accelerate-Library von HF auch dynamisch Teile
des Modells auf die GPU, andere Teile im Hauptspeicher belassen, um
sehr große Modelle zu nutzen.

<!-- Folie 25 -->
Wir übersetzen von Englisch nach Deutsch mit Facebook’s WMT19
Was zuvor geschah (in Ubuntu Linux auf NVIDIA Hardware):
$ lspci | grep -i nvidia
0d:00.0 VGA compatible controller: NVIDIA Corporation TU104 [GeForce RTX 2060] (rev a1)
$ nvidia-smi
+------------------------------------------------------------------------------+
| NVIDIA-SMI 470.199.02
Driver Version: 470.199.02
CUDA Version: 11.4 |
|-------------------------------+----------------------+-----------------------+
$ sudo apt install cuda
$ sudo systemctl reboot

<!-- Folie 26 -->
Wir übersetzen von Englisch nach Deutsch mit Facebook’s WMT19
Was zuvor geschah (in Ubuntu Linux auf NVIDIA Hardware):
$ nvidia-smi
+------------------------------------------------------------------------------+
| NVIDIA-SMI 470.199.02
Driver Version: 470.199.02
CUDA Version: 11.4 |
|-------------------------------+----------------------+-----------------------+
$ nvcc --version
nvcc: NVIDIA (R) Cuda compiler driver
Copyright (c) 2005-2019 NVIDIA Corporation
Built on Sun_Jul_28_19:07:16_PDT_2019
Cuda compilation tools, release 10.1, V10.1.243
Das bedeutet, die GPU kann CUDA 11.4, installiert ist CUDA 10.1. Passt!

<!-- Folie 27 -->
Wir übersetzen von Englisch nach Deutsch mit Facebook’s WMT19
Was zuvor geschah (in Ubuntu Linux auf NVIDIA Hardware):
$ pip install torch torchvision --index-url \
https://download.pytorch.org/whl/cu129
Hat es geklappt? Python Interpreter auf und:
import torch
torch.cuda.is_available()
Auf AMD GPUs: statt CUDA heißt das ROCm, aber der Befehl ist der selbe.
Auf MacOS 12.3+ gibt es auch Beschleunigung, MPS.

<!-- Folie 28 -->
Wir übersetzen von Englisch nach Deutsch mit Facebook’s WMT19
Was zuvor geschah (in Linux):
In dem Ordner, in dem man gerade arbeitet (also .py-Code speichert usw.):
$ python -m venv .env
$ source .env/bin/activate
Und erst DANACH mit pip fleissig installieren.
Oder entspannt
uv benutzen ;-)
Später ggf.
$ source .env/bin/deactivate

<!-- Folie 29 -->
Alternative zur lokalen Installation: Google Colab
Übersicht, was Google Colab ist und kann:
colab.research.google.com/notebooks/intro.ipynb
Neues Notebook ausprobieren: http://colab.research.google.com/#create=true
Beispiel eines Hugging Face Tutorials / Dokumentation Notebooks:
colab.research.google.com/github/huggingface/notebooks/blob/main/transformers_doc/en/task_summary.ipynb

## PyTorch Basics: Tensoren

<!-- Folie 30 -->

## PyTorch Datenmodell

<!-- Folie 31 -->
Tensoren ≈ Arrays
Was ist ein Array?
Was ist ein Tensor?
Was ist ein Array in Numpy?
Was ist ein Tensor in Torch?

<!-- Folie 32 -->
Tensoren ≈ Arrays
Was ist ein Array?
Was ist ein Tensor?
Was ist ein Array in Numpy?
Ein Array ist eine Sammlung von Daten von
gleichem Typ, die fortlaufend im Speicher
liegen (können).
Physiker: Ein Tensor ist ein Objekt, dass
sich tensoriell transformiert.
Was ist ein Tensor in Torch?

<!-- Folie 33 -->
Tensoren ≈ Arrays
Was ist ein Array?
Was ist ein Tensor?
Was ist ein Array in Numpy?
Was ist ein Tensor in Torch?
Ein Array ist eine Sammlung von Daten von
gleichem Typ, die fortlaufend im Speicher
liegen.
Physiker: Ein Tensor ist ein Objekt, dass
sich tensoriell transformiert.
Mathematiker: Ein Tensor ist ein Element in
einem Tensorproduktraum.

<!-- Folie 34 -->
Tensoren ≈ Arrays
Was ist ein Array?
Was ist ein Tensor?
Was ist ein Array in Numpy?
Was ist ein Tensor in Torch?
Ein Array ist eine Sammlung von Daten von
gleichem Typ, die fortlaufend im Speicher
liegen.
Physiker: Ein Tensor ist ein Objekt, dass
sich tensoriell transformiert.
Mathematiker: Ein Tensor ist ein Element in
einem Tensorproduktraum.
Informatiker: Ein Tensor ist ein fancy Wort
für Arrays.

<!-- Folie 35 -->
Tensoren ≈ Arrays
Was ist ein Array?
Was ist ein Tensor?
Was ist ein Array in Numpy?
Was ist ein Tensor in Torch?
Ein Tensor in Torch ist eine Sammlung
von Daten von gleichem Typ (dem dtype),
die fortlaufend im Speicher liegen, und
zwar potentiell im GPU-Speicher,
optimiert für Gradientenabstiegsmethoden
(Attribut “grad”).
Man kann einen Torch Tensor aus einem
Numpy Array herstellen - sogar ohne
zusätzlichen Speicher zu verbrauchen!
→ PyTorch Tutorial “Tensors”

## Ausflug: Tensoren in der Mathematik

<!-- Folie 36 -->
Definitionen
Gegeben Vektorräume U, V, W
(z.B. V = ℝn und W = ℝm)
kann man das Tensorprodukt bilden:
V ⊗ W ist definiert als ein Vektorraum
sodass es eine 1:1-Korrespondenz gibt:
{Bilineare Abbildungen V ✕ W → U}
{Lineare Abbildungen V ⊗ W → U}
Insbesondere gibt es eine bilineare Abb.
V ✕ W → V ⊗ W.

<!-- Folie 37 -->
Definitionen
Gegeben Vektorräume U, V, W
(z.B. V = ℝn und W = ℝm)
kann man das Tensorprodukt bilden:
V ⊗ W ist definiert als ein Vektorraum
sodass es eine 1:1-Korrespondenz gibt:
{Bilineare Abbildungen V ✕ W → U}
{Lineare Abbildungen V ⊗ W → U}
Insbesondere gibt es eine bilineare Abb.
V ✕ W → V ⊗ W.
Wenn v1, ..., vn ∊ V und w1, ..., wm ∊ W
Basen sind, so ist vi⊗wj Basis von V ⊗ W.

<!-- Folie 38 -->
Definitionen
Gegeben Vektorräume U, V, W
(z.B. V = ℝn und W = ℝm)
kann man das Tensorprodukt bilden:
V ⊗ W ist definiert als ein Vektorraum
sodass es eine 1:1-Korrespondenz gibt:
{Bilineare Abbildungen V ✕ W → U}
{Lineare Abbildungen V ⊗ W → U}
Insbesondere gibt es eine bilineare Abb.
V ✕ W → V ⊗ W.
Wenn v1, ..., vn ∊ V und w1, ..., wm ∊ W
Basen sind, so ist vi⊗wj Basis von V ⊗ W.
Man kann den Dualraum bilden:
Vv := Hom(V, ℝ), (ein neuer Vektorraum)
Die Menge der linearen Abbildungen V→ℝ.
Man nennt die Elemente von V Vektoren,
die Elemente von Vv Kovektoren oder
Linearformen.

<!-- Folie 39 -->
Definitionen
Gegeben Vektorräume U, V, W
(z.B. V = ℝn und W = ℝm)
kann man das Tensorprodukt bilden:
V ⊗ W ist definiert als ein Vektorraum
sodass es eine 1:1-Korrespondenz gibt:
{Bilineare Abbildungen V ✕ W → U}
{Lineare Abbildungen V ⊗ W → U}
Insbesondere gibt es eine bilineare Abb.
V ✕ W → V ⊗ W.
Wenn v1, ..., vn ∊ V und w1, ..., wm ∊ W
Basen sind, so ist vi⊗wj Basis von V ⊗ W.
Man kann den Dualraum bilden:
Vv := Hom(V, ℝ), (ein neuer Vektorraum)
Die Menge der linearen Abbildungen V→ℝ.
Man nennt die Elemente von V Vektoren,
die Elemente von Vv Kovektoren oder
Linearformen.
Wenn v1, ..., vn ∊ V eine Basis ist, sind die
Linearformen viv := vi· eine Basis von Vv.
Man sagt, die Elemente von W⊗Vv sind
kovariant in W und kontravariant in V.
In Einstein-Notation schreiben wir Indizes
für W unten, für Vv oben.

<!-- Folie 40 -->
Dualisieren mit Standardskalarprodukt
Gegeben einen Vektorraum ℝn mit der
Standardbasis und dem
Standard-Skalarprodukt können wir
Vektoren in Kovektoren verwandeln (und
zurück) durch Transponieren:
Spaltenvektor v ∊ ℝn wird zu
Zeilenvektor vT ∊ (ℝn)v,
über die Matrixmultiplikation
(Skalarprodukt):
vT w = v · w ∊ ℝ

<!-- Folie 41 -->
Skalare, Vektoren und Matrizen als Tensoren
Gegeben einen Vektorraum V lässt sich
auch das iterierte Tensorprodukt
betrachten:
V⊗k = V⊗ … ⊗V (k mal)
Dabei ist es Konvention, dass
V⊗0 = ℝ, denn V⊗ℝ = V.

<!-- Folie 42 -->
Skalare, Vektoren und Matrizen als Tensoren
Gegeben einen Vektorraum V lässt sich
auch das iterierte Tensorprodukt
betrachten:
V⊗k = V⊗ … ⊗V (k mal)
Dabei ist es Konvention, dass
V⊗0 = ℝ, denn V⊗ℝ = V.
Eine Matrix M ∊ ℝnxm lässt sich auffassen
als lineare Abbildung F : ℝm → ℝn.
Die Spalten der Matrix sind F(e1), …, F(em),
die Bilder der Basisvektoren (in ℝn).
Es ist für jeden Vektor v ∊ ℝm stets
v = (e1 · v)e1 + … + (em · v)em
= ∑i=1..m (ei·v)ei

<!-- Folie 43 -->
Skalare, Vektoren und Matrizen als Tensoren
Gegeben einen Vektorraum V lässt sich
auch das iterierte Tensorprodukt
betrachten:
V⊗k = V⊗ … ⊗V (k mal)
Dabei ist es Konvention, dass
V⊗0 = ℝ, denn V⊗ℝ = V.
Es ist für jeden Vektor v ∊ ℝm stets
v = (e1 · v)e1 + … + (em · v)em
= ∑i=1..m (ei·v)ei
Eine Matrix M ∊ ℝnxm lässt sich auffassen
als lineare Abbildung F : ℝm → ℝn.
Die Spalten der Matrix sind F(e1), …, F(em),
die Bilder der Basisvektoren (in ℝn).
F(v) = F( ∑i=1..m (ei·v)ei )
= ∑i=1..m (ei·v) F(ei) also
F = ∑i=1..m F(ei) (ei· )
= ∑i=1..m F(ei) (ei)v ∊ ℝn⊗(ℝm)v

<!-- Folie 44 -->
Skalare, Vektoren und Matrizen als Tensoren
Gegeben einen Vektorraum V lässt sich
auch das iterierte Tensorprodukt
betrachten:
V⊗k = V⊗ … ⊗V (k mal)
Dabei ist es Konvention, dass
V⊗0 = ℝ, denn V⊗ℝ = V.
Es ist für jeden Vektor v ∊ ℝm stets
v = (e1 · v)e1 + … + (em · v)em
= ∑i=1..m (ei·v)ei
Eine Matrix M ∊ ℝnxm lässt sich auffassen
als lineare Abbildung F : ℝm → ℝn
bzw. als Element des Tensorproduktraums:
F = ∑i=1..m F(ei) (ei)v ∊ ℝn⊗(ℝm)v
Jedes Element eines Tensorproduktraums,
also auch Skalare x ∊ ℝ = V⊗0,
Vektoren v ∊ V = V⊗1 und lineare
Abbildungen F ∊ Hom(W,V) = V⊗(W)v
wird Tensor genannt.

<!-- Folie 45 -->
Größere Tensoren
Was ist mit T ∊ ℝn⊗ℝm⊗(ℝp)v⊗(ℝq)v,
was ist das für ein Tensor?

<!-- Folie 46 -->
Obacht: lineare Abbildung ≠ Matrix
Wir wissen: jede Matrix lässt sich als
lineare Abbildung interpretieren.
Umgekehrt: gegeben eine Wahl von Basen
lässt sich jede lineare Abbildung als Matrix
schreiben, die darstellende Matrix.
Wir können so auch jeden Vektor in einer
Basis darstellen, und der gleiche Vektor
v ∊ V kann mehrere verschiedene
darstellende Vektoren [v]B ∊ ℝn haben
(wobei n = dimV ist und B eine Basis).

<!-- Folie 47 -->
Obacht: lineare Abbildung ≠ Matrix
Wir wissen: jede Matrix lässt sich als
lineare Abbildung interpretieren.
Umgekehrt: gegeben eine Wahl von Basen
lässt sich jede lineare Abbildung als Matrix
schreiben, die darstellende Matrix.
Wir können so auch jeden Vektor in einer
Basis darstellen, und der gleiche Vektor
v ∊ V kann mehrere verschiedene
darstellende Vektoren [v]B ∊ ℝn haben
(wobei n = dimV ist und B eine Basis).
Zu einem Tensor T ∊ U⊗V⊗W lässt sich
auch eine Darstellung finden, wenn man
Basen von U, V und W wählt.
Diese hat nun zu jedem Tripel von Indizes
(i, j, k) ein “Matrixelement”, nämlich den
Koeffizienten von ui⊗vj⊗wk.
Das lässt sich dreidimensional darstellen,
analog zur zweidimensionalen Darstellung
für Matrizen.

<!-- Folie 48 -->
Zurück zu Numpy & Co
In der Mathematik müssen wir uns zu
einem Tensor in einem Tensorproduktraum
merken, wie das Tensorprodukt zustande
kam, um zu wissen, welche Variablen
kovariant und welche kontravariant sind.

<!-- Folie 49 -->
Zurück zu Numpy & Co
In der Mathematik müssen wir uns zu
einem Tensor in einem Tensorproduktraum
merken, wie das Tensorprodukt zustande
kam, um zu wissen, welche Variablen
kovariant und welche kontravariant sind.
Wählt man überall Basen, so verschwindet
der Unterschied (man sieht nur noch die
Koeffizienten).
In Numpy arbeiten wir implizit mit
Darstellungen in der Standardbasis von ℝn.

<!-- Folie 50 -->
Zurück zu Numpy & Co
In der Mathematik müssen wir uns zu
einem Tensor in einem Tensorproduktraum
merken, wie das Tensorprodukt zustande
kam, um zu wissen, welche Variablen
kovariant und welche kontravariant sind.
Wählt man überall Basen, so verschwindet
der Unterschied (man sieht nur noch die
Koeffizienten).
In Numpy arbeiten wir implizit mit
Darstellungen in der Standardbasis von ℝn.
Ist der Shape eines Numpy Arrays a z.B.
a.shape == (4,10,2)
So bedeutet dies, dass mathematisch
gesehen
a ∊ ℝ4⊗ℝ10⊗ℝ2.
Quizfrage: Was macht der Reshape?

## Ausflug beendet.

<!-- Folie 51 -->
Zurück zu Numpy & Co
In der Mathematik müssen wir uns zu
einem Tensor in einem Tensorproduktraum
merken, wie das Tensorprodukt zustande
kam, um zu wissen, welche Variablen
kovariant und welche kontravariant sind.
Wählt man überall Basen, so verschwindet
der Unterschied (man sieht nur noch die
Koeffizienten).
In Numpy arbeiten wir implizit mit
Darstellungen in der Standardbasis von ℝn.
n
m
n*m
Es ist ℝ ⊗ℝ = ℝ
.
Ist der Shape eines Numpy Arrays a z.B.
a.shape == (4,10,2)
So bedeutet dies, dass mathematisch
gesehen
a ∊ ℝ4⊗ℝ10⊗ℝ2.
Quizfrage: Was macht der Reshape?
Beispiel: ℝ4⊗ℝ10 hat eine Basis der Form
ei⊗ej, also insgesamt der Länge 4*10=40.
a.reshape(-1,2) == a.reshape(40,2)

## Lineare Regression zur Klassifikation

<!-- Folie 52 -->

<!-- Folie 53 -->
Wenn wir an Regression denken, dann oft an eine Regressionsgerade in einem x-y-Plot,
bei dem auf der x-Achse die unabhängige Variable (der Regressor) und auf der y-Achse
die abhängige Variable (der Regressand) aufgetragen ist.

<!-- Folie 54 -->

<!-- Folie 55 -->
Eindimensionaler Plot der gleichen Situation:

<!-- Folie 56 -->
Eindimensionaler Plot, harte Klassifikation

<!-- Folie 57 -->
Verallgemeinerung auf zweidimensionalen Regressor

<!-- Folie 58 -->
Visualisierung der Entscheidungsgrenze

<!-- Folie 59 -->
Dreidimensionales Bild, Regressionshyperebene

<!-- Folie 60 -->
Eindimensionaler Fall, Vorhersage auf y-Achse

<!-- Folie 61 -->
Eindimensionaler Fall, Vorhersage auf y-Achse

<!-- Folie 62 -->
Eindimensionaler Fall, Vorhersage auf y-Achse

<!-- Folie 63 -->
S-Förmigkeit herstellen
Anstelle von [y > ½] könnte man auch [tanh(y) > 0] verwenden;
tanh liegt zwischen -1 und +1.
Um zwischen 0 und 1 zu landen, kann z.B. ½ * (tanh(y)+1) nutzen.
Das liefert eine S-förmige Kurve.
Aber: Interpretation einer Zahl zwischen 0 und 1 als Wahrscheinlichkeit unklar.

## Zum neuen Übungsblatt

<!-- Folie 64 -->
Tipps für Blatt 3
◼ Das Beispiel mit der Betragsfunktion ist wichtig. Versuchen Sie zu
verstehen, dass die veränderte Vorzeichenfunktion “quatschi” mit
der Definition quatschi(x) = sign(x) für x≠0 und quatschi(0) := 100
ebenfalls eine schwache Ableitung der Betragsfunktion ist.
◼ Lassen Sie sich nicht von Integralen einschüchtern,
Denn um die geht es “in Wirklichkeit” nicht.
Aber Integrale haben eine besondere Eigenschaft,
die hier zur Geltung kommt - gerade bei dem Beispiel oben.
→ Wir brauchen das später beim Gradientenabstieg/Backpropagation.
