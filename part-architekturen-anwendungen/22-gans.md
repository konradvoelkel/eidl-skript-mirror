---
title: "Generative Adversarial Networks"
short_title: "GANs"
---

# Generative Adversarial Networks

## Historie

### NeurIPS 2014

Goodfellow et al., *Generative Adversarial Nets*: „We propose a new framework for estimating generative models via adversarial nets, in which we simultaneously train two models: a generative model $G$ that captures the data distribution, and a discriminative model $D$ that estimates the probability that a sample came from the training data rather than $G$. The training procedure for $G$ is to maximize the probability of $D$ making a mistake. This framework corresponds to a minimax two-player game. In the space of arbitrary functions $G$ and $D$, a unique solution exists, with $G$ recovering the training data distribution and $D$ equal to $1/2$ everywhere. In the case where $G$ and $D$ are defined by multilayer perceptrons, the entire system can be trained with backpropagation.“

Der letzte Satz ist der Punkt: Kein Markov-Chain-Sampling, keine Variationsrechnung wie beim VAE – nur zwei Netze und Backpropagation.

### LeCun 2016

Yann LeCun, auf Quora: „There are many interesting recent developments in deep learning […] The most important one, in my opinion, is adversarial training (also called GAN for Generative Adversarial Networks). This is an idea that was originally proposed by Ian Goodfellow when he was a student with Yoshua Bengio at the University of Montreal […] This, and the variations that are now being proposed is the most interesting idea in the last 10 years in ML, in my opinion.“

## GANs technisch

### Aufbau

Zwei Netze: Der **Generator** $G$ bekommt einen zufälligen latenten Vektor $z \sim \mathcal{N}(0, I)$ (das *Rauschen*) und erzeugt daraus ein Sample $G(z)$, z.B. ein Bild. Der **Diskriminator** $D$ bekommt ein Bild – entweder ein echtes $x$ aus dem Trainingsdatensatz oder ein generiertes $G(z)$ – und gibt eine Wahrscheinlichkeit $D(x) \in (0, 1)$ aus, dass das Bild echt ist. Man beachte: Der Generator bekommt *nie* echte Bilder als Input; er sieht die Daten nur indirekt, über den Gradienten des Diskriminators.

:::{figure} ../images/vl12-gan-schema.png
:width: 90%

Generator und Diskriminator. Der Generator sieht nie echte Daten – nur den Gradienten, der durch den Diskriminator zurückfließt.
:::

### Erinnerung: Samples generieren

Der Generator generiert Samples aus einer Verteilung. Diese Verteilung ist, was im (Pre-)Training gelernt wird, indem die Samples aus dem Trainingsdatensatz als latente Vektoren repräsentiert werden. Generatives Modell = Verteilung lernen ([Kapitel „Was ist Deep Learning?“](../part-grundlagen/01-was-ist-deep-learning.md)). Beim VAE haben wir dafür den latenten Raum explizit auf eine Normalverteilung gezwungen; beim GAN sagt uns der Diskriminator, ob die generierte Verteilung schon von der echten zu unterscheiden ist.

### GAN-Training

Das *Minimax-Spiel* aus dem Abstract als Formel:

$$
\min_G \max_D \; V(D, G) = \mathbb{E}_{x \sim p_{\text{data}}}\bigl[\log D(x)\bigr] + \mathbb{E}_{z \sim \mathcal{N}(0, I)}\bigl[\log\bigl(1 - D(G(z))\bigr)\bigr].
$$

Das ist die binäre Kreuzentropie des Diskriminators mit Label 1 für echt und 0 für generiert. $D$ will sie maximieren (gut klassifizieren), $G$ will sie minimieren ($D$ täuschen). In der Praxis werden beide abwechselnd mit Gradientenabstieg trainiert:

**Diskriminator**: Er bekommt eine Penalty in der Loss-Funktion für die Fehlklassifikation eines Eingabebildes, also sowohl für falsch positive („echt“ behauptet, war aber generiert) als auch falsch negative („generiert“ behauptet, war aber echt). Ein Schritt: ein Batch echter Bilder mit Label 1, ein Batch generierter Bilder mit Label 0, BCE-Loss, `backward`, `step` – nur die Parameter von $D$.

**Generator**: Nach einem optionalen Pretraining (z.B. als Decoder eines Autoencoders, um die Verteilung der Trainings-Samples grob zu lernen) wird der Generator zusammen mit dem Diskriminator trainiert (Finetuning). Dazu bekommt der Generator eine Penalty in der Loss-Funktion für das Generieren von Bildern, die der Diskriminator als generiert erkennt: ein Batch $G(z)$, durch $D$ schicken, BCE-Loss *mit Label 1* (der Generator will, dass $D$ „echt“ sagt), `backward`, `step` – nur die Parameter von $G$. Der Gradient fließt dabei durch $D$ hindurch bis in $G$, das ist Backpropagation durch zwei Netze.

Im Gleichgewicht, wenn $G$ die Datenverteilung exakt trifft, kann $D$ nicht besser als raten: $D \equiv \tfrac12$.

### GAN-Modelle

Der **Diskriminator** kann ein einfaches Multilayer Perceptron sein, d.h. mehrere lineare Layer und zuletzt ein einzelnes Neuron zur Klassifikation „ist das echt?“ in 0 oder 1 – also logistische Regression auf Features. Alternativ kann der Diskriminator auch aus 2 Komponenten bestehen, wobei zunächst ein vortrainierter Encoder das Bild in latente Vektoren umrechnet, die dann an einen Klassifikator weitergegeben werden. Dabei kann z.B. ein CNN zur Extraktion von Features sinnvoll sein.

Der **Generator** kann ein einfaches Multilayer Perceptron sein, etwa der Decoder eines Autoencoders, sodass es einen latenten Raum gibt, aus dem man sampeln kann. Mit Faltungen (genauer: *transponierten* Faltungen, die die Auflösung erhöhen) im Generator und einem CNN im Diskriminator heißt das **DCGAN** (deep convolutional GAN, Radford et al. 2015).

### Ausprobieren: GAN Lab

:::{admonition} Ausprobieren: GAN Lab
:class: tip
[poloclub.github.io/ganlab](https://poloclub.github.io/ganlab/) (2019, Georgia Tech und Google Brain): ein GAN auf 2D-Punktwolken im Browser, mit der Generator-Verteilung, dem Gradientenfeld des Diskriminators und den Loss-Kurven live. Was man dort sehen sollte: Bei der Ring- oder Gauß-Wolke wandert die generierte Verteilung zur echten, bis das Gradientenfeld flach wird. Beim *linearen* Datensatz läuft das Training regelmäßig in ein lokales Minimum, in dem der Generator nur einen Teil der Linie bedient, und mehrere Neustarts liefern verschiedene Ergebnisse; das ist Mode Collapse in klein. Daraus folgt die Faustregel für GANs: *früh aufhören.* Anders als beim Autoencoder wird es nicht monoton besser. Man beobachtet die Samples und behält die Gewichte von dem Zeitpunkt, an dem sie gut aussahen. Die Loss-Kurven sind dabei nur bedingt hilfreich, siehe unten bei Wasserstein.
:::

## Varianten von GANs

### Conditional GANs

Generator und Diskriminator bekommen Zusatzinformationen, z.B. Klassenlabels: Der Generator generiert $G(z, y)$ bedingt auf ein gegebenes Klassenlabel $y$, der Diskriminator entscheidet $D(x, y)$ bedingt zum Klassenlabel. So bekommt man einen Generator, dem man sagen kann, *welche* Ziffer er zeichnen soll (die vierte MNIST-Task aus dem [Kapitel „Autoencoder“](../part-representation-learning/14-autoencoder.md)). Geht auch mit anderen Zusatzinformationen, z.B. Text kodiert als Vektor von Wort-Embeddings – das ist der Weg zu Text-zu-Bild-Modellen.

### Wasserstein GANs – wozu?

Probleme mit klassischen GANs bei der Bildgenerierung:

* **Mode Collapse** – der Generator produziert nur (noch) stereotype Bilder ohne große Variation. Die Verteilung kollabiert auf die Moden, also die Wahrscheinlichkeitsmasse konzentriert sich auf einige wenige Punkte, die $D$ gerade nicht erkennt.
* **Vanishing Gradients** – wenn der Diskriminator zu schnell gut wird, ist $D(G(z)) \approx 0$ überall, $\log(1 - D(G(z)))$ ist flach, und der Lernprozess geht für den Generator nicht weiter.
* **Instabilität im Training** – die Loss-Funktion des Generators entspricht nicht unbedingt der Qualität der Bilder; man kann am Loss nicht ablesen, ob es besser wird.

### Wasserstein GANs – was?

Andere Loss-Funktion: die **Wasserstein-Distanz**, auch „Earth Mover's Distance“ – wie viel Wahrscheinlichkeitsmasse (mal Weglänge) bewegt werden muss, um aus einer Verteilung eine andere zu machen (analog zur Levenshtein-Distanz als Editierabstand für Strings). Die Verteilungen sind zum einen die echten Bilder, zum anderen die generierten Bilder (je ein Batch). Der Vorteil gegenüber der KL-Divergenz bzw. der Kreuzentropie: Die Wasserstein-Distanz ist auch dann endlich und hat einen nützlichen Gradienten, wenn sich die beiden Verteilungen gar nicht überlappen.

**Kritiker** statt Diskriminator: Statt einer Wahrscheinlichkeit in $(0, 1)$ gibt der Kritiker eine reelle Zahl aus und schätzt damit die Wasserstein-Distanz zwischen den realen Bildern und den gegebenen Bildern. Wenn der Kritiker alle Bilder für echt hält, schätzt er $0$, ansonsten gibt es ein Signal, welches für das Training genutzt werden kann. Beides führt zu glatteren Loss-Landschaften und damit zu effektiverem Gradientenabstieg, und der Kritiker-Loss korreliert tatsächlich mit der Bildqualität.

:::{admonition} Vertiefung: warum der Kritiker die Wasserstein-Distanz schätzt
:class: note dropdown
Die Wasserstein-1-Distanz zwischen zwei Verteilungen $p$ und $q$ ist als Transportproblem definiert. Die Kantorovich-Rubinstein-Dualität sagt, dass man sie auch so schreiben kann:

$$
W(p, q) = \sup_{\|f\|_{\text{Lip}} \le 1} \Bigl( \mathbb{E}_{x \sim p}[f(x)] - \mathbb{E}_{x \sim q}[f(x)] \Bigr),
$$

ein Supremum über alle Funktionen $f$, die höchstens Steigung $1$ haben (1-Lipschitz). Der Kritiker *ist* dieses $f$: ein Netz, das auf echten Bildern hohe und auf generierten Bildern niedrige Werte ausgeben soll; die Differenz der Mittelwerte ist die geschätzte Distanz. Damit das eine Schranke bleibt, muss der Kritiker Lipschitz-beschränkt bleiben: im Original-WGAN (Arjovsky et al. 2017) durch Abschneiden der Gewichte (*weight clipping*), in WGAN-GP (Gulrajani et al. 2017) durch einen Strafterm auf die Gradientennorm (*gradient penalty*). Tutorial: Lilian Weng, [From GAN to WGAN](https://lilianweng.github.io/posts/2017-08-20-gan).
:::

## Konkrete Modelle

### CycleGAN

Zhu, Park, Isola, Efros (ICCV 2017), *Unpaired Image-to-Image Translation using Cycle-Consistent Adversarial Networks*: Image-to-image translation lernt die Abbildung von einem Eingabebild auf ein Ausgabebild – normalerweise aus einem Trainingsdatensatz *gepaarter* Bilder. Für viele Tasks gibt es aber keine Paare (Foto $\leftrightarrow$ Monet-Gemälde, Pferd $\leftrightarrow$ Zebra, Sommer $\leftrightarrow$ Winter). CycleGAN lernt eine Abbildung $G \colon X \to Y$, sodass die Verteilung von $G(X)$ von $Y$ nicht unterscheidbar ist (adversarial loss) – und weil das allein hochgradig unterbestimmt ist, gleichzeitig die inverse Abbildung $F \colon Y \to X$ mit einem **Cycle-Consistency-Loss** $F(G(x)) \approx x$ (und umgekehrt). Ein Pferd, das zum Zebra und zurück wird, muss wieder dasselbe Pferd sein.

Beispielbilder (Monet $\leftrightarrow$ Foto, Zebra $\leftrightarrow$ Pferd, Sommer $\leftrightarrow$ Winter) auf der Projektseite [junyanz.github.io/CycleGAN](https://junyanz.github.io/CycleGAN/).

### StyleGAN

Karras, Laine, Aila – NVIDIA (CVPR 2019), *A Style-Based Generator Architecture for Generative Adversarial Networks*: eine alternative Generator-Architektur, die sich an der Style-Transfer-Literatur orientiert. Der latente Vektor $z$ wird zuerst durch ein MLP in einen Zwischenraum $w$ abgebildet und dann *auf jeder Auflösungsstufe* des Generators als „Stil“ eingespeist. Das führt zu einer automatisch gelernten, unsupervised Trennung von High-Level-Attributen (z.B. Pose und Identität bei Gesichtern) und stochastischer Variation (z.B. Sommersprossen, Haare), und erlaubt intuitive, skalenspezifische Kontrolle der Synthese. Dazu ein neuer Datensatz von Gesichtern (FFHQ). StyleGAN2 ist hinter [thispersondoesnotexist.com](https://thispersondoesnotexist.com).

Beispielgesichter und das Video zur Interpolation im Stil-Raum: [github.com/NVlabs/stylegan](https://github.com/NVlabs/stylegan).

### Viele konkrete Modelle

*The GAN Zoo*, [github.com/hindupuravinash/the-gan-zoo](https://github.com/hindupuravinash/the-gan-zoo): eine Liste von mehreren hundert benannten GAN-Varianten. Seit ca. 2021 haben Diffusionsmodelle die GANs bei der Bildgenerierung weitgehend abgelöst, aber das adversarielle Prinzip lebt weiter – z.B. als Loss-Term beim Training von VAE-Decodern für Stable Diffusion.

## Selbst GANs basteln

Tutorial time: [pytorch.org/tutorials/beginner/dcgan_faces_tutorial.html](https://pytorch.org/tutorials/beginner/dcgan_faces_tutorial.html), das offizielle DCGAN-Tutorial auf dem CelebA-Gesichterdatensatz. Die Trainingsschleife dort ist genau die oben beschriebene: erst $D$ mit echten und generierten Bildern, dann $G$ mit Label „echt“, abwechselnd pro Batch.

:::{admonition} Weiterlesen
:class: seealso
Prince, *UDL*, Kap. 15 (Generative adversarial networks), inklusive Wasserstein-GAN und StyleGAN. Das Buch ist frei verfügbar, siehe [Über dieses Skript](../README.md).
:::
