#!/usr/bin/env python3
"""Die OpenGraph-Tags nachtragen, die MyST ausläßt, die Sprache setzen und die
Abbildungen unter der Falz verzögert laden.

    python3 tools/head_meta.py <site-url> <html-verzeichnis> [--lang de]

Portiert aus ds-skript `tools/head_meta.py` (2026-10-19), das seinerseits aus ds-en
stammt. Alles als Nachbearbeitung am gebauten HTML, weil keines davon in myst.yml oder
im Frontmatter eines Kapitels gesagt werden kann. Läuft **nach** dem Canonical-Schritt
in `tools/publish_urls.py`: og:url bekommt dieselbe URL, die der Canonical nennt.


1. Die Karten-Tags, die MyST ausläßt
------------------------------------

MyST schreibt og:title, og:description und og:image und hört dann auf. Vier fehlen:

- **og:url** ist, was eine Plattform als kanonische Identität eines geteilten Links
  behandelt; ohne es werden aus zwei Schreibweisen derselben URL zwei Karten mit zwei
  Kommentarsträngen.
- **og:site_name** setzt den Namen des Buchs auf die Karte und speist Googles
  Site-Name-Signal.
- **twitter:card = summary_large_image.** Die Karte liegt in 1200x630 vor
  (`tools/social_card.py`); ohne diese Zeile zeigt X die kleine Karte mit
  Briefmarkenbild. Inhalt holt X aus den og:-Tags, twitter:title und
  twitter:description sind deshalb überflüssig.
- **og:type**: „book" auf dem Titelblatt, „article" auf den Kapiteln. Die Vorgabe ohne
  Angabe ist „website", also das, was eine Shop-Startseite wäre.
- **og:locale = de_DE.** Ohne Alternate: Dieses Buch gibt es nur auf Deutsch (anders als
  das Data-Science-Skript, das ein englisches Gegenstück hat).

**Der Name wird aus der Landingpage gelesen, nie hart geschrieben.** Deren <title> ist
der Projekttitel allein; ein Umbenennen in myst.yml trägt sich also von selbst durch und
kann keine veraltete Zeichenkette hinterlassen.


2. lang="de" am <html>
----------------------

Das Theme schreibt `<html lang="en">` -- hart im Bundle, und myst.yml hat keinen Schalter
dafür. Eine deutsche Seite, die sich als englisch ausgibt, läßt Screenreader den Text
englisch aussprechen und widerspricht allem anderen am Dokument: `inLanguage: "de"` im
JSON-LD, 90 000 Wörter Deutsch.

Das Attribut im ausgelieferten HTML zu setzen reicht nicht: Die Hydration des Themes
schreibt lang="en" zurück. Deshalb geht ein kleiner Wächter mit, ein MutationObserver auf
genau diesem Attribut. Einmalig zuweisen genügt nicht, weil das Theme ein Client-Router
ist und jeder Kapitelwechsel ohne Neuladen das Attribut erneut setzt. (In ds-skript am
2026-10-16 im Browser nachgemessen; hier übernommen, weil es dasselbe book-theme ist.)


3. loading="lazy" auf den Abbildungen -- und die Preloads, die es aufgehoben hätten
-----------------------------------------------------------------------------------

Das erste Bild in <main> bleibt eager: Das LCP-Element verzögert zu laden heißt genau die
Messung zu verschlechtern, um die es geht. Alles danach bekommt `loading="lazy"` und
`decoding="async"`. Das Logo der Navigation steht außerhalb von <main> und wird nie
angefaßt.

**Das Attribut allein hätte nichts getan.** MyST schreibt für *jedes* Bild der Seite ein
`<link rel="preload" as="image">` in den Kopf; ein vorgeladenes Bild wird sofort geholt,
was `loading` auch sagt -- die zwei Tags widersprechen sich und das Preload gewinnt. Das
Preload wird deshalb für genau die Bilder entfernt, die lazy geworden sind, und bleibt
für die zwei, die es haben sollen: das Logo und die erste Abbildung.

Nur die <main>-Scheibe wird umgeschrieben. Der Rest des Dokuments trägt MySTs
Hydrations-Nutzlast -- die ganze Seite noch einmal als JSON in einem <script> --, und ein
freilaufender regulärer Ausdruck darauf änderte Zeichenketten, die der Browser als Daten
liest.


4. Die Vorschaukarte, und die Abbildungen, die keine ist
--------------------------------------------------------

Jede Seite erklärt `twitter:card=summary_large_image`, und das will 1200x630. MyST füllt
og:image aber mit der *ersten Abbildung* der Seite und greift erst dann auf das
Projekt-Thumbnail zurück -- die echte Karte aus `tools/social_card.py` --, wenn eine
Seite gar keine hat. Am 2026-10-19 am gebauten Artefakt nachgemessen: **18 der 30 Seiten**
trugen eine Abbildung als Karte, darunter `backpropagation` mit 843x237,
`representation-learning-graphen` mit 712x353 und `autoencoder` mit 479x445. Keine
einzige dieser 18 erreicht 630 Pixel Höhe; unter dem Mindestmaß wird eine Karte je nach
Plattform beschnitten, gefüllt oder gar nicht gezeigt.

Die Regel wird deshalb je Seite angewandt: Eine Abbildung bleibt die Karte nur, wenn sie
mindestens 1200x630 **und** querformatig ist und 500 kB nicht überschreitet; sonst bekommt
die Seite die allgemeine Karte, die 1200x630 ist und von `social_card.py --verify` auch
so geprüft wird. Die Byte-Grenze ist aus ds-en übernommen und trifft hier genau eine
Datei, `faltung-cnn` mit 462 kB -- knapp darunter, also unberührt; sie fängt die
Abbildung ab, die eine Karte nur dem Maß nach wäre.

Der Dateiname der Karte wird **aus der Landingpage gelesen**, nicht geraten: MyST hängt
einen Hash an, der sich bei jedem Neuerzeugen ändert. Die URL, die in eine Seite
geschrieben wird, entsteht aus dem Präfix, das deren *eigenes* Bild-Tag schon trägt --
damit funktioniert der Schritt vor und nach dem Absolutmachen der Asset-URLs und kann
keine zweite Schreibweise der Origin erfinden.

`<meta name="image">` wird mitgeschrieben: MySTs eigenes allgemeines Tag mit demselben
Wert; zwei Tags, die verschiedene Bilder nennen, wären schlimmer als jede der beiden
Antworten. Und die Hydrations-Nutzlast ebenso, weil das Theme og:image aus
`page.frontmatter.thumbnail` neu rendert -- Markup allein setzte die abgelehnte Abbildung
im gerenderten DOM zurück. Für die Plattformen, die eine Karte zeichnen, ändert das
nichts (keine führt das Skript aus); es ist Google, das rendert, bevor es indexiert.

**Nur `page.frontmatter`.** Die Nutzlast führt auch `config.projects[0].pages[]` und
`project.pages[]` mit je einem `thumbnail` -- das sind keine Kartenangaben, sondern die
kleine Vorschau, die beim Überfahren eines internen Links aufklappt. Eine 843x237-Grafik
ist dafür vollkommen in Ordnung, und sie alle auf die eine Karte umzuschreiben machte
jede Vorschau im Buch gleich.


Was hier absichtlich fehlt
--------------------------

Vier Abschnitte der Vorlagen sind **nicht** portiert, jeder aus einem Grund, der hier
nachprüfbar ist:

* **Das Vorladen der Schriften** (ds-skript 2). Dieses Buch liefert keine eigenen
  woff2-Dateien aus; ein Preload auf `/fonts/…` zeigte ins Leere. Das Theme holt KaTeX,
  Font-Awesome und das Matplotlib-Widget-CSS weiterhin von zwei CDN -- das zu ändern ist
  `vendor_assets.py` in den Schwesterrepos und ein eigenes Vorhaben.
* **Das Eindeutschen des sichtbaren Datums** (ds-skript, `datum_eindeutschen`). Es setzt
  ein `date:` im Frontmatter voraus, das hier keine Seite hat, weil `freshness.py` nicht
  portiert ist.
* **Das Kürzen des Titel-Suffix** (ds-en 1). Der Suffix dieses Buchs ist
  „ - Einführung in Deep Learning", und MyST setzt ihn hier ohnehin nicht auf jede Seite;
  die Messung, die ihn in ds-en rechtfertigte, gibt es hier nicht.
* **Die Bildmaße im Markup und im Stylesheet und die Gliederungsreservierung**
  (ds-en 7 und 9). Beide hängen an Messungen (CLS, Layoutverschiebung) am dortigen Satz
  von Abbildungen; sie hier ungemessen nachzubauen hieße, Zahlen zu behaupten statt sie
  zu kennen. Offen in `devnotes/TODO.md`.


Zweimal laufen
--------------

Idempotent, und es prüft Nachbedingungen statt der eigenen Änderungen: Jede Seite muß am
Ende die Karten-Tags und lang="de" führen, und kein lazy gemachtes Bild darf noch ein
Preload tragen. Ein zweiter Lauf ist ein zulässiger Leerlauf, der trotzdem besteht,
während Markup, das MyST unter uns verschoben hat, auffällt -- der Fall, für den die
Prüfung eigentlich da ist.

Ergänzt wird **je Tag**, nicht pauschal: Ein Artefakt, das eine frühere Fassung dieses
Skripts bearbeitet hat, bekommt genau die Tags nach, die ihm fehlen. Ein Riegel an og:url
für alle Tags bricht in dem Moment, in dem ein Tag dazukommt.
"""

from __future__ import annotations

import argparse
import html
import json
import pathlib
import re
import struct
import sys

# Erkennungszeichen des Sprach-Wächters, damit ein zweiter Lauf Leerlauf bleibt.
MARKER_LANG = "/*lang-waechter*/"

# Was eine Abbildung erfüllen muss, um als summary_large_image durchzugehen. Die
# Byte-Grenze stammt aus ds-en: Dort kam eine Seite mit 1600x983 und 1,2 MB durch die
# Maßregel, für ein Bild, das ohnehin auf 1200x630 skaliert gezeigt wird.
CARD_MIN_WIDTH, CARD_MIN_HEIGHT = 1200, 630
CARD_MAX_BYTES = 500 * 1024


def page_url(site: str, rel: pathlib.PurePath) -> str:
    """Die URL, die 200 liefert: mit Schrägstrich, so wie der Canonical sie hat."""
    return f"{site}/" if str(rel) == "." else f"{site}/{rel}/"


def project_title(index_html: str) -> str:
    m = re.search(r"<title[^>]*>(.*?)</title>", index_html, re.S | re.I)
    if not m:
        sys.exit("FEHLER: die Landingpage hat kein <title>; kein Name für og:site_name")
    title = html.unescape(m.group(1).strip())
    if not title:
        sys.exit("FEHLER: der <title> der Landingpage ist leer")
    return title


def head_tags(url: str, site_name: str, lang: str, is_landing: bool) -> list[tuple[str, str]]:
    """Die Tags als (Merkmal, Tag); das Merkmal sagt, ob die Seite das Tag schon hat."""
    # de -> de_DE: OpenGraph will den Unterstrich-Code, nicht das Sprachkürzel.
    locale = {"de": "de_DE", "en": "en_US"}.get(lang, lang)
    return [
        ('property="og:url"',
         f'<meta property="og:url" content="{html.escape(url, quote=True)}"/>'),
        ('property="og:site_name"',
         f'<meta property="og:site_name" content="{html.escape(site_name, quote=True)}"/>'),
        ('property="og:type"',
         f'<meta property="og:type" content="{"book" if is_landing else "article"}"/>'),
        ('property="og:locale"', f'<meta property="og:locale" content="{locale}"/>'),
        ('name="twitter:card"',
         '<meta name="twitter:card" content="summary_large_image"/>'),
    ]


def set_html_lang(doc: str, lang: str) -> tuple[str, bool]:
    """Die Sprache am <html> setzen. Gibt das Dokument und zurück, ob sie schon stand."""
    m = re.search(r"<html\b[^>]*>", doc, re.I)
    if not m:
        return doc, False
    tag = m.group(0)
    if re.search(rf'\blang="{re.escape(lang)}"', tag, re.I):
        return doc, True
    if re.search(r'\blang="[^"]*"', tag, re.I):
        neu = re.sub(r'\blang="[^"]*"', f'lang="{lang}"', tag, count=1, flags=re.I)
    else:
        neu = tag[:5] + f' lang="{lang}"' + tag[5:]
    return doc[: m.start()] + neu + doc[m.end():], False


def keep_html_lang(doc: str, lang: str) -> tuple[str, bool]:
    """Das lang nach der Hydration wieder setzen -- sonst hält es nur bis zum ersten Frame."""
    if MARKER_LANG in doc:
        return doc, True
    if "</head>" not in doc:
        return doc, False
    script = (
        f'<script>{MARKER_LANG}(function(){{var l="{lang}",h=document.documentElement;'
        "function f(){if(h.lang!==l)h.lang=l}f();"
        'new MutationObserver(f).observe(h,{attributes:true,attributeFilter:["lang"]});'
        "})();</script>"
    )
    return doc.replace("</head>", script + "</head>", 1), False


def lazy_load_figures(doc: str) -> tuple[str, set[str]]:
    """Jedes <img> in <main> außer dem ersten verzögert laden.

    Gibt das Dokument und die Menge der src-URLs zurück, die lazy geworden sind, damit
    der Aufrufer die passenden Preloads entfernen kann -- ohne das hat das Attribut
    überhaupt keine Wirkung.
    """
    m = re.search(r"<main\b[^>]*>.*?</main>", doc, re.S | re.I)
    if not m:
        return doc, set()
    main = m.group(0)
    lazied: set[str] = set()
    gesehen = 0

    def img_sub(tag: re.Match) -> str:
        nonlocal gesehen
        gesehen += 1
        t = tag.group(0)
        if gesehen == 1:  # LCP-Kandidat bleibt eager und behält sein Preload
            return t
        src = re.search(r'\bsrc="([^"]*)"', t, re.I)
        if src:
            lazied.add(src.group(1))
        if re.search(r"\bloading=", t, re.I):
            return t
        return t[:-1].rstrip() + ' loading="lazy" decoding="async"' + t[-1]

    main_neu = re.sub(r"<img\b[^>]*?/?>", img_sub, main, flags=re.I)
    return doc[: m.start()] + main_neu + doc[m.end():], lazied


def drop_image_preloads(doc: str, srcs: set[str]) -> tuple[str, int]:
    """`<link rel="preload" as="image">` für die jetzt lazy geladenen Bilder entfernen."""
    if not srcs:
        return doc, 0
    n = 0

    def link_sub(m: re.Match) -> str:
        tag = m.group(0)
        nonlocal n
        if 'as="image"' not in tag:
            return tag
        href = re.search(r'\bhref="([^"]*)"', tag)
        if href and href.group(1) in srcs:
            n += 1
            return ""
        return tag

    doc = re.sub(r'<link\b[^>]*rel="preload"[^>]*/?>', link_sub, doc, flags=re.I)
    return doc, n


def image_size(path: pathlib.Path) -> tuple[int, int]:
    """Breite und Höhe eines PNG oder JPEG, ohne Pillow.

    Ohne Pillow, damit dieser Schritt in jedem Container läuft -- der pages-Job dieses
    Repos installiert kein einziges Python-Paket, und das soll so bleiben (CLAUDE.md,
    bewusste Entscheidung 5). PNG steht im IHDR, JPEG im ersten SOF-Segment.
    """
    data = path.read_bytes()
    if data[:8] == b"\x89PNG\r\n\x1a\n":
        return struct.unpack(">II", data[16:24])
    if data[:2] == b"\xff\xd8":
        i = 2
        while i + 9 < len(data):
            if data[i] != 0xFF:
                break
            marker, laenge = data[i + 1], int.from_bytes(data[i + 2:i + 4], "big")
            # SOF0..SOF15 ohne die vier, die keine Rahmenköpfe sind (DHT, JPG, DAC, RST).
            if marker in (0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7,
                          0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF):
                h, w = struct.unpack(">HH", data[i + 5:i + 9])
                return w, h
            i += 2 + laenge
    sys.exit(f"FEHLER: {path} ist weder PNG noch JPEG; Kartenmaß nicht feststellbar")


def card_ok(path: pathlib.Path) -> tuple[bool, str]:
    """Ob dieses Bild eine summary_large_image-Karte sein kann -- und warum nicht."""
    width, height = image_size(path)
    kb = path.stat().st_size // 1024
    if width < CARD_MIN_WIDTH or height < CARD_MIN_HEIGHT:
        return False, f"{width}x{height}, unter {CARD_MIN_WIDTH}x{CARD_MIN_HEIGHT}"
    if height >= width:
        return False, f"{width}x{height}, kein Querformat"
    if path.stat().st_size > CARD_MAX_BYTES:
        return False, f"{kb} kB, über {CARD_MAX_BYTES // 1024} kB"
    return True, f"{width}x{height}, {kb} kB"


def card_file(root: pathlib.Path, url: str) -> pathlib.Path:
    """Die gebaute Datei, auf die ein og:image zeigt -- absolute URL oder nicht."""
    if "/build/" not in url:
        sys.exit(f"FEHLER: og:image {url} ist kein gebautes Asset; Maß nicht prüfbar")
    return root / "build" / url.rsplit("/build/", 1)[1]


def social_card(root: pathlib.Path, index_html: str) -> str:
    """Der Dateiname der allgemeinen Karte, aus dem og:image der Landingpage gelesen.

    Nicht geglobt und nicht hart geschrieben: MyST hängt einen Hash an den Dateinamen,
    der sich bei jedem Neuerzeugen der Karte ändert, und legt dieselbe Datei unter zwei
    Hashes ab. Die Landingpage hat keine eigene erste Abbildung, trägt also das
    Projekt-Thumbnail -- und das ist die Karte.
    """
    m = re.search(r'<meta property="og:image" content="([^"]+)"', index_html)
    if not m:
        sys.exit("FEHLER: die Landingpage hat kein og:image; steht `thumbnail:` in "
                 "myst.yml, und ist tools/social_card.py gelaufen?")
    name = m.group(1).rsplit("/", 1)[-1]
    ok, warum = card_ok(card_file(root, m.group(1)))
    if not ok:
        sys.exit(f"FEHLER: die Karte selbst besteht die Kartenregel nicht: {warum}")
    return name


def read_payload(doc: str):
    """Die Hydrations-Nutzlast samt Anfang und Ende; None, wenn es keine gibt.

    Die Seite ist eine Remix-Anwendung: Das ganze Dokument steht ein zweites Mal in
    `window.__remixContext`, und bei der Hydration rendert das Theme den Kopf aus *der*
    neu. Was im Markup geändert wird und in der Nutzlast ebenfalls steht, muss an beiden
    Stellen geändert werden -- sonst widersprechen sich ausgeliefertes und hydriertes
    Dokument, und da Google rendert, bevor es indexiert, verliert das, was wir geändert
    haben.
    """
    key = "window.__remixContext = "
    i = doc.find(key)
    if i < 0:
        return None
    start = i + len(key)
    try:
        # raw_decode gibt den Index *in doc* zurück, an dem das JSON endet, nicht die
        # Länge. Das als Länge zu behandeln schneidet den Rest des Dokuments ab -- in
        # ds-en einmal passiert und ausgeliefert: jede Seite endete mitten in der
        # Nutzlast, ohne </html> und ohne das Modul, das den Client startet.
        payload, end = json.JSONDecoder().raw_decode(doc, start)
    except ValueError:
        return None
    return payload, start, end


def routes(payload: dict):
    """Die loaderData-Routen -- dort stehen die Werte, die hier geändert werden."""
    for route in (payload.get("state", {}).get("loaderData") or {}).values():
        if isinstance(route, dict):
            yield route


def edit_payload(doc: str, mutate) -> tuple[str, bool]:
    """Die Nutzlast an `mutate` geben und zurückschreiben, wenn sie etwas geändert hat."""
    gefunden = read_payload(doc)
    if gefunden is None:
        return doc, False
    payload, start, end = gefunden
    if not mutate(payload):
        return doc, False
    # Kompakt neu serialisiert. Die drei Ersetzungen halten das JSON als
    # JavaScript-Literal *innerhalb eines <script>* sicher: Ein wörtliches "<" könnte
    # das Element früh schließen, und U+2028/U+2029 sind in JSON gewöhnliche Zeichen,
    # in JavaScript aber Zeilenenden.
    out = json.dumps(payload, separators=(",", ":"), ensure_ascii=False)
    out = (out.replace("<", "\\u003c")
              .replace("\u2028", "\\u2028")
              .replace("\u2029", "\\u2029"))
    return doc[:start] + out + doc[end:], True


def set_payload_card(doc: str, card: str) -> tuple[str, bool]:
    """Die Karte der Nutzlast auf die Karte zeigen lassen, die das Markup jetzt nennt.

    Dieselbe Falle wie beim Titel, ein Tag tiefer: Das Theme baut og:image aus
    `page.frontmatter.thumbnailOptimized || page.frontmatter.thumbnail`. Eine Seite,
    deren Markup oben korrigiert wurde und deren Nutzlast nicht, zeigt die abgelehnte
    Abbildung wieder, sobald sie hydriert.

    **Nur `page.frontmatter`** -- Begründung im Docstring, Abschnitt 4.
    """
    def mutate(payload: dict) -> bool:
        geaendert = False
        for route in routes(payload):
            page = route.get("page")
            front = page.get("frontmatter") if isinstance(page, dict) else None
            if not isinstance(front, dict):
                continue
            for key in ("thumbnail", "thumbnailOptimized"):
                url = front.get(key)
                if isinstance(url, str) and "/build/" in url and not url.endswith(card):
                    front[key] = f"{url.rsplit('/build/', 1)[0]}/build/{card}"
                    geaendert = True
        return geaendert

    return edit_payload(doc, mutate)


def vet_card(doc: str, root: pathlib.Path, card: str) -> tuple[str, str]:
    """Die Karte einer Seite durch die allgemeine ersetzen, wenn ihre Abbildung keine ist.

    Gibt das Dokument und den Grund zurück, fürs Protokoll. Die Ersetzung behält das
    Präfix, das das eigene og:image der Seite schon trägt -- so schreibt sie dieselbe
    Schreibweise der Origin wie der übrige Bau, vor und nach dem Absolutmachen.
    """
    m = re.search(r'<meta property="og:image" content="([^"]+)"', doc)
    if not m:
        sys.exit("FEHLER: eine Seite hat gar kein og:image; MyST schreibt immer eines")
    url = m.group(1)
    if url.endswith(card):
        return doc, "schon die Karte"
    ok, warum = card_ok(card_file(root, url))
    if ok:
        return doc, f"Abbildung behalten ({warum})"

    def swap(m: re.Match) -> str:
        if "/build/" not in m.group(2):
            sys.exit(f"FEHLER: {m.group(0)} ist kein gebautes Asset")
        return (m.group(1) + m.group(2).rsplit("/build/", 1)[0]
                + f"/build/{card}" + m.group(3))

    for kind, name in (("property", "og:image"), ("name", "image")):
        doc = re.sub(rf'(<meta {kind}="{name}" content=")([^"]*)(")', swap, doc)
    return doc, f"ersetzt ({warum})"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("site")
    ap.add_argument("html_dir")
    ap.add_argument("--lang", default="de",
                    help='Sprache für <html lang> (Vorgabe "de"; das Theme sagt "en")')
    args = ap.parse_args()

    site = args.site.rstrip("/")
    root = pathlib.Path(args.html_dir)
    index = root / "index.html"
    if not index.exists():
        sys.exit(f"FEHLER: {index} existiert nicht; nach dem HTML-Bau laufen lassen")

    name = project_title(index.read_text(encoding="utf-8"))
    karte = social_card(root, index.read_text(encoding="utf-8"))
    seiten = sorted(root.rglob("index.html"))
    n_lazy = n_preload = n_head = n_lang = n_guard = n_karten = 0

    for f in seiten:
        rel = f.parent.relative_to(root)
        doc = f.read_text(encoding="utf-8")

        fehlend = [
            tag for marker, tag in head_tags(
                page_url(site, rel), name, args.lang, str(rel) == "."
            ) if marker not in doc
        ]
        if fehlend:
            if "</head>" not in doc:
                sys.exit(f"FEHLER: {f} hat kein </head>")
            doc = doc.replace("</head>", "".join(fehlend) + "</head>", 1)
            n_head += 1

        doc, hatte_lang = set_html_lang(doc, args.lang)
        n_lang += not hatte_lang
        doc, hatte_guard = keep_html_lang(doc, args.lang)
        n_guard += not hatte_guard

        doc, grund = vet_card(doc, root, karte)
        if grund.startswith("ersetzt"):
            n_karten += 1
            doc, _ = set_payload_card(doc, karte)

        doc, lazied = lazy_load_figures(doc)
        doc, entfernt = drop_image_preloads(doc, lazied)
        n_lazy += len(lazied)
        n_preload += entfernt

        f.write_text(doc, encoding="utf-8")

    # Nachbedingungen, keine Bilanz dieses Laufs.
    for f in seiten:
        doc = f.read_text(encoding="utf-8")
        for prop, kind in (("og:url", "property"), ("og:site_name", "property"),
                           ("og:type", "property"), ("og:locale", "property"),
                           ("twitter:card", "name")):
            if f'{kind}="{prop}"' not in doc:
                sys.exit(f"FEHLER: {f} hat weiterhin kein {prop}")
        m_html = re.search(r"<html\b[^>]*>", doc, re.I)
        if not m_html or not re.search(rf'\blang="{re.escape(args.lang)}"',
                                       m_html.group(0), re.I):
            sys.exit(f'FEHLER: {f} führt weiterhin nicht lang="{args.lang}"')
        if MARKER_LANG not in doc:
            sys.exit(f"FEHLER: {f} hat keinen Sprach-Wächter -- die Hydration setzt lang"
                     ' wieder auf "en"')
        # Die Karte: gegen die Datei geprüft, nicht gegen das, was dieser Lauf gerechnet
        # hat. Eine zu kleine Karte ist der Fehler, dessentwegen es social_card.py gibt.
        m_karte = re.search(r'<meta property="og:image" content="([^"]+)"', doc)
        if not m_karte:
            sys.exit(f"FEHLER: {f} hat weiterhin kein og:image")
        if not m_karte.group(1).endswith(karte):
            ok, warum = card_ok(card_file(root, m_karte.group(1)))
            if not ok:
                sys.exit(f"FEHLER: {f} trägt weiterhin eine Abbildung als Karte: {warum}")
        m_generisch = re.search(r'<meta name="image" content="([^"]+)"', doc)
        if m_generisch and m_generisch.group(1) != m_karte.group(1):
            sys.exit(f"FEHLER: {f} nennt in og:image und name=image verschiedene Bilder")
        # Ein lazy gemachtes Bild, das noch ein Preload trägt, hebt sich selbst auf.
        m = re.search(r"<main\b[^>]*>.*?</main>", doc, re.S | re.I)
        if not m:
            continue
        lazy_urls = {
            s.group(1)
            for tag in re.findall(r'<img\b[^>]*\bloading="lazy"[^>]*>', m.group(0), re.I)
            if (s := re.search(r'\bsrc="([^"]*)"', tag))
        }
        for tag in re.findall(r'<link\b[^>]*rel="preload"[^>]*>', doc, re.I):
            if 'as="image"' not in tag:
                continue
            href = re.search(r'\bhref="([^"]*)"', tag)
            if href and href.group(1) in lazy_urls:
                sys.exit(f"FEHLER: {f} lädt ein lazy-Bild weiterhin vor: {href.group(1)}")

    print(f"head_meta: {len(seiten)} Seiten, fünf Karten-Tags auf allen "
          f"({n_head} ergänzt), lang=\"{args.lang}\" auf allen ({n_lang} gesetzt, "
          f"{n_guard} Wächter), {n_karten} zu kleine Abbildungen durch {karte} ersetzt, "
          f"{n_lazy} Abbildungen lazy, {n_preload} Bild-Preloads entfernt")


if __name__ == "__main__":
    main()
