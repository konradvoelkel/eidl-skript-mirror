---
title: "Universelle Approximation"
short_title: "Universalität"
---

# Universelle Approximation

## Universelle Approximation

### Warum neuronale Netze funktionieren

**Universelles Approximationstheorem, grobe Aussage** (wir erinnern uns an das [Kapitel „Netze von Hand bauen“](12-netze-von-hand.md)): Mit neuronalen Netzen (beliebig viele Neuronen, beliebig viele Layer, fully connected, ReLU) lässt sich jede Funktion beliebig gut approximieren. Der Beweis in fünf Schritten:

1. Jede beschränkte messbare Funktion $f \colon E \subseteq \mathbb{R} \to \mathbb{R}$ ist beliebig gut ($\forall \varepsilon > 0$) durch *einfache Funktionen* $g, h$ approximierbar: $g \le f \le h$ und $0 \le h - g < \varepsilon$. Dabei sind einfache Funktionen endliche Linearkombinationen von Indikatorfunktionen messbarer Mengen. (Stetige Funktionen sind integrierbar, integrierbare Funktionen sind messbar.)
2. Eine Funktion $f \colon E \to \mathbb{R}$ (für $E$ messbar) ist messbar genau dann, wenn es eine Folge einfacher Funktionen $f_n$ gibt, die punktweise gegen $f$ konvergieren und $|f_n| \le |f|$ erfüllen. Eine messbare Funktion ist integrierbar, wenn es eine dominierende integrierbare Funktion $h$ gibt, $|f| \le |h|$. Wir können also sagen: $\{\text{messbare Funktionen}\} \approx \{\text{interessante Funktionen}\}$.
3. Jede einfache Funktion ist beliebig genau approximierbar durch *Stufenfunktionen*, d.h. endliche Linearkombinationen von Indikatorfunktionen von Intervallen. Also: $\{\text{messbare Funktionen}\} \approx \{\text{approximierbar mit Stufenfunktionen}\}$.
4. Eine einzelne Stufe lässt sich mit einem einfachen neuronalen Netz realisieren: Zwei Neuronen mit sehr steilen Sigmoiden an den Intervallgrenzen, mit Gewichten $+h$ und $-h$ in der Ausgabeschicht, ergeben eine Stufe der Höhe $h$ auf dem Intervall (Grafik von Michael Nielsen, Kapitel 4 seines Buchs). Mit ReLUs statt Sigmoiden reichen zwei Neuronen dafür **nicht**: $a\operatorname{ReLU}(x-p) + b\operatorname{ReLU}(x-q)$ ist rechts von beiden Knicken affin mit Steigung $a+b$ und kommt nie auf null zurück – man bekommt eine Rampe mit Plateau, keinen Buckel. Für ein Dreieck über dem Intervall braucht man drei ReLUs, für ein Trapez mit flachem Dach vier.
5. Die leicht zu verstehende Konstruktion mit 2 Hidden Layers bei Michael Nielsen funktioniert auch mit beliebig hoher Ein- und Ausgabedimension, also zur Approximation von Funktionen $\mathbb{R}^n \to \mathbb{R}^n$. Es gibt auch Konstruktionen mit nur 1 Hidden Layer.

Die richtige Frage ist also nie „Geht das mit neuronalen Netzen?“ (Antwort: JA), sondern „*Wie* geht das am *effizientesten* mit neuronalen Netzen?“

:::{figure} ../images/vl11-step-from-sigmoids.png
:width: 90%

Zwei steile Sigmoide mit entgegengesetzten Ausgabegewichten ergeben eine Stufe. Aus Stufen baut man Stufenfunktionen, aus Stufenfunktionen approximiert man alles Messbare.
:::

### Präzisere Ergebnisse

:::{prf:theorem} Universelle Approximation (Pinkus / Kidger–Lyons)
Sei $E \subseteq \mathbb{R}^d$ eine kompakte (d.h. beschränkte und abgeschlossene) Teilmenge. Sei $\sigma \colon \mathbb{R} \to \mathbb{R}$ eine beliebige stetige Funktion, aber keine affin-lineare Abbildung, die in wenigstens einem Punkt stetig differenzierbar mit Ableitung ungleich $0$ ist. Dann gibt es zu jeder stetigen Funktion $f \colon E \to \mathbb{R}^D$ und jedem $\varepsilon > 0$ ein neuronales Netz $n$ mit Aktivierungen $\sigma$ und endlich vielen hidden Layers, je höchstens $d + D + 2$ groß, mit

$$
\sup_{x \in E} \| n(x) - f(x) \| < \varepsilon .
$$
:::

Also: schmale, aber tiefe Netze reichen. Und noch präziser, mit Aussage über die *Größe*:

:::{prf:theorem} Yarotsky (2017)
Es gibt eine Konstante $c$, sodass gilt: Zu jeder $k$-fach stetig differenzierbaren Funktion $f \colon E \to \mathbb{R}^D$ und jedem $\varepsilon > 0$ gibt es ein neuronales Netz $n$ mit ReLU-Aktivierungen und $c \log(1/\varepsilon)$ vielen hidden Layers, insgesamt etwa $c\, \varepsilon^{-d/k}$ Gewichten und $\sup_{x \in E} \| n(x) - f(x) \| < \varepsilon$.
:::

Siehe auch Andreas Thom, *Approximation of functions by neural networks* ([arXiv:1901.10267](https://arxiv.org/abs/1901.10267), 2019). Die Anzahl der Gewichte wächst mit der Eingabedimension $d$ exponentiell (der Fluch der Dimensionalität), aber glattere Funktionen (größeres $k$) brauchen weniger – und die Tiefe wächst nur logarithmisch in der Genauigkeit.

### Neuronale Netze vs. Bäume und Wälder

Umgekehrt lässt sich jedes ReLU-Netz auch als Entscheidungsbaum schreiben: Jedes ReLU-Neuron ist eine Ja/Nein-Entscheidung „$\langle w, x \rangle + b > 0$?“, und die Regionen, in denen alle Entscheidungen feststehen, sind genau die Stücke, auf denen das Netz linear ist (Caglar Aytekin, *Neural Networks are Decision Trees*, [arXiv:2210.05189](https://arxiv.org/abs/2210.05189), 2022). Der Baum ist allerdings exponentiell groß.

## Übung

1. Geben Sie zwei Neuronen mit steilen **Sigmoiden** und Ausgabegewichte an, deren Summe
   die Funktion $f(x) = 1$ für $x \in [1,2]$ und $0$ sonst **näherungsweise** darstellt.
   *Tipp: Zwei steile Stufen an den Stellen $1$ und $2$, die zweite mit umgekehrtem
   Vorzeichen. Der Steilheitsparameter $h$ bestimmt, wie gut die Näherung ist.*
2. Mit **ReLUs** statt Sigmoiden reichen zwei Neuronen nicht. Wie viele brauchen Sie für
   ein Dreieck über $[1,2]$, wie viele für ein Trapez mit flachem Dach?
   *Tipp: Sehen Sie sich an, welche Steigung die Summe rechts von allen Knicken hat, und
   was sie sein müsste, damit die Funktion wieder auf $0$ zurückkommt.*
3. Wie viele Neuronen brauchen Sie für eine Treppenfunktion mit $k$ Stufen?

*Antwortprobe: Die beiden Zahlen in (2) unterscheiden sich um genau eins, und die Antwort
auf (3) ist linear in $k$.*

:::{admonition} Weiterlesen
:class: seealso
Prince, *UDL*, Kap. 3 (Universal approximation theorem), Kap. 4 (Depth vs. width) und Kap. 20 (Why does deep learning work?). Das Buch ist frei verfügbar, siehe [Über dieses Skript](../README.md).
:::
