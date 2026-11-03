#!/usr/bin/env python3
"""Interne Kapitellinks auf die URL bringen, die 200 liefert -- mit Schraegstrich.

    python3 tools/trailing_slash.py <html-verzeichnis> [--base BASE_URL]
    python3 tools/trailing_slash.py --check <html-verzeichnis> [--base BASE_URL]

Im `pages`-Job nach `outline_reserve.py` laufen lassen. Port aus ds-skript
(2026-10-29); dessen Messungen und Pfade (`/ds-skript/kmeans`) stehen unten unveraendert.
Fuer eidl angepasst: `--base` darf leer sein, denn die Seite liegt an der Wurzel ihres
Hosts. Ein `hydration.py` gibt es hier nicht (die Hydration gelingt, siehe
`image_dims.py`); wo unten davon die Rede ist, ist ds-skript gemeint.

Warum es dieses Skript gibt
---------------------------

MyST verlinkt Kapitel ohne Schraegstrich (`/ds-skript/kmeans`), GitLab Pages antwortet
darauf mit **302** auf `/ds-skript/kmeans/`. Canonical und Sitemap nennen seit `d929f14`
die Form mit Schraegstrich; die Links taten es nicht. Kein Dubletten-Problem, nur ein
Round-Trip, den jeder Zugriff ohne JavaScript und jeder Crawler bezahlt.

Am 2026-10-29 gemessen, fuenf Durchlaeufe auf derselben Verbindung
(`curl -L -w %{time_total}`, `num_connects` bleibt 1):

| Form | Median |
|---|---|
| `/ds-skript/kmeans` (302 dann 200) | 0,254 s |
| `/ds-skript/kmeans/` (200) | 0,214 s |

Also rund **40 ms** je Link, und die Weiterleitung schickt `location:
//voelkel.pages.cs.uni-duesseldorf.de/...` -- protokollrelativ, was GitLab Pages so
ausliefert und hier nichts aendert.

Markup allein reicht nicht, Nutzlast allein auch nicht
------------------------------------------------------

Die Hydration schlaegt auf jeder Seite fehl (React #418, siehe `hydration.py`) und
rendert das ganze Dokument neu, `<main>` inbegriffen. Am 2026-10-29 mit einem Proxy
gemessen, der eine bearbeitete `/kmeans/` ausliefert und alles andere vom Live-Server
holt, je Variante im Browser 7 s nach dem Laden nachgesehen:

| Fixture | im DOM danach |
|---|---|
| nur Markup mit Schraegstrich | **ohne** -- das Neurendern holt den href aus der Nutzlast |
| nur Nutzlast mit Schraegstrich | mit |

Welches Feld welchen href ergibt, ist mit Marken gemessen statt gelesen: je Feld ein
`?marke=N` in die Nutzlast, dann im DOM gesucht. Alle drei Marken kamen an, und damit
steht fest, woraus das Theme die Links baut:

| href im DOM | Feld in der Nutzlast |
|---|---|
| Links im Artikel (`a.hover-link`, `a.link`) | mdast-Knoten `link.url` |
| Fusszeile vor/zurueck (`a.myst-footer-link`) | `page.footer.navigation.{prev,next}.url` |
| Seitenleiste | `config.projects[].pages[].slug` |

Geschrieben wird trotzdem beides. Das ausgelieferte Dokument ist, was ein Crawler ohne
JavaScript liest, und das ist derselbe Grund, aus dem `head_meta.py` sein
`loading="lazy"` setzt, obwohl die Hydration es wegwirft: die Ersparnis liegt in der Zeit
davor.

Die Seitenleiste bleibt, und das ist gemessen, nicht geschaetzt
--------------------------------------------------------------

Der Slug waere der Griff fuer die Seitenleiste -- das Theme baut daraus
`path = "/" + slug` und daraus den href. Ein Schraegstrich am Slug kommt auch im DOM an.
Er kostet aber zwei Dinge, beide in derselben Probe gesehen (93 Slugs in allen drei
Kopien der Konfiguration):

* **Die Vorschaukarten der Links im Artikel sind weg.** Das Theme sucht die Zielseite
  ueber `pages.find(s => s.slug === pfad)`, wobei `pfad` aus der Link-URL kommt und
  keinen Schraegstrich traegt. Findet es nichts, rendert es `a.link` statt
  `a.hover-link`: kein Titel, keine Beschreibung, kein Thumbnail beim Hovern. In der
  Probe fielen alle vier internen Links von `/kmeans/` aus `hover-link` heraus.
* **Die Gruppe der aktuellen Seite klappt nicht mehr auf.** Der Vergleich dort schneidet
  am Ort einen Schraegstrich ab und vergleicht mit `path`, der jetzt einen hat. Statt 11
  Eintraegen zeigte die Leiste 3.

Deshalb bleibt der Slug unberuehrt. Von den 502 hrefs im Artefakt tragen danach alle den
Schraegstrich, nach der Hydration aber nur die 285, die aus `link.url` und der Fusszeile
kommen; die Seitenleiste faellt zurueck. Das ist die Haelfte eines Fundes und nicht das
Ganze -- der Rest braucht einen Patch am Theme, nicht am Artefakt.

Die Seiten-JSON kommen mit, aus demselben Grund wie bei `hydration.py`: sie tragen
dieselben Felder (`link.url`, `footer.navigation`), und zwei Fassungen derselben Angabe
koennen nur auseinanderlaufen.

Was absichtlich unberuehrt bleibt
---------------------------------

Ergaenzt wird nur `<base>/<slug>` und nur fuer einen Slug aus der Kapitelliste. Am
Artefakt durchgespielt, alle sechs bleiben, wie sie sind:

| Probe | warum |
|---|---|
| `/ds-skript/nichtsda` | kein Kapitel -- ein Schraegstrich waere eine neue 302 |
| `/ds-skript/kmeans#abschnitt` | Fragment, die Seite liefert schon 200 |
| `/ds-skript/kmeans?x=1` | Query, dito |
| `/ds-skript/kmeans.md` | Datei, keine Seite |
| `https://.../ds-skript/kmeans` | absolut; davon gibt es im Artefakt null, gezaehlt |
| `/ds-skript/Kmeans` | Grossbuchstabe, also kein Slug |
"""

from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys

NUTZLAST = "window.__remixContext = "
# `href="` kann in der Nutzlast nicht vorkommen: JSON schreibt dort `href=\"`, mit
# Backslash. Deshalb darf der Ausdruck ueber das ganze Dokument laufen.
HREF = re.compile(r'(\bhref=")([^"]*)(")')


def seiten_slugs(root: pathlib.Path) -> set[str]:
    """Die Slugs aller Kapitel, aus `config.json` des gebauten Ordners.

    Dieselbe Quelle, aus der `head_meta.py` seinen `og:site_name` und
    `inject_jsonld.py` seine Kapitel liest. Mit der Liste ergaenzt dieses Skript nur
    Pfade, die wirklich eine Seite sind -- ein Schraegstrich an etwas anderem waere eine
    neue Weiterleitung statt einer gesparten.
    """
    cfg = root / "config.json"
    if not cfg.exists():
        sys.exit(f"FEHLER: {cfg} fehlt; ohne die Kapitelliste waere jeder Pfad geraten")
    try:
        pages = json.loads(cfg.read_text(encoding="utf-8"))["projects"][0]["pages"]
    except (ValueError, KeyError, IndexError, TypeError) as e:
        sys.exit(f"FEHLER: {cfg} hat kein projects[0].pages ({e})")
    slugs = {p["slug"] for p in pages if isinstance(p, dict) and isinstance(p.get("slug"), str)}
    if not slugs:
        sys.exit(f"FEHLER: {cfg} nennt keinen einzigen Slug")
    return slugs


def lies_nutzlast(doc: str):
    """Die Hydrations-Nutzlast als Objekt, mit Anfang und Ende im Dokument.

    `raw_decode` gibt den **absoluten Index** des JSON-Endes zurueck, nicht die Laenge.
    Wer ihn als Laenge liest, schneidet um `start` zu weit -- die Falle, die in ds-en
    jede Seite mitten in der Nutzlast abgeschnitten hat (siehe `hydration.py`).
    """
    i = doc.find(NUTZLAST)
    if i < 0:
        return None
    start = i + len(NUTZLAST)
    try:
        obj, ende = json.JSONDecoder().raw_decode(doc, start)
    except ValueError:
        return None
    return obj, start, ende


def js_literal(obj) -> str:
    """JSON als JavaScript-Literal innerhalb eines `<script>`.

    Ein nacktes `<` koennte das Tag frueh schliessen, und U+2028/U+2029 sind in JSON
    gewoehnliche Zeichen, in JavaScript aber Zeilenenden. Wie in `hydration.py`.
    """
    out = json.dumps(obj, separators=(",", ":"), ensure_ascii=False)
    return out.replace("<", "\\u003c").replace("\u2028", "\\u2028").replace("\u2029", "\\u2029")


def fehlt_schraegstrich(wert, slugs: set[str]) -> bool:
    """Ist das ein Kapitelpfad ohne Schraegstrich am Ende?

    Nur genau `/<slug>`: nichts mit Punkt (`.md`, `.json`, `.pdf`), nichts mit `?` oder
    `#`, nichts Absolutes, und nichts, was nicht in der Kapitelliste steht.
    """
    return isinstance(wert, str) and wert.startswith("/") and wert[1:] in slugs


def markup(doc: str, base: str, slugs: set[str]) -> tuple[str, int]:
    """Jeden Kapitel-href im Markup auf die Form mit Schraegstrich bringen."""
    n = 0

    def auf(m: re.Match[str]) -> str:
        nonlocal n
        ziel = m.group(2)
        if not ziel.startswith(base + "/"):
            return m.group(0)
        if not fehlt_schraegstrich(ziel[len(base) :], slugs):
            return m.group(0)
        n += 1
        return m.group(1) + ziel + "/" + m.group(3)

    return HREF.sub(auf, doc), n


def felder(obj, slugs: set[str]) -> tuple[int, int]:
    """Die beiden Felder, die das Neurendern ueberleben. Mutiert `obj`.

    Gibt (Links im Artikel, Eintraege der Fusszeile) zurueck. Der Slug wird mit Absicht
    nicht angefasst, siehe Docstring.
    """
    n_link = n_fuss = 0

    def lauf(o) -> None:
        nonlocal n_link, n_fuss
        if isinstance(o, dict):
            if o.get("type") == "link" and o.get("internal") and fehlt_schraegstrich(o.get("url"), slugs):
                o["url"] += "/"
                n_link += 1
            nav = o.get("navigation")
            if isinstance(nav, dict):
                for k in ("prev", "next"):
                    eintrag = nav.get(k)
                    if isinstance(eintrag, dict) and fehlt_schraegstrich(eintrag.get("url"), slugs):
                        eintrag["url"] += "/"
                        n_fuss += 1
            for v in o.values():
                lauf(v)
        elif isinstance(o, list):
            for v in o:
                lauf(v)

    lauf(obj)
    return n_link, n_fuss


def seite(f: pathlib.Path, base: str, slugs: set[str]) -> tuple[int, int, int]:
    """Eine Seite: Markup und Nutzlast. Gibt (hrefs, Links, Fusszeile) zurueck."""
    doc = f.read_text(encoding="utf-8")
    doc, n_href = markup(doc, base, slugs)
    gelesen = lies_nutzlast(doc)
    n_link = n_fuss = 0
    if gelesen:
        obj, start, ende = gelesen
        n_link, n_fuss = felder(obj, slugs)
        if n_link or n_fuss:
            doc = doc[:start] + js_literal(obj) + doc[ende:]
    elif NUTZLAST in doc:
        sys.exit(f"FEHLER: {f} hat keine lesbare Hydrations-Nutzlast")
    if n_href or n_link or n_fuss:
        f.write_text(doc, encoding="utf-8")
    return n_href, n_link, n_fuss


def seiten_json(f: pathlib.Path, slugs: set[str]) -> tuple[int, int]:
    """Dieselben Felder in MySTs Seiten-JSON.

    `config.json`, `myst.search.json` und `myst.xref.json` tragen kein `mdast` und keine
    `navigation`; sie bleiben damit von selbst unberuehrt.
    """
    data = json.loads(f.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        return 0, 0
    n_link, n_fuss = felder(data, slugs)
    if n_link or n_fuss:
        f.write_text(
            json.dumps(data, separators=(",", ":"), ensure_ascii=False), encoding="utf-8"
        )
    return n_link, n_fuss


def pruefen(root: pathlib.Path, base: str, slugs: set[str]) -> None:
    """Nachbedingung, am Artefakt neu gesucht statt dem Lauf geglaubt.

    Geprueft wird das Ergebnis, nicht die Zahl der Aenderungen: ein zweiter Lauf
    korrigiert null und muss trotzdem gruen sein.

    `felder()` mutiert sein Argument, und genau das ist hier der Test: was es noch zu
    aendern findet, haette der schreibende Lauf aendern muessen. Geaendert wird dabei nur
    die weggeworfene Kopie im Speicher -- geschrieben wird in diesem Zweig nichts.
    """
    seiten = sorted(root.rglob("index.html"))
    if not seiten:
        sys.exit(f"FEHLER: keine Seite unter {root}")
    for f in seiten:
        doc = f.read_text(encoding="utf-8")
        for m in HREF.finditer(doc):
            ziel = m.group(2)
            if ziel.startswith(base + "/") and fehlt_schraegstrich(ziel[len(base) :], slugs):
                sys.exit(
                    f"FEHLER: {f} verlinkt {ziel} ohne Schraegstrich -- darauf antwortet"
                    " GitLab Pages mit 302"
                )
        gelesen = lies_nutzlast(doc)
        if gelesen is None:
            if NUTZLAST in doc:
                sys.exit(f"FEHLER: {f} hat keine lesbare Hydrations-Nutzlast mehr")
            continue
        n_link, n_fuss = felder(gelesen[0], slugs)
        if n_link or n_fuss:
            sys.exit(
                f"FEHLER: {f} hat in der Nutzlast {n_link} Links und {n_fuss}"
                " Fusszeilen-Eintraege ohne Schraegstrich -- nach der Hydration stehen"
                " die im DOM"
            )
    for f in sorted(root.glob("*.json")):
        if not f.is_file():
            continue
        data = json.loads(f.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            continue
        n_link, n_fuss = felder(data, slugs)
        if n_link or n_fuss:
            sys.exit(
                f"FEHLER: {f.name} hat {n_link + n_fuss} Pfade ohne Schraegstrich --"
                " dieselbe Angabe in zwei Fassungen"
            )


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
    base = args.base.rstrip("/")
    # In eidl leer: die Seite liegt an der Wurzel ihres Hosts (BASE_URL "" in
    # .gitlab-ci.yml). Jeder Kapitelpfad beginnt dann mit "/" und wird an der
    # Kapitelliste erkannt, nicht am Praefix; ds-skript verlangte hier ein --base.
    slugs = seiten_slugs(root)

    if args.check:
        pruefen(root, base, slugs)
        print(
            f"trailing_slash --check: {len(sorted(root.rglob('index.html')))} Seiten,"
            f" {len(slugs)} Kapitel, kein Kapitellink ohne Schraegstrich"
        )
        return

    seiten = sorted(root.rglob("index.html"))
    if not seiten:
        sys.exit(f"FEHLER: keine Seite unter {root}")
    n_href = n_link = n_fuss = 0
    for f in seiten:
        a, b, c = seite(f, base, slugs)
        n_href += a
        n_link += b
        n_fuss += c
    j_link = j_fuss = 0
    for f in sorted(root.glob("*.json")):
        if f.is_file():
            a, b = seiten_json(f, slugs)
            j_link += a
            j_fuss += b
    pruefen(root, base, slugs)
    print(
        f"trailing_slash: {len(seiten)} Seiten, {len(slugs)} Kapitel,"
        f" {n_href} hrefs im Markup, {n_link + n_fuss} in der Nutzlast"
        f" ({n_link} Links, {n_fuss} Fusszeile), {j_link + j_fuss} in den Seiten-JSON"
    )


if __name__ == "__main__":
    main()
