#!/usr/bin/env python3
"""Erzeugt die Abbildungen für das Skript in ../images/ (matplotlib, deterministisch).

Aufruf aus dem Projektverzeichnis:  uv run --only-group figures devnotes/make_figures.py

**Nicht mit dem System-Python aufrufen.** Die erzeugten PNGs sind versioniert, und
matplotlib ändert zwischen Minor-Fassungen den Satz: Schriftmetrik, Tick-Wahl,
Leinwandgröße um ein Pixel. Bis zum 2026-10-14 stand hier `python3 …`; dessen matplotlib
(3.10.9) war eine andere Fassung als die angeheftete (3.11.2), und ein unveränderter
Komplettlauf änderte zwei Abbildungen, an denen niemand etwas getan hatte. Wer die echte
Änderung von diesem Rauschen trennen will, braucht beide Male dieselbe Fassung – die
Gruppe `figures` in pyproject.toml heftet sie an. In dieser Gruppe steckt kein torch,
der Lauf kostet also keine Gigabyte.

Gegenprobe: zweimal hintereinander laufen lassen, `git status images/` muss danach
dasselbe zeigen wie nach dem ersten Lauf.

**Jede Abbildung wird beim Speichern geprüft** (`text_kollisionen` in `save`): Texte mit
Mindestabstand, kein Pfeil durch einen Text, Text passt in seine Form, Panel-Titel nicht
Kante an Kante. Ein Befund schreibt die PNG trotzdem, damit man sie ansehen kann, lässt den
Lauf aber mit Fehlercode enden. Entstanden am 2026-11-02, nachdem das Autoencoder-Schema
sieben Wochen lang unlesbar im Buch stand. Was die Prüfung nicht sieht -- Beschriftungen in
Markern, Legenden über Kurven, falsche Inhalte --, sieht nur, wer jede geänderte PNG öffnet.

Acht Dateien kommen aus dem Material von 2025 und liegen in **Sciebo**, nicht im Repo
(siehe `SRC_KANDIDATEN` unten). Fehlt der Ordner, läuft alles andere trotzdem durch; das
Skript nennt am Ende, was fehlte, und endet mit einem Fehlercode.
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Arc, Circle, FancyArrowPatch, FancyBboxPatch, Polygon

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "images"

# Acht Fremddateien kommen nicht aus diesem Skript, sondern aus dem Material von 2025
# (ein Foto, ein Tafelbild, zwei Playground-Bilder, zwei Paper-Abbildungen, ein
# Notebook-Bild, eine Kurstabelle): Sie liegen in Sciebo, nicht im Repo. Der Ordner hieß
# `from_2025/slides` neben dem Buch; seit der Umstellung auf Jahresordner heißt er
# `eidl-25/slides` eine Ebene höher. Bis zum 2026-10-16 stand hier nur der alte Name, und
# weil `vl10_asml_convolutions` alphabetisch die dreißigste Abbildung ist, brach der Lauf
# dort ab -- die letzten fünf Abbildungen hat er nie erreicht.
SRC_KANDIDATEN = [
    ROOT.parent.parent / "eidl-25" / "slides",
    ROOT.parent / "from_2025" / "slides",
]
SRC = next((p for p in SRC_KANDIDATEN if p.is_dir()), SRC_KANDIDATEN[0])

# Die Kurstabelle ist die einzige der acht, die auch **versioniert** vorliegt; sie wird
# deshalb aus dem Repo gelesen und nicht aus Sciebo (byte-gleich geprüft am 2026-10-16).
ASML_CSV = ROOT / "notebooks" / "ASML.csv"

OUT.mkdir(exist_ok=True)

HHU_BLUE = "#006AB3"
HHU_DARK = "#003964"
HHU_ICE = "#B5CBD6"
HHU_GREEN = "#8CB110"
HHU_RED = "#BE0A26"
HHU_ORANGE = "#EE7F00"
GREY = "#777777"

plt.rcParams.update(
    {
        "font.family": "sans-serif",
        "font.size": 11,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.prop_cycle": plt.cycler(color=[HHU_BLUE, HHU_ORANGE, HHU_GREEN, HHU_RED, HHU_DARK]),
        "figure.dpi": 150,
        "savefig.bbox": "tight",
    }
)
rng = np.random.default_rng(0)


# Was `save` an Kollisionen findet, sammelt sich hier; der Lauf endet dann mit Fehlercode.
# Entstanden am 2026-11-02: Das Autoencoder-Schema hatte seit dem 2026-09-17 drei
# übereinanderliegende Überschriften und Pfeile durch "Encoder"/"Decoder" -- unlesbar, aber
# weder der Buchbau noch ein PDF-Check noch der Byte-Vergleich sehen Bildinhalte.
KOLLISIONEN: list[str] = []


def _text_umriss(t, r, rand):
    """Umriss eines Texts in Pixeln als geschlossener Pfad, um `rand` geschrumpft.

    Für gedrehte Texte ist der achsenparallele Rahmen aus `get_window_extent` viel zu groß
    (eine schräge Beschriftung längs eines Pfeils "überlappt" sonst den Pfeil); der Umriss
    ist dann das gedrehte Rechteck. Ein Rechteck hat denselben Mittelpunkt wie sein
    achsenparalleler Rahmen, also genügen Mittelpunkt, Breite, Höhe und Winkel.
    """
    from matplotlib.path import Path
    from mpl_toolkits.mplot3d import art3d, proj3d

    if isinstance(t, art3d.Text3D):
        # Text3D projiziert seine Position nur während draw() und meldet danach die rohe
        # 2D-Position -- alle "z"-Beschriftungen lägen scheinbar an derselben Stelle.
        # Dieselbe Projektion wie in Text3D.draw, vorübergehend eingesetzt.
        xs, ys, _ = proj3d.proj_transform(t._x, t._y, t._z, t.axes.get_proj())
        alt = t._x, t._y
        t._x, t._y = xs, ys
        try:
            bb = t.get_window_extent(r)
        finally:
            t._x, t._y = alt
    else:
        bb = t.get_window_extent(r)
    phi = np.radians(t.get_rotation())
    if abs(np.sin(phi)) < 1e-6:
        w, h = bb.width, bb.height
    else:
        s, ismath = t._preprocess_math(t.get_text())
        w, h, _ = r.get_text_width_height_descent(s, t.get_fontproperties(), ismath=ismath)
    w, h = w - 2 * rand, h - 2 * rand
    if w <= 0 or h <= 0:
        return None
    ecken = np.array([[-w, -h], [w, -h], [w, h], [-w, h], [-w, -h]]) / 2
    c, si = np.cos(phi), np.sin(phi)
    ecken = ecken @ np.array([[c, si], [-si, c]]) + [(bb.x0 + bb.x1) / 2, (bb.y0 + bb.y1) / 2]
    return Path(ecken, closed=True)


def text_kollisionen(fig, abstand=3.0, titelabstand=20.0):
    """Findet Texte, die sich überlappen, und Pfeile, die durch einen Text laufen.

    Drei Prüfungen, alle in Pixeln der gespeicherten Abbildung:

    * Zwei Texte (Titel, Achsen- und Tickbeschriftungen, Legenden, ax.text, Annotationen)
      halten mindestens `abstand` Pixel Abstand. Ein Überlappungstest allein reicht nicht:
      Zwei Panel-Titel, die Kante an Kante stehen, lesen sich als ein Satz.
    * Kein Pfeil (`annotate`, `FancyArrowPatch` aus `arrow()`) läuft durch einen Text; den
      eigenen Text einer Annotation darf er berühren.
    * Ein Text, dessen Mitte in einer Form steht (Kreis, Ellipse, Kasten aus `box()`), passt
      ganz hinein, mit `abstand` Pixeln Luft zum Rand.
    * Panel-Titel, die nebeneinander in einer Zeile stehen, halten `titelabstand` Pixel
      Abstand. Zwei überbreite Titel mit einem Wortabstand dazwischen überlappen nicht, lesen
      sich aber als ein Satz.

    Linien aus `plot` prüft das nicht -- eine Legende über einer Kurve ist oft gewollt, und
    ob sie eine wichtige Stelle verdeckt, sieht nur ein Mensch.
    """
    from matplotlib.patches import Circle, Ellipse, FancyBboxPatch, Rectangle
    from matplotlib.patches import FancyArrowPatch
    from matplotlib.text import Annotation, Text

    rand = -abstand / 2  # jeder Umriss wächst um die Hälfte des Abstands
    fig.canvas.draw()
    r = fig.canvas.get_renderer()
    # Tickbeschriftungen ausserhalb des sichtbaren Bereichs legt matplotlib an, zeichnet sie
    # aber nicht; sie stehen trotzdem mit Text und Position im Baum und dürfen nicht zählen.
    ungezeichnet = set()
    for ax in fig.axes:
        for achse in (ax.xaxis, ax.yaxis):
            lo, hi = sorted(achse.get_view_interval())
            for tick in achse.get_major_ticks() + achse.get_minor_ticks():
                if not lo - 1e-9 * (hi - lo) <= tick.get_loc() <= hi + 1e-9 * (hi - lo):
                    ungezeichnet |= {id(tick.label1), id(tick.label2)}
    texte = []
    for t in fig.findobj(Text):
        if not t.get_visible() or not t.get_text().strip() or id(t) in ungezeichnet:
            continue
        umriss = _text_umriss(t, r, rand)
        if umriss is not None:
            texte.append((t, umriss))
    befunde = []
    for i, (t1, u1) in enumerate(texte):
        for t2, u2 in texte[i + 1:]:
            if u1.intersects_path(u2, filled=True):
                befunde.append(f"Text {t1.get_text()!r} überlappt {t2.get_text()!r}")
    pfeile = [(t.arrow_patch, t) for t in fig.findobj(Annotation) if t.arrow_patch is not None]
    pfeile += [(p, None) for p in fig.findobj(FancyArrowPatch)]
    for p, eigener in pfeile:
        for poly in p.get_path().to_polygons(p.get_transform(), closed_only=False):
            punkte = np.concatenate([np.linspace(a, b, 20) for a, b in zip(poly[:-1], poly[1:])])
            for t, umriss in texte:
                if t is not eigener and umriss.contains_points(punkte).any():
                    befunde.append(f"Pfeil läuft durch Text {t.get_text()!r}")
    titel = [(t, t.get_window_extent(r)) for ax in fig.axes
             for t in (ax.title, ax._left_title, ax._right_title)
             if t.get_visible() and t.get_text().strip()]
    for i, (t1, b1) in enumerate(titel):
        for t2, b2 in titel[i + 1:]:
            gleiche_zeile = min(b1.y1, b2.y1) > max(b1.y0, b2.y0)
            luecke = max(b1.x0, b2.x0) - min(b1.x1, b2.x1)
            if gleiche_zeile and luecke < titelabstand:
                befunde.append(f"Titel {t1.get_text()!r} und {t2.get_text()!r} zu dicht")
    formen = [p for ax in fig.axes for p in ax.patches
              if isinstance(p, (Circle, Ellipse, FancyBboxPatch, Rectangle)) and p.get_visible()]
    for t, umriss in texte:
        ecken = umriss.vertices[:4]
        mitte = ecken.mean(axis=0)
        for p in formen:
            rand_form = p.get_transform().transform_path(p.get_path())
            if not rand_form.contains_point(mitte):
                continue
            # Luft zum Rand: `abstand` plus die halbe Strichstärke der Form, denn der Strich
            # liegt je zur Hälfte innen. Ohne das "passte" "Mühle" mit 0,4 Pixeln in seinen
            # Kreis und klebte sichtbar an der Linie.
            extra = abstand + p.get_linewidth() * fig.dpi / 72 / 2
            richtung = (ecken - mitte) / np.linalg.norm(ecken - mitte, axis=1, keepdims=True)
            if not rand_form.contains_points(ecken + extra * richtung).all():
                befunde.append(f"Text {t.get_text()!r} ragt aus seiner Form")
    return sorted(set(befunde))


def save(fig, name):
    for b in text_kollisionen(fig):
        KOLLISIONEN.append(f"{name}: {b}")
        print(f"KOLLISION {name}: {b}")
    fig.savefig(OUT / f"{name}.png")
    plt.close(fig)
    print("wrote", name)


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


def relu(x):
    return np.maximum(0, x)


# ----------------------------------------------------------------------------
# Zeichenhilfen für Netzdiagramme
# ----------------------------------------------------------------------------
def draw_layers(ax, sizes, labels=None, colors=None, x0=0.0, dx=2.0, r=0.28, edge_alpha=0.6):
    """Zeichnet ein vollverbundenes Schichtennetz; gibt Knotenpositionen zurück."""
    pos = []
    for k, n in enumerate(sizes):
        ys = np.linspace(-(n - 1) / 2, (n - 1) / 2, n) if n > 1 else np.array([0.0])
        pos.append([(x0 + k * dx, y) for y in ys])
    for k in range(len(sizes) - 1):
        for (xa, ya) in pos[k]:
            for (xb, yb) in pos[k + 1]:
                ax.plot([xa, xb], [ya, yb], color=GREY, lw=0.8, alpha=edge_alpha, zorder=1)
    for k, layer in enumerate(pos):
        c = (colors or [HHU_BLUE] * len(sizes))[k]
        for (x, y) in layer:
            ax.add_patch(Circle((x, y), r, facecolor=c, edgecolor="white", lw=1.2, zorder=2))
        if labels:
            ax.text(layer[0][0], max(y for _, y in layer) + 0.9, labels[k], ha="center", va="bottom", fontsize=10)
    ax.set_aspect("equal")
    ax.axis("off")
    return pos


def box(ax, xy, w, h, text, fc="white", ec=HHU_BLUE, fontsize=10):
    ax.add_patch(FancyBboxPatch(xy, w, h, boxstyle="round,pad=0.02,rounding_size=0.08", fc=fc, ec=ec, lw=1.5))
    ax.text(xy[0] + w / 2, xy[1] + h / 2, text, ha="center", va="center", fontsize=fontsize)


def arrow(ax, p, q, text=None, color=HHU_DARK, **kw):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=14, color=color, lw=1.4, **kw))
    if text:
        ax.text((p[0] + q[0]) / 2, (p[1] + q[1]) / 2 + 0.12, text, ha="center", va="bottom", fontsize=9, color=color)


# ----------------------------------------------------------------------------
# VL 01
# ----------------------------------------------------------------------------
def vl01_gmm_segmentation():
    from scipy import ndimage
    from sklearn.mixture import GaussianMixture

    n = 128
    # Grauwerte in echten 8-Bit-Einheiten: Hinter- und Vordergrund als zwei Niveaus,
    # dazu Rauschen, danach auf 0..255 beschnitten. Bis zum 2026-10-14 standen hier
    # 0 und 1 plus Rauschen – die Achse hieß "Pixelwert" und lief von -0,5 bis 1,5.
    blobs = ndimage.gaussian_filter(rng.normal(size=(n, n)), sigma=3)
    noise = ndimage.gaussian_filter(rng.normal(size=(n, n)), sigma=1)
    img = np.clip(np.where(blobs > 0.03, 170.0, 70.0) + noise / noise.std() * 18.0, 0, 255)
    gmm = GaussianMixture(2, random_state=0).fit(img.reshape(-1, 1))
    labels = gmm.predict(img.reshape(-1, 1)).reshape(n, n)
    fig, axs = plt.subplots(1, 3, figsize=(10, 3.3))
    axs[0].imshow(img, cmap="gray", vmin=0, vmax=255)
    axs[0].set_title("verrauschtes Bild")
    xs = np.linspace(0, 255, 300)
    axs[1].hist(img.ravel(), bins=60, density=True, color=HHU_ICE)
    for m, v, w in zip(gmm.means_.ravel(), gmm.covariances_.ravel(), gmm.weights_):
        axs[1].plot(xs, w * np.exp(-(xs - m) ** 2 / (2 * v)) / np.sqrt(2 * np.pi * v), lw=2)
    axs[1].set_title("Histogramm + 2 Gaußkurven")
    axs[1].set_xlabel("Pixelwert (0–255)")
    axs[1].set_xlim(0, 255)
    axs[1].set_xticks([0, 64, 128, 192, 255])
    axs[1].set_ylabel("Dichte")
    axs[1].set_yticks([])
    axs[2].imshow(labels, cmap="gray")
    axs[2].set_title("Segmentierung (GMM)")
    for a in (axs[0], axs[2]):
        a.axis("off")
    save(fig, "vl01-gmm-segmentation")


def vl01_blobs_linreg():
    from sklearn.datasets import make_blobs
    from sklearn.linear_model import LinearRegression

    X, y = make_blobs(400, centers=[(-1.5, 0), (1.5, 0)], cluster_std=0.9, random_state=1)
    lr = LinearRegression().fit(X, y)
    fig, axs = plt.subplots(1, 2, figsize=(9, 3.8))
    axs[0].scatter(X[:, 0], X[:, 1], c=y, cmap="viridis", s=12)
    axs[0].set_title("zwei Klassen (Farbe = Label)")
    pred = lr.predict(X)
    sc = axs[1].scatter(X[:, 0], X[:, 1], c=pred, cmap="viridis", s=12)
    axs[1].set_title("lineare Regression (Farbe = $f(x)$)")
    fig.colorbar(sc, ax=axs[1])
    for a in axs:
        a.set_xlabel("$x_1$")
        a.set_ylabel("$x_2$")
    save(fig, "vl01-blobs-linreg")


def vl01_neuron():
    fig, ax = plt.subplots(figsize=(6, 3.6))
    ax.set_xlim(-0.5, 8.5)
    ax.set_ylim(-2.6, 2.6)
    ax.axis("off")
    ys = np.linspace(2, -2, 5)
    for i, y in enumerate(ys, 1):
        ax.add_patch(Circle((0.5, y), 0.3, fc=HHU_ICE, ec=HHU_BLUE))
        ax.text(0.5, y, f"$x_{i}$", ha="center", va="center")
        arrow(ax, (0.85, y), (2.6, 0.15 * y))
        # Beschriftung auf ein Drittel des Pfeils, senkrecht darüber versetzt: in der Mitte
        # lief der steile erste und letzte Pfeil durch sein "w"
        p, q = np.array([0.85, y]), np.array([2.6, 0.15 * y])
        n = np.array([-(q - p)[1], (q - p)[0]]) / np.linalg.norm(q - p)
        m = p + 0.4 * (q - p) + 0.22 * n * (1 if y >= 0 else -1) * (1 if n[1] >= 0 else -1)
        ax.text(*m, f"$w_{i}$", ha="center", va="center", fontsize=9, color=HHU_DARK)
    ax.add_patch(Circle((3.6, 0), 0.95, fc="white", ec=HHU_BLUE, lw=2))
    ax.text(3.6, 0.2, r"$\zeta=\sum_j w_j x_j$", ha="center", va="center", fontsize=10)
    ax.text(3.6, -0.3, r"$y=\tau(\zeta)$", ha="center", va="center", fontsize=10)  # tau: beliebige Aktivierung, sigma ist im Buch die logistische
    arrow(ax, (4.6, 0), (6.6, 0))
    ax.add_patch(Circle((7.0, 0), 0.3, fc=HHU_ICE, ec=HHU_BLUE))
    ax.text(7.0, 0, "$y$", ha="center", va="center")
    save(fig, "vl01-neuron")


def vl01_mlp():
    fig, ax = plt.subplots(figsize=(6, 3.6))
    draw_layers(ax, [3, 4, 1], labels=["Eingabe", "versteckte Schicht", "Ausgabe"],
                colors=[HHU_RED, HHU_GREEN, HHU_BLUE])
    ax.set_xlim(-0.8, 4.8)
    ax.set_ylim(-2.4, 2.8)
    save(fig, "vl01-mlp")


# ----------------------------------------------------------------------------
# VL 02
# ----------------------------------------------------------------------------
def vl02_perceptron_achsenabschnitt():
    """Ein Perzeptron nach einer Epoche, für das Rechenbeispiel zur Geradengleichung im
    Kapitel „Neuron und Perzeptron“. Die Gewichte werden auf zwei Stellen gerundet, damit
    Bild und Text dieselben Zahlen zeigen (die Fehlerrate bleibt dabei 0)."""
    from sklearn.datasets import make_blobs

    X, y = make_blobs(40, centers=[(-1, 3), (2, 0)], cluster_std=0.9, random_state=2)
    Xb = np.hstack([np.ones((len(X), 1)), X])  # Bias-Trick: (b, w1, w2)
    start = np.array([1.0, 1.0, 1.0])
    w = start.copy()
    for xi, yi in zip(Xb, y):
        w = w + 0.5 * (yi - float(w @ xi > 0)) * xi
    b, w1, w2 = np.round(w, 2)
    assert (b, w1, w2) == (1.0, 1.7, -0.49) and np.all((Xb @ [b, w1, w2] > 0) == y)
    achse = -b / w2

    fig, ax = plt.subplots(figsize=(5.6, 5))
    for k, c in [(0, HHU_BLUE), (1, HHU_ORANGE)]:
        ax.scatter(X[y == k, 0], X[y == k, 1], s=20, color=c, label=f"Klasse {k}", zorder=3)
    xs = np.array([-4, 4])
    ax.plot(xs, -(b + w1 * xs) / w2, color=HHU_RED, lw=2, label=r"$w \cdot x + b = 0$")
    ax.axhline(0, color=GREY, lw=0.6)
    ax.axvline(0, color=GREY, lw=0.6)
    ax.annotate("", xy=(w1, achse + w2), xytext=(0, achse),
                arrowprops={"arrowstyle": "-|>", "color": HHU_DARK, "lw": 2, "shrinkA": 0,
                            "shrinkB": 0, "mutation_scale": 14}, zorder=4)
    ax.text(w1 + 0.1, achse + w2 - 0.1, "$w$", color=HHU_DARK, fontsize=13)
    ax.scatter([0], [achse], color=HHU_RED, s=40, zorder=5)
    ax.annotate(rf"$-b/w_2 \approx {achse:.2f}$".replace(".", "{,}"), (0, achse), (-3.6, 3.9),
                fontsize=11, color=HHU_RED, arrowprops={"arrowstyle": "->", "color": HHU_RED})
    ax.set_xlim(-4, 4)
    ax.set_ylim(-2.5, 5.5)
    ax.set_aspect("equal")
    ax.set_xlabel("$x_1$")
    ax.set_ylabel("$x_2$")
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.13), ncol=3, fontsize=9, frameon=False)
    save(fig, "vl02-perceptron-achsenabschnitt")


def vl02_perceptron_updates():
    from sklearn.datasets import make_blobs

    X, y = make_blobs(60, centers=[(-2, -1), (2, 1)], cluster_std=1.0, random_state=3)
    Xb = np.hstack([np.ones((len(X), 1)), X])  # Bias-Trick
    w = np.array([0.0, -1.0, 1.0])
    r = 0.05
    snapshots = [w.copy()]
    for epoch in range(3):
        for xi, yi in zip(Xb, y):
            f = float(w @ xi > 0)
            w = w + r * (yi - f) * xi
        snapshots.append(w.copy())
    fig, axs = plt.subplots(1, 4, figsize=(13, 3.3), sharey=True)
    xs = np.linspace(-5, 5, 2)
    for ax, ws, t in zip(axs, snapshots, ["Start $w=(0,-1,1)$", "nach 1 Epoche", "nach 2 Epochen", "nach 3 Epochen"]):
        ax.scatter(X[:, 0], X[:, 1], c=y, cmap="viridis", s=16)
        if abs(ws[2]) > 1e-9:
            ax.plot(xs, -(ws[0] + ws[1] * xs) / ws[2], color=HHU_RED, lw=2)
        err = np.mean((Xb @ ws > 0) != y)
        ax.set_title(f"{t}\nFehlerrate {err:.0%}", fontsize=10)
        ax.set_xlim(-5, 5)
        ax.set_ylim(-4, 4)
        ax.set_xticks([-4, -2, 0, 2, 4])
    save(fig, "vl02-perceptron-updates")


def vl02_perceptron_updates_folie():
    """Zwei Stufen statt vier, für die Folie: ein 1x4-Streifen ist auf 16:9 unlesbar (2026-10-02)."""
    from sklearn.datasets import make_blobs

    X, y = make_blobs(60, centers=[(-2, -1), (2, 1)], cluster_std=1.0, random_state=3)
    Xb = np.hstack([np.ones((len(X), 1)), X])
    w = np.array([0.0, -1.0, 1.0])
    r = 0.05
    start = w.copy()
    for epoch in range(3):
        for xi, yi in zip(Xb, y):
            f = float(w @ xi > 0)
            w = w + r * (yi - f) * xi
    fig, axs = plt.subplots(1, 2, figsize=(7.5, 3.4), sharey=True)
    xs = np.linspace(-5, 5, 2)
    for ax, ws, t in zip(axs, [start, w], ["Start $w=(0,-1,1)$", "nach 3 Epochen"]):
        ax.scatter(X[:, 0], X[:, 1], c=y, cmap="viridis", s=22)
        ax.plot(xs, -(ws[0] + ws[1] * xs) / ws[2], color=HHU_RED, lw=2)
        err = np.mean((Xb @ ws > 0) != y)
        ax.set_title(f"{t}, Fehlerrate {err:.0%}", fontsize=11)
        ax.set_xlim(-5, 5)
        ax.set_ylim(-4, 4)
    save(fig, "vl02-perceptron-updates-folie")


# ----------------------------------------------------------------------------
# VL 03: lineare Regression zur Klassifikation
# ----------------------------------------------------------------------------
def vl03_linreg_classification():
    from sklearn.linear_model import LinearRegression

    x0 = rng.normal(-1.0, 1.0, 80)
    x1 = rng.normal(1.2, 1.0, 80)
    x = np.concatenate([x0, x1])
    y = np.concatenate([np.zeros(80), np.ones(80)])
    lr = LinearRegression().fit(x[:, None], y)
    xs = np.linspace(-4.5, 4.5, 300)
    yhat = lr.predict(xs[:, None])
    xstar = (0.5 - lr.intercept_) / lr.coef_[0]

    fig, axs = plt.subplots(1, 3, figsize=(13, 3.6))
    for a in axs:
        a.scatter(x0, np.zeros_like(x0), s=12, color=HHU_BLUE, label="Klasse 0")
        a.scatter(x1, np.ones_like(x1), s=12, color=HHU_ORANGE, label="Klasse 1")
        a.set_xlabel("$x$ (Regressor)")
    axs[0].plot(xs, yhat, color=HHU_DARK, lw=2, label="Regressionsgerade")
    axs[0].set_title("lineare Regression auf 0/1-Labels")
    axs[1].plot(xs, yhat, color=HHU_DARK, lw=1, alpha=0.4)
    axs[1].plot(xs, (yhat > 0.5).astype(float), color=HHU_RED, lw=2, label=r"$[\hat y > 1/2]$")
    axs[1].axvline(xstar, color=GREY, ls="--")
    axs[1].set_title("harte Klassifikation, Grenze $x^*$")
    axs[2].plot(xs, yhat, color=HHU_DARK, lw=1, alpha=0.4)
    axs[2].plot(xs, 0.5 * (np.tanh(yhat - 0.5) + 1), color=HHU_GREEN, lw=2, label=r"$\frac{1}{2}(\tanh(\hat y - \frac{1}{2})+1)$")
    axs[2].set_title("S-förmig gemacht")
    for a in axs:
        a.set_ylim(-0.6, 1.6)
        a.legend(fontsize=8, loc="upper left")
    save(fig, "vl03-linreg-classification-1d")

    # 2D: Entscheidungsgrenze und Hyperebene
    from sklearn.datasets import make_blobs

    X, y = make_blobs(200, centers=[(-1.5, -1), (1.5, 1)], cluster_std=1.0, random_state=5)
    lr2 = LinearRegression().fit(X, y)
    fig = plt.figure(figsize=(10, 4))
    ax = fig.add_subplot(1, 2, 1)
    ax.scatter(X[:, 0], X[:, 1], c=y, cmap="viridis", s=14)
    gx = np.linspace(-5, 5, 2)
    a, b = lr2.coef_
    ax.plot(gx, (0.5 - lr2.intercept_ - a * gx) / b, color=HHU_RED, lw=2, label=r"$w\cdot x + b = 1/2$")
    ax.set_xlim(-5, 5)
    ax.set_ylim(-4.5, 4.5)
    ax.legend()
    ax.set_title("2D-Regressor: Entscheidungsgrenze ist eine Gerade")
    ax3 = fig.add_subplot(1, 2, 2, projection="3d")
    ax3.scatter(X[:, 0], X[:, 1], y, c=y, cmap="viridis", s=8)
    g1, g2 = np.meshgrid(np.linspace(-5, 5, 10), np.linspace(-4.5, 4.5, 10))
    ax3.plot_surface(g1, g2, lr2.intercept_ + a * g1 + b * g2, alpha=0.3, color=HHU_BLUE)
    ax3.set_title("Regressionshyperebene")
    ax3.set_zlabel("$\\hat y$")
    save(fig, "vl03-linreg-classification-2d")


# ----------------------------------------------------------------------------
# VL 04
# ----------------------------------------------------------------------------
def vl04_sigmoid():
    xs = np.linspace(-6, 6, 400)
    fig, ax = plt.subplots(figsize=(6, 3.3))
    ax.plot(xs, sigmoid(xs), lw=2, label=r"$\sigma(x)$")
    ax.plot(xs, np.tanh(xs), lw=2, ls="--", label=r"$\tanh(x) = 2\sigma(2x)-1$")
    ax.plot(xs, sigmoid(xs) * (1 - sigmoid(xs)), lw=1.5, ls=":", label=r"$\sigma'(x)$")
    ax.axhline(0.5, color=GREY, lw=0.6)
    ax.axvline(0, color=GREY, lw=0.6)
    ax.legend(loc="lower right")
    ax.set_xlabel("$x$")
    save(fig, "vl04-sigmoid")


def vl04_regressions():
    from sklearn.linear_model import LinearRegression, LogisticRegression

    x = np.concatenate([rng.normal(-1.2, 0.9, 60), rng.normal(1.2, 0.9, 60)])
    y = np.concatenate([np.zeros(60), np.ones(60)])
    xs = np.linspace(-4, 4, 300)
    lin = LinearRegression().fit(x[:, None], y)
    log = LogisticRegression().fit(x[:, None], y)
    fig, axs = plt.subplots(1, 2, figsize=(10, 3.5), sharey=True)
    for a in axs:
        a.scatter(x, y, c=y, cmap="viridis", s=14)
        a.set_xlabel("$x$")
    axs[0].plot(xs, lin.predict(xs[:, None]), color=HHU_RED, lw=2)
    axs[0].set_title("lineare Regression (MSE)")
    axs[1].plot(xs, log.predict_proba(xs[:, None])[:, 1], color=HHU_RED, lw=2)
    axs[1].set_title(r"logistische Regression (BCE): $\sigma(wx+b)$")
    axs[0].set_ylim(-0.5, 1.5)
    save(fig, "vl04-lin-vs-log-regression")


# ----------------------------------------------------------------------------
# VL 05
# ----------------------------------------------------------------------------
def vl05_loss_landscape():
    w1, w2 = np.meshgrid(np.linspace(-3, 3, 200), np.linspace(-3, 3, 200))
    L = 0.6 * (w1 - 1) ** 2 + 2.0 * (w2 + 0.5) ** 2 + 0.8 * np.sin(2 * w1) * np.cos(1.5 * w2)
    grad = lambda w: np.array([1.2 * (w[0] - 1) + 1.6 * np.cos(2 * w[0]) * np.cos(1.5 * w[1]),
                               4.0 * (w[1] + 0.5) - 1.2 * np.sin(2 * w[0]) * np.sin(1.5 * w[1])])
    fig, ax = plt.subplots(figsize=(5.5, 4.5))
    cs = ax.contourf(w1, w2, L, levels=30, cmap="Blues_r")
    fig.colorbar(cs, label="$L(w)$")
    for start, rho, c in [((-2.5, 2.5), 0.08, HHU_ORANGE), ((2.5, -2.5), 0.08, HHU_RED)]:
        w = np.array(start, float)
        path = [w.copy()]
        for _ in range(40):
            w = w - rho * grad(w)
            path.append(w.copy())
        path = np.array(path)
        ax.plot(path[:, 0], path[:, 1], "o-", color=c, ms=3, lw=1.2, label=f"Gradientenabstieg ab {start}")
    ax.set_xlabel("$w_1$")
    ax.set_ylabel("$w_2$")
    ax.set_xticks([-2, -1, 0, 1, 2, 3])
    ax.legend(fontsize=8, loc="lower left")
    ax.set_title("Loss-Gebirge über der $w$-Ebene")
    save(fig, "vl05-loss-landscape")


def vl05_loss_curves():
    f = np.linspace(-4, 4, 400)
    fig, ax = plt.subplots(figsize=(6, 3.6))
    ax.plot(f, relu(-f), lw=2, label="Perceptron Loss $\\max(0,-f(x))$")
    ax.plot(f, relu(1 - f), lw=2, label="Hinge Loss $\\max(0,1-f(x))$")
    ax.plot(f, -np.log(sigmoid(f)), lw=2, label="BCE Loss $-\\log\\sigma(f(x))$")
    ax.set_xlabel("Entscheidungsfunktion $f(x)$")
    ax.set_ylabel("$L(y{=}1, f(x))$")
    ax.set_ylim(0, 6)
    ax.legend()
    save(fig, "vl05-loss-curves")


# ----------------------------------------------------------------------------
# VL 06
# ----------------------------------------------------------------------------
def vl06_two_neurons():
    fig, ax = plt.subplots(figsize=(7, 1.8))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 2)
    ax.axis("off")
    ax.add_patch(Circle((0.8, 1), 0.35, fc=HHU_ICE, ec=HHU_BLUE))
    ax.text(0.8, 1, "$x$", ha="center", va="center")
    arrow(ax, (1.2, 1), (3.0, 1), text=r"$w_{\mathrm{erst}}$")
    ax.add_patch(Circle((3.6, 1), 0.5, fc="white", ec=HHU_BLUE, lw=2))
    ax.text(3.6, 1, r"$\sigma$", ha="center", va="center", fontsize=13)
    arrow(ax, (4.2, 1), (6.0, 1), text=r"$w_{\mathrm{zweit}}$")
    ax.add_patch(Circle((6.6, 1), 0.5, fc="white", ec=HHU_BLUE, lw=2))
    ax.text(6.6, 1, r"$\mathrm{id}$", ha="center", va="center", fontsize=11)
    arrow(ax, (7.2, 1), (8.6, 1))
    ax.text(9.2, 1, r"$y_{\mathrm{pred}}$", ha="center", va="center")
    save(fig, "vl06-two-neurons")


def vl06_relu_sum():
    xs = np.linspace(-3, 3, 400)
    fig, axs = plt.subplots(1, 2, figsize=(10, 3.4))
    axs[0].plot(xs, relu(xs), lw=2)
    axs[0].set_title(r"$\mathrm{ReLU}(x)=\max(0,x)$")
    terms = [(1.0, -2.0), (-1.5, 0.0), (2.0, 1.5)]
    total = np.zeros_like(xs)
    for a, b in terms:
        y = a * relu(xs - b)
        total += y
        arg = "x" if b == 0 else f"x {'+' if b < 0 else '-'} {abs(b):g}"  # nicht "x - -2"
        axs[1].plot(xs, y, lw=1, ls="--", label=f"${a:g}\\,\\mathrm{{ReLU}}({arg})$")
    axs[1].plot(xs, total, lw=2.5, color=HHU_DARK, label="Summe")
    axs[1].set_title("Summe von drei ReLUs: stückweise linear")
    axs[1].legend(fontsize=8)
    save(fig, "vl06-relu-sum")


def vl06_activations():
    from scipy.stats import norm

    xs = np.linspace(-4, 4, 400)
    fig, ax = plt.subplots(figsize=(6.5, 3.8))
    ax.plot(xs, relu(xs), lw=2, label="ReLU")
    ax.plot(xs, np.where(xs < 0, 0.01 * xs, xs), lw=1.5, ls=":", label="Leaky ReLU (0,01)")
    ax.plot(xs, np.where(xs < 0, 1.0 * (np.exp(xs) - 1), xs), lw=2, label=r"ELU ($\alpha=1$)")
    ax.plot(xs, xs * sigmoid(xs), lw=2, label="Swish / SiLU")
    ax.plot(xs, xs * norm.cdf(xs), lw=2, ls="--", label="GELU")
    ax.axhline(0, color=GREY, lw=0.6)
    ax.axvline(0, color=GREY, lw=0.6)
    ax.set_ylim(-1.2, 4)
    ax.legend(loc="upper left")
    save(fig, "vl06-activations")


def vl06_autoencoder_schema():
    # draw_layers setzt aspect="equal": Die Zeichenfläche richtet sich nach dem Netz, nicht
    # nach figsize. Bis zum 2026-11-02 stand hier dx=1.8 -- ein schmales Hochformat, in dem die
    # drei Überschriften übereinanderlagen und die Pfeile durch "Encoder"/"Decoder" liefen.
    fig, ax = plt.subplots(figsize=(8, 5.2))
    draw_layers(ax, [8, 5, 3, 5, 8], dx=2.8, r=0.22,
                colors=[HHU_RED, HHU_BLUE, HHU_GREEN, HHU_BLUE, HHU_ORANGE])
    ax.text(0, 4.3, "Input\n$x\\in\\mathbb{R}^D$", ha="center", va="bottom")
    ax.text(5.6, 4.3, "latenter Vektor\n$z\\in\\mathbb{R}^L$", ha="center", va="bottom")
    ax.text(11.2, 4.3, "Rekonstruktion\n$\\hat x\\in\\mathbb{R}^D$", ha="center", va="bottom")
    ax.annotate("", xy=(5.2, -4.5), xytext=(0.4, -4.5), arrowprops={"arrowstyle": "->", "color": HHU_DARK})
    ax.text(2.8, -4.8, "Encoder", ha="center", va="top")
    ax.annotate("", xy=(10.8, -4.5), xytext=(6.0, -4.5), arrowprops={"arrowstyle": "->", "color": HHU_DARK})
    ax.text(8.4, -4.8, "Decoder", ha="center", va="top")
    ax.set_xlim(-1.4, 12.6)
    ax.set_ylim(-5.8, 5.6)
    save(fig, "vl06-autoencoder-schema")


def vl06_ae_vs_pca():
    from sklearn.datasets import load_digits
    from sklearn.decomposition import PCA
    from sklearn.neural_network import MLPRegressor
    from sklearn.preprocessing import MinMaxScaler

    X, _ = load_digits(return_X_y=True)
    X = MinMaxScaler().fit_transform(X)
    k = 4
    pca = PCA(k).fit(X)
    Xp = pca.inverse_transform(pca.transform(X))
    ae = MLPRegressor(hidden_layer_sizes=(32, k, 32), activation="relu", max_iter=600, random_state=0, learning_rate_init=3e-3)
    ae.fit(X, X)
    Xa = ae.predict(X)
    idx = [0, 1, 2, 3, 4, 5, 6, 7]
    fig, axs = plt.subplots(3, len(idx), figsize=(9, 3.6))
    for j, i in enumerate(idx):
        for row, (img, name) in enumerate([(X[i], "Original"), (Xp[i], f"PCA ($k={k}$)"), (Xa[i], f"Autoencoder ($L={k}$)")]):
            axs[row, j].imshow(img.reshape(8, 8), cmap="gray_r", vmin=0, vmax=1)
            axs[row, j].axis("off")
            if j == 0:
                axs[row, j].set_title(name, fontsize=9, loc="left")
    fig.suptitle(f"Rekonstruktion von 8×8-Ziffern: MSE PCA {np.mean((X-Xp)**2):.4f}, AE {np.mean((X-Xa)**2):.4f}", fontsize=10)
    save(fig, "vl06-ae-vs-pca")


# Kleine Netze R^2 -> R als Fläche im R^3: der Graph eines ReLU-Netzes ist ein Polyeder.
# Farben sind Aktivierungsmuster (welche Neuronen an sind), nicht Höhen. Keine Zufallszahlen
# aus dem globalen `rng`: Die Reihenfolge der vl06-Funktionen ist alphabetisch, und ein
# Verbrauch hier würde vl06_relu_sum und vl06_two_neurons verschieben.
_POLY_PAL = ["#9cc3e4", "#f6c48f", "#c5dc86", "#e8a0aa", "#b7a8d6", "#9fd8cf", "#f1dd8a",
             "#c9c9c9", "#d9b48f", "#a9cfa0", "#f0b8d8", "#8fb3c9", "#e2c6a0", "#bfe0f0"]


def _poly_netz(X, Y, schichten, beta=None):
    """Wertet ein Netz mit ReLU (beta=None) oder SiLU_beta(z) = z*sigma(beta z) aus.
    Gibt den Funktionswert und die Vor-Aktivierungen aller versteckten Neuronen zurück."""
    h = np.stack([X, Y], axis=-1)
    vor = []
    for W, b in schichten[:-1]:
        z = h @ W.T + b
        vor.append(z)
        h = np.maximum(z, 0) if beta is None else z * sigmoid(beta * z)
    W, b = schichten[-1]
    return (h @ W.T + b)[..., 0], np.concatenate(vor, axis=-1)


def _poly_stuecke(z):
    """Nummer des Aktivierungsmusters je Gitterpunkt und die passende Farbtabelle."""
    from matplotlib.colors import ListedColormap

    muster = (z > 0).astype(int) @ (1 << np.arange(z.shape[-1]))
    codes, idx = np.unique(muster, return_inverse=True)
    cmap = ListedColormap([_POLY_PAL[k % len(_POLY_PAL)] for k in range(len(codes))])
    return idx.reshape(muster.shape), cmap


def _poly_flaeche(ax, X, Y, f, farben, g):
    """3D-Fläche mit sanfter Schattierung von Hand (matplotlibs `shade` dunkelt zu stark)."""
    fy, fx = np.gradient(f, g, g)
    nrm = np.stack([-fx, -fy, np.ones_like(f)], -1)
    nrm /= np.linalg.norm(nrm, axis=-1, keepdims=True)
    hell = 0.7 + 0.3 * np.clip(nrm @ (np.array([-1.0, -1.0, 2.0]) / np.sqrt(6)), 0, 1)
    farben = farben.copy()
    farben[..., :3] *= hell[..., None]
    s = 3
    ax.plot_surface(X[::s, ::s], Y[::s, ::s], f[::s, ::s], facecolors=farben[::s, ::s],
                    linewidth=0, antialiased=False, shade=False, rstride=1, cstride=1)
    ax.view_init(elev=28, azim=-55)
    ax.set_xticks([]); ax.set_yticks([]); ax.set_zticks([])


def _poly_winkel(grad, abstand):
    """Erste Schicht aus Normalenrichtungen (in Grad) und Abständen zum Nullpunkt."""
    phi = np.radians(grad)
    return np.c_[np.cos(phi), np.sin(phi)], -np.array(abstand)


_POLY_EINE = [_poly_winkel([10, 70, 130, 200, 290], [1.3, -0.9, 0.5, -1.6, 1.1]),
              (np.array([[1.0, -1.4, 0.9, 1.2, -0.8]]), np.array([0.0]))]


def vl06_relu_polyeder():
    r = np.random.default_rng(187)  # eigener Generator, ausgesucht: keine winzigen Splitter
    W1, b1 = _poly_winkel([20, 100, 160, 250], [0.5, -0.4, 0.3, -0.7])
    zwei = [(W1, b1), (r.normal(0, 1, (3, 4)), r.normal(0, 0.8, 3)),
            (r.normal(0, 1, (1, 3)), np.array([0.0]))]
    lim = 3.0
    g = np.linspace(-lim, lim, 301)
    X, Y = np.meshgrid(g, g)
    fig = plt.figure(figsize=(11, 9))
    for zeile, (netz, titel) in enumerate([(_POLY_EINE, r"eine Schicht: $2 \to 5 \to 1$"),
                                           (zwei, r"zwei Schichten: $2 \to 4 \to 3 \to 1$")]):
        f, z = _poly_netz(X, Y, netz)
        idx, cmap = _poly_stuecke(z)
        n1 = netz[0][0].shape[0]
        ax2 = fig.add_subplot(2, 2, 2 * zeile + 2)
        ax2.imshow(idx, origin="lower", extent=(-lim, lim, -lim, lim), cmap=cmap, interpolation="nearest")
        linien = []
        for k in range(z.shape[-1]):
            c = HHU_RED if k < n1 else HHU_DARK
            cs = ax2.contour(X, Y, z[..., k], levels=[0], colors=c, linewidths=1.2)
            linien += [(seg, c) for seg in cs.allsegs[0]]
        ax2.set_xticks([]); ax2.set_yticks([])
        ax2.set_title(f"{idx.max() + 1} lineare Stücke", fontsize=10)
        ax = fig.add_subplot(2, 2, 2 * zeile + 1, projection="3d")
        _poly_flaeche(ax, X, Y, f, cmap(idx), g)
        for seg, c in linien:
            fz, _ = _poly_netz(seg[:, 0], seg[:, 1], netz)
            ax.plot(seg[:, 0], seg[:, 1], fz + 0.02, color=c, lw=1.0, zorder=10)
        ax.set_title(titel, fontsize=11)
    save(fig, "vl06-relu-polyeder")


def vl06_silu_vs_relu():
    lim = 3.0
    g = np.linspace(-lim, lim, 301)
    X, Y = np.meshgrid(g, g)
    _, z_relu = _poly_netz(X, Y, _POLY_EINE)
    idx, cmap = _poly_stuecke(z_relu)
    fig = plt.figure(figsize=(9.5, 8.4))
    for j, (beta, titel) in enumerate([(1.0, "SiLU"), (None, "ReLU")]):
        f, z = _poly_netz(X, Y, _POLY_EINE, beta)
        farben = cmap(idx)
        if beta is not None:
            # aufhellen, wo ein Neuron im Übergang ist: 4 sigma (1 - sigma) ist 1 auf der
            # Knickgeraden des ReLU-Netzes und fällt weit weg davon auf 0
            s = sigmoid(beta * z)
            u = np.max(4 * s * (1 - s), axis=-1)[..., None]
            farben[..., :3] = farben[..., :3] * (1 - 0.75 * u) + 0.75 * u
        ax = fig.add_subplot(2, 2, j + 1, projection="3d")
        _poly_flaeche(ax, X, Y, f, farben, g)
        ax.set_title(titel, fontsize=11)
        ax = fig.add_subplot(2, 2, j + 3)
        ax.imshow(farben, origin="lower", extent=(-lim, lim, -lim, lim), interpolation="nearest")
        for k in range(z_relu.shape[-1]):
            ax.contour(X, Y, z_relu[..., k], levels=[0], colors=HHU_RED, linewidths=0.9,
                       linestyles="-" if beta is None else "--")
        ax.set_xticks([]); ax.set_yticks([])
    save(fig, "vl06-silu-vs-relu")


# ----------------------------------------------------------------------------
# VL 07
# ----------------------------------------------------------------------------
def vl07_or_heatmap():
    g = np.linspace(-1, 2, 200)
    X, Y = np.meshgrid(g, g)
    fig, axs = plt.subplots(1, 2, figsize=(9.5, 4))
    for ax, Z, t in [(axs[0], relu(X) + relu(Y), r"OR: $\mathrm{ReLU}(x)+\mathrm{ReLU}(y)$"),
                     (axs[1], 1 - (relu(X) + relu(Y)), r"NOR: $1-(\mathrm{ReLU}(x)+\mathrm{ReLU}(y))$")]:
        im = ax.pcolormesh(X, Y, Z, cmap="RdBu_r", vmin=-2, vmax=2, shading="auto")
        ax.contour(X, Y, Z, levels=[0], colors="k", linewidths=1)
        for (px, py) in [(0, 0), (0, 1), (1, 0), (1, 1)]:
            ax.plot(px, py, "o", color="white", mec="k", ms=8)
            ax.text(px + 0.07, py + 0.07, f"({px},{py})", fontsize=8)
        ax.set_title(t, fontsize=10)
        ax.set_xlabel("$x$")
        ax.set_ylabel("$y$")
        ax.set_xticks([-1, 0, 1, 2])
        ax.set_yticks([0, 1, 2])  # ohne -1: in der Ecke stiessen x- und y-Beschriftung zusammen
        ax.set_aspect("equal")
        fig.colorbar(im, ax=ax)
    fig.subplots_adjust(wspace=0.45)  # sonst klebt das y des rechten Panels an der linken Farbskala
    save(fig, "vl07-or-nor-heatmap")


def vl07_xor_region():
    g = np.linspace(-0.6, 1.6, 300)
    X, Y = np.meshgrid(g, g)
    OR = (X + Y > 0.5).astype(float)
    NAND = (X + Y < 1.5).astype(float)
    fig, axs = plt.subplots(1, 3, figsize=(11, 3.5))
    for ax, Z, t in [(axs[0], OR, "OR $>0$"), (axs[1], NAND, "NAND $>0$"), (axs[2], OR * NAND, "XOR = AND(NAND, OR)")]:
        ax.pcolormesh(X, Y, Z, cmap="Blues", vmin=0, vmax=1.4, shading="auto")
        for (px, py), lab in zip([(0, 0), (0, 1), (1, 0), (1, 1)], ["F", "T", "T", "F"]):
            ax.plot(px, py, "o", color="white", mec="k", ms=15)
            ax.text(px, py, lab, ha="center", va="center", fontsize=9, fontweight="bold")
        ax.set_title(t)
        ax.set_aspect("equal")
    save(fig, "vl07-xor-region")


def vl07_square_interpolation():
    xs = np.linspace(-3, 3, 400)
    Q = 9 - 5 * relu(xs + 3) + sum(2 * relu(xs - k) for k in range(-2, 3))
    fig, ax = plt.subplots(figsize=(6, 3.8))
    ax.plot(xs, xs ** 2, lw=1.5, ls="--", color=GREY, label="$x^2$")
    ax.plot(xs, Q, lw=2.5, label="$Q(x)$: 6 ReLU-Neuronen")
    ks = np.arange(-3, 4)
    ax.plot(ks, ks ** 2, "o", color=HHU_RED, label="Stützstellen")
    ax.legend()
    ax.set_xlabel("$x$")
    save(fig, "vl07-square-interpolation")


def vl07_label_autoencoder():
    fig, ax = plt.subplots(figsize=(8, 3.6))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 4.5)
    ax.axis("off")
    box(ax, (0.3, 1.7), 1.8, 1.0, "Bild\n$x\\in\\mathbb{R}^{784}$", fc=HHU_ICE)
    box(ax, (3.0, 1.7), 2.0, 1.0, "Encoder")
    box(ax, (5.9, 1.7), 1.4, 1.0, "latent\n$\\mathbb{R}^L$", fc="#fff3e0", ec=HHU_ORANGE)
    box(ax, (8.4, 2.9), 2.0, 1.0, "Decoder")
    box(ax, (8.4, 0.5), 2.0, 1.2, "Linear (10)\n+ Softmax", fontsize=9)
    arrow(ax, (2.1, 2.2), (3.0, 2.2))
    arrow(ax, (5.0, 2.2), (5.9, 2.2))
    arrow(ax, (7.3, 2.4), (8.4, 3.4))
    arrow(ax, (7.3, 2.0), (8.4, 1.0))
    arrow(ax, (10.4, 3.4), (11.3, 3.4))
    arrow(ax, (10.4, 1.0), (11.3, 1.0))
    ax.text(11.4, 3.4, "$\\hat x$ → reconstruction loss (MSE)", va="center", fontsize=9)
    ax.text(11.4, 1.0, "$\\hat y$ → classification loss (CE)", va="center", fontsize=9)
    ax.set_xlim(0, 15.5)
    save(fig, "vl07-label-autoencoder")


# ----------------------------------------------------------------------------
# VL 08
# ----------------------------------------------------------------------------
def vl08_sparse_vs_dense():
    L = 16
    dense = rng.uniform(0.2, 0.9, (5, L))
    sparse = np.where(rng.uniform(size=(5, L)) < 0.15, rng.uniform(0.6, 1.0, (5, L)), rng.uniform(0, 0.05, (5, L)))
    fig, axs = plt.subplots(1, 2, figsize=(10, 2.8))
    for ax, M, t in [(axs[0], dense, "dense latents"), (axs[1], sparse, r"sparse latents ($\varrho\approx0{,}15$)")]:
        ax.imshow(M, cmap="Blues", vmin=0, vmax=1, aspect="auto")
        ax.set_title(t)
        ax.set_xlabel("latente Dimension $j$")
        ax.set_ylabel("Datenpunkt")
    save(fig, "vl08-sparse-vs-dense")


def vl08_latent_variations():
    pts = np.array([[-1.5, 0.5], [1.0, 1.2], [0.3, -1.4]])
    sig = np.array([0.15, 0.5, 0.3])
    fig, axs = plt.subplots(1, 3, figsize=(11, 3.4), sharex=True, sharey=True)
    axs[0].scatter(pts[:, 0], pts[:, 1], s=60, color=HHU_BLUE)
    axs[0].set_title("klassisch: 3 Punkte")
    for i, p in enumerate(pts):
        eps = rng.normal(size=(200, 2)) * 0.3
        axs[1].scatter(*(p + eps).T, s=6, alpha=0.5)
        eps2 = rng.normal(size=(200, 2)) * sig[i]
        axs[2].scatter(*(p + eps2).T, s=6, alpha=0.5)
    axs[1].set_title(r"$+\varepsilon$, gleiche Wolkengröße")
    axs[2].set_title(r"$+\sigma_x\varepsilon$, Größe pro Datenpunkt")
    for a in axs:
        a.set_aspect("equal")
    save(fig, "vl08-latent-3points")

    fig, axs = plt.subplots(1, 2, figsize=(8, 3.6), sharex=True, sharey=True)
    ae = np.vstack([rng.normal(c, 0.25, (100, 2)) for c in [(-2, 1.5), (1.8, 1.2), (0.4, -1.8)]])
    axs[0].scatter(ae[:, 0], ae[:, 1], s=6)
    axs[0].set_title("Autoencoder: Löcher und Ausreißer")
    vae = rng.normal(size=(300, 2))
    axs[1].scatter(vae[:, 0], vae[:, 1], s=6, color=HHU_GREEN)
    axs[1].set_title(r"VAE: latente Codes $\approx\mathcal{N}(0,1)$")
    for a in axs:
        a.set_aspect("equal")
    save(fig, "vl08-latent-300points")


def vl08_vae_schema():
    fig, ax = plt.subplots(figsize=(9, 3))
    ax.set_xlim(0, 13)
    ax.set_ylim(0, 3.5)
    ax.axis("off")
    box(ax, (0.3, 1.2), 1.4, 1.0, "$x$", fc=HHU_ICE)
    box(ax, (2.4, 1.2), 1.8, 1.0, "Encoder")
    box(ax, (5.0, 2.1), 1.2, 0.8, r"$\mu_x$", ec=HHU_ORANGE)
    box(ax, (5.0, 0.5), 1.2, 0.8, r"$\sigma_x$", ec=HHU_ORANGE)
    box(ax, (7.2, 1.2), 1.8, 1.0, r"$y=\mu_x+\sigma_x\varepsilon$", ec=HHU_GREEN, fontsize=9)
    box(ax, (9.8, 1.2), 1.6, 1.0, "Decoder")
    box(ax, (12.0, 1.2), 0.9, 1.0, r"$\hat x$", fc=HHU_ICE)
    arrow(ax, (1.7, 1.7), (2.4, 1.7))
    arrow(ax, (4.2, 1.9), (5.0, 2.5))
    arrow(ax, (4.2, 1.5), (5.0, 0.9))
    arrow(ax, (6.2, 2.5), (7.2, 1.9))
    arrow(ax, (6.2, 0.9), (7.2, 1.5))
    arrow(ax, (9.0, 1.7), (9.8, 1.7))
    arrow(ax, (11.4, 1.7), (12.0, 1.7))
    ax.text(8.1, 0.4, r"$\varepsilon\sim\mathcal{N}(0,1)$", ha="center", fontsize=9, color=HHU_GREEN)
    ax.text(5.6, 3.25, r"$D_{KL}(\mathcal{N}(\mu_x,\sigma_x^2)\,\|\,\mathcal{N}(0,1))$", ha="center", fontsize=9, color=HHU_ORANGE)
    ax.set_xlim(0, 13.2)
    save(fig, "vl08-vae-schema")


def vl08_word2vec():
    fig, axs = plt.subplots(1, 2, figsize=(11, 3.8))
    for ax, t, left, right in [(axs[0], "CBOW: Kontext → Wort", 4, 1), (axs[1], "Skip-gram: Wort → Kontext", 1, 4)]:
        ax.set_xlim(0, 10)
        ax.set_ylim(-2.6, 2.6)
        ax.axis("off")
        ys = np.linspace(1.8, -1.8, left) if left > 1 else [0]
        for y in ys:
            box(ax, (0.2, y - 0.35), 1.6, 0.7, "one-hot\n$\\mathbb{R}^N$", fc=HHU_ICE, fontsize=8)
            arrow(ax, (1.8, y), (3.6, 0))
            if y == ys[0]:
                # Der Pfeil fällt nach rechts ab: Beschriftung rechts darüber, nicht auf ihn
                ax.text(2.9 if left > 1 else 2.7, y / 2 + 0.25, "$W$", ha="left" if left > 1 else "center",
                        va="bottom", fontsize=9, color=HHU_DARK)
        box(ax, (3.6, -0.4), 1.6, 0.8, "$\\mathbb{R}^K$", ec=HHU_ORANGE)
        ys2 = np.linspace(1.8, -1.8, right) if right > 1 else [0]
        for y in ys2:
            arrow(ax, (5.2, 0), (7.0, y))
            if y == ys2[0]:
                ax.text(6.1, y / 2 + 0.25, "$W'$", ha="right" if right > 1 else "center",
                        va="bottom", fontsize=9, color=HHU_DARK)
            box(ax, (7.0, y - 0.35), 2.2, 0.7, "Softmax $\\mathbb{R}^N$", fontsize=8)
        ax.set_title(t)
    save(fig, "vl08-cbow-skipgram")


# ----------------------------------------------------------------------------
# VL 09
# ----------------------------------------------------------------------------
def vl09_sentence_graph():
    nodes = {"Die": (0, 1), "Katze": (2, 1), "frisst": (4, 0), "Mäuse": (6, 1), "Der": (0, -1), "Hund": (2, -1), "Leckerli": (6, -1)}
    edges = [("Die", "Katze"), ("Katze", "frisst"), ("frisst", "Mäuse"), ("Der", "Hund"), ("Hund", "frisst"), ("frisst", "Leckerli")]
    fig, ax = plt.subplots(figsize=(7, 2.8))
    for a, b in edges:
        pa, pb = np.array(nodes[a]), np.array(nodes[b])
        d = (pb - pa) / np.linalg.norm(pb - pa)
        arrow(ax, pa + 0.55 * d, pb - 0.55 * d)
    for n, (x, y) in nodes.items():
        ax.add_patch(Circle((x, y), 0.5, fc=HHU_ICE, ec=HHU_BLUE))
        ax.text(x, y, n, ha="center", va="center", fontsize=9)
    ax.set_xlim(-0.8, 6.8)
    ax.set_ylim(-1.8, 1.8)
    ax.set_aspect("equal")
    ax.axis("off")
    save(fig, "vl09-sentence-graph")


def vl09_message_passing():
    nodes = {"Kaffee": (0, 1), "Tee": (0, -1), "Kanne": (2, 0), "Tasse": (4, 0), "Mühle": (-2, 1)}
    edges = [("Kaffee", "Kanne"), ("Tee", "Kanne"), ("Kanne", "Tasse"), ("Mühle", "Kaffee")]
    fig, axs = plt.subplots(1, 2, figsize=(10, 3))
    for ax, t, hl in [(axs[0], "Graph", None), (axs[1], "Message Passing: Kanne sammelt von Nachbarn", "Kanne")]:
        for a, b in edges:
            ax.plot(*zip(nodes[a], nodes[b]), color=GREY, lw=1.2, zorder=1)
        for n, (x, y) in nodes.items():
            c = HHU_ORANGE if n == hl else HHU_ICE
            ax.add_patch(Circle((x, y), 0.62, fc=c, ec=HHU_BLUE, zorder=2))
            ax.text(x, y, n, ha="center", va="center", fontsize=8, zorder=3)
        if hl:
            for nb in ["Kaffee", "Tee", "Tasse"]:
                pa, pb = np.array(nodes[nb]), np.array(nodes[hl])
                d = (pb - pa) / np.linalg.norm(pb - pa)
                arrow(ax, pa + 0.66 * d, pb - 0.66 * d, color=HHU_ORANGE)
        ax.set_xlim(-2.8, 4.8)
        ax.set_ylim(-1.8, 1.8)
        ax.set_aspect("equal")
        ax.axis("off")
        ax.set_title(t, fontsize=10)
    save(fig, "vl09-message-passing")


def vl09_rnn_unrolled():
    fig, axs = plt.subplots(1, 2, figsize=(10, 3), gridspec_kw={"width_ratios": [1, 3]})
    ax = axs[0]
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.8, 1.8)
    ax.axis("off")
    ax.add_patch(Circle((0, 0), 0.5, fc="white", ec=HHU_BLUE, lw=2))
    ax.text(0, 0, "$h$", ha="center", va="center")
    arrow(ax, (0, -1.6), (0, -0.55), text=None)
    ax.text(0.15, -1.3, "$x_t$", fontsize=9)
    arrow(ax, (0, 0.55), (0, 1.6))
    ax.text(0.15, 1.3, "$y_t$", fontsize=9)
    ax.add_patch(FancyArrowPatch((0.45, 0.25), (0.45, -0.25), connectionstyle="arc3,rad=-1.6", arrowstyle="-|>", mutation_scale=12, color=HHU_ORANGE, lw=1.4))
    ax.text(1.1, 0, "$U$", color=HHU_ORANGE, va="center")
    ax.set_title("gefaltet", fontsize=10)
    ax = axs[1]
    ax.set_xlim(-0.5, 8.5)
    ax.set_ylim(-1.8, 1.8)
    ax.axis("off")
    for t in range(4):
        x = 2 * t + 0.5
        ax.add_patch(Circle((x, 0), 0.5, fc="white", ec=HHU_BLUE, lw=2))
        ax.text(x, 0, f"$h_{t}$", ha="center", va="center")
        arrow(ax, (x, -1.6), (x, -0.55))
        ax.text(x + 0.15, -1.3, f"$x_{t}$", fontsize=9)
        arrow(ax, (x, 0.55), (x, 1.6))
        ax.text(x + 0.15, 1.3, f"$y_{t}$", fontsize=9)
        if t < 3:
            arrow(ax, (x + 0.55, 0), (x + 1.45, 0), text="$U$", color=HHU_ORANGE)
    ax.set_title("entfaltet über die Zeit", fontsize=10)
    save(fig, "vl09-rnn-unrolled")


# ----------------------------------------------------------------------------
# VL 10
# ----------------------------------------------------------------------------
def vl10_blur_edges():
    from PIL import Image
    from scipy import ndimage

    img = np.asarray(Image.open(SRC / "pallino.jpg").convert("L"), dtype=float) / 255
    img = img[::2, ::2]
    blur = ndimage.gaussian_filter(img, 3)
    fig, axs = plt.subplots(1, 3, figsize=(11, 3.6))
    for ax, im, t in [(axs[0], img, "Original"), (axs[1], blur, "Gauß-Blur ($\\sigma=3$)"), (axs[2], img - blur, "Original − Blur = Kanten")]:
        ax.imshow(im, cmap="gray")
        ax.set_title(t)
        ax.axis("off")
    save(fig, "vl10-blur-edges")


def vl10_asml_convolutions():
    import pandas as pd
    from scipy.signal import convolve

    df = pd.read_csv(ASML_CSV, parse_dates=["Date"]).sort_values("Date")
    df = df[(df["Date"] >= "2020-12-15") & (df["Date"] <= "2025-12-15")]
    data = df["Close"].to_numpy()
    n = 30
    t = np.arange(-n, n + 1)
    filters = {
        "Peak (Delta)": (t == 0).astype(float),
        "Kasten (Breite 21)": (np.abs(t) <= 10) / 21,
        "Gauß ($\\sigma=5$)": np.exp(-t ** 2 / 50) / np.exp(-t ** 2 / 50).sum(),
        "DoG ($\\sigma=3$ − $\\sigma=8$)": np.exp(-t ** 2 / 18) / np.exp(-t ** 2 / 18).sum() - np.exp(-t ** 2 / 128) / np.exp(-t ** 2 / 128).sum(),
    }
    fig, axs = plt.subplots(len(filters), 2, figsize=(11, 9),
                            gridspec_kw={"width_ratios": [1, 3], "hspace": 0.55})
    for i, (name, f) in enumerate(filters.items()):
        axs[i, 0].plot(t, f, lw=1.5)
        axs[i, 0].set_title(name, fontsize=9)
        out = convolve(data, f, mode="same")
        if "DoG" in name:
            axs[i, 1].plot(out, lw=1, color=HHU_RED)
        else:
            axs[i, 1].plot(data, lw=0.6, color=GREY, alpha=0.6, label="ASML Close")
            axs[i, 1].plot(out, lw=1.3, color=HHU_RED, label="gefaltet")
        axs[i, 1].set_xlim(0, len(data))
        axs[i, 1].set_yticks([])
    axs[0, 1].legend(fontsize=8)
    axs[-1, 1].set_xlabel("Handelstag")
    fig.suptitle("ASML-Aktienkurs (2020–2025) gefaltet mit verschiedenen Filtern", fontsize=11)
    save(fig, "vl10-asml-convolutions")


# ----------------------------------------------------------------------------
# VL 11
# ----------------------------------------------------------------------------
def vl11_step_from_sigmoids():
    xs = np.linspace(0, 1, 500)
    k = 200
    s1, s2 = sigmoid(k * (xs - 0.3)), sigmoid(k * (xs - 0.6))
    h = 0.8
    fig, axs = plt.subplots(1, 2, figsize=(10, 3.3))
    axs[0].plot(xs, s1, label=r"$\sigma(200(x-0{,}3))$")
    axs[0].plot(xs, s2, label=r"$\sigma(200(x-0{,}6))$")
    axs[0].legend(fontsize=8)
    axs[0].set_title("zwei steile Sigmoide")
    axs[1].plot(xs, h * s1 - h * s2, color=HHU_DARK, lw=2)
    axs[1].set_title("$0{,}8\\cdot\\sigma_1 - 0{,}8\\cdot\\sigma_2$:\n"
                     "eine Stufe der Höhe 0,8 auf $[0{,}3;\\,0{,}6]$")
    axs[1].set_ylim(-0.1, 1)
    save(fig, "vl11-step-from-sigmoids")


# ----------------------------------------------------------------------------
# VL 12
# ----------------------------------------------------------------------------
def vl12_gan_schema():
    fig, ax = plt.subplots(figsize=(9, 3.4))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 4)
    ax.axis("off")
    box(ax, (0.3, 0.4), 1.6, 0.9, r"$z\sim\mathcal{N}(0,I)$", fc=HHU_ICE, fontsize=9)
    box(ax, (2.8, 0.4), 1.8, 0.9, "Generator $G$")
    box(ax, (5.5, 0.4), 1.6, 0.9, "$G(z)$\n(generiert)", fc="#fff3e0", ec=HHU_ORANGE, fontsize=9)
    box(ax, (5.5, 2.6), 1.6, 0.9, "$x$\n(echt)", fc="#e8f5e9", ec=HHU_GREEN, fontsize=9)
    box(ax, (8.4, 1.5), 2.4, 0.9, "Diskriminator $D$")
    box(ax, (11.3, 1.5), 0.9, 0.9, "echt?", fontsize=9)
    arrow(ax, (1.9, 0.85), (2.8, 0.85))
    arrow(ax, (4.6, 0.85), (5.5, 0.85))
    arrow(ax, (7.1, 0.85), (8.4, 1.7))
    arrow(ax, (7.1, 3.05), (8.4, 2.2))
    arrow(ax, (10.8, 1.95), (11.3, 1.95))
    # Der Bogen läuft unter den Kästen entlang; bis zum 2026-11-02 lief er quer durch
    # "Generator G" und über zwei Pfeile.
    ax.text(6.3, -0.75, "Backprop durch $D$ bis in $G$", fontsize=8, color=HHU_RED, ha="center", va="top")
    ax.add_patch(FancyArrowPatch((9.4, 1.45), (3.7, 0.35), connectionstyle="arc3,rad=-0.35", arrowstyle="-|>", mutation_scale=12, color=HHU_RED, lw=1, ls="--"))
    ax.set_xlim(0, 12.4)
    ax.set_ylim(-1.2, 4)
    save(fig, "vl12-gan-schema")


# ----------------------------------------------------------------------------
# VL 13
# ----------------------------------------------------------------------------
def vl13_word_arithmetic():
    words = {"man": (0, 0), "woman": (1.0, 1.6), "king": (3.0, 0.3), "queen": (4.0, 1.9),
             "walk": (0.2, -2.6), "walking": (1.6, -1.8), "swim": (2.8, -2.9), "swimming": (4.2, -2.1)}
    fig, ax = plt.subplots(figsize=(6.5, 5))
    start = {"man", "king", "walk", "swim"}  # von hier geht ein Pfeil nach oben rechts ab
    for w, (x, y) in words.items():
        ax.plot(x, y, "o", color=HHU_BLUE)
        ax.text(x + 0.1, y - 0.12 if w in start else y + 0.1, w, fontsize=10,
                va="top" if w in start else "baseline")
    for a, b, c in [("man", "woman", HHU_ORANGE), ("king", "queen", HHU_ORANGE), ("walk", "walking", HHU_GREEN), ("swim", "swimming", HHU_GREEN)]:
        arrow(ax, words[a], words[b], color=c)
    ax.text(2.2, 1.4, "„feminin“", color=HHU_ORANGE)
    ax.text(2.0, -1.4, "„Verlaufsform“", color=HHU_GREEN)
    ax.set_xlim(-0.8, 5.5)
    ax.set_ylim(-3.6, 2.8)
    ax.set_title("Beziehungen als parallele Richtungen (schematisch)")
    ax.set_xticks([])
    ax.set_yticks([])
    save(fig, "vl13-word-arithmetic")


def vl13_latent_interpolation():
    from sklearn.datasets import load_digits
    from sklearn.decomposition import PCA

    X, y = load_digits(return_X_y=True)
    pca = PCA(16).fit(X)
    a, b = X[y == 3][0], X[y == 8][0]
    za, zb = pca.transform([a, b])
    ts = np.linspace(0, 1, 8)
    fig, axs = plt.subplots(1, len(ts), figsize=(9, 1.6))
    for ax, t in zip(axs, ts):
        img = pca.inverse_transform(((1 - t) * za + t * zb)[None])[0]
        ax.imshow(img.reshape(8, 8), cmap="gray_r")
        ax.set_title(f"$t={t:.2f}$", fontsize=7)
        ax.axis("off")
    fig.suptitle("Interpolation im latenten Raum eines (linearen) Autoencoders: 3 → 8", fontsize=9)
    save(fig, "vl13-latent-interpolation")


# ----------------------------------------------------------------------------
# VL 15
# ----------------------------------------------------------------------------
def vl15_manifolds():
    fig, axs = plt.subplots(1, 4, figsize=(13, 3.2))
    t = np.linspace(0, 2 * np.pi, 60)
    curve = np.c_[t, np.sin(t)]
    axs[0].plot(curve[:, 0], curve[:, 1], color=HHU_ICE, lw=8, alpha=0.7)
    axs[0].scatter(curve[:, 0], curve[:, 1] + rng.normal(0, 0.05, 60), s=10, color="k")
    axs[0].set_title("Manifold-Hypothese: Daten nahe\neiner 1D-Kurve in 2D", fontsize=9)
    axs[1].plot(curve[:, 0], curve[:, 1], color=HHU_ICE, lw=8, alpha=0.7)
    axs[1].scatter(curve[:, 0], curve[:, 1] + rng.normal(0, 0.6, 60), s=10, color="k")
    axs[1].set_title("Problem: Rauschen", fontsize=9)
    c1 = np.c_[t, 0.6 * np.sin(t)]
    c2 = np.c_[np.pi + 0.8 * np.cos(t), 1.5 * np.sin(t) - 0.2]
    axs[2].scatter(c1[:, 0], c1[:, 1], s=10, color="k")
    axs[2].scatter(c2[:, 0], c2[:, 1], s=10, color=HHU_GREEN)
    axs[2].set_title("Problem: Kreuzung – keine Mannigfaltigkeit\n(Polysemie: zwei Bedeutungen treffen sich)", fontsize=9)
    x = np.linspace(-3, 3, 200)
    axs[3].plot(x, 0.3 * np.sin(2 * x), color=HHU_ICE, lw=8, alpha=0.7, label="Datenmannigfaltigkeit")
    axs[3].plot(x, 0.3 * np.sin(2 * x) + 0.25 - 0.2 * np.exp(-((x - 0.8) ** 2) * 6), color=HHU_RED, lw=1.5, label="Entscheidungsgrenze")
    axs[3].scatter([0.8], [0.3 * np.sin(1.6)], color="k", zorder=3)
    axs[3].annotate("adversarial:\nwinziger Schritt\nüber die Grenze", (0.8, 0.3 * np.sin(1.6)), (-2.9, 1.25),
                    fontsize=8, va="top", arrowprops={"arrowstyle": "->"})
    axs[3].set_ylim(-0.75, 1.3)
    axs[3].legend(fontsize=7, loc="lower left")
    axs[3].set_title("Dimpled Manifold Model", fontsize=9)
    for a in axs:
        a.set_xticks([])
        a.set_yticks([])
    save(fig, "vl15-manifolds")


# ----------------------------------------------------------------------------
# Kapitel „Hintergrundwissen Lineare Algebra“ (keine Vorlesung, daher Präfix la_)
# Die Tafelbilder aus der Übung. Keine Zufallszahlen: Die Funktionen laufen alphabetisch
# vor den vl-Funktionen und dürfen deren `rng`-Folge nicht verschieben.
# ----------------------------------------------------------------------------
def _la_ebene(ax, xlim, ylim):
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_aspect("equal")
    ax.axhline(0, color=GREY, lw=0.8)
    ax.axvline(0, color=GREY, lw=0.8)
    for s in ax.spines.values():
        s.set_visible(False)
    ax.set_xticks([])
    ax.set_yticks([])


def _la_pfeil(ax, v, color, label=None, off=(0.08, 0.08), lw=2, alpha=1.0):
    ax.annotate("", xy=(v[0], v[1]), xytext=(0, 0),
                arrowprops={"arrowstyle": "-|>", "color": color, "lw": lw, "alpha": alpha,
                            "shrinkA": 0, "shrinkB": 0, "mutation_scale": 14})
    if label:
        ax.text(v[0] + off[0], v[1] + off[1], label, color=color, fontsize=13, alpha=alpha)


def _la_grad(v):
    return np.degrees(np.arctan2(v[1], v[0]))


def _la_winkel(ax, a, b, r, label=r"$\theta$", grad=None):
    t1, t2 = sorted([_la_grad(a), _la_grad(b)])
    ax.add_patch(Arc((0, 0), 2 * r, 2 * r, theta1=t1, theta2=t2, color=HHU_DARK, lw=1.5))
    m = np.radians((t1 + t2) / 2 if grad is None else grad)
    ax.text(1.25 * r * np.cos(m), 1.25 * r * np.sin(m), label, color=HHU_DARK, fontsize=13,
            ha="center", va="center")


def _la_drehmatrix(phi):
    c, s = np.cos(phi), np.sin(phi)
    return np.array([[c, -s], [s, c]])


def la_drehung():
    v, w = np.array([1.6, 1.9]), np.array([-1.2, 1.5])
    A = _la_drehmatrix(-np.arctan2(v[1], v[0]))
    fig, axs = plt.subplots(1, 2, figsize=(9, 3.8))
    for ax, (a, b), names, title in [(axs[0], (v, w), ("$v$", "$w$"), r"$v \cdot w$"),
                                     (axs[1], (A @ v, A @ w), ("$Av$", "$Aw$"), r"$(Av) \cdot (Aw)$")]:
        _la_ebene(ax, (-2.3, 2.8), (-0.6, 2.8))
        _la_pfeil(ax, a, HHU_BLUE, names[0])
        _la_pfeil(ax, b, HHU_ORANGE, names[1], off=(-0.35, 0.08))
        # rechts liegt die blasse Kopie von v genau auf der Winkelhalbierenden
        _la_winkel(ax, a, b, 0.55, grad=None if ax is axs[0] else 22)
        ax.set_title(title)
    for g in (v, w):
        _la_pfeil(axs[1], g, GREY, alpha=0.3, lw=1.2)
    axs[1].add_patch(Arc((0, 0), 2.6, 2.6, theta1=_la_grad(A @ v) + 3, theta2=_la_grad(v) - 3,
                         color=GREY, lw=1, ls="--"))
    axs[1].text(1.5, 0.75, r"$A$", color=GREY, fontsize=13)
    save(fig, "la-drehung")


def la_einheitskreis():
    th = np.radians(55)
    v = np.array([np.cos(th), np.sin(th)])
    fig, ax = plt.subplots(figsize=(4.6, 4.4))
    _la_ebene(ax, (-1.3, 1.4), (-1.3, 1.4))
    ax.add_patch(Circle((0, 0), 1, fill=False, ec=HHU_ICE, lw=2))
    _la_pfeil(ax, np.array([1, 0]), HHU_DARK, r"$e_1$", off=(0.05, -0.18))
    _la_pfeil(ax, v, HHU_BLUE, r"$v$")
    ax.plot([v[0], v[0]], [0, v[1]], color=GREY, ls="--", lw=1)
    ax.plot([0, v[0]], [-0.06, -0.06], color=HHU_RED, lw=3, solid_capstyle="butt")
    q = 0.07  # rechter Winkel am Lotfußpunkt
    ax.plot([v[0] - q, v[0] - q, v[0]], [0, q, q], color=GREY, lw=0.8)
    ax.text(v[0] / 2, -0.17, "Ankathete", color=HHU_RED, ha="center", va="top", fontsize=10)
    ax.text(v[0] / 2, -0.33, r"$\cos\theta = v \cdot e_1$", color=HHU_RED, ha="center", va="top", fontsize=12)
    ax.text(v[0] + 0.05, v[1] / 2, "Gegenkathete\n" + r"$\sin\theta$", color=GREY, fontsize=10, va="center")
    ax.text(v[0] / 2 - 0.05, v[1] / 2 + 0.04, "Hypotenuse", color=HHU_BLUE, fontsize=10,
            rotation=np.degrees(th), rotation_mode="anchor", ha="center", va="bottom")
    _la_winkel(ax, np.array([1, 0]), v, 0.3)
    save(fig, "la-einheitskreis")


def la_normalisierung():
    v, w = np.array([2.2, 0.9]), np.array([0.5, 1.6])
    fig, ax = plt.subplots(figsize=(5.4, 4))
    _la_ebene(ax, (-1.15, 2.7), (-1.15, 2.0))
    ax.add_patch(Circle((0, 0), 1, fill=False, ec=HHU_ICE, lw=2))
    for x, c, n, off in [(v, HHU_BLUE, "v", (0.06, -0.2)), (w, HHU_ORANGE, "w", (-0.25, 0.0))]:
        _la_pfeil(ax, x, c, rf"${n}$", alpha=0.45, lw=1.5)
        _la_pfeil(ax, x / np.linalg.norm(x), c, rf"$\tilde{{{n}}}$", lw=2.5, off=off)
    _la_winkel(ax, v, w, 0.45)
    save(fig, "la-normalisierung")


def la_projektion():
    w = np.array([1, 0.35])
    wt = w / np.linalg.norm(w)
    fig, axs = plt.subplots(1, 2, figsize=(9, 3.4))
    for ax, v, sign in [(axs[0], np.array([1.3, 1.5]), "> 0"), (axs[1], np.array([-1.1, 1.4]), "< 0")]:
        _la_ebene(ax, (-1.8, 2.3), (-0.8, 1.9))
        t = np.array([-2, 2.5])
        ax.plot(t * wt[0], t * wt[1], color=HHU_ICE, lw=1)
        p = (v @ wt) * wt
        _la_pfeil(ax, wt, HHU_ORANGE, r"$\tilde w$", off=(0.05, 0.12))
        _la_pfeil(ax, v, HHU_BLUE, r"$v$")
        ax.plot([v[0], p[0]], [v[1], p[1]], color=GREY, ls="--", lw=1)
        ax.plot([0, p[0]], [0, p[1]], color=HHU_RED, lw=4, alpha=0.7, solid_capstyle="butt")
        ax.text(0.25, -0.6, rf"$v \cdot \tilde w = \|v\|\cos\theta {sign}$", color=HHU_RED, ha="center")
        _la_winkel(ax, wt, v, 0.6)
    save(fig, "la-projektion")


def la_halbebenen():
    w = np.array([1.0, 0.6])
    fig, ax = plt.subplots(figsize=(4.6, 4.4))
    _la_ebene(ax, (-2, 2), (-2, 2))
    g = np.linspace(-2, 2, 300)
    X, Y = np.meshgrid(g, g)
    ax.contourf(X, Y, w[0] * X + w[1] * Y, levels=[-10, 0, 10], colors=[HHU_ICE, "#E3EEC2"], alpha=0.7)
    n = np.array([-w[1], w[0]]) * 3
    ax.plot([-n[0], n[0]], [-n[1], n[1]], color=HHU_DARK, lw=1.5)
    _la_pfeil(ax, w, HHU_RED, r"$w$")
    ax.text(0.9, -1.4, r"$w \cdot x > 0$", fontsize=12)
    ax.text(-1.8, 1.2, r"$w \cdot x < 0$", fontsize=12)
    ax.text(-1.15, 1.75, r"$w \cdot x = 0$", fontsize=11, color=HHU_DARK)
    for x in [np.array([1.4, -0.6]), np.array([-1.0, -0.6])]:
        _la_pfeil(ax, x, HHU_BLUE, lw=1.3)
    save(fig, "la-halbebenen")


def la_lineare_abbildung():
    mats = [(np.eye(2), "$I$"), (_la_drehmatrix(np.radians(30)), r"Drehung, $A^\top A = I$"),
            (np.array([[1.5, 0.7], [0.2, 0.9]]), r"allgemein, $A^\top A \neq I$")]
    fig, axs = plt.subplots(1, 3, figsize=(11, 3.6))
    for ax, (A, title) in zip(axs, mats):
        _la_ebene(ax, (-1.4, 2.6), (-0.9, 2.1))
        for k in range(-1, 3):
            for a, b in [((k, -1), (k, 2)), ((-1, k), (2, k))]:
                p, q = A @ np.array(a), A @ np.array(b)
                ax.plot([p[0], q[0]], [p[1], q[1]], color=HHU_ICE, lw=0.8)
        sq = A @ np.array([[0, 1, 1, 0], [0, 0, 1, 1]])
        ax.add_patch(Polygon(sq.T, fc=HHU_ICE, alpha=0.5, ec="none"))
        _la_pfeil(ax, A[:, 0], HHU_BLUE, r"$Ae_1$", off=(0.05, -0.25))
        _la_pfeil(ax, A[:, 1], HHU_ORANGE, r"$Ae_2$", off=(-0.45, 0.05))
        c = A[:, 0] @ A[:, 1] / np.linalg.norm(A[:, 0]) / np.linalg.norm(A[:, 1])
        winkel = f"{np.degrees(np.arccos(c)):.0f}"
        flaeche = f"{abs(np.linalg.det(A)):.2f}".replace(".", "{,}")
        ax.set_title(f"{title}\nWinkel ${winkel}^\\circ$, Fläche ${flaeche}$", fontsize=10)
    save(fig, "la-lineare-abbildung")


def la_ebene_r3():
    # Zahlen wie im Kapitel: Die Zeilen von A sind u1 = v/|v|, u2 (Gram-Schmidt aus w)
    # und n = u1 x u2. Dann ist alles ganzzahlig, und Av, Aw liegen in der x-y-Ebene.
    v, w = np.array([1, 2, 2]), np.array([5, 4, -2])
    A = np.array([[1, 2, 2], [2, 1, -2], [-2, 2, -1]]) / 3
    u1, u2, n = A
    assert np.allclose(A.T @ A, np.eye(3)) and np.isclose(n @ v, 0) and np.isclose(n @ w, 0)
    assert np.allclose(A @ v, [3, 0, 0]) and np.allclose(A @ w, [3, 6, 0])
    lim = (-2.6, 6)

    def raum(ax):
        ax.set_xlim(*lim); ax.set_ylim(*lim); ax.set_zlim(*lim)
        ax.set_box_aspect((1, 1, 1))
        ax.view_init(elev=24, azim=-30)
        for d, lab in enumerate("xyz"):
            e = np.zeros(3)
            e[d] = lim[1]
            ax.plot(*np.c_[np.zeros(3), e], color=GREY, lw=0.8)
            ax.text(*(e * 1.05), lab, color=GREY)
        ax.set_axis_off()

    def pfeil(ax, x, color, label, lw=2.2):
        ax.quiver(0, 0, 0, *x, color=color, lw=lw, arrow_length_ratio=0.1)
        ax.text(*(x * 1.08), label, color=color, fontsize=13)

    def flaeche(ax, a, b):
        s, t = np.meshgrid(np.linspace(-0.15, 1.15, 2), np.linspace(-0.15, 1.15, 2))
        P = s[..., None] * a + t[..., None] * b
        ax.plot_surface(P[..., 0], P[..., 1], P[..., 2], color=HHU_BLUE, alpha=0.25, shade=False)

    fig = plt.figure(figsize=(15, 4.6))
    gs = fig.add_gridspec(1, 4, wspace=0.02)
    ax = fig.add_subplot(gs[0], projection="3d")
    raum(ax)
    pfeil(ax, v, HHU_BLUE, "$v$")
    pfeil(ax, w, HHU_ORANGE, "$w$")
    ax = fig.add_subplot(gs[1], projection="3d")
    raum(ax)
    flaeche(ax, 3 * u1, 6 * u2)
    pfeil(ax, v, HHU_BLUE, "$v$")
    pfeil(ax, w, HHU_ORANGE, "$w$")
    pfeil(ax, 2.5 * n, GREY, "$n$", lw=1.4)
    ax = fig.add_subplot(gs[2], projection="3d")
    raum(ax)
    flaeche(ax, np.array([3, 0, 0]), np.array([0, 6, 0]))
    pfeil(ax, A @ v, HHU_BLUE, "$Av$")
    pfeil(ax, A @ w, HHU_ORANGE, "$Aw$")
    pfeil(ax, 2.5 * (A @ n), GREY, "$An = e_3$", lw=1.4)

    ax = fig.add_subplot(gs[3])
    ax.set_xlim(-0.8, 4.8); ax.set_ylim(-0.8, 6.8); ax.set_aspect("equal")
    for s in ax.spines.values():
        s.set_visible(False)
    ax.set_xticks(range(5)); ax.set_yticks(range(7)); ax.grid(color=HHU_ICE, lw=0.6)
    ax.tick_params(length=0, labelsize=8, labelcolor=GREY)
    for x, c, lab, off in [((3, 0), HHU_BLUE, "$Av$", (0.1, -0.5)), ((3, 6), HHU_ORANGE, "$Aw$", (0.1, 0.1))]:
        _la_pfeil(ax, x, c)
        ax.text(x[0] + off[0], x[1] + off[1], lab, color=c, fontsize=13)
    ax.add_patch(Arc((0, 0), 1.6, 1.6, theta1=0, theta2=np.degrees(np.arctan2(6, 3)), color=HHU_DARK, lw=1.5))
    ax.text(0.95, 0.55, r"$\theta$", color=HHU_DARK, fontsize=13)
    # Gemeinsame Titelzeile: 3D-Achsen setzen ihre Titel tiefer als 2D-Achsen.
    for i, t in enumerate(["zwei Vektoren in allgemeiner Lage", "die Ebene, die sie aufspannen",
                           r"nach $A$: die Ebene $z = 0$", "in der Ebene gezeichnet"]):
        pos = fig.axes[i].get_position()
        fig.text((pos.x0 + pos.x1) / 2, 0.95, t, ha="center", fontsize=11)
    save(fig, "la-ebene-r3")


# ----------------------------------------------------------------------------
def copy_existing():
    import shutil

    for src, dst in [
        ("tafelbild-gradientenabstieg-weiss.jpg", "vl05-tafelbild-gradientenabstieg.jpg"),
        ("krude-xor-approximation.png", "vl07-xor-playground-3hidden.png"),
        ("krude-xor-approximation-2.png", "vl07-xor-playground-2hidden.png"),
        ("bolukbasi16-man-is-to-computer-programmer-figure7.png", "vl13-bolukbasi-fig7.png"),
        ("arvanitidis2021-latent-space-oddity-figure1.png", "vl13-arvanitidis-fig1.png"),
        ("convolutions.png", "vl10-convolutions-notebook.png"),
    ]:
        shutil.copy(SRC / src, OUT / dst)
        print("copied", dst)


if __name__ == "__main__":
    # Eine fehlende Fremddatei darf nicht die Abbildungen danach verschlucken: Der Lauf
    # macht weiter, nennt am Ende, was fehlte, und endet trotzdem mit einem Fehlercode.
    fehlt: list[str] = []
    for fn in [v for k, v in sorted(globals().items()) if k.startswith(("la_", "vl")) and callable(v)]:
        try:
            fn()
        except FileNotFoundError as e:
            fehlt.append(f"{fn.__name__}: {e.filename}")
            print(f"ÜBERSPRUNGEN {fn.__name__}: {e.filename} fehlt")
    try:
        copy_existing()
    except FileNotFoundError as e:
        fehlt.append(f"copy_existing: {e.filename}")
        print(f"ÜBERSPRUNGEN copy_existing: {e.filename} fehlt")

    if KOLLISIONEN:
        print(f"\n{len(KOLLISIONEN)} Kollision(en) in den Abbildungen -- erst beheben, dann einchecken:")
        for k in KOLLISIONEN:
            print(f"  - {k}")
    if fehlt:
        print(f"\n{len(fehlt)} Schritt(e) ohne Material, gesucht in:")
        for kandidat in SRC_KANDIDATEN:
            print(f"  {kandidat}{'' if kandidat.is_dir() else '   (nicht da)'}")
        for z in fehlt:
            print(f"  - {z}")
    if fehlt or KOLLISIONEN:
        raise SystemExit(1)
