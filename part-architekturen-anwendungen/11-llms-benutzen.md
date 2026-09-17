---
title: "VL 11: LLMs benutzen"
short_title: "VL 11"
---

# LLMs benutzen

:::{warning} Rohfassung
Dieses Kapitel ist eine automatische Transkription der Folien von VL 11 aus dem WiSe 2025/26
(`from_2025/slides/Einführung in Deep Learning 2025_26 VL 11_ LLMs benutzen.pdf`), Folie für Folie in der Originalreihenfolge.
Formeln und Abbildungen sind dabei größtenteils verloren gegangen; der Text ist noch nicht überarbeitet.
:::

## Recap & Vertiefung:

<!-- Folie 2 -->
Backpropagation (im Notebook)

## Recap & Vertiefung: Universalität

<!-- Folie 3 -->

## Warum Neuronale Netze funktionieren

<!-- Folie 4 -->
Universelles Approximationstheorem, Überblick
Grobe Aussage:
Mit neuronalen Netzen
(beliebig viele Neuronen, beliebig viele Layer, fully connected, ReLU)
lässt sich jede Funktion berechnen.

<!-- Folie 5 -->
Universelles Approximationstheorem, Überblick
Grobe Aussage:
(wir erinnern uns!)
Mit neuronalen Netzen
(beliebig viele Neuronen, beliebig viele Layer, fully connected, ReLU)
lässt sich jede Funktion berechnen.
beliebig gut approximieren

<!-- Folie 6 -->
Universelles Approximationstheorem, Schritt 1
Jede beschränkte messbare Funktion f : E ⊆ ℝ → ℝ
ist beliebig gut (∀ε>0) durch einfache Funktionen g, h approximierbar:
g ≤ f ≤ h und 0 ≤ h-g < ε
Stetige Funktionen sind integrierbar,
integrierbare Funktionen sind messbar.
Einfache Funktionen sind endliche Linearkombinationen
von Indikatorfunktionen messbarer Mengen.

<!-- Folie 7 -->
Universelles Approximationstheorem, Schritt 2
Jede Funktion f : E ⊆ ℝ → ℝ
(für E eine messbare Menge)
Ist messbar genau dann wenn
es eine Folge einfache Funktionen fn gibt,
die gegen f punktweise konvergieren und |fn| ≤ |f| erfüllen.
Eine messbare Funktion f ist integrierbar,
wenn es eine dominierende integrierbare Funktion h gibt,
Also |f| ≤ |h|.
Wir können also sagen: {messbare Funktionen} ≈ {interessante Fkt.}

<!-- Folie 8 -->
Universelles Approximationstheorem, Schritt 3
Jede einfache Funktion f : E ⊆ ℝ → ℝ
ist beliebig genau approximierbar durch Stufenfunktionen,
d.h. eine endliche Linearkombination
von Indikatorfunktionen von Intervallen.
Wir können also sagen:
{messbare Funktionen} ≈ {approximierbar mit Stufenfunktionen}

<!-- Folie 9 -->
Universelles Approximationstheorem, Schritt 4
Eine einzelne Stufe lässt sich mit einem
einfachen neuronalen Netz realisieren:
Grafik von
Michael Nielsen

<!-- Folie 10 -->
Universelles Approximationstheorem, Schritt 5
Die leicht zu verstehende Konstruktion mit 2 Hidden Layer bei Michael
Nielsen funktioniert auch mit beliebig hoher Ein- und
Ausgabedimension, also zur Approximation von Funktionen ℝn → ℝn.
Es gibt auch Konstruktionen mit nur 1 Hidden Layer.
Die richtige Frage ist also nie “geht das mit neuronalen Netzen?”
(Antwort: JA) sondern
“(Wie) geht das am effizientesten mit neuronalen Netzen?”

<!-- Folie 11 -->
Universelle Approximationstheoreme: Präzisere Ergebnisse
Satz. Sei E ⊆ ℝd eine kompakte (d.h. beschränkte und
abgeschlossene) Teilmenge. Sei 𝜎 : ℝ → ℝ eine beliebige
stetige Funktion, aber keine affin-lineare Abbildung, die in
wenigstens einem Punkt stetig differenzierbar mit Ableitung
ungleich 0 ist. Dann gibt es zu jeder stetigen Funktion
f : E → ℝD und jedem ε ein neuronales Netz n mit
Aktivierungen 𝜎 und endlich vielen hidden Layern, je
höchstens d+D+2 groß, mit
supx∊E || n(x) - f(x) || < ε.

<!-- Folie 12 -->
Universelle Approximationstheoreme: Noch präziser!
Satz. Es gibt eine Konstante c sodass gilt:
Zu jeder k-fach stetig differenzierbaren Funktion
f : E → ℝD und jedem ε gibt es ein neuronales Netz n mit
ReLU-Aktivierungen und c log(1/ε) vielen hidden Layern,
insgesamt etwa c ε-d/k Gewichte insgesamt und
supx∊E || n(x) - f(x) || < ε.
[Yarotsky (2017)], s.a. arXiv:1901.10267

## Neuronale Netze vs. Bäume und Wälder

<!-- Folie 13 -->
Entscheidungsbäume aus neuronalen Netzen
Quelle: Neural Networks are Decision Trees, Caglar Aytekin 2022

## Transformer LLMs in der Praxis

<!-- Folie 14 -->
einsetzen

## Transformer technisch

<!-- Folie 15 -->
Aufbau
Quelle: Fig. 1 in
“Attention is all you need”

## Verschiedene Wege, LLMs zu nutzen

<!-- Folie 16 -->
◼
Wort-Vektor-Einbettungen direkt verwenden (statt word2vec z.B. Gemma)
→ semantische Ähnlichkeit, semantische Suche, semantisches Clustering etc.
Pro: sehr billig (keine tiefen Modelle für Inferenz notwendig)
Contra: Zusammenhänge über längere Texte hinweg nicht sichtbar

<!-- Folie 17 -->
◼
Wort-Vektor-Einbettungen direkt verwenden (statt word2vec z.B. Gemma)
→ semantische Ähnlichkeit, semantische Suche, semantisches Clustering etc.
Pro: sehr billig (keine tiefen Modelle für Inferenz notwendig)
Contra: Zusammenhänge über längere Texte hinweg nicht sichtbar
Für die (kommende) Aufzählung konkretisieren wir anhand eines Beispiel-Tasks,
z.B. “Gegeben einen Text, identifiziere ob emotional positiv oder negativ gefärbt”

<!-- Folie 18 -->
◼
◼
Wort-Vektor-Einbettungen direkt verwenden (statt word2vec z.B. Gemma)
→ semantische Ähnlichkeit, semantische Suche, semantisches Clustering etc.
Satz-Vektor-Einbettungen bzw. längere Texte in Vektoren umwandeln (z.B. BERT)
Pro: sehr hohe Qualität der Repräsentationen
Contra: LLM notwendig zur Berechnung der Repräsentationen

<!-- Folie 19 -->
◼
◼
◼
Wort-Vektor-Einbettungen direkt verwenden (statt word2vec z.B. Gemma)
→ semantische Ähnlichkeit, semantische Suche, semantisches Clustering etc.
Satz-Vektor-Einbettungen bzw. längere Texte in Vektoren umwandeln (z.B. BERT)
Nicht Token sampeln sondern die Verteilung der Ausgabetoken direkt betrachten
Pro: Vollständige Information aus dem LLM, kein “zufälliges” Sampling
Contra: Weniger intuitiv zu verwenden,
man arbeitet mit Verteilungen im latent Space statt mit Text

<!-- Folie 20 -->
◼
◼
◼
◼
Wort-Vektor-Einbettungen direkt verwenden (statt word2vec z.B. Gemma)
→ semantische Ähnlichkeit, semantische Suche, semantisches Clustering etc.
Satz-Vektor-Einbettungen bzw. längere Texte in Vektoren umwandeln (z.B. BERT)
Nicht Token sampeln sondern die Verteilung der Ausgabetoken direkt betrachten
Fertig trainierte Transformer mit bestimmten Prompts verwenden,
z.B. “Analog zur Transformation [A]-->[B] verarbeite [C]” (one-shot prompt)
z.B. [A] = Text auf englisch, [B] = Text auf deutsch, [C] = neuer Text auf englisch.
Pro: extrem vielseitig und bisher sehr, sehr erfolgreich
Contra: benötigt viele Token (noch mehr für few-shot prompts)

<!-- Folie 21 -->
◼
◼
◼
◼
◼
Wort-Vektor-Einbettungen direkt verwenden (statt word2vec z.B. Gemma)
→ semantische Ähnlichkeit, semantische Suche, semantisches Clustering etc.
Satz-Vektor-Einbettungen bzw. längere Texte in Vektoren umwandeln (z.B. BERT)
Nicht Token sampeln sondern die Verteilung der Ausgabetoken direkt betrachten
Fertig trainierte Transformer mit bestimmten Prompts verwenden,
z.B. “Analog zur Transformation [A]-->[B] verarbeite [C]” (one-shot prompt)
z.B. [A] = Text auf englisch, [B] = Text auf deutsch, [C] = neuer Text auf englisch.
Transformer von Grund auf trainieren (eigenes Pretraining)
Pro: vollständige Kontrolle über Trainingsdaten und damit prinzipiell über Outputs
Contra: extrem teuer; Llama2 (~Gemini 1 Pro / ChatGPT 3.5) kostete ~2-10 Mio. $

<!-- Folie 22 -->
◼
◼
◼
◼
◼
◼
Wort-Vektor-Einbettungen direkt verwenden (statt word2vec z.B. Gemma)
→ semantische Ähnlichkeit, semantische Suche, semantisches Clustering etc.
Satz-Vektor-Einbettungen bzw. längere Texte in Vektoren umwandeln (z.B. BERT)
Nicht Token sampeln sondern die Verteilung der Ausgabetoken direkt betrachten
Fertig trainierte Transformer mit bestimmten Prompts verwenden,
z.B. “Analog zur Transformation [A]-->[B] verarbeite [C]” (one-shot prompt)
z.B. [A] = Text auf englisch, [B] = Text auf deutsch, [C] = neuer Text auf englisch.
Transformer von Grund auf trainieren (eigenes Pretraining)
Vortrainierte Transformer auf besonderen Daten weiter trainieren (Finetuning)
Pro: relativ billig (keine sehr langen Trainingszeiten = Stromkosten nötig)
Contra: benötige wenigstens Hardware zum Training (teurer für größere Modelle)

<!-- Folie 23 -->
◼
◼
◼
◼
◼
◼
◼
Wort-Vektor-Einbettungen direkt verwenden (statt word2vec z.B. Gemma)
→ semantische Ähnlichkeit, semantische Suche, semantisches Clustering etc.
Satz-Vektor-Einbettungen bzw. längere Texte in Vektoren umwandeln (z.B. BERT)
Nicht Token sampeln sondern die Verteilung der Ausgabetoken direkt betrachten
Fertig trainierte Transformer mit bestimmten Prompts verwenden,
z.B. “Analog zur Transformation [A]-->[B] verarbeite [C]” (one-shot prompt)
z.B. [A] = Text auf englisch, [B] = Text auf deutsch, [C] = neuer Text auf englisch.
Transformer von Grund auf trainieren (eigenes Pretraining)
Vortrainierte Transformer auf besonderen Daten weiter trainieren (Finetuning)
Transformer-Modell auf Chat-Formate finetunen mit RLHF (wie ChatGPT)
Pro: Feedback führt zu Qualitätssteigerung, z.B. NSFW-Removal o.ä.
Contra: etwas komplizierter als “einfaches” Training

<!-- Folie 24 -->
◼
◼
◼
◼
◼
◼
◼
◼
Wort-Vektor-Einbettungen direkt verwenden (statt word2vec z.B. Gemma)
→ semantische Ähnlichkeit, semantische Suche, semantisches Clustering etc.
Satz-Vektor-Einbettungen bzw. längere Texte in Vektoren umwandeln (z.B. BERT)
Nicht Token sampeln sondern die Verteilung der Ausgabetoken direkt betrachten
Fertig trainierte Transformer mit bestimmten Prompts verwenden,
z.B. “Analog zur Transformation [A]-->[B] verarbeite [C]” (one-shot prompt)
z.B. [A] = Text auf englisch, [B] = Text auf deutsch, [C] = neuer Text auf englisch.
Transformer von Grund auf trainieren (eigenes Pretraining)
Vortrainierte Transformer auf besonderen Daten weiter trainieren (Finetuning)
Transformer-Modell auf Chat-Formate finetunen mit RLHF (wie ChatGPT)
Sehr große Modelle über eine API verwenden (ggf. nur Sampling-Output)
Der de facto Standard für die “meisten” LLM-use-cases für Softwareentwickler.

<!-- Folie 25 -->
◼
◼
◼
◼
◼
◼
◼
◼
◼
Wort-Vektor-Einbettungen direkt verwenden (statt word2vec z.B. Gemma)
→ semantische Ähnlichkeit, semantische Suche, semantisches Clustering etc.
Satz-Vektor-Einbettungen bzw. längere Texte in Vektoren umwandeln (z.B. BERT)
Nicht Token sampeln sondern die Verteilung der Ausgabetoken direkt betrachten
Fertig trainierte Transformer mit bestimmten Prompts verwenden,
z.B. “Analog zur Transformation [A]-->[B] verarbeite [C]” (one-shot prompt)
z.B. [A] = Text auf englisch, [B] = Text auf deutsch, [C] = neuer Text auf englisch.
Transformer von Grund auf trainieren (eigenes Pretraining)
Vortrainierte Transformer auf besonderen Daten weiter trainieren (Finetuning)
Transformer-Modell auf Chat-Formate finetunen mit RLHF (wie ChatGPT)
Sehr große Modelle über eine API verwenden (ggf. nur Sampling-Output)
Vorhersagen eines großen Modells in ein kleineres übertragen (Destillation)
→ das schauen wir uns noch an, so lässt sich z.B. die Inferenz beschleunigen

<!-- Folie 26 -->
◼
◼
◼
◼
◼
◼
◼
◼
◼
◼
Wort-Vektor-Einbettungen direkt verwenden (statt word2vec z.B. Gemma)
→ semantische Ähnlichkeit, semantische Suche, semantisches Clustering etc.
Satz-Vektor-Einbettungen bzw. längere Texte in Vektoren umwandeln (z.B. BERT)
Nicht Token sampeln sondern die Verteilung der Ausgabetoken direkt betrachten
Fertig trainierte Transformer mit bestimmten Prompts verwenden,
z.B. “Analog zur Transformation [A]-->[B] verarbeite [C]” (one-shot prompt)
z.B. [A] = Text auf englisch, [B] = Text auf deutsch, [C] = neuer Text auf englisch.
Transformer von Grund auf trainieren (eigenes Pretraining)
Vortrainierte Transformer auf besonderen Daten weiter trainieren (Finetuning)
Transformer-Modell auf Chat-Formate finetunen mit RLHF (wie ChatGPT)
Sehr große Modelle über eine API verwenden (ggf. nur Sampling-Output)
Vorhersagen eines großen Modells in ein kleineres übertragen (Destillation)
Constrained Generation: Ausgabe sampeln, die einem (z.B. JSON) Schema genügt
ein wesentlicher Baustein für “agentische Workflows”

## Selbst Inferenz & Training durchführen

<!-- Folie 27 -->
Huggingface Transformers
Dokumentation
z.B. LLama 2 7B benötigt bei voller Präzision (etwa zum Training)
ca. 7*4GB = 28 GB VRAM, aber bei halber Präzision
ca. 7*2GB = 14 GB VRAM, passt also auf eine 16GB Consumer-GPU.
Für Inferenz benötigt man keine Gradienten → halber Platzbedarf: 8GB
Aber: LLama 2 70B ist erst in einer Liga mit GPT-4 → 80 bis 280 GB
Auch: llama.cpp

## Llamas & Co

<!-- Folie 28 -->
Noch mehr Rechnung mit Parametermenge
◼ Llama (1,2,3) sind open-weight-Modelle mit verschiedenen
Lizenzen.
◼ Llama2-7B ist etwa 8.6 GB groß,
passt also auf eine einfache Consumer Grafikkarte;
◼ Llama3.3-70B braucht sehr viel VRAM oder rechnet langsam,
dafür ‘in der selben Liga’ wie GPT-4.
◼ Llama3.1-405B verteilt man eher auf mehrere GPUs
(vgl. auch GPT3 mit ca 170B Parameter).

## Llamas benutzen

<!-- Folie 29 -->
◼ Sofort ausprobieren mit
Ollama (https://github.com/ollama/ollama/blob/main/README.md#quickstart)
(startet einen Webservice / Chatinterface, lädt Modelle selbst herunter)
◼ baut auf Llama.cpp auf,
bzw. auf Georgi Gerganovs ggml Bibliothek,
eine Transformer-Architektur-optimierte Deep-Learning-Bibliothek in C/C++.
◼ Eigenes Dateiformat: GGUF für Modelle
◼ Achtung: nicht immer sind die Chat/RLHF/Instruct-Modelle die
geeigneten LLMs (z.B. für Code ‘copilot’ autocompletion oder RAG).

## Beispiel mit Ollama

<!-- Folie 30 -->
“Fertiges LLM benutzen”
curl -fsSL https://ollama.com/install.sh | sh
ollama run llama3.2:1b "Explain how LLMs work"
→ das ist kein Deep Learning, das ist “Deep Learning Produkte benutzen”
Trotzdem super für Rapid Prototyping und jede Menge Anwendungen!
→ OpenAI-kompatibler API Endpoint: verhindert Vendor Lock-in

## Selbst Transformer benutzen

<!-- Folie 31 -->
Huggingface Transformers
Finetuning ist auch sehr teuer…
Lösung:
Parameter-Efficient Finetuning (PEFT) mit
Low-Rank Adaptations (LoRA)
huggingface.co/docs/peft/main/en/conceptual_guides/lora

## Lokale LLMs benutzen

<!-- Folie 32 -->
(im Notebook)

## Wie geht eigentlich …

<!-- Folie 33 -->
Konkret eine Anwendung wie z.B. der “Chatbot” hAInrich:
https://www.heicad.hhu.de/lehre/masters-programme-ai-and-data-science/hainrich

## Tipps zum Übungsblatt 10

<!-- Folie 34 -->
Wir schauen rein, wenn dazu noch Zeit bleibt
Kaggle Notebook
PyTorch|Flowers|TransLearing+Ensemble|Test=99.67%
Fragen, die wir klären wollen:
◼ Worum geht es da überhaupt?
◼ Was “ist” Ensembling / ein Ensemble-Modell?
◼ Was ist z.B. das Modell GoogLeNet von 2014,
was da verwendet wird?
