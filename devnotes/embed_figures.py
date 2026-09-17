#!/usr/bin/env python3
"""Ersetzt `<!-- TODO Abbildung ... -->`-Marker in den Kapiteln durch figure-Direktiven.
Marker, für die es (noch) kein Bild gibt, bleiben stehen (Liste am Ende)."""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# (eindeutiger Teilstring des TODO-Kommentars) -> (Bilddatei(en), Bildunterschrift)
FIG = {
    "Segmentation with Gaussian mixture": ("vl01-gmm-segmentation.png", "Ein generatives Modell in Aktion: Ein Gaussian Mixture Model mit zwei Komponenten wird an das Histogramm der Pixelwerte gefittet und trennt so Vorder- und Hintergrund (nach einem Beispiel aus den Scipy Lectures)."),
    "two-class demo data": ("vl01-blobs-linreg.png", "Zwei linear trennbare Klassen (links) und eine lineare Regression mit der Klasse als abhängiger Variable (rechts): Die Vorhersage ist eine reelle Zahl, die man bei $\\tfrac12$ abschneiden kann."),
    "schematisches Neuron": ("vl01-neuron.png", "Das McCulloch-Pitts-Neuron: gewichtete Summe der Eingaben, dann eine nichtlineare Aktivierungsfunktion."),
    "MLP mit 3 Eingabeneuronen": ("vl01-mlp.png", "Ein Multilayer Perceptron mit 3 Eingaben, einer versteckten Schicht aus 4 Neuronen und einem Ausgabeneuron. Jeder Pfeil ist ein Gewicht."),
    "make_blobs-Daten in R^2 mit Trenngerade": ("vl02-perceptron-updates.png", "Die Perzeptronregel bei der Arbeit: Trenngerade $w \\cdot x + b = 0$ nach 0, 1, 2 und 3 Epochen über 60 Datenpunkte, Lernrate $r = 0{,}05$."),
    "Regressionsgerade auf 0/1-Daten": (["vl03-linreg-classification-1d.png", "vl03-linreg-classification-2d.png"], "Lineare Regression zur Klassifikation. Oben, eindimensionaler Regressor: Regressionsgerade durch die 0/1-Daten, harte Klassifikation mit Entscheidungsgrenze $x^*$, und die $\\tanh$-Variante. Unten, zweidimensionaler Regressor: Die Entscheidungsgrenze ist eine Gerade, die Regressionsfunktion eine Ebene."),
    "Plot von σ(x)": ("vl04-sigmoid.png", "Das Standardsigmoid $\\sigma$, der Tangens hyperbolicus als umskaliertes Sigmoid, und die Ableitung $\\sigma' = \\sigma(1-\\sigma)$ mit Maximum $\\tfrac14$ bei $0$."),
    "Ergebnis der linearen Regression (Folie 44)": ("vl04-lin-vs-log-regression.png", "Dieselben 0/1-Daten, einmal mit linearer Regression (MSE-Loss) und einmal mit logistischer Regression (BCE-Loss) gefittet."),
    "Ergebnis der logistischen Regression, S-Kurve": None,  # im selben Bild wie oben
    "Loss-Gebirge über der w-Ebene": ("vl05-loss-landscape.png", "Ein (erfundenes) Loss-Gebirge über der $w$-Ebene mit zwei Gradientenabstiegspfaden von verschiedenen Startpunkten. Beide landen im selben Tal – das ist nicht immer so."),
    "Tafelbild Gradientenabstieg": ("vl05-tafelbild-gradientenabstieg.jpg", "Tafelbild zum Gradientenschritt von Hand (WiSe 2025/26)."),
    "die drei Loss-Kurven": ("vl05-loss-curves.png", "Drei Loss-Funktionen für ein Sample der Klasse $y = 1$ in Abhängigkeit vom Wert der Entscheidungsfunktion $f(x)$."),
    "x → [w_erst] → σ → [w_zweit]": ("vl06-two-neurons.png", "Beispielsetup 1: zwei Neuronen hintereinander."),
    "ReLU-Graph; Summe von drei ReLUs": ("vl06-relu-sum.png", "Links die ReLU, rechts eine gewichtete Summe von drei verschobenen ReLUs: eine stückweise lineare Funktion mit Knicken an den Verschiebungen."),
    "ReLU, ELU, Swish, GELU": ("vl06-activations.png", "Aktivierungsfunktionen im Vergleich. ELU, Swish und GELU sind im negativen Bereich nicht konstant null."),
    "Autoencoder schematisch (Michaela Massi": ("vl06-autoencoder-schema.png", "Autoencoder schematisch: Encoder, Flaschenhals (latenter Vektor), Decoder."),
    "Rekonstruktion Autoencoder vs. PCA": ("vl06-ae-vs-pca.png", "Rekonstruktion von 8×8-Ziffern aus scikit-learn durch PCA mit 4 Komponenten und durch einen kleinen Autoencoder mit $L = 4$ (erzeugt mit `sklearn.neural_network.MLPRegressor`)."),
    "Heatmap von ReLU(x)+ReLU(y)": ("vl07-or-nor-heatmap.png", "OR und NOR als Funktionen auf ganz $\\mathbb{R}^2$: Die vier Booleschen Ecken sind markiert, die schwarze Linie ist die Nullstellenmenge."),
    "XOR-Region; Playground-Lösungen": (["vl07-xor-region.png", "vl07-xor-playground-3hidden.png", "vl07-xor-playground-2hidden.png"], "Oben: XOR als Schnitt von NAND und OR. Unten: Vom Gradientenabstieg gefundene Approximationen im TensorFlow Playground mit 3 bzw. 2 versteckten Schichten."),
    "x² und stückweise lineare Interpolation": ("vl07-square-interpolation.png", "$x^2$ auf $[-3, 3]$ und die stückweise lineare Interpolation $Q(x)$ an ganzzahligen Stützstellen, ein Netz mit 6 ReLU-Neuronen."),
    "Autoencoder-Layout, mit NN-SVG": None,  # Schema bereits oben im Kapitel
    "Label-Autoencoder-Architektur": ("vl07-label-autoencoder.png", "Label Autoencoder: ein Encoder, zwei Köpfe, zwei Loss-Terme."),
    "Sparse latents vs. dense latents": ("vl08-sparse-vs-dense.png", "Latente Vektoren von fünf Datenpunkten (Zeilen), 16 Dimensionen (Spalten): dicht besetzt vs. dünn besetzt."),
    "Ergebnis-Beispiele MNIST / USPS": None,  # benötigt trainiertes Modell -> TODO bleibt
    "latenter Raum mit 3 bzw. 300 Punkten": (["vl08-latent-3points.png", "vl08-latent-300points.png"], "Oben: drei Datenpunkte im latenten Raum – klassisch, mit gleichem Rauschen $+\\varepsilon$, mit datenabhängigem Rauschen $+\\sigma_x\\varepsilon$. Unten: 300 Datenpunkte – ein klassischer Autoencoder lässt Löcher und Ausreißer, ein VAE zieht die Codes zur Standardnormalverteilung."),
    "VAE-Schema (Lilian Weng)": ("vl08-vae-schema.png", "Der Variational Autoencoder mit Reparametrisierungstrick: Der Encoder liefert $\\mu_x$ und $\\sigma_x$, das Rauschen $\\varepsilon$ ist eine Konstante für die Backpropagation, der KL-Term zieht die Codes zum Prior."),
    "CBOW und Skip-gram Architekturen": ("vl08-cbow-skipgram.png", "CBOW und Skip-gram: dieselben zwei Matrizen $W$ (Encoder, $N \\to K$) und $W'$ (Decoder, $K \\to N$), einmal von mehreren Kontextwörtern auf ein Wort, einmal umgekehrt."),
    "Satzgraph Die→Katze": ("vl09-sentence-graph.png", "Zwei Sätze als Graph: Der gemeinsame Knoten „frisst“ erzeugt Pfade, die keine ursprünglichen Sätze sind."),
    "Message Passing auf dem Kaffee/Tee-Graphen": ("vl09-message-passing.png", "Message Passing in einem GNN: Jeder Knoten aktualisiert seinen Vektor aus den Vektoren seiner Nachbarn, hier für „Kanne“."),
    "rekurrentes Neuron, gefaltet und entfaltet": ("vl09-rnn-unrolled.png", "Ein rekurrentes Neuron: gefaltet mit der Rückkopplung $U$ (links) und über vier Zeitschritte entfaltet (rechts) – ein tiefes Netz mit geteilten Gewichten."),
    "GRU (Wikipedia": None,  # Link auf Wikipedia im Text
    "Transformer-Architektur (Fig. 1": None,  # Verweis auf Paper im Text
    "Blur-Beispiel, Kantenfindung": ("vl10-blur-edges.png", "Faltung in der Bildverarbeitung: Original, mit einer Gaußfunktion weichgezeichnet, und die Differenz beider – die Kanten."),
    "Hubel & Wiesel": None,
    "Filterfunktionen (peak, constant, box": ("vl10-asml-convolutions.png", "Der ASML-Aktienkurs (Schlusskurse 2020–2025) gefaltet mit vier Filtern. Delta lässt das Signal unverändert, Kasten und Gauß glätten, die Difference of Gaussians hebt Änderungen hervor."),
    "GIMP-Faltungsmatrix": None,
    "Stufe aus zwei steilen Sigmoiden": ("vl11-step-from-sigmoids.png", "Zwei steile Sigmoide mit entgegengesetzten Ausgabegewichten ergeben eine Stufe. Aus Stufen baut man Stufenfunktionen, aus Stufenfunktionen approximiert man alles Messbare."),
    "GAN-Aufbau": ("vl12-gan-schema.png", "Generator und Diskriminator. Der Generator sieht nie echte Daten – nur den Gradienten, der durch den Diskriminator zurückfließt."),
    "CycleGAN-Beispiele": None,
    "StyleGAN-Gesichter": None,
    "2D-Projektion von Wortvektoren mit Parallelogrammen": (["vl13-word-arithmetic.png", "vl13-bolukbasi-fig7.png"], "Oben: Beziehungen zwischen Wörtern als parallele Richtungen im Vektorraum (schematisch). Unten: Figure 7 aus Bolukbasi et al. 2016 – Berufe, projiziert auf die Gender-Richtung."),
    "Interpolation im latenten Raum eines MNIST-Autoencoders": ("vl13-latent-interpolation.png", "Lineare Interpolation zwischen den Codes einer 3 und einer 8 im latenten Raum eines linearen Autoencoders (PCA mit 16 Komponenten auf den 8×8-Ziffern aus scikit-learn): Jeder Zwischenpunkt ist ein Bild."),
    "latenter Raum AE (3 Punkte) vs. VAE": None,  # bereits oben im Kapitel
    "Arvanitidis et al., Figure 1": ("vl13-arvanitidis-fig1.png", "Figure 1 aus Arvanitidis, Hansen, Hauberg: *Latent Space Oddity* (ICLR 2018): Die Gerade im latenten Raum (links) und die Geodäte bezüglich der vom Decoder induzierten Metrik führen zu unterschiedlichen Interpolationen."),
    "Dimpled Manifold": None,  # im Sammelbild unten
    "Manifold-Hypothese, Problemfälle": ("vl15-manifolds.png", "Die Manifold-Hypothese und ihre Grenzen: Daten nahe einer Kurve; Rauschen; zwei sich kreuzende Kurven (keine Mannigfaltigkeit – so sieht Polysemie im Embedding-Raum aus); und das Dimpled Manifold Model, in dem die Entscheidungsgrenze sich an die Daten schmiegt und Adversarial Examples nur einen winzigen Schritt entfernt sind."),
    "Screenshot huggingface.co/tasks": None,
}


def directive(files, caption):
    if isinstance(files, str):
        files = [files]
    if len(files) == 1:
        return f":::{{figure}} ../images/{files[0]}\n:width: 90%\n\n{caption}\n:::"
    inner = "\n".join(f"![](../images/{f})" for f in files)
    return f":::{{figure}}\n:width: 90%\n\n{inner}\n\n{caption}\n:::"


left = []
for md in sorted(ROOT.glob("part-*/[0-9]*.md")):
    s = md.read_text(encoding="utf-8")

    def repl(m):
        body = m.group(1)
        for key, val in FIG.items():
            if key in body:
                if val is None:
                    if key in ("Ergebnis der logistischen Regression, S-Kurve", "Autoencoder-Layout, mit NN-SVG", "latenter Raum AE (3 Punkte) vs. VAE", "Dimpled Manifold"):
                        return ""  # anderswo abgedeckt
                    left.append((md.name, body.strip()))
                    return m.group(0)
                return directive(*val)
        left.append((md.name, body.strip()))
        return m.group(0)

    s2 = re.sub(r"<!-- TODO Abbildung(?:en)?:?(.*?)-->", repl, s, flags=re.S)
    s2 = re.sub(r"\n{3,}", "\n\n", s2)
    if s2 != s:
        md.write_text(s2, encoding="utf-8")
        print("updated", md.name)

print("\nVerbleibende TODO-Abbildungen:")
for f, b in left:
    print(" ", f, "–", b[:90])
