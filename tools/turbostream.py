#!/usr/bin/env python3
"""Die Hydrations-Nutzlast von Theme 2.x lesen und ändern.

Theme 1.4.x legte die Nutzlast als gewöhnliches JSON-Objekt in die Seite:

    window.__remixContext = {"state":{"loaderData":{...}}}

und drei Schritte in `tools/` haben darin Felder korrigiert, weil React nach der
Hydration das Markup aus der **Nutzlast** neu rendert und ein nur im Markup
korrigierter Wert damit nach dem ersten Frame wieder verschwindet.

Theme 2.x (React Router 8) schickt dieselben Daten als **Turbo-Stream**:

    window.__reactRouterContext.streamController.enqueue("[{\\"_1\\":2},\\"loaderData\\",…]")

Das ist ein **flaches** Array. Ein Objekt nennt seine Schlüssel und Werte über Indizes in
dasselbe Array: `{"_363":364}` heißt „Schlüssel steht bei 363, Wert bei 364". Zeichenketten
sind dadurch nur einmal da und werden von vielen Knoten geteilt. Eine Textersetzung wie
`"url":"…"` findet darin nichts, denn Schlüssel und Wert stehen nicht beieinander.

Dieses Modul kapselt das: Es dekodiert, gibt die Knoten als Python-Objekte heraus und
schreibt zurück. **Angehängt wird immer am Ende** -- die Indizes der vorhandenen Einträge
bleiben damit gültig, und ein Knoten, der niemand anfaßt, bleibt Byte für Byte derselbe.

Negative Werte sind Sonderfälle des Formats (`-5`, `-7`: undefined, null); sie werden nie
als Index gelesen.

Was `js_literal()` escapet und warum, steht an der Funktion.
"""

from __future__ import annotations

import json
import re
from typing import Any, Callable, Iterator

#: Der Aufruf, der die Nutzlast in die Seite bringt, samt Zeichenkettenliteral.
#:
#: Das Literal wird **vollständig** gelesen (`"(?:[^"\\]|\\.)*"`), nicht mit `".*?"`:
#: In der Nutzlast steht HTML, und ein Alt-Text oder ein Code-Schnipsel kann `\");`
#: enthalten -- ein ungieriges `".*?"` endet dann mitten im Literal. Gemessen am
#: 2026-11-27: von 33 Seiten traf das 20, und die Nutzlast war danach unlesbar.
RX = re.compile(r'(streamController\.enqueue\()("(?:[^"\\]|\\.)*")(\);)', re.S)


def vorhanden(doc: str) -> bool:
    """Trägt dieses Dokument eine Turbo-Stream-Nutzlast?"""
    return RX.search(doc) is not None


def js_literal(daten: list) -> str:
    """Das Array als JS-Zeichenkettenliteral, wie das Theme es selbst schreibt.

    Jedes `<` wird zu `\\u003c`: Ein wörtliches `</script>` in einem Alt-Text würde das
    `<script>`-Element früh schließen. Das Theme escapet aus demselben Grund alle
    Vorkommen so (gezählt an einer Kapitelseite: 5.039). U+2028 und U+2029 sind in JSON
    gewöhnliche Zeichen, in JavaScript aber Zeilenenden.
    """
    text = json.dumps(daten, separators=(",", ":"), ensure_ascii=False)
    literal = json.dumps(text, ensure_ascii=False)
    return (literal.replace("<", "\\u003c")
                   .replace(" ", "\\u2028")
                   .replace(" ", "\\u2029"))


def bearbeiten(doc: str, fn: Callable[[list], int]) -> tuple[str, int]:
    """`fn` auf jede Nutzlast des Dokuments anwenden; sie gibt die Zahl der Änderungen.

    Geschrieben wird nur, wenn `fn` etwas geändert hat; eine Nutzlast, die sich nicht
    dekodieren läßt, bleibt unberührt (und zählt nicht als Änderung).
    """
    gesamt = 0

    def ein(m: re.Match[str]) -> str:
        nonlocal gesamt
        try:
            daten = json.loads(json.loads(m.group(2)))
        except (json.JSONDecodeError, TypeError):
            return m.group(0)
        if not isinstance(daten, list):
            return m.group(0)
        n = fn(daten)
        if not n:
            return m.group(0)
        gesamt += n
        return m.group(1) + js_literal(daten) + m.group(3)

    return RX.sub(ein, doc), gesamt


def lesen(doc: str) -> list | None:
    """Die erste Nutzlast als flaches Array, ohne sie zu ändern. None, wenn keine da ist."""
    m = RX.search(doc)
    if m is None:
        return None
    try:
        daten = json.loads(json.loads(m.group(2)))
    except (json.JSONDecodeError, TypeError):
        return None
    return daten if isinstance(daten, list) else None


# --- Arbeiten mit den Knoten ---------------------------------------------------------

def schluessel(daten: list, name: str) -> int | None:
    """Der Index der Schlüsselzeichenkette `name`, oder None."""
    try:
        return daten.index(name)
    except ValueError:
        return None


def schluessel_oder_neu(daten: list, name: str) -> int:
    """Wie `schluessel()`, hängt den Schlüssel aber an, wenn er fehlt."""
    i = schluessel(daten, name)
    if i is None:
        i = len(daten)
        daten.append(name)
    return i


def hole(daten: list, knoten: dict, name: str) -> tuple[int, Any] | None:
    """`(Wertindex, Wert)` eines Feldes dieses Knotens, oder None.

    None auch dann, wenn der Wert ein Sonderfall des Formats ist (negativer Index).
    """
    i = schluessel(daten, name)
    if i is None:
        return None
    w = knoten.get(f"_{i}")
    if not isinstance(w, int) or not 0 <= w < len(daten):
        return None
    return w, daten[w]


def setze(daten: list, knoten: dict, name: str, wert: Any,
          cache: dict[Any, int] | None = None) -> None:
    """Ein Feld dieses Knotens setzen; Schlüssel und Wert werden angehängt.

    `cache` spart Dubletten, wenn derselbe Wert an viele Knoten kommt.
    """
    i = schluessel_oder_neu(daten, name)
    if cache is not None and wert in cache:
        knoten[f"_{i}"] = cache[wert]
        return
    j = len(daten)
    daten.append(wert)
    if cache is not None:
        cache[wert] = j
    knoten[f"_{i}"] = j


def knoten_mit(daten: list, name: str) -> Iterator[tuple[dict, int, Any]]:
    """Jeden Knoten, der das Feld `name` trägt, samt Wertindex und Wert."""
    i = schluessel(daten, name)
    if i is None:
        return
    marke = f"_{i}"
    for eintrag in daten:
        if not isinstance(eintrag, dict) or marke not in eintrag:
            continue
        w = eintrag[marke]
        if isinstance(w, int) and 0 <= w < len(daten):
            yield eintrag, w, daten[w]


def bildknoten(daten: list) -> Iterator[tuple[dict, str]]:
    """Jeden mdast-Bildknoten (`"type":"image"`) samt seiner Adresse."""
    for knoten, _, typ in knoten_mit(daten, "type"):
        if typ != "image":
            continue
        gefunden = hole(daten, knoten, "url")
        if gefunden is None or not isinstance(gefunden[1], str):
            continue
        yield knoten, gefunden[1]


def routen(daten: list) -> Iterator[dict]:
    """Die Daten je Route aus `loaderData` -- dasselbe, was `routes()` im JSON tat.

    Aufbau: `daten[0]` ist die Wurzel, ihr Feld `loaderData` ein Objekt, dessen Werte die
    Routendaten sind (`root`, `routes/_index`, …). Daran hängen `page` und `project`.
    """
    if not daten or not isinstance(daten[0], dict):
        return
    gefunden = hole(daten, daten[0], "loaderData")
    if gefunden is None or not isinstance(gefunden[1], dict):
        return
    for w in gefunden[1].values():
        if isinstance(w, int) and 0 <= w < len(daten) and isinstance(daten[w], dict):
            yield daten[w]


def kartenknoten(daten: list) -> Iterator[dict]:
    """Die Knoten, aus denen das Theme `og:image` baut: `page.frontmatter` und `project`.

    **Nicht** `project.pages[]` oder `config.projects[0].pages[]`: Deren `thumbnail` ist
    die kleine Vorschau beim Überfahren eines internen Links, keine Kartenangabe. Dieselbe
    Einschränkung wie in `tools/head_meta.py` und `tools/hydration.py` für die alte
    Nutzlast.
    """
    for route in routen(daten):
        seite = hole(daten, route, "page")
        if seite is not None and isinstance(seite[1], dict):
            front = hole(daten, seite[1], "frontmatter")
            if front is not None and isinstance(front[1], dict):
                yield front[1]
        projekt = hole(daten, route, "project")
        if projekt is not None and isinstance(projekt[1], dict):
            yield projekt[1]
