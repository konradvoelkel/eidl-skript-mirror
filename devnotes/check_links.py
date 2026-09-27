#!/usr/bin/env python3
"""Prüft die Links des Buchs: interne Ziele auf Existenz, externe auf Erreichbarkeit.

Der HTML-Build meldet `Cross-reference target not found`, wenn ein **Markdown-Ziel** im
Projekt fehlt — aber nur dafür. Er sagt nichts über einen Link auf eine Bilddatei, ein
Notebook oder eine CSV, und über das halbe Hundert externer Links sagt er erst recht nichts:
Die verrotten still, und im PDF sieht ein toter Link genauso aus wie ein lebender. Beim
Semesterstart ist das die eine Sorte Fehler, die Studierende zuverlässig finden.

Zwei Prüfungen:

0. **Kein Urteil nach einem HEAD.** Kaggle antwortet auf HEAD mit **404** und auf GET mit
   200 — HEAD ist nur die billige Vorfrage, entschieden wird nach dem GET, und wer dann noch
   ablehnt, wird ein zweites Mal als Browser gefragt.
1. **Intern.** Jedes relative Ziel (`../part-lernen/08-….md`, `notebooks/…ipynb`,
   `images/…png`) existiert, relativ zur verweisenden Datei aufgelöst. Fehlt es, ist das ein
   Fehler (Exit-Code 1).
2. **Extern.** HEAD, bei Ablehnung GET mit Ein-Byte-Bereich. 2xx ist gut; 404 und 410 und
   Namensauflösungsfehler sind Fehler; 401/403/405/429 und Weiterleitungen auf einen anderen
   Host sind **Hinweise** — Cloudflare und arXiv lehnen Skripte ab, ohne dass der Link kaputt
   wäre. Solche Fälle muss ein Mensch ansehen; sie lassen den Lauf nicht scheitern.

Anker (`…#abschnitt`) werden nur gemeldet, nicht geprüft: MyST erzeugt sie aus den
Überschriften nach eigenen Regeln, und die hier nachzubauen hieße, sie zweimal zu pflegen.
Dieses Repo benutzt ohnehin keine expliziten Anker (`CLAUDE.md`, Abschnitt „Querverweise“).

Aufruf:

    uv run devnotes/check_links.py                 # intern und extern
    uv run devnotes/check_links.py --offline       # nur intern, ohne Netz
    uv run devnotes/check_links.py --jobs 12

**Nicht in die CI.** Der Job dort baut ohne Netzzugriff auf Fremdhosts, und ein Buch soll
nicht rot werden, weil ein Server einen schlechten Tag hat. Dies ist ein Prüfer für die Hand
— vor dem Semesterstart und bei der fachlichen Durchsicht.
"""

from __future__ import annotations

import argparse
import re
import sys
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.parse import quote, urlsplit, urlunsplit

WURZEL = Path(__file__).resolve().parent.parent
TEILE = (
    "part-grundlagen",
    "part-lernen",
    "part-representation-learning",
    "part-architekturen-anwendungen",
)
# Das Buch plus die beiden Seiten, die Studierende außerdem lesen. `kurs-2026-27.md` ist nicht
# Teil des Buchs, aber seine Links (LSF, Mediathek, Rocket.Chat) sind die, an denen zuerst
# jemand hängenbleibt.
EINZELDATEIEN = ("index.md", "README.md", "glossar.md", "kurs-2026-27.md")

LINK = re.compile(r"\[[^\]]*\]\(\s*([^)\s]+?)\s*\)|<(https?://[^>\s]+)>")
NACHSATZ = "`.,;:!?\"')"
# Zwei Kennungen mit Absicht. Gefragt wird zuerst als das, was dieses Skript ist; wer darauf
# mit 403/404 antwortet, wird ein zweites Mal als Browser gefragt. Kaggle etwa schickt
# Skripten ein **404** statt eines 403 — beim ersten Lauf sah das nach drei toten
# Notebook-Links aus, die im Browser tadellos aufgehen. Ein Prüfer, der so etwas meldet, wird
# nach dem zweiten Fehlalarm nicht mehr benutzt.
UA_SKRIPT = "Mozilla/5.0 (compatible; eidl-skript check_links.py)"
UA_BROWSER = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/140.0.0.0 Safari/537.36"
)
# Ein lokaler Dienst, den das Buch als Beispiel nennt — der läuft beim Leser, nicht hier.
UEBERGEHEN = ("localhost", "127.0.0.1", "thispersondoesnotexist.com")


def buchdateien() -> list[Path]:
    pfade = [p for teil in TEILE for p in sorted((WURZEL / teil).glob("*.md"))]
    pfade += [WURZEL / n for n in EINZELDATEIEN if (WURZEL / n).is_file()]
    return pfade


def ziele_sammeln() -> tuple[list[tuple[Path, int, str]], list[tuple[Path, int, str]]]:
    """(intern, extern), je als Liste von (Datei, Zeile, Ziel)."""
    intern: list[tuple[Path, int, str]] = []
    extern: list[tuple[Path, int, str]] = []
    for p in buchdateien():
        in_fence = False
        for nr, zeile in enumerate(p.read_text(encoding="utf-8").splitlines(), start=1):
            if zeile.strip().startswith("```"):
                in_fence = not in_fence
                continue
            if in_fence:
                continue
            for treffer in LINK.finditer(zeile):
                ziel = (treffer.group(1) or treffer.group(2)).rstrip(NACHSATZ)
                if not ziel or ziel.startswith(("mailto:", "#")):
                    continue
                if ziel.startswith(("http://", "https://")):
                    extern.append((p, nr, ziel))
                else:
                    intern.append((p, nr, ziel))
    return intern, extern


def intern_pruefen(intern: list[tuple[Path, int, str]]) -> tuple[list[str], list[str]]:
    fehler: list[str] = []
    hinweise: list[str] = []
    for datei, nr, ziel in intern:
        pfad_teil = ziel.split("#", 1)[0]
        if pfad_teil.startswith("/"):
            # Wurzel-relativ auf der veröffentlichten Seite (z. B. `/eidl-skript.pdf`, das die
            # CI nach `public/` legt). Im Arbeitsbaum gibt es das Ziel nicht, und ein Pfad im
            # Repo wäre hier falsch — also melden, nicht beanstanden.
            ziel_in_public = WURZEL / "public" / pfad_teil.lstrip("/")
            zustand = "liegt in public/" if ziel_in_public.exists() else "public/ nicht gebaut"
            hinweise.append(
                f"{datei.name}:{nr}: `{ziel}` ist wurzel-relativ auf der Website ({zustand})"
            )
            continue
        if "#" in ziel and pfad_teil:
            hinweise.append(f"{datei.name}:{nr}: Anker in `{ziel}` — ungeprüft (MyST vergibt sie)")
        if not pfad_teil:
            continue
        aufgeloest = (datei.parent / pfad_teil).resolve()
        if not aufgeloest.exists():
            fehler.append(f"{datei.relative_to(WURZEL)}:{nr}: `{ziel}` existiert nicht ({aufgeloest})")
    return fehler, hinweise


def ascii_form(ziel: str) -> str:
    """URL mit nicht-ASCII-Zeichen in Pfad und Query prozentkodieren.

    `https://media.hhu.de/search/title/Einführung+in+…` ist ein gültiger Link im Buch, aber
    `urllib` schickt den Request-Pfad als ASCII und wirft sonst einen UnicodeEncodeError —
    der sah beim ersten Lauf wie ein toter Link aus.
    """
    t = urlsplit(ziel)
    host = t.netloc.encode("idna").decode("ascii") if not t.netloc.isascii() else t.netloc
    return urlunsplit((
        t.scheme, host, quote(t.path, safe="/%:@!$&'()*+,;=~-._"),
        quote(t.query, safe="/?=&%+:@!$'()*,;~-._"), "",
    ))


def einmal_fragen(ziel: str, ua: str, timeout: float) -> tuple[str, str]:
    for methode, kopf in (("HEAD", {}), ("GET", {"Range": "bytes=0-0"})):
        anfrage = urllib.request.Request(
            ascii_form(ziel), method=methode, headers={"User-Agent": ua, **kopf}
        )
        try:
            with urllib.request.urlopen(anfrage, timeout=timeout) as antwort:
                if urlsplit(antwort.geturl()).hostname != urlsplit(ziel).hostname:
                    return "hinweis", f"{antwort.status}, weitergeleitet auf {urlsplit(antwort.geturl()).hostname}"
                return "ok", str(antwort.status)
        except urllib.error.HTTPError as e:
            if methode == "HEAD":
                continue  # ein HEAD entscheidet nichts: Kaggle antwortet darauf mit 404
            if e.code in (404, 410):
                return "fehler", f"HTTP {e.code}"
            return "hinweis", f"HTTP {e.code} (Host lehnt Skripte ab? von Hand ansehen)"
        except urllib.error.URLError as e:
            return "fehler", f"nicht erreichbar: {e.reason}"
        except Exception as e:  # Timeout, defekte Weiterleitung, kaputtes Zertifikat
            return "fehler", f"{type(e).__name__}: {e}"
    return "hinweis", "HEAD und GET beide abgelehnt"


def abfragen(ziel: str, timeout: float) -> tuple[str, str]:
    """(status, bemerkung) — status ist 'ok', 'fehler' oder 'hinweis'."""
    host = urlsplit(ziel).hostname or ""
    if any(u in host for u in UEBERGEHEN):
        return "hinweis", "übergangen (lokal bzw. absichtlich flüchtig)"
    status, bemerkung = einmal_fragen(ziel, UA_SKRIPT, timeout)
    if status == "ok":
        return status, bemerkung
    zweitversuch, bemerkung2 = einmal_fragen(ziel, UA_BROWSER, timeout)
    if zweitversuch == "ok":
        return "ok", f"{bemerkung2} (erst als Browser; als Skript: {bemerkung})"
    return zweitversuch, bemerkung2


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--offline", action="store_true", help="nur interne Ziele prüfen")
    p.add_argument("--jobs", type=int, default=8, help="parallele Abfragen (Standard 8)")
    p.add_argument("--timeout", type=float, default=15.0, help="Sekunden je Abfrage")
    args = p.parse_args()

    intern, extern = ziele_sammeln()
    fehler, hinweise = intern_pruefen(intern)
    print(f"{len(buchdateien())} Dateien, {len(intern)} interne und {len(extern)} externe Ziele.")

    if not args.offline:
        einmalig = sorted({z for _, _, z in extern})
        herkunft: dict[str, list[str]] = {}
        for datei, nr, ziel in extern:
            herkunft.setdefault(ziel, []).append(f"{datei.name}:{nr}")
        with ThreadPoolExecutor(max_workers=args.jobs) as pool:
            ergebnisse = list(pool.map(lambda z: (z, *abfragen(z, args.timeout)), einmalig))
        for ziel, status, bemerkung in ergebnisse:
            wo = ", ".join(herkunft[ziel])
            if status == "fehler":
                fehler.append(f"{wo}: {ziel} — {bemerkung}")
            elif status == "hinweis":
                hinweise.append(f"{wo}: {ziel} — {bemerkung}")
        gut = sum(1 for _, s, _ in ergebnisse if s == "ok")
        print(f"{gut} von {len(einmalig)} verschiedenen externen Zielen glatt erreichbar.")

    if hinweise:
        print(f"\n{len(hinweise)} Hinweis(e) — ansehen, aber kein Fehler:")
        for h in hinweise:
            print(f"  · {h}")
    if fehler:
        sys.stdout.flush()
        print(f"\n{len(fehler)} Beanstandung(en):", file=sys.stderr)
        for f in fehler:
            print(f"  - {f}", file=sys.stderr)
        return 1
    print("\nAlle Links in Ordnung.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
