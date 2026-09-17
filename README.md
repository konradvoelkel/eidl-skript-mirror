---
title: Rahmen (Voraussetzungen, Ablauf, Prüfung)
short_title: Rahmen
---

# Einführung in Deep Learning

## Rahmen der Vorlesung

### Voraussetzungen

*Formale Voraussetzungen*: keine.

*Inhaltliche Voraussetzungen*: Inhalte des Moduls **Data Science**, denn wir setzen rudimentäre Python-Kenntnisse und Grundlagen des maschinellen Lernens voraus, insbesondere die vektorisierte Programmierung mit NumPy und die Idee der linearen Regression.

### Zulassung zur Prüfung

Alle (mindestens 10, höchstens 12) Übungsblätter müssen bearbeitet werden und mindestens 8 abgegeben und als "bestanden" (= mindestens die Hälfte der Punkte) bewertet worden sein.

### Prüfungsform

Schriftlich (Klausur, i.d.R. 90 Minuten) ohne Hilfsmittel/Computer, Fokus auf Theorie.
Die Note wird vollständig aus der Klausur gebildet, die Übungsblätter zuvor sind lediglich eine Studienleistung.

### Ablauf

* Vorlesung (Theorie) immer Mittwochs 12:30 in Hörsaal 5E.
* Übungen (Besprechung der Musterlösung, Fragestunde und zusätzliche Anwesenheitsaufgaben unter Anleitung bearbeiten) Do 10:30 in 2522.U1.52.
* Aus 2025/26 gibt es VL-Aufzeichnungen in der Mediathek: <https://media.hhu.de/search/title/Einführung+in+Deep+Learning+2025/>
* Die Übungsaufgaben kommen als wöchentliches PDF, größtenteils mit Musterlösung.
* Die Vorlesungsfolien sind als PDF wöchentlich vorab verfügbar.

## Inhalt

Grober zeitlicher Ablauf:

1. Geschichte (Perzeptron)
2. Logistische Regression ($\sim$ 1 Neuron) ausführlichst
3. Stochastischer Gradientenabstieg
4. Backpropagation: effiziente Berechnung der Ableitung für tiefe Netze
5. `PyTorch` für Inferenz und Training from Scratch
6. AutoEncoder und VAE (unsupervised Representation Learning)
7. Latente Vektoren für Natural Language Processing (NLP) mit word2vec
8. Intro Convolutional Neural Networks (CNN)
9. Intro Generative-Adversarial Networks (GAN)
10. Vortrainierte LLMs in DL-Anwendungen nutzen
11. Einzelne Exkurse/Vertiefungen nach Laune

Was wir nicht machen werden: Transformer-Modelle trainieren (GPT usw.), auf großen echten Daten arbeiten, aktuelle Architekturen nachimplementieren, Optimierungstheorie, CUDA-Programmierung, Reinforcement Learning.

### Lernziele (Modulhandbuch)

Nach erfolgreicher Teilnahme können die Studierenden:

* Grundbegriffe und -konzepte neuronaler Netze benennen und erklären,
* mathematische Grundlagen für neuronale Netze anwenden,
* einfache Modelle selbst implementieren,
* vortrainierte Modelle in andere Systeme integrieren und
* beurteilen, welche der besprochenen Modelle hinsichtlich einer Anwendung in Frage kommen.

### Relation zu anderen Modulen

* Wenig bis keine Überschneidung: Machine Learning, Data Science 2, Introduction to NLP, Python for NLP
* Vertiefung: Deep Learning im Master, zahlreiche darauf aufbauende Kurse wie etwa Advanced Deep Learning, Implementing Transformer Models, Representations in Natural Language Processing, Probabilistic Machine Learning, Reinforcement Learning

## Literatur

* Simon J.D. Prince, *Understanding Deep Learning*, MIT Press 2023, frei verfügbar unter <https://udlbook.github.io/udlbook/>
* Deisenroth, Faisal, Ong, *Mathematics for Machine Learning*, Cambridge University Press 2020, frei verfügbar unter <https://mml-book.github.io/>
