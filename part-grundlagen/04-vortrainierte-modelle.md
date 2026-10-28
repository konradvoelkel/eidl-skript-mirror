---
title: "Vortrainierte Modelle verwenden"
short_title: "Vortrainierte Modelle"
---

# Vortrainierte Modelle verwenden

## Orientierung

### Was tun mit Deep Learning?

Bevor wir selbst Modelle trainieren, lohnt sich ein Blick darauf, was es schon gibt. Wenn wir für eine Aufgabe ein vortrainiertes Modell verwenden wollen, müssen wir wissen, welches Modell geeignet sein kann. Dafür schauen wir bei **Hugging Face**: [huggingface.co/models](https://huggingface.co/models) listet Modelle, [huggingface.co/tasks](https://huggingface.co/tasks) sortiert sie nach Aufgabe („The Hugging Face Hub hosts many models for a variety of machine learning tasks.“). Die Task-Seiten sind ein guter Einstieg, um das Vokabular zu lernen: Was ist Image Classification, Object Detection, Token Classification, Text Generation, …? Einen systematischen Rundgang machen wir im nächsten Abschnitt.

Die Task-Seite gruppiert nach Modalität. Zur Orientierung, in der Reihenfolge von dort:

| Modalität | Tasks (Auswahl) |
|---|---|
| Computer Vision | Image Classification, Object Detection, Image Segmentation, Depth Estimation, Image-to-Image, Text-to-Image, Zero-Shot Image Classification |
| Natural Language Processing | Text Classification, Token Classification, Question Answering, Summarization, Translation, Text Generation, Fill-Mask, Sentence Similarity |
| Audio | Automatic Speech Recognition, Text-to-Speech, Audio Classification |
| Multimodal | Image-to-Text, Visual Question Answering, Document Question Answering, Feature Extraction |
| Tabular, Reinforcement Learning | Tabular Classification und Regression; Reinforcement Learning |

Die Namen sind das Vokabular, in dem Modellkarten, Papers und Stellenanzeigen reden.

### Hugging Face …?

Surfen Sie ruhig weiter auf huggingface.co. Hier ein paar Fakten zur Einordnung:

* HF verdient Geld mit gehosteter Inferenz.
* HF lockt Entwickler an mit guter Infrastruktur: Libraries (z.B. `transformers`, `diffusers`, `gradio`), Hosting (git-Repositories für Modelle, Datensätze und „Spaces“) und Dokumentation – insbesondere für **Finetuning**, das Nachtrainieren von vortrainierten Modellen.
* HF ist ein Unternehmen aus New York City, gegründet 2016. In der Finanzierungsrunde vom August 2023 war es 4,5 Mrd. US-Dollar wert; gut drei Jahre später, im September 2026, hat **Nvidia** den Kauf für 12,93 Mrd. US-Dollar vereinbart – der Abschluss wird für die erste Hälfte 2027 erwartet, vorbehaltlich der Freigaben. Die Plattform, auf der die offenen Gewichte liegen, gehört damit demselben Konzern wie die Hardware, auf der sie gerechnet werden.

Mit anderen Worten: Der Hub ist ein kommerzielles Angebot, aber die Modelle und Libraries darauf sind größtenteils offen, und für uns ist er die bequemste Art, an Gewichte zu kommen.

## Ein Rundgang durch die Tasks

Wenn wir für eine Aufgabe ein vortrainiertes Modell verwenden wollen, müssen wir wissen, welches Modell geeignet sein kann. Auf [huggingface.co/tasks](https://huggingface.co/tasks) sind die Modelle nach *Tasks* sortiert. Wir gehen exemplarisch einige davon durch – nicht, um die Modelle zu verstehen, sondern um das Vokabular zu lernen und ein Gefühl dafür zu bekommen, was heute „von der Stange“ geht.

### Tasks in Computer Vision

* **Depth Estimation**: Von einem Bild für jeden Pixel bei $(x, y)$ auch eine $z$-Koordinate schätzen. Beispiel: Intels *Dense Prediction Transformer* (DPT) von 2021, ein Vision Transformer.
* **Image Classification**: Von einem Bild sagen, was es ist. Beispiel: Microsofts *ResNet* (CNN, 2016), trainiert auf ImageNet – gibt zu einem Foto „Igel“ zurück.
* **Object Detection**: Von einem Bild sagen, was drauf ist, mit Bounding Boxes. Beispiel: *YOLOS* (NeurIPS 2021), trainiert auf ImageNet und COCO – findet in Bild #7781 des COCO-Datensatzes „Cat, Banana, Chair“.
* **Image Segmentation**: Auf einem Bild für jedes erkannte Objekt die Umrisse finden, das Bild also aufteilen. Beispiel: Nvidias *Segformer* (2021), auf ImageNet vortrainiert und auf ADE20k gefinetunt.
* **Image-to-Image**: Ein Bild als Input, ein Bild als Output, z.B. historische Fotos einfärben. Beispiel: Renato Sortinos *ColorizeNet*, ein Finetune von ControlNet / Stable Diffusion 2.1 auf bearbeitetem COCO.
* **Unconditional Image Generation**: Nur ein Bild als Output, z.B. ein Katzenbild (je nach Datenbasis). Beispiel: *DDPM* (Ho et al., 2020), Denoising Diffusion Probabilistic Models – auf dem Hub liegt der Checkpoint unter `google/`, das Verfahren kommt aus Berkeley.
* **Zero-Shot Image Classification**: Von einem Bild sagen, was es ist – ohne dass für die Klassen gelabelte Daten vorlagen. Beispiel: OpenAIs *CLIP-ViT* (2021), Contrastive Language-Image Pretrained Vision Transformer, dem man die Kandidaten als Text gibt („a photo of a car“).

Zur Einordnung des Vokabulars: **Zero-Shot** heißt ohne gelabelte Daten für die neue Aufgabe, **One-Shot** (oder Single-Shot) mit einem gelabelten Sample, **Few-Shot** mit einigen wenigen gelabelten Samples.

### Tasks in NLP

Wir betrachten nur einen Teil der NLP-Tasks:

* **Text Classification**: Texten ein Genre, eine Stimmung (Sentiment) o.ä. zuordnen. Beispiel: *DistilBERT* (2019), self-supervised trainiert mit BERT (Bidirectional Encoder Representations from Transformers) als Lehrer – zur [Destillation](../part-architekturen-anwendungen/25-destillation.md) kommen wir gegen Ende der Vorlesung.
* **Token Classification**: Named Entity Recognition (NER) oder Part-of-Speech (PoS) Tagging, also jedem Wort ein Label geben. Beispiel: *flair ner-german* (2020) von der HU Berlin.
* **Summarization**: Zu einem Text (Satz oder Dokument) eine kurze Zusammenfassung schreiben. Beispiel: Facebooks *BART* (2019), Bidirectional and Auto-Regressive Transformers.
* **Fill-Mask**: Einen Lückentext füllen. Beispiel: wieder *DistilBERT* – das ist nämlich genau die Aufgabe, mit der BERT-artige Modelle vortrainiert werden.

## Praktisch

### Beispiel: Übersetzen mit WMT19

Wir übersetzen von Englisch nach Deutsch mit Facebooks WMT19-Modell, nach der Anleitung von Hugging Face. Dieses Beispiel braucht ein Paket mehr als die Installation weiter unten: Der FSMT-Tokenizer bricht ohne `sacremoses` mit einem `ImportError` ab, und `transformers[torch]` zieht es nicht mit. Also `pip install 'transformers[torch]' sacremoses` – oder, ohne vorher etwas einzurichten, `uv run --with 'transformers[torch]' --with sacremoses uebersetzen.py`.

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

Das Muster ist typisch für alle Modelle auf dem Hub: Ein **Tokenizer** verwandelt Text in Zahlen (`input_ids`, als PyTorch-Tensor, daher `return_tensors="pt"`), das **Modell** verwandelt Zahlen in Zahlen, und der Tokenizer verwandelt das Ergebnis zurück in Text. Für Bild- und Audiomodelle gilt dasselbe Muster, nur heißt der erste Schritt dort nicht Tokenizer: Ein Bild wird zu Pixelwerten, Audio zu einem Spektrogramm, und das Gegenstück heißt in `transformers` `AutoProcessor` oder `FeatureExtractor`. Kodieren, rechnen, dekodieren. `from_pretrained` lädt die Gewichte beim ersten Aufruf aus dem Hub herunter und cached sie lokal.

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

`pip install 'transformers[torch]'` in der Shell (oder `!pip install ...` in einem Notebook) installiert `transformers` und PyTorch. Das allein installiert noch kein CUDA, d.h. alle Rechnungen finden auf der CPU mit dem Hauptspeicher statt – in PyTorch ist das schlicht das Gerät `cpu`, ohne Indexnummer. In den `pipeline`-Aufrufen von `transformers` schreibt man dafür `device=-1`; `device=0` meint dort die *erste GPU*.

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
python -m venv .venv
source .venv/bin/activate
```

und erst *danach* mit `pip` fleißig installieren. Oder entspannt `uv` benutzen, das Umgebung und Pakete in einem Schritt verwaltet.

### Alternative: Google Colab

Wer nicht lokal installieren will oder keine GPU hat: [Google Colab](https://colab.research.google.com/notebooks/intro.ipynb) bietet Jupyter-Notebooks mit (begrenzter) GPU-Zeit im Browser. Ein neues Notebook gibt es unter [colab.research.google.com/#create=true](http://colab.research.google.com/#create=true); die Hugging-Face-Dokumentation ist als Colab-Notebooks verfügbar, z.B. die [Task Summary](https://colab.research.google.com/github/huggingface/notebooks/blob/main/transformers_doc/en/task_summary.ipynb).
