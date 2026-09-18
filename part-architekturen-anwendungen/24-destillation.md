---
title: "Destillation"
short_title: "Destillation"
---

# Destillation

## Was lernen wir beim Deep Learning eigentlich?

### Ansatz 1: Regression zu bekannter Funktion

Wenn eine Funktion der Daten bekannt ist, also $f \colon \mathbb{R}^n \to \mathbb{R}^m$ für Datenpunkte $x_1, \dots, x_N \in \mathbb{R}^n$ bekannt ($y_i = f(x_i)$ liegen vor) oder billig zu berechnen ist, können wir ein neuronales Netz $\mathcal{N}$ trainieren, sodass $\mathcal{N}(x_i) \approx y_i$ ist (Regression, MSE-Loss). Analog für $c \colon \mathbb{R}^n \to \{0, 1\}$ eine Klassifikation: Wenn $y_i = c(x_i)$ bekannt sind, lässt sich $\mathcal{N}$ trainieren, sodass $\mathcal{N}(x_i) = y_i$ in möglichst vielen Fällen (Klassifikation, BCE-Loss).

Problem: Manchmal kennen wir die Funktion $f$ bzw. $c$ nicht – z.B. wenn wir Daten ohne Label haben (aber klassifizieren oder clustern wollen). Oder wenn die gesuchte Funktion $f$ komplizierter ist, z.B. wenn die Eingabe $x$ eine Sequenz von Token $x_1, \dots, x_k$ repräsentiert und

$$
f(x_1, \dots, x_k) := P(x_k \mid x_1, \dots, x_{k-1}),
$$

die Wahrscheinlichkeit, eine Sequenz $x_1, \dots, x_k$ vorzufinden, wenn man $x_1, \dots, x_{k-1}$ gesehen hat (*next token prediction*). Das kann man immer noch aus den Daten schätzen, aber relativ teuer.

### Ansatz 2: Regression zu unbekannter Funktion

Beispiel Autoencoder: Wir trainieren eine Regression des neuronalen Netzes $\mathcal{N}$ auf die Identitätsfunktion (wie in Ansatz 1), aber $\mathcal{N} = D \circ E$ (Decoder nach Encoder mit Bottleneck dazwischen). Die Abbildung $E \colon \mathbb{R}^n \to \mathbb{R}^m$, die der Encoder lernt, ist vor dem Training völlig unbekannt. Es gibt mehr als eine „korrekte“ solche Abbildung. Die Menge aller möglichen Funktionen $f \colon \mathbb{R}^n \to \mathbb{R}^m$ ist sehr groß; welche Teilmenge zu sinnvollen Encodern gehört, ist a priori unklar.

## Model Compression

### Zwei Ansätze vereint: Suchproblem und Regression

Die *Suche* nach der richtigen Funktion braucht viel Platz und Flexibilität, daher sind große (tiefe) neuronale Netze besser geeignet zum Lernen unbekannter Funktionen. Eine *Regression* auf eine bekannte Funktion braucht nicht viel Flexibilität, daher lassen sich auch flache neuronale Netze einsetzen; die benötigte Komplexität hängt nur von der Funktion ab, nicht davon, wie schwer es ist, diese zu erraten.

Das legt nahe: erst mit einem großen Netz suchen, dann das Ergebnis in ein kleines Netz überführen. Zwei Strategien:

**Strategie 1: Pruning.** Beim Pruning (Abschneiden) werden Bereiche des neuronalen Netzes identifiziert, die wenig zur Berechnung beitragen, und entfernt (Gewichte auf $0$ gesetzt, Layer entfernt). Es ist schwierig auszuwählen, was weg kann, und nach dem Entfernen „unwichtiger“ Teile ist oft ein Finetuning erforderlich.

**Strategie 2: Destillation.** Beim Destillieren wird ein kleineres **Schüler**-Netzwerk trainiert mit Hilfe eines größeren **Lehrer**-Netzwerks (welches zuvor teuer trainiert wurde). Dabei gibt es 3 wesentliche Ansätze:

1. Lehrer-Labels auf Daten ermöglichen supervised Training der Schüler. (Lehrer-Training ist „Suche“, Schüler-Training ist „Regression“.)
2. Synthetische Daten, generiert durch das Lehrer-Netzwerk, beschleunigen das Schüler-Training.
3. Der Schüler lernt direkt aus den Logits das darin verborgene Wissen. (Destillation im engeren Sinne.)

### Vorläufer: Ensemble Model Compression

Buciluă, Caruana, Niculescu-Mizil: *Model Compression* (2006):

1. Trainiere ein großes Ensemble-Modell (z.B. Random Forest, XGBoost) auf den Daten,
2. generiere synthetische Eingabedaten,
3. generiere Labels mit dem trainierten Ensemble-Modell,
4. trainiere ein neuronales Netz auf den neuen, viel umfangreicheren Daten.

Das Training wirkt regularisierend, das neuronale Netz verallgemeinert besser – und ist zur Inferenz um Größenordnungen schneller als das Ensemble.

### Wie deep muss es sein?

Ba, Caruana: *Do Deep Nets Really Need to be Deep?* (2013). Wie muss ein neuronales Netz aufgestellt sein (Architektur), um eine Funktion zu lernen? Zwei getrennte Fragen:

1. **Expressivity**: Ist das Netz komplex genug, um die Funktion abzubilden?
2. **Learnability**: Kann der Gradientenabstieg diese Funktion im großen Suchraum finden?

Ergebnisse: Expressivity ist nicht das Problem (vgl. das [Kapitel „Universelle Approximation“](../part-lernen/12-universelle-approximation.md)), flache und breite Netzwerke sind stark. Learnability ist das Problem flacher Netze: Ein flaches Netz, das mit den Soft-Labels eines tiefen Netzes trainiert wird, erreicht dessen Genauigkeit – dasselbe flache Netz direkt auf den Daten trainiert aber nicht.

## Model Distillation

### Distillation Loss

Hinton, Vinyals, Dean: *Distilling the Knowledge in a Neural Network* (2015). Für eine $k$-Klassen-Klassifikationsaufgabe ist der letzte Schritt im großen Lehrer-Modell ein Softmax $\mathbb{R}^k \to [0, 1]^k$, gefolgt von der „harten“ Klassifikation $\operatorname{argmax}$, um zu einem Klassenurteil zu kommen. Idee: Lerne nicht aus dem harten, sondern aus dem *weichen* Urteil. Und mach es noch weicher.

Loss-Funktion zum Schüler-Training: KL-Divergenz (relative Entropie) zwischen Schüler-Verteilung und Lehrer-Verteilung, jeweils reskaliert mit Temperatur $T$:

$$
q_i = \frac{\exp(z_i / T)}{\sum_j \exp(z_j / T)},
\qquad
L_{\text{distill}} = T^2 \cdot D_{KL}\bigl( q^{\text{Lehrer}} \,\|\, q^{\text{Schüler}} \bigr).
$$

Mit $T > 1$ werden die kleinen Wahrscheinlichkeiten der falschen Klassen sichtbar (Temperature Scaling im [Kapitel „Latente Räume geometrisch“](22-latente-raeume.md)), und genau die tragen die Information. In der Praxis kombiniert man das mit dem gewöhnlichen Kreuzentropie-Loss auf den echten Labels bei $T = 1$.

### Dark Knowledge

Beispiel: fehlerhaft gelabelte Daten, z.B. ein Hund $x$ mit dem Label „Katze“. Der Lehrer klassifiziert nach dem Lernen „Katze“ (leider falsch). Aber vor dem $\operatorname{argmax}$ sehen wir vermutlich $P(x = \text{Hund}) > 0$, und zwar deutlich – d.h. in $P(x = \text{Hund})$ steckt noch Information, „dunkles Wissen“: Der Lehrer weiß, dass das Bild einem Hund ähnlich sieht, auch wenn er es der falschen Klasse zuordnet. Der Schüler lernt aus dunklem Wissen und leidet weniger unter falschen Labels. Allgemeiner: Die Ähnlichkeitsstruktur zwischen den Klassen (eine 7 sieht eher wie eine 1 aus als wie eine 0) wird mitübertragen.

### Schüler übertreffen Lehrer

Furlanello, Lipton, Tschannen, Itti, Anandkumar: *Born Again Neural Networks* (2018), inspiriert von „born again trees“ aus 1996. Das Schüler-Netzwerk ist nicht nur kleiner und damit schneller und billiger als das Lehrer-Netzwerk – es kann sogar *besser* werden, selbst bei gleicher Architektur. Die implizite Neugewichtung der Trainingsdaten führt zu Fokus auf „schwere Fälle“; der Loss berücksichtigt weniger den einfachen Teil der Aufgabe. Knowledge Distillation ist damit Regularisierung bzw. Optimierung statt nur Kompression. Und man kann iterieren: ein Ensemble aus Generationen von Schülern.

### DistilBERT

Sanh, Debut, Chaumond, Wolf: *DistilBERT, a distilled version of BERT: smaller, faster, cheaper and lighter* (2019): „we leverage knowledge distillation during the pre-training phase and show that it is possible to reduce the size of a BERT model by 40 %, while retaining 97 % of its language understanding capabilities and being 60 % faster. To leverage the inductive biases learned by larger models during pre-training, we introduce a triple loss combining language modeling, distillation and cosine-distance losses.“

DistilBERT := jeder zweite Layer von BERT (als Initialisierung). Der Loss ist die Summe aus drei Teilen:

* **Distillation Loss**: KL-Divergenz zu den temperatur-skalierten Logits des Lehrers.
* **Masked Language Modeling Loss**: wie BERT, Lernen aus den Daten, mit Temperatur 1.
* **Cosine-Distance Loss**: latente Mannigfaltigkeiten beibehalten, d.h. die Outputs der Layer (die hidden states) von Schüler und Lehrer im Kosinusabstand vergleichen.

Das ist das Modell aus dem [Kapitel „Vortrainierte Modelle“](../part-grundlagen/04-vortrainierte-modelle.md) für Text Classification und Fill-Mask.

## Anwendungen

### Speculative Decoding

Vgl. Yan, Agarwal, Venkataraman: *Decoding Speculative Decoding* (2024). Problem: Das (autoregressive) Sampling eines nächsten Tokens mit einem LLM ist teuer, benötigt aber ein Ergebnis, um das darauf folgende Token zu sampeln – man kann nicht parallelisieren. Trick: Rate die kommenden 5 Token mit einem kleinen, billigen Modell, und *verifiziere* sie mit dem teuren LLM in einem einzigen Forward-Pass (der ist parallel). Stimmen sie, hat man 5 Token zum Preis von einem; sonst nimmt man das erste abweichende Token des großen Modells und rät neu. Trick 2: Das billige Modell ist vom LLM destilliert, damit es möglichst oft richtig rät.

### SDXL Turbo

Sauer, Lorenz, Blattmann, Rombach: *Adversarial Diffusion Distillation* (2023). Aus einem vortrainierten tiefen Diffusionsmodell (SDXL) zum Generieren von Bildern aus Bildbeschreibungen in einem $k$-Schritte-Iterationsprozess des Entrauschens wird ein 1-Schritt-Modell destilliert – mit Distillation Loss (Schüler-Output soll dem Lehrer-Output nach $k$ Schritten ähneln) und Adversarial Loss (GAN-Training aus dem [Kapitel „GANs“](21-gans.md), damit die Bilder scharf bleiben). Bildgenerierung in Echtzeit.

### Gemini Flash

Google Gemini Team: *Gemini 1.5: Unlocking multimodal understanding across millions of tokens of context* (2024). Auch Google benutzt Destillation, um aus dem großen, teuren Gemini 1.5 Pro das günstigere, schnellere Gemini 1.5 Flash zu destillieren. Analog: OpenAIs GPT-Mini-Modelle.

### Chain of Thought

1. Bringe ein LLM dazu, länger bzw. mehr nachzudenken (= mehr Output zu produzieren): die „Chain of Thought“ – warum diese Antwort, Begründungen, Zwischenschritte.
2. Verstecke langwierige oder schlechte Zwischenüberlegungen und lass Schüler aus den „wohlüberlegten“ Inhalten lernen, mit Destillation.

So entstehen „Reasoning“-Modelle, die kompakt das können, wofür der Lehrer viele Token gebraucht hat.
