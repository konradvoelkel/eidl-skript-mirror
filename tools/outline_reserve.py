#!/usr/bin/env python3
"""Platz fuer die Gliederung freihalten, die das Theme erst nach dem Mount fuellt.

    python3 tools/outline_reserve.py <html-verzeichnis>
    python3 tools/outline_reserve.py --check <html-verzeichnis>

Im `pages`-Job nach `image_dims.py` laufen lassen. Port aus ds-skript (2026-10-29); die
Messwerte unten sind dessen Seiten, die Ursache ist im eidl-Artefakt dieselbe (am
2026-11-03 nachgesehen: dasselbe leere `<nav></nav>` im selben Kasten).

Warum es dieses Skript gibt
---------------------------

Das Theme liefert den Kasten der Artikel-Gliederung mit einem **leeren** `<nav></nav>`
aus und fuellt ihn aus einem Effekt nach dem Mount. `myst-outline` und
`CollapsibleContent` stehen im ausgelieferten Markup nirgends; auch React rendert
serverseitig nichts dorthin. Unterhalb von `lg` steht der Kasten im Fluss, also faellt
alles darunter in dem Moment nach unten, in dem die Gliederung erscheint.

Am 2026-10-29 am Live-Stand bei 375x812 gemessen, je Seite der Kasten leer gegen
gefuellt und dazu der erste Absatz in `<main>`:

| Seite | Kasten leer | gefuellt | der erste Absatz rutscht |
|---|---|---|---|
| Startseite | 44 px | 340 px | **296 px** |
| `/kmeans/` | 44 px | 436 px | **392 px** |
| `/expectation-maximization/` | 44 px | 740 px (gedeckelt) | **696 px** |

Das ist dieselbe Ursache, die ds-en am 2026-10-18 gefunden und mit `88c5664` behoben hat
(dort 0,153 auf der Startseite und 0,278 auf einer Kapitelseite, danach beides 0). Die
Zeile 1g(b) in `TODO.md` fuehrte den Sprung bis hierher als Theme-Untersuchung, weil die
Messung an der Hydration haengen blieb; der Kasten war es.

Warum CSS im Kopf und kein Attribut am Kasten
---------------------------------------------

ds-en setzt eine Custom Property **an den Kasten** und loest sie in `myst-theme.css`
auf. In ds-skript geht das nicht: dort schlaegt die Hydration fehl (React #418) und
rendert das ganze Dokument neu, und ein Waechter haengt ein `<style>` im Kopf zurueck. In
eidl gelingt die Hydration (siehe `image_dims.py`), der Kopf bleibt stehen, und das
`<style>` braucht keinen Waechter. Uebernommen ist der Griff trotzdem unveraendert: ein
Selektor auf die **eigenen Klassen des Themes** trifft den Kasten, wie immer er
gerendert wurde, und eine Fassung fuer zwei Repos ist weniger als zwei.

Der Selektor ist am 2026-10-29 in beiden Fassungen gegengeprueft: im ausgelieferten HTML
trifft er genau einen `<div>`, dessen einziges Kind das leere `<nav>` ist, und im
hydrierten DOM genau denselben Knoten, dann mit `div.myst-outline-section` darin. Mehr
als einen `lg:col-margin-right` gibt es in `<main>` nicht.

`min-height` und nicht `height`, und nur unterhalb von `lg`
-----------------------------------------------------------

`min-height` ist ein Boden: zu viel reserviert kostet Leerraum und verschiebt nichts, zu
wenig reserviert laesst den Inhalt aus dem Kasten wachsen, und *das* verschiebt. Der
Fehler ist also einseitig, und nur deshalb darf hier ueberhaupt gerechnet statt gemessen
werden. Oberhalb von `lg` ist der Kasten `lg:h-0` und sitzt im Rand, wo er nichts
verdraengt; ein Boden wuerde dort das Layout kaputtmachen statt es zu schuetzen.

Die Zahlen
----------

Ein Eintrag ist 32 px hoch (`h2` und `h3`, 14 px Schrift auf 24 px Zeile plus 2x4 px
Polsterung) oder 24 px (`h4`, `text-xs`: 12 px auf 16 px Zeile). Der Kopf des `nav`
(24 px plus 16 px `mb-4`), seine eigene Polsterung (2x8 px) und der Kasten selbst
(28 px) sind zusammen 84 px. Am 2026-10-29 im Browser nachgerechnet: die Summe der
Eintragshoehen auf `/expectation-maximization/` ist 808 px und genau so hoch ist dort
`.CollapsibleContent`.

**Was die Rechnung nicht weiss, ist der Zeilenumbruch.** Ob ein Eintrag zweizeilig wird,
haengt an der gerenderten Breite proportionaler Schrift; der Bau hat den Text, aber keine
Schriftmetrik. Mit `measureText` im Browser gegen alle 32 Seiten gemessen, haben vier
Seiten ueberhaupt einen umgebrochenen Eintrag: `/expectation-maximization/` drei (dort
schluckt der Deckel die Differenz), `/statistische-tests/` zwei, `/datenschutz/` und
`/wichtigste-diskrete-verteilungen/` je einen. Eine zweite Zeile kostet 24 px, der
schlimmste Fall sind also 48 px von 812 -- und zwar nach unten, in die Richtung, in die
man fehlen darf. Der genaue Weg waere eine Schriftmetrik im Bau und in der CI; dafuer ist
das zu wenig. Die 28 anderen Seiten trifft die Rechnung aufs Pixel.

Unter zwei Eintraegen rendert das Theme keine Gliederung (`/stetige-verteilungen/` hat
eine `h2`, `/iris/` keine) -- dort wird nichts reserviert.
"""

from __future__ import annotations

import argparse
import pathlib
import re
import sys

MAIN = re.compile(r"<main\b[^>]*>.*?</main>", re.S | re.I)
UEBERSCHRIFT = re.compile(r"<(h[234])\b", re.I)

# Die id ist der Griff, an dem ein zweiter Lauf hier den Block ersetzt.
STYLE_ID = "gliederungsplatz"
STYLE_RE = re.compile(r'<style\b[^>]*\bid="' + STYLE_ID + r'"[^>]*>.*?</style>', re.S | re.I)

# Der Kasten, wie er ausgeliefert wird: der einzige <div> in <main>, dessen einziges Kind
# ein leeres <nav> ist. Erkannt an dieser Form und nicht an der vollen Klassenliste --
# die ist ein Stapel Utilities, den ein Theme-Update umsortieren kann, ohne es zu sagen.
KASTEN = re.compile(r"<div\b[^>]*>\s*<nav></nav>\s*</div>", re.I)
# Der Selektor fuers Stylesheet. Zwei Klassen aus der Liste des Themes, die beide auch
# das neu gerenderte Markup tragen: `my-10` (der Aussenabstand im Fluss) und
# `lg:col-margin-right` (die Spalte oberhalb von lg). Mit `class~=` statt mit einem
# Teilstring, damit `my-10` nicht auch `my-100` trifft.
KASTEN_SEL = 'main div[class~="my-10"][class~="lg:col-margin-right"]'
# Zum Gegenpruefen, dass derselbe Kasten gemeint ist, den KASTEN gefunden hat.
KASTEN_KLASSEN = ("my-10", "lg:col-margin-right")

# 32 px je Eintrag aus h2 und h3, 24 px je Eintrag aus h4; siehe Docstring.
EINTRAG_PX = {"h2": 32, "h3": 32, "h4": 24}
# Kopf des nav (24 + 16 mb-4), seine Polsterung (2x8) und der Kasten selbst (28).
RAHMEN_PX = 84
# Unter zwei Eintraegen rendert das Theme gar keine Gliederung.
MIN_EINTRAEGE = 2
# Das nav deckelt sich selbst auf `calc(100vh - 100px)` und scrollt dann; plus die 28 px
# des Kastens ist das die Hoehe, die der Inhalt nie ueberschreitet. Als CSS und nicht als
# Zahl, weil es am Viewport haengt und das hier zur Bauzeit laeuft.
DECKEL = "calc(100vh - 72px)"
# `lg` ist in diesem Theme 1024 px. Darunter steht der Kasten im Fluss, darueber im Rand.
BREAKPOINT = "1023.98px"


def eintraege(doc: str, seite: pathlib.Path) -> dict[str, int]:
    """Die Ueberschriften in <main>, nach Ebene gezaehlt.

    Nur auf dem <main>-Ausschnitt, aus demselben Grund wie in den Nachbarskripten: der
    Rest des Dokuments ist die Hydrations-Nutzlast, wo dieselben Ueberschriften noch
    einmal als JSON stehen.
    """
    m = MAIN.search(doc)
    if not m:
        sys.exit(f"FEHLER: {seite} hat kein <main>; nach dem HTML-Bau laufen lassen")
    gezaehlt = dict.fromkeys(EINTRAG_PX, 0)
    for lvl in UEBERSCHRIFT.findall(m.group(0)):
        gezaehlt[lvl.lower()] += 1
    return gezaehlt


def platz(gezaehlt: dict[str, int]) -> int:
    """Die Hoehe, die die gefuellte Gliederung einnehmen wird, oder 0.

    Ohne den Deckel: der steht als `min()` in der Regel, weil er den Viewport braucht.
    """
    n = sum(gezaehlt.values())
    if n < MIN_EINTRAEGE:
        return 0
    return sum(EINTRAG_PX[lvl] * k for lvl, k in gezaehlt.items()) + RAHMEN_PX


def kasten_pruefen(doc: str, seite: pathlib.Path) -> None:
    """Dass es den Kasten gibt, genau einmal, und dass der Selektor ihn trifft.

    Bricht ab statt zu warnen: ohne den Kasten hat die Reservierung keinen Ort, und eine
    stillschweigend wirkungslose Regel waere schlimmer als keine. Faellt das hier einmal
    aus, weil das Theme die Gliederung serverseitig rendert, dann ist dieses ganze Skript
    gegenstandslos und gehoert geloescht -- nicht wieder passend gemacht.
    """
    treffer = KASTEN.findall(doc)
    if len(treffer) != 1:
        sys.exit(
            f"FEHLER: {seite} hat {len(treffer)} Kaesten der Form <div><nav></nav></div>,"
            " erwartet genau einen. Rendert das Theme die Gliederung jetzt selbst, ist"
            f" tools/{pathlib.Path(__file__).name} gegenstandslos."
        )
    klassen = re.search(r'\bclass="([^"]*)"', treffer[0], re.I)
    fehlend = [k for k in KASTEN_KLASSEN if k not in (klassen.group(1).split() if klassen else [])]
    if fehlend:
        sys.exit(
            f"FEHLER: {seite}: der Gliederungskasten traegt {fehlend} nicht --"
            f" der Selektor {KASTEN_SEL} trifft ihn dann nicht."
            f" Klassen sind: {klassen.group(1) if klassen else '(keine)'}"
        )


def stilblock(px: int) -> str:
    """Der <style>-Block zu einer Hoehe, oder "" fuer eine Seite ohne Gliederung.

    Nicht in einer Cascade Layer, anders als das Stylesheet von `image_dims.py`: jenes
    soll das Theme ueberstimmen koennen, weil das Theme eigene Vorstellungen von
    Bildbreiten hat. Auf diesen Kasten setzt im Theme nichts eine `min-height`, es gibt
    also nichts, dem nachzugeben waere -- eine Layer wuerde die Reservierung nur gegen
    die naechste zufaellig passende Utility verlieren lassen.
    """
    if not px:
        return ""
    css = (
        f"@media (max-width:{BREAKPOINT}){{"
        f"{KASTEN_SEL}{{min-height:min({px}px,{DECKEL})}}"
        f"}}"
    )
    return f'<style id="{STYLE_ID}">{css}</style>'


def mit_stil(doc: str, seite: pathlib.Path, block: str) -> str:
    """Den Block in den Kopf setzen, einen vorhandenen ersetzen, einen leeren entfernen."""
    vorhanden = STYLE_RE.search(doc)
    if vorhanden:
        return doc[: vorhanden.start()] + block + doc[vorhanden.end() :]
    if not block:
        return doc
    i = doc.find("</head>")
    if i < 0:
        sys.exit(f"FEHLER: {seite} hat kein </head>")
    return doc[:i] + block + doc[i:]


def pruefen(doc: str, seite: pathlib.Path) -> int:
    """Nachbedingung, aus der Seite neu gerechnet statt dem Lauf geglaubt.

    Geprueft wird die **Eingabe** der Rechnung -- die Ueberschriften, die jetzt in
    `<main>` stehen, gegen die Hoehe, die im Kopf steht. Die gerenderte Hoehe ist zur
    Bauzeit nicht behauptbar (der Umbruch, siehe Docstring), also wird das geprueft, was
    tatsaechlich wegdriften kann: ein Kasten, der nicht mehr passt, oder eine Seite, die
    Ueberschriften dazubekommen hat, ohne dass die Hoehe mitlief.

    Gibt die reservierte Hoehe zurueck, 0 wenn nichts reserviert ist.
    """
    kasten_pruefen(doc, seite)
    erwartet = stilblock(platz(eintraege(doc, seite)))
    gefunden = STYLE_RE.search(doc)
    if not erwartet:
        if gefunden:
            sys.exit(
                f'FEHLER: {seite} hat ein <style id="{STYLE_ID}">, aber unter'
                f" {MIN_EINTRAEGE} Ueberschriften -- dort rendert das Theme keine"
                " Gliederung, der Platz waere Leerraum"
            )
        return 0
    if not gefunden:
        sys.exit(
            f'FEHLER: {seite} hat kein <style id="{STYLE_ID}"> -- die Gliederung'
            " schiebt dann beim Fuellen alles darunter nach unten"
        )
    if gefunden.group(0) != erwartet:
        sys.exit(
            f"FEHLER: {seite}: die reservierte Hoehe passt nicht zu ihren"
            f" Ueberschriften.\n  im Kopf:   {gefunden.group(0)}\n  erwartet:  {erwartet}"
        )
    kopf_ende = doc.find("</head>")
    if kopf_ende < 0 or gefunden.start() > kopf_ende:
        sys.exit(
            f'FEHLER: {seite}: das <style id="{STYLE_ID}"> steht nicht im Kopf'
        )
    return platz(eintraege(doc, seite))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("html_dir")
    ap.add_argument(
        "--check",
        action="store_true",
        help="nichts schreiben, nur die Nachbedingung am gebauten Artefakt pruefen",
    )
    args = ap.parse_args()

    root = pathlib.Path(args.html_dir)
    seiten = sorted(root.rglob("index.html"))
    if not seiten:
        sys.exit(f"FEHLER: unter {root} liegt keine index.html; nach dem HTML-Bau laufen lassen")

    if not args.check:
        for f in seiten:
            doc = f.read_text(encoding="utf-8")
            kasten_pruefen(doc, f)
            neu = mit_stil(doc, f, stilblock(platz(eintraege(doc, f))))
            if neu != doc:
                f.write_text(neu, encoding="utf-8")

    hoehen = []
    ohne = 0
    for f in seiten:
        px = pruefen(f.read_text(encoding="utf-8"), f)
        hoehen.append(px) if px else None
        ohne += 0 if px else 1
    if not hoehen:
        sys.exit(
            "FEHLER: keine einzige Seite reserviert Platz -- entweder zaehlt niemand"
            " mehr Ueberschriften in <main> oder der Kasten ist weg"
        )
    wie = "outline_reserve --check" if args.check else "outline_reserve"
    print(
        f"{wie}: {len(seiten)} Seiten, {len(hoehen)} mit Gliederung"
        f" ({min(hoehen)}-{max(hoehen)} px reserviert, gedeckelt auf {DECKEL}),"
        f" {ohne} ohne (unter {MIN_EINTRAEGE} Ueberschriften)"
    )


if __name__ == "__main__":
    main()
