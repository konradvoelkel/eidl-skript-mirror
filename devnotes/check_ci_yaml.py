#!/usr/bin/env python3
"""Prüft `.gitlab-ci.yml` auf die Form, die GitLab erwartet — nicht nur auf YAML.

Am 2026-09-27 scheiterte Pipeline #182378 mit

    jobs:pages:script config should be a string or a nested array of strings

Die Datei war **valides YAML**. Die Zeile

    - if [ -f x ]; then cp x y; else echo "WARNUNG: kein x"; fi

enthält ein `: ` in einem unquotierten Skalar, und YAML macht daraus brav eine Map
statt eines Strings. Ein `yaml.safe_load` sagt dazu nichts — es *ist* ja gültig.
Gefunden hat es erst GitLab, nach dem Push, und dann läuft **kein einziger Job**:
Eine kaputte `.gitlab-ci.yml` kann sich nicht selbst prüfen.

Deshalb vor dem Push:

    uv run devnotes/check_ci_yaml.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import yaml

WURZEL = Path(__file__).resolve().parent.parent
DATEI = WURZEL / ".gitlab-ci.yml"

# Schlüssel auf oberster Ebene, die keine Jobs sind
KEINE_JOBS = {"stages", "variables", "default", "include", "workflow", "image", "cache"}

# Job-Schlüssel, die eine Liste von Strings sein müssen
STRINGLISTEN = ("script", "before_script", "after_script")


def main() -> int:
    if not DATEI.is_file():
        print(f"FEHLER: {DATEI} fehlt", file=sys.stderr)
        return 1

    inhalt = yaml.safe_load(DATEI.read_text(encoding="utf-8"))
    fehler: list[str] = []

    for name, job in inhalt.items():
        if name in KEINE_JOBS or name.startswith(".") or not isinstance(job, dict):
            continue
        for schluessel in STRINGLISTEN:
            zeilen = job.get(schluessel)
            if zeilen is None:
                continue
            if isinstance(zeilen, str):
                continue
            for i, zeile in enumerate(zeilen):
                if not isinstance(zeile, str):
                    fehler.append(
                        f"{name}:{schluessel}[{i}] ist {type(zeile).__name__}, nicht str — "
                        f"meist ein unquotiertes ': ' in der Zeile: {zeile!r}"
                    )

    if fehler:
        print(f"{len(fehler)} Formfehler in {DATEI.name}:")
        for f in fehler:
            print("  " + f)
        return 1

    jobs = [n for n in inhalt if n not in KEINE_JOBS and not n.startswith(".")]
    print(f"{DATEI.name}: {len(jobs)} Jobs, alle Skriptzeilen sind Strings ({', '.join(jobs)}).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
