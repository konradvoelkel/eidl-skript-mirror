---
title: "VL 09: Representation Learning, RNNs und Transformer"
short_title: "VL 09"
---

# Representation Learning, RNNs und Transformer

:::{warning} Rohfassung
Dieses Kapitel ist eine automatische Transkription der Folien von VL 09 aus dem WiSe 2025/26
(`from_2025/slides/Einführung in Deep Learning 2025_26 VL 09_ Representation Learning.pdf`), Folie für Folie in der Originalreihenfolge.
Formeln und Abbildungen sind dabei größtenteils verloren gegangen; der Text ist noch nicht überarbeitet.
:::

## Variationen von word2vec

<!-- Folie 2 -->

## Word2vec (Wiederholung)

<!-- Folie 3 -->
Kernidee
Die Semantik eines Wortes ergibt sich durch seine Nutzung in Sätzen.
Beispiel:
“Die [MASK] frisst ihr Futter am liebsten aus dem goldenen Napf”
kommt in Texten mit [MASK]=Katze und [MASK]=Hündin vor.
Machine Learning Task, unsupervised: (CBOW)
Gegeben Text, ersetze ein Wort durch [MASK],
lasse vorhersagen was [MASK] ist (wie ein Denoising Autoencoder).

## word2vec

<!-- Folie 4 -->
CBOW
K
N
N
K
K
K
N
Grafik von Lilian
Weng, “Learning
Word Embedding”
2017, Blog post

## Representation Learning

<!-- Folie 5 -->

<!-- Folie 6 -->
Worum geht’s?
Gegeben Daten, die einer unbekannten
Verteilung folgen, wollen wir automatisch
Features entwickeln, die spätere Aufgaben
mit diesen Daten erleichtern.
Spätere Aufgaben:
◼
◼
◼
Die Verteilung schätzen (daraus
sampeln können, z.B. Text generieren)
Klassifikation
(z.B. Spam/Ham)
Ähnlichkeit bestimmen
(z.B. zwischen 2 Texten)

<!-- Folie 7 -->
Worum geht’s?
Gegeben Daten, die einer unbekannten
Verteilung folgen, wollen wir automatisch
Features entwickeln, die spätere Aufgaben
mit diesen Daten erleichtern.
Oberste Ziele sind eine höhere
Modellperformance (für die späteren
Aufgaben) und bessere Generalisierbarkeit.
Spätere Aufgaben:
◼
◼
◼
Die Verteilung schätzen (daraus
sampeln können, z.B. Text generieren)
Klassifikation
(z.B. Spam/Ham)
Ähnlichkeit bestimmen
(z.B. zwischen 2 Texten)

<!-- Folie 8 -->
Worum geht’s?
Gegeben Daten, die einer unbekannten
Verteilung folgen, wollen wir automatisch
Features entwickeln, die spätere Aufgaben
mit diesen Daten erleichtern.
Spätere Aufgaben:
◼
◼
◼
Oberste Ziele sind eine höhere
Modellperformance (für die späteren
Aufgaben) und bessere Generalisierbarkeit.
Ein weiteres Ziel ist möglicher Transfer.
(Beispiel: Übersetzungen)
Die Verteilung schätzen (daraus
sampeln können, z.B. Text generieren)
Klassifikation
(z.B. Spam/Ham)
Ähnlichkeit bestimmen
(z.B. zwischen 2 Texten)

<!-- Folie 9 -->
Worum geht’s?
Gegeben Daten, die einer unbekannten
Verteilung folgen, wollen wir automatisch
Features entwickeln, die spätere Aufgaben
mit diesen Daten erleichtern.
Spätere Aufgaben:
◼
◼
◼
Die Verteilung schätzen (daraus
sampeln können, z.B. Text generieren)
Klassifikation
(z.B. Spam/Ham)
Ähnlichkeit bestimmen
(z.B. zwischen 2 Texten)
Oberste Ziele sind eine höhere
Modellperformance (für die späteren
Aufgaben) und bessere Generalisierbarkeit.
Ein weiteres Ziel ist möglicher Transfer.
(Beispiel: Übersetzungen)
Wie genau?
◼
◼
Dimensionsreduktion durch
“intelligentes Downsampling”,
Kompression (wie Autoencoder)
Nichtlineare neue Features aus alten
Features entwickeln

<!-- Folie 10 -->
Andere Features, die man manuell hinzufügen kann:
◼
Spektrogramm einer Audiodatei
So wird eine Waveform-Datei
(z.B. eine Unterhaltung, ein Song)
in ein Bild umgewandelt,
indem die Fourier-Transformation genutzt
wird.
→ Relevant für Sprachsynthese und
Spracherkennung
◼
Enthält ein Bild horizontale Kanten?
Vertikale Kanten? Ecken?
Ein Klassifikator für
“Das Bild enthält ein Haus” ist leichter zu
trainieren, wenn nicht nur Pixelwerte
eingehen, sondern auch die Positionen von
Ecken und Kanten.
→ Betrachten wir noch: CNNs
(convolutional neural networks),
die automatische Variante davon

## node2vec

<!-- Folie 11 -->

<!-- Folie 12 -->
word2vec aus anderer Perspektive
Ein Satz, wie er bei word2vec eingeht,
kann als linearer Graph modelliert werden:
Die
Katze
frisst
Mäuse
Mehrere Sätze können gleiche Worte
enthalten, damit bilden mehrere Sätze
größere Graphen mit linearen Teilgraphen

<!-- Folie 13 -->
word2vec aus anderer Perspektive
Ein Satz, wie er bei word2vec eingeht,
kann als linearer Graph modelliert werden:
Die
Katze
Mäuse
frisst
Der
Hund
Leckerli
Mehrere Sätze können gleiche Worte
enthalten, damit bilden mehrere Sätze
größere Graphen mit linearen Teilgraphen

<!-- Folie 14 -->
word2vec aus anderer Perspektive
Ein Satz, wie er bei word2vec eingeht,
kann als linearer Graph modelliert werden:
Die
Katze
Mäuse
Mit diesem Graph allein lassen sich die
Sätze nicht zurückgewinnen, denn
“Der Hund frisst Mäuse” sowie
“Die Katze frisst Leckerli”
sind keine ursprünglichen Sätze.
frisst
Der
Hund
Leckerli
Mehrere Sätze können gleiche Worte
enthalten, damit bilden mehrere Sätze
größere Graphen mit linearen Teilgraphen

<!-- Folie 15 -->
word2vec aus anderer Perspektive
Ein Satz, wie er bei word2vec eingeht,
kann als linearer Graph modelliert werden:
Die
Katze
Mäuse
Mit diesem Graph allein lassen sich die
Sätze nicht zurückgewinnen, denn
“Der Hund frisst Mäuse” sowie
“Die Katze frisst Leckerli”
sind keine ursprünglichen Sätze.
frisst
Der
Hund
Leckerli
Mehrere Sätze können gleiche Worte
enthalten, damit bilden mehrere Sätze
größere Graphen mit linearen Teilgraphen
Besser: probabilistisches Modell
auf Grundlage des Graphen,
für jeden Knoten x eine
Wahrscheinlichkeitsverteilung auf den
Knoten y mit Kante x→y, abhängig von der
vorherigen Kante z→x.
(Markovkette)

<!-- Folie 16 -->
Aus anderer Perspektive
Gegeben ein Graph
Die
Katze
Mäuse
frisst
Der
Hund
Leckerli
lassen sich daraus “Sätze” bilden durch
wiederholtes Verfolgen einer ausgehenden
Kante.

<!-- Folie 17 -->
Aus anderer Perspektive
Gegeben ein Graph
Die
Katze
Mäuse
Vereinfachtes Probabilistisches Modell
auf Grundlage des Graphen:
für jeden Knoten x eine Gleichverteilung auf
den Knoten y mit Kante x→y,
unabhängig von der vorherigen Kante z→x.
frisst
Der
Hund
Leckerli
lassen sich daraus “Sätze” bilden durch
wiederholtes Verfolgen einer ausgehenden
Kante.

<!-- Folie 18 -->
Aus anderer Perspektive
Gegeben ein Graph aus der Wikipedia
Katze
Sendung
mit der
Maus
Mäuse
Vereinfachtes Probabilistisches Modell
auf Grundlage des Graphen:
für jeden Knoten x eine Gleichverteilung auf
den Knoten y mit Kante x→y,
unabhängig von der vorherigen Kante z→x.
Maus
Lesk
LeskAlgorithmus
Computer
maus
lassen sich daraus endliche Random Walks
bilden durch wiederholtes Verfolgen einer
ausgehenden Kante.
Ziel:
Verstehe einen Knoten durch seinen
Kontext
Beispiel: Haushund und Hausmaus haben
gemeinsame eingehende Links

<!-- Folie 19 -->
Praktisch
Beispielanwendungen:
Bei node2vec haben wir 2 Schritte:
1.
2.
◼
Generiere “Sätze” (Knoten, [Kontext])
durch Random Walks auf dem
Graphen
Benutze word2vec skip-gram Training
auf den Sätzen
Schritt 1 ist sehr ressourcenintensiv,
kann aber parallelisiert werden.
◼
https://www.kaggle.com/code/himj26/recom
medations-using-node2vec
Aus einem Netflix Datensatz werden
Serien und Filme sowie deren Genres
extrahiert und zu einem bipartiten
Graph gebaut:
Titel -> Genre
Nach node2vec kann man zu einem
Titel im Latent Space nach ähnlichen
Titeln suchen.
https://www.kaggle.com/code/ferdzso/knowl
edge-graph-analysis-with-node2vec
Ähnlich, mehr Klassen von Knoten

## wordnode2vec

<!-- Folie 20 -->
skip-gram
K
N
N
K
Grafik von Lilian
Weng, “Learning
Word Embedding”
2017, Blog post
K
N
K
N

## node2vec

<!-- Folie 21 -->
Praktisch
Software für Schritt 1:
Bei node2vec haben wir 2 Schritte:
◼
https://stellargraph.readthedocs.io/en/stable/demos
/link-prediction/node2vec-link-prediction.html
OK API, nutzt gensim
1.
2.
Generiere “Sätze” (Knoten, [Kontext])
durch Random Walks auf dem
Graphen
Benutze word2vec skip-gram Training
auf den Sätzen
Schritt 1 ist sehr ressourcenintensiv,
kann aber parallelisiert werden.
◼
◼
https://arxiv.org/abs/1805.00280
Schnelle Impl mit Apache Spark
https://pytorch-geometric.readthedocs.io/en/latest/gener
ated/torch_geometric.nn.models.Node2Vec.html
Modul für PyTorch
Siehe auch
https://github.com/pyg-team/pytorch_geome
tric/blob/master/examples/node2vec.py

## Wie könnte wav2vec aussehen?

<!-- Folie 22 -->

## Graph Neural Networks

<!-- Folie 23 -->

## GNNs

<!-- Folie 24 -->
Etwas anderes
Anstatt die Struktur des Graphen in (Knoten, Kontext)-Paare zu
entwickeln, lässt sich die Struktur des Graphen auch direkt im
neuronalen Netz nutzen.
Kaffee
Beispiel:
Mühle
Tee
Kanne
Tasse
Kaffee
Tee
Kanne
Tasse
Mühle
“Message Passing”

## Recurrent Neural Networks

<!-- Folie 25 -->

## RNNs

<!-- Folie 26 -->
Recurrent Neural Networks, Rekurrente neuronale Netze
Input:
Ein linearer Strom von Daten, z.B. Text,
Audio, Video oder andere Zeitreihen.
Output:
Irgendeine vektorielle oder skalare Größe
z.B. Vorhersage des nächsten Wortes
Idee:
Zum Zeitpunkt t nicht nur die neuen Daten
von t sondern auch die Ergebnisse aus den
Daten von t-1 verwenden, um zum
Ergebnis zu kommen.
Ein rekurrentes Neuron:
“Entfaltete Perspektive”:
→ LSTMs

## Historie: Rekurrente Netze

<!-- Folie 27 -->
RNNs
Quelle: CC-BY-SA 4.0 Wikipedia User Fdeloche 2017
1982: Hopfield Netzwerk
1985: Boltzmann Machine (Hinton, Sejnowksi)
1980s: RNNs
1991: Schmidthuber’s frühe Attention
1990s: Gated RNNs
1997: LSTM (Hochreiter, Schmidthuber)
2014: GRUs (Cho, Bengio et al.)
2017: Transformer (Vaswani et al.)
Im Gegensatz zur Finite Impulse Response (FIR) eines CNNs (machen wir noch),
ist ein RNN ein Infinite Impulse Response (IIR) Signalverarbeiter.

## Trick: Skip Connections

<!-- Folie 28 -->
Auch bekannt als: Residual Connections
Anstatt x(m) = f𝜗(x(m-1)) (z.B. f=MLP)
Parametrisiere x(m) = x(m-1) + res(x(m-1))
Und berechne res(x(m-1)) = f𝜗(x(m-1))
Idee: Jeder Layer ist nah dran an “nichts ändern” (Identität)
Hilft gegen verschwindende oder explodierende Gradienten.

## Historie: Rekurrente Netze

<!-- Folie 29 -->
Gated RNNs (Gated Recurrent Unit, GRU)
Quelle: CC-BY-SA 4.0 Wikipedia User Jeblad 2018

<!-- Folie 30 -->
Gated RNNs (Gated Recurrent Unit, GRU)
Output = hidden state
Kandidat für hidden state
Hidden
state
Update gate output
Input
Quelle: CC-BY-SA 4.0 Wikipedia User Jeblad 2018
Reset gate output

<!-- Folie 31 -->
LSTM (long short-term memory)
Quelle: CC-BY-SA 4.0 Wikipedia User Guillaume Chevalier 2018

<!-- Folie 32 -->
LSTM (long short-term memory)
Cell state
(long term memory)
Hidden state = output
(short term memory)
3 gates (sigmoids):
forget, input, output
Quelle: CC-BY-SA 4.0 Wikipedia User Guillaume Chevalier 2018
Mehr Erklärungen:
Shi Yan @ MLReview:
Understanding LSTM and its diagrams

<!-- Folie 33 -->
LSTM (long short-term memory)
Bill Gates (2018):
“huge milestone in advancing artificial intelligence”
weil OpenAI mit LSTMs Dota 2 gewann.
Auch mit LSTMs gebaut:
AlphaStar von Google DeepMind,
spielt StarCraft 2 (2019)

## LSTM praktisch

<!-- Folie 34 -->
Mit PyTorch
import torch.nn as nn
class MyModel(nn.Module):
def __init__(self, ...):
self.lstm = nn.LSTM(embedding_length,
hidden_size)
self.label = nn.Linear(hidden_size,
output_size)
def forward(self, x):
h, c = self.lstm(x)
return self.label(h)

## Am Rande: Konkatenieren vs. Summe

<!-- Folie 35 -->
Wenn wir zwei verschiedene
Eingabevektoren in einer Schicht
verarbeiten wollen, ist es naheliegend,
diese zu einem längeren Vektor zu
konkatenieren.
Oft sehen wir aber im Code stattdessen ein
einfaches +
Wie kann das funktionieren???

<!-- Folie 36 -->
Wenn wir zwei verschiedene
Eingabevektoren in einer Schicht
verarbeiten wollen, ist es naheliegend,
diese zu einem längeren Vektor zu
konkatenieren.
Oft sehen wir aber im Code stattdessen ein
einfaches +
Wie kann das funktionieren???
Eine einfachere Frage:
Unter welchen Umständen lässt sich für
zwei Vektoren v,w ∊ ℝn aus der Summe
v+w ∊ ℝn
wieder das Paar (v,w) rekonstruieren?
Probieren Sie explizite Beispiele mit n=2
aus, etwa v=(3,0) und w=(1,1).
Überlegen Sie hinterher, wie das bei der
eigentlichen Frage weiterhilft.

## Transformer - Historie

<!-- Folie 37 -->

## Historie: BLEU (2001)

<!-- Folie 38 -->
Abstract
Human evaluations of machine translation are extensive but expensive.
Human evaluations can take months to finish and involve human labor
that can not be reused. We propose a method of automatic machine
translation
evaluation
that
is
quick,
inexpensive,
and
language-independent, that correlates highly with human evaluation, and
that has little marginal cost per run. We present this method as an
automated understudy to skilled human judges which substitutes for
them when there is need for quick or frequent evaluations.

<!-- Folie 39 -->
“The closer a machine translation is to a professional human translation, the better it is”
Der BLEU Score zwischen 0 und 1
(auch skaliert 0 - 10 oder 0 - 100)
ist das arithmetische Mittel aus den
n-gram Präzisionsscores der MaschinenÜbersetzung relativ zu einer menschlichen
Referenzübersetzung,
multipliziert mit einem Strafterm für
abweichende Übersetzungslänge
(“brevity penalty”).
N-Gram Präzision =
Anzahl (mit Mehrfachzählung) der
n-Gramme, die in der MaschinenÜbersetzung vorkommen und in der
Referenzübersetzung, normiert mit der
Anzahl der n-Gramme der MaschinenÜbersetzung.
Für BLEU mit n=1,2,3,4 üblich.

## Historie: NeurIPS 2017

<!-- Folie 40 -->

<!-- Folie 41 -->
The dominant sequence transduction models are based on complex
recurrent or convolutional neural networks in an encoder-decoder
configuration. The best performing models also connect the encoder and
decoder through an attention mechanism. We propose a new simple
network architecture, the Transformer, based solely on attention
mechanisms, dispensing with recurrence and convolutions entirely.
Experiments on two machine translation tasks show these models to be
superior in quality while being more parallelizable and requiring
significantly less time to train. Our model achieves 28.4 BLEU on the
WMT 2014 English-to-German translation task, improving over the
existing best results, including ensembles by over 2 BLEU. On the WMT
2014 English-to-French translation task, our model establishes a new
single-model state-of-the-art BLEU score of 41.8 after training for 3.5
days on eight GPUs, a small fraction of the training costs of the best
models from the literature. We show that the Transformer generalizes well
to other tasks by applying it successfully to English constituency parsing
both with large and limited training data.

<!-- Folie 42 -->
The dominant sequence transduction models are based on complex
recurrent or convolutional neural networks in an encoder-decoder
configuration. The best performing models also connect the encoder and
decoder through an attention mechanism. We propose a new simple
network architecture, the Transformer, based solely on attention
mechanisms, dispensing with recurrence and convolutions entirely.
Experiments on two machine translation tasks show these models to be
superior in quality while being more parallelizable and requiring
significantly less time to train. Our model achieves 28.4 BLEU on the
WMT 2014 English-to-German translation task, improving over the
existing best results, including ensembles by over 2 BLEU. On the WMT
2014 English-to-French translation task, our model establishes a new
single-model state-of-the-art BLEU score of 41.8 after training for 3.5
days on eight GPUs, a small fraction of the training costs of the best
models from the literature. We show that the Transformer generalizes well
to other tasks by applying it successfully to English constituency parsing
both with large and limited training data.
BLEU = bilingual evaluation understudy
WMT = Workshop on Statistical
Machine Translation [Task/Dataset]
Aktuell: WMT23 als
Challenge/Daten
sacreBLEU als Implementierung
41.8 “BLEU” = 0.418 BLEU

## Transformer technisch

<!-- Folie 43 -->
Aufbau
Quelle: Fig. 1 in
“Attention is all you need”

## Konkrete Modelle mit Transformern

<!-- Folie 44 -->

## Konkrete Modelle

<!-- Folie 45 -->
GPT
Generative Pretrained Transformer
◼ Trainiert unsupervised auf gigantischen Textmassen
(präziser: self-supervised)
◼ BPE (Byte Pair Encoding) als Tokenization Schema
◼ Sehr große Modelle (= sehr viele Layer, sehr viele Parameter)
◼ Gelernte Positionskodierung, begrenzter Kontext
◼ Decoder-Only: das nächste Token vorhersagen
→ Varianten GPT-J, GPT-NeoX, GPT-2, LLama 1,2,3 und nichtöffentlich GPT-3, 3.5, 4, etc

## Byte Pair Encoding (BPE)

<!-- Folie 46 -->
Ein Tokenization Schema (Gage 1994)
Vokabulargröße bei GPT-4’s BPE “tiktoken” z.B. ist 100256,
Durchschnittlich entspricht ein Token etwa 4 Bytes.
BPE baut auf einem Tokenizer auf, meist Token=Byte oder Character.
Algorithmus:
1. Sortiere alle möglichen Tokenpaare nach Häufigkeit,
2. Verschmelze die 2 häufigsten zu einem neuen Token,
3. Ende, wenn es genug verschiedene Token gibt.

<!-- Folie 47 -->
Ein Tokenization Schema (Gage 1994)
Algorithmus:
1. Sortiere alle möglichen
Tokenpaare nach
Häufigkeit,
2. Verschmelze die 2
häufigsten zu einem
neuen Token,
3. Ende, wenn es genug
verschiedene Token gibt.

## Konkrete Modelle

<!-- Folie 48 -->
NanoGPT
Visualisierung + Erklärung,
Layer für Layer
von Brendan Bycroft:
https://bbycroft.net/llm

<!-- Folie 49 -->
BERT
Bidirectional Encoder Representations from Transformers
◼ Encoder-Only (nicht zwangsläufig generativ)
◼ Tokenization auf Subwort-Level (WordPiece)
◼ Training mit 2 Tasks:
◼ Masked Language Modeling (ähnlich wie bei word2vec)
◼ Nächsten Satz vorhersagen
◼ Bei gleicher Modellgröße besser als GPT für manche Tasks
→ Varianten RoBERTa, ALBERT, DistilBERT

<!-- Folie 50 -->
ViT
Vision Transformer (Dosovitskiy et al.)
“An Image is Worth 16x16 Words”
◼
◼
◼
◼
Bild wird grob gerastert in “Patches” aufgeteilt
Jeder Patch (=Token) wird in einen Vektor umgewandelt
Positionskodierung für 2D-Position statt 1D wie bei Text
Ansonsten: “klassischer” Transformer
Für Klassifikationsaufgaben manchmal besser als CNNs.

## Implementierung des Transformers

<!-- Folie 51 -->
“Attention is all you need”
Alexander Rush et al.:
The Annotated Transformer
(updated 2022 edition),
der Artikel zusammen mit Codeschnipseln (und einigen Kommentaren).
Für Verrückte oder sehr Interessierte:
“I made a transformer by hand (no training!)” von Theia Vogel
(Gewichte sorgfältig von Hand bestimmt)
