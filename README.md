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

Das Skript ist nach Themen gegliedert, die Vorlesung nach Wochen. Der grobe zeitliche Ablauf (Vorlesung 1–15) und die zugehörigen Kapitel:

| VL | Kapitel |
|---|---|
| 1 | [Was ist Deep Learning?](part-grundlagen/01-was-ist-deep-learning.md), [Das Perzeptron](part-grundlagen/02-perzeptron.md) (Neuron, MLP) |
| 2 | [Das Perzeptron](part-grundlagen/02-perzeptron.md) (Training, verallgemeinertes Perzeptron), [Vortrainierte Modelle](part-grundlagen/03-vortrainierte-modelle.md) (Orientierung) |
| 3 | [Vortrainierte Modelle](part-grundlagen/03-vortrainierte-modelle.md) (Tasks, Praxis), [Tensoren](part-grundlagen/04-tensoren.md), [Logistische Regression](part-lernen/05-logistische-regression.md) (Einstieg) |
| 4 | [Logistische Regression](part-lernen/05-logistische-regression.md), Kettenregel |
| 5 | [Gradientenabstieg](part-lernen/06-gradientenabstieg.md) |
| 6 | [Backpropagation](part-lernen/07-backpropagation.md), [Aktivierungsfunktionen](part-lernen/08-aktivierungsfunktionen-universalitaet.md), [Autoencoder](part-representation-learning/09-autoencoder.md) (Idee) |
| 7 | [Aktivierungsfunktionen und Universalität](part-lernen/08-aktivierungsfunktionen-universalitaet.md) (Netze von Hand), [Autoencoder](part-representation-learning/09-autoencoder.md) (MNIST, Label-AE) |
| 8 | [Autoencoder](part-representation-learning/09-autoencoder.md) (Sparse, Denoising), [VAE](part-representation-learning/10-variational-autoencoder.md), [word2vec](part-representation-learning/11-word2vec.md) |
| 9 | [Representation Learning und Graphen](part-representation-learning/12-representation-learning-graphen.md), [RNNs und Transformer](part-representation-learning/13-sequenzen-rnn-transformer.md) |
| 10 | [Faltung und CNNs](part-architekturen-anwendungen/14-faltung-cnn.md) |
| 11 | [Backpropagation](part-lernen/07-backpropagation.md) (Berechnungsgraph), [Universalität](part-lernen/08-aktivierungsfunktionen-universalitaet.md), [LLMs benutzen](part-architekturen-anwendungen/15-llms-benutzen.md) |
| 12 | [GANs](part-architekturen-anwendungen/16-gans.md) |
| 13 | [Backpropagation](part-lernen/07-backpropagation.md) (Induktion), [word2vec](part-representation-learning/11-word2vec.md) (Geometrie), [VAE](part-representation-learning/10-variational-autoencoder.md) (latente Räume), [Anwendungsbeispiele](part-architekturen-anwendungen/17-anwendungsbeispiele.md) |
| 14 | [Destillation](part-architekturen-anwendungen/18-destillation.md) |
| 15 | [Optimierer](part-architekturen-anwendungen/19-optimierer.md), [Adversarial Attacks und Polysemie](part-architekturen-anwendungen/20-adversarial-attacks-polysemie.md) |

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
