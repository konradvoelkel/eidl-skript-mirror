---
title: "LLMs benutzen"
short_title: "LLMs benutzen"
---

# LLMs benutzen

## Transformer-LLMs in der Praxis einsetzen

Zur Erinnerung der Aufbau eines Transformers ([Kapitel „Transformer“](../part-representation-learning/18-transformer.md), Fig. 1 in „Attention is all you need“): Encoder- und Decoder-Stapel aus Attention- und MLP-Blöcken. Ein *Large Language Model* ist ein sehr großer, meist Decoder-only Transformer, der das nächste Token vorhersagt.

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
9. **Vorhersagen eines großen Modells in ein kleineres übertragen** (Destillation). Das schauen wir uns im [Kapitel „Destillation“](24-destillation.md) noch an; so lässt sich z.B. die Inferenz beschleunigen.
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

## Tipps zu Übungsblatt 11

Wir schauen rein, wenn dazu noch Zeit bleibt: das Kaggle-Notebook „PyTorch | Flowers | TransLearning + Ensemble | Test = 99.67 %“. Fragen, die wir klären wollen: Worum geht es da überhaupt? Was „ist“ Ensembling bzw. ein Ensemble-Modell? Was ist z.B. das Modell GoogLeNet von 2014, das da verwendet wird?
