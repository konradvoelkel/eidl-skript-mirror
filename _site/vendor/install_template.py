#!/usr/bin/env python3
"""Legt das mitgelieferte Site-Template dort ab, wo `myst build` es erwartet.

Hintergrund: MyST laedt das Site-Template bei jedem Lauf von
`https://github.com/myst-templates/book-theme/archive/refs/heads/main.zip`
nach — von einem *Branch*, nicht von einem Tag. Damit ist das Aussehen der Seite
eine unversionierte Abhaengigkeit an fremdem `main`, und jeder Netzausfall bricht
den Build (so am 2026-09-24/25 dreimal in Folge).

`site.template` kann in `myst.yml` **keinen** lokalen Pfad aufnehmen: Der Wert wird
als Template-*Name* gegen api.mystmd.org aufgeloest, und `file://`-URLs lehnt
node-fetch ab. Was funktioniert, ist das Verzeichnis vorzubelegen, in dem MyST das
Template zwischenspeichert — dann laedt es nichts nachher.

Genau das tut dieses Skript. Es ist idempotent und braucht kein Netz.

Danach setzt es **deutsche Kastennamen** ein (seit 2026-11-02): Das Template schreibt in
den Kopf jedes `{prf:…}`-Kastens das `kind` mit großem Anfangsbuchstaben, also „Example 1“,
„Theorem 2“. Dieselbe Stelle steht zweimal im Template, im Bündel fürs Server-Rendering
(`build/index.js`) und in dem für den Browser (`public/build/_shared/…`); beide werden
gepatcht, sonst schreibt der Browser beim Hydrieren das Englische zurück. Gesucht wird nach
Struktur, nicht nach den minifizierten Namen; findet sich die Stelle nicht genau einmal je
Bündel, endet das Skript mit Fehler — dann hat sich das Template bewegt. Das PDF repariert
`devnotes/patch_myst_tex.py`.

Ebenso übersetzt es die **Bedienung** (seit 2026-11-02): Suche, Sprunglinks, Download-Menü,
Kopierknöpfe und die Beschriftungen für Screenreader. Jede Ersetzung ist ein genaues Muster
mit Kontext (`placeholder:"Search"`, nicht `"Search"` – dasselbe Wort ist im Suchdialog
auch ein interner Zustandsname), und jedes Muster muss im Server-Bündel genauso oft stehen
wie in den Browser-Bündeln, mindestens einmal. Eigennamen („Open Access“) und Wörter, die
im Deutschen gleich lauten („Navigation“, „Downloads“), bleiben.

Aufruf (vor `myst build`):

    python _site/vendor/install_template.py
"""

from __future__ import annotations

import re
import shutil
import sys
import zipfile
from pathlib import Path

WURZEL = Path(__file__).resolve().parent.parent.parent
ARCHIV = WURZEL / "_site" / "vendor" / "book-theme.zip"
ZIEL = WURZEL / "_build" / "templates" / "site" / "myst" / "book-theme"

# Woran man erkennt, dass MyST das Template als vorhanden ansieht. Liegt eine
# dieser Dateien eine Ebene zu tief (im `book-theme-main/` des Archivs), laedt
# MyST trotzdem neu — deshalb wird der Wrapper beim Entpacken entfernt.
MARKER = "template.yml"

# Deutsche Namen der prf-Kästen; was hier fehlt, behält den englischen Namen.
KASTENNAMEN = {
    "proof": "Beweis", "theorem": "Satz", "lemma": "Lemma", "definition": "Definition",
    "example": "Beispiel", "remark": "Bemerkung", "corollary": "Folgerung",
    "proposition": "Proposition", "axiom": "Axiom", "conjecture": "Vermutung",
    "observation": "Beobachtung", "algorithm": "Algorithmus", "exercise": "Aufgabe",
}
KOPF = re.compile(r'kind:(\w+)\((\w)\),children:\[\1\(\2\)," ",(\w)\]')
GEPATCHT = "/*eidl:kastennamen*/"

# (Muster, Ersatz, Prüftext): Prüftext steht nach dem Ersetzen im Bündel und zeigt einen
# früheren Lauf an. Die Muster sind reguläre Ausdrücke; Gruppen werden mitgenommen.
BEDIENUNG = [
    (r'"Skip to article frontmatter"', '"Zum Artikelkopf springen"', "Zum Artikelkopf springen"),
    (r'"Skip to article content"', '"Zum Inhalt springen"', "Zum Inhalt springen"),
    (r'"skip to content options"', '"Sprungmarken"', '"Sprungmarken"'),
    (r'"article frontmatter"', '"Artikelkopf"', '"Artikelkopf"'),
    (r'placeholder:"Search"', 'placeholder:"Suchen"', 'placeholder:"Suchen"'),
    (r'children:"Search"\}', 'children:"Suche"}', 'children:"Suche"}'),
    (r'"Search Website"', '"Website durchsuchen"', "Website durchsuchen"),
    (r'"Search articles and their contents using fuzzy-search and prefix-matching"',
     '"Durchsucht Titel und Text aller Kapitel; ungefähre Schreibweise und Wortanfänge genügen"',
     "Wortanfänge genügen"),
    (r'"No results found\."', '"Keine Treffer."', '"Keine Treffer."'),
    (r'title:"Download"\}', 'title:"Herunterladen"}', 'title:"Herunterladen"}'),
    (r'children:\["Download",(\w)\?` as \$\{\1\}`:""',
     r'children:["Herunterladen",\1?` (${\1})`:""', 'children:["Herunterladen",'),
    (r'children:\["Visit URL ",', 'children:["Öffnen: ",', 'children:["Öffnen: ",'),
    (r'"Open Menu"', '"Menü öffnen"', '"Menü öffnen"'),
    (r'"aria-label":"Table of Contents"', '"aria-label":"Inhaltsverzeichnis"', '"aria-label":"Inhaltsverzeichnis"'),
    (r'"Open Folder"', '"Ordner öffnen"', '"Ordner öffnen"'),
    (r'"Toggle theme between light and dark mode"', '"Zwischen hellem und dunklem Design wechseln"',
     "Zwischen hellem und dunklem Design wechseln"),
    (r'"Launch in external computing interface"', '"In externer Rechenumgebung starten"',
     "In externer Rechenumgebung starten"),
    (r'"Copied!!":"Copy to Clipboard"', '"Kopiert":"In die Zwischenablage kopieren"',
     '"Kopiert":"In die Zwischenablage kopieren"'),
    (r'"Copy code to clipboard"', '"Code in die Zwischenablage kopieren"', "Code in die Zwischenablage kopieren"),
    (r'defaultMessage:"Copy Link",copiedMessage:"Link Copied"',
     'defaultMessage:"Link kopieren",copiedMessage:"Link kopiert"', 'copiedMessage:"Link kopiert"'),
    (r'"Author Details"', '"Zur Person"', '"Zur Person"'),
    (r'"Document Outline"', '"Gliederung"', '"Gliederung"'),
    (r'"Open Contents"', '"Inhaltsverzeichnis öffnen"', '"Inhaltsverzeichnis öffnen"'),
    (r'preamble:"Content License: "', 'preamble:"Lizenz: "', 'preamble:"Lizenz: "'),
    (r'"table content"', '"Tabelleninhalt"', '"Tabelleninhalt"'),
    (r'="Contents",top:', '="Inhalt",top:', '="Inhalt",top:'),
    (r'"Previous: ":"Next: "', '"Zurück: ":"Weiter: "', '"Zurück: ":"Weiter: "'),
    (r'`Link to this \$\{(\w)\}`', '`Link zu dieser Stelle`', "`Link zu dieser Stelle`"),
    (r'"aria-label":"Close"', '"aria-label":"Schließen"', '"aria-label":"Schließen"'),
    (r'"aria-label":"code block content"', '"aria-label":"Codeblock"', '"aria-label":"Codeblock"'),
    # Erläuterungen an den Lizenz-Symbolen; der Lizenzname selbst bleibt der offizielle.
    (r'title:"Credit must be given to the creator"', 'title:"Namensnennung erforderlich"',
     'title:"Namensnennung erforderlich"'),
    (r'title:"Adaptations must be shared under the same terms"',
     'title:"Bearbeitungen nur unter denselben Bedingungen weitergeben"', "unter denselben Bedingungen weitergeben"),
    (r'title:"Only noncommercial uses of the work are permitted"', 'title:"Nur nicht kommerzielle Nutzung erlaubt"',
     'title:"Nur nicht kommerzielle Nutzung erlaubt"'),
    (r'title:"No derivatives or adaptations of the work are permitted"', 'title:"Keine Bearbeitungen erlaubt"',
     'title:"Keine Bearbeitungen erlaubt"'),
    (r'title:"CC0: Work is in the worldwide public domain"', 'title:"CC0: gemeinfrei"', 'title:"CC0: gemeinfrei"'),
]


def bedienung_eindeutschen() -> int:
    """Übersetzt die Bedientexte des Templates, in Server- und Browser-Bündeln gleich oft."""
    server = ZIEL / "build" / "index.js"
    browser = sorted((ZIEL / "public" / "build").rglob("*.js"))
    texte = {p: p.read_text(encoding="utf-8", errors="surrogateescape") for p in [server, *browser]}
    fehler = 0
    for muster, ersatz, pruef in BEDIENUNG:
        rx = re.compile(muster)
        n_server = len(rx.findall(texte[server]))
        n_browser = sum(len(rx.findall(texte[p])) for p in browser)
        if n_server == n_browser == 0:
            if pruef in texte[server] and any(pruef in texte[p] for p in browser):
                continue  # schon übersetzt
            print(f"FEHLER: Bedientext {muster!r} nicht gefunden — Template bewegt?", file=sys.stderr)
            fehler += 1
        elif n_server != n_browser:
            print(f"FEHLER: {muster!r} {n_server}x im Server-, {n_browser}x in den Browser-Bündeln",
                  file=sys.stderr)
            fehler += 1
        else:
            for p in texte:
                texte[p] = rx.sub(ersatz, texte[p])
    if fehler:
        return 1
    for p, t in texte.items():
        if t != p.read_text(encoding="utf-8", errors="surrogateescape"):
            p.write_text(t, encoding="utf-8", errors="surrogateescape")
            print(f"Bedienung übersetzt: {p.relative_to(WURZEL)}")
    return 0


def kastennamen_eindeutschen() -> int:
    """Ersetzt im Kopf der prf-Kästen `Gross(kind)` durch den deutschen Namen."""
    tabelle = "{" + ",".join(f'{k}:"{v}"' for k, v in KASTENNAMEN.items()) + "}"
    buendel = [ZIEL / "build" / "index.js", *sorted((ZIEL / "public" / "build" / "_shared").glob("*.js"))]
    gefunden = 0
    for pfad in buendel:
        text = pfad.read_text(encoding="utf-8", errors="surrogateescape")
        if GEPATCHT in text:
            gefunden += 1
            continue
        treffer = KOPF.findall(text)
        if not treffer:
            continue
        if len(treffer) != 1:
            print(f"FEHLER: {len(treffer)} Kastenköpfe in {pfad.name}, erwartet 1", file=sys.stderr)
            return 1
        gross, k, nr = treffer[0]
        alt = f'kind:{gross}({k}),children:[{gross}({k})," ",{nr}]'
        neu = f'kind:{gross}({k}),children:[{GEPATCHT}({tabelle}[{k}]||{gross}({k}))," ",{nr}]'
        pfad.write_text(text.replace(alt, neu), encoding="utf-8", errors="surrogateescape")
        print(f"Kastennamen eingedeutscht: {pfad.relative_to(WURZEL)}")
        gefunden += 1
    if gefunden != 2:
        print(f"FEHLER: Kastenkopf in {gefunden} statt 2 Bündeln gefunden — Template bewegt?", file=sys.stderr)
        return 1
    return 0


def main() -> int:
    if not ARCHIV.is_file():
        print(f"FEHLER: {ARCHIV.relative_to(WURZEL)} fehlt", file=sys.stderr)
        return 1

    if (ZIEL / MARKER).is_file():
        print(f"Template liegt schon in {ZIEL.relative_to(WURZEL)}.")
        return kastennamen_eindeutschen() or bedienung_eindeutschen()

    ZIEL.parent.mkdir(parents=True, exist_ok=True)
    if ZIEL.exists():
        shutil.rmtree(ZIEL)

    # In einen Nachbarordner entpacken und dann die eine Wrapper-Ebene
    # (`book-theme-main/`) zum Zielnamen machen.
    roh = ZIEL.parent / "_entpackt"
    if roh.exists():
        shutil.rmtree(roh)
    with zipfile.ZipFile(ARCHIV) as archiv:
        archiv.extractall(roh)

    inhalt = [p for p in roh.iterdir() if p.is_dir()]
    if len(inhalt) != 1:
        print(
            f"FEHLER: erwartet genau ein Wurzelverzeichnis im Archiv, "
            f"gefunden: {[p.name for p in inhalt]}",
            file=sys.stderr,
        )
        return 1

    inhalt[0].rename(ZIEL)
    shutil.rmtree(roh)

    if not (ZIEL / MARKER).is_file():
        print(f"FEHLER: {MARKER} fehlt nach dem Entpacken", file=sys.stderr)
        return 1

    print(f"Template entpackt nach {ZIEL.relative_to(WURZEL)}")
    return kastennamen_eindeutschen() or bedienung_eindeutschen()


if __name__ == "__main__":
    raise SystemExit(main())
