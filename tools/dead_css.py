#!/usr/bin/env python3
"""Die Stylesheets, die dieses Buch nicht benutzen kann, nicht einbinden.

    python3 tools/dead_css.py <html-verzeichnis>
    python3 tools/dead_css.py <html-verzeichnis> --check

Das Theme bindet in **jede** Seite mehrere Stylesheets ein, davon zwei rendernde für
Jupyter-Ausgaben, die es hier nicht gibt:

    .../font-awesome/css/font-awesome.css  37 kB  Icons der ipywidgets-Views
    .../jupyter-matplotlib/mpl_widget.css 911 B   ipympl-Widget

**Seit dem Umstieg auf Theme 2.1.1 (2026-11-27) sind es zwei und nicht mehr drei.**
`thebe-core.css` (87 kB) war das größte Ziel und ist in 2.x **kein eingebundenes
Stylesheet mehr**: Die Datei liegt noch im Baum, verwiesen wird nicht mehr darauf, und
ihre Regeln stecken im Hauptstylesheet, das dadurch von 155 auf 237 kB wächst (brotli
16.684 auf 28.219 B). Dieser Schnitt ist also nicht mehr zu haben -- die eine Regel
daraus, an der in diesem Buch wirklich etwas hing (Schriftgröße und Zeilenhöhe der
Codeblöcke), steht seit dem 2026-11-16 ohnehin in `_site/custom-style.css` und ist
davon unberührt. Messung: `devnotes/build-log-2026-11-27-js.md`.

Dieses Buch hat **keine ausgeführte Zelle**: kein `vnd.jupyter.widget-view`, kein
`jupyter-output`, keine `myst-jp`-Klasse, kein `ipympl` in den 33 gebauten Seiten
(gemessen 2026-11-16, alle vier Marker null). Die interaktiven Teile sind
`{anywidget}`-ES-Module, die ohne Widget-Manager rendern. `tools/thebe_gate.py` hält
deshalb schon das *JavaScript* fern; das **CSS** räumte bis zum 2026-11-16 niemand weg.


Was gemessen wurde, bevor es entfernt wurde
-------------------------------------------

Nicht „welche Klasse kommt im Markup vor" -- das beantwortet die Frage nicht, weil ein
Blatt auch über CSS-Variablen wirken kann, die ein anderes Blatt benutzt. Gemessen wurde
mit **Ablation**: Blatt im Browser abschalten (`sh.disabled = true`), danach Geometrie und
alle Eigenschaften je Element vergleichen, die diese Blätter überhaupt setzen, samt
`::before`/`::after`, dazu ein Vollbild-Schnappschuß. Vier Seiten, hell und dunkel.

| Blatt | Elemente mit anderem Stil | Bild |
|---|---|---|
| `mpl_widget.css` | 0 von 447 / 10.323 / 8.974 / 2.093 | gleich |
| `font-awesome.css` | 2 (unsichtbar, siehe unten) | gleich |
| `thebe-core.css` | 5 / 12 / 12 / 35 | eine Stelle anders |

Zur Kontrolle dieselbe Messung an den Blättern, die wirken **müssen**: `app-*.css` ändert
alle 447 bzw. 10.323 Elemente, `myst-theme.css` 416 bzw. 10.155, `katex.min.css` 10.025 auf
einer Mathematikseite und null auf der Landingpage, die keine Formel hat. Ohne diese
Gegenprobe wäre die Null oben wertlos: die erste Fassung dieser Messung las
`getComputedStyle(el).cssText` -- in Chromium die leere Zeichenkette --, verglich also
lauter leere Strings und meldete für *jedes* Blatt null Unterschiede.

Die zwei Treffer von Font Awesome sind zwei `span.sr-only`, deren `border-*-color` sich von
`currentColor` (dessen `.sr-only{...;border:0}`) zu Tailwinds `gray-200` ändert. Die
Rahmenbreite ist in beiden Fällen 0, und die Elemente sind für Sehende ohnehin weggeclippt;
das Bild ist byte-gleich.

Bei thebe-core ist es **eine** Regel, und die trägt mehr, als sie aussieht:

    tt,code,kbd,samp,pre{font-family:var(--jp-code-font-family);
                         font-size:var(--jp-code-font-size);      /* 13px */
                         line-height:var(--jp-code-line-height)}  /* 1.3077 */

Unser eigenes Blatt setzt für dieselben Elemente nur die `font-family`. **Die Zeilenhöhe
jedes Codeblocks im Buch hing also an einem Stylesheet für Notebook-Ausgaben** -- ohne es
erben Codeblöcke die 1,75 des Fließtexts. Die Stichprobe von vier Seiten oben hat das
*nicht* gezeigt, weil keine davon einen langen Codeblock hat; der Vergleich zweier
Artefakte über alle 33 Seiten dann sehr wohl: `/autograd-berechnungsgraph/` wurde 219 px
länger (3.620 verschobene Elemente), `/faltung-cnn/` 123 px, `/autoencoder/` 144 px,
`/logistische-regression/` 132 px, insgesamt 12.339 Abweichungen -- bei einem
Rauschboden von **0** (dieselbe Messung A gegen A, also dieselbe Variante zweimal
geladen). Ohne diese Kontrolle wäre eine Seitenhöhe, die sich um 219 px unterscheidet,
auch als Ladezeit durchgegangen.

Deshalb stehen die beiden Werte seit dem 2026-11-16 in `_site/custom-style.css`
(`tt, code, kbd, samp, pre { font-size: 13px; line-height: 1.3077 }`, ohne
`.math-display` -- 13 px würden abgesetzte Formeln stauchen). Danach unterscheiden sich
die zwei Artefakte je Seite in genau **zwei** Elementen, und das sind die zwei
`span.sr-only` von Font Awesome oben.

Die zwei weiteren Stellen, die an der Regel hingen, sind damit auch unverändert: die zwei
`kbd` der Suchzeile (`CTRL`, `K`; 13 px, Kasten 27 px hoch -- ohne die Regel 14/30) und
`code` im `<dialog id="myst-no-css">`, den `tools/no_css_dialog.py` aus dem Markup nimmt
und den React bei der Hydration wieder einsetzt; er ist `display:none`.

Von den 1.200 Stilregeln der drei Blätter (481 + 710 + 9) trifft im gerenderten DOM genau
sieben überhaupt etwas, und das sind die hier genannten.


Warum es im JavaScript stehen muß und nicht nur im Markup
---------------------------------------------------------

Dieselbe Falle wie bei `tools/vendor_assets.py`: Remix rendert den `<head>` aus dem
`links()`-Export des Wurzel-Routenmoduls, und das steht als Array im Client-Bündel

    ()=>[{rel:"stylesheet",href:Be},{rel:"stylesheet",href:Le},{rel:"stylesheet",href:"...mpl_widget.css"},...]

Nur die `<link>`-Tags aus dem HTML zu nehmen hieße: die Seite lädt ohne sie und die
Hydration fügt sie wieder hinzu -- nichts gewonnen, dafür ein Unterschied zwischen erstem
Frame und Rest. Also beides, und `Be`/`Le` werden über ihre `var`-Definition in derselben
Datei aufgelöst, statt auf die Reihenfolge im Array zu vertrauen.


Warum es laut scheitert
-----------------------

Zwei Dinge können sich bewegen, und beide dürfen nicht still durchlaufen:

* **Das Theme.** Ein mystmd-Update kann das Array umbauen oder ein viertes Blatt
  hinzufügen. Gefordert ist deshalb: das Array genau einmal gefunden, jedes Ziel genau
  einmal je Seite, mindestens ein Eintrag bleibt übrig, und die Datei danach genau um die
  entfernten Teile kürzer. Was übrig bleibt, nennt die Meldung namentlich -- ein neues
  Blatt fällt damit im Protokoll auf.
* **Das Buch.** Bekommt ein Kapitel eine ausgeführte Zelle, ein ipywidget oder eine
  ipympl-Abbildung, sind diese Blätter nicht mehr totes Gewicht, sondern nötig. Dann
  **bricht dieser Schritt ab** und nennt Seite und Marker. Das ist die Richtung, in die er
  scheitern muß: ein Buch mit Widgets und ohne deren CSS sähe kaputt aus, und niemand
  weiter unten in der Kette würde es merken. Font Awesome und jupyter-matplotlib liegen
  dann nicht mehr in `_site/vendor/` (am 2026-11-16 entfernt, siehe PROVENANCE.txt) und
  müssen neu geholt werden; in der Historie stehen sie.

**Vor `tools/vendor_assets.py`**, denn dessen Nachbedingung ist, daß jedes vendorierte
Blatt auch eingebunden ist -- nach diesem Schritt wären es zwei weniger. In dieser
Reihenfolge trägt `vendor_assets.py` nur noch KaTeX, und die zwei CDN-URLs verlassen das
Artefakt hier. Deshalb prüft dieser Schritt am Ende selbst, daß **nichts** im Artefakt die
drei Blätter mehr einbindet: fände er hinterher noch einen Verweis, wäre aus einem
Datenschutzversprechen eine Zufallssache geworden.

Was es nicht behauptet: Es macht die Seite nicht meßbar schneller *im Feld* -- dazu gibt es
für diese Domain keine Felddaten (`devnotes/seo-audit-2026-11-15.md` §11). Es nimmt drei
rendernde Anfragen und rund 14 kB über die Leitung weg; das ist eine Messung am Artefakt
und an der Wasserfall-Ansicht, keine über Nutzer gemittelte Ladezeit.
"""

import argparse
import pathlib
import re
import sys

# Je Ziel: ein sprechender Name und ein Muster, das die URL in **jeder** Fassung trifft --
# die vom CDN wie die von `vendor_assets.py` umgeschriebene, mit jedem BASE_URL davor.
# Damit ist dieser Schritt gegen die Reihenfolge robust, auch wenn er vor vendor_assets
# gehoert.
ZIELE = {
    # Vom CDN, oder schon von vendor_assets.py auf den eigenen Pfad umgeschrieben --
    # mit beliebigem BASE_URL davor.
    "font-awesome": re.compile(
        r"(?:https://cdnjs\.cloudflare\.com/ajax/libs/font-awesome/[\d.]+/css"
        r"|[\w./-]*/vendor/font-awesome/css)/font-awesome\.css"
    ),
    "mpl_widget": re.compile(
        r"(?:https://cdn\.jsdelivr\.net/npm/jupyter-matplotlib@[\d.]+/css"
        r"|[\w./-]*/vendor/jupyter-matplotlib)/mpl_widget\.css"
    ),
}

# Ein <link rel="stylesheet" ...> als ganzes Tag, in beiden Attributreihenfolgen.
LINK = re.compile(r'<link\b[^>]*\brel="stylesheet"[^>]*>', re.I)
HREF = re.compile(r'\bhref="([^"]*)"', re.I)

# Der links()-Export des Wurzel-Routenmoduls: ein Pfeilausdruck, der ein Array aus
# {rel:"stylesheet",href:...} liefert. Auf die Form verankert, nicht auf Namen -- die sind
# minifiziert und wechseln mit jeder Theme-Fassung.
# `Q` statt eines festen Anfuehrungszeichens: Der Buendler von Theme 1.4.x schreibt
# Zeichenketten doppelt gequotet, der von 2.x in Backticks (gemessen 2026-11-27:
# ``()=>[{rel:`stylesheet`,href:`https://...mpl_widget.css`},...]``).
Q = r"[\"'`]"
ARRAY = re.compile(
    r"\(\)=>\[(\{rel:" + Q + r"stylesheet" + Q + r",href:[^}]+\}"
    r"(?:,\{rel:" + Q + r"stylesheet" + Q + r",href:[^}]+\})*)\]"
)
EINTRAG = re.compile(
    r"\{rel:" + Q + r"stylesheet" + Q + r",href:"
    r"(?P<href>\"[^\"]*\"|`[^`]*`|[A-Za-z0-9_$]+)\}"
)

# In Theme 2.x fuehrt das Array **nur** die zwei Ziele; nach dem Raeumen ist es leer, und
# ein leeres `()=>[]` ist als Muster nicht brauchbar -- jedes zweite Buendel enthaelt so
# einen Pfeilausdruck. Das geraeumte Array traegt deshalb diesen Marker, damit `--check`
# und ein zweiter Lauf dieselbe Datei wiederfinden.
GERAEUMT = "/*eidl:dead_css*/"

# Marker dafuer, dass das Buch doch etwas Ausfuehrbares enthaelt. Dann sind diese
# Blaetter nicht tot, und dieser Schritt darf nicht laufen.
MARKER = {
    "vnd.jupyter.widget-view": "eine ipywidgets-Ausgabe",
    "jupyter-output": "eine Notebook-Ausgabe im Markup",
    "myst-jp": "eine Seite mit Jupyter-Klassen",
    '"type":"output"': "ein Ausgabeknoten in der Nutzlast",
    '\\"type\\":\\"output\\"': "ein Ausgabeknoten in der escapeten Nutzlast",
    # Thebes eigene Bedingung ist `computables.length > 0 || kind === Notebook`: eine
    # Notebook-Seite *ohne* Ausgabe gilt ihm auch als ausfuehrbar, und dann erscheinen
    # seine Knoepfe, die Font Awesome brauchen. Deshalb auch darauf.
    '"kind":"Notebook"': "eine Seite, die MyST als Notebook fuehrt",
    '\\"kind\\":\\"Notebook\\"': "eine Notebook-Seite in der escapeten Nutzlast",
}


def seiten(wurzel: pathlib.Path) -> list[pathlib.Path]:
    """Die Seiten des Buchs: jede ist eine `index.html`, in der Wurzel oder im Slug-Ordner.

    **Nicht `*.html`.** Im Artefakt des `pages`-Jobs liegt daneben die
    Google-Verifikationsdatei (`google<token>.html`, eine Zeile Text ohne Kopf), und mit
    ihr sind es 34 Dateien statt 33. Der erste Deploy dieses Schritts ist genau daran
    gescheitert -- „thebe-core stand in 33 von 34 Seiten, erwartet in allen oder in
    keiner" (Pipeline #185807). Das war die Nachbedingung, die richtig anschlug, und die
    Lehre ist die Zaehlung: `head_meta.py`, `publish_urls.py`, `image_dims.py` und
    `check_css_assets.py` zaehlen laengst ueber `index.html`, und hier war der Grund dafuer
    lokal nicht sichtbar, weil die Testkopie die Verifikationsdatei nicht enthielt.
    """
    return sorted(wurzel.rglob("index.html"))


def stylesheet_hrefs(seite: pathlib.Path) -> list[str]:
    """Die href jedes `<link rel="stylesheet">` einer Seite, in Reihenfolge."""
    if not seite.is_file():
        return []
    text = seite.read_text(encoding="utf-8", errors="replace")
    out = []
    for tag in LINK.findall(text):
        m = HREF.search(tag)
        if m:
            out.append(m.group(1))
    return out


def ziel_von(url: str) -> str | None:
    """Welches Ziel diese href ist, oder None."""
    for name, muster in ZIELE.items():
        if muster.fullmatch(url):
            return name
    return None


def pruefe_marker(dateien: list[pathlib.Path], wurzel: pathlib.Path) -> list[str]:
    """Seiten, die doch etwas Ausfuehrbares tragen -- je Fund eine Zeile.

    Mit dem Pfad relativ zur Wurzel, nicht mit dem Dateinamen: die heissen alle
    index.html, und "index.html: ..." nennt die Seite nicht.
    """
    funde = []
    for f in dateien:
        text = f.read_text(encoding="utf-8", errors="replace")
        for marker, was in MARKER.items():
            if marker in text:
                funde.append(f"{f.relative_to(wurzel)}: {marker} -- {was}")
    return funde


def links_im_markup(dateien: list[pathlib.Path]) -> dict[str, int]:
    """Wie oft jedes Ziel als <link> eingebunden ist, ueber alle Seiten."""
    zahl = {name: 0 for name in ZIELE}
    for f in dateien:
        for tag in LINK.findall(f.read_text(encoding="utf-8", errors="replace")):
            m = HREF.search(tag)
            if m and (name := ziel_von(m.group(1))):
                zahl[name] += 1
    return zahl


def raeume_markup(dateien: list[pathlib.Path]) -> tuple[dict[str, int], list[str]]:
    """Die <link>-Tags der Ziele aus jeder Seite nehmen."""
    zahl = {name: 0 for name in ZIELE}
    schief = []
    for f in dateien:
        text = f.read_text(encoding="utf-8")
        hier = {name: 0 for name in ZIELE}

        def weg(m: re.Match) -> str:
            h = HREF.search(m.group(0))
            if h and (name := ziel_von(h.group(1))):
                hier[name] += 1
                return ""
            return m.group(0)

        neu = LINK.sub(weg, text)
        for name, n in hier.items():
            if n > 1:
                schief.append(f"{f.parent.name or '/'}: {name} {n}-mal eingebunden, "
                              "erwartet einmal")
            zahl[name] += n
        if neu != text:
            f.write_text(neu, encoding="utf-8")
    return zahl, schief


def aufloesen(js: str, href: str) -> str:
    """Den href eines Array-Eintrags zu einer URL machen: Zeichenkette oder Variable."""
    if href[:1] in ('"', "`"):
        return href[1:-1]
    m = re.search(
        r"(?:var|let|const)\s+" + re.escape(href) + r"\s*=\s*" + Q + r"([^\"'`]*)" + Q,
        js,
    )
    return m.group(1) if m else ""


def chunk_mit_array(wurzel: pathlib.Path) -> pathlib.Path:
    """Den einen Client-Chunk finden, der das links()-Array traegt."""
    kandidaten = []
    for f in sorted(wurzel.rglob("*.js")):
        text = f.read_text(encoding="utf-8", errors="replace")
        if ARRAY.search(text) or GERAEUMT in text:
            kandidaten.append(f)
    if len(kandidaten) != 1:
        sys.exit(
            f"::error::dead_css: {len(kandidaten)} Chunks mit einem "
            f"links()-Stylesheet-Array gefunden, erwartet genau einen "
            f"{[str(f) for f in kandidaten]}\n"
            "  Das Theme hat seine Kopf-Links umgebaut. Docstring lesen: dieser Schritt "
            "muss scheitern, statt rendernde Blaetter still weiterzuliefern."
        )
    return kandidaten[0]


def ziele_im_bundle(ziel: pathlib.Path) -> dict[str, int]:
    """Wie oft die Ziele im links()-Array stehen -- nur lesen, fuer --check."""
    js = ziel.read_text(encoding="utf-8", errors="replace")
    m = ARRAY.search(js)
    if m is None:
        # Entweder geraeumt (Marker) oder gar nicht da; beides heisst: keines der Ziele
        # steht noch im Array. Ob die Datei die richtige ist, hat chunk_mit_array geklaert.
        return {name: 0 for name in ZIELE}
    zahl = {name: 0 for name in ZIELE}
    for e in EINTRAG.finditer(m.group(1)):
        if name := ziel_von(aufloesen(js, e.group("href"))):
            zahl[name] += 1
    return zahl


def raeume_bundle(wurzel: pathlib.Path) -> tuple[pathlib.Path, dict[str, int], list[str]]:
    """Die Eintraege der Ziele aus dem links()-Array des Wurzel-Chunks nehmen."""
    ziel = chunk_mit_array(wurzel)
    js = ziel.read_text(encoding="utf-8")
    if ARRAY.search(js) is None and GERAEUMT in js:
        return ziel, {name: 0 for name in ZIELE}, []

    treffer = list(ARRAY.finditer(js))
    if len(treffer) != 1:
        sys.exit(
            f"::error::dead_css: {ziel.name} enthaelt das Array {len(treffer)}-mal, "
            "erwartet einmal"
        )

    m = treffer[0]
    eintraege = list(EINTRAG.finditer(m.group(1)))
    if not eintraege:
        sys.exit(f"::error::dead_css: {ziel.name}: Array ohne Eintraege")

    zahl = {name: 0 for name in ZIELE}
    bleibt = []
    for e in eintraege:
        url = aufloesen(js, e.group("href"))
        if not url:
            sys.exit(
                f"::error::dead_css: {ziel.name}: href {e.group('href')} laesst sich "
                "nicht aufloesen -- keine var-Definition dazu in derselben Datei"
            )
        if name := ziel_von(url):
            zahl[name] += 1
        else:
            bleibt.append((e.group(0), url))

    if not bleibt:
        # In Theme 1.4.x stand das Hauptstylesheet selbst in diesem Array, ein leeres
        # Array waere dort also ein Unfall gewesen. In 2.x fuehrt das Array nur die zwei
        # CDN-Blaetter, und das Hauptstylesheet haengt im Markup -- leer ist dann richtig.
        # Gepruefte Bedingung ist deshalb nicht mehr "ein Eintrag bleibt", sondern: die
        # Seite bindet weiterhin ein Stylesheet ein, das keines der Ziele ist.
        fremd = [u for u in stylesheet_hrefs(wurzel / "index.html")
                 if ziel_von(u) is None]
        if not fremd:
            sys.exit(
                f"::error::dead_css: {ziel.name}: nach dem Raeumen bliebe weder im Array "
                "noch im Markup der Startseite ein Stylesheet uebrig. So war das nicht "
                "gemeint -- das Hauptstylesheet traegt das gesamte Theme."
            )

    neues_array = ("()=>[" + ",".join(t for t, _ in bleibt) + "]" if bleibt
                   else "()=>[" + GERAEUMT + "]")
    neu = js[: m.start()] + neues_array + js[m.end():]
    entfernt = len(js) - len(neu)
    erwartet = len(m.group(0)) - len(neues_array)
    if entfernt != erwartet:
        sys.exit(
            f"::error::dead_css: {ziel.name} hat sich um {entfernt} Bytes geaendert, "
            f"erwartet {erwartet} -- die Ersetzung hat mehr getroffen als das Array"
        )
    if neu != js:
        ziel.write_text(neu, encoding="utf-8")
    return ziel, zahl, [u for _, u in bleibt]


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("verzeichnis")
    p.add_argument("--check", action="store_true",
                   help="nur pruefen, dass keines dieser Blaetter eingebunden ist")
    args = p.parse_args()

    wurzel = pathlib.Path(args.verzeichnis)
    dateien = seiten(wurzel)
    if not dateien:
        print(f"FEHLER: keine HTML-Datei unter {wurzel}")
        return 1

    if args.check:
        # Beides pruefen, Markup und Buendel: ein Theme-Update koennte die Links nur im
        # einen von beiden zurueckbringen, und im Buendel saehe man es erst nach der
        # Hydration.
        zahl = links_im_markup(dateien)
        chunk = chunk_mit_array(wurzel)
        im_js = ziele_im_bundle(chunk)
        uebrig = {n: (zahl[n], im_js[n]) for n in ZIELE if zahl[n] or im_js[n]}
        if uebrig:
            print("dead_css --check: noch eingebunden: " + ", ".join(
                f"{n} {k}-mal im Markup, {j}-mal in {chunk.name}"
                for n, (k, j) in uebrig.items()))
            return 1
        print(f"dead_css --check: keines der {len(ZIELE)} Blaetter wird von den "
              f"{len(dateien)} Seiten oder von {chunk.name} eingebunden")
        return 0

    funde = pruefe_marker(dateien, wurzel)
    if funde:
        print("::error::dead_css: dieses Buch hat jetzt Ausfuehrbares -- diese "
              "Blaetter sind nicht mehr totes Gewicht:")
        for f in funde[:10]:
            print(f"  {f}")
        print(
            "  Also: diesen Schritt aus dem pages-Job nehmen, font-awesome und "
            "jupyter-matplotlib wieder nach _site/vendor/ holen (Historie, "
            "PROVENANCE.txt) und in ASSETS von tools/vendor_assets.py eintragen."
        )
        return 1

    markup, schief = raeume_markup(dateien)
    if schief:
        print("::error::dead_css: unerwartete Zahl von Einbindungen:")
        for s in schief[:10]:
            print(f"  {s}")
        return 1

    ziel, bundle, bleibt = raeume_bundle(wurzel)

    rest = links_im_markup(dateien)
    if any(rest.values()):
        print("::error::dead_css: nach dem Raeumen bindet das Artefakt noch ein: "
              + ", ".join(f"{n} {k}-mal" for n, k in rest.items() if k))
        return 1

    for name in ZIELE:
        if markup[name] and markup[name] != len(dateien):
            print(f"::error::dead_css: {name} stand in {markup[name]} von "
                  f"{len(dateien)} Seiten, erwartet in allen oder in keiner")
            return 1

    bleibt_text = ", ".join(bleibt)
    if sum(markup.values()) + sum(bundle.values()):
        je_ziel = ", ".join(f"{n}={markup[n]}+{bundle[n]}" for n in ZIELE)
        print(f"✓ dead_css: {sum(markup.values())} <link> aus {len(dateien)} Seiten und "
              f"{sum(bundle.values())} Eintraege aus {ziel.name} entfernt ({je_ziel}); "
              f"eingebunden bleiben: {bleibt_text}")
    else:
        print(f"✓ dead_css: schon weg -- keines der drei Blaetter in den {len(dateien)} "
              f"Seiten, {ziel.name} bindet nur {bleibt_text} ein")
    return 0


if __name__ == "__main__":
    sys.exit(main())
