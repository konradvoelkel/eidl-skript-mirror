#!/usr/bin/env python3
"""Die Vorschaukarte erzeugen: images/social-card.png, 1200x630.

    uv run --only-group figures python tools/social_card.py            # Karte schreiben
    uv run --only-group figures python tools/social_card.py --check    # byte-genau
    python3 tools/social_card.py --verify                              # Form, nur stdlib

Portiert aus ds-en `tools/social_card.py` (2026-10-19), Farben aus BRANDING.md, Text aus
myst.yml. Die Karte ist **versioniert**; dieses Skript gibt es, damit sie neu erzeugt
werden kann, wenn Titel oder Markenfarbe sich ändern, statt sie von Hand zu malen. Die CI
erzeugt sie nie, sie kopiert nur die eingecheckte PNG.

**Warum überhaupt eine Karte.** MyST leitet `og:image` aus dem ersten Bild einer Seite
ab; hat eine Seite keines, greift es zum ersten Bild des Projekts. Dieses Buch hatte
bis zum 2026-10-19 **gar kein** `og:image` -- weder Projekt-`thumbnail` noch eine
absolute URL. Eine Antwortmaschine, die die Seite zitiert, lässt den Bildplatz dann nicht
leer, sondern füllt ihn: Im Oktober 2026 hing ChatGPT an diesem Buch ein fremdes
neuronales Netz, das jemand anderem gehört (ds-en `SEO-NOTES.md` §21). Ein eigenes Bild
ist der ganze Unterschied.

**Warum die Fassung von Pillow angeheftet ist.** Aus demselben Grund wie bei
`devnotes/make_figures.py`: Die Ausgabe liegt im Repo. Mit einer anderen Pillow- oder
freetype-Fassung ändert sich der Satz, und `--check` meldet dann eine Abweichung, die
keine inhaltliche ist. Deshalb die Gruppe `figures` aus `pyproject.toml` und **nicht**
System-Python.

**Warum zwei Prüfungen.** `--check` rendert neu und vergleicht Bytes -- das findet eine
von Hand bearbeitete PNG oder einen geänderten Generator, aber nur auf einer Maschine mit
derselben Pillow/zlib/freetype. In der CI ist das wertlos. `--verify` liest mit der
Standardbibliothek den PNG-Kopf, prüft 1200x630 und vergleicht die im tEXt-Block
mitgeschriebenen Texte mit `myst.yml`. Das ist die Eigenschaft, auf die es ankommt: eine
zu kleine Karte zeigt keine Plattform an, und eine Karte mit dem alten Buchtitel ist
schlimmer als keine.

Der tEXt-Block ist die Ergänzung gegenüber ds-en, und er ist der Grund, warum `--verify`
mehr kann als dort: ds-ens Fassung kann eine Karte mit veraltetem Titel nicht von einer
richtigen unterscheiden, weil im PNG nicht steht, was darauf steht.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "images" / "social-card.png"
MYST = ROOT / "myst.yml"

W, H = 1200, 630
BRAND = (111, 89, 166)       # #6f59a6, BRANDING.md: Markenfarbe, weiße Schrift 5.8:1
TINT = (239, 235, 255)       # #efebff, die helle Fläche desselben Farbtons
WHITE = (255, 255, 255)

# DejaVu liegt auf dem System und deckt „Völkel" ab; die Webschrift der Seite wird hier
# nicht gebraucht, weil die Karte einmal gerendert und als PNG eingecheckt wird.
FONTS = Path("/usr/share/fonts/truetype/dejavu")

# Die Zeile über dem Titel. Keine Jahreszahl und kein Semester: Die Karte steht in jedem
# geteilten Link und überlebt das Semester, die Beschreibung in myst.yml tut das auch.
EYEBROW = "VORLESUNGSSKRIPT  ·  CC BY-SA 4.0"
CLAIM = "Perzeptron · Backpropagation · Transformer"
BYLINE = "Konrad Völkel   ·   konradvoelkel.com"

# Der Schlüssel des tEXt-Blocks, in dem Titel und Untertitel mitgeschrieben werden.
TEXT_KEY = "eidl-card-source"


def myst_strings() -> tuple[str, str]:
    """`title` und `subtitle` aus myst.yml, ohne PyYAML.

    Mit der Standardbibliothek, damit `--verify` in jedem Container läuft -- derselbe
    Grund, aus dem die übrigen Prüfskripte dieses Repos mit `--no-project` auskommen.
    Gelesen werden genau die zwei Zeilen auf Projektebene (zwei Leerzeichen Einzug); eine
    `title:`-Zeile tiefer im Baum (im TOC etwa) hat mehr Einzug und wird nicht getroffen.
    """
    text = MYST.read_text(encoding="utf-8")
    out = []
    for key in ("title", "subtitle"):
        m = re.search(rf"^  {key}: *(.+?) *$", text, re.M)
        if not m:
            raise SystemExit(f"✗ myst.yml hat kein `{key}:` auf Projektebene")
        out.append(m.group(1).strip().strip("\"'"))
    return out[0], out[1]


def _png_chunks(data: bytes):
    """(Typ, Nutzlast) je Chunk, ohne Pillow."""
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("keine PNG-Datei")
    pos = 8
    while pos + 8 <= len(data):
        length = int.from_bytes(data[pos:pos + 4], "big")
        kind = data[pos + 4:pos + 8]
        yield kind, data[pos + 8:pos + 8 + length]
        pos += 12 + length


def _png_size(data: bytes) -> tuple[int, int]:
    """Breite und Höhe aus dem IHDR, ohne Pillow."""
    for kind, payload in _png_chunks(data):
        if kind == b"IHDR":
            return (int.from_bytes(payload[:4], "big"),
                    int.from_bytes(payload[4:8], "big"))
    raise ValueError("kein IHDR")


def _png_text(data: bytes, key: str) -> str | None:
    """Der tEXt-Block unter diesem Schlüssel, ohne Pillow."""
    for kind, payload in _png_chunks(data):
        if kind == b"tEXt" and payload.split(b"\x00", 1)[0] == key.encode("latin-1"):
            return payload.split(b"\x00", 1)[1].decode("latin-1")
    return None


def _stamp(title: str, subtitle: str) -> str:
    return f"{title}\n{subtitle}"


def font(name: str, size: int):
    from PIL import ImageFont
    return ImageFont.truetype(str(FONTS / name), size)


def wrap(draw, text: str, f, width: int) -> list[str]:
    """Umbruch an Leerzeichen, gegen die tatsächlich gemessene Breite."""
    zeilen: list[str] = []
    rest = text.split()
    while rest:
        zeile = rest[0]
        rest = rest[1:]
        while rest and draw.textlength(f"{zeile} {rest[0]}", font=f) <= width:
            zeile += " " + rest.pop(0)
        zeilen.append(zeile)
    return zeilen


def draw_card(title: str, subtitle: str):
    from PIL import Image, ImageDraw
    img = Image.new("RGB", (W, H), BRAND)
    d = ImageDraw.Draw(img)
    pad = 76
    innen = W - 2 * pad

    d.text((pad, pad), EYEBROW, font=font("DejaVuSans-Bold.ttf", 23), fill=TINT)

    # Titel fett, Untertitel leichter, damit der erste als Name gelesen wird. Beide
    # umgebrochen statt auf eine Zeile gezwungen: „Einführung in Deep Learning" passt in
    # 68 pt, ein längerer Titel in myst.yml soll nicht in den Rand laufen.
    f_t1 = font("DejaVuSans-Bold.ttf", 68)
    y = pad + 62
    for zeile in wrap(d, title, f_t1, innen):
        d.text((pad, y), zeile, font=f_t1, fill=WHITE)
        y += 86

    f_t2 = font("DejaVuSans.ttf", 40)
    y += 10
    for zeile in wrap(d, subtitle, f_t2, innen):
        d.text((pad, y), zeile, font=f_t2, fill=WHITE)
        y += 52

    # Der Satz, der das Buch von anderen Deep-Learning-Skripten unterscheidet, in den
    # Wörtern, nach denen jemand sucht.
    y = pad + 330
    d.rectangle([pad, y, pad + 92, y + 5], fill=TINT)
    d.text((pad, y + 34), CLAIM, font=font("DejaVuSans-Bold.ttf", 32), fill=TINT)

    # Der Autor gehört an den Fuß, nicht in den Titel. Bewusst die eigene Domain und
    # nicht die Pages-URL: Das Buch kann umziehen, eine in die PNG gebackene URL zieht
    # still nicht mit.
    d.text((pad, H - pad - 30), BYLINE, font=font("DejaVuSans.ttf", 26), fill=TINT)
    return img


def verify() -> int:
    rel = OUT.relative_to(ROOT)
    if not OUT.exists():
        print(f"✗ {rel} fehlt; tools/social_card.py laufen lassen")
        return 1
    data = OUT.read_bytes()
    try:
        size = _png_size(data)
    except ValueError as exc:
        print(f"✗ {rel}: {exc}")
        return 1
    if size != (W, H):
        print(f"✗ {rel} ist {size[0]}x{size[1]}, erwartet {W}x{H}. Unter 200x200 zeigt "
              "keine Plattform eine Vorschaukarte an.")
        return 1
    title, subtitle = myst_strings()
    stamp = _png_text(data, TEXT_KEY)
    if stamp is None:
        print(f"✗ {rel} trägt keinen {TEXT_KEY}-Block; mit diesem Skript neu erzeugen")
        return 1
    if stamp != _stamp(title, subtitle):
        print(f"✗ {rel} zeigt {stamp.splitlines()!r}, myst.yml sagt "
              f"{[title, subtitle]!r}; Karte neu erzeugen")
        return 1
    print(f"✓ {rel} ist eine {W}x{H}-PNG und zeigt den Titel aus myst.yml")
    return 0


def main() -> int:
    if "--verify" in sys.argv:
        return verify()

    # Pillow wird erst hier gebraucht: --verify kommt mit der Standardbibliothek aus und
    # muss in jedem Container laufen.
    from PIL.PngImagePlugin import PngInfo

    title, subtitle = myst_strings()
    img = draw_card(title, subtitle)
    meta = PngInfo()
    meta.add_text(TEXT_KEY, _stamp(title, subtitle))

    from io import BytesIO
    buf = BytesIO()
    img.save(buf, "PNG", pnginfo=meta)

    if "--check" in sys.argv:
        if not OUT.exists():
            print(f"✗ {OUT.relative_to(ROOT)} fehlt; tools/social_card.py laufen lassen")
            return 1
        if buf.getvalue() != OUT.read_bytes():
            print(f"✗ {OUT.relative_to(ROOT)} ist nicht aktuell; neu erzeugen")
            return 1
        print(f"✓ {OUT.relative_to(ROOT)} entspricht tools/social_card.py")
        return 0

    OUT.write_bytes(buf.getvalue())
    print(f"✓ {OUT.relative_to(ROOT)} geschrieben ({OUT.stat().st_size} Bytes, {W}x{H})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
