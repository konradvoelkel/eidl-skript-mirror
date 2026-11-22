#!/usr/bin/env python3
"""Was die Hydration dieses Themes wegwirft, und wie es zurückkommt.

    python3 tools/hydration.py <site-url> <html-verzeichnis> [--base BASE_URL] [--lang de]
    python3 tools/hydration.py --check <html-verzeichnis> [--base BASE_URL] [--lang de]

Im `pages`-Job als **letzter** Schritt laufen zu lassen, der HTML anfaßt: nach
`publish_urls.py`, `head_meta.py`, `inject_jsonld.py`, `freshness.py`, `llms_txt.py`,
`image_dims.py`, `outline_reserve.py`, `trailing_slash.py` und `no_css_dialog.py` -- es
liest die Tags und Knoten, die diese geschrieben haben, aus dem Kopf zurück und baut
daraus seinen Wächter. Vor `precompress.py`, wie jeder Schritt, der HTML ändert.


Warum es dieses Skript gibt
---------------------------

Der `<head>` gehört zum React-Baum, und Remix hydriert das ganze Dokument. Alles, was die
Schritte davor nach dem Bau ins Markup geschrieben haben, ist nach dem ersten Frame weg.

Bis zum 2026-11-15 stand in `CLAUDE.md`, in `tools/head_meta.py` §2 und in
`devnotes/erledigt.md:384` das Gegenteil: „Die Hydration gelingt hier, anders als in
ds-skript ... Canonical, `og:*`, JSON-LD und `loading="lazy"` stehen nach der Hydration
noch", gemessen am 2026-11-03. **Das war falsch**, und zwar für jede Seite. Am 2026-11-15
im sichtbaren Browserfenster und, unabhängig davon, an Googles eigenem Renderer
nachgemessen (Rich Results Test, „View tested page", 435.761 bzw. 48.448 Zeichen
gerendertes HTML, beide Seiten „Crawled successfully", Befund „No items detected"):

| | ausgeliefert | gerendert |
|---|---|---|
| `<html lang>`                                  | `de`      | **`en`** |
| `ld+json`-Blöcke                               | 1         | **0** |
| `rel="canonical"`                              | da        | **weg** |
| `og:url`, `og:site_name`, `og:type`, `og:locale` | da      | **weg** |
| `twitter:card`                                 | da        | **weg** |
| `link rel="alternate" type="text/markdown"`    | da        | **weg** |
| `style id="bildmasse"`, `id="gliederungsplatz"`| da        | **weg** |
| `<title>` der Landingpage                      | mit Zusatz| **ohne Zusatz** |
| `og:image`                                     | absolut   | **wieder wurzelrelativ** |
| `<meta name="description">`                    | da        | da (MyST setzt es selbst) |
| `<dialog id="myst-no-css">`                    | **weg**   | **wieder da** (seit 2026-11-17 raeumt der Waechter ihn ab) |

Was MyST selbst setzt, überlebt; was ein Schritt nachträgt, überlebt nicht.

Die Ursache steht in der Konsole: **React #418 und #423** auf jeder Seite. #418 ist die
Abweichung zwischen servergerendertem und clientseitig gerendertem Baum, #423 der
Abbruch, nach dem React die Wurzel vollständig neu rendert. ds-skript hat nur #418; dort
überleben deshalb das `ld+json` (ein `<script>` verwaltet React nicht) und `lang="de"`.
Hier überlebt beides nicht, und das ist der Grund, warum dieses Skript nicht die Kopie
des dortigen ist.


Warum der Wächter `document` beobachtet und nicht `document.head`
-----------------------------------------------------------------

ds-skripts Wächter hängt einen `MutationObserver` auf `document.head` mit
`{childList:true}`. **Das wäre hier still wirkungslos**, und das ist gemessen, nicht
vermutet. Eine Sonde, die zur Parse-Zeit Referenzen auf `document.head` und
`document.documentElement` festhält, meldet nach der Hydration (lokales Artefakt, Port
8791, 14 s nach dem Laden):

    headSame: false      headConnected: false     headFired: 4
    deSame:   false      langFired:     0

React **ersetzt `documentElement`**, mitsamt `<head>`. Der alte Kopf ist danach abgehängt;
ein Observer auf ihm feuert noch viermal, solange er hängt, und ist danach ein Observer
auf einem Knoten, der nicht mehr im Dokument steht. Genau daran ist der `lang`-Wächter in
`head_meta.py` gestorben: Er beobachtet `documentElement` mit
`attributeFilter:["lang"]`, und der wurde nicht *mutiert*, sondern *getauscht* --
`langFired: 0`. Gegenprobe an der ausgelieferten Seite: `lang` von Hand auf `xx` gesetzt,
nach 600 ms steht weiterhin `xx` da. Der Wächter lebt nicht mehr.

`document` wird nie ersetzt. Der Observer hängt deshalb dort, mit `subtree:true`, und der
Rückschreiber schlägt `document.head` und `document.documentElement` bei **jedem** Lauf
frisch nach, statt sie festzuhalten. Am Kandidaten nachgemessen, dieselbe Seite: `lang`
steht auf `de`, Canonical, `og:url`, `og:site_name`, `twitter:card` und das `ld+json`
sind wieder da, der Titelzusatz steht, der Rückschreiber lief neunmal.

`head_meta.py` behält seinen `lang`-Wächter: Er ist nach der Hydration wirkungslos, aber
bis dahin tut er seine Arbeit, und das Attribut im Markup ist ohnehin das, was jeder
Leser ohne JavaScript sieht. Dieses Skript übernimmt nur den Teil danach.

Nachtrag 2026-11-22: Der Abbruch findet nicht mehr statt
--------------------------------------------------------

Unter mystmd 1.13.0 und Theme 1.4.1 meldet die Konsole **keinen React-Fehler mehr**, und
ohne diesen Wächter überleben `lang="de"`, der `ld+json`-Block samt Typen und die zwei
Stylesheets `bildmasse` und `gliederungsplatz`. `documentElement` wird also nicht mehr
ersetzt. Verloren gehen nur die `<meta>`- und `<link>`-Tags, die React im Kopf selbst
verwaltet: Canonical, die vier `og:*`, `twitter:card`, der Markdown-`alternate`,
`article:modified_time` und der Titelzusatz der Startseite, dazu `og:image` zurück auf die
wurzelrelative Adresse und der `myst-no-css`-Kasten wieder da -- auf sechs von sechs
gemessenen Seiten. Der Wächter bleibt deshalb nötig; daß er an `document` hängt und Kopf
und Wurzel frisch nachschlägt, ist jetzt Vorsorge statt Notwendigkeit. Zahlen und Methode:
`devnotes/build-log-2026-11-22-hydration.md`.


Welcher Weg für welches Tag -- das ist keine Geschmacksfrage
------------------------------------------------------------

Dieselbe Regel wie in ds-skript: **Wo das Theme ein Feld der Nutzlast rendert, wird das
Feld gesetzt** -- dann rendert React von selbst das Richtige und es gibt gar keine
Abweichung. **Wo es keines gibt, bleibt nur der Wächter.**

Genau ein Fall hat ein Feld: `og:image`. Das Theme baut es aus
`page.frontmatter.thumbnailOptimized || thumbnail` (Kapitel) bzw. aus demselben Paar unter
`project` (Landingpage) neu. `head_meta.py` setzt dort schon die Karte ein, aber
**wurzelrelativ** -- am 2026-11-15 in der Nutzlast nachgemessen:
`'/build/social-card-3fd4fb7a....png'`. OpenGraph verlangt eine absolute URL, und genau
deshalb stand in Googles Rendering ein relatives `og:image`. `absolute_card()` macht die
vier Felder absolut; der Wächter führt `og:image` deshalb **nicht**.

`page.domain` ist hier nichts zu tun: `publish_urls.py` setzt es schon auf die echte
Origin (nachgemessen, und `localhost:3000` kommt nach der Kette in keiner der 33 Seiten
und in keinem der Seiten-JSON mehr vor). In ds-skript war das anders; wer dort sucht,
findet `set_domain()` und `set_json_domain()`.

**Die zwei Schrift-Preloads führt der Wächter nicht**, und das ist eine Entscheidung. Ein
Preload wirkt im ausgelieferten Dokument, bevor das Stylesheet geparst ist; zum Zeitpunkt
der Hydration sind beide `woff2` längst angefragt. Ihn danach wieder einzuhängen bewirkt
nichts, außer daß eine Messung grün aussieht.


Die bewahrten Knoten, und warum das die mobile Layoutverschiebung mitnimmt
--------------------------------------------------------------------------

`GESCHUETZT` sind Tags, die sich aus ihren Attributen neu bauen lassen. `BEWAHRT` sind
Knoten mit *Inhalt*, die man nur zurückhängen kann: der `ld+json`-Block und die zwei
Stylesheets `id="bildmasse"` (aus `image_dims.py`) und `id="gliederungsplatz"` (aus
`outline_reserve.py`). Der Wächter greift sie beim Parsen per Selektor und hängt sie
zurück, sobald sie abgehängt sind -- deshalb steht er am **Ende** des Kopfes, hinter
ihnen.

Das ist nicht nur eine Frage der Suchmaschine. Die 276 px, die `outline_reserve.py` für
die Gliederung reserviert, stehen in genau diesem `<style id="gliederungsplatz">`. Fällt
es bei der Hydration weg, springt alles darunter -- gemessen am 2026-11-15:
CLS 0,208 auf der Startseite, **0,43** auf `/backpropagation/` im Mobilprofil, bei einem
Grenzwert von 0,1. Der Wächter hängt das Stylesheet zurück, und damit hat die
Reservierung wieder etwas, woran sie hängt. Ob das die Zahl wirklich unter 0,1 drückt,
ist **nicht gemessen** -- der Sprung passiert im Fenster zwischen Wegfall und
Rückhängen, und wie groß das Fenster ist, hängt am Gerät.


Der Titel
---------

`head_meta.py` hängt den Zusatz „ — Vorlesungsskript, HHU Düsseldorf" an den `<title>`
**der Landingpage** (nicht an `h1` und `og:title`, das ist dort begründet). Das Theme
baut den Titel aus der Nutzlast neu, der Zusatz fällt also weg -- und er ist genau das,
was die eine gewinnbare Query-Familie adressiert („Deep Learning Vorlesung Skript", siehe
`devnotes/seo-audit-2026-11-15.md` §4). Der Wächter trägt den gebauten `<title>` als
Daten und setzt ihn zurück. Auf den Kapitelseiten ist das ein Leerlauf, weil das Theme
dort denselben Titel erzeugt; eine Sonderbehandlung der Landingpage wäre eine zweite
Stelle, die wüßte, welche Seite die Landingpage ist.


Die Falle aus ds-en, und warum hier nach jedem Schreiben geprüft wird
---------------------------------------------------------------------

`json.JSONDecoder().raw_decode` liefert den **absoluten Index** des JSON-Endes im
Dokument, nicht die Anzahl verbrauchter Zeichen. Wer ihn als Länge liest und
`doc[start + end:]` schneidet, schneidet um `start` zu weit -- hinter das Dokumentende,
und der Rest wird stillschweigend `""`. Genau das ist in ds-en ausgeliefert worden: jede
Seite 85 kB zu kurz, ohne `</script>`, `</body>`, `</html>` und ohne das Modul-Script,
das den Client startet. Browser bügeln offene Tags glatt, es sah also nichts falsch aus.

Deshalb steht hier nach jedem Schreiben die Frage „endet das Dokument noch auf `</html>`
und ist die Nutzlast wieder gültiges JSON", und `--check` stellt sie noch einmal über
alles.


Was `--check` nicht kann
------------------------

Es prüft das **Artefakt**: steht der Wächter da, passt er zu seinem Kopf, ist das
Dokument ganz. Es prüft **nicht**, was der Browser daraus macht -- und genau diese Lücke
hat den Befund zwei Audits lang verdeckt. Dafür gibt es `--check-rendered`: es lädt die
Seiten in dem Chromium, den Playwright mitbringt, wartet die Hydration ab und sieht im
gerenderten DOM nach. Das braucht ein Paket und läuft deshalb **nicht** in der CI (das
Image installiert kein einziges Python-Paket, CLAUDE.md, bewußte Entscheidung 5), sondern
von Hand nach einem Theme- oder mystmd-Update:

    uv run --only-group dev python tools/hydration.py --check-rendered _build/html

Ohne Playwright sagt es das und endet mit 2, nicht mit 0 -- „nicht gemessen" ist kein
Erfolg.


Zweimal laufen
--------------

Idempotent. In der Nutzlast wird nur gesetzt, was noch nicht gesetzt ist. Der Wächter
wird an seinem Erkennungszeichen erkannt und **ersetzt**, nicht ein zweites Mal
angehängt: er trägt Daten, und die können sich geändert haben. Er wandert dabei immer ans
Ende des Kopfes, weil er die bewahrten Knoten beim Parsen greift.
"""

from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys

# Erkennungszeichen des Kopf-Wächters. Ein zweiter Lauf ersetzt ihn daran.
MARKER = "/*kopf-waechter*/"
GUARD_RE = re.compile(r"<script>" + re.escape(MARKER) + r".*?</script>", re.S)

# Tags, die die Hydration wegwirft und die der Wächter aus ihren Attributen neu baut, je
# als (Muster im Kopf, Attribute, die die Identität des Tags ausmachen).
#
# Die Werte stehen *nicht* hier, sondern werden aus dem gebauten Kopf gelesen: sonst wäre
# dies eine zweite Quelle der Wahrheit neben publish_urls.py, head_meta.py, freshness.py
# und llms_txt.py und liefe irgendwann auseinander. og:image fehlt mit Absicht -- dafür
# gibt es ein Feld in der Nutzlast, siehe absolute_card().
GESCHUETZT = (
    (re.compile(r'<link\b[^>]*\brel="canonical"[^>]*>', re.I), ("rel",)),
    (
        re.compile(
            r'<meta\b[^>]*\bproperty="(?:og:url|og:site_name|og:type|og:locale'
            r'|article:modified_time)"[^>]*>',
            re.I,
        ),
        ("property",),
    ),
    (re.compile(r'<meta\b[^>]*\bname="twitter:card"[^>]*>', re.I), ("name",)),
    (re.compile(r'<link\b[^>]*\btype="text/markdown"[^>]*>', re.I), ("rel", "type")),
)

# Knoten mit Inhalt, die der Wächter nur zurückhängen kann. Reihenfolge ist die, in der
# er sie wieder anhängt; sie spielt für keinen davon eine Rolle.
BEWAHRT = (
    'script[type="application/ld+json"]',
    'style[id="bildmasse"]',
    'style[id="gliederungsplatz"]',
)
BEWAHRT_RE = {
    'script[type="application/ld+json"]': re.compile(
        r'<script\b[^>]*\btype="application/ld\+json"', re.I
    ),
    'style[id="bildmasse"]': re.compile(r'<style\b[^>]*\bid="bildmasse"', re.I),
    'style[id="gliederungsplatz"]': re.compile(
        r'<style\b[^>]*\bid="gliederungsplatz"', re.I
    ),
}

ATTR_RE = re.compile(r'([a-zA-Z:_-]+)\s*=\s*"([^"]*)"')
TITLE_RE = re.compile(r"<title[^>]*>(.*?)</title>", re.S | re.I)


def head_slice(doc: str, f: pathlib.Path) -> str:
    """Nur der Kopf. Der Rest des Dokuments trägt die Nutzlast -- die ganze Seite noch
    einmal als JSON --, und ein Muster darauf fände Zeichenketten, die Daten sind."""
    i = doc.find("</head>")
    if i < 0:
        sys.exit(f"FEHLER: {f} hat kein </head>")
    return doc[:i]


def collect_tags(head: str, f: pathlib.Path) -> list[dict]:
    """Die geschützten Tags aus dem Kopf lesen, als Daten für den Wächter.

    Der Selektor nennt nur die Identitätsattribute (`rel`, `property`, `name`, `type`),
    nicht `href` oder `content`: sonst würde ein Tag mit falschem Wert nicht korrigiert,
    sondern ein zweites daneben gestellt.
    """
    tags: list[dict] = []
    gesehen: set[str] = set()
    for muster, ident in GESCHUETZT:
        for m in muster.finditer(head):
            tag = m.group(0)
            name = "link" if tag.lower().startswith("<link") else "meta"
            attrs = dict(ATTR_RE.findall(tag))
            fehlend = [k for k in ident if k not in attrs]
            if fehlend:
                sys.exit(f"FEHLER: {f}: {tag} fehlt {fehlend} -- kein Selektor zu bauen")
            sel = name + "".join(f'[{k}="{attrs[k]}"]' for k in ident)
            if sel in gesehen:
                sys.exit(
                    f"FEHLER: {f}: zwei Tags mit demselben Selektor {sel} -- der"
                    " Wächter könnte sie nicht auseinanderhalten"
                )
            gesehen.add(sel)
            tags.append({"n": name, "s": sel, "a": attrs})
    return tags


def bewahrte(head: str) -> list[str]:
    """Die Selektoren aus BEWAHRT, zu denen in diesem Kopf überhaupt ein Knoten steht.

    Eine Seite ohne Abbildung hat kein `bildmasse`, und der Wächter soll dann auch nicht
    danach greifen -- sonst stünde in seinen Daten ein Selektor, der nie etwas trifft.
    """
    return [s for s in BEWAHRT if BEWAHRT_RE[s].search(head)]


def js_literal(obj) -> str:
    """JSON als JavaScript-Literal innerhalb eines `<script>`.

    Ein nacktes `<` könnte das Tag früh schließen, und U+2028/U+2029 sind in JSON
    gewöhnliche Zeichen, in JavaScript aber Zeilenenden.
    """
    out = json.dumps(obj, separators=(",", ":"), ensure_ascii=False)
    return (
        out.replace("<", "\\u003c")
        .replace(" ", "\\u2028")
        .replace(" ", "\\u2029")
    )


def guard_script(path: str, tags: list[dict], keep: list[str], lang: str, title: str) -> str:
    """Der Wächter.

    `location.pathname` wird gegen den Pfad geprüft, für den dieser Satz gebaut wurde.
    Beim statischen Bau ist jeder Klick im Buch ein echter Seitenaufruf, der Fall tritt
    also nicht ein; täte er es doch, trägt die Seite *keine* Tags statt der falschen, und
    das ist die richtige Richtung -- ein Canonical, der auf die vorige Seite zeigt, ist
    schlimmer als keiner.

    `document` als Beobachtungsziel und das frische Nachschlagen von `document.head` und
    `document.documentElement` bei jedem Lauf sind der Kern: React ersetzt beide, siehe
    Docstring.
    """
    daten = js_literal({"p": path, "t": tags, "k": keep, "l": lang, "ti": title})
    js = (
        "(function(){var D=" + daten + ",b=false,K=[];"
        # Die bewahrten Knoten beim Parsen greifen -- danach sind sie abgehaengt, und
        # querySelector findet sie nicht mehr.
        "for(var j=0;j<D.k.length;j++){var n=document.head.querySelector(D.k[j]);"
        "if(n)K.push(n)}"
        'function p(){var x=location.pathname;return x.charAt(x.length-1)==="/"?x:x+"/"}'
        "function f(){if(b||p()!==D.p)return;b=true;try{"
        "var h=document.head,e=document.documentElement;"
        'if(e.getAttribute("lang")!==D.l)e.setAttribute("lang",D.l);'
        "if(document.title!==D.ti)document.title=D.ti;"
        "for(var i=0;i<D.t.length;i++){var t=D.t[i],x=h.querySelector(t.s);"
        "if(!x){x=document.createElement(t.n);h.appendChild(x)}"
        "for(var k in t.a){if(x.getAttribute(k)!==t.a[k])x.setAttribute(k,t.a[k])}}"
        "for(var j=0;j<K.length;j++){if(!K[j].isConnected)h.appendChild(K[j])}"
        # Der Kasten "Site not loading correctly?" kommt mit der Hydration zurueck:
        # `no_css_dialog.py` nimmt ihn aus dem Artefakt, React baut ihn aus der Nutzlast
        # neu. Er ist `display:none` und fuer Menschen unsichtbar, steht aber als erster
        # Knoten im Body -- wer die gerenderte Seite als Text liest, beginnt mit einer
        # Deploy-Fehlermeldung (SEO-Audit 2026-11-17, §7).
        'var c=document.getElementById("myst-no-css");if(c)c.remove();'
        "}finally{b=false}}f();"
        "new MutationObserver(f).observe(document,{childList:true,subtree:true,"
        'attributes:true,attributeFilter:["lang"]});})();'
    )
    return f"<script>{MARKER}{js}</script>"


def read_payload(doc: str):
    """Die Hydrations-Nutzlast mit Anfang und Ende. None, wenn die Seite keine hat.

    `raw_decode` gibt den **absoluten Index** des JSON-Endes zurück, nicht die Länge --
    die Falle, die in ds-en jede Seite abgeschnitten hat, siehe Docstring.
    """
    key = "window.__remixContext = "
    i = doc.find(key)
    if i < 0:
        return None
    start = i + len(key)
    try:
        payload, end = json.JSONDecoder().raw_decode(doc, start)
    except ValueError:
        return None
    return payload, start, end


def routes(payload: dict):
    """Die loaderData-Routen -- dort liegt jeder Wert, den dieses Skript anfaßt.

    Über alle Routen, nicht über einen Namen: die Landingpage liegt je nach BASE_URL
    unter `routes/_index` oder `routes/$`, und das ist nichts, woran ein Skript hängen
    sollte.
    """
    for route in (payload.get("state", {}).get("loaderData") or {}).values():
        if isinstance(route, dict):
            yield route


def edit_payload(doc: str, mutate) -> tuple[str, bool]:
    """Die Nutzlast an `mutate` geben und zurückschreiben, wenn sie sich geändert hat."""
    found = read_payload(doc)
    if found is None:
        return doc, False
    payload, start, end = found
    if not mutate(payload):
        return doc, False
    return doc[:start] + js_literal(payload) + doc[end:], True


def absolute_card(doc: str, site: str, base: str) -> tuple[str, bool]:
    """Die Vorschaukarte in der Nutzlast absolut machen.

    Umgeschrieben wird nur, was wurzelrelativ unter dem Basispfad auf `/build/` zeigt --
    damit ein zweiter Lauf Leerlauf bleibt und eine fremde URL unberührt. Die vier
    Felder sind die, aus denen das Theme `og:image` baut; `project.pages[]` und
    `config.projects[0].pages[]` tragen ebenfalls je ein `thumbnail`, das sind aber keine
    Kartenangaben, sondern die kleine Vorschau beim Überfahren eines internen Links.
    """
    prefix = f"{base}/build/"

    def mutate(payload: dict) -> bool:
        changed = False
        for route in routes(payload):
            page = route.get("page")
            front = page.get("frontmatter") if isinstance(page, dict) else None
            for node in (front, route.get("project")):
                if not isinstance(node, dict):
                    continue
                for key in ("thumbnail", "thumbnailOptimized"):
                    url = node.get(key)
                    if isinstance(url, str) and url.startswith(prefix):
                        node[key] = site + url[len(base) :]
                        changed = True
        return changed

    return edit_payload(doc, mutate)


def whole(doc: str, f: pathlib.Path) -> None:
    """Die Nachbedingung, die der ds-en-Unfall gekostet hat: ist das Dokument ganz?"""
    if not doc.rstrip().endswith("</html>"):
        sys.exit(f"FEHLER: {f} endet nicht auf </html> -- der Schnitt war zu weit")
    if "window.__remixContext" in doc and read_payload(doc) is None:
        sys.exit(f"FEHLER: {f} hat keine lesbare Hydrations-Nutzlast mehr")


def titel(head: str, f: pathlib.Path) -> str:
    m = TITLE_RE.search(head)
    if not m:
        sys.exit(f"FEHLER: {f} hat keinen <title>")
    return m.group(1).strip()


def page_path(base: str, rel: pathlib.PurePath) -> str:
    """Der Pfad, unter dem die Seite ausgeliefert wird -- mit Schrägstrich am Ende."""
    return f"{base}/" if str(rel) == "." else f"{base}/{rel}/"


def guard_for(doc: str, f: pathlib.Path, base: str, root: pathlib.Path, lang: str) -> str:
    head = head_slice(doc, f)
    return guard_script(
        page_path(base, f.parent.relative_to(root)),
        collect_tags(head, f),
        bewahrte(head),
        lang,
        titel(head, f),
    )


def check(root: pathlib.Path, base: str, lang: str) -> int:
    """Noch einmal über alles, am Artefakt. Was das nicht kann, siehe Docstring."""
    pages = sorted(root.rglob("index.html"))
    if not pages:
        sys.exit(f"FEHLER: keine Seite unter {root}")
    n_tags = n_keep = 0
    for f in pages:
        doc = f.read_text(encoding="utf-8")
        whole(doc, f)
        head = head_slice(doc, f)
        if guard_for(doc, f, base, root, lang) not in doc:
            sys.exit(
                f"FEHLER: {f} trägt keinen Wächter, der zu ihrem Kopf paßt -- hat ein"
                " Schritt nach hydration.py noch Tags geschrieben?"
            )
        tags = collect_tags(head, f)
        keep = bewahrte(head)
        if not any(t["s"] == 'link[rel="canonical"]' for t in tags):
            sys.exit(f"FEHLER: {f} hat keinen Canonical, den der Wächter halten könnte")
        for sel in keep:
            if BEWAHRT_RE[sel].search(head).start() > head.find(MARKER):
                sys.exit(
                    f"FEHLER: {f}: {sel} steht hinter dem Wächter -- der greift die"
                    " bewahrten Knoten beim Parsen, dann wäre dieser nicht dabei"
                )
        if 'script[type="application/ld+json"]' not in keep:
            sys.exit(f"FEHLER: {f} hat kein ld+json, das der Wächter bewahren könnte")
        n_tags += len(tags)
        n_keep += len(keep)
        found = read_payload(doc)
        if not found:
            sys.exit(f"FEHLER: {f} hat keine Hydrations-Nutzlast")
        for route in routes(found[0]):
            page = route.get("page")
            front = page.get("frontmatter") if isinstance(page, dict) else None
            for node in (front, route.get("project")):
                if not isinstance(node, dict):
                    continue
                for key in ("thumbnail", "thumbnailOptimized"):
                    url = node.get(key)
                    if isinstance(url, str) and url.startswith(f"{base}/build/"):
                        sys.exit(
                            f"FEHLER: {f}: {key} in der Nutzlast ist weiterhin relativ"
                            f" ({url}) -- og:image wäre nach der Hydration wieder relativ"
                        )
    print(
        f"✓ {len(pages)} Seiten: Dokument ganz, Nutzlast lesbar, Karte absolut; "
        f"{n_tags} Tags und {n_keep} bewahrte Knoten in den Wächtern, "
        "jeder passend zu seinem Kopf"
    )
    print("  (am Artefakt gemessen -- was der Browser daraus macht, sagt --check-rendered)")
    return 0


def check_rendered(root: pathlib.Path, lang: str, seiten: int) -> int:
    """Im echten Browser nachsehen, nach der Hydration. Nicht für die CI, siehe Docstring."""
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print(
            "FEHLER: --check-rendered braucht Playwright, und das Image installiert kein"
            " Python-Paket (CLAUDE.md, Entscheidung 5).\n"
            "  uv run --only-group dev python tools/hydration.py --check-rendered"
            " _build/html\n"
            "„nicht gemessen\" ist kein Erfolg, deshalb Rückgabewert 2."
        )
        return 2
    import functools
    import http.server
    import socketserver
    import threading

    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(root))
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("127.0.0.1", 0), handler) as srv:
        port = srv.server_address[1]
        threading.Thread(target=srv.serve_forever, daemon=True).start()
        ziele = sorted(root.rglob("index.html"))[:seiten]
        schlecht = 0
        with sync_playwright() as pw:
            browser = pw.chromium.launch()
            page = browser.new_page()
            for f in ziele:
                rel = f.parent.relative_to(root)
                # Die Landingpage als "/" ausgeben und nicht als "/./" -- sie wird auch
                # unter "/" geladen, und eine Ausgabe, die anders aussieht als die
                # Adresse, kostet beim Lesen eine Rueckfrage.
                pfad = "" if str(rel) == "." else f"{rel}/"
                url = f"http://127.0.0.1:{port}/" + pfad
                page.goto(url, wait_until="load")
                page.wait_for_timeout(6000)
                ist = page.evaluate(
                    "() => ({lang: document.documentElement.lang,"
                    " canonical: !!document.head.querySelector('link[rel=canonical]'),"
                    " ogurl: !!document.head.querySelector('meta[property=\"og:url\"]'),"
                    " ldjson: document.querySelectorAll"
                    "('script[type=\"application/ld+json\"]').length,"
                    " nocss: !!document.getElementById('myst-no-css'),"
                    " title: document.title})"
                )
                soll_titel = titel(head_slice(f.read_text(encoding="utf-8"), f), f)
                fehler = []
                if ist["lang"] != lang:
                    fehler.append(f"lang={ist['lang']!r}")
                if not ist["canonical"]:
                    fehler.append("kein Canonical")
                if not ist["ogurl"]:
                    fehler.append("kein og:url")
                if ist["ldjson"] != 1:
                    fehler.append(f"{ist['ldjson']} ld+json")
                if ist["title"] != soll_titel:
                    fehler.append(f"Titel {ist['title']!r} statt {soll_titel!r}")
                if ist["nocss"]:
                    fehler.append("myst-no-css nach der Hydration wieder da")
                if fehler:
                    schlecht += 1
                    print(f"✗ /{pfad} nach der Hydration: {', '.join(fehler)}")
                else:
                    print(f"✓ /{pfad}")
            browser.close()
        srv.shutdown()
    if schlecht:
        print(f"FEHLER: {schlecht} von {len(ziele)} Seiten verlieren Kopf-Angaben")
        return 1
    print(f"✓ {len(ziele)} Seiten halten nach der Hydration Sprache, Canonical, "
          "og:url, ld+json und Titel und tragen den myst-no-css-Kasten nicht mehr")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("site", nargs="?", help="Site-URL mit Basispfad, also $SITE")
    ap.add_argument("html_dir")
    ap.add_argument("--base", default="", help="BASE_URL, der Pfad, unter dem die Seite liegt")
    ap.add_argument("--lang", default="de", help="Sprache, die der Wächter hält")
    ap.add_argument("--check", action="store_true", help="nur am Artefakt nachmessen")
    ap.add_argument(
        "--check-rendered",
        action="store_true",
        help="im Browser nach der Hydration nachmessen (braucht Playwright)",
    )
    ap.add_argument("--seiten", type=int, default=4, help="wie viele Seiten --check-rendered lädt")
    args = ap.parse_args()

    root = pathlib.Path(args.html_dir)
    base = args.base.rstrip("/")

    if args.check_rendered:
        return check_rendered(root, args.lang, args.seiten)
    if args.check:
        return check(root, base, args.lang)

    if not args.site:
        sys.exit("FEHLER: ohne --check ist die Site-URL nötig")
    site = args.site.rstrip("/")
    if base and not site.endswith(base):
        sys.exit(f"FEHLER: {site} endet nicht auf {base} -- dann wäre die Origin geraten")

    pages = sorted(root.rglob("index.html"))
    if not pages:
        sys.exit(f"FEHLER: keine Seite unter {root}")

    n_card = n_tags = n_keep = 0
    for f in pages:
        doc = f.read_text(encoding="utf-8")
        doc, karte = absolute_card(doc, site, base)
        n_card += karte

        # Immer ans **Ende** des Kopfes, auch wenn schon einer drinsteht: der Wächter
        # greift die bewahrten Knoten beim Parsen per Selektor, also müssen sie vor ihm
        # stehen. Ein Ersetzen an alter Stelle ließe ihn vor einem <style>, das ein
        # späterer Schritt geschrieben hat.
        if MARKER in doc:
            doc = GUARD_RE.sub("", doc, count=1)
        head = head_slice(doc, f)
        tags = collect_tags(head, f)
        keep = bewahrte(head)
        script = guard_script(
            page_path(base, f.parent.relative_to(root)), tags, keep, args.lang,
            titel(head, f),
        )
        doc = doc.replace("</head>", script + "</head>", 1)
        n_tags += len(tags)
        n_keep += len(keep)

        whole(doc, f)
        f.write_text(doc, encoding="utf-8")

    print(
        f"hydration: {len(pages)} Seiten, Karte in der Nutzlast absolut ({n_card}), "
        f"{n_tags} Tags und {n_keep} bewahrte Knoten in den Wächtern"
    )
    return check(root, base, args.lang)


if __name__ == "__main__":
    raise SystemExit(main())
