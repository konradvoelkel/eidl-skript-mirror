---
title: "Adversarial Attacks und Polysemie"
short_title: "Adversarial Attacks"
---

# Adversarial Attacks und Polysemie

Zwei Themen zum Abschluss, die über die Vorlesung hinausgehen, aber mit dem Gelernten schon verständlich sind.

## Adversarial Attacks

### Definition

Die gezielte Manipulation des Inputs eines Machine-Learning-Modells, um ein spezifisch falsches Ergebnis oder ein unerwartetes Verhalten zu produzieren. Die Manipulation ist häufig nicht direkt für Menschen zu erkennen.

Beispiel: die gezielte Manipulation des Inputs eines Bildklassifikators, um eine spezifisch falsche Klasse zu produzieren. Also: Wir stecken einen weißen Hai rein, aber „die KI“ sagt „Goldfisch“ dazu. Reingelegt!

### Theorie

Wir betrachten den Eingaberaum „Menge aller Bilddateien“ ($[0, 1]^{3 \cdot H \cdot W}$) sowie die Eingabemenge „Menge aller Trainingsbilder“. Das Modell lernt Entscheidungsgrenzen im Eingaberaum, um Klassenlabel zu vergeben. Hypothese: Nahe der Entscheidungsgrenze liegen *adversarial examples* – und da die Trainingsbilder nur auf einer winzigen Teilmenge des Eingaberaums liegen (Manifold-Hypothese), verläuft die Entscheidungsgrenze fast überall dicht an jedem Bild vorbei, nur in Richtungen, die „aus der Mannigfaltigkeit heraus“ zeigen und für Menschen wie Rauschen aussehen.

Das ist die These der Bachelorarbeit „Das Dimpled Manifold Model als Erklärung für die Existenz und die Eigenschaften von Adversarial Examples“ von N. Wieczorek (HHU 2023), nach Shamir et al. 2021: Die Entscheidungsgrenze schmiegt sich wie eine Folie mit kleinen Dellen (*dimples*) an die Datenmannigfaltigkeit an.

### Wie wird's gemacht?

Mit Gradientenabstiegsmethoden sucht man, ausgehend von einem Bild eines weißen Hais, Richtungen, die die Klassifikation ändern, ohne besonders viel am Bild zu ändern:

$$
x_{\text{adv}} := x + \epsilon \cdot \operatorname{sign}\bigl(\nabla_x L(f(x), y_{\text{Ziel}})\bigr)
$$

(Fast Gradient Sign Method, Goodfellow et al. 2014) oder iterativ mit kleinen Schritten. Anders als sonst: Gradientenabstieg im **Eingaberaum**, nicht im Gewichtsraum – Backpropagation liefert $\nabla_x$ genauso wie $\nabla_w$, denn im DAG ist $x$ nur ein weiteres Blatt.

Dass das nicht nur mit Pixeln funktioniert: Sharif et al. 2016, *Accessorize to a Crime: Real and Stealthy Attacks on State-of-the-Art Face Recognition* – eine bedruckte Brillenfassung lässt ein Gesichtserkennungssystem eine andere Person erkennen. Und aus dem Heise-Newsticker vom 2.2.2026: [Manipulierte Straßenschilder: Wenn das autonome Auto Fußgänger umfährt](https://www.heise.de/news/Manipulierte-Strassenschilder-Wenn-das-autonome-Auto-Fussgaenger-umfaehrt-11162744.html).

## Polysemie und die Manifold-Hypothese

(Folien von Ben Ruppik, aus der Vorlesung *Topological Data Analysis* im Master AI & Data Science, Juni 2025; siehe `from_2025/slides/2025-06-09 TDA guest lecture Ben Ruppik.pdf`.)

**Manifold Hypothesis**: High-dimensional data lies on or near a low-dimensional structure called a *manifold*. Das ist die Annahme hinter allem, was wir über latente Räume gesagt haben: Der Autoencoder findet die Parametrisierung der Mannigfaltigkeit, der VAE glättet sie, word2vec legt Wörter auf eine Mannigfaltigkeit, auf der Richtungen Bedeutung haben.

**Problems with the Manifold Hypothesis**: Sometimes data does *not* have a low-dimensional structure and cannot be effectively mapped onto a lower-dimensional space – wegen Rauschen, oder wegen zu weniger Samples, sodass die zugrundeliegende Struktur nicht geschätzt werden kann. Und manchmal ist die Struktur zwar niedrigdimensional, aber keine Mannigfaltigkeit: Zwei Kurven, die sich kreuzen, haben am Schnittpunkt keine eindeutige Tangente.

Genau das passiert bei **Polysemie**: Ein Wort wie „Maus“ (Tier, Computermaus) oder „Bank“ (Sitzgelegenheit, Geldinstitut) hat mehrere Bedeutungen, die in verschiedenen Kontexten vorkommen. Im Embedding-Raum eines kontextabhängigen Modells (BERT) liegen die Vorkommen von „Maus“ auf mehreren „Ästen“, die sich an einem Punkt treffen – eine *Singularität* der Datenmannigfaltigkeit. Topologische Datenanalyse (persistent homology, lokale Dimension) kann solche Singularitäten finden und damit polyseme Wörter *ohne Wörterbuch* aus den Embeddings entdecken. word2vec mit einem Vektor pro Wort kann das prinzipiell nicht: Es muss alle Bedeutungen in einen Punkt mitteln.

:::{figure} ../images/vl15-manifolds.png
:width: 90%

Die Manifold-Hypothese und ihre Grenzen: Daten nahe einer Kurve; Rauschen; zwei sich kreuzende Kurven (keine Mannigfaltigkeit – so sieht Polysemie im Embedding-Raum aus); und das Dimpled Manifold Model, in dem die Entscheidungsgrenze sich an die Daten schmiegt und Adversarial Examples nur einen winzigen Schritt entfernt sind.
:::

Damit schließt sich der Kreis zur Kernfrage aus Kapitel 8: Welche Struktur finden wir im Latent Space? Manchmal eine schöne Mannigfaltigkeit – und manchmal etwas Interessanteres.
