#!/usr/bin/env python3
"""Die drei fremden Stylesheets des Themes von dieser Herkunft ausliefern, nicht von zwei CDN.

    python3 tools/vendor_assets.py <html-dir> [--base BASE_URL]

Jede Seite holte drei rendernde Stylesheets von `cdn.jsdelivr.net` und
`cdnjs.cloudflare.com`, und jede Seite mit Mathematik dazu bis zu zwanzig
Schriftdateien von jsdelivr -- die zieht das KaTeX-Stylesheet relativ zu seiner *eigenen*
URL, sie stehen also in keinem HTML und sind von aussen nur im Netzwerkprotokoll zu
sehen. Das ist ein Dritter, der die IP-Adresse jedes Lesers eines Buchs mit einem
Datenschutzkapitel haelt -- dasselbe Argument, das `_site/fonts/PROVENANCE.txt` ueber den
Google-Fonts-`@import` macht.

Der Unterschied ist, wessen Markup es ist. Der `@import` war Zeile 3 unseres eigenen
Stylesheets und liess sich loeschen. Diese `<link>`-Tags gehoeren dem MyST-Book-Theme,
werden also nach dem Bau umgeschrieben -- das ist dieses Werkzeug. Die Dateien selbst
liegen unveraendert in `_site/vendor/`, mit Hashes und Lizenzen.


Der Teil, der das mehr als ein sed macht
----------------------------------------

**Die URLs stehen auch im Client-JavaScript, nicht nur im HTML.** Remix rendert die
`<head>`-Links aus Route-Modulen, das Bundle traegt also dieselben drei URLs. Nur das
servergerenderte Markup umzuschreiben hiesse: die Seite laedt richtig und fuegt bei der
Hydration die CDN-Links wieder hinzu -- holt also beide Kopien, was schlechter ist als
vorher und unsichtbar, wenn man nicht ins Netzwerkprotokoll sieht.

Deshalb deckt die Umschreibung `.html` und `.js` gleichermassen ab, und der Waechter
greppt das ganze Artefakt, nicht nur das HTML.


Warum es scheitert statt zurueckzufallen
----------------------------------------

Jede URL wird von einem Muster getroffen, das *jede* Version erlaubt. Ein
MyST-Upgrade, das KaTeX hochzieht, wird damit als genau das gemeldet -- "das Theme will
katex@0.16.0, _site/vendor hat 0.15.2" -- und nicht als Zeichenkette, die nicht gefunden
wurde. Dann endet es mit einem Fehler.

Das ist Absicht. Das verlockende Verhalten waere, eine unbekannte Version auf dem CDN
stehen zu lassen, damit der Bau weiterlaeuft; das stellt stillschweigend genau das
wieder her, wofuer dieses Verzeichnis existiert.


Was das *nicht* entfernt, und nicht zu behaupten hat
----------------------------------------------------

Danach stehen die zwei CDN-Hostnamen weiter in den thebe-Bundles, und das ist richtig:
das ist thebes Laufzeit -- der Python-Kernel im Browser und der Lader fuer
Jupyter-Widget-Pakete -- und die wird erst geholt, wenn ein Leser den Knopf drueckt, der
ein Notebook lebendig macht. Pyodide allein sind Dutzende Megabyte vor jedem Paket; das
zu vendorieren steht nicht zur Debatte, und wer darum gebeten hat, Python im Browser
laufen zu lassen, hat per Definition um einen Netzabruf gebeten.

Die zutreffende Aussage ist also eng, und sie ist eng zu formulieren: **Das Buch zu lesen
kontaktiert keinen Dritten. Den Code darin laufen zu lassen schon.**

Der Waechter greppt deshalb die drei Stylesheet-URLs und **nicht die Hostnamen** -- ein
Waechter, der bei jeder Erwaehnung von jsdelivr anschlaegt, waere nur zu befriedigen,
indem man thebe loescht.

(`vendor/PROVENANCE.txt` zitiert alle drei URLs ebenfalls, als die Datei, die sie
erklaert. Sie wird mit den Lizenzen veroeffentlicht, wie die OFL es fuer die
Font-Awesome-Schrift verlangt, und nicht umgeschrieben: nur `.html` und `.js`.)


`integrity` und `crossorigin` fallen weg
----------------------------------------

Das Theme emittiert den KaTeX-Link mit einem SRI-Hash und `crossorigin="anonymous"`. Der
Hash wuerde tatsaechlich weiter stimmen -- die vendorierte Datei ist byte-exakt, und das
wurde *gegen genau diesen Hash* geprueft --, er wird aber trotzdem entfernt, mit dem
Attribut dazu. Ein Hash, der auf eine Version einer Datei gepinnt ist, die jetzt in
diesem Repository liegt, ist eine Stolperfalle fuer den Naechsten, der sie aktualisiert:
das Stylesheet wuerde nicht laut scheitern, es wuerde einfach blockiert, und die Seite
verloere ihren Mathematiksatz, ohne dass im Baulog etwas steht. Artefakte derselben
Herkunft deckt hier das Repository ab, nicht SRI.
"""

from __future__ import annotations

import argparse
import pathlib
import re
import shutil
import sys

# Je Eintrag: ein Muster, das die URL des Themes mit *jeder* Version trifft, die
# tatsaechlich vendorierte Version, und der Pfad, auf den umgeschrieben wird (relativ
# zur Wurzel der Seite).
ASSETS = [
    (
        r"https://cdn\.jsdelivr\.net/npm/katex@([\d.]+)/dist/katex\.min\.css",
        "0.15.2",
        "vendor/katex/katex.min.css",
    ),
    (
        r"https://cdnjs\.cloudflare\.com/ajax/libs/font-awesome/([\d.]+)/css/font-awesome\.css",
        "4.7.0",
        "vendor/font-awesome/css/font-awesome.css",
    ),
    (
        r"https://cdn\.jsdelivr\.net/npm/jupyter-matplotlib@([\d.]+)/css/mpl_widget\.css",
        "0.11.3",
        "vendor/jupyter-matplotlib/mpl_widget.css",
    ),
]

VENDOR_SRC = pathlib.Path("_site/vendor")

# **Nur die Unterbaeume kopieren, die oben auch referenziert werden**, und nicht wie in
# ds-skript den ganzen `_site/vendor`. Hier liegt daneben naemlich `book-theme.zip` (20 MB,
# das mitgelieferte Site-Template) und `install_template.py` -- ein `copytree` ueber alles
# wuerde beides mitveroeffentlichen. Die Liste leitet sich aus ASSETS ab, kann also nicht
# auseinanderlaufen: was nicht referenziert wird, wird auch nicht ausgeliefert.
VENDOR_DIRS = sorted({pathlib.PurePosixPath(local).parts[1] for _, _, local in ASSETS})


def strip_integrity(doc: str, local: str) -> str:
    """integrity= und crossorigin= an einem <link> entfernen, der jetzt lokal zeigt."""

    def fix(m: re.Match) -> str:
        tag = m.group(0)
        if local not in tag:
            return tag
        tag = re.sub(r'\s+integrity="[^"]*"', "", tag)
        tag = re.sub(r'\s+crossorigin="[^"]*"', "", tag)
        return tag

    return re.sub(r"<link\b[^>]*>", fix, doc)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("html_dir")
    ap.add_argument("--base", default="", help="BASE_URL, der Pfad, unter dem die Seite liegt")
    args = ap.parse_args()

    root = pathlib.Path(args.html_dir)
    if not (root / "index.html").exists():
        sys.exit(f"FEHLER: {root}/index.html existiert nicht; nach dem HTML-Bau laufen lassen")
    if not VENDOR_SRC.is_dir():
        sys.exit(f"FEHLER: {VENDOR_SRC} fehlt; dort liegen die eingecheckten Stylesheets")

    for name in VENDOR_DIRS:
        src = VENDOR_SRC / name
        if not src.is_dir():
            sys.exit(f"FEHLER: {src} fehlt; dort liegt das eingecheckte Stylesheet")
        shutil.copytree(src, root / "vendor" / name, dirs_exist_ok=True)
    vendored = sum(1 for p in (root / "vendor").rglob("*") if p.is_file())

    files = [p for p in root.rglob("*") if p.suffix in (".html", ".js") and p.is_file()]
    counts = {local: 0 for _, _, local in ASSETS}
    referenced = {local: False for _, _, local in ASSETS}

    for f in files:
        try:
            doc = f.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        before = doc
        for pattern, want, local in ASSETS:
            for version in set(re.findall(pattern, doc)):
                if version != want:
                    sys.exit(
                        f"FEHLER: {f} will Version {version} von {local.split('/')[1]}, "
                        f"_site/vendor hat aber {want}. Das Theme wurde hochgezogen: "
                        f"dieses Stylesheet und seine Schriften neu holen, die Hashes "
                        f"pruefen und _site/vendor/PROVENANCE.txt sowie ASSETS in dieser "
                        f"Datei nachziehen."
                    )
            doc, n = re.subn(pattern, f"{args.base}/{local}", doc)
            counts[local] += n
            if f"{args.base}/{local}" in doc:
                referenced[local] = True
        if doc != before:
            if f.suffix == ".html":
                for _, _, local in ASSETS:
                    doc = strip_integrity(doc, local)
            f.write_text(doc, encoding="utf-8")

    # Nachbedingungen, keine Bilanz dieses Laufs: zweimal laufen ist ein zulaessiger
    # Leerlauf, der bestehen muss, waehrend ein Theme, das eines davon nicht mehr laedt
    # -- oder es aus einer URL laedt, die diese Muster verfehlen --, auffallen muss.
    missing = [local for local, ok in referenced.items() if not ok]
    if missing:
        sys.exit(
            "FEHLER: nichts im Build referenziert diese, vor oder nach der Umschreibung: "
            f"{', '.join(missing)}. Entweder laedt das Theme sie nicht mehr -- dann aus "
            "ASSETS und aus _site/vendor werfen -- oder es laedt sie jetzt aus einer URL, "
            "die diese Muster nicht treffen, und das CDN wird weiter angefragt."
        )

    # Jede vendorierte Datei muss unter dem Pfad erreichbar sein, den die Umschreibung nennt.
    for _, _, local in ASSETS:
        if not (root / local).is_file():
            sys.exit(f"FEHLER: Referenzen auf /{local} umgeschrieben, das liegt nicht im Artefakt")

    breakdown = ", ".join(f"{local.split('/')[1]}={counts[local]}" for _, _, local in ASSETS)
    print(
        f"vendor_assets: {vendored} Dateien nach /vendor kopiert, "
        f"{sum(counts.values())} CDN-Referenzen in {len(files)} html/js-Dateien "
        f"umgeschrieben ({breakdown})"
    )


if __name__ == "__main__":
    main()
