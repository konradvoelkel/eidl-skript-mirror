---
title: "VL 11: LLMs benutzen"
short_title: "VL 11"
---

# LLMs benutzen

:::{note} Stand
Erste Prosafassung (aus den Folien von VL 11, WiSe 2025/26). Abbildungen fehlen noch, siehe die `TODO`-Kommentare. Der Code ist in den Notebooks `VL_11_backprop.ipynb` und `VL_11_llamacpp.ipynb`.
:::

## Recap & Vertiefung: Backpropagation im Notebook

Bevor es um LLMs geht, ein Blick darauf, wie PyTorch Backpropagation *tatsächlich* macht (`VL_11_backprop.ipynb`). Wir bauen ein sehr kleines „Netzwerk“:

```python
x = torch.tensor(3.0)                       # Input (Konstante)
w = torch.tensor(2.0, requires_grad=True)   # Gewicht: "Beobachte mich!"
b = torch.tensor(1.0, requires_grad=True)   # Bias
z = w * x     # z = 6
y = z + b     # y = 7
L = y ** 2    # Loss = 49
```

Der **Berechnungsgraph** (ein DAG, directed acyclic graph) entsteht erst beim Ausführen: Jeder Tensor, der aus einer Operation mit einem `requires_grad`-Tensor entstanden ist, trägt eine `grad_fn` (`L.grad_fn` ist `PowBackward0`, davor `AddBackward0`, davor `MulBackward0` und `AccumulateGrad` für die Blätter $w$ und $b$). Die `grad_fn` weiß, wie man die Operation ableitet, und hält Referenzen auf die *saved tensors*, die gespeicherten Zwischenergebnisse – genau die $z_k$ aus Kapitel 6.

`L.backward()` ist der rekursive Aufruf der Kettenregel, initial mit $\frac{dL}{dL} = 1$:

$$
\frac{dL}{dw} = \frac{dL}{dy} \cdot \frac{dy}{dz} \cdot \frac{dz}{dw} = 2y \cdot 1 \cdot x = 14 \cdot 3 = 42,
\qquad
\frac{dL}{db} = 2y \cdot 1 = 14.
$$

Danach steht das Ergebnis in `w.grad` und `b.grad`. Der Optimizer-Schritt muss unter `torch.no_grad()` passieren, damit der Update selbst nicht Teil des Graphen wird, und die Gradienten müssen danach mit `zero_()` zurückgesetzt werden – sonst *akkumuliert* PyTorch sie beim nächsten `backward()`. Das ist der Grund für `optimizer.zero_grad()` in jeder Trainingsschleife.

**Freezing**: Setzt man `w.requires_grad = False`, so hat `z = w * x` keine `grad_fn` mehr, der Graph ist an dieser Stelle abgeschnitten, und ein Optimizer verändert $w$ nicht mehr, $b$ aber schon. So friert man beim Transfer Learning Schichten eines vortrainierten Modells ein – und spart dabei Speicher, weil für eingefrorene Parameter keine Gradienten gehalten werden.

**Convolution Backprop**: Wie funktioniert Backprop, wenn Gewichte geteilt werden wie bei einem Faltungslayer? Der Kernel `[0.5]` wird über den Input `[1, 2, 3]` geschoben, $o_i = x_i \cdot k$, und der Loss ist $o_1 + o_2 + o_3$. Der Gradient nach $k$ ist die *Summe* der Beiträge aller Positionen, $\frac{dL}{dk} = x_1 + x_2 + x_3 = 6$: Ein geteilter Parameter bekommt die Gradienten aller seiner Verwendungen aufsummiert – im Graphen führen mehrere Kanten zu demselben Blatt.

## Recap & Vertiefung: Universalität

### Warum neuronale Netze funktionieren

**Universelles Approximationstheorem, grobe Aussage** (wir erinnern uns an Kapitel 7): Mit neuronalen Netzen (beliebig viele Neuronen, beliebig viele Layer, fully connected, ReLU) lässt sich jede Funktion beliebig gut approximieren. Der Beweis in fünf Schritten:

1. Jede beschränkte messbare Funktion $f \colon E \subseteq \mathbb{R} \to \mathbb{R}$ ist beliebig gut ($\forall \varepsilon > 0$) durch *einfache Funktionen* $g, h$ approximierbar: $g \le f \le h$ und $0 \le h - g < \varepsilon$. Dabei sind einfache Funktionen endliche Linearkombinationen von Indikatorfunktionen messbarer Mengen. (Stetige Funktionen sind integrierbar, integrierbare Funktionen sind messbar.)
2. Eine Funktion $f \colon E \to \mathbb{R}$ (für $E$ messbar) ist messbar genau dann, wenn es eine Folge einfacher Funktionen $f_n$ gibt, die punktweise gegen $f$ konvergieren und $|f_n| \le |f|$ erfüllen. Eine messbare Funktion ist integrierbar, wenn es eine dominierende integrierbare Funktion $h$ gibt, $|f| \le |h|$. Wir können also sagen: $\{\text{messbare Funktionen}\} \approx \{\text{interessante Funktionen}\}$.
3. Jede einfache Funktion ist beliebig genau approximierbar durch *Stufenfunktionen*, d.h. endliche Linearkombinationen von Indikatorfunktionen von Intervallen. Also: $\{\text{messbare Funktionen}\} \approx \{\text{approximierbar mit Stufenfunktionen}\}$.
4. Eine einzelne Stufe lässt sich mit einem einfachen neuronalen Netz realisieren: Zwei Neuronen mit sehr steilen Sigmoiden (oder zwei ReLUs) an den Intervallgrenzen, mit Gewichten $+h$ und $-h$ in der Ausgabeschicht, ergeben eine Stufe der Höhe $h$ auf dem Intervall (Grafik von Michael Nielsen, Kapitel 4 seines Buchs).
5. Die leicht zu verstehende Konstruktion mit 2 Hidden Layers bei Michael Nielsen funktioniert auch mit beliebig hoher Ein- und Ausgabedimension, also zur Approximation von Funktionen $\mathbb{R}^n \to \mathbb{R}^n$. Es gibt auch Konstruktionen mit nur 1 Hidden Layer.

Die richtige Frage ist also nie „Geht das mit neuronalen Netzen?“ (Antwort: JA), sondern „*Wie* geht das am *effizientesten* mit neuronalen Netzen?“

<!-- TODO Abbildung: Stufe aus zwei steilen Sigmoiden (Michael Nielsen, Kap. 4) -->

### Präzisere Ergebnisse

:::{prf:theorem} Universelle Approximation (Pinkus / Kidger–Lyons)
Sei $E \subseteq \mathbb{R}^d$ eine kompakte (d.h. beschränkte und abgeschlossene) Teilmenge. Sei $\sigma \colon \mathbb{R} \to \mathbb{R}$ eine beliebige stetige Funktion, aber keine affin-lineare Abbildung, die in wenigstens einem Punkt stetig differenzierbar mit Ableitung ungleich $0$ ist. Dann gibt es zu jeder stetigen Funktion $f \colon E \to \mathbb{R}^D$ und jedem $\varepsilon > 0$ ein neuronales Netz $n$ mit Aktivierungen $\sigma$ und endlich vielen hidden Layers, je höchstens $d + D + 2$ groß, mit

$$
\sup_{x \in E} \| n(x) - f(x) \| < \varepsilon .
$$
:::

Also: schmale, aber tiefe Netze reichen. Und noch präziser, mit Aussage über die *Größe*:

:::{prf:theorem} Yarotsky (2017)
Es gibt eine Konstante $c$, sodass gilt: Zu jeder $k$-fach stetig differenzierbaren Funktion $f \colon E \to \mathbb{R}^D$ und jedem $\varepsilon > 0$ gibt es ein neuronales Netz $n$ mit ReLU-Aktivierungen und $c \log(1/\varepsilon)$ vielen hidden Layers, insgesamt etwa $c\, \varepsilon^{-d/k}$ Gewichten und $\sup_{x \in E} \| n(x) - f(x) \| < \varepsilon$.
:::

Siehe auch arXiv:1901.10267. Die Anzahl der Gewichte wächst mit der Eingabedimension $d$ exponentiell (der Fluch der Dimensionalität), aber glattere Funktionen (größeres $k$) brauchen weniger – und die Tiefe wächst nur logarithmisch in der Genauigkeit.

### Neuronale Netze vs. Bäume und Wälder

Umgekehrt lässt sich jedes ReLU-Netz auch als Entscheidungsbaum schreiben: Jedes ReLU-Neuron ist eine Ja/Nein-Entscheidung „$\langle w, x \rangle + b > 0$?“, und die Regionen, in denen alle Entscheidungen feststehen, sind genau die Stücke, auf denen das Netz linear ist (Caglar Aytekin, *Neural Networks are Decision Trees*, 2022). Der Baum ist allerdings exponentiell groß.

## Transformer-LLMs in der Praxis einsetzen

Zur Erinnerung der Aufbau eines Transformers (Kapitel 9, Fig. 1 in „Attention is all you need“): Encoder- und Decoder-Stapel aus Attention- und MLP-Blöcken. Ein *Large Language Model* ist ein sehr großer, meist Decoder-only Transformer, der das nächste Token vorhersagt.

### Verschiedene Wege, LLMs zu nutzen

Wir konkretisieren anhand eines Beispiel-Tasks, z.B. „Gegeben einen Text, identifiziere, ob er emotional positiv oder negativ gefärbt ist“ (Sentiment-Analyse).

1. **Wort-Vektor-Einbettungen direkt verwenden** (statt word2vec z.B. die Embedding-Schicht von Gemma) → semantische Ähnlichkeit, semantische Suche, semantisches Clustering etc. Pro: sehr billig (keine tiefen Modelle für Inferenz notwendig). Contra: Zusammenhänge über längere Texte hinweg nicht sichtbar.
2. **Satz-Vektor-Einbettungen**, bzw. längere Texte in Vektoren umwandeln (z.B. mit BERT). Pro: sehr hohe Qualität der Repräsentationen. Contra: LLM notwendig zur Berechnung der Repräsentationen. (Blatt 11: BERT-Embeddings als Features für einen Klassifikator.)
3. **Nicht Token sampeln, sondern die Verteilung der Ausgabetoken direkt betrachten.** Pro: vollständige Information aus dem LLM, kein „zufälliges“ Sampling. Contra: weniger intuitiv zu verwenden, man arbeitet mit Verteilungen im Latent Space statt mit Text.
4. **Fertig trainierte Transformer mit bestimmten Prompts verwenden**, z.B. „Analog zur Transformation [A] → [B] verarbeite [C]“ (*one-shot prompt*), etwa [A] = Text auf Englisch, [B] = Text auf Deutsch, [C] = neuer Text auf Englisch. Pro: extrem vielseitig und bisher sehr, sehr erfolgreich. Contra: benötigt viele Token (noch mehr für *few-shot prompts*).
5. **Transformer von Grund auf trainieren** (eigenes Pretraining). Pro: vollständige Kontrolle über Trainingsdaten und damit prinzipiell über Outputs. Contra: extrem teuer; Llama 2 (etwa auf dem Niveau von Gemini 1 Pro / ChatGPT 3.5) kostete ca. 2–10 Mio. $.
6. **Vortrainierte Transformer auf besonderen Daten weiter trainieren** (Finetuning). Pro: relativ billig (keine sehr langen Trainingszeiten = Stromkosten nötig). Contra: benötigt wenigstens Hardware zum Training (teurer für größere Modelle).
7. **Transformer-Modell auf Chat-Formate finetunen mit RLHF** (Reinforcement Learning from Human Feedback, wie bei ChatGPT). Pro: Feedback führt zu Qualitätssteigerung, z.B. NSFW-Removal o.ä. Contra: etwas komplizierter als „einfaches“ Training.
8. **Sehr große Modelle über eine API verwenden** (ggf. nur Sampling-Output). Der De-facto-Standard für die „meisten“ LLM-Use-Cases für Softwareentwickler.
9. **Vorhersagen eines großen Modells in ein kleineres übertragen** (Destillation). Das schauen wir uns in Kapitel 14 noch an; so lässt sich z.B. die Inferenz beschleunigen.
10. **Constrained Generation**: Ausgabe sampeln, die einem (z.B. JSON-)Schema genügt – ein wesentlicher Baustein für „agentische Workflows“.

## Selbst Inferenz und Training durchführen

### Rechnung mit der Parametermenge

Hugging Face Transformers ist die Standardbibliothek; die Dokumentation rechnet vor: Llama 2 7B benötigt bei voller Präzision (32 Bit pro Parameter, etwa zum Training) ca. $7 \cdot 4 \text{ GB} = 28$ GB VRAM, aber bei halber Präzision (16 Bit) ca. $7 \cdot 2 \text{ GB} = 14$ GB VRAM, passt also auf eine 16-GB-Consumer-GPU. Für Inferenz benötigt man keine Gradienten und keine Optimizer-Zustände → halber Platzbedarf, und mit 4-Bit-**Quantisierung** nochmal weniger: 8 GB oder darunter. Aber: Llama 2 70B ist erst in einer Liga mit GPT-4 → 80 bis 280 GB.

### Llamas & Co

* Llama (1, 2, 3) sind *open-weight*-Modelle mit verschiedenen Lizenzen – die Gewichte sind frei verfügbar, die Trainingsdaten nicht.
* Llama2-7B ist etwa 8,6 GB groß, passt also auf eine einfache Consumer-Grafikkarte.
* Llama3.3-70B braucht sehr viel VRAM oder rechnet langsam, ist dafür „in derselben Liga“ wie GPT-4.
* Llama3.1-405B verteilt man eher auf mehrere GPUs (vgl. auch GPT-3 mit ca. 175B Parametern).

### Llamas benutzen

Sofort ausprobieren mit **Ollama** ([Quickstart](https://github.com/ollama/ollama/blob/main/README.md#quickstart)): startet einen Webservice mit Chat-Interface und lädt Modelle selbst herunter. Ollama baut auf **llama.cpp** auf, bzw. auf Georgi Gerganovs `ggml`-Bibliothek, einer Transformer-Architektur-optimierten Deep-Learning-Bibliothek in C/C++ – die auf CPUs erstaunlich schnell ist. Eigenes Dateiformat **GGUF** für (quantisierte) Modelle. Achtung: Nicht immer sind die Chat/RLHF/Instruct-Modelle die geeigneten LLMs (z.B. für Code-Autocompletion à la Copilot oder RAG nimmt man eher die Basismodelle).

```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama run llama3.2:1b "Explain how LLMs work"
```

Das ist kein Deep Learning, das ist „Deep-Learning-Produkte benutzen“ – trotzdem super für Rapid Prototyping und jede Menge Anwendungen. Ollama bietet einen OpenAI-kompatiblen API-Endpoint, das verhindert Vendor Lock-in: Code, der gegen die OpenAI-API geschrieben ist, läuft mit einer Zeile Änderung lokal.

### Lokale LLMs benutzen (im Notebook)

`VL_11_llamacpp.ipynb` zeigt die Wege 1–3 und 10 mit `qwen2.5:0.5b` (nur ~300 MB, läuft auf der Laptop-CPU):

* **Embeddings** mit `ollama.embeddings(model=..., prompt=TEXT)`: Ein Text wird zu einem Vektor mit 896 Dimensionen.
* **Wahrscheinlichkeitsverteilungen** mit `llama_cpp.Llama(model_path=..., logits_all=True)`: Statt Text zu generieren, schauen wir uns die Logits für das nächste Token nach „The color of the sky is“ an, wenden Softmax an und lesen die Top-25 ab – und die Wahrscheinlichkeit für ` red`. Das ist die logistische Regression aus Kapitel 4, nur mit 150 000 Klassen.
* **Strukturierter Output**: Wir zwingen das LLM, JSON auszugeben, und nutzen `pydantic`, um zu garantieren, dass die Datentypen (Integer, String, …) stimmen: Aus „Yesterday I met Sabine. She is 29 years old, works as a doctor and loves her life in Munich.“ wird ein `Person(name, age, occupation, location)`-Objekt.

### Selbst Transformer finetunen

Finetuning ist auch sehr teuer, weil alle Parameter Gradienten und Optimizer-Zustände brauchen. Lösung: **Parameter-Efficient Finetuning** (PEFT) mit **Low-Rank Adaptations** (LoRA, [Conceptual Guide](https://huggingface.co/docs/peft/main/en/conceptual_guides/lora)): Die Gewichtsmatrizen $W$ bleiben eingefroren, und man lernt nur eine kleine Korrektur $\Delta W = AB$ mit $A \in \mathbb{R}^{n \times r}$, $B \in \mathbb{R}^{r \times m}$ und Rang $r \ll n, m$. Statt $n \cdot m$ Parametern sind das $r(n + m)$ – für $r = 8$ oft unter einem Prozent des Modells.

## Wie geht eigentlich … eine Anwendung?

Konkret eine Anwendung wie z.B. der „Chatbot“ [hAInrich](https://www.heicad.hhu.de/lehre/masters-programme-ai-and-data-science/hainrich) am HeiCAD: Retrieval-Augmented Generation (RAG) – Dokumente werden mit Weg 2 in Vektoren verwandelt und in einer Vektordatenbank abgelegt, zur Anfrage werden die ähnlichsten Dokumente gesucht und mit Weg 4 als Kontext in den Prompt eines LLM gegeben. Mehr dazu in Kapitel 13.

## Tipps zum Übungsblatt

Wir schauen rein, wenn dazu noch Zeit bleibt: das Kaggle-Notebook „PyTorch | Flowers | TransLearning + Ensemble | Test = 99.67 %“. Fragen, die wir klären wollen: Worum geht es da überhaupt? Was „ist“ Ensembling bzw. ein Ensemble-Modell? Was ist z.B. das Modell GoogLeNet von 2014, das da verwendet wird?
