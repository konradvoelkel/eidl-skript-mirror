#!/usr/bin/env python3
"""Zu jeder im Buch verlinkten Abbildung eine WebP-Fassung neben die Quelle legen.

    uv run --only-group figures devnotes/make_webp.py          # fehlende/veraltete bauen
    uv run --only-group figures devnotes/make_webp.py --force  # alle neu
    uv run --no-project devnotes/make_webp.py --check          # nur prüfen (ohne Pillow)

Warum (2026-11-17, SEO-Audit §8)
--------------------------------
`/faltung-cnn/` lieferte 2,3 MB PNG aus, das Buch insgesamt 7,6 MB in 61 verlinkten
Dateien. Als WebP sind daraus 2,4 MB – **68 % weniger**, ohne an einer Abbildung etwas zu
ändern. Das PNG bleibt liegen: Der PDF-Bau braucht es (xelatex kennt kein WebP), und die
Vorschaukarte muss PNG bleiben, weil die sozialen Netze nichts anderes lesen.

**Verlustfrei oder q90 – je Bild das Kleinere**, und das ist gemessen, nicht geraten. Bei
den Matplotlib-Abbildungen mit großen einfarbigen Flächen gewinnt oft die verlustfreie
Fassung (`vl08-cbow-skipgram` 70 K auf 25 K), bei den Fotos und Screenshots die
verlustbehaftete (`vl10-faltungsmatrix` 823 K auf 185 K, verlustfrei wären es 368 K). Die
Qualitätsstufe ist **90 und nicht 82**, obwohl 82 noch einmal ein Drittel spart: In diesem
Buch steht in fast jeder Abbildung Text, und eine Abbildung mit unscharfem Text ist in
`CLAUDE.md` als Fehlerquelle verzeichnet. Bei 90 ist am Text im Vergleich bei 1:1 nichts
zu sehen.

**Deterministisch wie `make_figures.py`**: Die Pillow-Fassung ist in der Gruppe `figures`
angeheftet. Eine andere Fassung kodiert anders, und dann ändern sich alle Dateien auf
einmal, ohne dass sich an einer einzigen etwas Inhaltliches geändert hätte. Dieselbe
Lehre, dieselbe Vorsichtsmaßnahme.

Ausgeliefert wird die WebP-Fassung von `tools/webp.py` im `pages`-Job, das im Artefakt
die Verweise umschreibt – im Markup, im Stylesheet `bildmasse` und in der
Hydrations-Nutzlast.
"""

from __future__ import annotations

import argparse
import io
import pathlib
import re
import sys

WURZEL = pathlib.Path(__file__).resolve().parent.parent
BILDER = WURZEL / "images"
QUELLEN = ("*.png", "*.jpg", "*.jpeg")
VERWEIS = re.compile(r"(?:\.\./)?images/([\w.-]+\.(?:png|jpg|jpeg))", re.I)


# Das Logo der Kopfzeile steht nicht in `images/` und wird aus `myst.yml` geladen, kommt
# aber auf *jeder* Seite vor -- deshalb hier von Hand dazu. Die Vorschaukarte bleibt PNG:
# die sozialen Netze und Googles Vorschau lesen kein WebP.
EXTRA = (WURZEL / "site_logo.png",)


def verlinkte() -> set[str]:
    """Dateinamen, die aus dem Buch heraus verlinkt sind.

    Die Foliensätze und die Vorschaukarte zählen nicht: Sie brauchen PNG bzw. JPG.
    """
    namen: set[str] = set()
    for pfad in list(WURZEL.glob("part-*/*.md")) + [
        WURZEL / "index.md", WURZEL / "glossar.md", WURZEL / "ueber-dieses-skript.md",
        WURZEL / "uebungsblaetter.md", WURZEL / "kurs-2026-27.md",
    ]:
        if pfad.exists():
            namen |= set(VERWEIS.findall(pfad.read_text(encoding="utf-8")))
    return namen


def alle_quellen(namen: set[str]) -> list[pathlib.Path]:
    return sorted([p for muster in QUELLEN for p in BILDER.glob(muster) if p.name in namen]
                  + [p for p in EXTRA if p.exists()])


def ziel(quelle: pathlib.Path) -> pathlib.Path:
    return quelle.with_suffix(".webp")


def veraltet(quelle: pathlib.Path) -> bool:
    z = ziel(quelle)
    return not z.exists() or z.stat().st_mtime < quelle.stat().st_mtime


def bauen(quelle: pathlib.Path) -> tuple[int, int, str]:
    from PIL import Image

    with Image.open(quelle) as im:
        im.load()
        if im.mode not in ("RGB", "RGBA"):
            im = im.convert("RGBA" if "transparency" in im.info or im.mode in ("LA", "PA") else "RGB")
        fassungen = {}
        for name, kw in (("verlustfrei", dict(lossless=True, method=6)),
                         ("q90", dict(quality=90, method=6))):
            puffer = io.BytesIO()
            im.save(puffer, "WEBP", **kw)
            fassungen[name] = puffer.getvalue()
    wahl = min(fassungen, key=lambda k: len(fassungen[k]))
    ziel(quelle).write_bytes(fassungen[wahl])
    return quelle.stat().st_size, len(fassungen[wahl]), wahl


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--force", action="store_true", help="auch bauen, was aktuell ist")
    ap.add_argument("--check", action="store_true",
                    help="nur prüfen, ob zu jedem verlinkten Bild eine aktuelle WebP-Fassung liegt")
    args = ap.parse_args()

    namen = verlinkte()
    quellen = alle_quellen(namen)
    if not quellen:
        print("✗ keine verlinkten Bilder gefunden -- stimmt der Pfad?")
        return 1

    if args.check:
        fehlt = [p.name for p in quellen if veraltet(p)]
        # Eine WebP-Datei ohne Quelle ist ein Rest einer umbenannten Abbildung.
        verwaist = [w.name for w in BILDER.glob("*.webp")
                    if not any(ziel(p) == w for p in quellen)]
        for n in fehlt:
            print(f"✗ {n}: WebP fehlt oder ist älter als die Quelle")
        for n in verwaist:
            print(f"✗ {n}: WebP ohne verlinkte Quelle")
        if fehlt or verwaist:
            print("  bauen mit: uv run --only-group figures devnotes/make_webp.py")
            return 1
        print(f"✓ {len(quellen)} verlinkte Abbildungen, jede mit aktueller WebP-Fassung")
        return 0

    vorher = nachher = 0
    gebaut = 0
    for p in quellen:
        if not args.force and not veraltet(p):
            vorher += p.stat().st_size
            nachher += ziel(p).stat().st_size
            continue
        alt, neu, wahl = bauen(p)
        vorher += alt
        nachher += neu
        gebaut += 1
        print(f"  {p.name:44s} {alt / 1024:7.0f}K -> {neu / 1024:7.0f}K  {wahl}")
    print(f"✓ {gebaut} neu gebaut, {len(quellen)} verlinkte Abbildungen: "
          f"{vorher / 1024 / 1024:.2f} MB -> {nachher / 1024 / 1024:.2f} MB "
          f"({(1 - nachher / vorher) * 100:.0f} % weniger)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
