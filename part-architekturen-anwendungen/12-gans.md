---
title: "VL 12: Generative Adversarial Networks"
short_title: "VL 12"
---

# Generative Adversarial Networks

:::{warning} Rohfassung
Dieses Kapitel ist eine automatische Transkription der Folien von VL 12 aus dem WiSe 2025/26
(`from_2025/slides/Einführung in Deep Learning 2025_26 VL 12_ GANs.pdf`), Folie für Folie in der Originalreihenfolge.
Formeln und Abbildungen sind dabei größtenteils verloren gegangen; der Text ist noch nicht überarbeitet.
:::

## GANs - Historie

<!-- Folie 2 -->

## Historie: NeurIPS 2014

<!-- Folie 3 -->
We propose a new framework for estimating generative models via adversarial
nets, in which we simultaneously train two models: a generative model G that
captures the data distribution, and a discriminative model D that estimates the
probability that a sample came from the training data rather than G. The training
procedure for G is to maximize the probability of D making a mistake. This
framework corresponds to a minimax two-player game. In the space of arbitrary
functions G and D, a unique solution exists, with G recovering the training data
distribution and D equal to 1/2 everywhere. In the case where G and D are defined
by multilayer perceptrons, the entire system can be trained with backpropagation.
There is no need for any Markov chains or unrolled approximate inference
networks during either training or generation of samples. Experiments
demonstrate the potential of the framework through qualitative and quantitatively
evaluation of the generated samples.

## Historie: LeCun 2016

<!-- Folie 4 -->
There are many interesting recent development in deep learning,
probably too many for me to describe them all here. But there are
a few ideas that caught my attention enough for me to get
personally involved in research projects.
The most important one, in my opinion, is adversarial training
(also called GAN for Generative Adversarial Networks). This is an
idea that was originally proposed by Ian Goodfellow when he was
a student with Yoshua Bengio at the University of Montreal (he
since moved to Google Brain and recently to OpenAI).
This, and the variations that are now being proposed is the most
interesting idea in the last 10 years in ML, in my opinion.

## GANs technisch

<!-- Folie 5 -->

<!-- Folie 6 -->
Aufbau
Quelle:
www.kdnuggets.com/2017/01/generative-adver
sarial-networks-hot-topic-machine-learning.html

## Erinnerung

<!-- Folie 7 -->
Samples generieren
Der Generator generiert Samples aus einer Verteilung.
Diese Verteilung ist, was im (Pre)training gelernt wird,
indem die Samples aus dem Trainingsdatensatz
als latente Vektoren repräsentiert werden.
Generatives Modell = Verteilung lernen

## GAN-Training

<!-- Folie 8 -->
Generator
Nach einem Pretraining des Generators, um die Verteilung der
Trainings-Samples zu lernen, wird der Generator zusammen mit dem
Diskriminator trainiert (Finetuning).
Dazu bekommt der Generator eine Penalty in der Loss-Funktion für das
Generieren von Bildern, die der Diskriminator als generiert erkennt.

<!-- Folie 9 -->
Diskriminator
Nach einem Pretraining des Generators, um die Verteilung der
Trainings-Samples zu lernen, wird der Generator zusammen mit dem
Diskriminator trainiert (Finetuning).
Dazu bekommt der Diskriminator eine Penalty in der Loss-Funktion für
die Fehlklassifikation eines Eingabebildes,
also sowohl für falsch positive (“echt” behauptet, war aber generiert)
als auch falsch negative (“generiert” behauptet, war aber echt).

## GAN-Modelle

<!-- Folie 10 -->
Diskriminator
Der Diskriminator kann ein einfaches Multilayer Perzeptron sein,
d.h. mehrere lineare Layer und zuletzt ein einzelnes Neuron zur
Klassifikation “ist das echt?” in 0 oder 1.
Alternativ kann der Diskriminator auch aus 2 Komponenten bestehen,
Wobei zunächst ein vortrainierter Encoder das Bild in latente Vektoren
umrechnet, die dann an einen Klassifikator weitergegeben werden.
Dabei kann z.B. ein CNN zur Extraktion von Features sinnvoll sein.

<!-- Folie 11 -->
Generator
Der Generator kann ein einfaches Multilayer Perzeptron sein,
etwa der Decoder eines Autoencoders,
sodass es einen latenten Raum gibt, aus dem man sampeln kann.
Dabei kann z.B. ein CNN zur Extraktion von Features im Encoder
sinnvoll sein (‘deep convolutional GAN’, DCGAN).

## Ausprobieren: GAN Lab

<!-- Folie 12 -->
2019, Georgia Tech & Google Brain
poloclub.github.io/ganlab/

## Varianten von GANs

<!-- Folie 13 -->

## Varianten

<!-- Folie 14 -->
Conditional GANs
Generator und Diskriminator bekommen Zusatzinformationen,
z.B. Klassenlabels
Der Generator generiert bedingt auf ein gegebenes Klassenlabel,
Der Diskriminator entscheidet bedingt zum Klassenlabel.
Geht auch mit anderen Zusatzinformationen,
z.B. Text kodiert als Vektor von Wort-Embeddings.

<!-- Folie 15 -->
Wasserstein GANs -- Wozu?
Probleme mit klassischen GANs bei der Bildgenerierung:
◼ Mode Collapse - der Generator produziert nur (noch) stereotype
Bilder ohne große Variation.
(Kollabieren der Verteilung auf die Moden, also Konzentration der
Wahrscheinlichkeitsmasse auf einige wenige Punkte).
◼ Vanishing Gradients - wenn der Diskriminator zu schnell gut wird,
geht der Lernprozess nicht weiter für den Generator.
◼ Instabilität im Training - Die Loss-Funktion des Generators
entspricht nicht unbedingt der Qualität der Bilder.

<!-- Folie 16 -->
Wasserstein GANs -- Was?
Andere Loss-Funktion: Wasserstein-Distanz,
auch “Earth Mover’s Distance”,
wie viel Wahrscheinlichkeitsmasse bewegt werden muss,
um aus einer Verteilung eine andere zu machen
(analog Levenshtein-Distanz als Editierabstand).
Die Verteilungen sind zum einen die echten Bilder,
zum Anderen die generierten Bilder (je ein Batch).

<!-- Folie 17 -->
Wasserstein GANs -- Was?
Andere Loss-Funktion: Wasserstein-Distanz,
auch “Earth Mover’s Distance”,
wie viel Wahrscheinlichkeitsmasse bewegt werden muss,
um aus einer Verteilung eine andere zu machen
(analog Levenshtein-Distanz als Editierabstand).
Kritiker statt Diskriminator: Werte zwischen 0 und 1.
Beides führt zu glatteren Loss-Landschaften,
damit zu effektiverem Gradientenabstieg.

<!-- Folie 18 -->
Wasserstein GANs -- Was?
Andere Loss-Funktion: Wasserstein-Distanz
Kritiker statt Diskriminator: Werte zwischen 0 und 1.
Der Kritiker schätzt die Wasserstein-Distanz zwischen den realen
Bildern und den gegebenen Bildern.
Wenn der Kritiker alle Bilder für echt hält, schätzt er 0,
ansonsten gibt es ein Signal, welches für Training genutzt werden kann.

<!-- Folie 19 -->
Wasserstein GANs -- Wie?
Die Details (warum es funktioniert) sind mathematisch nicht trivial.
Ein Tutorial von Lilian Weng:
lilianweng.github.io/posts/2017-08-20-gan

## Konkrete Modelle

<!-- Folie 20 -->
Cycle GANs
Unpaired Image-to-Image Translation using Cycle-Consistent Adversarial Networks
Jun-Yan Zhu, Taesung Park, Phillip Isola, Alexei A. Efros (ICCV 2017)
Image-to-image translation is a class of vision and graphics problems where the goal is to learn the
mapping between an input image and an output image using a training set of aligned image pairs.
However, for many tasks, paired training data will not be available. We present an approach for
learning to translate an image from a source domain X to a target domain Y in the absence of paired
examples. Our goal is to learn a mapping G:X→Y such that the distribution of images from G(X) is
indistinguishable from the distribution Y using an adversarial loss. Because this mapping is highly
under-constrained, we couple it with an inverse mapping F:Y→X and introduce a cycle consistency
loss to push F(G(X))≈X (and vice versa). Qualitative results are presented on several tasks where
paired training data does not exist, including collection style transfer, object transfiguration, season
transfer, photo enhancement, etc. Quantitative comparisons against several prior methods
demonstrate the superiority of our approach.

<!-- Folie 21 -->
Cycle GANs

<!-- Folie 22 -->
StyleGANs
A Style-Based Generator Architecture for Generative Adversarial Networks
Tero Karras, Samuli Laine, Timo Aila - NVIDIA (CVPR 2019)
We propose an alternative generator architecture for generative adversarial networks, borrowing from
style transfer literature. The new architecture leads to an automatically learned, unsupervised
separation of high-level attributes (e.g., pose and identity when trained on human faces) and
stochastic variation in the generated images (e.g., freckles, hair), and it enables intuitive,
scale-specific control of the synthesis. The new generator improves the state-of-the-art in terms of
traditional distribution quality metrics, leads to demonstrably better interpolation properties, and also
better disentangles the latent factors of variation. To quantify interpolation quality and
disentanglement, we propose two new, automated methods that are applicable to any generator
architecture. Finally, we introduce a new, highly varied and high-quality dataset of human faces.

<!-- Folie 23 -->
StyleGANs
Quelle:
github.com/NVlabs/stylegan

<!-- Folie 24 -->
StyleGAN2
thispersondoesnotexist.com

## Viele konkrete Modelle

<!-- Folie 25 -->
The GAN Zoo
Quelle:
github.com/hindupuravinash/the-gan-zoo

## Selbst GANs basteln

<!-- Folie 26 -->

## Selbst machen

<!-- Folie 27 -->
Tutorial time!
pytorch.org/tutorials/beginner/dcgan_faces_tutorial.html
DCGAN = deep convolutional GAN
