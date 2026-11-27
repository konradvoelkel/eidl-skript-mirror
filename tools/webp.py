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

Zwei Größen, und warum das hier doch ohne Patch geht (2026-11-17, Audit §3)
---------------------------------------------------------------------------
Lighthouse meldet, dass drei Abbildungen größer ausgeliefert werden, als sie dargestellt
werden -- `vl10-blur-edges` 92,6 kB, davon 72,4 kB einsparbar. Die Dateien sind rund
1300 px breit, das Satzfeld ist 644 px: Auf einem Bildschirm ohne Retina-Auflösung lädt
der Browser doppelt so viele Pixel, wie er zeigt.

`devnotes/make_webp.py` legt deshalb neben jede Fassung eine halb so breite (`…@1x.webp`),
und dieses Skript bietet beide als `srcset` an -- mit `1x`/`2x` statt mit `w`-Deskriptoren:
Die kleine Datei *ist* genau die halbe Breite, also sagt `1x`/`2x` die Wahrheit, und der
Browser braucht kein `sizes`.

**Das Theme kann `<picture>` von sich aus**, und das ist der Grund, warum hier kein
Bündel-Patch nötig ist: Trägt ein Bildknoten der Nutzlast das Feld `urlOptimized`, rendert
es `<picture><source srcSet={urlOptimized} type="image/webp"><img src={url}></picture>`.
Geschrieben wird deshalb **beides**: das `<picture>` ins Markup (sonst lädt der erste
Anlauf die große Datei) und `urlOptimized` in die Nutzlast (sonst baut React nach der
Hydration wieder ein nacktes `<img>` -- und der Browser holt die große Datei ein zweites
Mal). Zusammen ist das, was vor und nach der Hydration dasselbe Bild lädt.

Und das Preload dazu (2026-11-26, `devnotes/seo-pruefung-2026-11-26.md` §3)
---------------------------------------------------------------------------
Das `<picture>` allein reichte nicht. `head_meta.py` läßt für die erste Abbildung ein
`<link rel="preload" as="image">` stehen, weil sie das LCP-Element ist — und das nennt
weiter die große Datei. Auf einem Bildschirm ohne Retina-Auflösung holt der Vorab-Scanner
deshalb die 2x-Fassung und der Browser danach die 1x des `<picture>` dazu: 19 der 33
Seiten luden ihr erstes Bild zweimal, zusammen 563 kB umsonst. `preload_srcset` gibt dem
Preload dasselbe `srcset` als `imagesrcset` mit; `--check` schlägt an, wenn ein
Bild-Preload ohne `imagesrcset` auf eine Datei zeigt, die daneben als 2x angeboten wird.

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
import artefakt
import turbostream

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


def halb(p: pathlib.Path) -> pathlib.Path:
    """Aus `x.webp` wird `x@1x.webp` -- dieselbe Regel wie in `devnotes/make_webp.py`."""
    return p.with_name(p.stem + "@1x.webp")


def paare(html: pathlib.Path, index: dict[str, pathlib.Path]) -> list[tuple[pathlib.Path, pathlib.Path]]:
    """(Bilddatei im Artefakt, WebP-Quelle) für alles, was ausgetauscht werden kann."""
    dateien = artefakt.pfad(html)
    if not dateien.is_dir():
        sys.exit(f"FEHLER: {dateien} gibt es nicht -- nach dem HTML-Bau laufen lassen")
    out = []
    for p in sorted(dateien.iterdir()):
        if p.suffix.lower() not in ENDUNGEN:
            continue
        webp = index.get(sha(p))
        if webp is not None:
            out.append((p, webp))
    return out


IMG = re.compile(r"<img\b[^>]*?/?>")


def markup_picture(text: str, srcset: dict[str, str]) -> tuple[str, int, set[str]]:
    """Jede Abbildung mit zwei Fassungen in ein `<picture>` fassen.

    Gebaut wird genau das, was das Theme aus `urlOptimized` rendert -- die Klasse wandert
    an das `<picture>`, das `<img>` behaelt `src`, Maße und `loading`. Steht im Markup
    etwas anderes als im gerenderten DOM, laedt der Browser zwei Dateien statt einer.
    """
    n = 0
    benutzt: set[str] = set()

    def ein(m: re.Match[str]) -> str:
        nonlocal n
        tag = m.group(0)
        q = re.search(r'\ssrc="([^"]+)"', tag)
        if q is None or q.group(1) not in srcset:
            return tag
        kl = re.search(r'\sclass="([^"]*)"', tag)
        klasse = kl.group(1) if kl else ""
        ohne = tag.replace(kl.group(0), "") if kl else tag
        n += 1
        benutzt.add(q.group(1))
        return (f'<picture class="{klasse}"><source srcset="{srcset[q.group(1)]}" '
                f'type="image/webp"/>{ohne}</picture>')

    if 'type="image/webp"' in text:   # schon gelaufen -- nicht doppelt einpacken
        return text, 0, benutzt
    return IMG.sub(ein, text), n, benutzt


PRELOAD = re.compile(r'<link\b[^>]*?\brel="preload"[^>]*?/?>', re.I)


def preload_srcset(text: str, srcset: dict[str, str]) -> tuple[str, int]:
    """Dem Bild-Preload dasselbe `srcset` geben wie dem `<source>` daneben.

    `head_meta.py` behält genau ein `<link rel="preload" as="image">`, nämlich das der
    ersten Abbildung, weil sie das LCP-Element ist. Bekommt dieselbe Abbildung hier ein
    `<picture>` mit zwei Größen, zeigen die beiden auf verschiedene Dateien: Der
    Vorab-Scanner holt wegen des Preloads die 2x-Fassung, und nach dem Layout wertet der
    Browser das `<picture>` aus und holt die 1x dazu. Am 2026-11-26 an der ausgelieferten
    Seite nachgemessen (`devnotes/seo-pruefung-2026-11-26.md` §3): 19 der 33 Seiten luden
    ihr erstes Bild zweimal, zusammen 563 kB, die niemand anzeigt -- und das ausgerechnet
    an der Stelle, die das LCP bestimmt.

    `imagesrcset` bekommt denselben Wert wie das `<source>`; `href` bleibt als Rückfall für
    Browser ohne `imagesrcset` (vor Safari 17.2 und Firefox 115). Ein `imagesizes` braucht
    es nicht: Die Deskriptoren sind `1x`/`2x`, nicht `w`.
    """
    n = 0

    def ein(m: re.Match[str]) -> str:
        nonlocal n
        tag = m.group(0)
        if 'as="image"' not in tag or "imagesrcset=" in tag:
            return tag
        q = re.search(r'\shref="([^"]+)"', tag)
        if q is None or q.group(1) not in srcset:
            return tag
        n += 1
        return tag[:q.start()] + f' imagesrcset="{srcset[q.group(1)]}"' + tag[q.start():]

    return PRELOAD.sub(ein, text), n


# Theme 2.x liefert die Nutzlast nicht als JSON-Objekt in `window.__remixContext`, sondern
# als Turbo-Stream (Aufbau und Werkzeug: `tools/turbostream.py`). Die Textersetzung unten
# greift darin nicht -- `"url"` und die Adresse stehen als zwei getrennte Einträge --, und
# ohne `urlOptimized` baut React nach der Hydration ein nacktes `<img>` auf die **große**
# Fassung. Gemessen am 2026-11-27 an `/faltung-cnn/`: zwei von fünf Abbildungen wurden
# dadurch zweimal geladen, klein und groß. Dieselbe Verschwendung wie der Preload-Befund
# vom 2026-11-26, nur von der anderen Seite.


def nutzlast_turbostream(text: str, srcset: dict[str, str]) -> tuple[str, int]:
    """`urlOptimized` in die Turbo-Stream-Nutzlast eintragen, je Bildknoten."""

    def tragen(daten: list) -> int:
        cache: dict[str, int] = {}
        n = 0
        for knoten, url in turbostream.bildknoten(daten):
            if url not in srcset:
                continue
            if turbostream.hole(daten, knoten, "urlOptimized") is not None:
                continue
            turbostream.setze(daten, knoten, "urlOptimized", srcset[url], cache)
            n += 1
        return n

    return turbostream.bearbeiten(text, tragen)


def zwei_groessen(html: pathlib.Path, srcset: dict[str, str]) -> tuple[int, int, int, set[str]]:
    """`urlOptimized` in die Nutzlast, `<picture>` ins Markup -- beides, siehe Kopf.

    Gibt zusätzlich zurück, welche Adressen wirklich vorkommen: mystmd legt jede Abbildung
    mehrfach unter verschiedenen Hashnamen im Dateiordner ab (527 Dateien für 61
    Abbildungen),
    verwiesen wird aber nur auf eine davon. Kopiert wird die halbe Fassung deshalb nur für
    die verwiesenen -- sonst lägen 390 Dateien im Artefakt, die niemand abruft.
    """
    n_bild = n_markup = n_preload = 0
    benutzt: set[str] = set()
    for muster in TEXTDATEIEN:
        for p in html.rglob(muster):
            text = p.read_text(encoding="utf-8")
            neu = text
            for url, satz in srcset.items():
                feld = f'"url":"{url}"'
                muster_url = re.escape(feld) + r'(?!,"urlOptimized")'
                neu, k = re.subn(muster_url, feld + f',"urlOptimized":"{satz}"', neu)
                n_bild += k
                if k:
                    benutzt.add(url)
            if p.suffix == ".html":
                neu, k = nutzlast_turbostream(neu, srcset)
                n_bild += k
                neu, k, k_url = markup_picture(neu, srcset)
                n_markup += k
                benutzt |= k_url
                neu, k = preload_srcset(neu, srcset)
                n_preload += k
            if neu != text:
                p.write_text(neu, encoding="utf-8")
    return n_bild, n_markup, n_preload, benutzt


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
        # Jede Adresse, die ein `srcset` nennt, muß auch im Artefakt liegen: ein
        # `srcset` auf eine fehlende Datei fällt im Browser still auf das `<img>` zurück.
        opt = pic = 0
        genannt: set[str] = set()
        for f in args.html.rglob("*.html"):
            text = f.read_text(encoding="utf-8")
            # In der Turbo-Stream-Nutzlast steht der Schlüssel escapet
            # (`\"urlOptimized\"`), in den Seiten-JSON wörtlich.
            opt += text.count('"urlOptimized"') + text.count('\\"urlOptimized\\"')
            pic += text.count('type="image/webp"')
            genannt |= set(re.findall(rf"{artefakt.praefix(args.html)}"
                                      r"([\w.@-]+@1x\.webp)", text))
            # Ein Preload ohne `imagesrcset` auf eine Datei, die daneben in einem
            # `srcset` als 2x steht, laedt die zweite Fassung dazu -- Befund 2026-11-26.
            zwei_x = {t.strip().split()[0]
                      for satz in re.findall(r'\ssrcset="([^"]+)"', text)
                      for t in satz.split(",")
                      if t.strip().endswith(" 2x")}
            for tag in PRELOAD.findall(text):
                if 'as="image"' not in tag or "imagesrcset=" in tag:
                    continue
                q = re.search(r'\shref="([^"]+)"', tag)
                if q is not None and q.group(1) in zwei_x:
                    print(f"✗ {f.relative_to(args.html)}: Preload auf {q.group(1)} ohne "
                          f"imagesrcset, daneben steht ein <source> mit zwei Größen")
                    fehler += 1
        for name in sorted(genannt):
            if not (artefakt.pfad(args.html) / name).is_file():
                print(f"✗ {name}: srcset nennt eine Datei, die nicht im Artefakt liegt")
                fehler += 1
        if any(halb(webp).is_file() for _, webp in gefunden) and not (opt and pic and genannt):
            print(f"✗ zwei Größen nicht eingetragen: {opt}x urlOptimized, {pic}x <source>")
            fehler += 1
        if fehler:
            return 1
        gespart = sum(p.stat().st_size - p.with_suffix(".webp").stat().st_size for p, _ in gefunden)
        print(f"✓ {len(gefunden)} Abbildungen als WebP ausgeliefert, "
              f"{gespart / 1024 / 1024:.2f} MB weniger als PNG/JPG; "
              f"{len(genannt)} in zwei Größen ({opt}x urlOptimized, {pic}x <source> im Markup)")
        return 0

    srcset: dict[str, str] = {}
    quelle_halb: dict[str, tuple[pathlib.Path, pathlib.Path]] = {}
    for p, webp in gefunden:
        shutil.copy2(webp, p.with_suffix(".webp"))
        klein = halb(webp)
        if klein.is_file():
            vor = artefakt.praefix(args.html)
            gross_url = vor + p.with_suffix(".webp").name
            klein_url = vor + halb(p.with_suffix(".webp")).name
            srcset[gross_url] = f"{klein_url} 1x, {gross_url} 2x"
            quelle_halb[gross_url] = (klein, halb(p.with_suffix(".webp")))
    dateien, treffer = ersetzen(args.html, karte)
    n_bild, n_markup, n_preload, benutzt = zwei_groessen(args.html, srcset)
    for url in sorted(benutzt):
        klein, ziel = quelle_halb[url]
        shutil.copy2(klein, ziel)
    gespart = sum(p.stat().st_size - p.with_suffix(".webp").stat().st_size for p, _ in gefunden)
    print(f"✓ {len(gefunden)} Abbildungen als WebP daneben gelegt, {treffer} Verweise in "
          f"{dateien} Dateien umgeschrieben, {gespart / 1024 / 1024:.2f} MB weniger; "
          f"{len(benutzt)} davon in zwei Größen ({n_bild} Knoten der Nutzlast, "
          f"{n_markup} <picture> im Markup, {n_preload} Preloads mit imagesrcset)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
