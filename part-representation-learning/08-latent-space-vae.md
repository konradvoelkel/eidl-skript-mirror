---
title: "VL 08: Latent Space, VAE und word2vec"
short_title: "VL 08"
---

# Latent Space, VAE und word2vec

:::{note} Stand
Erste Prosafassung (aus den Folien von VL 08, WiSe 2025/26). Abbildungen fehlen noch, siehe die `TODO`-Kommentare. Diese Vorlesung war mit 85 Folien sehr voll; ggf. word2vec/NLP in das nächste Kapitel verschieben.
:::

## Autoencoder-Varianten

Wie letztes Mal: Ein Autoencoder besteht aus Encoder $\mathbb{R}^D \to \mathbb{R}^L$ und Decoder $\mathbb{R}^L \to \mathbb{R}^D$, mit dem latenten Raum der Dimension $L$ als Flaschenhals. In diesem Kapitel variieren wir die Loss-Funktion und die Eingabe, und sehen, was das mit dem latenten Raum macht.

### Sparse Autoencoder

Idee: die Loss-Funktion um **Strafterme** ergänzen. Heute: dafür sorgen, dass ein latenter Vektor *dünn besetzt* (sparse) ist, also die meisten Einträge nahe $0$ sind.

Lösung: Unter der Annahme, dass die latenten Vektoren Einträge in $[0, 1]$ haben (z.B. durch ein Sigmoid am Ende des Encoders), betrachten wir für jede latente Dimension $j$ die mittlere Aktivierung $\hat\varrho_j$ über den Batch und bestrafen die Kullback-Leibler-Divergenz zwischen der Bernoulli-Verteilung mit Wahrscheinlichkeit $\varrho = 0{,}1$ und der Bernoulli-Verteilung mit Wahrscheinlichkeit $\hat\varrho_j$:

$$
L_{\text{sparse}} = \sum_{j=1}^L D_{KL}\bigl(\operatorname{Ber}(\varrho) \,\|\, \operatorname{Ber}(\hat\varrho_j)\bigr)
= \sum_{j=1}^L \left( \varrho \ln\frac{\varrho}{\hat\varrho_j} + (1 - \varrho) \ln\frac{1 - \varrho}{1 - \hat\varrho_j} \right).
$$

Der Term ist $0$ genau dann, wenn jede latente Dimension im Mittel nur zu 10 % „an“ ist. Dense latents nutzen alle Dimensionen für jeden Datenpunkt; sparse latents verteilen die Datenpunkte auf wenige aktive Dimensionen, was die einzelnen Dimensionen interpretierbarer macht.

<!-- TODO Abbildung: Sparse latents vs. dense latents (Folie 7) -->

### Denoising Autoencoder

Idee: Daten nicht putzen, sondern *verschmutzen*. Noise $\varepsilon$ generieren, auf die Daten addieren, $x_{\text{noisy}} = x + \varepsilon$, und das als Input für den Autoencoder verwenden. Die Loss-Funktion vergleicht aber $\operatorname{dec}(\operatorname{enc}(x_{\text{noisy}}))$ mit dem *sauberen* $x$:

$$
L_{\text{denoise}} = \operatorname{MSE}\bigl(x,\ \operatorname{dec}(\operatorname{enc}(x + \varepsilon))\bigr).
$$

Das zwingt das Netzwerk dazu, einzelne Pixel nicht zu stark zu gewichten und eher globale Strukturen zu suchen – ein einzelner verrauschter Pixel darf die Rekonstruktion nicht kippen.

<!-- TODO Abbildungen: Ergebnis-Beispiele MNIST / USPS / Fashion-MNIST (Folien 10–12), Latents von Fashion-MNIST & USPS -->

Code angucken: `denoising-autoencoder-mnist.py` (Blatt 8) implementiert genau das, als *Denoising Sparse Label Autoencoder* – alle Tricks auf einmal, mit SiLU, BatchNorm und Dropout.

### Bisher, und was es bringt

Wir haben das Autoencoder-Design eingesetzt, um Bilder zu komprimieren (mit Sparsity Constraint), Bilder zu klassifizieren, Bilder zu entrauschen – und all das zusammen. Ein ML-System, welches diese Bilder verarbeiten soll, kann nun den fertig trainierten Encoder verwenden und direkt auf den Repräsentationen im Latent Space arbeiten. Das ist **Modularisierung im Training**: Der Encoder wird einmal trainiert und dann als Feature-Extraktor wiederverwendet.

Frage: Welche Struktur finden wir im Latent Space bzw. in den Latent Vectors der Daten? Die **Latent-Manifold-Hypothese** besagt, dass die Daten in $\mathbb{R}^D$ nahe einer niedrigdimensionalen gekrümmten Fläche (Mannigfaltigkeit) liegen und der latente Raum diese Fläche „flach“ parametrisiert. Dazu mehr in VL 13.

Später werden wir das Autoencoder-Design einsetzen, um Text (Strings) natürlicher Sprache zu kodieren, sodass die latente Repräsentation interessante Struktur aufweist – das ist word2vec, weiter unten.

## Variational Autoencoder

### Motivation: probabilistische Modelle

Beim klassischen Autoencoder bildet der Encoder einen Datenpunkt $x \in D$ auf einen Punkt $\operatorname{enc}(x) \in L$ im latenten Raum ab, der Decoder $y \in L$ auf $\operatorname{dec}(y) \in F$ im Feature-Raum; Ziel ist $\operatorname{MSE}(x, \operatorname{dec}(\operatorname{enc}(x)))$ möglichst klein. Die Modellannahme war aber: Die Punkte $x \in D$ sind eine Stichprobe aus einer *Verteilung*. Können wir die Verteilung direkt mit modellieren, in $\operatorname{enc}(x)$?

**Variation des Ziels**: Auch $\operatorname{MSE}(x, \operatorname{dec}(\operatorname{enc}(x) + \varepsilon))$ soll möglichst klein sein, für einen normalverteilten Fehler $\varepsilon \sim \mathcal{N}(0, 1)$. **Variation des Trainings**: Nach $\operatorname{enc}(x)$ ein $\varepsilon$ sampeln, addieren, dann $\operatorname{dec}$. Der Decoder muss dann nicht nur den Punkt $\operatorname{enc}(x)$, sondern eine ganze Umgebung davon auf $x$ abbilden – der latente Raum wird „glatt“.

Oh: Wie geht Backpropagation für „ein $\varepsilon$ sampeln“? Da $\varepsilon$ nicht von den Gewichten abhängt, ganz normal mit der Kettenregel:

$$
\frac{d}{dw_{\text{enc}}} \operatorname{dec}(\operatorname{enc}(x) + \varepsilon) = \operatorname{dec}'(\operatorname{enc}(x) + \varepsilon) \cdot \frac{d}{dw_{\text{enc}}} \operatorname{enc}(x).
$$

Das gesampelte $\varepsilon$ ist im Rückwärtsdurchlauf einfach eine Konstante.

**Beispiel im latenten Raum.** Mit 3 Datenpunkten: Klassisch sind das 3 Punkte. Mit $+\varepsilon$ werden es 3 Wolken gleicher Größe. Mit $+\sigma\varepsilon$ für einen Skalierungsfaktor $\sigma$ kann man die Wolkengröße steuern. Mit 300 Datenpunkten: Klassisch eine Punktwolke mit Löchern und Ausreißern; gut wäre eine Verteilung, die den latenten Raum lückenlos und gleichmäßig füllt, sodass man an *jeder* Stelle dekodieren kann.

<!-- TODO Abbildungen: latenter Raum mit 3 bzw. 300 Punkten, klassisch / +ε / +σε (Folien 28–32) -->

Modelliere die Verteilung also mit einer Gaußschen Mischung im latenten Raum, in der die Störung $\varepsilon$ von den Daten abhängt: Zu jedem Datenpunkt $x \in D$ brauchen wir zusätzlich zu $\operatorname{enc}(x) \in L$ auch eine Standardabweichung $\sigma_x$ (bzw. besser noch eine Kovarianzmatrix $\operatorname{cov}(x)$), dann $\operatorname{dec}(\operatorname{enc}(x) + \varepsilon)$ mit $\varepsilon \sim \mathcal{N}(0, \sigma_x^2)$. Aber Sampling aus einer Verteilung, deren Parameter $\sigma_x$ von den Gewichten abhängen, lässt sich nicht ableiten. **Reparametrisierungstrick**: statt $\varepsilon \sim \mathcal{N}(0, \sigma_x^2)$ besser

$$
y := \operatorname{enc}(x) + \sigma_x \varepsilon, \qquad \varepsilon \sim \mathcal{N}(0, 1),
$$

denn dann ist $\varepsilon$ wieder eine Konstante und $\sigma_x$ ein ganz normaler Ausgang des Encoders, durch den Gradienten fließen.

### Training

Wie trainiert man einen Variational Autoencoder? Für jeden Datenpunkt $x \in D$ berechne $\operatorname{enc}(x) = (\mu_x, \sigma_x)$ – der Encoder hat jetzt $2L$ Ausgänge –, generiere ein $\varepsilon \sim \mathcal{N}(0, 1)$ und setze $y := \mu_x + \sigma_x \varepsilon$. Die Loss-Funktion ist *naiv* $\operatorname{MSE}(x, \operatorname{dec}(y))$. Das hat einen Haken: Das Netz kann $\sigma_x \to 0$ lernen und ist dann wieder ein klassischer Autoencoder.

Stabileres Training mit dem Extra-Term **Variational Loss**:

$$
L_{\text{VAE}} = \operatorname{MSE}(x, \operatorname{dec}(y)) + D_{KL}\bigl( q(y \mid x) \,\|\, \mathcal{N}(0, 1) \bigr),
$$

wobei $q(y \mid x) = \mathcal{N}(\mu_x, \sigma_x^2)$ die Dichte der latenten Verteilung für ein festes $x$ ist. Dabei sind die beiden Standardnormalverteilungen – das $\mathcal{N}(0,1)$ für $\varepsilon$ und das $\mathcal{N}(0,1)$ im KL-Term – nicht „dieselben“!! Die erste ist die Rauschquelle, die zweite ist die *Prior*-Verteilung, an die sich die Gesamtheit der latenten Verteilungen anschmiegen soll, damit der latente Raum um den Ursprung herum lückenlos gefüllt ist. Für Normalverteilungen hat der KL-Term eine geschlossene Form:

$$
D_{KL}\bigl( \mathcal{N}(\mu, \sigma^2) \,\|\, \mathcal{N}(0, 1) \bigr) = \tfrac12 \left( \mu^2 + \sigma^2 - 1 - \ln \sigma^2 \right).
$$

Diese Loss-Funktion ist genau der negative **ELBO** (evidence lower bound) $\mathcal{L}(\theta, q)$ aus dem Kapitel „Expectation Maximization“ in Data Science.

### Recap

Ein VAE ist ein Autoencoder, dessen Encoder statt eines Punkts eine Normalverteilung im latenten Raum ausgibt, dessen Decoder aus einer Stichprobe daraus rekonstruiert, und dessen Loss die Rekonstruktion plus die KL-Divergenz zum Standardnormal-Prior ist. Danach kann man neue Daten generieren, indem man $y \sim \mathcal{N}(0, 1)$ sampelt und dekodiert. Schön zusammengefasst in Lilian Wengs Blogpost [From Autoencoder to Beta-VAE](https://lilianweng.github.io/posts/2018-08-12-vae/). VAEs sind heute noch eine Komponente der Bildgeneratoren (DALL-E, Midjourney, Stable Diffusion): Die Diffusion findet im latenten Raum eines VAE statt.

<!-- TODO Abbildung: VAE-Schema (Lilian Weng) -->

## word2vec

### Von der Anwendung her gedacht

Ein Beispiel-Task, unsupervised mit neuronalen Netzen: Alle Dokumente $D_i$ einlesen als Liste von Wörtern (getrennt an Leerzeichen, Satzzeichen entfernt), dann jedes einzelne Wort mit einem zuvor trainierten neuronalen Netz umrechnen in eine andere Repräsentation, die sich besser vergleichen lässt. Die andere Repräsentation verschaffen wir uns durch latente Vektoren aus einem Autoencoder. Das ist die Idee von **word2vec** (Mikolov et al., Google, 2013).

### Vorverarbeitung und Ziel

1. Wir zählen alle Wörter (bzw. Token) im Korpus,
2. entfernen Stopwords und sortieren nach Häufigkeit,
3. behalten die häufigsten $N$ Wörter (z.B. $N = 5000$),
4. kodieren diese mit One-Hot-Encoding als Vektoren in $\mathbb{R}^N$,
5. mit dem Ziel, eine Abbildung $e \colon \mathbb{R}^N \to \mathbb{R}^K$ zu finden, $K \ll N$ (z.B. $K = 200$),
6. mit einer „Decoder“-Abbildung $d \colon \mathbb{R}^K \to \mathbb{R}^N$, sodass $d(e(w)) = w$ für alle $N$ Wörter unserer Liste gilt,
7. und semantisch ähnliche Wörter $w_1, w_2$ nach Kodieren in $\mathbb{R}^K$ einen kleinen Abstand $\operatorname{d}(e(w_1), e(w_2)) \approx 0$ haben.

Punkt 6 allein wäre ein gewöhnlicher Autoencoder auf One-Hot-Vektoren – und der lernt nichts über Bedeutung, denn One-Hot-Vektoren sind alle gleich weit voneinander entfernt. Punkt 7 ist der Clou.

### Kernidee

Die Semantik eines Wortes ergibt sich durch seine Nutzung in Sätzen (*distributional hypothesis*). Beispiel: „Die [MASK] frisst ihr Futter am liebsten aus dem goldenen Napf“ kommt in Texten mit [MASK] = Katze und [MASK] = Hündin vor. Der Machine-Learning-Task, unsupervised: Gegeben Text, ersetze ein Wort durch [MASK] und lasse vorhersagen, was [MASK] ist – wie ein Denoising Autoencoder, bei dem das Rauschen im Löschen eines Wortes besteht.

**CBOW** (Continuous Bag of Words, für kleinere Korpora). Hyperparameter ist die Fenstergröße $S$ (window size), z.B. $S = 2$. Eingabe: $2S + 1$ Token, die hintereinander im Text vorkommen, dabei das mittlere durch [MASK] ersetzt – also $2S$ One-Hot-Vektoren. Ausgabe: eine Wahrscheinlichkeitsverteilung auf allen $N$ Wörtern. Loss-Funktion: negative Log-Likelihood (NLL), d.h. Vergleich der ausgegebenen Verteilung mit dem One-Hot-Vektor für das Wort, welches sich hinter [MASK] verbirgt. Architektur: 1 Hidden Layer mit $K$ Neuronen, der „Encoder“ $W \in \mathbb{R}^{K \times N}$, angewendet auf alle $2S$ Kontextwörter und dann gemittelt (*averaging*), danach ein Layer „Decoder“ $W' \in \mathbb{R}^{N \times K}$ gefolgt von Softmax:

$$
P(w_{\text{mitte}} \mid \text{Kontext}) = \operatorname{sm}\Bigl( W' \cdot \frac{1}{2S} \sum_{j \in \text{Kontext}} W w_j \Bigr).
$$

Die Wortvektoren sind die Spalten von $W$: $e(w) = W w$ ist für einen One-Hot-Vektor $w$ einfach die entsprechende Spalte.

**Skip-gram**, die Alternative zu CBOW: Gegeben ein Token, sage den Kontext vorher. Eingabe: das mittlere Token als One-Hot-Vektor für eine Abfolge von $2S + 1$ Token. Ausgabe: eine Wahrscheinlichkeitsverteilung auf allen $N$ Token. Loss-Funktion: NLL, d.h. Vergleich der ausgegebenen Verteilung mit der Summe der One-Hot-Vektoren für alle $2S$ Kontexttoken. Architektur: 1 Hidden Linear Layer mit $K$ Neuronen (der „Encoder“), danach ein Layer „Decoder“ mit $N$ Neuronen gefolgt von Softmax. Skip-gram funktioniert bei großen Korpora und seltenen Wörtern besser.

<!-- TODO Abbildungen: CBOW und Skip-gram Architekturen (Lilian Weng, "Learning Word Embedding", 2017) -->

### word2vec benutzen

Verfügbare Gewichte $W$ gibt es mit Gensim (z.B. `wiki-english-20171001`) oder von Hugging Face (z.B. [word2vec-google-news-300](https://huggingface.co/fse/word2vec-google-news-300), $N = 3$ Millionen, $K = 300$). Klappt nicht gut? Drop-in-Ersatz für word2vec ist Facebooks **fastText**, welches hauptsächlich einen geeigneteren Tokenizer benutzt (Stichwort Subword-Tokenization) und dadurch auch mit unbekannten Wörtern umgehen kann.

### word2vec selbst trainieren (ein ganz knapper Überblick)

Zutatenliste: Keine GPU oder andere Beschleuniger zur Hand? Google Colab oder CPU reicht. Input: ein Textkorpus zum Training, eine Tokenization-Strategie bzw. ein Tokenizer (darüber sprechen wir noch), die Dimension $K$ des Latent Space, CBOW oder Skip-gram (wie groß ist der Korpus?), von Grund auf trainieren (Pretraining) oder Finetuning, und welche Implementierung?

* **Gensim** ([Tutorial](https://radimrehurek.com/gensim/auto_examples/tutorials/run_word2vec.html#training-your-own-model)). Pro: NLP-Gesamtlösung, gut dokumentiertes Paket. Contra: keine GPU-Beschleunigung (aber für word2vec ist das „egal“), und keine Kombination von word2vec im Training mit anderen Tasks (wie wir es beim Denoising Label Autoencoder getan haben).
* **PyTorch**, „so richtig von Hand“: [Skip-gram implementation step by step](https://www.kaggle.com/code/karthur10/skip-gram-implementation-with-pytorch-step-by-step/notebook); oder mit dem `torch.nn.Embedding`-Layer (das ist genau die Matrix $W$, mit One-Hot-Multiplikation als Lookup implementiert): [word2vec from scratch](https://muhark.github.io/python/ml/nlp/2021/10/21/word2vec-from-scratch.html), [d2l.ai](https://d2l.ai/chapter_natural-language-processing-pretraining/word2vec-pretraining.html).

Wozu? Durch Pretraining oder Finetuning von word2vec-Modellen mit PyTorch bekommt man Wortvektoren, die auf die eigene Domäne (Fachsprache, andere Sprache) passen, und kann sie als erste Schicht in ein größeres Modell einbauen.

## NLP

### Beispiel-Task: ähnliche Dokumente finden

Gegeben ist eine Menge von $N$ (kurzen) Dokumenten $\{D_1, \dots, D_N\}$ (z.B. Tweets, Webseiten, Hausarbeiten). Gesucht sind $k$ Paare ähnlicher Dokumente ($k \ll N$), z.B. um Tweets thematisch zu gruppieren oder Plagiate zu finden: $\{(x_1, y_1), \dots, (x_k, y_k)\}$, Paare von Indizes, sodass $D_{x_i}$ und $D_{y_i}$ ähnlich sind.

**Klassischer Ansatz**: Wörter in $D_i$ zählen, Häufigkeitsverteilungen von $D_i$ und $D_j$ vergleichen (*bag of words*). Probleme mit diesem Ansatz:

1. „Katze isst Maus“ und „Maus isst Katze“ sind ununterscheidbar.
2. „Schwimmen“ und „schwamm“ haben nichts miteinander zu tun.
3. „Hund“ und „Tier“ haben nichts miteinander zu tun.
4. Wörter wie „der“, „die“, „das“ sind sehr häufig, aber bedeutungslos.

Klassische Lösungsansätze: (1) $n$-Gramme statt Wörter betrachten, (2) Lemmatisierung, (3) komplexe Ontologien (formalisiertes Wissen), (4) Stopwords entfernen.

### Wörter? Token!

Alternative Lösung zu Problem 2 (statt Lemmatisierung): Buchstaben bzw. Zeichen anstelle von Wörtern als „Atome“ (= Token) nehmen, und $n$-Gramme davon (z.B. Trigramme, $n = 3$). Beispiel: „schwimm!“ und „schwimmen“ ergeben

$$
[\text{sch}, \text{chw}, \text{hwi}, \text{wim}, \text{imm}, \text{mm!}] \quad\text{und}\quad [\text{sch}, \text{chw}, \text{hwi}, \text{wim}, \text{imm}, \text{mme}, \text{men}],
$$

die haben sehr ähnliche Trigrammhäufigkeitsverteilungen. Konkret zu klärende Fragen: Leerzeichen wie jedes andere Zeichen behandeln? Über das Satzende „.“ hinaus? Flexibles $n$, z.B. Silben statt Buchstabentrigramme? Die Antworten darauf bilden die **Tokenisierungsstrategie**, den Tokenizer. Der Einfachheit halber bleiben wir zunächst bei Token = Wörter, d.h. wir löschen Satzzeichen und trennen an Leerzeichen; Byte Pair Encoding, der Tokenizer moderner LLMs, kommt im nächsten Kapitel.

**Modernerer Ansatz (supervised)**: mit einem neuronalen Netz; Menschen labeln Ähnlichkeit. Eingabe: Paare $(D_i, D_j)$, Ausgabe: Ähnlichkeitsschätzung. **Unsupervised mit neuronalen Netzen**:

1. Alle Dokumente $D_i$ einlesen als Liste von Wörtern.
2. Jedes einzelne Wort mit einem zuvor trainierten neuronalen Netz (word2vec) umrechnen in eine andere Repräsentation, die sich besser vergleichen lässt.
3. Für jedes Paar $(D_i, D_j)$ die Listen von Repräsentationen vergleichen (z.B. Kosinus-Ähnlichkeit der Mittelwerte), daraus ein Ähnlichkeitsmaß für das Paar berechnen.
4. Die Top-$k$ ähnlichsten Paare ausgeben.

Problem 3 („Hund“ und „Tier“) löst word2vec, weil beide in ähnlichen Kontexten vorkommen und daher nahe beieinander liegen. Problem 1 (Wortreihenfolge) löst es nicht – dafür braucht man Modelle, die Sequenzen verarbeiten (nächstes Kapitel).

### Literatur und Softwarepakete

* Das modernste Lehrbuch ist Dan Jurafsky, James H. Martin: *Speech and Language Processing*. Es gibt einen „Third Edition Draft“ frei verfügbar: [web.stanford.edu/~jurafsky/slp3/](https://web.stanford.edu/~jurafsky/slp3/).
* Das Python Natural Language Toolkit (NLTK), [nltk.org/book](https://www.nltk.org/book/), enthält z.B. den PunktTokenizer, der so arbeitet wie wir jetzt.
* Radim Řehůřeks (& Koautoren) gensim-Bibliothek für Python, [radimrehurek.com/gensim](https://radimrehurek.com/gensim/auto_examples/index.html).
