#!/usr/bin/env python3
"""Jede Abbildung bekommt ihre echten Pixelmasse als width/height ins Markup.

    python3 tools/image_dims.py <html-dir> [--base BASE_URL] [--check]

Gegen den Layoutsprung: ohne width/height kennt der Browser das Seitenverhaeltnis
einer Abbildung erst, wenn ihre ersten Bytes da sind. Bis dahin ist sie null Pixel
hoch, und in dem Moment, in dem der Header gelesen ist, ruckt der ganze Text darunter
nach unten. Ein Kapitel mit sechzehn Matplotlib-Bildern ruckt sechzehnmal. Mit beiden
Attributen rechnet der Browser aus ihnen `aspect-ratio` und haelt den Platz von Anfang
an frei -- das ist der ganze Mechanismus, und er braucht *beide* Werte, ein einzelnes
ist wertlos.

Die Masse stehen **nirgends gepflegt**, anders als bei den alt-Texten (alt-texte.yml):
sie stehen in der Bilddatei selbst, im Header. Also werden sie dort gelesen. Eine
Pflegedatei waere hier nur eine zweite Wahrheit, die veralten kann.


Zwei Stellen, nicht eine: Attribute und ein Stylesheet
------------------------------------------------------

Port aus ds-skript (2026-10-29), mit **einer** Abweichung, die an der Hydration haengt.

In ds-skript schlaegt die Hydration fehl (React #418) und rendert das ganze Dokument
neu; dort halten die Attribute nur bis dahin, und ein Waechter (dessen hydration.py)
muss ein <style> je Seite zurueckhaengen. **In eidl schlaegt sie nicht fehl** -- am
2026-11-03 im sichtbaren Browser gegen das gebaute Artefakt gemessen: keine
Fehlermeldung, und nach der Hydration tragen die Abbildungen weiter ihr loading="lazy"
aus head_meta.py. Die Attribute halten hier also beim ersten Laden.

Bleibt die Navigation ohne Neuladen: ein Klick in der Seitenleiste laesst React das
naechste Kapitel aus der Nutzlast rendern, und dessen <img> tragen keine Attribute. Das
Stylesheet ist deshalb hier **eines fuer das ganze Buch** -- je Abbildung aller Seiten
eine Regel

    img[src="..."]{width:1012px;aspect-ratio:1012/488}

und derselbe Block in jedem Kopf. Wer auf irgendeiner Seite einsteigt, hat damit die
Masse jeder Abbildung, die er danach anklickt. CSS haengt nicht am Knoten, sondern am
Selektor: egal wie oft React das <img> neu baut, der src bleibt und die Regel greift.

Warum `width` dazu noetig ist und `aspect-ratio` allein nicht genuegt: ein <img> ohne
geladene Datei hat keine eigene Groesse, seine Breite ist dann null -- und null mal
irgendein Verhaeltnis ist null. Erst `width` gibt die Breite, die das Theme mit
`max-width:100%` wieder einfaengt, und `height:auto` rechnet daraus mit dem Verhaeltnis
die Hoehe. Das ist genau, was die Attribute tun, nur als CSS gesagt.

Die Attribute bleiben trotzdem: sie wirken ohne Stylesheet, also auch dann, wenn das
<style> aus irgendeinem Grund nicht ankommt, und sie sind das, was ein Crawler ohne CSS
sieht.

Der Preis: rund 100 Zeichen je Abbildung im Kopf jeder Seite; die Zahl steht in der
Meldung des Laufs.

Konkurrenz im Stylesheet des Themes, nachgesehen statt angenommen: zu `img` gibt es dort
genau `img,video{max-width:100%;height:auto}` -- das will man -- und zwei
Tailwind-Hilfsklassen (`[&_img]:w-full`, `[&_img]:h-full`), die in keiner ausgelieferten
Seite vorkommen (nachgezaehlt: null Treffer auf allen 32). **Zwei bekannte Grenzen:** eine
Hoehe, die eine *Elternklasse* setzt, sieht dieses Skript nicht -- es liest nur das
style-Attribut des Bildes selbst; und ein Selektor auf den src wirkt im ganzen Dokument,
also auch auf ein gleiches Bild ausserhalb von <main>, dessen style-Attribut hier nie
angesehen wurde. Beides verzerrt dann genauso wie der Lizenzknopf unten und faellt nur im
Browser auf. Am 2026-10-29 nachgesehen: die Bilder in <main> und die der Navigation
teilen keinen src.

Gegengeprueft wurde das Stylesheet daran, dass es *nichts* sichtbar aendert: auf der
Landingpage rendern alle drei Bilder mit dem Stylesheet genau wie ohne (72x36, 722x780
und der Lizenzknopf 102x19 -- der bekommt ja keine Regel), auf kmeans alle elf
(536x585, 722x796, ...).


Was uebersprungen wird, und warum das keine Vorsicht ist, sondern Messung
-------------------------------------------------------------------------

Das width-Attribut ist kein blosser Hinweis: es wirkt als CSS-Eigenschaft (presentational
hint) und setzt die Breite. Solange die Hoehe `auto` ist -- und das ist sie, das Theme
hat `img, video { max-width: 100%; height: auto; }` --, folgt die Hoehe dem echten
Seitenverhaeltnis, und das Bild sieht aus wie vorher. Schreibt aber *CSS* eine feste
Hoehe und laesst die Breite frei, dann gewinnt die CSS-Hoehe, die Attribut-Breite
gewinnt gegen `auto`, und das Bild wird verzerrt.

Am 2026-10-29 im Browser vorgefuehrt, mit absichtlich falschen Massen 640x480:

- Abbildung ohne eigenes CSS: vorher 536x585 gerendert, nachher 640x699 -- unverzerrt,
  Verhaeltnis gehalten. Mit den **echten** Massen bleibt die Breite 536, es aendert
  sich also nichts am Bild; nur der Platz wird vorher freigehalten.
- Der Lizenzknopf der Landingpage, `style="height:20px"`: vorher rund 107x20, nachher
  **640x19**. Breitgezogen ueber die halbe Seite.

Deshalb zwei Ausnahmen, beide am Markup erkennbar:

1. **Hoehe im style-Attribut** -- der Lizenzknopf. Eine Breite im style ist dagegen
   harmlos (`width:100%` am Kursdiagramm): sie gewinnt gegen den Hinweis, die Hoehe
   bleibt auto, das Verhaeltnis kommt aus den Attributen.
2. **width oder height schon gesetzt** -- das Logo der Navigation traegt
   `height="2.25rem"` vom Theme. Das ist als HTML-Attribut ungueltig (dort stehen
   Pixelzahlen, keine CSS-Laengen) und wird vom Browser ignoriert; eine Breite
   dazuzuschreiben wuerde es aber gueltig machen und das Logo auf 216 Pixel ziehen,
   waehrend die Klasse h-9 die Hoehe bei 36 haelt. Das Logo steht ohnehin ausserhalb
   von <main> und wird hier nie angefasst.

Nur die <main>-Scheibe wird umgeschrieben, aus demselben Grund wie in head_meta.py: der
Rest des Dokuments traegt MySTs Hydrations-Nutzlast, die ganze Seite noch einmal als
JSON, und ein freilaufender regulaerer Ausdruck darauf aendert Daten statt Markup.


Zweimal laufen
--------------

Idempotent: ein Bild, das die Attribute schon fuehrt, faellt unter Ausnahme 2 und wird
nicht noch einmal angefasst; das <style> wird an seiner id erkannt und **ersetzt**, nicht
ein zweites Mal angehaengt -- und seine Regeln stehen nicht an den Attributen, sondern an
den Bilddateien, sonst waere der zweite Lauf ein leeres Stylesheet. `--check` ist die Nachbedingung am gebauten Artefakt und
prueft nicht, was dieser Lauf getan hat, sondern was am Ende dasteht -- jedes Bild in
<main> traegt entweder beide Attribute mit den Massen seiner Datei, oder es faellt unter
eine der zwei Ausnahmen. Ein Bild mit falschen Massen ist dabei der eigentliche
Fehlerfall: es haelt Platz frei, nur den falschen, und ruckt damit genauso.

Die Masse kommen aus dem Dateikopf, nicht aus einer Bibliothek: Pillow ist im Image des
Jobs (python:3.13-alpine) nicht da, und vier Formate von Hand zu lesen ist weniger
Angriffsflaeche als eine Abhaengigkeit dafuer einzufuehren. Ein unbekanntes Format
bricht ab, statt stillschweigend ohne Masse durchzulaufen.
"""

from __future__ import annotations

import argparse
import pathlib
import re
import struct
import sys
from urllib.parse import unquote, urlparse

IMG_TAG = re.compile(r"<img\b[^>]*?/?>", re.I)
MAIN = re.compile(r"<main\b[^>]*>.*?</main>", re.S | re.I)

# Das Stylesheet, das die Reservierung ueber die Navigation ohne Neuladen traegt. Die id
# ist der Griff, an dem ein zweiter Lauf hier den Block ersetzt.
STYLE_ID = "bildmasse"
STYLE_RE = re.compile(
    r'<style\b[^>]*\bid="' + STYLE_ID + r'"[^>]*>.*?</style>', re.S | re.I
)


# --- Die Masse aus dem Dateikopf lesen ---------------------------------------------


def png_masse(data: bytes) -> tuple[int, int]:
    """IHDR steht immer zuerst und immer an derselben Stelle: Breite und Hoehe als
    32-Bit-Zahlen ab Byte 16."""
    if len(data) < 24 or data[12:16] != b"IHDR":
        raise ValueError("PNG ohne IHDR an der erwarteten Stelle")
    w, h = struct.unpack(">II", data[16:24])
    return w, h


def gif_masse(data: bytes) -> tuple[int, int]:
    if len(data) < 10:
        raise ValueError("GIF zu kurz fuer den Bildschirm-Deskriptor")
    w, h = struct.unpack("<HH", data[6:10])
    return w, h


def jpeg_masse(data: bytes) -> tuple[int, int]:
    """Durch die Marker laufen, bis ein SOF-Segment kommt; dort stehen Hoehe und Breite.

    Die Laengen der uebersprungenen Segmente stehen im Segment selbst, geraten wird
    nichts. SOF4, SOF8 und SOF12 sind keine Rahmen-Marker und werden ausgelassen.
    """
    i = 2  # die beiden Bytes des SOI-Markers
    while i + 3 < len(data):
        if data[i] != 0xFF:
            raise ValueError(f"JPEG: kein Marker an Position {i}")
        marker = data[i + 1]
        if marker in (0xD8, 0xD9) or 0xD0 <= marker <= 0xD7:
            i += 2
            continue
        laenge = struct.unpack(">H", data[i + 2 : i + 4])[0]
        if marker in (0xC4, 0xC8, 0xCC):
            pass
        elif 0xC0 <= marker <= 0xCF:
            h, w = struct.unpack(">HH", data[i + 5 : i + 9])
            return w, h
        i += 2 + laenge
    raise ValueError("JPEG ohne SOF-Segment")


def svg_masse(text: str) -> tuple[int, int]:
    """width/height am Wurzelelement, sonst die letzten zwei Zahlen der viewBox.

    Prozentangaben taugen nicht als Attribut (sie sind keine Pixelzahl), deshalb
    faellt der Fall auf die viewBox zurueck -- genau die Form, die Matplotlib und
    unser eigenes Kursdiagramm schreiben.
    """
    m = re.search(r"<svg\b[^>]*>", text, re.I | re.S)
    if not m:
        raise ValueError("SVG ohne <svg>-Element")
    wurzel = m.group(0)

    def laenge(name: str) -> float | None:
        a = re.search(rf'\b{name}="([^"]+)"', wurzel, re.I)
        if not a:
            return None
        z = re.fullmatch(r"\s*([0-9.]+)(px|pt)?\s*", a.group(1))
        return float(z.group(1)) if z else None

    w, h = laenge("width"), laenge("height")
    if w is None or h is None:
        vb = re.search(r'\bviewBox="([^"]+)"', wurzel, re.I)
        if not vb:
            raise ValueError("SVG ohne brauchbare width/height und ohne viewBox")
        teile = re.split(r"[\s,]+", vb.group(1).strip())
        if len(teile) != 4:
            raise ValueError(f"SVG mit unlesbarer viewBox: {vb.group(1)!r}")
        w, h = float(teile[2]), float(teile[3])
    return round(w), round(h)


def masse(pfad: pathlib.Path) -> tuple[int, int]:
    """Nach der Signatur unterscheiden, nicht nach der Endung: eine falsch benannte
    Datei soll als das gelesen werden, was sie ist."""
    data = pfad.read_bytes()
    if data[:8] == b"\x89PNG\r\n\x1a\n":
        w, h = png_masse(data)
    elif data[:6] in (b"GIF87a", b"GIF89a"):
        w, h = gif_masse(data)
    elif data[:2] == b"\xff\xd8":
        w, h = jpeg_masse(data)
    elif b"<svg" in data[:2048].lower():
        w, h = svg_masse(data.decode("utf-8", "replace"))
    else:
        raise ValueError(f"unbekanntes Bildformat (erste Bytes: {data[:8]!r})")
    if w <= 0 or h <= 0:
        raise ValueError(f"unbrauchbare Masse {w}x{h}")
    return w, h


# --- Vom src zur Datei --------------------------------------------------------------


def quelle(src: str, seite: pathlib.Path, root: pathlib.Path, base: str) -> pathlib.Path | None:
    """Die Datei zu einem src, oder None, wenn sie nicht auf diesem Server liegt."""
    teil = urlparse(src)
    if teil.scheme or teil.netloc:  # http(s):, data:, //fremder.host
        return None
    pfad = unquote(teil.path)
    if not pfad:
        return None
    if pfad.startswith("/"):
        if base and pfad.startswith(base + "/"):
            pfad = pfad[len(base) :]
        return root / pfad.lstrip("/")
    return seite.parent / pfad


# --- Das Markup --------------------------------------------------------------------


def hoehe_im_stil(tag: str) -> bool:
    """CSS setzt die Hoehe fest -- dann zieht eine Breite daneben das Bild breit."""
    stil = re.search(r'\bstyle="([^"]*)"', tag, re.I)
    return bool(stil and re.search(r"(^|[;\s])height\s*:", stil.group(1), re.I))


def fremde_masse(tag: str) -> bool:
    """Ein width/height, das keine reine Zahl ist: eine CSS-Laenge, wie das Theme sie ans
    Logo schreibt (`height="2.25rem"`). Nichts, was dieses Skript geschrieben haette --
    also auch nichts, worueber es urteilt."""
    return any(
        not t.isdigit() for t in re.findall(r'\b(?:width|height)="([^"]*)"', tag, re.I)
    )


def ausnahme(tag: str) -> str | None:
    """Der Grund, aus dem dieses <img> nicht vermasst wird -- oder None."""
    if re.search(r"\b(width|height)=", tag, re.I):
        return "Masse schon gesetzt"
    if hoehe_im_stil(tag):
        return "Hoehe im style"
    return None


def mit_massen(tag: str, w: int, h: int) -> str:
    """Die zwei Attribute ans Ende des Tags, vor dem schliessenden Winkel.

    Der abschliessende Schraegstrich von `<img ... />` muss dabei *hinter* den neuen
    Attributen bleiben. Steht er davor, liest ein Parser ihn als Attributnamen: das
    ergibt `... alt="x"/ width="536">`, was Browser zwar verzeihen, ein Validator aber
    nicht -- genau das stand seit dem 2026-10-16 im ausgelieferten HTML, weil
    head_meta.py das loading-Attribut so angehaengt hat.
    """
    kern = tag[:-1].rstrip()
    schraeg = ""
    if kern.endswith("/"):
        kern, schraeg = kern[:-1].rstrip(), "/"
    return f'{kern} width="{w}" height="{h}"{schraeg}>'


def vermassen(
    doc: str, seite: pathlib.Path, root: pathlib.Path, base: str
) -> tuple[str, int, dict[str, int]]:
    """Die <main>-Scheibe umschreiben. Gibt Dokument, Anzahl und Ausnahmen zurueck."""
    m = MAIN.search(doc)
    if not m:
        sys.exit(f"FEHLER: {seite} hat kein <main>; nach dem HTML-Bau laufen lassen")

    gesetzt = 0
    uebersprungen: dict[str, int] = {}

    def img_sub(treffer: re.Match) -> str:
        nonlocal gesetzt
        tag = treffer.group(0)
        if (grund := ausnahme(tag)) is not None:
            uebersprungen[grund] = uebersprungen.get(grund, 0) + 1
            return tag
        src = re.search(r'\bsrc="([^"]*)"', tag, re.I)
        if not src:
            sys.exit(f"FEHLER: {seite} hat ein <img> ohne src: {tag[:80]}")
        datei = quelle(src.group(1), seite, root, base)
        if datei is None:
            uebersprungen["fremde Herkunft"] = uebersprungen.get("fremde Herkunft", 0) + 1
            return tag
        if not datei.exists():
            sys.exit(f"FEHLER: {seite} verweist auf {src.group(1)}, aber {datei} fehlt")
        try:
            w, h = masse(datei)
        except ValueError as e:
            sys.exit(f"FEHLER: {datei} (aus {seite}): {e}")
        gesetzt += 1
        return mit_massen(tag, w, h)

    neu = IMG_TAG.sub(img_sub, m.group(0))
    return doc[: m.start()] + neu + doc[m.end() :], gesetzt, uebersprungen


def regeln(
    doc: str, seite: pathlib.Path, root: pathlib.Path, base: str
) -> list[tuple[str, int, int]]:
    """Je Abbildung in <main>, die Platz halten darf: (src, Breite, Hoehe), nach src sortiert.

    Unabhaengig davon, ob *dieser* Lauf die Attribute geschrieben hat: beim zweiten Lauf
    tragen alle Bilder ihre Masse schon, und ein Stylesheet, das daraus nichts mehr
    ableiten koennte, waere beim naechsten Durchlauf leer. Zwei <img> mit demselben src
    ergeben eine Regel.
    """
    m = MAIN.search(doc)
    if not m:
        sys.exit(f"FEHLER: {seite} hat kein <main>; nach dem HTML-Bau laufen lassen")

    gefunden: dict[str, tuple[int, int]] = {}
    for tag in IMG_TAG.findall(m.group(0)):
        if hoehe_im_stil(tag) or fremde_masse(tag):
            continue
        src = re.search(r'\bsrc="([^"]*)"', tag, re.I)
        if not src:
            continue  # vermassen() bricht dafuer schon ab
        datei = quelle(src.group(1), seite, root, base)
        if datei is None or not datei.exists():
            continue
        try:
            gefunden[src.group(1)] = masse(datei)
        except ValueError as e:
            sys.exit(f"FEHLER: {datei} (aus {seite}): {e}")
    return [(s, *gefunden[s]) for s in sorted(gefunden)]


def stilblock(satz: list[tuple[str, int, int]], seite: pathlib.Path) -> str:
    """Der <style>-Block zu einem Satz Regeln, oder "" fuer eine Seite ohne Abbildung."""
    if not satz:
        return ""
    for src, _, _ in satz:
        if '"' in src or "<" in src or "\n" in src:
            sys.exit(f"FEHLER: {seite}: {src!r} passt nicht in einen CSS-Selektor")
    css = "".join(
        f'img[src="{src}"]{{width:{w}px;aspect-ratio:{w}/{h}}}' for src, w, h in satz
    )
    return f'<style id="{STYLE_ID}">{css}</style>'


def mit_stil(doc: str, seite: pathlib.Path, block: str) -> str:
    """Den Block in den Kopf setzen, einen vorhandenen ersetzen, einen leeren entfernen.

    Ans Ende des Kopfes, nach den Stylesheets des Themes: bei gleicher Spezifitaet
    entscheidet die Reihenfolge, und `img[src="..."]` soll gegen eine gleich spezifische
    Regel des Themes gewinnen.
    """
    vorhanden = STYLE_RE.search(doc)
    if vorhanden:
        return doc[: vorhanden.start()] + block + doc[vorhanden.end() :]
    if not block:
        return doc
    i = doc.find("</head>")
    if i < 0:
        sys.exit(f"FEHLER: {seite} hat kein </head>")
    return doc[:i] + block + doc[i:]


def stil_pruefen(doc: str, seite: pathlib.Path, erwartet: str) -> int:
    """Nachbedingung fuer das Stylesheet: genau der Block, der zu diesem <main> gehoert,
    und er steht im Kopf. Gibt die Zahl der Regeln zurueck."""
    gefunden = STYLE_RE.search(doc)
    if not erwartet:
        if gefunden:
            sys.exit(
                f"FEHLER: {seite} hat ein <style id=\"{STYLE_ID}\">, aber keine Abbildung,"
                " fuer die Platz zu halten waere"
            )
        return 0
    if not gefunden:
        sys.exit(
            f"FEHLER: {seite} hat kein <style id=\"{STYLE_ID}\"> -- nach einem Klick"
            " ohne Neuladen haelt dann nichts mehr den Platz frei"
        )
    if gefunden.group(0) != erwartet:
        sys.exit(
            f"FEHLER: {seite}: das <style id=\"{STYLE_ID}\"> passt nicht zu den"
            " Abbildungen des Buchs -- hat ein Schritt danach noch am Markup gedreht?"
        )
    kopf_ende = doc.find("</head>")
    if kopf_ende < 0 or gefunden.start() > kopf_ende:
        sys.exit(
            f"FEHLER: {seite}: das <style id=\"{STYLE_ID}\"> steht nicht im Kopf -- nur"
            " dort ueberlebt es den Wechsel des Kapitels"
        )
    return erwartet.count("img[src=")


def pruefen(doc: str, seite: pathlib.Path, root: pathlib.Path, base: str) -> int:
    """Nachbedingung: jedes <img> in <main> traegt die Masse seiner Datei oder faellt
    unter eine der zwei Ausnahmen. Gibt die Zahl der geprueften Bilder zurueck."""
    m = MAIN.search(doc)
    if not m:
        sys.exit(f"FEHLER: {seite} hat kein <main>")

    geprueft = 0
    for tag in IMG_TAG.findall(m.group(0)):
        # Dieselben zwei Grenzen wie beim Schreiben. Ohne die zweite waere die Pruefung
        # am Logo dauerhaft rot, ohne dass ein Lauf sie heilen koennte -- derselbe
        # Riegel, an dem head_meta.py schon einmal haengengeblieben ist.
        if hoehe_im_stil(tag) or fremde_masse(tag):
            continue
        src = re.search(r'\bsrc="([^"]*)"', tag, re.I)
        datei = quelle(src.group(1), seite, root, base) if src else None
        if datei is None:
            continue
        w_attr = re.search(r'\bwidth="(\d+)"', tag, re.I)
        h_attr = re.search(r'\bheight="(\d+)"', tag, re.I)
        if not (w_attr and h_attr):
            sys.exit(
                f"FEHLER: {seite} hat ein <img> ohne beide Masse: {src.group(1)} -- "
                f"ohne width *und* height haelt der Browser keinen Platz frei"
            )
        if not datei.exists():
            sys.exit(f"FEHLER: {seite} verweist auf {src.group(1)}, aber {datei} fehlt")
        w, h = masse(datei)
        if (int(w_attr.group(1)), int(h_attr.group(1))) != (w, h):
            sys.exit(
                f"FEHLER: {seite} gibt fuer {src.group(1)} "
                f"{w_attr.group(1)}x{h_attr.group(1)} an, die Datei ist {w}x{h} -- "
                f"falsche Masse halten den falschen Platz frei"
            )
        geprueft += 1
    return geprueft


def buchblock(seiten: list[pathlib.Path], root: pathlib.Path, base: str) -> str:
    """Ein <style>-Block mit den Regeln *aller* Seiten, fuer jeden Kopf derselbe."""
    alle: dict[str, tuple[int, int]] = {}
    for f in seiten:
        for src, w, h in regeln(f.read_text(encoding="utf-8"), f, root, base):
            alle[src] = (w, h)
    return stilblock([(s, *alle[s]) for s in sorted(alle)], root)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("html_dir")
    ap.add_argument("--base", default="", help="BASE_URL, der Pfad, unter dem die Seite liegt")
    ap.add_argument(
        "--check",
        action="store_true",
        help="nichts schreiben, nur die Nachbedingung am gebauten Artefakt pruefen",
    )
    args = ap.parse_args()

    root = pathlib.Path(args.html_dir)
    base = "/" + args.base.strip("/") if args.base.strip("/") else ""
    seiten = sorted(root.rglob("index.html"))
    if not seiten:
        sys.exit(f"FEHLER: unter {root} liegt keine index.html; nach dem HTML-Bau laufen lassen")

    if args.check:
        geprueft = 0
        block = buchblock(seiten, root, base)
        for f in seiten:
            doc = f.read_text(encoding="utf-8")
            geprueft += pruefen(doc, f, root, base)
            n_regeln = stil_pruefen(doc, f, block)
        if not geprueft:
            sys.exit(
                "FEHLER: kein einziges Bild geprueft -- entweder ist <main> leer oder "
                "die src-Pfade zeigen nicht mehr auf dieses Artefakt"
            )
        print(f"image_dims --check: {len(seiten)} Seiten, {geprueft} Abbildungen mit "
              f"den Massen ihrer Datei, {n_regeln} CSS-Regeln in jedem Kopf")
        return

    gesamt = 0
    uebersprungen: dict[str, int] = {}
    for f in seiten:
        doc = f.read_text(encoding="utf-8")
        neu, n, aus = vermassen(doc, f, root, base)
        if neu != doc:
            f.write_text(neu, encoding="utf-8")
        gesamt += n
        for grund, k in aus.items():
            uebersprungen[grund] = uebersprungen.get(grund, 0) + k

    # Die Regeln aus dem *neuen* Markup aller Seiten, damit beide Stellen dasselbe sagen;
    # derselbe Block in jeden Kopf (Docstring: Navigation ohne Neuladen).
    block = buchblock(seiten, root, base)
    for f in seiten:
        doc = f.read_text(encoding="utf-8")
        neu = mit_stil(doc, f, block)
        if neu != doc:
            f.write_text(neu, encoding="utf-8")

    geprueft = 0
    for f in seiten:
        doc = f.read_text(encoding="utf-8")
        geprueft += pruefen(doc, f, root, base)
        stil_pruefen(doc, f, block)
    rest = ", ".join(f"{k} {g}" for g, k in sorted(uebersprungen.items())) or "keine"
    print(
        f"image_dims: {len(seiten)} Seiten, {gesamt} Abbildungen vermasst, "
        f"{geprueft} tragen die Masse ihrer Datei; {block.count('img[src=')} CSS-Regeln "
        f"in jedem Kopf; uebersprungen: {rest}"
    )


if __name__ == "__main__":
    main()
