#!/usr/bin/env python3
"""Die Abbildungen als WebP ausliefern statt als PNG und JPG.

    python3 tools/webp.py <html-verzeichnis> [--check]

Im `pages`-Job **nach** `image_dims.py` und `head_meta.py` laufen zu lassen -- die lesen
die Maße aus der Bilddatei und kennen kein WebP -- und **vor** `hydration.py`, das den
Kopf samt dem Stylesheet `bildmasse` ausliest und daraus seinen Wächter baut. Vor
`precompress.py`, wie jeder Schritt, der am Artefakt schreibt.

Warum ein Austausch und kein `<picture>` (2026-11-17, SEO-Audit §8)
-------------------------------------------------------------------
Das Lehrbuch lieferte 7,6 MB Abbildungen aus, auf `/faltung-cnn/` allein 2,3 MB. Die
WebP-Fassungen neben den Quellen (`devnotes/make_webp.py`) sind zusammen 2,4 MB.

Der übliche Weg wäre ein `<picture>` mit `<source type="image/webp">` und dem PNG als
Rückfall. **Der funktioniert hier nicht**, und das ist der Grund für den harten Austausch:
Die Hydration dieses Themes rendert die Wurzel neu (React #423, siehe
`tools/hydration.py`), und was dabei entsteht, baut React aus seiner eigenen Nutzlast --
ein `<picture>`, das nur im ausgelieferten Markup steht, ist nach dem ersten Frame weg.
Am 2026-11-17 an der ausgelieferten Seite nachgemessen: `width`, `height` und
`loading="lazy"` stehen vor der Hydration an jeder Abbildung und **nach** ihr an keiner.

Deshalb wird der Dateiname überall ersetzt, wo er im Artefakt vorkommt: im Markup, im
Stylesheet `bildmasse` (dessen Selektoren am `src` hängen) und in der Hydrations-Nutzlast,
aus der React neu rendert. Dieselbe Stelle-für-Stelle-Ersetzung wie in
`tools/trailing_slash.py`, aus demselben Grund.

WebP und nicht AVIF: WebP liest jeder Browser seit 2020 (Safari 14), AVIF erst seit 2023
(Safari 16.4). Wo es keinen Rückfall geben kann, zählt das ältere Format.

Zugeordnet wird über den **Inhalt**, nicht über den Namen: mystmd hängt an jeden Dateinamen
einen Hash und kürzt den Namen dabei auf 20 Zeichen, und drei Bildpaare dieses Buchs
stimmen in den ersten 20 Zeichen überein (`vl03-linreg-classifi…`). Die gebaute Datei ist
aber bytegleich mit der Quelle (SEO-Audit §10), also ist der SHA-256 der sichere Schlüssel.

Die `.md`-Dateien der Markdown-Auslieferung bleiben unberührt: Sie zeigen auf die Quellen
im Repository, nicht ins Artefakt (SEO-Audit §6.3).
"""

from __future__ import annotations

import argparse
import hashlib
import pathlib
import re
import shutil
import sys

WURZEL = pathlib.Path(__file__).resolve().parent.parent
BILDER = WURZEL / "images"
ENDUNGEN = (".png", ".jpg", ".jpeg")
TEXTDATEIEN = ("*.html", "*.json")


def sha(p: pathlib.Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def quellen_index() -> dict[str, pathlib.Path]:
    """SHA-256 der Quelldatei -> die WebP-Fassung daneben.

    `site_logo.png` liegt in der Wurzel und nicht in `images/`, kommt aber auf jeder
    Seite vor; `devnotes/make_webp.py` baut es deshalb mit.
    """
    index: dict[str, pathlib.Path] = {}
    for p in sorted(BILDER.iterdir()) + [WURZEL / "site_logo.png"]:
        if p.suffix.lower() not in ENDUNGEN or not p.exists():
            continue
        webp = p.with_suffix(".webp")
        if webp.exists():
            index[sha(p)] = webp
    return index


def paare(html: pathlib.Path, index: dict[str, pathlib.Path]) -> list[tuple[pathlib.Path, pathlib.Path]]:
    """(Bilddatei im Artefakt, WebP-Quelle) für alles, was ausgetauscht werden kann."""
    build = html / "build"
    if not build.is_dir():
        sys.exit(f"FEHLER: {build} gibt es nicht -- nach dem HTML-Bau laufen lassen")
    out = []
    for p in sorted(build.iterdir()):
        if p.suffix.lower() not in ENDUNGEN:
            continue
        webp = index.get(sha(p))
        if webp is not None:
            out.append((p, webp))
    return out


def ersetzen(html: pathlib.Path, karte: dict[str, str]) -> tuple[int, int]:
    """Jeden alten Dateinamen durch den neuen ersetzen, in HTML und JSON."""
    dateien = treffer = 0
    for muster in TEXTDATEIEN:
        for p in html.rglob(muster):
            text = p.read_text(encoding="utf-8")
            neu = text
            n = 0
            for alt, w in karte.items():
                if alt in neu:
                    n += neu.count(alt)
                    neu = neu.replace(alt, w)
            if n:
                p.write_text(neu, encoding="utf-8")
                dateien += 1
                treffer += n
    return dateien, treffer


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("html", type=pathlib.Path)
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()

    index = quellen_index()
    if not index:
        sys.exit("FEHLER: keine WebP-Fassungen in images/ -- devnotes/make_webp.py laufen lassen")
    gefunden = paare(args.html, index)
    if not gefunden:
        sys.exit("FEHLER: keine austauschbare Abbildung im Artefakt gefunden")

    karte = {p.name: p.with_suffix(".webp").name for p, _ in gefunden}

    if args.check:
        fehler = 0
        for p, _ in gefunden:
            if not p.with_suffix(".webp").exists():
                print(f"✗ {p.with_suffix('.webp').name} fehlt im Artefakt")
                fehler += 1
        reste: dict[str, int] = {}
        for muster in TEXTDATEIEN:
            for f in args.html.rglob(muster):
                text = f.read_text(encoding="utf-8")
                for alt in karte:
                    if alt in text:
                        reste[alt] = reste.get(alt, 0) + text.count(alt)
        for alt, n in sorted(reste.items()):
            print(f"✗ {alt} steht noch {n}-mal im Artefakt")
            fehler += 1
        if fehler:
            return 1
        gespart = sum(p.stat().st_size - p.with_suffix(".webp").stat().st_size for p, _ in gefunden)
        print(f"✓ {len(gefunden)} Abbildungen als WebP ausgeliefert, "
              f"{gespart / 1024 / 1024:.2f} MB weniger als PNG/JPG")
        return 0

    for p, webp in gefunden:
        shutil.copy2(webp, p.with_suffix(".webp"))
    dateien, treffer = ersetzen(args.html, karte)
    gespart = sum(p.stat().st_size - p.with_suffix(".webp").stat().st_size for p, _ in gefunden)
    print(f"✓ {len(gefunden)} Abbildungen als WebP daneben gelegt, {treffer} Verweise in "
          f"{dateien} Dateien umgeschrieben, {gespart / 1024 / 1024:.2f} MB weniger")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
