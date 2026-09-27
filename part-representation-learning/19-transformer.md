---
title: "Transformer"
short_title: "Transformer"
---

# Transformer

## Transformer

### Historie: BLEU (2001)

Um Übersetzungsmodelle zu vergleichen, braucht man ein Maß. Papineni et al. (2001): „Human evaluations of machine translation are extensive but expensive. […] We propose a method of automatic machine translation evaluation that is quick, inexpensive, and language-independent, that correlates highly with human evaluation.“ Die Grundidee: „The closer a machine translation is to a professional human translation, the better it is.“

Der **BLEU-Score** (bilingual evaluation understudy) zwischen 0 und 1 (auch skaliert 0–10 oder 0–100) ist das geometrische Mittel aus den $n$-Gramm-Präzisionsscores der Maschinenübersetzung relativ zu einer menschlichen Referenzübersetzung, multipliziert mit einem Strafterm für abweichende Übersetzungslänge (*brevity penalty*). Die $n$-Gramm-Präzision ist die Anzahl (mit Mehrfachzählung, aber gedeckelt durch die Referenz) der $n$-Gramme, die in der Maschinenübersetzung vorkommen und in der Referenzübersetzung, normiert mit der Anzahl der $n$-Gramme der Maschinenübersetzung. Für BLEU ist $n = 1, 2, 3, 4$ üblich.

### Historie: NeurIPS 2017

Vaswani et al., *Attention is all you need*: „The dominant sequence transduction models are based on complex recurrent or convolutional neural networks in an encoder-decoder configuration. The best performing models also connect the encoder and decoder through an attention mechanism. We propose a new simple network architecture, the Transformer, based solely on attention mechanisms, dispensing with recurrence and convolutions entirely. […] Our model achieves 28.4 BLEU on the WMT 2014 English-to-German translation task, improving over the existing best results, including ensembles by over 2 BLEU. […] a new single-model state-of-the-art BLEU score of 41.8 after training for 3.5 days on eight GPUs.“

Zur Einordnung: WMT = Workshop on Statistical Machine Translation, Task und Datensatz; aktuell WMT23 als Challenge; sacreBLEU als Standard-Implementierung; 41.8 „BLEU“ = 0,418 BLEU. Und das WMT19-Modell aus dem [Kapitel „Vortrainierte Modelle“](../part-grundlagen/04-vortrainierte-modelle.md) ist genau ein Nachfolger davon.

### Transformer technisch

Der Aufbau (Fig. 1 in „Attention is all you need“): ein **Encoder**-Stapel und ein **Decoder**-Stapel, beide aus identischen Blöcken mit Multi-Head Self-Attention, einem MLP, Residual Connections und Layer-Normalisierung. Anstelle von Rekurrenz bekommt jedes Token eine **Positionskodierung** addiert. Der Kern ist die **Attention**:

$$
\operatorname{Attention}(Q, K, V) = \operatorname{sm}\!\left( \frac{Q K^T}{\sqrt{d_k}} \right) V ,
$$

wobei Queries $Q$, Keys $K$ und Values $V$ lineare Projektionen der Token-Vektoren sind: Jedes Token „fragt“ mit seiner Query alle anderen Tokens, vergleicht sie mit deren Keys (Skalarprodukt, Softmax $\to$ Gewichte) und sammelt eine gewichtete Summe ihrer Values ein. Das ist eine Schicht, in der jedes Token von jedem anderen abhängt – ohne Reihenfolge, daher die Positionskodierung – und die vollständig parallel berechnet werden kann. Wir implementieren keine Transformer in dieser Vorlesung; in VL 11 benutzen wir sie.

Das Architekturbild ist Figure 1 in Vaswani et al., *Attention Is All You Need* ([arXiv:1706.03762](https://arxiv.org/abs/1706.03762)): links der Encoder-Stapel, rechts der Decoder-Stapel, dazwischen die Cross-Attention. Eine annotierte, ausführbare Fassung ist [The Annotated Transformer](https://nlp.seas.harvard.edu/annotated-transformer/).

### Konkrete Modelle mit Transformern

**GPT** (Generative Pretrained Transformer): Trainiert unsupervised auf gigantischen Textmassen (präziser: self-supervised); BPE (Byte Pair Encoding) als Tokenization-Schema; sehr große Modelle (= sehr viele Layer, sehr viele Parameter); gelernte Positionskodierung, begrenzter Kontext; **Decoder-only**: das nächste Token vorhersagen. Varianten: GPT-2, GPT-J, GPT-NeoX, Llama 1/2/3, und nichtöffentlich GPT-3, 3.5, 4, etc.

**Byte Pair Encoding (BPE)**: ein Tokenization-Schema (Gage 1994). BPE baut auf einem Tokenizer auf, meist Token = Byte oder Character. Algorithmus:

1. Sortiere alle möglichen Tokenpaare nach Häufigkeit,
2. verschmelze die zwei häufigsten zu einem neuen Token,
3. Ende, wenn es genug verschiedene Token gibt.

Die Vokabulargröße bei GPT-4s BPE „tiktoken“ ist z.B. 100 256; durchschnittlich entspricht ein Token etwa 4 Bytes. Häufige Wörter werden zu einem Token, seltene in Silben oder Buchstaben zerlegt – das ist die „flexible $n$“-Antwort auf die Tokenisierungsfrage aus dem letzten Kapitel.

**NanoGPT**: Visualisierung und Erklärung, Layer für Layer, von Brendan Bycroft: [bbycroft.net/llm](https://bbycroft.net/llm).

**BERT** (Bidirectional Encoder Representations from Transformers): **Encoder-only** (nicht zwangsläufig generativ); Tokenization auf Subwort-Level (WordPiece); Training mit 2 Tasks: Masked Language Modeling (ähnlich wie bei word2vec, aber mit Kontext in beide Richtungen) und „nächsten Satz vorhersagen“. Bei gleicher Modellgröße besser als GPT für manche Tasks (Klassifikation, Embeddings). Varianten: RoBERTa, ALBERT, DistilBERT.

**ViT** (Vision Transformer, Dosovitskiy et al., „An Image is Worth 16x16 Words“): Das Bild wird grob gerastert in „Patches“ aufgeteilt; jeder Patch (= Token) wird in einen Vektor umgewandelt; Positionskodierung für 2D-Position statt 1D wie bei Text; ansonsten „klassischer“ Transformer. Für Klassifikationsaufgaben manchmal besser als CNNs.

### Implementierung des Transformers

Alexander Rush et al.: *The Annotated Transformer* (updated 2022 edition) – der Artikel „Attention is all you need“ zusammen mit Codeschnipseln und einigen Kommentaren. Für Verrückte oder sehr Interessierte: „I made a transformer by hand (no training!)“ von Theia Vogel, mit sorgfältig von Hand bestimmten Gewichten – die Fortsetzung unseres „Parameter von Hand wählen“ aus Kapitel 7.

## Übung

Drei Token mit Query-Key-Skalarprodukten $q \cdot k_1 = 2$, $q \cdot k_2 = 2$,
$q \cdot k_3 = 0$ und Values $v_1 = 1$, $v_2 = 3$, $v_3 = 10$.

1. Berechnen Sie die Attention-Gewichte mit Softmax (ohne Skalierung) und daraus die
   Ausgabe.
   *Tipp: Zwei der drei Exponenten sind gleich; $e^2 \approx 7{,}39$.*
2. Die Gewichte müssen sich zu 1 summieren — prüfen Sie das nach.
3. Warum braucht ein Transformer Positionsembeddings, ein RNN aber nicht?

*Antwortprobe: Die Ausgabe liegt näher an 3 als an 10.*

:::{admonition} Weiterlesen
:class: seealso
Prince, *UDL*, Kap. 12 (Transformers). Beide Bücher sind frei verfügbar, siehe [Über dieses Skript](../README.md).
:::
