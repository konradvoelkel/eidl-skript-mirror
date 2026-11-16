#!/usr/bin/env python3
"""Die Vorschaukarte unter einen Dateinamen bringen, der nicht bei jedem Lauf wechselt.

    python3 tools/stable_card.py <html-verzeichnis>
    python3 tools/stable_card.py --check <html-verzeichnis>

Im `pages`-Job nach `llms_txt.py` und vor `image_dims.py` laufen lassen. Nur
Standardbibliothek, weil das Image kein Python-Paket installiert.

Warum es dieses Skript gibt
---------------------------

MyST benennt jede kopierte Datei in `hashAndCopyStaticFile` so (nachgelesen im
ausgelieferten `myst.cjs`):

    const { mtime, size } = fs.fstatSync(fd);
    const hash = computeHash(`${file}${mtime.toString()}${size.toString()}`);
    const fileHash = `${name.slice(0, 20)}-${hash}${ext}`;

Also md5 ueber **absoluten Pfad, mtime und Groesse** -- nicht ueber den Inhalt. Zwei
Folgen, beide am 2026-11-16 gemessen:

* Lokal und CI stimmen nie ueberein, weil der Pfad eingeht
  (`/builds/voelkel/eidl-skript/...` gegen `/home/konrad/...`).
* Die meisten CI-Laeufe stimmen untereinander nicht ueberein, weil die Datei beim
  Checkout neu gestempelt wird. Gemessen an fuenf aufeinanderfolgenden Pipelines:
  viermal gewechselt, einmal nicht; ueber elf Pipelines sind es acht von zehn Uebergaengen.
  Die mtime laesst sich aus dem Hash zurueckrechnen, weil Pfad und Groesse bekannt sind; sie
  lag jedesmal 9 bis 18 Sekunden nach dem Start ihrer Pipeline. Namen kehren dabei wieder
  (`f425a4d6` zweimal, 85 Minuten auseinander), es gibt also mehrere Arbeitskopien: beide
  Jobs laufen unter dem Docker-Executor, `/builds/voelkel/eidl-skript` ist ein Cache-Volume
  je Nebenlaeufigkeits-Slot. Die Messung dazu steht in `devnotes/seo-audit-2026-11-15.md`
  §10; in welchem Slot ein Job landet, ist nicht gemessen.

Die Quelle `images/social-card.png` ist dabei seit Commit a3da25d unveraendert
(`md5 b6ec819d...`), und die gebaute Datei ist mit ihr bytegleich: MyST kodiert nicht
neu. Der Name wandert trotzdem, und die URL des vorigen Laufs antwortet 404. Wer die
**Bild-URL** gespeichert hat und die Seite nicht erneut liest, sieht danach kein Bild.
(Wer die Seite neu holt, merkt nichts -- deshalb steht der Befund im Audit unter LOW.)

Wie es das loest, und warum gerade so
-------------------------------------

Getauscht wird nur der **Dateiname**, nicht die URL: jedes Vorkommen von
`social-card-<32 hex>.png` wird zu `social-card.png`. Damit bleibt absolut absolut,
der Basispfad bleibt unberuehrt, und es ist gleichgueltig, an wie vielen Stellen die
Karte steht. Das sind naemlich drei, und zwei davon haette ein Blick aufs `og:image` der
Landingpage allein uebersehen:

1. `og:image` und `name="image"` im Markup -- auf *jeder* Seite, nicht nur auf der
   Landingpage: wo die erste Abbildung eines Kapitels zu klein fuer eine Karte ist,
   setzt `head_meta.py` die allgemeine ein (zuletzt auf 20 von 33 Seiten; ersetzt wird
   das Meta-Tag, nicht die Abbildung im Text),
2. `image` im JSON-LD der Landingpage (`inject_jsonld.py`),
3. `thumbnail` und `thumbnailOptimized` in der Hydrations-Nutzlast -- daraus baut das
   Theme `og:image` nach der Hydration neu. Nachgemessen am 2026-11-16: von den 196
   Thumbnail-Feldern einer Kapitelseite sind genau zwei Kartenangaben
   (`page.frontmatter` und `project`), und nur die macht `hydration.py` absolut; die
   uebrigen sind die kleinen Vorschauen der internen Links.

Ein `twitter:image` gibt es nicht und soll es nicht geben: X faellt auf `og:image`
zurueck, und `head_meta.py` setzt von den Karten-Tags nur `twitter:card`.

Die stabile Datei liegt **unter `build/`** und nicht in der Wurzel, und das ist der
Grund, warum `hydration.py` nicht angefasst werden muss: dessen `absolute_card()`
schreibt nur um, was wurzelrelativ unter `<base>/build/` zeigt. Ein Name in der Wurzel
faellt aus diesem Muster, und dann waere das nachgebaute `og:image` wurzelrelativ --
OpenGraph verlangt aber absolut. Ein Zusatz in der Wurzel haette also eine Aenderung an
zwei weiteren Werkzeugen gekostet; `build/social-card.png` kostet keine.

Die gehashte Datei bleibt liegen. Sie kostet 42 kB, auf sie zeigt danach nichts mehr,
und solange sie da ist, antwortet auch die URL *dieses* Laufs weiter mit 200.

Reihenfolge
-----------

Nach `head_meta.py` (das die Karte erst aus dem `og:image` der Landingpage *bestimmt*
und dabei auf `/build/` im Pfad besteht), nach `inject_jsonld.py` und `llms_txt.py`
(die den Namen weiterschreiben), und vor `image_dims.py` (das die ersetzten
Abbildungen ausmisst und die stabile Datei dafuer finden muss). Vor `hydration.py`,
damit der Kopf-Waechter den stabilen Namen einfriert und nicht den gehashten.

Was `--check` nicht kann
------------------------

Es prueft das Artefakt. Dass der Name ueber *zwei Laeufe hinweg* derselbe ist, kann es
nicht sehen -- das zeigt erst der naechste Deploy, und die Probe dafuer steht in
`devnotes/seo-audit-2026-11-15.md` §10.
"""

import argparse
import pathlib
import re
import shutil
import sys

STABIL = "social-card.png"
GEHASHT = re.compile(r"social-card-[0-9a-f]{32}\.png")

# Textdateien im Artefakt, in denen eine Karten-URL stehen kann. `.json` sind die
# Seiten-Daten des Themes, `.txt` ist llms.txt und llms-full.txt, `.xml` die Sitemap.
ENDUNGEN = (".html", ".json", ".txt", ".xml")

# Die Kartenregel: kleiner zeigt keine Plattform an. Gleiche Werte wie social_card.py.
SOLL = (1200, 630)


def png_masse(f: pathlib.Path) -> tuple[int, int]:
    """Breite und Hoehe aus dem IHDR, ohne Pillow -- wie in social_card.py."""
    data = f.read_bytes()
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        sys.exit(f"FEHLER: {f} ist keine PNG")
    i = 8
    while i + 8 <= len(data):
        laenge = int.from_bytes(data[i : i + 4], "big")
        kind = data[i + 4 : i + 8]
        nutz = data[i + 8 : i + 8 + laenge]
        if kind == b"IHDR":
            return (int.from_bytes(nutz[:4], "big"), int.from_bytes(nutz[4:8], "big"))
        i += 12 + laenge
    sys.exit(f"FEHLER: {f} hat kein IHDR")


def karte_aus_landingpage(root: pathlib.Path) -> str | None:
    """Der Dateiname der Karte, aus dem og:image der Landingpage.

    Dieselbe Quelle wie in head_meta.social_card(): die Landingpage hat keine eigene
    erste Abbildung, traegt also das Projekt-Thumbnail -- und das ist die Karte. Nicht
    geglobt, weil im Bau mehrere `social-card-*.png` liegen koennen (MyST legt dieselbe
    Datei unter zwei Hashes ab) und ein Glob dann raten muesste, welche gemeint ist.

    Rueckgabe None, wenn dort schon der stabile Name steht -- dann ist nichts zu tun.
    """
    f = root / "index.html"
    if not f.is_file():
        sys.exit(f"FEHLER: {f} fehlt; nach dem HTML-Bau laufen lassen")
    m = re.search(r'<meta property="og:image" content="([^"]+)"', f.read_text(encoding="utf-8"))
    if not m:
        sys.exit(
            "FEHLER: die Landingpage hat kein og:image, aus dem der Kartenname zu lesen "
            "waere -- lief head_meta.py vorher?"
        )
    name = m.group(1).rsplit("/", 1)[-1]
    if name == STABIL:
        return None
    if not GEHASHT.fullmatch(name):
        sys.exit(
            f"FEHLER: das og:image der Landingpage heisst {name!r} und ist weder der "
            f"stabile Name {STABIL!r} noch ein gehashter -- hat MyST seine "
            "Namensgebung geaendert?"
        )
    return name


def dateien(root: pathlib.Path) -> list[pathlib.Path]:
    return sorted(f for f in root.rglob("*") if f.is_file() and f.suffix in ENDUNGEN)


def umschreiben(root: pathlib.Path, gehasht: str) -> tuple[int, int]:
    """Jedes Vorkommen des gehashten Namens durch den stabilen ersetzen."""
    quelle = root / "build" / gehasht
    if not quelle.is_file():
        sys.exit(f"FEHLER: {quelle} fehlt, obwohl die Landingpage darauf zeigt")
    masse = png_masse(quelle)
    if masse != SOLL:
        sys.exit(f"FEHLER: {quelle} ist {masse[0]}x{masse[1]}, die Kartenregel verlangt "
                 f"{SOLL[0]}x{SOLL[1]}")
    ziel = root / "build" / STABIL
    shutil.copyfile(quelle, ziel)

    treffer = 0
    beruehrt = 0
    for f in dateien(root):
        alt = f.read_text(encoding="utf-8")
        neu = alt.replace(gehasht, STABIL)
        if neu != alt:
            treffer += alt.count(gehasht)
            beruehrt += 1
            f.write_text(neu, encoding="utf-8")
    return treffer, beruehrt


def pruefen(root: pathlib.Path) -> int:
    ziel = root / "build" / STABIL
    if not ziel.is_file():
        print(f"✗ {ziel} fehlt -- lief stable_card.py?")
        return 1
    masse = png_masse(ziel)
    if masse != SOLL:
        print(f"✗ {ziel} ist {masse[0]}x{masse[1]} statt {SOLL[0]}x{SOLL[1]}")
        return 1

    # Kein gehashter Verweis darf uebrig sein, sonst zeigt irgendeine Stelle weiter auf
    # einen Namen, der beim naechsten Lauf 404 antwortet.
    rest: list[str] = []
    for f in dateien(root):
        for m in set(GEHASHT.findall(f.read_text(encoding="utf-8"))):
            rest.append(f"{f.relative_to(root)}: {m}")
    if rest:
        print(f"✗ {len(rest)} Verweise zeigen noch auf einen gehashten Kartennamen:")
        for z in rest[:5]:
            print(f"    {z}")
        return 1

    m = re.search(
        r'<meta property="og:image" content="([^"]+)"',
        (root / "index.html").read_text(encoding="utf-8"),
    )
    if not m:
        print("✗ die Landingpage hat kein og:image")
        return 1
    url = m.group(1)
    if not url.startswith("http"):
        print(f"✗ das og:image der Landingpage ist relativ: {url}")
        return 1
    if not url.endswith(f"/build/{STABIL}"):
        print(f"✗ das og:image der Landingpage zeigt nicht auf den stabilen Namen: {url}")
        return 1

    print(f"✓ {url} ist stabil und {masse[0]}x{masse[1]}; kein gehashter Kartenverweis "
          f"in {len(dateien(root))} Dateien")
    return 0


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
    if not root.is_dir():
        sys.exit(f"FEHLER: {root} ist kein Verzeichnis")

    if args.check:
        sys.exit(pruefen(root))

    gehasht = karte_aus_landingpage(root)
    if gehasht is None:
        print(f"stable_card: {STABIL} steht schon im og:image, nichts zu tun")
        sys.exit(pruefen(root))

    treffer, beruehrt = umschreiben(root, gehasht)
    print(f"stable_card: {gehasht} -> {STABIL}, {treffer} Verweise in {beruehrt} Dateien")
    sys.exit(pruefen(root))


if __name__ == "__main__":
    main()
