---
title: "VL 13: Latent Spaces und Anwendungen"
short_title: "VL 13"
---

# Latent Spaces und Anwendungen

:::{note} Stand
Erste Prosafassung (aus den Folien von VL 13, WiSe 2025/26). Abbildungen fehlen noch, siehe die `TODO`-Kommentare.
:::

## Und noch einmal zur Backpropagation

Noch einmal systematisch, als Wiederholung und Zusammenfassung aus der Übung – denn Backpropagation ist Klausurstoff (Aufgabentyp 4), und die Formulierung als Induktion ist die, mit der man jede Architektur erschlägt.

### Warum Backpropagation funktioniert

1. Im **Forward Pass** speichern wir für jede Rechenoperation das Zwischenergebnis und merken uns die Ableitung der einzelnen Rechenoperation und auf welche vorangehenden Ergebnisse wir zurückgreifen müssen (Konstruktion des DAG).
2. Im **Backward Pass** können wir für jede Rechenoperation jeweils nach den Gewichten ableiten, die für diese Operation relevant sind. Wenn wir nach Gewichten ableiten, von denen die vorangegangenen Rechenoperationen abhängen, müssen wir die Kettenregel anwenden. Dazu benötigen wir nur die Ableitung der neuen Rechenoperation (gespeichert im Forward Pass), den Wert der Rechenoperation (gespeichert im Forward Pass) und die Ableitung der vorangegangenen Rechenoperationen.

Mit vollständiger Induktion sehen wir also: Wir können alle Ableitungen berechnen mit *einem* Durchlauf durch den DAG. Insbesondere können wir die Loss-Funktion (das „Ende“ des DAG) nach allen Gewichten ableiten und so den vollständigen Gradienten berechnen.

### Der Induktionsschritt, systematisch

Wir bezeichnen den Input als $x \in \mathcal{X}$. Die „bisherigen Rechenoperationen“ sind eine Abbildung $Y \colon \mathcal{X} \to \mathcal{Y}$, also $y := Y(x; w_Y)$, deren Ableitungen $\frac{dY}{dw_Y}(x; w_Y)$ wir per Induktion kennen. Die „nächste Rechenoperation“ ist eine Abbildung $Z \colon \mathcal{Y} \to \mathcal{Z}$, deren Ableitungen $\frac{dZ}{dy}$ und $\frac{dZ}{dw_Z}$ wir kennen. Die Kettenregel erlaubt uns, $Z(Y(x; w_Y); w_Z)$ nach $w_Y$ abzuleiten:

$$
\frac{d}{dw_Y} Z(Y(x; w_Y); w_Z) = \frac{dZ}{dy}(y; w_Z) \cdot \frac{dY}{dw_Y}(x; w_Y),
\qquad
\frac{d}{dw_Z} Z(Y(x; w_Y); w_Z) = \frac{dZ}{dw_Z}(y; w_Z).
$$

Spezialfälle: Wenn die nächste Rechenoperation der Loss ist, gibt es keine „neuen Gewichte“, dann ist nur die Ableitung nach „bisherigen Gewichten“ relevant. Der Induktionsanfang ist gegeben, indem $Y$ die Identitätsfunktion ist (Ableitung ist $1$). In knapperer Notation, mit Kleinbuchstaben als Funktionsnamen:

$$
\frac{dz}{dw} = \frac{dz}{dy} \cdot \frac{dy}{dw}.
$$

### Nicht konkret genug? Ein weiteres einfaches Beispiel

Wir wählen als Input $x \in \mathcal{X} \subseteq \mathbb{R}^n$. Im Beispiel soll $y := y(x; w) := w \cdot x$ sein, also ein linearer Layer. Die „nächste Rechenoperation“ ist $z \colon \mathbb{R} \to \mathbb{R}$, und zwar $z := z(y) := \operatorname{ReLU}(y) = \max(0, y)$. Die Ableitung nach $y$ ist $[y > 0]$. Aus $\frac{dz}{dw} = \frac{dz}{dy} \cdot \frac{dy}{dw}$ wird also

$$
\frac{dz}{dw} = [y > 0] \cdot x .
$$

Übungsaufgabe: Erweitern Sie den linearen Layer um ein zweites Neuron (also ein weiterer Gewichtsvektor $v \in \mathbb{R}^n$ tritt auf) und erweitern Sie die Berechnung um eine Loss-Funktion $\| z - z_{\text{ground truth}} \|^2$. (Das ist Blatt 7 in Kurzform.)

## Latent Spaces von LLMs: Wort-Vektor-Einbettungen geometrisch verstehen

### Arithmetik im Latent Space

Der Klassiker bei word2vec: KING − MAN + WOMAN = QUEEN. Also ist WOMAN − MAN die Richtung „feminin“. Auch:

* PARIS − FRANCE + ITALY = ROME (also PARIS − FRANCE die Richtung „Hauptstadt“),
* WALKING − WALK + SWIMMING = SWAM (also WALKING − WALK die Richtung „Vergangenheit“ bzw. Flexion),
* BIGGER − BIG = BIGGEST − BIGGER (also Steigerung der Intensität als Richtung).

Analog, aber in allen LLMs: Semantische Beziehungen werden zu *Richtungen* im latenten Raum, und Richtungen kann man addieren. Das ist keine Eigenschaft, auf die word2vec trainiert wurde, sie entsteht von selbst aus dem Kontext-Vorhersage-Training.

<!-- TODO Abbildung: 2D-Projektion von Wortvektoren mit Parallelogrammen (Folie 13) -->

**Bolukbasi et al. 2016, *Man is to Computer Programmer as Woman is to Homemaker? Debiasing Word Embeddings***: Dieselbe Arithmetik findet auch MAN − WOMAN ≈ COMPUTER PROGRAMMER − HOMEMAKER. Die Embeddings enthalten die Stereotype des Trainingskorpus als Richtungen, und man kann sie messen – und, das ist der Beitrag des Papers, durch Projektion auf das orthogonale Komplement der Gender-Richtung teilweise entfernen (`bolukbasi16-man-is-to-computer-programmer-figure7.png`).

### Interpolation und Superposition

Ein Vektor im Latent Space ist ausdrucksstärker als ein Token, er kann interpolieren und Superposition ausdrücken: Statt „Katze“ oder „Hund“ geht auch $\tfrac12 \text{Katze} + \tfrac12 \text{Hund}$, oder auch $t \cdot \text{Katze} + (1 - t) \cdot \text{Hund}$. Aber: $\operatorname{decode}(t \cdot \text{Katze} + (1 - t) \cdot \text{Hund})$ ist entweder Katze oder Hund, es gibt kein „dazwischen“-Token außerhalb des Vokabulars.

### Diskreter Latent Space

Bei word2vec und LLMs mit einem Vokabular von $N$ Token können nur genau $N$ Vektoren im Latent Space direkt zu Token dekodiert werden; für jeden anderen Vektor werden nahe liegende solche Vektoren ausgewählt zum Dekodieren. Gegeben ein Vektor im Latent Space, welches Token wählen wir aus? Das ist die **Sampling-Strategie**.

Gegeben Vektor $v \in \mathbb{R}^n$, welches Token $t \in$ Vokabular wählen wir?

* Berechne für jedes $t$ den Abstand $d(v, \operatorname{code}(t))$, z.B. im Kosinus-Abstand $1 - \cos(\angle(v, \operatorname{code}(t)))$, und wähle $t$, sodass dieser Abstand minimal wird (**top-1**, *greedy decoding*).
* Betrachte auf allen Token $t$ die Verteilung $\operatorname{Softmax}(-d(v, \operatorname{code}(t)))$ und **sample** aus dieser Verteilung.
* Für eine natürliche Zahl $k$ (z.B. $k = 5$) wähle die $k$ nächstgelegenen Token $t_1, \dots, t_k$ aus und sample mit der Softmax-Verteilung nur aus $\{t_1, \dots, t_k\}$ (**top-k sampling**; *top-p* nimmt stattdessen so viele Token, bis ihre Wahrscheinlichkeit $p$ überschreitet).
* Verändere die Verteilung: Richtung top-1 durch niedrige Temperatur, Richtung Gleichverteilung durch hohe Temperatur.

**Temperature Scaling**: Gegeben eine Temperatur $T > 0$, berechne die Verteilung

$$
P_i = \frac{\exp(v_i / T)}{\sum_j \exp(v_j / T)},
$$

d.h. die Einträge von $v$ (die Logits) werden durch $T$ geteilt, dann wird mit Softmax eine Wahrscheinlichkeitsverteilung daraus. Großes $T > 1$: Die verschiedenen $P_i$ werden sich ähnlicher, das Modell wird „kreativer“ (und fehleranfälliger). Kleines $T < 1$: Die großen $P_i$ werden größer, die kleinen $P_i$ werden kleiner; im Grenzfall $T \to 0$ ist es top-1.

## Latent Spaces von Autoencodern, VAEs und GANs für Bilder

### Erinnerung: kontinuierlich statt diskret

Bei word2vec und LLMs können nur $N$ Vektoren dekodiert werden. Bei Autoencodern für Bilder ist dies anders: *Jeder* Vektor im Latent Space lässt sich zu einem Bild dekodieren. Damit lässt sich z.B. zwischen Hund und Katze interpolieren – der Decoder produziert für $t \cdot \operatorname{enc}(\text{Hund}) + (1 - t) \operatorname{enc}(\text{Katze})$ tatsächlich ein Bild, ob es sinnvoll aussieht, ist eine andere Frage.

<!-- TODO Abbildung: Interpolation im latenten Raum eines MNIST-Autoencoders (Folie 27) -->

### Autoencoder vs. GANs

Der Generator eines GANs ist typischerweise gegeben durch eine Verteilung auf einem Latent Space, aus der gesampelt wird (i.d.R. eine Standardnormalverteilung), und einen Decoder, der aus dem latenten Vektor ein tatsächliches Bild generiert. Um einen guten Decoder zu bekommen, ist vor dem adversarial Training ein Pretraining in einem Autoencoder-Setup sinnvoll; daher ist der Latent Space zunächst derselbe. Nach dem GAN-Training des Decoders passen Encoder und Decoder aber nicht mehr zusammen, d.h. der Rekonstruktions-Loss steigt, während der Adversarial Loss sinkt. Der GAN-Decoder optimiert „sieht echt aus“, nicht „ist das Original“.

### Autoencoder vs. VAE

Der Encoder eines VAE kodiert ein Eingabebild $x$ als Paar $(v_x, \sigma_x)$, wobei $v_x \in \mathbb{R}^n$ ein latenter Vektor wie beim Autoencoder ist. Der Unterschied vom VAE zum AE liegt im Training: Statt $\operatorname{decode}(v_x)$ mit $x$ zu vergleichen, wird $\operatorname{decode}(v_x + \varepsilon)$ mit $x$ verglichen, wobei $\varepsilon$ Varianz $\sigma_x^2$ hat. Nach erfolgreichem Training ist dann auch $\operatorname{decode}(v_x) \approx x$, aber der Latent Space bzw. Decoder sieht anders aus als beim AE: Um jeden Code herum gibt es eine Umgebung, die ebenfalls zu einem ähnlichen Bild dekodiert.

Häufig wird zusätzlich zum $+\varepsilon$-Trick auch noch ein Summand zur Loss-Funktion hinzugefügt, damit die Codes der Trainingsdaten im Latent Space ungefähr standardnormalverteilt sind (Variational Loss, Kapitel 8). So kann man später aus der Standardnormalverteilung im Latent Space sampeln und bleibt in der gelernten Verteilung.

<!-- TODO Abbildungen: latenter Raum AE (3 Punkte) vs. VAE (+ε, +σε), Folien 32–34 -->

### Arvanitidis et al. 2017: Latent Space Oddity

*Latent Space Oddity: on the Curvature of Deep Generative Models* (ICLR 2018): Der latente Raum eines VAE sieht flach aus, aber der Decoder verzerrt ihn – die euklidische Gerade zwischen zwei Codes ist nicht der kürzeste Weg im *Bildraum*. Die richtige Geometrie ist die durch den Decoder induzierte Riemannsche Metrik, und Geodäten darin laufen um Regionen herum, in denen der Decoder unsicher ist (`arvanitidis2021-latent-space-oddity-figure1.png`). Praktisch: Interpolationen entlang Geodäten sehen besser aus als lineare.

<!-- TODO Abbildung: Arvanitidis et al., Figure 1 -->

## Anwendungsbeispiele

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

Wie trainieren wir das neuronale Netz? Die Listen der Nutzer sind „Sätze“, die Items sind „Wörter“ – das ist word2vec (Skip-gram) auf Kauflisten, bzw. node2vec auf dem bipartiten Nutzer-Item-Graphen aus Kapitel 9. Alternativ bettet man Nutzer *und* Items in denselben Latent Space ein und trainiert supervised darauf, dass gekaufte Paare einen kleinen Abstand haben (*two-tower model*).
