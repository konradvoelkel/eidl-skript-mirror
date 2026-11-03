#!/usr/bin/env python3
"""Die Textdateien des Artefakts vorkomprimieren, damit Pages sie komprimiert ausliefert.

    python3 tools/precompress.py <html-dir>            # .br- und .gz-Geschwister schreiben
    python3 tools/precompress.py <html-dir> --check     # nachmessen statt schreiben
    python3 tools/precompress.py <html-dir> --no-brotli # nur gzip (ohne das Paket brotli)


Warum ueberhaupt
----------------

GitLab Pages komprimiert nichts von sich aus. Am 2026-10-16 am Live-Stand gemessen: kein
`content-encoding` in der Antwort, auch nicht mit `Accept-Encoding: gzip, deflate, br`,
und im Browser `transferSize` 6.567 kB gegen `decodedBodySize` 6.580 kB -- die Seite geht
unkomprimiert ueber die Leitung, 6,5 MB je Seitenaufruf. Davon sind 4,87 MB JavaScript in
19 modulepreload-Chunks, der groesste 2,19 MB.

Was Pages statt dessen tut, steht in dessen Dokumentation: *vor* dem Ausliefern einer
Datei sieht es nach, ob daneben dieselbe Datei mit der Endung `.br` oder `.gz` liegt, und
liefert die, wenn der Browser die Kodierung akzeptiert. Das ist der ganze Mechanismus --
kein Schalter, keine Konfiguration, nur Dateien, die danebenliegen muessen.

Beides wird hingelegt, `.br` und `.gz`, und Pages nimmt von sich aus das `.br`, wenn der
Browser es akzeptiert -- praktisch jeder tut das. Die `.gz` bleibt die Rueckfallebene fuer
alte Clients und kostet nur Artefaktplatz, keine Anfrage.

Brotli kam am 2026-10-20 dazu, nachdem der Live-Nachweis fuer gzip da war (Zeile 1b der
TODO): dass diese Pages-Instanz eine daneben liegende Datei ueberhaupt ausliefert, war die
Voraussetzung, und sie ist jetzt gemessen -- `content-encoding: gzip`, 153.464 -> 33.670
Bytes auf der Startseite.

**Python kann kein Brotli**, weder in der Standardbibliothek noch im CI-Image; deshalb ruft
dieses Skript das Programm `brotli` auf, das im `pages`-Job ein `apk add --no-cache brotli`
mitbringt. Fehlt es, bricht der Lauf ab statt die `.br` still weglassen -- eine Seite, die
unbemerkt wieder 15 % groesser ausgeliefert wird, ist genau die Art Rueckschritt, die hier
niemandem auffaellt. Fuer einen Lauf ohne das Paket gibt es `--no-brotli`, ausdruecklich.

**Stufe 11, und warum nicht 9.** Am 2026-10-20 am groessten Brocken des Artefakts gemessen
(`plotly-PQJCFEUX.js`, 4,8 MB): gzip -9 1,42 MB in 0,14 s; brotli -q9 1,21 MB in 0,31 s;
brotli -q11 1,08 MB in 6,3 s. Stufe 11 ist also noch 10 % besser als 9 und kostet dafuer das
Zwanzigfache an Rechenzeit -- in einem Deploy-Job, der je Push einmal laeuft, ist das der
richtige Tausch: die Bytes zahlt jeder Leser, die Sekunden zahlt der Runner. Fuer einen
schnelleren Durchlauf gibt es `--brotli-quality`.


Die Falle: eine veraltete Kopie ist unsichtbar
----------------------------------------------

Ab jetzt existiert jede Textdatei dreimal. Liegt ein `.br` daneben, ist es das, was
praktisch jeder Leser bekommt -- jeder aktuelle Browser schickt `Accept-Encoding: br`, und
Pages bevorzugt es; ohne das `.br` bekommt er die `.gz`. Eine Kopie, die nicht zum Original
passt, liefert also die *alte* Seite an alle, waehrend ein `curl` ohne `Accept-Encoding` und
jeder Blick ins Artefakt die neue zeigt. Das ist derselbe Fehlertyp wie die
localhost-Sitemap und die Schriften hinter dem relativen url(): gruen bei der naheliegenden
Pruefung, falsch beim tatsaechlichen Abruf. Und mit zwei Kopien ist er zweimal moeglich --
deshalb prueft `--check` beide, und zwar durch Auspacken.

Zwei Dinge halten das in Schach:

1. **Dieser Schritt laeuft als letzter** im pages-Job, nach jeder Umschreibung von HTML,
   CSS und JS. Steht er vorher, ist er garantiert falsch.
2. **`--check` packt jede `.br` und jede `.gz` wieder aus und vergleicht byteweise** mit
   dem Original, statt nur ihre Existenz zu pruefen. Nur das faellt auf, wenn ein spaeterer
   Schritt die Datei doch noch anfasst.

Zusaetzlich faellt eine `.br` oder `.gz` ohne Original auf: sie ist der Rest eines
umbenannten Fingerprints und ein Zeichen, dass das Artefakt nicht frisch gebaut wurde.


Was ausgelassen wird und warum
------------------------------

- **Alles Binaere**, insbesondere `eidl-skript.pdf` (7,4 MB) und die PNG: schon komprimiert,
  gzip macht sie groesser und kostet nur Artefaktplatz.
- **Dateien unter 1 kB**: bei ihnen entscheidet der Round-Trip, nicht die Nutzlast.
- **Dateien, bei denen die Kompression nicht kleiner ist.** Dann ist die Abwesenheit der
  Kopie die richtige Antwort, und `--check` muss sie genauso akzeptieren wie ihr
  Vorhandensein -- sonst waere die Pruefung nicht erfuellbar. `--check` komprimiert dafuer
  selbst nach und verlangt die Kopie genau dann, wenn sie sich lohnt. Je Verfahren
  getrennt: es gibt Dateien, bei denen brotli gewinnt und gzip nicht.

Idempotent: ein zweiter Lauf schreibt Dateien gleichen Inhalts (`mtime=0`, damit das auch
byteweise stimmt und ein Vergleich zweier Laeufe aussagekraeftig ist).
"""

from __future__ import annotations

import argparse
import gzip
import io
import pathlib
import shutil
import subprocess
import sys

# Textendungen, die im Artefakt vorkommen. ".map" ist dabei, weil MyST Sourcemaps
# mitliefert und sie zu den groessten Einzeldateien gehoeren koennen.
TEXT_SUFFIXES = {
    ".html",
    ".css",
    ".js",
    ".map",
    ".svg",
    ".json",
    ".txt",
    ".xml",
    ".md",
    ".xsl",
}

MIN_SIZE = 1024


def eligible(path: pathlib.Path) -> bool:
    return (
        path.is_file()
        and not path.is_symlink()
        and path.suffix.lower() in TEXT_SUFFIXES
        and path.stat().st_size >= MIN_SIZE
    )


def brotli_bin() -> str:
    """Den Pfad zu `brotli` oder ein Abbruch mit der Zeile, die im Job fehlt."""
    found = shutil.which("brotli")
    if not found:
        sys.exit(
            "FEHLER: das Programm 'brotli' fehlt. Im pages-Job gehoert dafuer ein\n"
            "  apk add --no-cache brotli\n"
            "vor diesen Schritt; lokal 'apt install brotli'. Fuer einen Lauf ohne\n"
            "Brotli ausdruecklich --no-brotli uebergeben."
        )
    return found


def squeeze_br(raw: bytes, binary: str, quality: int) -> bytes:
    """brotli, Stufe 11 -- ueber das Programm, weil Python das Verfahren nicht kennt.

    Das Format traegt keinen Zeitstempel, zwei Laeufe sind also von sich aus
    byteidentisch; das `mtime=0` der gzip-Seite braucht es hier nicht.
    """
    done = subprocess.run(
        [binary, "-q", str(quality), "-c", "-"],
        input=raw, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )
    if done.returncode != 0:
        sys.exit(f"FEHLER: brotli brach ab ({done.returncode}): "
                 f"{done.stderr.decode('utf-8', 'replace')[:200]}")
    return done.stdout


def unsqueeze_br(data: bytes, binary: str) -> bytes | None:
    """Eine `.br` auspacken. None, wenn sie defekt ist -- Pages liefert sie als Muell aus."""
    done = subprocess.run(
        [binary, "-d", "-c", "-"],
        input=data, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )
    return done.stdout if done.returncode == 0 else None


def squeeze(raw: bytes) -> bytes:
    """gzip, Stufe 9, ohne Zeitstempel -- damit zwei Laeufe byteidentisch sind."""
    buf = io.BytesIO()
    with gzip.GzipFile(fileobj=buf, mode="wb", compresslevel=9, mtime=0) as fh:
        fh.write(raw)
    return buf.getvalue()


def write_mode(root: pathlib.Path, binary: str | None, quality: int) -> int:
    n = kept = n_br = kept_br = 0
    raw_gz = gz_total = raw_br = br_total = 0
    for f in sorted(root.rglob("*")):
        if not eligible(f):
            continue
        raw = f.read_bytes()

        gz = squeeze(raw)
        sibling = f.with_name(f.name + ".gz")
        if len(gz) >= len(raw):
            # Kein Gewinn: eine .gz hier waere nur eine zweite Wahrheit ohne Nutzen.
            if sibling.exists():
                sibling.unlink()
            kept += 1
        else:
            sibling.write_bytes(gz)
            n += 1
            raw_gz += len(raw)
            gz_total += len(gz)

        if not binary:
            continue
        br = squeeze_br(raw, binary, quality)
        br_sibling = f.with_name(f.name + ".br")
        if len(br) >= len(raw):
            if br_sibling.exists():
                br_sibling.unlink()
            kept_br += 1
        else:
            br_sibling.write_bytes(br)
            n_br += 1
            raw_br += len(raw)
            br_total += len(br)

    if not n:
        print("precompress: keine Datei kam in Frage -- ist das der gebaute Ordner?")
        return 1

    bericht = (
        f"precompress: {n} Dateien mit gzip, {raw_gz / 1024:.0f} kB -> "
        f"{gz_total / 1024:.0f} kB ({100 * (1 - gz_total / raw_gz):.0f} % gespart)"
    )
    if binary:
        # Der Vergleich beider Verfahren laeuft ueber dieselben Rohbytes, nicht ueber die
        # beiden Summen: sie koennen verschiedene Dateimengen betreffen.
        bericht += (
            f"; {n_br} mit brotli -q{quality}, {raw_br / 1024:.0f} kB -> "
            f"{br_total / 1024:.0f} kB ({100 * (1 - br_total / raw_br):.0f} % gespart)"
        )
        if n == n_br and raw_gz == raw_br:
            bericht += f", brotli {100 * (1 - br_total / gz_total):.0f} % kleiner als gzip"
    else:
        bericht += "; brotli uebersprungen (--no-brotli)"
        alt = sum(1 for g in root.rglob("*.br") if g.is_file())
        if alt:
            print(f"WARNUNG: {alt} .br liegen weiter im Artefakt und sind jetzt veraltet; "
                  f"Pages bevorzugt sie gegenueber der .gz")
    print(bericht + f"; {kept} ohne Gewinn uebersprungen"
          + (f" ({kept_br} bei brotli)" if binary and kept_br != kept else ""))
    return 0


def check_mode(root: pathlib.Path, binary: str | None, quality: int) -> int:
    problems: list[str] = []
    checked = checked_br = ohne_gewinn = 0

    # Ohne brotli liessen sich vorhandene .br nicht auspacken -- und genau die bekommt
    # praktisch jeder Leser. Ein "ok", das die ausgelieferte Fassung ueberspringt, waere
    # schlimmer als ein Fehler.
    if binary is None:
        vorhanden = sum(1 for f in root.rglob("*.br") if f.is_file())
        if vorhanden:
            problems.append(
                f"{vorhanden} .br im Artefakt, aber --no-brotli: ungeprueft bleibt genau "
                "die Fassung, die ausgeliefert wird"
            )

    for f in sorted(root.rglob("*")):
        if f.suffix in (".gz", ".br"):
            # Eine Kopie ohne Original ist ein Ueberrest, kein Fund.
            if not f.with_name(f.name[: -len(f.suffix)]).exists():
                problems.append(
                    f"{f}: {f.suffix} ohne Originaldatei (veraltetes Artefakt?)"
                )
            continue
        if not eligible(f):
            continue
        raw = f.read_bytes()

        sibling = f.with_name(f.name + ".gz")
        if not sibling.exists():
            # Erlaubt ist das nur, wenn gzip hier nichts gebracht haette.
            if len(squeeze(raw)) < len(raw):
                problems.append(f"{f}: keine .gz, obwohl gzip kleiner waere")
            else:
                ohne_gewinn += 1
        else:
            try:
                back = gzip.decompress(sibling.read_bytes())
            except OSError as exc:  # defekte .gz liefert Pages als Muell aus
                problems.append(f"{sibling}: laesst sich nicht entpacken ({exc})")
                back = None
            if back is None:
                pass
            elif back != raw:
                problems.append(
                    f"{sibling}: Inhalt weicht vom Original ab "
                    f"({len(back)} gegen {len(raw)} Bytes) -- "
                    "lief die Vorkompression vor einer Umschreibung?"
                )
            elif len(sibling.read_bytes()) >= len(raw):
                problems.append(f"{sibling}: nicht kleiner als das Original")
            else:
                checked += 1

        if not binary:
            continue
        br_sibling = f.with_name(f.name + ".br")
        if not br_sibling.exists():
            if len(squeeze_br(raw, binary, quality)) < len(raw):
                problems.append(f"{f}: keine .br, obwohl brotli kleiner waere")
            continue
        back = unsqueeze_br(br_sibling.read_bytes(), binary)
        if back is None:
            problems.append(f"{br_sibling}: laesst sich nicht entpacken")
        elif back != raw:
            problems.append(
                f"{br_sibling}: Inhalt weicht vom Original ab "
                f"({len(back)} gegen {len(raw)} Bytes) -- "
                "lief die Vorkompression vor einer Umschreibung?"
            )
        elif len(br_sibling.read_bytes()) >= len(raw):
            problems.append(f"{br_sibling}: nicht kleiner als das Original")
        else:
            checked_br += 1

    if problems:
        print(f"FEHLER: {len(problems)} Problem(e) bei der Vorkompression:")
        for pr in problems[:20]:
            print(f"  {pr}")
        if len(problems) > 20:
            print(f"  ... und {len(problems) - 20} weitere")
        return 1

    if not checked:
        print("FEHLER: keine einzige vorkomprimierte Datei gefunden")
        return 1
    if binary and not checked_br:
        print("FEHLER: keine einzige .br gefunden -- lief die Vorkompression mit --no-brotli?")
        return 1
    print(
        f"ok: {checked} .gz"
        + (f" und {checked_br} .br" if binary else " (brotli uebersprungen)")
        + ", alle entpacken byteidentisch zum Original"
        + (f", {ohne_gewinn} Dateien ohne Gewinn" if ohne_gewinn else "")
    )
    return 0


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("html_dir")
    ap.add_argument(
        "--check",
        action="store_true",
        help="nicht schreiben, sondern jede .br und .gz auspacken und mit dem Original "
             "vergleichen",
    )
    ap.add_argument(
        "--no-brotli",
        dest="brotli",
        action="store_false",
        help="nur gzip. Fuer Laeufe ohne das Paket brotli -- ausdruecklich, damit eine "
             "fehlende .br nie stillschweigend passiert",
    )
    ap.add_argument(
        "--brotli-quality",
        type=int,
        default=11,
        help="Kompressionsstufe fuer brotli (Vorgabe 11; 9 ist zwanzigmal schneller und "
             "10 %% groesser, Messung im Docstring)",
    )
    args = ap.parse_args()

    root = pathlib.Path(args.html_dir)
    if not root.is_dir():
        sys.exit(f"FEHLER: {root} ist kein Verzeichnis")

    binary = brotli_bin() if args.brotli else None

    sys.exit(
        check_mode(root, binary, args.brotli_quality)
        if args.check
        else write_mode(root, binary, args.brotli_quality)
    )


if __name__ == "__main__":
    main()
