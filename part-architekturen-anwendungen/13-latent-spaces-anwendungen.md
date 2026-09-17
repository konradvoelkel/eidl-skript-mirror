---
title: "VL 13: Latent Spaces und Anwendungen"
short_title: "VL 13"
---

# Latent Spaces und Anwendungen

:::{warning} Rohfassung
Dieses Kapitel ist eine automatische Transkription der Folien von VL 13 aus dem WiSe 2025/26
(`from_2025/slides/Einführung in Deep Learning 2025_26 VL 13_ Latent Spaces und Anwendungen.pdf`), Folie für Folie in der Originalreihenfolge.
Formeln und Abbildungen sind dabei größtenteils verloren gegangen; der Text ist noch nicht überarbeitet.
:::

## Und noch einmal zur

<!-- Folie 2 -->
Wiederholung: Backpropagation

## Backpropagation

<!-- Folie 3 -->
Noch einmal systematisch (Wdh.+Zusammenfassung aus der Übung)
Zusammenfassung, warum Backpropagation funktioniert:
1.
2.
Im “Forward Pass” speichern wir für jede Rechenoperation das Zwischenergebnis,
Und merken uns die Ableitung der einzelnen Rechenoperation und auf welche
vorangehenden Ergebnisse wir zurückgreifen müssen (Konstruktion des DAG)
Im “Backward Pass” können wir für jede Rechenoperation jeweils nach den
Gewichten ableiten, die für diese Operation relevant sind. Wenn wir nach Gewichten
ableiten, von denen die vorangegangene Rechenoperationen abhängen, müssen wir
die Kettenregel anwenden. Dazu benötigen wir nur die Ableitung der neuen
Rechenoperation (gespeichert im Forward Pass) und den Wert der Rechenoperation
(gespeichert im Forward Pass) und die Ableitung der vorangegangenen
Rechenoperationen. Mit vollständiger Induktion sehen wir also:
Wir können alle Ableitungen berechnen mit einem Durchlauf durch den DAG.
Insbesondere können wir die Loss-Funktion (das “Ende” des DAG) nach allen
Gewichten ableiten und so den vollständigen Gradienten berechnen.

<!-- Folie 4 -->
Noch einmal systematisch (Wdh.+Zusammenfassung aus der Übung)
Der Induktionsschritt (systematisch):
Wir bezeichnen den Input als x∊𝒳
Die “bisherigen Rechenoperationen” sind eine Abbildung Y : 𝒳 → 𝒴
also y := Y(x; wY), deren Ableitungen dY/dwY (x; wY) wir per Induktion kennen.
Die “nächste Rechenoperation” ist eine Abbildung Z : 𝒴 → 𝒵
deren Ableitung dZ/dy und dZ/dwZ wir kennen.
Die Kettenregel erlaubt uns, Z(Y(x; wY); wZ) nach wY abzuleiten:
d/dwY Z(Y(x; wY); wZ) = dZ/dy (y; wZ) · dY/dwY (x; wY)
Auch: d/dwZ Z(Y(x; wY); wZ) = dZ/dwZ (y; wZ).

<!-- Folie 5 -->
Noch einmal systematisch (Wdh.+Zusammenfassung aus der Übung)
Der Induktionsschritt (systematisch):
Wir bezeichnen den Input als x∊𝒳
Die “bisherigen Rechenoperationen” sind eine Abbildung Y : 𝒳 → 𝒴
also y := Y(x; wY), deren Ableitungen dY/dwY (x; wY) wir per Induktion kennen.
Die “nächste Rechenoperation” ist eine Abbildung Z : 𝒴 → 𝒵
deren Ableitung dZ/dy und dZ/dwZ wir kennen.
Spezialfälle:
◼
◼
Wenn die nächste Rechenoperation der Loss ist, gibt es keine “neuen Gewichte”,
dann ist nur die Ableitung nach “bisherigen Gewichten” relevant.
Der Induktionsanfang ist gegeben, indem Y die Identitätsfunktion ist (Ableitung ist 1).

<!-- Folie 6 -->
Noch einmal systematisch (Wdh.+Zusammenfassung aus der Übung)
Der Induktionsschritt (systematisch):
Wir bezeichnen den Input als x∊𝒳
Die “bisherigen Rechenoperationen” sind eine Abbildung Y : 𝒳 → 𝒴
also y := Y(x; wY), deren Ableitungen dY/dwY (x; wY) wir per Induktion kennen.
Die “nächste Rechenoperation” ist eine Abbildung Z : 𝒴 → 𝒵
deren Ableitung dZ/dy und dZ/dwZ wir kennen.
Andere (knappere, kompaktere) Notation:
d/dw Z = dZ/dy · dY/dw

<!-- Folie 7 -->
Noch einmal systematisch (Wdh.+Zusammenfassung aus der Übung)
Der Induktionsschritt (systematisch, aber Kleinbuchstaben als Funktionsnamen):
Wir bezeichnen den Input als x∊𝒳
Die “bisherigen Rechenoperationen” sind eine Abbildung y : 𝒳 → 𝒴
also y := y(x; wy), deren Ableitungen dy/dwy (x; wy) wir per Induktion kennen.
Die “nächste Rechenoperation” ist eine Abbildung z : 𝒴 → 𝒵
deren Ableitung dz/dy und dz/dwZ wir kennen.
Andere (knappere, kompaktere) Notation:
dz/dw = dz/dy · dy/dw

<!-- Folie 8 -->
Nicht konkret genug? Ein weiteres einfaches Beispiel
Wir können als Input x∊𝒳 ⊆ℝn wählen (n-dimensionaler Input).
Im Beispiel soll y := y(x; w) := w · x sein, also ein linearer Layer.
Die “nächste Rechenoperation” ist eine Abbildung z : ℝ → ℝ
und zwar z := z(y) := ReLU(y) = max(0, y). Die Ableitung nach y ist [y > 0].
Aus dz/dw = dz/dy · dy/dw
wird also [y > 0] · x.

<!-- Folie 9 -->
Nicht konkret genug? Ein weiteres einfaches Beispiel
Wir können als Input x∊𝒳 ⊆ℝn wählen (n-dimensionaler Input).
Im Beispiel soll y := y(x; w) := w · x sein, also ein linearer Layer.
Die “nächste Rechenoperation” ist eine Abbildung z : ℝ → ℝ
und zwar z := z(y) := ReLU(y) = max(0, y). Die Ableitung nach y ist [y > 0].
Aus dz/dw = dz/dy · dy/dw
wird also [y > 0] · x.
Übungsaufgabe: erweitern Sie den linearen Layer um ein zweites Neuron (also ein
weiterer Gewichtsvektor v ∊ ℝn tritt auf) und erweitern Sie die Berechnung um eine
Loss-Funktion ǁz - zground truthǁ2

## Latent Spaces von LLMs /

<!-- Folie 10 -->
Wort-Vektor-Einbettungen
geometrisch verstehen

## Arithmetik im latent Space

<!-- Folie 11 -->
word2vec
Der Klassiker: KING - MAN + WOMAN = QUEEN
Also ist WOMAN - MAN die Richtung “feminin”

<!-- Folie 12 -->
word2vec, analog aber in allen LLMs
Der Klassiker: KING - MAN + WOMAN = QUEEN
Also ist WOMAN - MAN die Richtung “feminin”
Auch:
◼ PARIS - FRANCE + ITALY = ROME
(also PARIS - FRANCE die Richtung “Hauptstadt”)
◼ WALKING - WALK + SWIMMING = SWAM
(also WALKING - WALK die Richtung “Vergangenheit”)
◼ BIGGER - BIG = BIGGEST - BIGGER
(also Steigerung der Intensität als Richtung)

<!-- Folie 13 -->
word2vec, analog aber in allen LLMs
Der Klassiker: KING - MAN + WOMAN = QUEEN
Also ist WOMAN - MAN die Richtung “feminin”
Auch:
◼ PARIS - FRANCE + ITALY = ROME
(also PARIS - FRANCE die Richtung “Hauptstadt”)
◼ WALKING - WALK + SWIMMING = SWAM
(also WALKING - WALK die Richtung “Vergangenheit”)
◼ BIGGER - BIG = BIGGEST - BIGGER
(also Steigerung der Intensität als Richtung)
r
u
l
ns
e
g
ei

## Bolukbasi et.al. 2016: Debiasing Word Embeddings

<!-- Folie 14 -->

## Arithmetik im latent Space

<!-- Folie 15 -->
word2vec, analog aber in allen LLMs
Ein Vektor im latent Space ist ausdrucksstärker als ein Token,
kann interpolieren und Superposition ausdrücken:
Statt “Katze” oder “Hund” geht auch
½ Katze + ½ Hund
oder auch
t*Katze + (1-t)*Hund.

<!-- Folie 16 -->
word2vec, analog aber in allen LLMs
Ein Vektor im latent Space ist ausdrucksstärker als ein Token,
kann interpolieren und Superposition ausdrücken:
Statt “Katze” oder “Hund” geht auch
½ Katze + ½ Hund
oder auch
t*Katze + (1-t)*Hund.
Aber: decode(t*Katze + (1-t)*Hund) ist entweder Katze oder Hund,
Es gibt kein “dazwischen”-Token außerhalb des Vokabulars.

## Diskreter Latent Space

<!-- Folie 17 -->
Bei Word2vec und LLMs mit einem Vokabular von N Token
können nur genau N Vektoren im latent Space direkt zu Token dekodiert
werden, für jeden anderen Vektor werden nahe liegende solche
Vektoren ausgewählt zum Dekodieren.

<!-- Folie 18 -->
Bei Word2vec und LLMs mit einem Vokabular von N Token
können nur genau N Vektoren im latent Space direkt zu Token dekodiert
werden, für jeden anderen Vektor werden nahe liegende solche
Vektoren ausgewählt zum Dekodieren.
Gegeben ein Vektor im latent Space, welches Token wählen wir aus?
→ Sampling-Strategie

<!-- Folie 19 -->
Sampling-Strategien
Gegeben Vektor v∊ℝn, welches Token t∊Vokabular wählen wir?
◼ Berechne für jedes t∊Vokabular den Abstand d(v, code(t))
z.B. im Kosinus-Abstand 1 - cos(Winkel(v, code(t)))
und wähle t sodass dieser Abstand minimal wird (top 1 token).

<!-- Folie 20 -->
Sampling-Strategien
Gegeben Vektor v∊ℝn, welches Token t∊Vokabular wählen wir?
◼ Berechne für jedes t∊Vokabular den Abstand d(v, code(t))
z.B. im Kosinus-Abstand 1 - cos(Winkel(v, code(t)))
und wähle t sodass dieser Abstand minimal wird (top 1 token).
◼ Betrachte auf allen Token t die Verteilung Softmax(d(v, code(t)))
Sample aus dieser Verteilung.

<!-- Folie 21 -->
Sampling-Strategien
Gegeben Vektor v∊ℝn, welches Token t∊Vokabular wählen wir?
◼ Berechne für jedes t∊Vokabular den Abstand d(v, code(t))
z.B. im Kosinus-Abstand 1 - cos(Winkel(v, code(t)))
und wähle t sodass dieser Abstand minimal wird (top 1 token).
◼ Betrachte auf allen Token t die Verteilung Softmax(d(v, code(t)))
Sample aus dieser Verteilung.
◼ Für eine natürliche Zahl k (z.B. k=5) wähle die 5 Token t1,...,t5 aus,
sodass kein t mit d(v, code(t)) > d(v, code(ti)) existiert.
Sample mit Verteilung Softmax(d(v, code(ti))) aus {t1,...,t5}.

<!-- Folie 22 -->
Sampling-Strategien
Gegeben Vektor v∊ℝn, welches Token t∊Vokabular wählen wir?
◼ Berechne für jedes t∊Vokabular den Abstand d(v, code(t))
z.B. im Kosinus-Abstand 1 - cos(Winkel(v, code(t)))
und wähle t sodass dieser Abstand minimal wird (top 1 token).
◼ Betrachte auf allen Token t die Verteilung Softmax(d(v, code(t)))
Sample aus dieser Verteilung.
◼ Für eine natürliche Zahl k (z.B. k=5) wähle die 5 Token t1,...,t5 aus,
sodass kein t mit d(v, code(t)) > d(v, code(ti)) existiert.
Sample mit Verteilung Softmax(d(v, code(ti))) aus {t1,...,t5}.
◼ Verändere die Verteilung: Richtung Top 1: niedrige Temperatur,
Richtung Gleichverteilung: hohe Temperatur

<!-- Folie 23 -->
Sampling-Strategien: Temperature Scaling
Gegeben Vektor v∊ℝn, welches Token t∊Vokabular wählen wir?
Gegeben eine Temperatur T>0, berechne die Verteilung:
Pi = exp(vi / T) / ( Σj exp(vj / T) )
D.h. die Einträge von v werden durch T geteilt,
Dann wird mit Softmax eine Wahrscheinlichkeitsverteilung daraus.

<!-- Folie 24 -->
Sampling-Strategien: Temperature Scaling
Gegeben Vektor v∊ℝn, welches Token t∊Vokabular wählen wir?
Gegeben eine Temperatur T>0, berechne die Verteilung:
Pi = exp(vi / T) / ( Σj exp(vj / T) )
D.h. die Einträge von v werden durch T geteilt,
Dann wird mit Softmax eine Wahrscheinlichkeitsverteilung daraus.
Großes T > 1: die verschiedenen Pi werden sich ähnlicher
Kleines T < 1: die großen Pi werden größer, die kleinen Pi werden
kleiner.

## Latent Spaces von Autoencodern

<!-- Folie 25 -->
und VAEs und GANs für Bilder

## Latent Space eines Autoencoders für Bilder

<!-- Folie 26 -->
Erinnerung
Bei Word2vec und LLMs mit einem Vokabular von N Token
können nur genau N Vektoren im latent Space direkt zu Token dekodiert
werden, für jeden anderen Vektor werden nahe liegende solche
Vektoren ausgewählt zum Dekodieren.
Bei Autoencodern für Bilder ist dies anders:
Jeder Vektor im latent Space lässt sich zu einem Bild dekodieren.
Damit lässt sich z.B. zwischen Hund und Katze interpolieren.

<!-- Folie 28 -->
Autoencoder vs. GANs
Der Generator eines GANs ist typischerweise gegeben durch eine
Verteilung auf einem latent Space, aus der gesampelt wird (i.d.R. eine
Standardnormalverteilung) und ein Decoder, der aus dem latenten
Vektor ein tatsächliches Bild generiert.

<!-- Folie 29 -->
Autoencoder vs. GANs
Der Generator eines GANs ist typischerweise gegeben durch eine
Verteilung auf einem latent Space, aus der gesampelt wird (i.d.R. eine
Standardnormalverteilung) und ein Decoder, der aus dem latenten
Vektor ein tatsächliches Bild generiert.
Um einen guten Decoder zu bekommen, ist vor dem adversarial
Training ein Pretraining in einem Autoencoder-Setup sinnvoll. Daher ist
der latent Space zunächst der selbe.

<!-- Folie 30 -->
Autoencoder vs. GANs
Der Generator eines GANs ist typischerweise gegeben durch eine
Verteilung auf einem latent Space, aus der gesampelt wird (i.d.R. eine
Standardnormalverteilung) und ein Decoder, der aus dem latenten
Vektor ein tatsächliches Bild generiert.
Um einen guten Decoder zu bekommen, ist vor dem adversarial
Training ein Pretraining in einem Autoencoder-Setup sinnvoll. Daher ist
der latent Space zunächst der selbe.
Nach dem GAN-Training des Decoders passen Encoder und Decoder
nicht mehr zusammen, d.h. Der Rekonstruktions-Loss steigt, während
der Adversarial Loss sinkt.

<!-- Folie 31 -->
Autoencoder vs. VAE
Der Encoder eines VAE kodiert ein Eingabebild x als Paar
(vx, σx), wobei vx∊ℝn ein latenter Vektor wie beim Autoencoder ist.
Nach erfolgreichem Training ist
decode(vx) ≈ x

## Autoencoder (AE)

<!-- Folie 32 -->
Beispiel
Mit 3 Datenpunkten,
Variation
Bild im latenten Raum:
+ε

## Variational Autoencoder (VAE)

<!-- Folie 33 -->
Beispiel
Mit 3 Datenpunkten,
2.Variation
Bild im latenten Raum:
+ 𝝈ε

## Variational Autoencoder (VAE) - Recap

<!-- Folie 34 -->

## Latent Space eines Autoencoders für Bilder

<!-- Folie 35 -->
Autoencoder vs. VAE
Der Encoder eines VAE kodiert ein Eingabebild x als Paar
(vx, σx), wobei vx∊ℝn ein latenter Vektor wie beim Autoencoder ist.
Nach erfolgreichem Training ist
decode(vx) ≈ x
Der Unterschied vom VAE zum AE liegt im Training:
Statt decode(vx) mit x zu vergleichen als Loss wird
decode(vx+ε) mit x verglichen, wobei ε Varianz σx2 hat.

<!-- Folie 36 -->
Autoencoder vs. VAE
Der Encoder eines VAE kodiert ein Eingabebild x als Paar
(vx, σx), wobei vx∊ℝn ein latenter Vektor wie beim Autoencoder ist.
Der Unterschied vom VAE zum AE liegt im Training:
Statt decode(vx) mit x zu vergleichen als Loss wird
decode(vx+ε) mit x verglichen, wobei ε Varianz σx2 hat.
Nach erfolgreichem Training ist dann auch
decode(vx) ≈ x
Aber der latent Space bzw. Decoder sieht anders aus als beim AE.

<!-- Folie 37 -->
Autoencoder vs. VAE
Der Encoder eines VAE kodiert ein Eingabebild x als Paar
(vx, σx), wobei vx∊ℝn ein latenter Vektor wie beim Autoencoder ist.
Der Unterschied vom VAE zum AE liegt im Training:
Häufig wird zusätzlich zum +ε Trick auch noch ein Summand zur
Loss-funktion hinzugefügt, damit die Codes der Trainingsdaten im latent
Space ungefähr standardnormalverteilt sind (Variational Loss).
→ So kann man später aus Standardnormalverteilung im latent Space
sampeln, und bleibt in der gelernten Verteilung.

## Arvanitidis et.al. 2017: Latent Space Oddity

<!-- Folie 38 -->

## Anwendungsbeispiele

<!-- Folie 39 -->

## Beispiel hAInrich Chatbot

<!-- Folie 40 -->
hAInrich: Get answers quickly (https://www.heicad.hhu.de/lehre/masters-programme-ai-and-data-science/hainrich)
Die Anwendung ist ein Interface zu einer Wissens-Datenbank,
eine semantische Suche im Gewand eines Chatbots.

<!-- Folie 41 -->
hAInrich: Get answers quickly (https://www.heicad.hhu.de/lehre/masters-programme-ai-and-data-science/hainrich)
Die Anwendung ist ein Interface zu einer Wissens-Datenbank,
eine semantische Suche im Gewand eines Chatbots.
Das Wissen liegt vor als Frage-Antwort-Pärchen-Liste (handgeschrieben: FAQ).
Ziel: eine beliebige Frage ‘korrekt’ beantworten

<!-- Folie 42 -->
hAInrich: Get answers quickly (https://www.heicad.hhu.de/lehre/masters-programme-ai-and-data-science/hainrich)
Die Anwendung ist ein Interface zu einer Wissens-Datenbank,
eine semantische Suche im Gewand eines Chatbots.
Das Wissen liegt vor als Frage-Antwort-Pärchen-Liste (handgeschrieben: FAQ).
Ziel: eine beliebige Frage ‘korrekt’ beantworten
Nebenbedingung: kein Logging (DSGVO), geringe Last auf Server (Kosten)

<!-- Folie 43 -->
hAInrich: Get answers quickly (https://www.heicad.hhu.de/lehre/masters-programme-ai-and-data-science/hainrich)
Die Anwendung ist ein Interface zu einer Wissens-Datenbank,
eine semantische Suche im Gewand eines Chatbots.
Das Wissen liegt vor als Frage-Antwort-Pärchen-Liste (handgeschrieben: FAQ).
Ziel: eine beliebige Frage ‘korrekt’ beantworten
Nebenbedingung: kein Logging (DSGVO), geringe Last auf Server (Kosten)
Erreichbares Ziel: oft korrekt raten, welche der handgeschriebenen Fragen (mit
vorhandenen Antworten) ungefähr der eingegebenen Nutzer-Frage entspricht.

<!-- Folie 44 -->
hAInrich: Get answers quickly (https://www.heicad.hhu.de/lehre/masters-programme-ai-and-data-science/hainrich)
Wir überlegen gemeinsam: wie implementiert man
eine semantische Suche im Gewand eines Chatbots?

<!-- Folie 45 -->
Implementierung
◼ Vorbereitung:
◼
◼
Wandle vorhandene HTML-FAQ um in JSON (beautifulsoup)
Tokenisiere Fragen & Wandle in Vektor um mit einem LLM
(jede Frage ein Vektor)

<!-- Folie 46 -->
Implementierung
◼ Vorbereitung:
◼
◼
Wandle vorhandene HTML-FAQ um in JSON (beautifulsoup)
Tokenisiere Fragen & Wandle in Vektor um mit einem LLM
(jede Frage ein Vektor)
◼ Anwendung:
◼
◼
◼
Tokenisiere Nutzerinput & Wandle in Vektor um mit dem selben LLM
Vergleiche mit Kosinus-Ähnlichkeit Inputvektor zu Fragenvektoren aus
der Datenbank, zeige Top 3 Treffer an
Zeige zu Top-Treffer die Antwort aus der Datenbank

<!-- Folie 47 -->
Implementierung
◼ Vorbereitung:
◼
◼
Wandle vorhandene HTML-FAQ um in JSON (beautifulsoup)
Tokenisiere Fragen & Wandle in Vektor um mit einem LLM
(jede Frage ein Vektor)
◼ Anwendung:
◼
◼
◼
Tokenisiere Nutzerinput & Wandle in Vektor um mit dem selben LLM
Vergleiche mit Kosinus-Ähnlichkeit Inputvektor zu Fragenvektoren aus
der Datenbank, zeige Top 3 Treffer an
Zeige zu Top-Treffer die Antwort aus der Datenbank
◼ Technisch:
◼
Inferenz vollständig im Browser/Javascript/ONNX, winziges LLM
genügt (20 MB, Downloadzeit = Wartezeit bis Anwendung reagiert)

## Beispiel Emails Klassifizieren

<!-- Folie 48 -->
Aufgabe:
Gegeben ein Postfach mit Emails der vergangenen Jahre,
berechne für neu eingehende Emails,
mit welcher Wahrscheinlichkeit sie beantwortet werden
( = Score, ob eine Email vermutlich eine Antwort erfordert ).

<!-- Folie 49 -->
Aufgabe:
Gegeben ein Postfach mit Emails der vergangenen Jahre,
berechne für neu eingehende Emails,
mit welcher Wahrscheinlichkeit sie beantwortet werden
( = Score, ob eine Email vermutlich eine Antwort erfordert ).
◼
◼
◼
◼
◼
IMAP zum Download von Mails + Metadaten
Muss in “Sent” die “Antwort” zu einer Mail zuordnen
Ggf. Teildatensatz ausschließen (Spam o.ä.)
Text der Mail in Vektor(en) umwandeln
Vektoren in MLP zur Klassifikation füttern, supervised

## Beispiel Empfehlungssystem

<!-- Folie 50 -->
Aufgabe:
Gegeben eine Liste besuchter/gekaufter Items (Artikel, Produkte) pro
Nutzer, empfehle einem neuen Nutzer ein Item, welches interessant ist
(mit hoher Wahrscheinlichkeit angeklickt/gekauft wird).

<!-- Folie 51 -->
Aufgabe:
Gegeben eine Liste besuchter/gekaufter Items (Artikel, Produkte) pro
Nutzer, empfehle einem neuen Nutzer ein Item, welches interessant ist
(mit hoher Wahrscheinlichkeit angeklickt/gekauft wird).
Lösungsansatz:
Neuronales Netz konvertiert Items in Vektoren, sodass Items, die auf
vielen Listen gemeinsam auftreten, zu Vektoren zugeordnet werden, die
einen kleinen (Kosinus)-Abstand zueinander haben (Feature
Engineering / Representation Learning). Dann finde im Latent Space
Items in der Nähe vergangener Items eines Nutzers.

<!-- Folie 52 -->
Aufgabe: Wie trainieren wir das neuronale Netz?
Gegeben eine Liste besuchter/gekaufter Items (Artikel, Produkte) pro
Nutzer, empfehle einem neuen Nutzer ein Item, welches interessant ist
(mit hoher Wahrscheinlichkeit angeklickt/gekauft wird).
Lösungsansatz:
Neuronales Netz konvertiert Items in Vektoren, sodass Items, die auf
vielen Listen gemeinsam auftreten, zu Vektoren zugeordnet werden, die
einen kleinen (Kosinus)-Abstand zueinander haben (Feature
Engineering / Representation Learning). Dann finde im Latent Space
Items in der Nähe vergangener Items eines Nutzers.
