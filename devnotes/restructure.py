#!/usr/bin/env python3
"""Einmaliges Umbau-Skript (2026-09-17): baut aus den 15 VL-Kapiteln 20 inhaltlich
geschnittene Kapitel. Quellen: die alten Dateien im Git-Stand vor dem Umbau.
Abschnitte werden anhand ihrer Überschriften ausgewählt; Abbildungen (TODO-Marker)
werden durch figure-Direktiven ersetzt.
"""

import re
import subprocess
import sys
from pathlib import Path

# ──────────────────────────────────────────────────────────────────────────────
# NICHT MEHR LAUFEN LASSEN (Sperre eingebaut 2026-09-27).
#
# Dieses Skript hat am 2026-09-17 aus den 15 Vorlesungs-Kapiteln 20 Themen-Kapitel
# geschnitten. Anders als `build_skript_from_2025.py` zeigt es auf **dieses** Repo
# (`ROOT = parent.parent`) und liest seine Quellen aus einem alten git-Stand — ein Lauf
# würde also die heutigen 27 Kapitel mit einer neu erzeugten 20-Kapitel-Fassung
# überschreiben und alle Überarbeitungen seit dem 17.09. verwerfen.
#
# Es bleibt im Repo als Protokoll des Umbaus. Wer es wirklich braucht, entfernt diesen
# Block bewusst und weiß, was er tut.
# ──────────────────────────────────────────────────────────────────────────────
print(
    "restructure.py ist gesperrt (2026-09-27): Ein Lauf überschriebe die heutigen 27 Kapitel\n"
    "mit einer neu erzeugten 20-Kapitel-Fassung aus einem alten git-Stand. Begründung im\n"
    "Kopf der Datei.",
    file=sys.stderr,
)
raise SystemExit(1)

ROOT = Path(__file__).resolve().parent.parent
OLD_REV = "HEAD"  # Stand vor dem Umbau

OLD = {
    1: "part-grundlagen/01-ueberblick-perzeptron.md",
    2: "part-grundlagen/02-perzeptron-vortrainierte-modelle.md",
    3: "part-grundlagen/03-pytorch-tensoren.md",
    4: "part-lernen/04-logistische-regression.md",
    5: "part-lernen/05-sgd.md",
    6: "part-lernen/06-backprop.md",
    7: "part-representation-learning/07-autoencoder.md",
    8: "part-representation-learning/08-latent-space-vae.md",
    9: "part-representation-learning/09-representation-learning.md",
    10: "part-architekturen-anwendungen/10-cnn.md",
    11: "part-architekturen-anwendungen/11-llms-benutzen.md",
    12: "part-architekturen-anwendungen/12-gans.md",
    13: "part-architekturen-anwendungen/13-latent-spaces-anwendungen.md",
    14: "part-architekturen-anwendungen/14-destillation.md",
    15: "part-architekturen-anwendungen/15-maerchenstunde.md",
}

HEAD_RE = re.compile(r"^(#{2,3}) (.*)$")


def parse(text):
    """-> list of nodes {level, title, body(lines)}; level 0 = Präambel nach der Stand-Box."""
    lines = text.splitlines()
    nodes = []
    # Präambel: alles nach der ersten ':::'-Box bis zur ersten Überschrift
    i = 0
    # skip frontmatter + H1 + note box
    depth = 0
    seen_box = False
    while i < len(lines):
        l = lines[i]
        if l.startswith(":::"):
            depth = 1 - depth
            seen_box = True
            i += 1
            continue
        if seen_box and depth == 0 and not l.startswith("#"):
            break
        if HEAD_RE.match(l) and seen_box and depth == 0:
            break
        i += 1
    cur = {"level": 0, "title": "PREAMBLE", "body": []}
    nodes.append(cur)
    for l in lines[i:]:
        m = HEAD_RE.match(l)
        if m:
            cur = {"level": len(m.group(1)), "title": m.group(2).strip(), "body": []}
            nodes.append(cur)
        else:
            cur["body"].append(l)
    return nodes


def load_old():
    out = {}
    for n, p in OLD.items():
        txt = subprocess.run(["git", "show", f"{OLD_REV}:{p}"], capture_output=True, text=True, check=True, cwd=ROOT).stdout
        out[n] = parse(txt)
    return out


SRC = load_old()


def sec(vl, title, level=None, nth=0, with_children=True):
    """Abschnitt `title` aus VL `vl` als Markdown, optional auf neue Überschriftenebene."""
    nodes = SRC[vl]
    hits = [i for i, nd in enumerate(nodes) if nd["title"] == title]
    if not hits:
        raise KeyError(f"VL{vl}: {title!r} nicht gefunden")
    i = hits[nth]
    nd = nodes[i]
    lvl = nd["level"]
    new_lvl = level or lvl
    shift = new_lvl - lvl
    out = []
    if nd["level"] > 0:
        out.append("#" * new_lvl + " " + nd["title"])
    out.extend(nd["body"])
    if with_children and lvl > 0:
        for nd2 in nodes[i + 1:]:
            if nd2["level"] <= lvl:
                break
            out.append("#" * (nd2["level"] + shift) + " " + nd2["title"])
            out.extend(nd2["body"])
    return "\n".join(out).strip("\n") + "\n"


def chapter(path, title, short, parts, intro=None):
    head = f'---\ntitle: "{title}"\nshort_title: "{short}"\n---\n\n# {title}\n\n'
    body = "\n".join(p.strip("\n") + "\n" for p in parts if p.strip())
    if intro:
        body = intro.strip("\n") + "\n\n" + body
    text = head + body
    text = re.sub(r"\n{3,}", "\n\n", text)
    (ROOT / path).write_text(text, encoding="utf-8")
    print("wrote", path)


# ----------------------------------------------------------------------------
CH = []  # (path, title) in Reihenfolge, für myst.yml

def add(path, title, short, parts, intro=None):
    chapter(path, title, short, parts, intro)
    CH.append((path, title))


# Teil I: Grundlagen ---------------------------------------------------------
add("part-grundlagen/01-was-ist-deep-learning.md", "Was ist Deep Learning?", "Was ist Deep Learning?", [
    sec(1, "Was ist eigentlich Deep Learning?"),
    sec(1, "Wieso Python eine Katastrophe ist"),
    sec(1, "Wieso Python ganz toll ist"),
    sec(1, "Erinnerung: Begriffe aus dem maschinellen Lernen"),
    sec(1, "Kurzgeschichte"),
])

add("part-grundlagen/02-perzeptron.md", "Das Perzeptron", "Perzeptron", [
    sec(1, "Das Neuron und das Perzeptron"),
    sec(1, "Was ist ein neuronales Netz?"),
    "## Das Perzeptron trainieren\n" + sec(2, "Wie war das mit dem Perzeptron?").split("\n", 1)[1],
    sec(2, "Zurück in die Theorie: Wozu das olle Perzeptron?"),
    sec(2, "Mehrere Schichten"),
    "## Tipps zu den Übungsblättern\n",
    sec(1, "Tipps zum Übungsblatt", level=3).replace("### Tipps zum Übungsblatt", "### Blatt 1: Lineare Algebra und NumPy"),
    sec(2, "Tipps zum Übungsblatt", level=3).replace("### Tipps zum Übungsblatt", "### Blatt 2: Perzeptron in NumPy"),
])

add("part-grundlagen/03-vortrainierte-modelle.md", "Vortrainierte Modelle verwenden", "Vortrainierte Modelle", [
    sec(2, "Vortrainierte Modelle verwenden: Orientierung").replace("## Vortrainierte Modelle verwenden: Orientierung", "## Orientierung"),
    sec(3, "Vortrainierte Modelle verwenden: Orientierung").replace("## Vortrainierte Modelle verwenden: Orientierung", "## Ein Rundgang durch die Tasks"),
    sec(3, "Vortrainierte Modelle verwenden: Praktisch").replace("## Vortrainierte Modelle verwenden: Praktisch", "## Praktisch"),
])

add("part-grundlagen/04-tensoren.md", "Tensoren", "Tensoren", [
    sec(3, "PyTorch Basics: Tensoren").replace("## PyTorch Basics: Tensoren", "## Tensoren in PyTorch"),
])

# Teil II: Lernen ------------------------------------------------------------
add("part-lernen/05-logistische-regression.md", "Logistische Regression", "Logistische Regression", [
    sec(3, "Lineare Regression zur Klassifikation"),
    sec(4, "Wahrscheinlichkeiten und Chancen (Odds)"),
    sec(4, "Logistische Sigmoidfunktion"),
    sec(4, "Sigmoid und Logit"),
    sec(4, "Logistische Regression"),
    sec(4, "Weg von der 2-Klassen-Gesellschaft: Softmax"),
    sec(4, "Tipps zum Übungsblatt").replace("## Tipps zum Übungsblatt", "## Tipps zu den Übungsblättern 4 und 5"),
], intro=SRC[4][0]["body"] and "\n".join(SRC[4][0]["body"]).replace("Am Ende des letzten Kapitels hatten wir", "Im ersten Abschnitt basteln wir").replace("aber keine Interpretation dafür. In diesem Kapitel", "aber haben keine Interpretation dafür. Danach"))

add("part-lernen/06-gradientenabstieg.md", "Gradientenabstieg", "Gradientenabstieg", [
    sec(5, "Training eines einzelnen Neurons: Was bisher geschah"),
    sec(5, "Optimieren mit Fehlerterm"),
    sec(4, "Kurze Erinnerung an die Kettenregel"),
    sec(5, "Gradienten"),
    sec(5, "Gradientenabstieg").replace("## Gradientenabstieg", "## Der Algorithmus"),
    sec(5, "Zurück zum Perzeptron"),
    sec(5, "Take-Home Message"),
    sec(5, "Nicht-stochastischer Gradientenabstieg??"),
    "## Tipps zu den Übungsblättern\n",
    sec(3, "Tipps zum Übungsblatt", level=3).replace("### Tipps zum Übungsblatt", "### Blatt 3: Schwache Ableitungen"),
    sec(5, "Tipps zum Übungsblatt", level=3).replace("### Tipps zum Übungsblatt", "### Blatt 5: Sigmoid, Softmax, Kreuzentropie"),
])

add("part-lernen/07-backpropagation.md", "Backpropagation", "Backpropagation", [
    sec(6, "Ziel für heute").replace("## Ziel für heute", "## Ziel"),
    sec(6, "Training mehrerer Schichten: Motivation"),
    sec(6, "Backpropagation konkret"),
    sec(13, "Und noch einmal zur Backpropagation").replace("## Und noch einmal zur Backpropagation", "## Backpropagation als Induktion"),
    sec(11, "Recap & Vertiefung: Backpropagation im Notebook").replace("## Recap & Vertiefung: Backpropagation im Notebook", "## Backpropagation in PyTorch: der Berechnungsgraph"),
])

add("part-lernen/08-aktivierungsfunktionen-universalitaet.md", "Aktivierungsfunktionen und Universalität", "Aktivierungsfunktionen", [
    sec(6, "Aktivierungsfunktionen und weitere Layer"),
    sec(7, "Das Geheimnis um Deep Learning lüften"),
    sec(7, "Parameter von Hand wählen"),
    sec(11, "Recap & Vertiefung: Universalität").replace("## Recap & Vertiefung: Universalität", "## Universelle Approximation"),
])

# Teil III: Representation Learning ------------------------------------------
add("part-representation-learning/09-autoencoder.md", "Autoencoder", "Autoencoder", [
    sec(6, "Autoencoder").replace("## Autoencoder", "## Lernen ohne Label"),
    sec(7, "Autoencoder").replace("## Autoencoder", "## Autoencoder für MNIST"),
    sec(7, "Label Autoencoder"),
    sec(8, "Autoencoder-Varianten"),
    sec(6, "Tipps zum Übungsblatt").replace("## Tipps zum Übungsblatt", "## Tipps zu Übungsblatt 6"),
])

add("part-representation-learning/10-variational-autoencoder.md", "Variational Autoencoder und latente Räume", "VAE", [
    sec(8, "Variational Autoencoder").replace("## Variational Autoencoder\n", "## Vom Autoencoder zum VAE\n"),
    sec(13, "Latent Spaces von Autoencodern, VAEs und GANs für Bilder").replace("## Latent Spaces von Autoencodern, VAEs und GANs für Bilder", "## Latente Räume für Bilder: AE, VAE, GAN"),
])

add("part-representation-learning/11-word2vec.md", "Wortvektoren: word2vec", "word2vec", [
    sec(8, "word2vec"),
    sec(8, "NLP").replace("## NLP", "## Von Wörtern zu Dokumenten: NLP"),
    sec(13, "Latent Spaces von LLMs: Wort-Vektor-Einbettungen geometrisch verstehen").replace("## Latent Spaces von LLMs: Wort-Vektor-Einbettungen geometrisch verstehen", "## Wortvektoren geometrisch verstehen"),
])

add("part-representation-learning/12-representation-learning-graphen.md", "Representation Learning und Graphen", "Representation Learning", [
    sec(9, "Representation Learning"),
    sec(9, "node2vec"),
])

add("part-representation-learning/13-sequenzen-rnn-transformer.md", "Sequenzen: RNNs und Transformer", "RNNs und Transformer", [
    sec(9, "Recurrent Neural Networks"),
    sec(9, "Transformer"),
])

# Teil IV: Architekturen und Anwendungen -------------------------------------
add("part-architekturen-anwendungen/14-faltung-cnn.md", "Faltung und Convolutional Neural Networks", "CNNs", [
    sec(10, "Motivation zur Faltung"),
    sec(10, "Eindimensionale Faltung"),
    sec(10, "Eindimensionales Pooling"),
    sec(10, "Zweidimensionale Faltung"),
    sec(10, "CNNs"),
])

add("part-architekturen-anwendungen/15-llms-benutzen.md", "LLMs benutzen", "LLMs benutzen", [
    sec(11, "Transformer-LLMs in der Praxis einsetzen"),
    sec(11, "Selbst Inferenz und Training durchführen"),
    sec(11, "Wie geht eigentlich … eine Anwendung?"),
    sec(11, "Tipps zum Übungsblatt").replace("## Tipps zum Übungsblatt", "## Tipps zu Übungsblatt 11"),
])

add("part-architekturen-anwendungen/16-gans.md", "Generative Adversarial Networks", "GANs", [
    sec(12, "Historie"),
    sec(12, "GANs technisch"),
    sec(12, "Varianten von GANs"),
    sec(12, "Konkrete Modelle"),
    sec(12, "Selbst GANs basteln"),
])

add("part-architekturen-anwendungen/17-anwendungsbeispiele.md", "Anwendungsbeispiele", "Anwendungsbeispiele", [
    sec(13, "Anwendungsbeispiele").replace("## Anwendungsbeispiele", "## Drei Beispiele aus der Praxis"),
    sec(14, "Vibecoding Deep Learning"),
], intro="Drei Beispiele, wie sich die Bausteine aus den vorigen Kapiteln zu Anwendungen zusammensetzen – und ein Blick darauf, wie man mit generiertem Code arbeitet.")

add("part-architekturen-anwendungen/18-destillation.md", "Destillation", "Destillation", [
    sec(14, "Was lernen wir beim Deep Learning eigentlich?"),
    sec(14, "Model Compression"),
    sec(14, "Model Distillation"),
    sec(14, "Anwendungen"),
])

add("part-architekturen-anwendungen/19-optimierer.md", "Optimierer: Momentum, Adam, Muon", "Optimierer", [
    sec(15, "Ein Märchen über Optimierung: Adam oder was?").replace("## Ein Märchen über Optimierung: Adam oder was?", "## Adam oder was?"),
])

add("part-architekturen-anwendungen/20-adversarial-attacks-polysemie.md", "Adversarial Attacks und Polysemie", "Adversarial Attacks", [
    sec(15, "Ein Märchen über Adversarial Attacks").replace("## Ein Märchen über Adversarial Attacks", "## Adversarial Attacks"),
    sec(15, "Ein Märchen über Polysemie").replace("## Ein Märchen über Polysemie", "## Polysemie und die Manifold-Hypothese"),
], intro="Zwei Themen zum Abschluss, die über die Vorlesung hinausgehen, aber mit dem Gelernten schon verständlich sind.")

# ----------------------------------------------------------------------------
# alte Dateien entfernen, TOC schreiben
for p in OLD.values():
    f = ROOT / p
    if f.exists() and p not in [c[0] for c in CH]:
        f.unlink()
        print("removed", p)

toc = ""
for part, title in [("part-grundlagen", "Grundlagen"), ("part-lernen", "Lernen"),
                    ("part-representation-learning", "Representation Learning"),
                    ("part-architekturen-anwendungen", "Architekturen und Anwendungen")]:
    toc += f"    - title: {title}\n      children:\n"
    for path, _ in CH:
        if path.startswith(part + "/"):
            toc += f"       - file: {path}\n"
myst = (ROOT / "myst.yml").read_text(encoding="utf-8")
myst = re.sub(r"    - title: Grundlagen\n.*?(?=    - title: Notebooks)", toc, myst, flags=re.S)
(ROOT / "myst.yml").write_text(myst, encoding="utf-8")
print("myst.yml updated")
