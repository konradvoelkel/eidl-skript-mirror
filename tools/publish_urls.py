#!/usr/bin/env python3
"""Die echte Adresse in den Bau schreiben: Sitemap, robots.txt, og:image, Canonical.

    python3 tools/publish_urls.py <site-url> <html-verzeichnis> [--base BASE_URL]
    python3 tools/publish_urls.py <site-url> <html-verzeichnis> --check

Vier Umschreibungen und eine Prüfung, die alle davon leben, dass MyST die Adresse der
Seite beim Bauen nicht kennt.


1. Die Sitemap zeigte auf `localhost`. Alle 30 Einträge -- und 60 Dateien mehr
--------------------------------------------------------------------------------

    sitemap.xml:  <loc>http://localhost:3000/transformer</loc>   ... 30 Einträge
    sitemap.xml:  <?xml-stylesheet href="http://localhost:3000/sitemap_style.xsl" ?>
    robots.txt:   Sitemap: http://localhost:3000/sitemap.xml
    index.html:   "domain":"http://localhost:3000"   ... je Seite einmal
    <slug>.json:  dasselbe                            ... je Seite einmal

MyST holt `robots.txt` und `sitemap.xml` beim statischen Bau vom **eigenen Dev-Server**
und schreibt dessen Origin hinein. MyST 1.11 hat keine Einstellung für die echte Origin
-- `BASE_URL` setzt nur den Pfad. Die Seite reichte Crawlern also eine Sitemap, in der
jede URL ins Leere zeigt, und eine robots.txt, die eine Maschine nennt, die es nicht
gibt. Derselbe Fehler, den ds-en im Oktober 2026 behoben hat (dort `SEO-NOTES.md` §2)
und den die beiden deutschen Ausgaben seither mitschleppten.

**Der dritte Fundort ist neu und stammt aus dem Schwesterrepo `eipy-skript`**
(2026-10-19): MyST schreibt die Origin seines Dev-Servers auch als `"domain"` in die
Hydrations-Nutzlast jeder `index.html` **und** in die `<slug>.json` daneben -- hier
zusammen 60 Dateien. ds-skript und ds-en ersetzen nur in sitemap.xml und robots.txt und
liefern diese Zeichenkette vermutlich bis heute aus. Deshalb ersetzt dieses Skript in
allen vier Dateiarten, und `--check` sucht `localhost` im **ganzen** Verzeichnis, nicht
nur in den zwei Dateien, an die man zuerst denkt.

2. Jede `<loc>` auf die URL, die wirklich 200 liefert
------------------------------------------------------

GitLab Pages beantwortet `/transformer` mit einer Weiterleitung auf `/transformer/`;
MyST schreibt die Form ohne Schrägstrich. Eine Sitemap voller Weiterleitungen ist eine
nachprüfbare Behauptung, die nicht stimmt, also wird der Schrägstrich ergänzt --
dieselbe Form, die der Canonical unten bekommt.

3. `og:image` absolut
----------------------

MyST schreibt es wurzelrelativ (`/build/social-card-<hash>.png`). OpenGraph verlangt
eine absolute URL: Slack, LinkedIn, Mastodon und WhatsApp können eine wurzelrelative
nicht auflösen, die Vorschaukarte bleibt leer. `name="image"` wird mitgenommen, es trägt
denselben Wert.

4. `rel="canonical"`
---------------------

MyST emittiert keinen. Hier zählt er doppelt: Derselbe Text erscheint auch als PDF, und
die Seite ist unter **zwei** Hostnamen erreichbar -- `voelkel.pages.cs.uni-duesseldorf.de
/eidl-skript/` antwortet mit 308 auf `eidl-skript-131e30.pages.cs.uni-duesseldorf.de`
(am 2026-10-19 gemessen). Ohne Canonical entscheidet die Suchmaschine selbst, welche der
beiden Schreibweisen sie indexiert. Deshalb steht in jeder Seite die Zieladresse, die
200 liefert, mit Schrägstrich.


Warum ein Skript und nicht fünf `sed` in der CI
------------------------------------------------

In ds-skript und ds-en stehen genau diese Schritte als `sed`-Zeilen im Deploy-Job. Hier
sind sie ein Skript, aus zwei Gründen, die beide in CLAUDE.md stehen: Was nur in der CI
läuft, kann lokal nicht geprüft werden -- „lokal grün" und „veröffentlicht" sind zwei
verschiedene Aussagen --, und die Prüfungen gehören an dieselbe Stelle wie die
Änderungen, damit niemand die eine ohne die andere kopiert. Die Umschreibungen sind
dieselben; `--check` ist die Gegenprobe und läuft in der CI noch einmal am fertigen
Artefakt.


Zweimal laufen
--------------

Idempotent: Eine Seite, die schon einen Canonical trägt, bekommt keinen zweiten, eine
schon absolute URL wird nicht noch einmal präfigiert, und `localhost` findet sich beim
zweiten Lauf nicht mehr. `--check` prüft Nachbedingungen am Artefakt, nicht die Bilanz
eines Laufs: Jede Seite trägt genau einen Canonical, die Menge der Sitemap-Einträge ist
genau die Menge der gebauten Seiten, keine URL ist relativ und nirgends steht noch
`localhost`.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

LOCALHOST = "http://localhost:3000"


def seiten(root: Path) -> list[Path]:
    return sorted(root.rglob("index.html"))


def seiten_url(site: str, root: Path, f: Path) -> str:
    """Die URL, die 200 liefert: mit Schrägstrich."""
    rel = f.parent.relative_to(root)
    return f"{site}/" if str(rel) == "." else f"{site}/{rel}/"


def origin_eintragen(root: Path, site: str) -> tuple[int, int]:
    """`localhost:3000` durch die echte Adresse ersetzen -- in jeder Datei, die sie trägt.

    sitemap.xml und robots.txt sind die bekannten zwei; `"domain"` in jeder index.html
    und jeder <slug>.json sind die anderen sechzig (siehe Abschnitt 1).
    """
    for name in ("sitemap.xml", "robots.txt"):
        if not (root / name).exists():
            sys.exit(f"FEHLER: {root / name} fehlt; hat `myst build --html` sie erzeugt?")
    dateien = [root / "sitemap.xml", root / "robots.txt",
               *root.rglob("*.html"), *root.rglob("*.json")]
    n = getroffen = 0
    for f in dateien:
        text = f.read_text(encoding="utf-8")
        if LOCALHOST not in text:
            continue
        n += text.count(LOCALHOST)
        getroffen += 1
        f.write_text(text.replace(LOCALHOST, site), encoding="utf-8")
    return n, getroffen


def loc_schraegstrich(root: Path, site: str) -> int:
    """Jeder `<loc>` die Form geben, die 200 liefert."""
    f = root / "sitemap.xml"
    text = f.read_text(encoding="utf-8")

    def sub(m: re.Match) -> str:
        url = m.group(1)
        return f"<loc>{url if url.endswith('/') else url + '/'}</loc>"

    neu, _ = re.subn(r"<loc>([^<]*)</loc>", sub, text)
    f.write_text(neu, encoding="utf-8")
    # Gezählt wird, was ergänzt *wurde* -- also am alten Text, nicht am neuen.
    return sum(1 for u in re.findall(r"<loc>([^<]*)</loc>", text) if not u.endswith("/"))


def bilder_absolut(doc: str, site: str, base: str) -> tuple[str, int]:
    """`og:image` und `name="image"` auf eine absolute URL bringen."""
    praefix = f'content="{base}/build/'
    n = doc.count(praefix)
    return doc.replace(praefix, f'content="{site}/build/'), n


def canonical(doc: str, url: str) -> tuple[str, bool]:
    if 'rel="canonical"' in doc:
        return doc, False
    if "</head>" not in doc:
        sys.exit(f"FEHLER: eine Seite hat kein </head>: {url}")
    return doc.replace("</head>", f'<link rel="canonical" href="{url}"/></head>', 1), True


def pruefen(site: str, root: Path) -> int:
    fehler: list[str] = []
    sitemap = (root / "sitemap.xml").read_text(encoding="utf-8")
    robots = (root / "robots.txt").read_text(encoding="utf-8")

    # Im ganzen Verzeichnis, nicht nur in den zwei Dateien, an die man zuerst denkt.
    for f in sorted([*root.rglob("*.html"), *root.rglob("*.json"),
                     root / "sitemap.xml", root / "robots.txt"]):
        if "localhost:3000" in f.read_text(encoding="utf-8"):
            fehler.append(f"{f.relative_to(root)}: enthält weiterhin eine localhost-URL")

    locs = set(re.findall(r"<loc>([^<]*)</loc>", sitemap))
    for u in sorted(locs):
        if not u.startswith(site + "/"):
            fehler.append(f"sitemap.xml: <loc>{u}</loc> steht nicht unter {site}/")
        elif not u.endswith("/"):
            fehler.append(f"sitemap.xml: <loc>{u}</loc> ohne Schrägstrich -- "
                          "darauf antwortet Pages mit einer Weiterleitung")

    gebaut = {seiten_url(site, root, f) for f in seiten(root)}
    if locs != gebaut:
        for u in sorted(locs - gebaut):
            fehler.append(f"sitemap.xml nennt {u}, dazu gibt es keine gebaute Seite")
        for u in sorted(gebaut - locs):
            fehler.append(f"{u} ist gebaut, steht aber nicht in der Sitemap")

    if f"Sitemap: {site}/sitemap.xml" not in robots:
        fehler.append(f"robots.txt nennt nicht `Sitemap: {site}/sitemap.xml`")

    for f in seiten(root):
        doc = f.read_text(encoding="utf-8")
        url = seiten_url(site, root, f)
        gefunden = re.findall(r'<link rel="canonical" href="([^"]*)"', doc)
        if len(gefunden) != 1:
            fehler.append(f"{f}: {len(gefunden)} Canonicals, erwartet genau einen")
        elif gefunden[0] != url:
            fehler.append(f"{f}: Canonical {gefunden[0]}, erwartet {url}")
        for kind, name in (("property", "og:image"), ("name", "image")):
            for wert in re.findall(rf'<meta {kind}="{name}" content="([^"]*)"', doc):
                if not wert.startswith("http"):
                    fehler.append(f"{f}: {name} ist weiterhin relativ: {wert}")

    if fehler:
        for z in fehler[:40]:
            print(f"✗ {z}")
        if len(fehler) > 40:
            print(f"  ... und {len(fehler) - 40} weitere")
        return 1
    print(f"✓ {len(seiten(root))} Seiten, je ein Canonical, "
          f"{len(locs)} Sitemap-Einträge (dieselbe Menge), alle Bild-URLs absolut, "
          f"kein localhost")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("site")
    ap.add_argument("html_dir")
    ap.add_argument("--base", default="", help="BASE_URL, der Pfad unter der Origin")
    ap.add_argument("--check", action="store_true", help="nur prüfen, nichts ändern")
    args = ap.parse_args()

    site = args.site.rstrip("/")
    root = Path(args.html_dir)
    if not (root / "index.html").exists():
        sys.exit(f"FEHLER: {root / 'index.html'} fehlt; nach dem HTML-Bau laufen lassen")
    if args.check:
        return pruefen(site, root)

    n_origin, n_dateien = origin_eintragen(root, site)
    n_slash = loc_schraegstrich(root, site)

    n_bilder = n_canonical = 0
    for f in seiten(root):
        doc = f.read_text(encoding="utf-8")
        doc, n = bilder_absolut(doc, site, args.base)
        n_bilder += n
        doc, gesetzt = canonical(doc, seiten_url(site, root, f))
        n_canonical += gesetzt
        f.write_text(doc, encoding="utf-8")

    print(f"publish_urls: {n_origin}x localhost in {n_dateien} Dateien ersetzt, "
          f"{n_slash} <loc> mit "
          f"Schrägstrich ergänzt, {n_bilder} Bild-URLs absolut gemacht, "
          f"{n_canonical} Canonicals gesetzt")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
