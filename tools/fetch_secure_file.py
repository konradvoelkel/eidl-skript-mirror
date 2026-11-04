#!/usr/bin/env python3
"""Eine Secure File des eigenen GitLab-Projekts holen, mit dem Job-Token.

    python3 tools/fetch_secure_file.py <name> <zielpfad>

Warum als eigenes Skript und als eigener Job (2026-11-04)
---------------------------------------------------------
Das HHU-Beamer-Theme darf nicht ins Repository (kein Lizenzvermerk, HHU-Bildmarke im
`fig/`, und der Spiegel auf GitHub ist öffentlich). Es liegt deshalb als Secure File im
Projekt und muss im CI in den Build-Kontext von kaniko kommen.

Der erste Versuch holte es im `before_script` des kaniko-Jobs mit `wget` -- und scheiterte:
Das busybox-`wget` in `kaniko:debug` kann kein TLS gegen diesen Server
(„TLS certificate validation not implemented", dann „TLS error from peer (alert code 47)").
Deshalb ein eigener kleiner Job in `python:3.13-alpine`, der die Datei als Artefakt
weiterreicht. Python holt sie mit der Standardbibliothek: kein `curl`, kein `apk add`, und
vor allem nicht der Installer von gitlab.com, der ein unangeheftetes Skript als root
ausführen würde.

Fehlt die Datei, endet das Skript mit 0 und einer Meldung: Die Pipeline soll an einem
fehlenden Theme nicht sterben, sondern `build-slides` soll es sagen.
"""

import json
import os
import pathlib
import sys
import urllib.error
import urllib.request


def api(pfad, token):
    r = urllib.request.Request(pfad, headers={"JOB-TOKEN": token})
    return urllib.request.urlopen(r, timeout=60)


def main():
    if len(sys.argv) != 3:
        print(__doc__.splitlines()[2])
        return 2
    name, ziel = sys.argv[1], pathlib.Path(sys.argv[2])

    token = os.environ.get("CI_JOB_TOKEN")
    basis = os.environ.get("CI_API_V4_URL")
    projekt = os.environ.get("CI_PROJECT_ID")
    if not (token and basis and projekt):
        print("Keine CI-Umgebung (CI_JOB_TOKEN/CI_API_V4_URL/CI_PROJECT_ID fehlen)")
        return 0

    wurzel = "%s/projects/%s/secure_files" % (basis, projekt)
    try:
        liste = json.loads(api(wurzel, token).read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        print("Secure-Files-Liste nicht lesbar (HTTP %s) -- ohne %s weiter" % (e.code, name))
        return 0
    treffer = [d for d in liste if d.get("name") == name]
    if not treffer:
        print("Keine Secure File namens %s (%d vorhanden) -- ohne sie weiter"
              % (name, len(liste)))
        return 0

    d = treffer[0]
    try:
        daten = api("%s/%s/download" % (wurzel, d["id"]), token).read()
    except urllib.error.HTTPError as e:
        print("Download von %s scheiterte (HTTP %s) -- ohne sie weiter" % (name, e.code))
        return 0

    # Die API nennt eine Pruefsumme; sie wird geprueft, statt ihr zu glauben.
    pruefsumme = d.get("checksum")
    if pruefsumme and d.get("checksum_algorithm", "sha256") == "sha256":
        import hashlib
        ist = hashlib.sha256(daten).hexdigest()
        if ist != pruefsumme:
            print("Pruefsumme von %s weicht ab (erwartet %s, bekommen %s) -- nicht benutzt"
                  % (name, pruefsumme[:12], ist[:12]))
            return 0

    ziel.parent.mkdir(parents=True, exist_ok=True)
    ziel.write_bytes(daten)
    print("%s geholt: %d Bytes, Pruefsumme %s" % (name, len(daten), "ok" if pruefsumme else "ungeprueft"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
