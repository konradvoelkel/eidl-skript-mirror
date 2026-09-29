---
title: "LLMs benutzen"
short_title: "LLMs benutzen"
downloads:
  - file: ../notebooks/latent-classifier.ipynb
    title: "latent-classifier.ipynb (Klassifikation im latenten Raum, Dreaming, Saliency)"
---

# LLMs benutzen

## Transformer-LLMs in der Praxis einsetzen

Zur Erinnerung der Aufbau eines Transformers ([Kapitel „Transformer“](../part-representation-learning/19-transformer.md), Fig. 1 in „Attention is all you need“): Encoder- und Decoder-Stapel aus Attention- und MLP-Blöcken. Ein *Large Language Model* ist ein sehr großer, meist Decoder-only Transformer, der das nächste Token vorhersagt.

### Verschiedene Wege, LLMs zu nutzen

Wir konkretisieren anhand eines Beispiel-Tasks, z.B. „Gegeben einen Text, identifiziere, ob er emotional positiv oder negativ gefärbt ist“ (Sentiment-Analyse).

1. **Wort-Vektor-Einbettungen direkt verwenden** (statt word2vec z.B. die Embedding-Schicht von Gemma) $\to$ semantische Ähnlichkeit, semantische Suche, semantisches Clustering etc. Pro: sehr billig (keine tiefen Modelle für Inferenz notwendig). Contra: Zusammenhänge über längere Texte hinweg nicht sichtbar.
2. **Satz-Vektor-Einbettungen**, bzw. längere Texte in Vektoren umwandeln (z.B. mit BERT). Pro: sehr hohe Qualität der Repräsentationen. Contra: LLM notwendig zur Berechnung der Repräsentationen. (Das Notebook `latent-classifier.ipynb` – Download oben auf dieser Seite – baut genau das: BERT-Embeddings als Features für einen Klassifikator.)
3. **Nicht Token sampeln, sondern die Verteilung der Ausgabetoken direkt betrachten.** Pro: vollständige Information aus dem LLM, kein „zufälliges“ Sampling. Contra: weniger intuitiv zu verwenden, man arbeitet mit Verteilungen im Latent Space statt mit Text.
4. **Fertig trainierte Transformer mit bestimmten Prompts verwenden**, z.B. „Analog zur Transformation [A] $\to$ [B] verarbeite [C]“ (*one-shot prompt*), etwa [A] = Text auf Englisch, [B] = Text auf Deutsch, [C] = neuer Text auf Englisch. Pro: extrem vielseitig und bisher sehr, sehr erfolgreich. Contra: benötigt viele Token (noch mehr für *few-shot prompts*).
5. **Transformer von Grund auf trainieren** (eigenes Pretraining). Pro: vollständige Kontrolle über Trainingsdaten und damit prinzipiell über Outputs. Contra: extrem teuer; Llama 2 (etwa auf dem Niveau von Gemini 1 Pro / ChatGPT 3.5) kostete ca. 2–10 Mio. $.
6. **Vortrainierte Transformer auf besonderen Daten weiter trainieren** (Finetuning). Pro: relativ billig (keine sehr langen Trainingszeiten = Stromkosten nötig). Contra: benötigt wenigstens Hardware zum Training (teurer für größere Modelle).
7. **Transformer-Modell auf Chat-Formate finetunen mit RLHF** (Reinforcement Learning from Human Feedback, wie bei ChatGPT). Pro: Feedback führt zu Qualitätssteigerung, z.B. NSFW-Removal o.ä. Contra: etwas komplizierter als „einfaches“ Training.
8. **Sehr große Modelle über eine API verwenden** (ggf. nur Sampling-Output). Der De-facto-Standard für die „meisten“ LLM-Use-Cases für Softwareentwickler.
9. **Vorhersagen eines großen Modells in ein kleineres übertragen** (Destillation). Das schauen wir uns im [Kapitel „Destillation“](25-destillation.md) noch an; so lässt sich z.B. die Inferenz beschleunigen.
10. **Constrained Generation**: Ausgabe sampeln, die einem (z.B. JSON-)Schema genügt – ein wesentlicher Baustein für „agentische Workflows“.

## Selbst Inferenz und Training durchführen

### Rechnung mit der Parametermenge

Hugging Face Transformers ist die Standardbibliothek; die Faustrechnung geht so. Allein die **Gewichte** von Llama 2 7B belegen bei 32 Bit pro Parameter $7 \cdot 4 \text{ GB} = 28$ GB, bei 16 Bit $7 \cdot 2 \text{ GB} = 14$ GB und mit 4-Bit-**Quantisierung** noch $7 \cdot \tfrac12 \text{ GB} \approx 3{,}5$ GB. Für **Inferenz** kommt darüber hinaus nur wenig dazu (Aktivierungen und der KV-Cache), 16 Bit passen also auf eine 16-GB-Consumer-GPU und 4 Bit auf fast alles. Beim **Training** dagegen braucht jeder Parameter zusätzlich einen Gradienten und die Zustände des Optimierers – bei Adam zwei Momente, zusammen grob das Vierfache der Gewichte. Nicht die Inferenz ist also das Problem auf Consumer-Hardware, sondern das Training. Llama 2 70B ist erst in einer Liga mit GPT-4, und dessen Gewichte allein sind 35 GB (4 Bit) bis 280 GB (32 Bit).

### Llamas & Co

* Llama (1, 2, 3) sind *open-weight*-Modelle mit verschiedenen Lizenzen – die Gewichte sind frei verfügbar, die Trainingsdaten nicht.
* Llama 2 7B ist als fp16-Download 13,5 GB groß (das sind die $7 \cdot 2$ GB von oben); als 4-Bit-GGUF sind es gut 4 GB, und damit passt es auf eine einfache Consumer-Grafikkarte.
* Llama3.3-70B braucht sehr viel VRAM oder rechnet langsam, ist dafür „in derselben Liga“ wie GPT-4.
* Llama3.1-405B verteilt man eher auf mehrere GPUs (vgl. auch GPT-3 mit ca. 175B Parametern).

### Llamas benutzen

Sofort ausprobieren mit **Ollama** ([Quickstart](https://github.com/ollama/ollama/blob/main/README.md#quickstart)): startet einen Webservice mit Chat-Interface und lädt Modelle selbst herunter. Ollama baut auf **llama.cpp** auf, bzw. auf Georgi Gerganovs `ggml`-Bibliothek, einer Transformer-Architektur-optimierten Deep-Learning-Bibliothek in C/C++ – die auf CPUs erstaunlich schnell ist. Eigenes Dateiformat **GGUF** für (quantisierte) Modelle. Achtung: Nicht immer sind die Chat/RLHF/Instruct-Modelle die geeigneten LLMs (z.B. für Code-Autocompletion à la Copilot oder RAG nimmt man eher die Basismodelle).

```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama run llama3.2:1b "Explain how LLMs work"
```

Das ist kein Deep Learning, das ist „Deep-Learning-Produkte benutzen“ – trotzdem super für Rapid Prototyping und jede Menge Anwendungen. Ollama bietet einen OpenAI-kompatiblen API-Endpoint, das verhindert Vendor Lock-in: Code, der gegen die OpenAI-API geschrieben ist, läuft mit einer Zeile Änderung lokal.

### Lokale LLMs benutzen: Wege 2, 3 und 10 in Code

Wir probieren die Wege 2, 3 und 10 mit `qwen2.5:0.5b` aus – knapp 400 MB, läuft auf der Laptop-CPU. Vorbereitung im Terminal:

```bash
ollama pull qwen2.5:0.5b
ollama run qwen2.5:0.5b     # interaktiver Chat, mit /bye beenden
pip install ollama llama-cpp-python pydantic
```

Ein erster Test im Chat: „Wie kann man mit Deep Learning Hunde von Katzen unterscheiden (also, warum funktioniert das)? Zähle nur 5–10 Stichpunkte auf.“ Lesen und amüsieren – 0,5 Milliarden Parameter sind eben nicht 50 Milliarden; auf Englisch fällt die Antwort meist besser aus. Ollama läuft danach als Server auf Port 11434 (`http://localhost:11434` zeigt „Ollama is running“, unter `/v1/models` steht das Modell).

**Weg 2, Embeddings.** Ein Text wird zu einem Vektor fester Länge (bei Qwen 2.5 0.5B: 896 Dimensionen), ideal für semantische Suche oder als Feature für einen Klassifikator:

```python
import ollama, numpy as np

response = ollama.embeddings(model="qwen2.5:0.5b", prompt="Heute ist es kalt draußen.")
vector = np.array(response["embedding"])
print(vector.shape, np.linalg.norm(vector))     # (896,)  ~300
```

**Weg 3, die Verteilung des nächsten Tokens.** Statt Text zu generieren, schauen wir uns die Logits an. Dafür nehmen wir llama.cpp direkt (den Python-Wrapper `llama_cpp`) und das Modell als GGUF-Datei von [huggingface.co/Qwen/Qwen2.5-0.5B-Instruct-GGUF](https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct-GGUF) (Variante `q4_k_m`, 491 MB):

```python
from llama_cpp import Llama
import numpy as np

llm = Llama(model_path="qwen2.5-0.5b-instruct-q4_k_m.gguf", logits_all=True, n_ctx=512, verbose=False)

def next_token_probs(text):
    llm.reset()
    tokens = llm.tokenize(text.encode("utf-8"))
    llm.eval(tokens)
    logits = np.array(llm.scores[len(tokens) - 1])   # Logits an der letzten Position
    return np.exp(logits) / np.sum(np.exp(logits))    # Softmax

probs = next_token_probs("The color of the sky is")
print(probs.shape)                                   # (151936,) -- die Vokabulargröße
for i in np.argsort(probs)[-5:][::-1]:
    print(repr(llm.detokenize([i]).decode()), f"{probs[i]:.2%}")
# ' changing' 10.3%, ' always' 6.7%, ' blue' 4.0%, ' a' 3.2%, ' determined' 3.0%
red = llm.tokenize(b" red")[0]
print(f"{probs[red]:.2%}")                           # 0.72%
```

Das ist die logistische Regression aus dem [Kapitel „Logistische Regression“](../part-lernen/06-logistische-regression.md) – Softmax über Logits –, nur mit 150 000 Klassen; alles aus dem [Kapitel „Latente Räume geometrisch“](23-latente-raeume.md) über Sampling-Strategien und Temperatur setzt genau hier an. (Bei `llm.scores` gibt es einen Fallstrick: Das Array hat immer `n_ctx` Zeilen, `scores[-1]` wäre also die falsche Position.)

**Weg 10, strukturierter Output.** Wir zwingen das LLM, JSON auszugeben, und nutzen `pydantic`, um zu garantieren, dass die Datentypen stimmen:

```python
from pydantic import BaseModel
import ollama

class Person(BaseModel):
    name: str
    age: int
    occupation: str
    location: str

text = "Yesterday I met Sabine. She is 29 years old, works as a doctor and loves her life in Munich."
response = ollama.chat(
    model="qwen2.5:0.5b", format="json",
    messages=[{"role": "user", "content":
        f"Extract information about the person from this text into JSON using {list(Person.model_fields)}: {text}"}],
)
person = Person.model_validate_json(response["message"]["content"])
print(person)   # name='Sabine' age=29 occupation='doctor' location='Munich'
```

`format="json"` ist *constrained generation*: Beim Sampling werden nur Token zugelassen, die die Ausgabe syntaktisch gültig halten. Die Validierung mit `pydantic` prüft danach, ob auch die Typen stimmen (`age` ist wirklich ein `int`) – erst damit wird die Ausgabe eines LLM zu etwas, worauf man Software bauen kann.

### Selbst Transformer finetunen

Finetuning ist auch sehr teuer, weil alle Parameter Gradienten und Optimizer-Zustände brauchen. Lösung: **Parameter-Efficient Finetuning** (PEFT) mit **Low-Rank Adaptations** (LoRA, [Conceptual Guide](https://huggingface.co/docs/peft/main/en/conceptual_guides/lora)): Die Gewichtsmatrizen $W$ bleiben eingefroren, und man lernt nur eine kleine Korrektur $\Delta W = AB$ mit $A \in \mathbb{R}^{n \times r}$, $B \in \mathbb{R}^{r \times m}$ und Rang $r \ll n, m$. Statt $n \cdot m$ Parametern sind das $r(n + m)$ – für $r = 8$ oft unter einem Prozent des Modells.

## Wie geht eigentlich … eine Anwendung?

Konkret eine Anwendung wie z.B. der „Chatbot“ [hAInrich](https://www.heicad.hhu.de/lehre/masters-programme-ai-and-data-science/hainrich) am HeiCAD: Retrieval-Augmented Generation (RAG) – Dokumente werden mit Weg 2 in Vektoren verwandelt und in einer Vektordatenbank abgelegt, zur Anfrage werden die ähnlichsten Dokumente gesucht und mit Weg 4 als Kontext in den Prompt eines LLM gegeben. Mehr dazu im [Kapitel „Anwendungsbeispiele“](24-anwendungsbeispiele.md).

## Ausblick: Transfer Learning und Ensembles

Wir schauen rein, wenn dazu noch Zeit bleibt: das Kaggle-Notebook „PyTorch | Flowers | TransLearning + Ensemble | Test = 99.67 %“. Fragen, die wir klären wollen: Worum geht es da überhaupt? Was „ist“ Ensembling bzw. ein Ensemble-Modell? Was ist z.B. das Modell GoogLeNet von 2014, das da verwendet wird?
