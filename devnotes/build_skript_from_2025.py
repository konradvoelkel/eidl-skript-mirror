"""One-off migration script: seeds eidl-26/eidl-skript from the 2025 material.

- transcribes the 2025 lecture PDFs (pdftotext) into one MyST chapter per lecture,
  slide by slide, in order
- converts the 2025 German exercise sheets (LaTeX) to MyST markdown via pandoc
- copies the lecture notebooks
"""

import glob
import re
import shutil
import subprocess
from pathlib import Path

ROOT = Path("/home/voelkel/sciebo/hhu/eidl-26")
SRC = ROOT / "from_2025"
DST = ROOT / "eidl-skript"

# --------------------------------------------------------------------------
# Lecture -> chapter mapping (part directory, slug, chapter title)
# --------------------------------------------------------------------------
LECTURES = [
    ("part-grundlagen", "01-ueberblick-perzeptron", "Überblick und Perzeptron"),
    ("part-grundlagen", "02-perzeptron-vortrainierte-modelle", "Perzeptron in der Praxis, vortrainierte Modelle"),
    ("part-grundlagen", "03-pytorch-tensoren", "PyTorch Basics und Tensoren"),
    ("part-lernen", "04-logistische-regression", "Logistische Regression"),
    ("part-lernen", "05-sgd", "Stochastischer Gradientenabstieg"),
    ("part-lernen", "06-backprop", "Backpropagation"),
    ("part-representation-learning", "07-autoencoder", "Handgemachte Netze und Autoencoder"),
    ("part-representation-learning", "08-latent-space-vae", "Latent Space, VAE und word2vec"),
    ("part-representation-learning", "09-representation-learning", "Representation Learning, RNNs und Transformer"),
    ("part-architekturen-anwendungen", "10-cnn", "Convolutional Neural Networks"),
    ("part-architekturen-anwendungen", "11-llms-benutzen", "LLMs benutzen"),
    ("part-architekturen-anwendungen", "12-gans", "Generative Adversarial Networks"),
    ("part-architekturen-anwendungen", "13-latent-spaces-anwendungen", "Latent Spaces und Anwendungen"),
    ("part-architekturen-anwendungen", "14-destillation", "Destillation"),
    ("part-architekturen-anwendungen", "15-maerchenstunde", "Märchenstunde: Optimierer, Adversarial Attacks, Polysemie"),
]

FOOTER_RE = re.compile(
    r"^(\d{1,3}|hhu\.de|Einführung in Deep Learning, Wintersemester 2025/26, konrad\.voelkel@hhu\.de|"
    r"Bachelor Informatik, WiSe 2025/26|Dr\. Konrad Völkel)$"
)


def clean_page(page: str) -> list[str]:
    lines = [l.rstrip() for l in page.splitlines()]
    lines = [l for l in lines if l.strip() and not FOOTER_RE.match(l.strip())]
    return lines


def transcribe_lecture(pdf: Path, number: int, title: str) -> str:
    txt = subprocess.run(["pdftotext", str(pdf), "-"], capture_output=True, text=True, check=True).stdout
    pages = txt.split("\f")
    out = [
        "---",
        f"title: \"VL {number:02d}: {title}\"",
        f"short_title: \"VL {number:02d}\"",
        "---",
        "",
        f"# {title}",
        "",
        ":::{warning} Rohfassung",
        f"Dieses Kapitel ist eine automatische Transkription der Folien von VL {number:02d} aus dem WiSe 2025/26",
        f"(`from_2025/slides/{pdf.name}`), Folie für Folie in der Originalreihenfolge.",
        "Formeln und Abbildungen sind dabei größtenteils verloren gegangen; der Text ist noch nicht überarbeitet.",
        ":::",
        "",
    ]
    prev_title = None
    for i, page in enumerate(pages, start=1):
        lines = clean_page(page)
        if not lines:
            continue
        if i == 1:  # title slide
            continue
        slide_title = lines[0].strip()
        body = lines[1:]
        if slide_title.startswith("Danke für Ihre"):
            continue
        if slide_title != prev_title:
            out.append(f"## {slide_title}")
            out.append("")
            prev_title = slide_title
        out.append(f"<!-- Folie {i} -->")
        for l in body:
            out.append(l.strip())
        out.append("")
    return "\n".join(out).rstrip() + "\n"


# --------------------------------------------------------------------------
# Exercises: LaTeX -> MyST via pandoc
# --------------------------------------------------------------------------
MACROS = r"""
\newcommand{\pvec}[2]{\begin{pmatrix} #1 \\ #2 \end{pmatrix}}
\newcommand{\tvec}[3]{\begin{pmatrix} #1 \\ #2 \\ #3 \end{pmatrix}}
\newcommand{\alttext}[2]{#1}
\newcommand{\thesolution}[1]{\begin{solutions}#1\end{solutions}}
\DeclareMathOperator{\Mat}{Mat}
\DeclareMathOperator{\sign}{sign}
"""


def convert_sheet(tex: Path, number: int) -> str:
    src = tex.read_text(encoding="utf-8")
    meta = {}
    for key in ("Blatt", "Abgabetag", "Punktegesamt"):
        m = re.search(r"\\newcommand\{\\" + key + r"\}\{([^}]*)\}", src)
        if m:
            meta[key] = m.group(1)
    body = src.split(r"\begin{document}", 1)[1].split(r"\end{document}", 1)[0]
    md = subprocess.run(
        ["pandoc", "-f", "latex", "-t", "markdown+tex_math_dollars", "--wrap=none", "--markdown-headings=atx"],
        input=MACROS + body,
        capture_output=True,
        text=True,
        check=True,
    ).stdout

    # post-processing
    md = re.sub(r"\s*\{#[^}]*\.unnumbered\}", "", md)
    md = re.sub(r"^# ", "## ", md, flags=re.M)
    task_no = [0]

    def repl_task(m):
        task_no[0] += 1
        return f"### Aufgabe {task_no[0]}\n"

    md = re.sub(r"^::: aufgabe\n", repl_task, md, flags=re.M)
    # closing ":::" that belong to aufgabe blocks: remove the ones not opened by another div
    # simple approach: drop every ":::" line that is not preceded by an open solutions/other div
    lines = md.splitlines()
    out, stack = [], []
    for l in lines:
        if re.match(r"^:{3,} (\S+)", l):
            name = re.match(r"^:{3,} (\S+)", l).group(1)
            stack.append(name)
            if name == "solutions":
                out.append(":::{admonition} Lösungsvorschlag\n:class: dropdown")
            elif name == "hidefromsolutions":
                pass
            else:
                titles = {"bemerkung": "Bemerkung", "definition": "Definition", "beispiel": "Beispiel", "satz": "Satz"}
                out.append(f":::{{admonition}} {titles.get(name, name)}")
            continue
        if re.match(r"^:{3,}\s*$", l):
            name = stack.pop() if stack else None
            if name in ("solutions",) or (name not in (None, "hidefromsolutions", "aufgabe")):
                out.append(":::")
            continue
        out.append(l)
    md = "\n".join(out)
    md = re.sub(r"\n{3,}", "\n\n", md)

    abgabe = ""
    if "Abgabetag" in meta:
        abgabe = f"\n{meta.get('Punktegesamt', '?')} Punkte, Abgabe bis 12:00 am Mittwoch, dem {meta['Abgabetag']} (Termin aus 2025, noch anzupassen).\n"
    else:
        abgabe = "\nOhne Abgabe.\n"
    head = (
        "---\n"
        f"title: \"Blatt {number}\"\n"
        "---\n\n"
        f"# Übungsblatt {number}\n"
        f"{abgabe}\n"
        ":::{note}\n"
        f"Übernommen aus dem WiSe 2025/26 (`from_2025/exercises/{tex.name}`), noch nicht an die neue Vorlesung angepasst.\n"
        ":::\n\n"
    )
    return head + md.strip() + "\n"


# --------------------------------------------------------------------------
def main():
    # chapters
    pdfs = {}
    for p in (SRC / "slides").glob("Einführung in Deep Learning 2025_26 VL *.pdf"):
        if "Extra" in p.name:
            continue
        n = int(re.search(r"VL (\d+)_", p.name).group(1))
        pdfs[n] = p
    for n, (part, slug, title) in enumerate(LECTURES, start=1):
        d = DST / part
        d.mkdir(parents=True, exist_ok=True)
        (d / f"{slug}.md").write_text(transcribe_lecture(pdfs[n], n, title), encoding="utf-8")
        print("wrote", part, slug)

    # exercises
    ex = DST / "part-exercises"
    ex.mkdir(exist_ok=True)
    for tex in sorted((SRC / "exercises").glob("blatt[0-9][0-9].tex")):
        n = int(tex.stem[5:])
        (ex / f"eidl2026blatt{n:02d}.md").write_text(convert_sheet(tex, n), encoding="utf-8")
        print("wrote exercise", n)

    # notebooks used in lectures
    nb = DST / "notebooks"
    nb.mkdir(exist_ok=True)
    for name in ["nn-by-hand.ipynb", "VL_10_convolutions.ipynb", "VL_11_backprop.ipynb",
                 "VL_11_llamacpp.ipynb", "latent-classifier.ipynb"]:
        shutil.copy(SRC / "slides" / name, nb / name)
    print("copied notebooks")


if __name__ == "__main__":
    main()
