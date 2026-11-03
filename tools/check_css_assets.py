#!/usr/bin/env python3
"""Pruefen, dass jede url() der eingebundenen Stylesheets im Artefakt existiert.

    python3 tools/check_css_assets.py <html-dir> [--base BASE_URL]

Warum es dieses Skript gibt
---------------------------

Am 2026-10-16 lief die deutsche Ausgabe mit der Systemschrift, waehrend die englische
Inter zeigte. Aufgefallen ist das Konrad im Vergleich der zwei Seiten, nicht einer
Pruefung -- und die Pipeline war gruen.

Die Ursache: `custom-style.css` deklarierte `src: url('../fonts/inter-latin.woff2')`.
MyST legt dieses Stylesheet **zweimal** ab,

    /myst-theme.css                        <- das bindet das HTML ein
    /build/custom-style-<hash>.css         <- fingerprinted, wird nie geladen

und von der Kopie im Wurzelpfad zeigte `../fonts/` eine Ebene *ueber* `/ds-skript/`,
also auf den Server-Root. Antwort: 302, keine Schrift, stiller Rueckfall auf die
Systemschrift. Fuer zwei Ablageorte kann kein relativer Pfad richtig sein.

Meine erste Pruefung hatte den Pfad gegen die *fingerprinted* Kopie aufgeloest und
"DA" gemeldet. Sie hat damit die richtige Frage an der falschen Datei gestellt. Dieses
Skript stellt sie an der Datei, die im `<link>` steht -- das ist der ganze Unterschied,
und es ist der Unterschied zwischen gruen und richtig.

Zweiter Nutzen: KaTeX nennt seine zwanzig woff2 relativ zu seinem eigenen Stylesheet
(`_site/vendor/PROVENANCE.txt`). Auch das prueft dieses Skript, ohne davon zu wissen --
es faellt unter dieselbe Regel.


Pro @font-face genuegt EINE aufloesbare Quelle
----------------------------------------------

Ein `@font-face` nennt vier oder fuenf Formate je Schnitt, und `_site/vendor/` vendoriert
absichtlich nur das woff2 (Begruendung dort). Jede einzelne url() zu verlangen hiesse,
Absicht zu beanstanden -- ein Waechter, der nicht zu befriedigen ist, und den lernt man
zu ignorieren. Gefordert ist deshalb, was der Browser braucht: **mindestens eine** Quelle
je @font-face muss da sein. Fehlt die *letzte*, faellt der Schnitt aus, und genau das
schlaegt an.

url() ausserhalb eines @font-face -- Hintergrundbilder etwa -- muss einzeln aufloesen,
dort gibt es keine Alternative.

Query und Fragment werden vor dem Aufloesen abgeschnitten: Font Awesome haengt
`?v=4.7.0` und `#iefix` an, das ist Teil der URL und nicht des Dateinamens.


Was es nicht prueft
-------------------

Absolute URLs auf andere Hosts werden uebersprungen; ob ein Dritter erreichbar ist,
ist nicht die Frage dieses Skripts (und der Waechter im pages-Job verbietet die drei
CDN-Stylesheets ohnehin). `data:`-URIs ebenso.

Es prueft Existenz, nicht Inhalt. Eine Schrift, die da ist und die falschen Glyphen
hat, faellt hier nicht auf; dafuer sind die Pruefsummen in PROVENANCE.txt da.
"""

from __future__ import annotations

import argparse
import pathlib
import posixpath
import re
import sys

LINK = re.compile(r'<link\b[^>]*rel="stylesheet"[^>]*>', re.I)
HREF = re.compile(r'\bhref="([^"]*)"', re.I)
URL = re.compile(r"url\(\s*['\"]?([^)'\"]+)['\"]?\s*\)")
FONTFACE = re.compile(r"@font-face\s*\{[^}]*\}", re.I)


def artifact_path(root: pathlib.Path, url: str, base: str) -> pathlib.Path | None:
    """Wurzelabsolute Site-URL -> Pfad im Artefakt, oder None wenn ausserhalb.

    Liegt BASE_URL vor und faellt die URL nicht darunter, ist sie **ausserhalb dieser
    Ausgabe** -- auf dem Server etwas anderes, nicht dieselbe Datei eine Ebene hoeher.
    Das ist der Unterschied, an dem der Fehler vom 2026-10-16 hing: "../fonts/" von
    /ds-skript/myst-theme.css aus ergibt /fonts/, und das ist der Server-Root.

    Die erste Fassung dieser Funktion hat genau das verwechselt -- sie schnitt das
    fuehrende "/" ab und fand die Datei unter public/fonts/, obwohl der Browser sie dort
    nie suchen wuerde. Damit war der Pruefer gruen fuer exakt den Fehler, fuer den er
    geschrieben wurde. Nachgestellt, bevor er in die CI ging.
    """
    if base:
        if url == base:
            url = "/"
        elif url.startswith(base + "/"):
            url = url[len(base):]
        else:
            return None          # ausserhalb dieser Ausgabe
    if not url.startswith("/"):
        return None
    return root / url.lstrip("/")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("html_dir")
    ap.add_argument("--base", default="", help="BASE_URL, der Pfad, unter dem die Seite liegt")
    args = ap.parse_args()

    root = pathlib.Path(args.html_dir)
    base = args.base.rstrip("/")
    index = root / "index.html"
    if not index.exists():
        sys.exit(f"FEHLER: {index} existiert nicht; nach dem HTML-Bau laufen lassen")

    # Welche Stylesheets bindet das HTML ein? Genau die zaehlen.
    hrefs: set[str] = set()
    for page in root.rglob("index.html"):
        doc = page.read_text(encoding="utf-8", errors="replace")
        for tag in LINK.findall(doc):
            m = HREF.search(tag)
            if m:
                hrefs.add(m.group(1))

    extern = sorted(h for h in hrefs if h.startswith(("http://", "https://", "//")))
    lokal = sorted(h for h in hrefs if h not in extern)
    if not lokal:
        sys.exit("FEHLER: keine eingebundenen Stylesheets gefunden; hat das Theme sein Markup geaendert?")

    fehler: list[str] = []
    geprueft = 0

    for href in lokal:
        css = artifact_path(root, href, base)
        if css is None:
            fehler.append(f"{href}: kein wurzelabsoluter Pfad, nicht aufloesbar")
            continue
        if not css.is_file():
            fehler.append(f"{href}: eingebunden, liegt aber nicht im Artefakt ({css})")
            continue
        text = css.read_text(encoding="utf-8", errors="replace")

        if "__BASE__" in text:
            fehler.append(
                f"{href}: enthaelt noch den Platzhalter __BASE__ -- der pages-Job hat ihn "
                "nicht ersetzt, die Schriften wuerden auf eine wortwoertliche URL zeigen"
            )

        def loest_auf(ref: str) -> tuple[bool, str]:
            """Relativ zur URL *dieses* Stylesheets aufloesen, so wie der Browser es tut."""
            # Query und Fragment gehoeren zur URL, nicht zum Dateinamen (?v=4.7.0, #iefix).
            pfad = ref.split("?", 1)[0].split("#", 1)[0]
            ziel_url = posixpath.normpath(posixpath.join(posixpath.dirname(href), pfad))
            ziel = artifact_path(root, ziel_url, base)
            return (ziel is not None and ziel.is_file()), ziel_url

        # Erst die @font-face-Bloecke: je Block genuegt eine Quelle.
        schnitte = 0
        for block in FONTFACE.findall(text):
            refs = [r for r in URL.findall(block)
                    if not r.startswith(("http://", "https://", "//", "data:"))]
            if not refs:
                continue
            schnitte += 1
            geprueft += len(refs)
            treffer = [loest_auf(r) for r in refs]
            if not any(ok for ok, _ in treffer):
                fam = re.search(r"font-family:\s*['\"]?([^;'\"]+)", block)
                fehler.append(
                    f"{href}: @font-face {fam.group(1).strip() if fam else '?'} hat keine "
                    f"einzige aufloesbare Quelle ({', '.join(u for _, u in treffer)})"
                )

        # Und alles ausserhalb: dort gibt es keine Alternative, jede muss stimmen.
        ausserhalb = URL.findall(FONTFACE.sub("", text))
        for ref in sorted(set(ausserhalb)):
            if ref.startswith(("http://", "https://", "//", "data:")):
                continue
            geprueft += 1
            ok, ziel_url = loest_auf(ref)
            if not ok:
                fehler.append(
                    f"{href}: url({ref}) zeigt auf {ziel_url}, das liegt nicht im Artefakt"
                )

    if fehler:
        print("FEHLER: Stylesheets verweisen auf Dateien, die nicht ausgeliefert werden:")
        for f in fehler:
            print(f"  {f}")
        print(
            "\n  Erinnerung: MyST legt custom-style.css zweimal ab, und das HTML bindet die\n"
            "  Kopie im Wurzelpfad ein. Ein relativer url() ist deshalb falsch; __BASE__\n"
            "  plus die Ersetzung im pages-Job ist der Weg."
        )
        sys.exit(1)

    print(
        f"✓ {len(lokal)} eingebundene Stylesheets, {geprueft} url()-Verweise geprueft, "
        f"jeder Schnitt mit mindestens einer vorhandenen Quelle"
        + (f"; {len(extern)} externe uebersprungen" if extern else "")
    )


if __name__ == "__main__":
    main()
