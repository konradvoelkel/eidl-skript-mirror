# devnotes

Arbeitsnotizen und Prüfskripte zum Skript, nicht Teil des Buchs. Stand 2026-10-19.
Die Skripte der **Veröffentlichung** liegen dagegen in `../tools/` (Vorschaukarte,
Sitemap-URLs, Kopf-Tags, JSON-LD) — sie laufen im Deploy und gehören nicht zu den
Arbeitsnotizen; `build-log-2026-10-19.md` erklärt sie.

| Datei | Was | Status |
|---|---|---|
| `TODO.md` | Die eine Liste offener Punkte und Entscheidungen, mit Erledigt-Historie | **aktuell**, hier zuerst schauen |
| `erledigt.md` | Was erledigt wurde und warum — am 2026-09-27 aus `TODO.md` herausgelöst, weil 65 erledigte gegen 24 offene Punkte die Liste unlesbar machten | Historie, erklärt Entscheidungen |
| `migrationsplan.md` | Wie das Skript aus den Folien 2025/26 entstanden ist; Zuordnung Vorlesung ↔ Kapitel ↔ Blatt ↔ Klausur; Links zu den Google-Slides 2025 | Referenz, Historie |
| `klausur-abdeckung.md` | Abgleich des Klausur-Aufgabenschatzes 2025/26 mit den Kapiteln | Referenz (Stand 2026-09-17, Kapitelnamen gelten weiter) |
| `diskussion-vorlesung-vs-skript.md` | Was die Aufzeichnungen 2025/26 über das Skript sagen: neun Thesen, Konrads Entscheidungen, Umsetzung | abgeschlossen, Entscheidungen umgesetzt |
| `vorschlag-grundlagen.md` | Zwölf Grundlagen-Snippets und wo sie eingebaut wurden | abgeschlossen, umgesetzt |
| `codecheck-2026-09-24.md` | Alle 24 Python-Blöcke der Kapitel ausgeführt: was lief, was nicht, mit Umgebung | Referenz (Stand 2026-09-24) |
| `folien-review-2026-09-25.md` | Durchsicht der 15 Beamer-Decks: Schriftbild, Titel/Labels, Ablaufplan-Nummern, Blatt-Zuordnung, fachliche Unschärfen, fehlende Bilder | A1–A3, Blatt-Verweise, VL-3-Code erledigt (2026-09-25); A5 und alles zu VL 1 erledigt (2026-10-02); Rest offen |
| `folien-review-vl01-2026-10-02.md` | Durchsicht des VL-1-Decks vor der ersten Sitzung: Umfrage-Fenster, Ablaufplan, Notizseite, Auflösung der Quizfrage, Take-Home, Bilder, Bildnachweis, Header (babel statt `german.sty`, Markenfarbe) — mit Gegenprobe nach dem Umbau | abgeschlossen, alles umgesetzt (2026-10-02); Muster für die übrigen Decks |
| `folien-review-vl02-2026-10-02.md` | Durchsicht des VL-2-Decks nach der Playbook-Prüfliste: σ gegen τ (Wurzel in `make_figures.py`), fünf Fragen ohne Antworten, XOR ohne Auflösung, Bias-Update, Bildbreiten — mit Gegenprobe | abgeschlossen, alles umgesetzt (2026-10-02) |
| `folien-review-vl03-2026-10-28.md` | Durchsicht des VL-3-Decks am Vorlesungstag: fehlende Multimodal-Folie (Ablaufplan rechnete mit 19 Seiten), neue Folie zum Torch-Tensor, Reshape-Notiz, Batch gegen Datensatz — und das WMT19-Beispiel, das ohne `sacremoses` seit 2025 nicht lief | abgeschlossen, alles umgesetzt und hochgeladen (2026-10-28) |
| `build-log-2026-09-27.md` | Playbook-Durchgang: Messwerte vorher/nachher, die zwei Konversions-Fehlerklassen, minted zurück, Gegenprobe im Image | Protokoll, abgeschlossen |
| `build-log-2026-10-15.md` | Abhängigkeiten angehoben: mystmd 1.10.1 auf 1.11.0 (beide Anheftungen), numpy, torch, transformers, huggingface-hub 2.x; Messwerte des Baus vorher/nachher, zwei Randbefunde (`scipy` undeklariert, torch cu130 gegen Treiber 12.9) | Protokoll, abgeschlossen |
| `build-log-2026-10-19.md` | Veröffentlichungs-Metadaten nachgerüstet: Vorschaukarte, Sitemap ohne `localhost`, Canonical, JSON-LD mit den drei Werken desselben Autors; Messwerte, die zwei Adressen dieser Seite, was aus den Schwesterbüchern nicht portiert wurde | Protokoll, abgeschlossen |
| `mathe-hintergrund-2026-10-19.md` | Was das Skript an Mathematik still voraussetzt: Messung über alle Kapitel, was das Buch selbst einführt, was die Übungsblätter abdecken (und was nicht), was bewusst draußen blieb | Befundnotiz zum Kapitel „Hintergrundwissen Lineare Algebra“ |
| `patch_myst_tex.py` | Repariert den mystmd-Fehler, der vor jeden Bindestrich in Codeblöcken ein Leerzeichen setzt | **nach jedem `uv sync`** laufen lassen; im CI-Image automatisch |
| `check_pdf_build.py` | Prüft das gebaute PDF: LaTeX-Fehler, Abbruch, fehlende Glyphen, Seitenzahl, Stichproben | läuft im CI-Job `build-pdf`, lokal vor jedem PDF-Commit |
| `pruefliste_durchsicht.py` | Erzeugt die Prüfliste der fachlichen Durchsicht: Formelblöcke, Zahlen, Jahre, Quellen, Bibliotheksangaben, Antwortproben, Boxen und Links je Kapitel, in Vorlesungsreihenfolge | für die Durchsicht; liest nur, Ausgabe in den Scratchpad |
| `check_doku.py` | Prüft die Doku gegen das Repo: Pfade, Zahlen, `--min-pages`, Vollständigkeit dieses Index, und die Regeln, die im Buch gelten | vor jedem Push, der Doku oder Struktur anfasst |
| `sprachpruefliste.py` | Erzeugt die Atome des **Sprachdurchgangs**: Typografie (Anführungszeichen, Striche, Leerzeichen, Wortdoppelungen), Abkürzungsvarianten, lange Sätze und eine gefilterte Rechtschreibliste. Prüft nur Prosa — Code, Mathe und Directives werden vorher herausgenommen | für den Sprachdurchgang; liest nur, Ausgabe in den Scratchpad. Braucht `aspell` mit deutschem Wörterbuch |
| `sprachpruefliste-woerter.txt` | Die Projektwortliste dazu: was hier steht, meldet die Rechtschreibprüfung nicht mehr. Wächst mit jedem Durchgang; ein Wort kommt erst hinein, wenn jemand es angesehen hat | wird von `sprachpruefliste.py` gelesen |
| `grammatikpruefung.py` | Prüft die Prosa mit **LanguageTool** auf das, was `aspell` prinzipiell nicht sieht: Kongruenz, Zusammenschreibung und — der eigentliche Ertrag — uneinheitlich gekoppelte Komposita (`Lehrermodell` neben `Lehrer-Modell`). Gefiltert auf die zwölf Regeln, die im Buch je etwas Echtes gefunden haben; ungefiltert sind es 1 930 Treffer auf 6 Befunde | einmal je größerem Umbau, **nicht** in der CI. Ephemer aufrufen (`uv run --no-project --with language-tool-python …`), braucht Java und ~260 MB; Ablage über `LTP_PATH` steuern |
| `folienprosa.py` | Holt die Prosa aus `slides/*.tex` — Gegenstück zu `prosa_zeilen()` für Beamer. Behält `\frametitle`, `\emph`, `\item` und vor allem `\note{}`; wirft Kommentare, `lstlisting`, Mathematik und Bildmakros weg. Im Docstring stehen die vier Fallen, die je eine Ladung Falschmeldungen erzeugt haben | Bibliothek, keine Kommandozeile; benutzt von `folienpruefliste.py` |
| `folienpruefliste.py` | Sprachprüfung der **Folien**: Typografie, Rechtschreibung und der Strich. In LaTeX ist `---` der Geviertstrich, den die Stilregeln in CLAUDE.md verbieten (D2) — am 2026-09-29 waren es 316 in 15 Decks | beim Folien-Durchgang; `--woerter`, `--deck 05` |
| `sprachpruefliste-woerter-folien.txt` | Die Wortliste der Folien. Getrennt von der des Buchs, damit Folienvokabular die Buchprüfung nicht stumpf macht; gelesen werden beide | wird von `folienpruefliste.py` gelesen |
| `check_links.py` | Prüft interne Linkziele auf Existenz und externe auf Erreichbarkeit (braucht Netz, urteilt nie nach einem HEAD) | vor dem Semesterstart und bei der Durchsicht; **nicht** in der CI |
| `check_ci_yaml.py` | Prüft `.gitlab-ci.yml` auf die Form, die GitLab erwartet (nicht nur auf YAML) | vor jedem Push, der die CI anfasst |
| `make_figures.py`, `embed_figures.py` | Abbildungen mit matplotlib erzeugen und einbetten | bei Bedarf erneut laufen lassen — **nur** mit `uv run --only-group figures`, nie mit dem System-Python (sonst ändern sich Abbildungen allein durch die matplotlib-Fassung) |

Die beiden einmaligen Umbau-Skripte von 2026-09-17 (`build_skript_from_2025.py`, das die erste
Prosafassung aus den Folien-PDFs erzeugte, und `restructure.py`, das daraus die Themen-Kapitel
schnitt) sind am 2026-09-27 **gelöscht** worden. Sie hätten das Repo zurückdrehen können:
`part-exercises/` samt Lösungen neu anlegen bzw. die heutigen 27 Kapitel mit einer alten
20-Kapitel-Fassung überschreiben. Wer sie als Protokoll braucht:
`git show 946600f:devnotes/restructure.py`.

Der Befundbogen der **fachlichen Durchsicht** liegt in `devnotes/durchsicht/` und ist **gitignored** —
`devnotes/durchsicht/durchsicht-2026-10.md` trägt Verfahren, Übergabe, Fortschritt je Kapitel und die
Befunde des Durchgangs, also Zwischenstände und offene Entscheidungsfragen. Das Projekt ist
öffentlich; ins Repo kommt, was aus den Befunden folgt, nicht der Weg dahin. Die
Werkzeuge dazu (`pruefliste_durchsicht.py`, `sprachpruefliste.py`, `grammatikpruefung.py`,
`check_links.py`) stehen oben im Index und sind versioniert.

Die Übungsblätter von 2025 samt Lösungsvorschlägen liegen seit dem 2026-09-27 in
`../uebungen-2025/` (gitignored, nur in Sciebo) und sind aus der git-Historie entfernt —
vorher standen sie im Buch, die Lösungen also im veröffentlichten PDF.
`../uebungen-2025/README.md` sagt, was dort liegt und warum.

Die Vorlesungsaufzeichnungen 2025/26 (Transkripte, Standbilder, Sitzungsnotizen, Übersicht, Abschlussbericht) liegen in
`../transcripts/` (gitignored, nur in Sciebo). Der Vorlesungsplan 2026/27 steht in `../kurs-2026-27.md`.
