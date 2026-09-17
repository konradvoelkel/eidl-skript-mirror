---
title: "VL 08: Latent Space, VAE und word2vec"
short_title: "VL 08"
---

# Latent Space, VAE und word2vec

:::{warning} Rohfassung
Dieses Kapitel ist eine automatische Transkription der Folien von VL 08 aus dem WiSe 2025/26
(`from_2025/slides/Einführung in Deep Learning 2025_26 VL 08_ Latent Space und VAE.pdf`), Folie für Folie in der Originalreihenfolge.
Formeln und Abbildungen sind dabei größtenteils verloren gegangen; der Text ist noch nicht überarbeitet.
:::

## Autoencoder

<!-- Folie 2 -->

<!-- Folie 3 -->
Wie letztes Mal bereits …
Das Autoencoder-Layout
Regression,
Input: Vektor x der Länge D
Encoder: reduziert in mehreren Schichten
von Dimension D auf Dimension L
Decoder: erhöht in mehreren Schichten von
Dimension L auf Dimension D
Input/Output im “Datenraum”
(bei Bildern: “Pixelraum”, pixel space)
Flaschenhals-Hidden Layer, Dimension L
“Latenter Raum”, latent space
(Grafik mit NN-SVG erstellt)

## Sparse Autoencoder

<!-- Folie 4 -->

<!-- Folie 5 -->
Idee: Loss-Funktion um Strafterme ergänzen.
Heute: dafür sorgen, dass ein latenter Vektor dünn besetzt ist.

<!-- Folie 6 -->
Idee: Loss-Funktion um Strafterme ergänzen.
Heute: dafür sorgen, dass ein latenter Vektor dünn besetzt ist.
Lösung: Kullback-Leibler-Divergenz zwischen der BernoulliVerteilung mit Wahrscheinlichkeit ϱ=0.1 und der tatsächlichen
Verteilung der Einträge im latenten Vektor.
Annahme: latente Vektoren haben Einträge in [0,1]

## Sparse latents vs. dense latents

<!-- Folie 7 -->

## Denoising Autoencoder

<!-- Folie 8 -->

<!-- Folie 9 -->
Idee: Daten nicht putzen, sondern verschmutzen
Noise ε generieren,
auf Daten x addieren: xnoisy = x + ε
als Input für den Autoencoder
Loss-Funktion: Vergleich von decoder(encoder(xnoisy)) mit x

## Ergebnis-Beispiele

<!-- Folie 10 -->
Oben:
MNIST
Unten:
USPS

<!-- Folie 11 -->
Oben:
MNIST
Unten:
Fashion-MNIST

## Fashion-MNIST & USPS latents

<!-- Folie 12 -->

## Denoising Autoencoder

<!-- Folie 13 -->
Noise ε generieren,
auf Daten x addieren: xnoisy = x + ε
als Input für den Autoencoder
Loss-Funktion: Vergleich von decoder(encoder(xnoisy)) mit x
Zwingt das Netzwerk dazu, einzelne Pixel nicht zu stark zu
gewichten, eher globale Strukturen zu suchen.

## Modelle

<!-- Folie 14 -->

## Code angucken!

<!-- Folie 15 -->
denoising-autoencoder.py

## Autoencoder

<!-- Folie 16 -->
Bisher …
Wir haben das Autoencoder-Design
eingesetzt um
◼
Bilder zu komprimieren
(mit Sparsity Constraint)
◼
◼
Bilder zu klassifizieren
Bilder zu entrauschen
und all das zusammen
(Denoising Sparse Label Autoencoder)

<!-- Folie 17 -->
Bisher …
Wir haben das Autoencoder-Design
eingesetzt um
◼
Bilder zu komprimieren
(mit Sparsity Constraint)
◼
◼
Bilder zu klassifizieren
Bilder zu entrauschen
und all das zusammen
Ein ML-System, welches diese Bilder
verarbeiten soll, kann nun den fertig
trainierten Encoder verwenden und direkt
auf den Repräsentationen im Latent Space
arbeiten.
→ Modularisierung im Training
(Denoising Sparse Label Autoencoder)

<!-- Folie 18 -->
Bisher …
Wir haben das Autoencoder-Design
eingesetzt um
◼
Bilder zu komprimieren
(mit Sparsity Constraint)
◼
◼
Bilder zu klassifizieren
Bilder zu entrauschen
und all das zusammen
(Denoising Sparse Label Autoencoder)
Ein ML-System, welches diese Bilder
verarbeiten soll, kann nun den fertig
trainierten Encoder verwenden und direkt
auf den Repräsentationen im Latent Space
arbeiten.
→ Modularisierung im Training
Frage:
Welche Struktur finden wir im Latent Space
/ in den Latent Vectors der Daten?
→ Latent Manifold Hypothese

<!-- Folie 19 -->
Später:
Wir werden das Autoencoder-Design
einsetzen um
◼
Text (Strings) natürlicher Sprache zu
kodieren (komprimieren)
◼
Ein ML-System, welches diese Bilder
verarbeiten soll, kann nun den fertig
trainierten Encoder verwenden und direkt
auf den Repräsentationen im Latent Space
arbeiten.
sodass die latente Repräsentation
interessante Struktur aufweist.
→ Modularisierung im Training
→ Wir werden NLP (Natural Language
Processing) noch weiter vertiefen, aber
zunächst sehen, wie word2vec benutzt
werden kann.
Frage:
Welche Struktur finden wir im Latent Space
/ in den Latent Vectors der Daten?
→ Latent Manifold Hypothese

## Zeit für eine Pause?

<!-- Folie 20 -->

## Variational Autoencoder

<!-- Folie 21 -->

## Variational Autoencoder (VAE) - Motivation

<!-- Folie 22 -->
Probabilistische Modelle
Klassischer Autoencoder:
Encoder: Datenpunkt x ∊ D → enc(x) ∊ L, Punkt im latenten Raum

<!-- Folie 23 -->
Probabilistische Modelle
Klassischer Autoencoder:
Encoder: Datenpunkt x ∊ D → enc(x) ∊ L, Punkt im latenten Raum
Modellannahme:
Die Punkte x ∊ D sind eine Stichprobe aus einer Verteilung
→ direkt Verteilung mit modellieren in enc(x)?

<!-- Folie 24 -->
Probabilistische Modelle
Klassischer Autoencoder:
Encoder: Datenpunkt x ∊ D → enc(x) ∊ L, Punkt im latenten Raum
Decoder: y ∊ L → dec(y) ∊ F, Punkt im Feature-Raum.
Ziel: MSE(x, dec(enc(x))) möglichst klein.
Variation des Ziels: auch MSE(x, dec(enc(x) + ε)) möglichst klein,
für einen normalverteilten Fehler ε ~

<!-- Folie 25 -->
Probabilistische Modelle
Klassischer Autoencoder:
Encoder: Datenpunkt x ∊ D → enc(x) ∊ L, Punkt im latenten Raum
Decoder: y ∊ L → dec(y) ∊ F, Punkt im Feature-Raum.
Ziel: MSE(x, dec(enc(x))) möglichst klein.
Variation des Ziels: auch MSE(x, dec(enc(x) + ε)) möglichst klein,
für einen normalverteilten Fehler ε ~
Variation des Trainings: nach enc(x) ein ε samplen, addieren, dann dec.

<!-- Folie 26 -->
Probabilistische Modelle
Variation des Ziels: auch MSE(x, dec(enc(x) + ε)) möglichst klein,
für einen normalverteilten Fehler ε ~
Variation des Trainings: nach enc(x) ein ε samplen, addieren, dann dec.
Oh: wie geht Backpropagation für “ein ε sampeln”?

<!-- Folie 27 -->
Probabilistische Modelle
Variation des Ziels: auch MSE(x, dec(enc(x) + ε)) möglichst klein,
für einen normalverteilten Fehler ε ~
Variation des Trainings: nach enc(x) ein ε samplen, addieren, dann dec.
Oh: wie geht Backpropagation für “ein ε sampeln”?
Da ε nicht von den Gewichten abhängt,
So:

<!-- Folie 28 -->
Probabilistische Modelle
Beispiel
Mit 3 Datenpunkten,
Bild im latenten Raum:
(klassisch)

<!-- Folie 29 -->
Probabilistische Modelle
Beispiel
Mit 3 Datenpunkten,
Variation
Bild im latenten Raum:
+ε

<!-- Folie 30 -->
Probabilistische Modelle
Beispiel
Mit 3 Datenpunkten,
2.Variation
Bild im latenten Raum:
+ 𝝈ε

<!-- Folie 31 -->
Probabilistische Modelle
Beispiel
Mit 300 Datenpunkten,
Bild im latenten Raum:
(klassisch)

<!-- Folie 32 -->
Probabilistische Modelle
Beispiel
Mit 300 Datenpunkten,
Bild im latenten Raum:
(wäre gut!)

<!-- Folie 33 -->
Probabilistische Modelle
Modelliere Verteilung mit Gaußscher Mischung im latenten Raum
Störung ε hängt von Daten ab:
Zu jedem Datenpunkt x ∊ D brauche zusätzlich zu enc(x) ∊ L
auch 𝝈x bzw. besser noch cov(x),
dann dec(enc(x) + ε) mit ε ~

<!-- Folie 34 -->
Probabilistische Modelle
Modelliere Verteilung mit Gaußscher Mischung im latenten Raum
Störung ε hängt von Daten ab:
Zu jedem Datenpunkt x ∊ D brauche zusätzlich zu enc(x) ∊ L
auch 𝝈x aber enc(x)+ε =:
Reparametrisierungstrick: statt
hängt von x ab.
besser y := enc(x)+𝝈xε

## Variational Autoencoder (VAE) - Training

<!-- Folie 35 -->
Wie trainiert man einen variational Autoencoder?
Für jeden Datenpunkt x ∊ D, berechne enc(x) = (𝛍x, 𝝈x)
generiere ein
und setze
.
Loss-Funktion ist naiv MSE(x, dec(y)).

<!-- Folie 36 -->
Wie trainiert man einen variational Autoencoder?
Für jeden Datenpunkt x ∊ D, berechne enc(x) = (𝛍x, 𝝈x)
generiere ein
und setze
.
Loss-Funktion ist naiv MSE(x, dec(y)).
Stabileres Training mit Extra-Term Variational Loss
wobei q(y|x) die Dichte der latenten Verteilung für ein festes x ist.

<!-- Folie 37 -->
Wie trainiert man einen variational Autoencoder?
Für jeden Datenpunkt x ∊ D, berechne enc(x) = (𝛍x, 𝝈x)
generiere ein
und setze
.
Loss-Funktion ist klug MSE(x, dec(y)) +
Dabei sind die beiden Standardnormalverteilungen nicht “die selben”!!

<!-- Folie 38 -->
Wie trainiert man einen variational Autoencoder?
Für jeden Datenpunkt x ∊ D, berechne enc(x) = (𝛍x, 𝝈x)
generiere ein
und setze
.
Loss-Funktion ist klug MSE(x, dec(y)) +
Dabei sind die beiden Standardnormalverteilungen nicht “die selben”!!
Diese Loss-Funktion ist genau der ELBO (evidence lower bound) L(θ,q)
→ Kapitel “Expectation Maximization” in Data Science

## Variational Autoencoder (VAE) - Recap

<!-- Folie 39 -->

<!-- Folie 40 -->
Grafik von Lilian Weng (ex-OpenAI)
→Blogpost
“From Autoencoder to Beta-VAE”
lilianweng.github.io/posts/2018-08-12-vae/
→ VAE sind heute noch Komponente der
Bildgeneratoren (Dall-E, Midjourney, etc.)

## Zeit für eine Pause?

<!-- Folie 41 -->

## word2vec

<!-- Folie 42 -->

## word2vec, von der Anwendung her gedacht

<!-- Folie 43 -->
Beispiel-Task, unsupervised mit neuronalen Netzen
1. Alle Dokumente Di einlesen als Liste von Wörtern
(getrennt an Leerzeichen; Satzzeichen entfernt).
2. Jedes einzelne Wort mit einem zuvor trainierten neuronalen Netz
umrechnen in eine andere Repräsentation.
3,4..
Die andere Repräsentation verschaffen wir uns durch latente Vektoren
aus einem Autoencoder.

## 2013

<!-- Folie 44 -->

## word2vec

<!-- Folie 45 -->
Vorverarbeitung, Ziel
1. Wir zählen alle Wörter (bzw. Token) im Korpus,

<!-- Folie 46 -->
Vorverarbeitung, Ziel
1. Wir zählen alle Wörter (bzw. Token) im Korpus,
2. entfernen Stopwords und sortieren nach Häufigkeit,
3. behalten die häufigsten N Wörter (z.B. N=5000),

<!-- Folie 47 -->
Vorverarbeitung, Ziel
1.
2.
3.
4.
Wir zählen alle Wörter (bzw. Token) im Korpus,
entfernen Stopwords und sortieren nach Häufigkeit,
behalten die häufigsten N Wörter (z.B. N=5000),
kodieren diese mit One-Hot-Encoding als Vektoren in ℝN

<!-- Folie 48 -->
Vorverarbeitung, Ziel
1.
2.
3.
4.
5.
6.
Wir zählen alle Wörter (bzw. Token) im Korpus,
entfernen Stopwords und sortieren nach Häufigkeit,
behalten die häufigsten N Wörter (z.B. N=5000),
kodieren diese mit One-Hot-Encoding als Vektoren in ℝN
mit dem Ziel, eine Abbildung e: ℝN→ℝK zu finden, K ≪ N (z.B. K=200)
mit einer “Decoder”-Abbildung d: ℝK→ℝN sodass
d(e(w)) = w für alle N Wörter unserer Liste gilt,

<!-- Folie 49 -->
Vorverarbeitung, Ziel
Wir zählen alle Wörter (bzw. Token) im Korpus,
entfernen Stopwords und sortieren nach Häufigkeit,
behalten die häufigsten N Wörter (z.B. N=5000),
kodieren diese mit One-Hot-Encoding als Vektoren in ℝN
mit dem Ziel, eine Abbildung e: ℝN→ℝK zu finden, K ≪ N (z.B. K=200)
mit einer “Decoder”-Abbildung d: ℝK→ℝN sodass
d(e(w)) = w für alle N Wörter unserer Liste gilt,
7. und semantisch ähnliche Wörter w1,w2 nach kodieren in ℝK
d( e(w1), e(w2) ) ≈ 0 erfüllen.
1.
2.
3.
4.
5.
6.

<!-- Folie 50 -->
Kernidee
Die Semantik eines Wortes ergibt sich durch seine Nutzung in Sätzen.

<!-- Folie 51 -->
Kernidee
Die Semantik eines Wortes ergibt sich durch seine Nutzung in Sätzen.
Beispiel:
“Die XYZ frisst ihr Futter am liebsten aus dem goldenen Napf”
kommt in Texten mit XYZ=Katze und XYZ=Hündin vor.

<!-- Folie 52 -->
Kernidee
Die Semantik eines Wortes ergibt sich durch seine Nutzung in Sätzen.
Beispiel:
“Die [MASK] frisst ihr Futter am liebsten aus dem goldenen Napf”
kommt in Texten mit [MASK]=Katze und [MASK]=Hündin vor.
Machine Learning Task, unsupervised:
Gegeben Text, ersetze ein Wort durch [MASK],
lasse vorhersagen was [MASK] ist (wie ein Denoising Autoencoder).

<!-- Folie 53 -->
Kernidee: CBOW
Continuous Bag of Words (für kleinere Corpora):
Hyperparameter Fenstergröße S (window size), z.B. S=2;
Eingabe: 2S+1 Token, die hintereinander im Text vorkommen,
dabei das mittlere durch [MASK] ersetzt → 2S One-Hot Vektoren
Ausgabe: Wahrscheinlichkeitsverteilung auf allen N Worten

<!-- Folie 54 -->
Kernidee: CBOW
Continuous Bag of Words (für kleinere Corpora):
Hyperparameter Fenstergröße S (window size), z.B. S=2;
Eingabe: 2S+1 Token, die hintereinander im Text vorkommen,
dabei das mittlere durch [MASK] ersetzt → 2S One-Hot Vektoren
Ausgabe: Wahrscheinlichkeitsverteilung auf allen N Worten
Loss-Funktion: negative Log Likelihood (NLL), d.h.
Vergleich der ausgegebenen Verteilung mit One-Hot für das Wort,
welches sich hinter [MASK] verbirgt.

<!-- Folie 55 -->
Kernidee: CBOW
Continuous Bag of Words (für kleinere Corpora):
Hyperparameter Fenstergröße S (window size), z.B. S=2;
Eingabe: 2S+1 Token, die hintereinander im Text vorkommen,
dabei das mittlere durch [MASK] ersetzt → 2S One-Hot Vektoren
Ausgabe: Wahrscheinlichkeitsverteilung auf allen N Worten
Loss-Funktion: negative Log Likelihood (NLL), d.h.
Vergleich der ausgegebenen Verteilung mit One-Hot für das Wort,
welches sich hinter [MASK] verbirgt.
Architektur: 1 Hidden Layer mit K Neuronen, der “Encoder”, W Averaging,
danach ein Layer “Decoder” mit N Neuronen gefolgt von Softmax.

<!-- Folie 56 -->
Kernidee: CBOW
Continuous Bag of Words (für kleinere Corpora):
Hyperparameter max. Fenstergröße S (window size), z.B. S=3;
Eingabe: ≤ S Token, die hintereinander im Text vorkommen,
dabei eins davon durch [MASK] ersetzt → ≤ S One-Hot Vektoren
Ausgabe: Wahrscheinlichkeitsverteilung auf allen N Worten
Loss-Funktion: negative Log Likelihood (NLL), d.h.
Vergleich der ausgegebenen Verteilung mit One-Hot für das Wort,
welches sich hinter [MASK] verbirgt.
Architektur: 1 Hidden Layer mit K Neuronen, der “Encoder”, W Averaging,
danach ein Layer “Decoder” mit N Neuronen gefolgt von Softmax.

<!-- Folie 57 -->
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

<!-- Folie 58 -->
skip-gram ← Alternative zu CBOW
Gegeben ein Token, sage Kontext vorher
Hyperparameter Fenstergröße S (window size), z.B. S=2;
Eingabe: Mittleres Token als One-Hot-Vektor für Abfolge von 2S+1 Token.
Ausgabe: Wahrscheinlichkeitsverteilung auf allen N Token

<!-- Folie 59 -->
skip-gram
Gegeben ein Token, sage Kontext vorher
Hyperparameter Fenstergröße S (window size), z.B. S=2;
Eingabe: Mittleres Token als One-Hot-Vektor für Abfolge von 2S+1 Token.
Ausgabe: Wahrscheinlichkeitsverteilung auf allen N Token
Loss-Funktion: negative Log Likelihood (NLL), d.h.
Vergleich der ausgegebenen Verteilung mit Summe der
One-Hot-Vektoren für alle 2S Kontexttoken.

<!-- Folie 60 -->
skip-gram
Gegeben ein Token, sage Kontext vorher
Hyperparameter Fenstergröße S (window size), z.B. S=2;
Eingabe: Mittleres Token als One-Hot-Vektor für Abfolge von 2S+1 Token.
Ausgabe: Wahrscheinlichkeitsverteilung auf allen N Token
Loss-Funktion: negative Log Likelihood (NLL), d.h.
Vergleich der ausgegebenen Verteilung mit Summe der
One-Hot-Vektoren für alle 2S Kontexttoken.
Architektur: 1 Hidden Linear Layer mit K Neuronen, der “Encoder”,
danach ein Layer “Decoder” mit N Neuronen gefolgt von Softmax.

<!-- Folie 61 -->
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

## word2vec benutzen

<!-- Folie 62 -->
Verfügbare Gewichte W
Mit Gensim:
z.B. wiki-english-20171001
Von HuggingFace:
z.B. word2vec-google-news-300
huggingface.co/fse/word2vec-google-news-300

<!-- Folie 63 -->
Klappt nicht gut?
Drop-in Ersatz für word2vec ist Facebook’s fasttext,
welches hauptsächlich einen geeigneteren Tokenizer benutzt
(Stichwort Subwordtokenization).

## word2vec selbst trainieren

<!-- Folie 64 -->
(ein ganz knapper Überblick)

<!-- Folie 65 -->
Zutatenliste
Keine GPU / andere Beschleuniger zur Hand? → Google Colab / CPU
Input:
◼ Textkorpus zum Training
◼ Tokenization-Strategie / Tokenizer (darüber sprechen wir noch)
◼ Dimension des Latent Space
◼ CBOW oder Skipgram (wie groß ist der Korpus?)
◼ Von Grund auf trainieren (Pretraining) oder Finetuning?
◼ Welche Implementierung?

<!-- Folie 66 -->
Gensim
https://radimrehurek.com/gensim/auto_examples/tutorials/run_word2vec.html#training-your-own-model
◼ Pro Gensim:
◼
NLP-Gesamtlösung, gut dokumentiertes Paket.
◼ Contra Gensim:
◼
Keine GPU-Beschleunigung (aber für word2vec ist das “egal”).
◼
Keine Kombination von word2vec im Training mit anderen Tasks
(wie wir es beim Denoising Label Autoencoder getan haben)

<!-- Folie 67 -->
PyTorch
“So richtig von Hand”:
→https://www.kaggle.com/code/karthur10/skip-gram-implementation-with-pytorch-step-by-step/notebook
Mit torch.nn.Embedding Layer:
→https://muhark.github.io/python/ml/nlp/2021/10/21/word2vec-from-scratch.html
→https://d2l.ai/chapter_natural-language-processing-pretraining/word2vec-pretraining.html

<!-- Folie 68 -->
Wozu?
Was lässt sich durch Pretraining oder Finetuning von
word2vec-Modellen mit PyTorch erreichen?

## NLP

<!-- Folie 69 -->

<!-- Folie 70 -->
Beispiel-Task
Gegeben ist eine Menge von N (kurzen) Dokumenten
(z.B. Tweets, Webseiten, Hausarbeiten)
{ D1, …, DN }.
Gesucht sind k Paare ähnlicher Dokumente (k ≪ N)
(z.B. Tweets thematisch gruppieren, Plagiate finden)
{ (x1, y1), …, (xk, yk) }
wobei dies Paare von Indizes sind, sodass Dxi und Dyi ähnlich sind.

<!-- Folie 71 -->
Beispiel-Task
Gegeben ist eine Menge von N (kurzen) Dokumenten
{ D1, …, DN }.
Gesucht sind k Paare ähnlicher Dokumente (k ≪ N)
{ (x1, y1), …, (xk, yk) }
wobei dies Paare von Indizes sind, sodass Dxi und Dyi ähnlich sind.
Klassischer Ansatz:
Wörter in Di zählen,
Häufigkeitsverteilungen von Di und Dj vergleichen.

<!-- Folie 72 -->
Beispiel-Task
Gegeben ist eine Menge von N (kurzen) Dokumenten
{ D1, …, DN }.
Gesucht sind k Paare ähnlicher Dokumente (k ≪ N)
Klassischer Ansatz:
Wörter in Di zählen,
Häufigkeitsverteilungen von Di und Dj vergleichen.
Probleme mit diesem Ansatz:
1. “Katze isst Maus” und “Maus isst Katze” sind ununterscheidbar.
2. “Schwimmen” und “schwamm” haben nichts miteinander zu tun.
3. “Hund” und “Tier” haben nichts miteinander zu tun.
4. Wörter wie “der”, ”die”, ”das” sind sehr häufig, aber bedeutungslos.

<!-- Folie 73 -->
Beispiel-Task; Zusammenfassung klassische Probleme
Probleme mit Worthäufigkeitsverteilungsvergleich:
1. “Katze isst Maus” und “Maus isst Katze” sind ununterscheidbar.
2. “Schwimmen” und “schwamm” haben nichts miteinander zu tun.
3. “Hund” und “Tier” haben nichts miteinander zu tun.
4. Wörter wie “der”, ”die”, ”das” sind sehr häufig, aber bedeutungslos.
Lösungsansätze:
1. n-Gramme statt Worte betrachten
2. Lemmatisierung
3. Komplexe Ontologien (formalisiertes Wissen)
4. Stopwords entfernen

<!-- Folie 74 -->
Wörter? Token!
Alternative Lösung zu Problem 2 (statt Lemmatisierung):
◼ Buchstaben/Zeichen anstelle von Wörtern als “Atome”

<!-- Folie 75 -->
Wörter? Token!
Alternative Lösung zu Problem 2 (statt Lemmatisierung):
◼ Buchstaben/Zeichen anstelle von Wörtern als “Atome”
◼ n-Gramme davon

<!-- Folie 76 -->
Wörter? Token!
Alternative Lösung zu Problem 2 (statt Lemmatisierung):
◼ Buchstaben/Zeichen anstelle von Wörtern als “Atome”
◼ n-Gramme davon (z.B. Trigramme, n=3)
Beispiel “schwimm!” und “schwimmen”
[“sch”, “chw”, “hwi”, “wim”, “imm”, “mm!”] und
[“sch”, “chw”, “hwi”, “wim”, “imm”, “mme”, “men”]
haben sehr ähnliche Trigrammhäufigkeitsverteilungen.

<!-- Folie 77 -->
Wörter? Token!
Alternative Lösung zu Problem 2 (statt Lemmatisierung):
◼ Buchstaben/Zeichen anstelle von Wörtern als “Atome” (=Token)
◼ n-Gramme davon (z.B. Trigramme, n=3)
Konkret zu klärende Fragen:
◼ Leerzeichen wie jedes andere Zeichen behandeln?
◼
◼
→ Tokenisierungsstrategie, Tokenizer

<!-- Folie 78 -->
Wörter? Token!
Alternative Lösung zu Problem 2 (statt Lemmatisierung):
◼ Buchstaben/Zeichen anstelle von Wörtern als “Atome” (=Token)
◼ n-Gramme davon (z.B. Trigramme, n=3)
Konkret zu klärende Fragen:
◼ Leerzeichen wie jedes andere Zeichen behandeln?
◼ Über das Satzende “.” hinaus?
◼
→ Tokenisierungsstrategie, Tokenizer

<!-- Folie 79 -->
Wörter? Token!
Alternative Lösung zu Problem 2 (statt Lemmatisierung):
◼ Buchstaben/Zeichen anstelle von Wörtern als “Atome” (=Token)
◼ n-Gramme davon (z.B. Trigramme, n=3)
Konkret zu klärende Fragen:
◼ Leerzeichen wie jedes andere Zeichen behandeln?
◼ Über das Satzende “.” hinaus?
◼ Flexibles n, z.B. Silben statt Buchstabentrigramme?
→ Tokenisierungsstrategie, Tokenizer

<!-- Folie 80 -->
Wörter? Token!
Der Einfachheit halber bleiben wir bei Token=Wörter,
d.h. wir löschen Satzzeichen und trennen an Leerzeichen.

<!-- Folie 81 -->
Literatur und Softwarepakete
◼ Das modernste Lehrbuch ist
Dan Jurafsky, James H. Martin: Speech and Language Processing
Es gibt einen “Third Edition Draft” von August 2024 frei verfügbar:
https://web.stanford.edu/~jurafsky/slp3/
◼ Das Python Natural Language Toolkit (NLTK)
https://www.nltk.org/book/
Enthält z.B. den PunktTokenizer, der so arbeitet wie wir jetzt.
◼ Radim Řehůřek’s (&Koautoren) gensim Bibliothek für Python
https://radimrehurek.com/gensim/auto_examples/index.html

<!-- Folie 82 -->
Beispiel-Task
Gegeben ist eine Menge von N (kurzen) Dokumenten
{ D1, …, DN }.
Gesucht sind k Paare ähnlicher Dokumente (k ≪ N)
{ (x1, y1), …, (xk, yk) }
wobei dies Paare von Indizes sind, sodass Dxi und Dyi ähnlich sind.
Modernerer Ansatz (supervised):
Mit einem neuronalen Netz; Menschen labeln Ähnlichkeit.
Eingabe: Paare (Di, Dj). Ausgabe: Ähnlichkeitsschätzung.

<!-- Folie 83 -->
Beispiel-Task, unsupervised mit neuronalen Netzen
1. Alle Dokumente Di einlesen als Liste von Wörtern
(getrennt an Leerzeichen; Satzzeichen entfernt).
2. Jedes einzelne Wort mit einem zuvor trainierten neuronalen Netz
umrechnen in eine andere Repräsentation,
die sich besser vergleichen lässt.

<!-- Folie 84 -->
Beispiel-Task, unsupervised mit neuronalen Netzen
1. Alle Dokumente Di einlesen als Liste von Wörtern
(getrennt an Leerzeichen; Satzzeichen entfernt).
2. Jedes einzelne Wort mit einem zuvor trainierten neuronalen Netz
umrechnen in eine andere Repräsentation,
die sich besser vergleichen lässt.
3. Für jedes Paar (Di, Dj) die Listen von Repräsentationen vergleichen,
daraus ein Ähnlichkeitsmaß für das Paar berechnen.
4. Die Top k ähnlichsten Paare ausgeben.
