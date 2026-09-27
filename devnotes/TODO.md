# TODO eidl-skript

Stand: 2026-09-27, nach dem Umbau der Übungen. **Hier stehen nur offene Punkte** (24 Stück); was
erledigt ist, steht in [`erledigt.md`](erledigt.md). Punkte mit **[Entscheidung]** brauchen eine
Antwort von Konrad; ein Vorschlag steht jeweils dabei.

## Einstieg

**Lesereihenfolge:** `../CLAUDE.md` (wie hier gearbeitet wird — Bauen, Stil, Markup-Fallen, bewusste
Entscheidungen) → diese Liste → `build-log-2026-09-27.md` (was am 27.09. umgebaut wurde und warum,
mit Messwerten) → `~/Sciebo/hhu/PLAYBOOK.md` (CI, Image, PDF-Prüfung; gilt für alle drei HHU-Bücher).
Was sonst in `devnotes/` liegt, steht in `devnotes/README.md`.

**Stand prüfen** (fünf Minuten, bevor man etwas ändert):

```sh
uv sync && uv run devnotes/patch_myst_tex.py      # der Patch ist nach jedem sync nötig
uv run _site/vendor/install_template.py
uv run --only-group dev myst build --html         # keine Warnungen erwartet
uv run --only-group dev myst build --pdf
uv run devnotes/check_pdf_build.py --min-pages 100
uv run devnotes/check_doku.py           # stimmt die Doku noch mit dem Repo überein?
```

Erwartung: **27 Kapitel plus Glossar, 113 Seiten A4**, 0 LaTeX-Fehler, 0 fehlende Glyphen,
5 überlange Zeilen, 23 Übungsabschnitte. Weicht etwas davon ab, ist das der erste Befund, nicht
Hintergrundrauschen.

**Womit anfangen**, wenn nichts anderes vorgegeben ist:

1. **Fachliche Durchsicht der Prosafassung** (Abschnitt „Inhalt“, erster Punkt). Der größte offene
   Posten und der einzige, der das Buch besser macht statt nur ordentlicher. Verfahren, Übergabe und
   Befunde stehen in `devnotes/durchsicht/durchsicht-2026-10.md` — **dort** wird gearbeitet, nicht in
   dieser Liste; hier bleibt der Punkt als Verweis stehen, bis er erledigt ist. Der Ordner ist
   gitignored (nur lokal und in Sciebo), die Werkzeuge dazu sind versioniert.
2. **Die echten Übungsblätter auf 2026/27 anziehen** (Abschnitt „Übungsblätter“): Punkte und
   Bestehensgrenzen, die Kopfzeile je Blatt, Blatt 12 als Take-Home-Probeklausur. Sie werden **in
   TeX** gepflegt, nicht hier — `uebungen-2025/blaetter/` ist nur die Markdown-Konversion von 2025.
3. **Folien gegenlesen und in ILIAS hochladen** (Abschnitte „Beamer-Folien“ und „ILIAS“).
4. Die kleinen Reste unter „Infrastruktur“ — alle geprüft und beschrieben, keiner dringend.

**Was auf Konrad wartet** (alles andere ist Arbeit, keine Entscheidung):

| | Wo | Vorschlag |
|---|---|---|
| Punkte und Bestehensgrenzen der Blätter 1, 3, 5 | „Übungsblätter“ | je +1 Punkt, Grenze bleibt „die Hälfte“ |
| Reserve-Kapitel 26/27: raus oder 16. Termin? | „Vorlesungsplan“ | 15 Termine wie 2025 |
| Blatt 6 kommt vor der Autoencoder-Vorlesung | „Übungsblätter“ | vertagt bis zur Blatt-Überarbeitung |
| Antwortenbox in Kapitel 01 steht im PDF offen | „Inhalt“ | in einen Anhang oder auf eine Antwortprobe eindampfen |
| Anhang mit den Endergebnissen der Übungen? | „Übungsblätter“ | erst, wenn die Antwortproben sich als zu dünn erweisen |

Der erste Punkt ist der einzige, der jemanden blockiert: An ihm hängt die Kopfzeile „N Punkte,
Abgabe bis …“ in den TeX-Blättern.

**Drei Dinge, die man nicht nebenbei ändert:**

* **Das Repository ist öffentlich.** Keine Lösungen, keine Klausuraufgaben, keine Personendaten in
  Dateien, die committet werden. `uebungen-2025/` und `transcripts/` sind deshalb gitignored.
* **Die Anheftungen** (Basis-Image per Digest, Debian-Pakete per Snapshot, mystmd per Version,
  kaniko per Tag). Wer eine anhebt, baut das Image und prüft das PDF im Container, bevor er
  committet — das Rezept steht im Dockerfile und in PLAYBOOK §3.2.
* **Das tex-Template.** Es trägt nur, was für alle drei Bücher gilt; Buchspezifisches gehört in
  `options.preamble` in der `myst.yml` (PLAYBOOK §3.8i).

## Inhalt (Skript)

- [ ] **Fachliche Durchsicht** der Prosafassung — Verfahren und Befundbogen in
  `devnotes/durchsicht/` (gitignored, nur lokal), Werkzeuge `devnotes/pruefliste_durchsicht.py`
  und `devnotes/check_links.py`. Zwei Sorten von Stellen:
  - *(a) Stoff, der in der Vorlesung 2026/27 vorkommen soll* (steht im Plan in `kurs-2026-27.md` oder wird in der
    Klausur gefragt): Hyperebenen-Geometrie und Abstand (02), Ein-Sample-Argument für die Perzeptronregel (03),
    Batch-Bild für Tensoren (05), Numerik-Box zu `exp`/`log` (06), Maximum Likelihood → BCE und Gradient $p - y$
    (07/08), Summe über Pfade und numerische Probe (08), Feature-Skalierung (08), Erwartungswert-Absatz zu SGD (08),
    Playground-Box (09), VAE-Fragenbox (15), GAN-Lab-Box mit Regel „früh aufhören“ (22), CBOW-Formel (16),
    Ausgabegrößen-Formel und Shape-Beispiel (20), Minimax-Formel (22), Reparametrisierung (15), $T^2$-Faktor (25),
    Antwortbox zu GPU/SIMD, PyTorch, CUDA/ROCm (01), Rezept Anwendungskonzept (24), Glossar (`glossar.md`).
  - *(b) Vertiefungen*, als aufklappbare Box „Vertiefung: …“ markiert und nicht Vorlesungsstoff:
    Konvergenzsatz (03), Cauchy-Schwarz (08), Spur-Trick (09), Message-Passing-Formel (17), Wasserstein-Dualität (22),
    FGSM (27). Nur auf Korrektheit prüfen, nicht auf Didaktik.
  - Erste Befunde stehen schon im Bogen: die Lernrate heißt in 03 $r$ und ab 07/08 $\rho$ (**N1**),
    $\sigma$ ist in 15 die Streuung statt der Sigmoidfunktion (**N2**), und der paperswithcode-Link
    in 11 leitet heute auf eine unbezogene Seite weiter (**K1** — behebt zugleich die längste
    überlange Zeile im PDF).
  - Konkrete Prüfaufträge: Encoder mit oder ohne Sigmoid in „Autoencoder“ (14) entscheiden (Skript: ohne, mit
    Hinweis „man kann auch“; Vorlesung 2025: mit – der Verweis auf 2025 steht seit 2026-09-21 nicht mehr im Text); die neuen Lösungsvorschläge zu Blatt 1 Aufgabe 4b, Blatt 3 Aufgabe 2b und Blatt 5
    Aufgabe 1b gegenrechnen; die „Weiterlesen“-Boxen (17 Kapitel) auf passende UDL/MML-Kapitelnummern prüfen.
- [ ] **Die Antwortenbox in Kapitel 01 steht im PDF offen da.** „Antworten zum Lesetext“ (drei Fragen zum
  HPCwire-Artikel) ist eine `dropdown`-Box — im HTML zugeklappt, im PDF nicht, weil `dropdown` im
  LaTeX-Export keine Wirkung hat. Wer das PDF liest, sieht die Antworten direkt unter den Fragen. Dieselbe
  Mechanik hat bis zum 2026-09-27 die Lösungsvorschläge der Übungsblätter veröffentlicht; hier ist es kein
  Vertraulichkeitsproblem, nur ein didaktisches. Optionen: so lassen, in einen Anhang verschieben, oder wie
  bei den Übungen auf eine Antwortprobe eindampfen. Die sechs `Vertiefung:`-Boxen sind davon nicht betroffen
  — sie sollen gelesen werden.
- [ ] **Abbildungen**, verbleibende Wünsche (alle `<!-- TODO Abbildung -->`-Marker sind seit 2026-09-20 aufgelöst,
  entweder durch eigene Bilder, Bilder aus den Musterlösungen 2025 oder Links): Hubel & Wiesel und GRU/LSTM sind
  nur verlinkt (Wikipedia, CC-BY-SA); wer sie einbetten will, lädt die Dateien nach `images/` und ergänzt den
  Lizenzhinweis in der Bildunterschrift.
- [ ] „Rezept Anwendungskonzept“ (24) ist geschrieben; die 2025 angekündigte Klausurfrage „wie trainiert man das
  Netz für das Empfehlungssystem“ ist dort noch nicht als ausformulierte Aufgabe, nur als Absatz im Beispiel.
- [ ] Zeitreihen / Aktienkurs-Beispiel (2025 gewünscht, nicht geliefert): bewusst zurückgestellt, sprengt den Rahmen.
  `notebooks/ASML.csv` liegt bereit, falls „RNNs“ (18) später ein Beispiel bekommen soll.

## Vorlesungsplan (`kurs-2026-27.md`)

- [ ] **[Entscheidung]** Die Reserve-Kapitel 26/27 ganz aus dem Plan nehmen oder als 16. Termin (Fragestunde vor
  der Klausur) einplanen? *Vorschlag:* 15 Termine wie 2025, Reserve nur, wenn eine Woche ausfällt.

## Übungsblätter

- [ ] **Offen aus dem Vorschlag:** ob die Antwortproben genügen oder ein Anhang mit den Endergebnissen
  (nicht den Rechenwegen) dazukommt, und wie sich die Übungen zu einem etwaigen Kapitel-Abspann mit
  Kontrollfragen verhalten (wie in eipy-skript) — sonst steht dreimal dasselbe am Kapitelende.
- [ ] **[Entscheidung] Punkte und Bestehensgrenzen** der Blätter 1, 3, 5 nach den neuen Aufgaben 4b, 2b, 1b
  anpassen (*Vorschlag:* je +1 Punkt, Bestehensgrenze bleibt „die Hälfte“).
- [ ] Die Zeile „N Punkte, Abgabe bis …“ je Blatt eintragen — **in den TeX-Quellen**, nicht mehr im Skript;
  die Termine stehen fest, die Punkte hängen an der Entscheidung oben.
- [ ] **[Entscheidung vertagt]** Blatt 6 (Iris-Autoencoder) wird nach dem neuen Wochenplan eine Woche *vor* der
  Autoencoder-Vorlesung ausgegeben (AE ist jetzt VL 8 statt VL 7, CNNs VL 11, LLMs VL 12). Optionen: Blätter 6/7
  in der Ausgabe tauschen, Blatt 6 anpassen, oder so lassen (Skript-Kapitel steht online). Bei der
  Blatt-Überarbeitung ansehen; in ILIAS ist vorerst die unveränderte Reihenfolge eingetragen.
- [ ] Blatt 12 = Take-Home-Probeklausur anlegen (Grundlage: `~/Sciebo/hhu/eidl-25/exam/`, Probeklausur 2025).
- [ ] Lösungen: Die 15 Textlösungen von 2025 liegen in `uebungen-2025/loesungen/`, Notebook- und
  Skriptlösungen in `~/Sciebo/hhu/eidl-25/exercises/blattNN-solution/`. Beides gitignored bzw. außerhalb.
  *Vorschlag:* so lassen — ins öffentliche Repo gehört keine Lösung, und in ILIAS liegen sie ohnehin
  getrennt.

## Klausur

- [ ] `exam2026-eidl-exam-1/2.tex` (englische Entwürfe vom 20.01.2026 in `~/Sciebo/hhu/eidl-25/exam/`) – Status klären:
  Vorlagen für 2026/27?
- Keine weiteren Klausuransagen aus den Aufzeichnungen übernehmen (Entscheidung Konrad 2026-09-20).

## Notebooks

- [ ] `latent-classifier.ipynb` ist das einzige verbleibende Notebook mit Funktion (seit 2026-09-27 als
  `downloads:` am Kapitel 21).
  Vor Semesterstart mit aktuellem torch/transformers durchlaufen lassen (bert-medium-Download, `ipywidgets` für die
  Saliency-Zelle) und Outputs neu einchecken.
- [ ] Torch aus `uv sync` ist der cu130-Build, der NVIDIA-Treiber hier ist 12.9 → `torch.cuda.is_available()`
  ist False, alles läuft auf der CPU. Vor Demos im Hörsaal entweder Treiber aktualisieren oder einen
  passenden Torch-Build pinnen.

## Beamer-Folien (Schritt 4 des Migrationsplans)

- [ ] Rest aus der Durchsicht: Notizseite (`note page` plain + `\scriptsize`, sonst läuft die Titelnotiz
  über), Ablaufplan-Foliennummern in 10 Decks, fachliche Punkte in VL 5/7/9/14 (siehe Abschnitt B),
  Bilder für VL 10/13/15 und neun zu kleine Bilder (Abschnitt C).
- [ ] Decks inhaltlich gegenlesen und im Hörsaal erproben; Folien-PDFs in ILIAS hochladen (die kopierten
  Dateien dort sind noch die von 2025/26).

## ILIAS (Kurs 2026/27, ref_id 2165367)

Textfassung von Seite und Objektbaum: `~/Sciebo/hhu/eidl-26/ilias/` (analog zu
`~/Sciebo/hhu/ds2-26/ilias/`) — also **neben** diesem Repo, nicht darin. Workflow in
`~/Sciebo/hhu/eidl-26/ilias/README.md`, aktueller Durchlauf in
`~/Sciebo/hhu/eidl-26/ilias/runs/ws2026-27.yaml`.

- [ ] Vorlesungsfolien 2026/27 wöchentlich vor der Sitzung als **neue Dateien** in den Ordner „Vorlesungsfolien“
  hochladen und in der Wochentabelle verlinken (Entscheidung 2026-09-25: die 2025/26er Folien bleiben dort
  zugänglich, sind aber seit 2026-09-25 in der Tabelle entlinkt; Mechanik `unlinked_object_keys` in
  `~/Sciebo/hhu/eidl-26/ilias/runs/ws2026-27.yaml`).
- [ ] Zusatzmaterial aktualisieren: „EiDL-Klausur-2024“ durch die Erstklausur 2025/26 ersetzen, Probeklausur
  und Blatt 0 / Sheet 0 prüfen.
- [ ] Kurs online schalten, wenn die Blätter und die erste Foliensitzung stehen.

## Infrastruktur

- [ ] **Zwei Handgriffe in GitLab, die nur Konrad machen kann** (seit dem History-Rewrite vom
  2026-09-27 offen): *Settings → Repository → Protected branches* → bei `main` **Allowed to force
  push wieder ausschalten** (es wurde für den Rewrite eingeschaltet), und *Settings → Repository →
  Housekeeping* einen Lauf anstoßen, damit die vor dem Rewrite gepushten Objekte wirklich
  eingesammelt werden — bis dahin sind sie über ihre SHA erreichbar.
- [ ] `devnotes/embed_figures.py` hat nichts mehr zu tun: Es ersetzt `<!-- TODO Abbildung -->`-Marker,
  und davon gibt es null. Löschen wie die beiden Umbau-Skripte, oder behalten, falls neue Abbildungen
  wieder über Marker eingebaut werden? *Vorschlag:* behalten, bis die Abbildungsliste unter „Inhalt“
  abgearbeitet ist — dann löschen.
- [ ] Die verbliebenen überlangen Zeilen (9 am Tag der Änderung, 6 nach dem Einbau der Übungen) sind
  — die schlimmste davon ist Befund **K1** im Durchsichtsbogen, weil ihr Link ohnehin ins Leere führt —
  URLs im Linktext: MyST setzt sie als gewöhnlichen
  Text in `\href`, nicht als `\url`, deshalb greift keine URL-Trennung. Die schlimmste (77 pt) ist
  `paperswithcode.com/methods/category/activation-…` in 11. Abhilfe wäre, die Linktexte zu kürzen
  („paperswithcode“ statt der vollen Adresse) — Inhaltsarbeit, keine Technik.
- [ ] **Das HHU-Beamer-Theme fehlt auf dieser Maschine.** `slides/build.sh` scheitert mit
  „File `beamerthemehhubeamer.sty' not found“; `slides/README.md` sagt richtig, dass es unter
  `/usr/share/texmf/tex/latex/beamer/themes/` liegen muss, dort liegt aber nichts. Kopien gibt es
  in `~/Sciebo/hhu/ds2026/ds-skript/slides/hhu-beamer-theme/` und in `~/Sciebo/hhu/ds2025/slides/`.
  Am 2026-09-27 behelfsweise mit `TEXINPUTS=".:…/hhu-beamer-theme//:"` gebaut. Vor der ersten
  Sitzung am 14.10. richtig installieren, sonst lässt sich kein Deck aktualisieren.
- [ ] **`imagemagick` ist bewusst nicht im Image.** Dieses Buch hat 45 PNG und 2 JPG und kein einziges SVG, also
  wandelt MyST nichts. Sobald ein SVG dazukommt, meldet MyST das auf stdout, und `check_pdf_build.py --myst-log`
  liest es mit — dann gehören `imagemagick` und `librsvg2-bin` ins Dockerfile (wie in EiPy).
- `_site/sidebar_footer.md` leer, `navbar_end.md` nur „Inhaltsverzeichnis“ – wie bei EiPy; lassen.
- Logo: `logo/` enthält SVGs und Exporte; für Rocket.Chat `logo/eidl-logo-512.png`.

## Erledigt

Die Historie steht in [`erledigt.md`](erledigt.md) — abgetrennt am 2026-09-27, weil sie mit
65 erledigten gegen 24 offene Punkte die Liste unlesbar machte. Sie erklärt, warum manches
ist, wie es ist; für die Frage „was ist zu tun“ steht sie im Weg.
