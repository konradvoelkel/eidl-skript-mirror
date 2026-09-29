---
title: "Variational Autoencoder"
short_title: "VAE"
---

# Variational Autoencoder

## Vom Autoencoder zum VAE

### Motivation: probabilistische Modelle

Beim klassischen Autoencoder bildet der Encoder einen Datenpunkt $x$ aus dem Datenraum $\mathbb{R}^D$ auf einen Punkt $\operatorname{enc}(x)$ im latenten Raum $\mathbb{R}^L$ ab, der Decoder einen Punkt $y \in \mathbb{R}^L$ zurück in den Datenraum ($D$ und $L$ sind dieselben Dimensionen wie im [Kapitel „Autoencoder“](14-autoencoder.md)); Ziel ist $\operatorname{MSE}(x, \operatorname{dec}(\operatorname{enc}(x)))$ möglichst klein. Die Modellannahme war aber: Die Punkte $x \in D$ sind eine Stichprobe aus einer *Verteilung*. Können wir die Verteilung direkt mit modellieren, in $\operatorname{enc}(x)$?

**Variation des Ziels**: Auch $\operatorname{MSE}(x, \operatorname{dec}(\operatorname{enc}(x) + \varepsilon))$ soll möglichst klein sein, für einen normalverteilten Fehler $\varepsilon \sim \mathcal{N}(0, 1)$. **Variation des Trainings**: Nach $\operatorname{enc}(x)$ ein $\varepsilon$ sampeln, addieren, dann $\operatorname{dec}$. Der Decoder muss dann nicht nur den Punkt $\operatorname{enc}(x)$, sondern eine ganze Umgebung davon auf $x$ abbilden – der latente Raum wird „glatt“.

Oh: Wie geht Backpropagation für „ein $\varepsilon$ sampeln“? Da $\varepsilon$ nicht von den Gewichten abhängt, ganz normal mit der Kettenregel:

$$
\frac{d}{dw_{\text{enc}}} \operatorname{dec}(\operatorname{enc}(x) + \varepsilon) = \operatorname{dec}'(\operatorname{enc}(x) + \varepsilon) \cdot \frac{d}{dw_{\text{enc}}} \operatorname{enc}(x).
$$

Das gesampelte $\varepsilon$ ist im Rückwärtsdurchlauf einfach eine Konstante.

**Beispiel im latenten Raum.** Mit 3 Datenpunkten: Klassisch sind das 3 Punkte. Mit $+\varepsilon$ werden es 3 Wolken gleicher Größe. Mit $+\sigma\varepsilon$ für einen Skalierungsfaktor $\sigma$ kann man die Wolkengröße steuern. (In diesem Kapitel ist $\sigma$ durchgehend eine Streuung, nicht die logistische Sigmoidfunktion aus dem [Kapitel „Logistische Regression“](../part-lernen/06-logistische-regression.md).) Mit 300 Datenpunkten: Klassisch eine Punktwolke mit Löchern und Ausreißern; gut wäre eine Verteilung, die den latenten Raum lückenlos und gleichmäßig füllt, sodass man an *jeder* Stelle dekodieren kann.

:::{figure} ../images/vl08-latent-3points.png
:width: 90%

Drei Datenpunkte im latenten Raum – klassisch, mit gleichem Rauschen $+\varepsilon$, mit datenabhängigem Rauschen $+\sigma_x\varepsilon$.
:::

:::{figure} ../images/vl08-latent-300points.png
:width: 90%

300 Datenpunkte – ein klassischer Autoencoder lässt Löcher und Ausreißer, ein VAE zieht die Codes zur Standardnormalverteilung.
:::

Modelliere die Verteilung also mit einer Gaußschen Mischung im latenten Raum, in der die Störung $\varepsilon$ von den Daten abhängt: Zu jedem Datenpunkt $x \in D$ brauchen wir zusätzlich zu $\operatorname{enc}(x) \in L$ auch eine Standardabweichung $\sigma_x$ (bzw. besser noch eine Kovarianzmatrix $\operatorname{cov}(x)$), dann $\operatorname{dec}(\operatorname{enc}(x) + \varepsilon)$ mit $\varepsilon \sim \mathcal{N}(0, \sigma_x^2)$. Aber Sampling aus einer Verteilung, deren Parameter $\sigma_x$ von den Gewichten abhängen, lässt sich nicht ableiten. **Reparametrisierungstrick**: statt $\varepsilon \sim \mathcal{N}(0, \sigma_x^2)$ besser

$$
y := \operatorname{enc}(x) + \sigma_x \varepsilon, \qquad \varepsilon \sim \mathcal{N}(0, 1),
$$

denn dann ist $\varepsilon$ wieder eine Konstante und $\sigma_x$ ein ganz normaler Ausgang des Encoders, durch den Gradienten fließen.

### Training

Wie trainiert man einen Variational Autoencoder? Für jeden Datenpunkt $x \in D$ berechne $\operatorname{enc}(x) = (\mu_x, \sigma_x)$ – der Encoder hat jetzt $2L$ Ausgänge –, generiere ein $\varepsilon \sim \mathcal{N}(0, 1)$ und setze $y := \mu_x + \sigma_x \varepsilon$. Die Loss-Funktion ist *naiv* $\operatorname{MSE}(x, \operatorname{dec}(y))$. Das hat einen Haken, und zwar in beide Richtungen: Das Netz kann $\sigma_x \to 0$ lernen und ist dann wieder ein klassischer Autoencoder. Oder es lässt $\mu_x$ und $\sigma_x$ beliebig groß werden, dann explodieren die latenten Vektoren, die Wolken der einzelnen Datenpunkte liegen weit auseinander, und der latente Raum füllt sich nie lückenlos.

Stabileres Training mit dem Extra-Term **Variational Loss**:

$$
L_{\text{VAE}} = \operatorname{MSE}(x, \operatorname{dec}(y)) + D_{KL}\bigl( q(y \mid x) \,\|\, \mathcal{N}(0, 1) \bigr),
$$

wobei $q(y \mid x) = \mathcal{N}(\mu_x, \sigma_x^2)$ die Dichte der latenten Verteilung für ein festes $x$ ist. Dabei sind die beiden Standardnormalverteilungen – das $\mathcal{N}(0,1)$ für $\varepsilon$ und das $\mathcal{N}(0,1)$ im KL-Term – nicht „dieselben“!! Die erste ist die Rauschquelle, die zweite ist die *Prior*-Verteilung, an die sich die Gesamtheit der latenten Verteilungen anschmiegen soll, damit der latente Raum um den Ursprung herum lückenlos gefüllt ist. In der Praxis lässt man den Encoder statt $\sigma_x$ den Logarithmus der Varianz ausgeben, $\ell_x := \ln \sigma_x^2$ (im Code meist `logvar`), damit kein Ausgang auf positive Werte eingeschränkt werden muss; dann ist $\sigma_x = \exp(\ell_x / 2)$. Für Normalverteilungen hat der KL-Term eine geschlossene Form:

$$
D_{KL}\bigl( \mathcal{N}(\mu, \sigma^2) \,\|\, \mathcal{N}(0, 1) \bigr) = \tfrac12 \left( \mu^2 + \sigma^2 - 1 - \ln \sigma^2 \right).
$$

Diese Loss-Funktion ist der negative **ELBO** (evidence lower bound) aus dem Kapitel [Expectation Maximization](https://voelkel.pages.cs.uni-duesseldorf.de/ds-skript/expectation-maximization) in Data Science – bis auf einen Faktor und eine additive Konstante, die daher rühren, dass wir den Rekonstruktionsterm als schlichten MSE schreiben statt als negative Log-Likelihood eines gaußschen Decoders mit fester Varianz. Für die Optimierung macht das keinen Unterschied, für den Vergleich der Zahlenwerte schon.

:::{admonition} Zwei Fragen, die immer kommen
:class: note
*Wie wird $\sigma_x$ berechnet?* Gar nicht aus den Daten, sondern erfunden: $\mu_x$ und $\sigma_x$ sind einfach die $2L$ Ausgänge des Encoders, und der Gradientenabstieg stellt sie so ein, dass der Loss klein wird. Der Encoder lernt, wie unsicher er sich bei jedem Datenpunkt sein darf.

*Was hat das mit PCA und EM zu tun?* Ein linearer Autoencoder ohne Aktivierungsfunktionen findet denselben Unterraum wie PCA ([Kapitel „Autoencoder“](14-autoencoder.md)), nur bis auf Drehung und Vertauschung der Achsen. Ein Gaussian Mixture Model mit EM aus Data Science fittet *wenige* Cluster, jeder mit eigener Normalverteilung, und ordnet jeden Datenpunkt einem Cluster zu. Der VAE geht den umgekehrten Weg: *Jeder* Datenpunkt bekommt seine eigene Normalverteilung im latenten Raum, und der KL-Term sorgt dafür, dass alle zusammen ungefähr eine Standardnormalverteilung ergeben.
:::

### Recap

Ein VAE ist ein Autoencoder, dessen Encoder statt eines Punkts eine Normalverteilung im latenten Raum ausgibt, dessen Decoder aus einer Stichprobe daraus rekonstruiert, und dessen Loss die Rekonstruktion plus die KL-Divergenz zum Standardnormal-Prior ist. Danach kann man neue Daten generieren, indem man $y \sim \mathcal{N}(0, 1)$ sampelt und dekodiert. Schön zusammengefasst in Lilian Wengs Blogpost [From Autoencoder to Beta-VAE](https://lilianweng.github.io/posts/2018-08-12-vae/). VAEs sind heute noch eine Komponente der Bildgeneratoren (DALL-E, Midjourney, Stable Diffusion): Die Diffusion findet im latenten Raum eines VAE statt.

:::{figure} ../images/vl08-vae-schema.png
:width: 90%

Der Variational Autoencoder mit Reparametrisierungstrick: Der Encoder liefert $\mu_x$ und $\sigma_x$, das Rauschen $\varepsilon$ ist eine Konstante für die Backpropagation, der KL-Term zieht die Codes zum Prior.
:::

## Übung

Der variational loss term für eine latente Dimension ist
$\tfrac12\left(\mu^2 + \sigma^2 - \ln \sigma^2 - 1\right)$.

1. Für welches Paar $(\mu, \sigma)$ wird er null? Rechnen Sie nach, dass er dort ein
   Minimum hat.
   *Tipp: Leiten Sie nach $\mu$ und nach $\sigma$ getrennt ab.*
2. Berechnen Sie den Wert für $(\mu,\sigma) = (2, 1)$ und für $(0\ ,\ 0{,}5)$. Welche der
   beiden Abweichungen bestraft der Term stärker?
3. Der Reparametrisierungstrick schreibt $z = \mu + \sigma\varepsilon$ mit
   $\varepsilon \sim \mathcal{N}(0,1)$. Warum lässt sich ohne ihn nicht nach $\mu$ und
   $\sigma$ ableiten?

*Antwortprobe: Bei (2) ist genau ein Wert größer als 1.*

:::{admonition} Weiterlesen
:class: seealso
Prince, *UDL*, Kap. 17 (Variational autoencoders) mit ELBO und Reparametrisierung; Deisenroth et al., *MML*, Kap. 11 (Gaussian mixture models, EM) zum Vergleich. Beide Bücher sind frei verfügbar, siehe [Über dieses Skript](../README.md).
:::
