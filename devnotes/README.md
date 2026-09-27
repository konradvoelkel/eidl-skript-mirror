# devnotes

Arbeitsnotizen und Prüfskripte zum Skript, nicht Teil des Buchs. Stand 2026-09-27.

| Datei | Was | Status |
|---|---|---|
| `TODO.md` | Die eine Liste offener Punkte und Entscheidungen, mit Erledigt-Historie | **aktuell**, hier zuerst schauen |
| `migrationsplan.md` | Wie das Skript aus den Folien 2025/26 entstanden ist; Zuordnung Vorlesung ↔ Kapitel ↔ Blatt ↔ Klausur; Links zu den Google-Slides 2025 | Referenz, Historie |
| `klausur-abdeckung.md` | Abgleich des Klausur-Aufgabenschatzes 2025/26 mit den Kapiteln | Referenz (Stand 2026-09-17, Kapitelnamen gelten weiter) |
| `diskussion-vorlesung-vs-skript.md` | Was die Aufzeichnungen 2025/26 über das Skript sagen: neun Thesen, Konrads Entscheidungen, Umsetzung | abgeschlossen, Entscheidungen umgesetzt |
| `vorschlag-grundlagen.md` | Zwölf Grundlagen-Snippets und wo sie eingebaut wurden | abgeschlossen, umgesetzt |
| `build_skript_from_2025.py` | Erzeugte die erste Prosafassung aus den Folien-PDFs und die Blätter aus den `.tex` | einmalig gelaufen (2026-09-17), nicht mehr nötig |
| `restructure.py` | Kapitelschnitt 2026-09-17 (Folien-Kapitel → Themen-Kapitel) | einmalig gelaufen, nicht mehr nötig |
| `folien-review-2026-09-25.md` | Durchsicht der 15 Beamer-Decks: Schriftbild, Titel/Labels, Ablaufplan-Nummern, Blatt-Zuordnung, fachliche Unschärfen, fehlende Bilder | A1–A3, Blatt-Verweise, VL-3-Code erledigt (2026-09-25); Rest offen |
| `build-log-2026-09-27.md` | Playbook-Durchgang: Messwerte vorher/nachher, die zwei Konversions-Fehlerklassen, minted zurück, Gegenprobe im Image | Protokoll, abgeschlossen |
| `patch_myst_tex.py` | Repariert den mystmd-Fehler, der vor jeden Bindestrich in Codeblöcken ein Leerzeichen setzt | **nach jedem `uv sync`** laufen lassen; im CI-Image automatisch |
| `check_pdf_build.py` | Prüft das gebaute PDF: LaTeX-Fehler, Abbruch, fehlende Glyphen, Seitenzahl, Stichproben | läuft im CI-Job `build-pdf`, lokal vor jedem PDF-Commit |
| `check_ci_yaml.py` | Prüft `.gitlab-ci.yml` auf die Form, die GitLab erwartet (nicht nur auf YAML) | vor jedem Push, der die CI anfasst |
| `make_figures.py`, `embed_figures.py` | Abbildungen mit matplotlib erzeugen und einbetten | bei Bedarf erneut laufen lassen |

Die Lösungsvorschläge zu den Übungsblättern liegen seit dem 2026-09-27 in `../loesungen/`
(gitignored, nur in Sciebo) — vorher standen sie in den Blättern und damit im
veröffentlichten PDF. `../loesungen/README.md` sagt, was dort liegt und was noch zu klären ist.

Die Vorlesungsaufzeichnungen 2025/26 (Transkripte, Standbilder, Sitzungsnotizen, Übersicht, Abschlussbericht) liegen in
`../transcripts/` (gitignored, nur in Sciebo). Der Vorlesungsplan 2026/27 steht in `../kurs-2026-27.md`.
