---
title: "Anwendungsbeispiele"
short_title: "Anwendungsbeispiele"
---

# Anwendungsbeispiele

Drei Beispiele, wie sich die Bausteine aus den vorigen Kapiteln zu Anwendungen zusammensetzen – und ein Blick darauf, wie man mit generiertem Code arbeitet.

## Drei Beispiele aus der Praxis

### Beispiel: hAInrich-Chatbot

[hAInrich: Get answers quickly](https://www.heicad.hhu.de/lehre/masters-programme-ai-and-data-science/hainrich). Die Anwendung ist ein Interface zu einer Wissensdatenbank, eine semantische Suche im Gewand eines Chatbots. Das Wissen liegt vor als Frage-Antwort-Pärchen-Liste (handgeschrieben: FAQ). Ziel: eine beliebige Frage „korrekt“ beantworten. Nebenbedingung: kein Logging (DSGVO), geringe Last auf dem Server (Kosten). Erreichbares Ziel: oft korrekt raten, welche der handgeschriebenen Fragen (mit vorhandenen Antworten) ungefähr der eingegebenen Nutzerfrage entspricht.

Wir überlegen gemeinsam: Wie implementiert man eine semantische Suche im Gewand eines Chatbots?

**Vorbereitung**: Wandle die vorhandene HTML-FAQ um in JSON (`beautifulsoup`). Tokenisiere die Fragen und wandle sie in Vektoren um mit einem LLM (jede Frage ein Vektor, Weg 2 aus Kapitel 11).

**Anwendung**: Tokenisiere den Nutzerinput und wandle ihn in einen Vektor um mit demselben LLM. Vergleiche mit Kosinus-Ähnlichkeit den Inputvektor zu den Fragenvektoren aus der Datenbank, zeige die Top-3-Treffer an. Zeige zum Top-Treffer die Antwort aus der Datenbank.

**Technisch**: Die Inferenz läuft vollständig im Browser (JavaScript, ONNX), ein winziges LLM genügt (20 MB; die Downloadzeit ist die Wartezeit, bis die Anwendung reagiert). Kein Server, der Fragen sieht, also kein Logging-Problem.

### Beispiel: E-Mails klassifizieren

Aufgabe: Gegeben ein Postfach mit E-Mails der vergangenen Jahre, berechne für neu eingehende E-Mails, mit welcher Wahrscheinlichkeit sie beantwortet werden (= Score, ob eine E-Mail vermutlich eine Antwort erfordert).

* IMAP zum Download von Mails + Metadaten.
* Muss in „Sent“ die „Antwort“ zu einer Mail zuordnen (über `In-Reply-To`-Header) – das erzeugt die Labels.
* Ggf. Teildatensatz ausschließen (Spam o.ä.).
* Text der Mail in Vektor(en) umwandeln (LLM-Embedding).
* Vektoren in ein MLP zur Klassifikation füttern, supervised, mit BCE-Loss.

### Beispiel: Empfehlungssystem

Aufgabe: Gegeben eine Liste besuchter bzw. gekaufter Items (Artikel, Produkte) pro Nutzer, empfehle einem neuen Nutzer ein Item, welches interessant ist (mit hoher Wahrscheinlichkeit angeklickt oder gekauft wird).

Lösungsansatz: Ein neuronales Netz konvertiert Items in Vektoren, sodass Items, die auf vielen Listen gemeinsam auftreten, zu Vektoren zugeordnet werden, die einen kleinen (Kosinus-)Abstand zueinander haben (Feature Engineering / Representation Learning). Dann finde im Latent Space Items in der Nähe vergangener Items eines Nutzers.

Wie trainieren wir das neuronale Netz? Die Listen der Nutzer sind „Sätze“, die Items sind „Wörter“ – das ist word2vec (Skip-gram) auf Kauflisten, bzw. node2vec auf dem bipartiten Nutzer-Item-Graphen aus dem [Kapitel über Representation Learning und Graphen](../part-representation-learning/17-representation-learning-graphen.md). Alternativ bettet man Nutzer *und* Items in denselben Latent Space ein und trainiert supervised darauf, dass gekaufte Paare einen kleinen Abstand haben (*two-tower model*).

## Vibecoding Deep Learning

Wir schauen uns praktisch an, wie man mit generiertem Code arbeiten kann. Beispiel-Aufgabe (das Empfehlungssystem von oben): Gegeben eine Liste besuchter bzw. gekaufter Items (Artikel, Produkte) pro Nutzer, empfehle einem neuen Nutzer ein Item, welches interessant ist (mit hoher Wahrscheinlichkeit angeklickt oder gekauft wird). Die Kompetenz, die dabei geübt wird, ist dieselbe, die auch die Übungsblätter verlangen: generierten Deep-Learning-Code anhand der Dokumentation kritisch prüfen – stimmt die Loss-Funktion, stimmen die Shapes, wird tatsächlich das trainiert, was behauptet wird?

## Rezept: ein Anwendungskonzept schreiben

Die drei Beispiele oben folgen alle demselben Muster, und dasselbe Muster ist in der Klausur der Aufgabentyp „Anwendungskonzept“: Zu einer Aufgabenstellung aus der Praxis (Müll auf Fotos erkennen, Lagerbestände vorhersagen, Produktbeschreibungen erzeugen) soll man skizzieren, wie man sie mit Deep Learning angeht. Was dabei immer beantwortet werden muss, in dieser Reihenfolge:

1. **Was haben wir?** Welche Daten liegen vor, in welcher Modalität (Bild, Text, Tabelle, Zeitreihe, Graph), mit welchen Labels, wie viele. Was fehlt, und was können wir uns beschaffen oder selbst labeln.
2. **Was soll rauskommen?** Klassifikation, Regression, Ranking, Generierung, oder nur eine Repräsentation für die Nachbarsuche. Damit steht die Ausgabeschicht fest: Sigmoid, Softmax, linear, oder gar keine.
3. **Welches Modell, und woher?** Fast nie selbst von null trainieren: ein vortrainiertes Modell als Feature-Extraktor einfrieren und einen kleinen Kopf trainieren, oder finetunen, oder ein fertiges Modell nur benutzen. Erst wenn das nicht reicht, eigene Architektur.
4. **Welcher Loss?** Er folgt aus Punkt 2: BCE für binär, Kreuzentropie für Klassen, MSE für Zahlen, Rekonstruktion für Autoencoder, kontrastiv für Paare. Wer zwei Ziele hat, addiert zwei Terme.
5. **Womit messen wir Güte?** Train-Test-Split, und eine Metrik, die zur Aufgabe passt: Accuracy nur bei balancierten Klassen, sonst Precision und Recall; bei Rankings Top-k; bei Generierung ein Mensch. Ohne diesen Punkt weiß man nicht, ob es funktioniert.
6. **Was kann schiefgehen?** Datenschutz und Logging, Kosten und Latenz, Verteilungsverschiebung zwischen Trainingsdaten und Einsatz, Overfitting auf das Testset, Bias in den Labels.

Wer diese sechs Punkte zu einer Aufgabe in je zwei Sätzen beantworten kann, hat ein Anwendungskonzept. Die Punkte 1 und 5 sind die, die in der Praxis am häufigsten vergessen werden.

## Übung

Ein Verlag möchte eingehende Leserbriefe automatisch an die richtige Redaktion leiten
(acht Ressorts).
Gehen Sie die sechs Punkte des Rezepts durch: Was haben wir, was soll herauskommen,
welches Modell und woher, welcher Loss, womit messen wir Güte, was kann schiefgehen.
*Tipp: Die Antwort auf „welches Modell und woher“ ist in diesem Kapitel nie „selbst
trainieren“, solange es ein vortrainiertes gibt.*

*Antwortprobe: Beim Loss sollte etwas mit „Kreuzentropie“ dastehen, bei der Güte etwas anderes als „Accuracy“ — die Ressorts sind ungleich häufig.*
