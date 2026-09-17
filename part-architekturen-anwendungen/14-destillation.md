---
title: "VL 14: Destillation"
short_title: "VL 14"
---

# Destillation

:::{warning} Rohfassung
Dieses Kapitel ist eine automatische Transkription der Folien von VL 14 aus dem WiSe 2025/26
(`from_2025/slides/Einführung in Deep Learning 2025_26 VL 14_ Destillation.pdf`), Folie für Folie in der Originalreihenfolge.
Formeln und Abbildungen sind dabei größtenteils verloren gegangen; der Text ist noch nicht überarbeitet.
:::

## Was lernen wir beim Deep

<!-- Folie 2 -->
Learning eigentlich?

## Zwei Ansätze

<!-- Folie 3 -->
Ansatz 1: Regression zu bekannter Funktion
Wenn eine Funktion der Daten bekannt ist,
also f : ℝn → ℝm für Datenpunkte x1,...,xN∊ ℝn
bekannt (yi=f(xi) liegen vor) oder billig zu berechnen ist,
können wir ein neuronales Netz N trainieren sodass
N(xi) ≈ yi ist.

<!-- Folie 4 -->
Ansatz 1: Regression zu bekannter Funktion
Wenn eine Funktion der Daten bekannt ist,
also f : ℝn → ℝm für Datenpunkte x1,...,xN∊ ℝn
bekannt (yi=f(xi) liegen vor) oder billig zu berechnen ist,
können wir ein neuronales Netz N trainieren sodass
N(xi) ≈ yi ist.
(Regression, MSE Loss)
Analog für c : ℝn → {0, 1} eine Klassifikation,
wenn yi=c(xi) bekannt sind, lässt sich N trainieren sodass
N(xi) = yi in möglichst vielen Fällen.
(Klassifikation, BCE Loss)

<!-- Folie 5 -->
Ansatz 1: Regression zu bekannter Funktion
Problem: manchmal kennen wir die Funktion f bzw. c nicht
z.B. wenn wir Daten ohne Label haben (aber klassifizieren/clustern wollen)

<!-- Folie 6 -->
Ansatz 1: Regression zu bekannter Funktion
Problem: manchmal kennen wir die Funktion f bzw. c nicht
z.B. wenn wir Daten ohne Label haben (aber klassifizieren/clustern wollen)
Oder wenn die gesuchte Funktion f komplizierter ist, z.B.
Wenn die Eingabe x eine Sequenz von Token x1,...,xk repräsentiert und
f(x1,...,xk) := P(xk | x1,...,xk-1)
Die Wahrscheinlichkeit, eine Sequenz x1,...,xk vorzufinden,
wenn man x1,...,xk-1 gesehen hat.
(next Token prediction)

<!-- Folie 7 -->
Ansatz 1: Regression zu bekannter Funktion
Problem: manchmal kennen wir die Funktion f bzw. c nicht
z.B. wenn wir Daten ohne Label haben (aber klassifizieren/clustern wollen)
Oder wenn die gesuchte Funktion f komplizierter ist, z.B.
Wenn die Eingabe x eine Sequenz von Token x1,...,xk repräsentiert und
f(x1,...,xk) := P(xk | x1,...,xk-1)
Die Wahrscheinlichkeit, eine Sequenz x1,...,xk vorzufinden,
wenn man x1,...,xk-1 gesehen hat.
(next Token prediction)
→ kann man immer noch aus den Daten schätzen, aber relativ teuer.

<!-- Folie 8 -->
Ansatz 2: Regression zu unbekannter Funktion
Beispiel Autoencoder:
Wir trainieren eine Regression des neuronalen Netzes N auf die Identitätsfunktion
(wie in Ansatz 1) aber N = D ○ E (decoder nach encoder mit Bottleneck dazwischen).
Die Abbildung E : ℝn → ℝm, die der Encoder lernt, ist vor dem Training völlig unbekannt.

<!-- Folie 9 -->
Ansatz 2: Regression zu unbekannter Funktion
Beispiel Autoencoder:
Wir trainieren eine Regression des neuronalen Netzes N auf die Identitätsfunktion
(wie in Ansatz 1) aber N = D ○ E (decoder nach encoder mit Bottleneck dazwischen).
Die Abbildung E : ℝn → ℝm, die der Encoder lernt, ist vor dem Training völlig unbekannt.
Es gibt mehr als eine “korrekte” solche Abbildung.
Die Menge aller möglichen Funktionen f : ℝn → ℝm ist sehr groß,
Welche Teilmenge zu sinnvollen Encodern gehört, ist a priori unklar.

## Model Compression

<!-- Folie 10 -->

## Zwei Ansätze vereint

<!-- Folie 11 -->
Suchproblem und Regression
Die Suche nach der richtigen Funktion braucht viel Platz / Flexibilität,
daher sind große (tiefe) neuronale Netze besser geeignet zum Lernen unbekannter
Funktionen.

<!-- Folie 12 -->
Suchproblem und Regression
Die Suche nach der richtigen Funktion braucht viel Platz / Flexibilität,
daher sind große (tiefe) neuronale Netze besser geeignet zum Lernen unbekannter
Funktionen.
Eine Regression auf eine bekannte Funktion braucht nicht viel Flexibilität,
daher lassen sich auch flache neuronale Netze einsetzen;
die benötigte Komplexität hängt nur von der Funktion ab,
nicht davon, wie schwer es ist, diese zu erraten.

<!-- Folie 13 -->
Suchproblem und Regression
Strategie 1: Pruning
Beim Pruning (Abschneiden) werden Bereiche des neuronalen Netzes identifiziert, die
wenig zur Berechnung beitragen, und entfernt (Gewichte auf 0 gesetzt, Layer entfernt).

<!-- Folie 14 -->
Suchproblem und Regression
Strategie 1: Pruning
Beim Pruning (Abschneiden) werden Bereiche des neuronalen Netzes identifiziert, die
wenig zur Berechnung beitragen, und entfernt (Gewichte auf 0 gesetzt, Layer entfernt).
Es ist schwierig, auszuwählen, was weg kann.
Nach dem entfernen “unwichtiger” Teile ist oft ein Finetuning erforderlich.

<!-- Folie 15 -->
Suchproblem und Regression
Strategie 2: Destillation
Beim Destillieren wird ein kleineres “Schüler”-Netzwerk trainiert mit Hilfe eines größeren
“Lehrer”-Netzwerks (welches zuvor teuer trainiert wurde).

<!-- Folie 16 -->
Suchproblem und Regression
Strategie 2: Destillation
Beim Destillieren wird ein kleineres “Schüler”-Netzwerk trainiert mit Hilfe eines größeren
“Lehrer”-Netzwerks (welches zuvor teuer trainiert wurde).
Dabei gibt es 3 wesentliche Ansätze:
1.
Lehrer-Labels auf Daten ermöglichen supervised Training der Schüler.
(Lehrer-Training ist “Suche”, Schüler-Training ist “Regression”)

<!-- Folie 17 -->
Suchproblem und Regression
Strategie 2: Destillation
Beim Destillieren wird ein kleineres “Schüler”-Netzwerk trainiert mit Hilfe eines größeren
“Lehrer”-Netzwerks (welches zuvor teuer trainiert wurde).
Dabei gibt es 3 wesentliche Ansätze:
1.
2.
Lehrer-Labels auf Daten ermöglichen supervised Training der Schüler.
(Lehrer-Training ist “Suche”, Schüler-Training ist “Regression”)
Synthetische Daten, generiert durch Lehrer-Netzwerk, beschleunigen Schüler-Training.

<!-- Folie 18 -->
Suchproblem und Regression
Strategie 2: Destillation
Beim Destillieren wird ein kleineres “Schüler”-Netzwerk trainiert mit Hilfe eines größeren
“Lehrer”-Netzwerks (welches zuvor teuer trainiert wurde).
Dabei gibt es 3 wesentliche Ansätze:
1.
2.
3.
Lehrer-Labels auf Daten ermöglichen supervised Training der Schüler.
(Lehrer-Training ist “Suche”, Schüler-Training ist “Regression”)
Synthetische Daten, generiert durch Lehrer-Netzwerk, beschleunigen Schüler-Training.
Schüler lernt direkt aus den Logits das darin verborgene Wissen.
(Destillation)

## Vorläufer: Ensemble Model Compression

<!-- Folie 19 -->
Buciluă, Caruana, Niculescu-Mizil: Model
Compression (2006)
1.
2.
3.
4.
Trainiere ein großes Ensemble-Modell
(z.B. Random Forest, XGBoost) auf
den Daten,
Generiere synthetische Eingabedaten,
Generiere Labels mit dem trainierten
Ensemble-Modell,
Trainiere ein neuronales Netz auf den
neuen, viel umfangreicheren Daten.

<!-- Folie 20 -->
Buciluă, Caruana, Niculescu-Mizil: Model
Compression (2006)
1.
2.
3.
4.
Trainiere ein großes Ensemble-Modell
(z.B. Random Forest, XGBoost) auf
den Daten,
Generiere synthetische Eingabedaten,
Generiere Labels mit dem trainierten
Ensemble-Modell,
Trainiere ein neuronales Netz auf den
neuen, viel umfangreicheren Daten.
Das Training wirkt regularisierend,
das neuronale Netz verallgemeinert besser.

## Wie deep muss es sein?

<!-- Folie 21 -->
Ba, Caruana: Do Deep Nets Really Need to
be Deep? (2013)
Wie muss ein neuronales Netz aufgestellt
sein (Architektur), um eine Funktion zu
lernen?
1.
2.
Expressivity:
Ist das Netz komplex genug,
Um die Funktion abzubilden?
Learnability:
Kann der Gradientenabstieg diese
Funktion im großen Suchraum finden?

<!-- Folie 22 -->
Ba, Caruana: Do Deep Nets Really Need to
be Deep? (2013)
Wie muss ein neuronales Netz aufgestellt
sein (Architektur), um eine Funktion zu
lernen?
Ergebnisse:
1.
Expressivity ist nicht das Problem
(vgl. Universal Approximation),
Flache+breite Netzwerke sind stark.
2.
Expressivity:
Ist das Netz komplex genug,
Um die Funktion abzubilden?
Learnability:
Kann der Gradientenabstieg diese
Funktion im großen Suchraum finden?
Learnability ist das Problem flacher Netze.

## Model Distillation

<!-- Folie 23 -->

## Distillation Loss

<!-- Folie 24 -->
Hinton, Vinyals, Dean: Distilling the
Knowledge in a Neural Network (2015)
Für eine k-Klassen-Klassifikationsaufgabe
ist der letzte Schritt im großen
Lehrer-Modell ein Softmax : ℝk → [0,1]k
gefolgt von der “harten” Klassifikation
argmax, um zu einem Klassenurteil zu
kommen.

<!-- Folie 25 -->
Hinton, Vinyals, Dean: Distilling the
Knowledge in a Neural Network (2015)
Für eine k-Klassen-Klassifikationsaufgabe
ist der letzte Schritt im großen
Lehrer-Modell ein Softmax : ℝk → [0,1]k
gefolgt von der “harten” Klassifikation
argmax, um zu einem Klassenurteil zu
kommen.
Idee: lerne nicht aus dem harten, sondern
dem weichen Urteil. Mach es weicher.

<!-- Folie 26 -->
Hinton, Vinyals, Dean: Distilling the
Knowledge in a Neural Network (2015)
Für eine k-Klassen-Klassifikationsaufgabe
ist der letzte Schritt im großen
Lehrer-Modell ein Softmax : ℝk → [0,1]k
gefolgt von der “harten” Klassifikation
argmax, um zu einem Klassenurteil zu
kommen.
Loss-Funktion zum Schüler-Training:
KL-Divergenz (relative Entropie)
Schüler-Verteilung vs. Lehrer-Verteilung
reskaliert mit Temperatur:
Idee: lerne nicht aus dem harten, sondern
dem weichen Urteil. Mach es weicher.

## Dark Knowledge

<!-- Folie 27 -->
Beispiel:
Fehlerhaft gelabelte Daten, z.B.
Ein Hund x mit dem Label “Katze”.
Lehrer klassifiziert “Katze” nach dem
Lernen (leider falsch).

<!-- Folie 28 -->
Beispiel:
Fehlerhaft gelabelte Daten, z.B.
Ein Hund x mit dem Label “Katze”.
Aber: vor dem argmax sehen wir
vermutlich:
Lehrer klassifiziert “Katze” nach dem
Lernen (leider falsch).
P(x = Hund) > 0
D.h. in P(x = Hund) steckt noch
Information, “dunkles Wissen”.

<!-- Folie 29 -->
Beispiel:
Fehlerhaft gelabelte Daten, z.B.
Ein Hund x mit dem Label “Katze”.
Aber: vor dem argmax sehen wir
vermutlich:
Lehrer klassifiziert “Katze” nach dem
Lernen (leider falsch).
P(x = Hund) > 0
Schüler lernt aus dunklem Wissen,
leidet weniger unter falschen Labels.
D.h. in P(x = Hund) steckt noch
Information, “dunkles Wissen”.

## Schüler übertreffen Lehrer

<!-- Folie 30 -->
Furlanello, Lipton, Tschannen, Itti,
Anandkumar: Born Again Neural Networks
(2018)
(inspiriert von “born again trees” aus 1996)
Das Schüler-Netzwerk ist nicht nur kleiner
und damit schneller, billiger als das
Lehrer-Netzwerk - es kann sogar besser
werden.

<!-- Folie 31 -->
Furlanello, Lipton, Tschannen, Itti,
Anandkumar: Born Again Neural Networks
(2018)
(inspiriert von “born again trees” aus 1996)
Implizite Neugewichtung der
Trainingsdaten führt zu Fokus auf “schwere
Fälle”, Loss berücksichtigt weniger den
einfachen Teil der Aufgabe.
Das Schüler-Netzwerk ist nicht nur kleiner
und damit schneller, billiger als das
Lehrer-Netzwerk - es kann sogar besser
werden.
Knowledge Distillation als
Regularisierung/Optimierung statt nur
Kompression.
(Ensemble aus Generationen von Schülern)

## DistilBERT

<!-- Folie 32 -->
Sanh, Debut, Chaumond, Wolf: DistilBERT,
a distilled version of BERT: smaller, faster,
cheaper and lighter (2019)
“we leverage knowledge distillation during the
pre-training phase and show that it is possible
to reduce the size of a BERT model by 40%,
while retaining 97% of its language
understanding capabilities and being 60%
faster. To leverage the inductive biases
learned by larger models during pre-training,
we introduce a triple loss combining language
modeling, distillation and cosine-distance
losses.”

<!-- Folie 33 -->
Sanh, Debut, Chaumond, Wolf: DistilBERT,
a distilled version of BERT: smaller, faster,
cheaper and lighter (2019)
“we leverage knowledge distillation during the
pre-training phase and show that it is possible
to reduce the size of a BERT model by 40%,
while retaining 97% of its language
understanding capabilities and being 60%
faster. To leverage the inductive biases
learned by larger models during pre-training,
we introduce a triple loss combining language
modeling, distillation and cosine-distance
losses.”
DistilBERT := jeder zweite Layer von BERT
Loss = Summe aus drei Teilen:
◼
Distillation Loss
◼
Masked Language Modeling Loss
◼
Cosine-Distance Loss

<!-- Folie 34 -->
Sanh, Debut, Chaumond, Wolf: DistilBERT,
a distilled version of BERT: smaller, faster,
cheaper and lighter (2019)
“we leverage knowledge distillation during the
pre-training phase and show that it is possible
to reduce the size of a BERT model by 40%,
while retaining 97% of its language
understanding capabilities and being 60%
faster. To leverage the inductive biases
learned by larger models during pre-training,
we introduce a triple loss combining language
modeling, distillation and cosine-distance
losses.”
DistilBERT := jeder zweite Layer von BERT
Loss = Summe aus drei Teilen:
◼
Distillation Loss
(KL-Divergenz zu
Temperatur-skalierten Logits)
◼
Masked Language Modeling Loss
◼
Cosine-Distance Loss

<!-- Folie 35 -->
Sanh, Debut, Chaumond, Wolf: DistilBERT,
a distilled version of BERT: smaller, faster,
cheaper and lighter (2019)
“we leverage knowledge distillation during the
pre-training phase and show that it is possible
to reduce the size of a BERT model by 40%,
while retaining 97% of its language
understanding capabilities and being 60%
faster. To leverage the inductive biases
learned by larger models during pre-training,
we introduce a triple loss combining language
modeling, distillation and cosine-distance
losses.”
DistilBERT := jeder zweite Layer von BERT
Loss = Summe aus drei Teilen:
◼
Distillation Loss
(KL-Divergenz zu
Temperatur-skalierten Logits)
◼
Masked Language Modeling Loss
(wie BERT, lernen aus den Daten,
mit Temperatur 1)
◼
Cosine-Distance Loss

<!-- Folie 36 -->
Sanh, Debut, Chaumond, Wolf: DistilBERT,
a distilled version of BERT: smaller, faster,
cheaper and lighter (2019)
“we leverage knowledge distillation during the
pre-training phase and show that it is possible
to reduce the size of a BERT model by 40%,
while retaining 97% of its language
understanding capabilities and being 60%
faster. To leverage the inductive biases
learned by larger models during pre-training,
we introduce a triple loss combining language
modeling, distillation and cosine-distance
losses.”
DistilBERT := jeder zweite Layer von BERT
Loss = Summe aus drei Teilen:
◼
Distillation Loss
(KL-Divergenz zu
Temperatur-skalierten Logits)
◼
Masked Language Modeling Loss
(wie BERT, lernen aus den Daten,
mit Temperatur 1)
◼
Cosine-Distance Loss
(latente Mannigfaltigkeiten
beibehalten: Outputs der Layer im
Kosinusabstand vergleichen)

## Anwendung: Speculative Decoding

<!-- Folie 37 -->
Vgl. Yan, Agarwal, Venkataraman:
Decoding Speculative Decoding (2024)
Problem: Das (autoregressive) Sampling
eines nächsten Token mit einem LLM ist
teuer, benötigt aber ein Ergebnis um das
darauf folgende Token zu sampeln.

<!-- Folie 38 -->
Vgl. Yan, Agarwal, Venkataraman:
Decoding Speculative Decoding (2024)
Problem: Das (autoregressive) Sampling
eines nächsten Token mit einem LLM ist
teuer, benötigt aber ein Ergebnis um das
darauf folgende Token zu sampeln.
Trick: rate die kommenden 5 Token mit
einem kleinen billigen Modell, verifiziere mit
dem teuren LLM.
Trick 2: billiges Modell destilliert vom LLM.

## Anwendung: SDXL Turbo

<!-- Folie 39 -->
Sauer, Lorenz, Blattmann, Rombach:
Adversarial Diffusion Distillation (2023)
Aus einem vortrainierten tiefen
Diffusionsmodell (SDXL) zum Generieren
von Bildern aus Bildbeschreibungen in
einem k-Schritte-Iterationsprozess des
Entrauschens;
Destilliere ein 1-Schritt-Modell,
mit Destillation Loss und Adverserial Loss
(GAN Training)

## Anwendung: Gemini Flash

<!-- Folie 40 -->
Google Gemini Team: Gemini 1.5:
Unlocking multimodal understanding across
millions of tokens of context (2024)
Auch Google benutzt Destillation, um aus
dem großen, teuren Gemini 1.5 Pro das
günstigere, schnellere Gemini 1.5 Flash zu
destillieren.
(Analog: OpenAIs GPT-Mini Modelle)

## Anwendung: Chain of Thought

<!-- Folie 41 -->
1.
Bringe ein LLM dazu,
länger/mehr nachzudenken
(= mehr Output zu produzieren),
Die “Chain of Thought”
(warum diese Antwort, Begründungen)
2.
Verstecke langwierige/schlechte
Zwischenüberlegungen,
lass Schüler aus den
“wohlüberlegten” Inhalten lernen
mit Destillation.

## Vibecoding Deep Learning

<!-- Folie 42 -->

<!-- Folie 43 -->
Wir schauen uns praktisch an, wie man mit generiertem Code arbeiten kann.
Beispiel-Aufgabe:
Gegeben eine Liste besuchter/gekaufter Items (Artikel, Produkte) pro Nutzer,
empfehle einem neuen Nutzer ein Item,
welches interessant ist (mit hoher Wahrscheinlichkeit angeklickt/gekauft wird).
