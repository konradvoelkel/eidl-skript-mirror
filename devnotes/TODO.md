# TODO eidl-skript

Stand: 2026-10-19, nach dem Nachrüsten der Veröffentlichungs-Metadaten. **Hier stehen nur offene Punkte**; was erledigt ist,
steht in [`erledigt.md`](erledigt.md). Punkte mit **[Entscheidung]** brauchen eine
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

Erwartung: **29 Kapitel plus Glossar, 120 Seiten A4 lokal** (veröffentlicht eine Seite
mehr — die Abweichung ist seit dem 2026-10-15 erklärt, siehe `../CLAUDE.md`), 0 LaTeX-Fehler, 0 fehlende Glyphen,
5 überlange Zeilen, 23 Übungsabschnitte. Weicht etwas davon ab, ist das der erste Befund, nicht
Hintergrundrauschen.

**Womit anfangen**, wenn nichts anderes vorgegeben ist:

1. **Der Sprachdurchgang ist durch — Buch *und* Folien** (2026-09-29, 24 Befunde:
   R1–R13, E1–E6, dazu 8 in den Decks). Verfahren, Befunde und Entscheidungen stehen in
   `devnotes/durchsicht/sprachdurchgang-2026-10.md`; die Konventionen D1–D6 sind in
   `CLAUDE.md` unter „Schreibstil“ festgeschrieben, damit kein späterer Durchgang sie neu
   verhandelt. Vier versionierte Werkzeuge: `sprachpruefliste.py` (+ Wortliste),
   `grammatikpruefung.py`, `folienprosa.py`, `folienpruefliste.py` (+ Folienwortliste).
   Alle Prüfungen melden **null**.

   **Zwei Dinge, die dabei aufgefallen sind und nicht Sprache sind:**

   * **Der Folienbau war kaputt und hat es verschwiegen.** `/usr/share/texmf` steht in
     `TEXMF` mit `!!` (nur Datenbank, nie Platte), und `/var/lib/texmf/ls-R-TEXMFMAIN`
     war sechs Wochen älter als das installierte Theme — **kein Deck baute**. `latexmk`
     meldet bei vorhandenem PDF „up-to-date“, deshalb gab `slides/build.sh` 15-mal `ok`
     aus und einmal `FEHLER`. Einmal `sudo mktexlsr` genügt (steht in
     `slides/README.md`); auf dieser Maschine liegt das Theme seit dem 2026-09-29 in
     `~/texmf/tex/latex/hhubeamer/`, weil `mktexlsr` Root braucht. Danach bauen alle
     Decks von Null, 0 zu volle Rahmen, Seitenzahlen unverändert.
     ***Offen, zwei kleine Sachen an `slides/build.sh`:*** (a) Der Default-Glob `*VL*.tex`
     trifft das Vorstellungs-Deck nicht — dort saßen drei der acht Folienbefunde, und es
     ist das, was Studierende vor der Anmeldung sehen. (b) Ein ausgefallener Bau meldet
     `ok`, weil `latexmk` bei vorhandenem PDF „up-to-date“ sagt.
   * **Kapitelfehler wandern in die Decks.** Drei der acht Folienbefunde waren
     Durchreichungen aus dem Buch (dieselben Stellen wie R7, R12, E2). Wer am Buch
     korrigiert, sucht es in `slides/` gleich mit.

   **Was ein dritter Durchgang täte:** die Kapitel am laufenden Text auf Bezüge lesen
   („dieses“, „das“ — worauf?), was keine Maschine prüft. Alles Mechanische ist erledigt.
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
| Eingangsumfrage schließt am 14.10. um 13:55, also mit der ersten Sitzung | „Beamer-Folien“ | so lassen; die Notiz in VL 1 sagt seit 2026-10-02 „jetzt, nicht morgen“. Alternative: Fenster in ILIAS bis 15.10. verlängern, dann die Notiz zurückdrehen |
| Mark-I-Foto (`images/vl01-mark-i-perceptron.jpg`) im öffentlichen Repo, Rechte ungeklärt: Wikipedia nutzt dieselbe Aufnahme nur unter Fair Use | „Beamer-Folien“, `folien-review-vl01-2026-10-02.md` | Rechteangabe bei Cornell (`ss:550351`) im Browser nachsehen; wenn nicht frei, durch das US-Navy-Foto bei Wikimedia Commons ersetzen (Public Domain) |

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
  die Termine stehen fest, die Punkte hängen an der Entscheidung oben. **Die TeX-Quellen 2026/27 liegen
  seit dem 2026-10-12 in `../../exercises/`** (Sciebo, kein Repo, wie bei ds2-26 und eipy-26): Header,
  Blatt 0 und Blatt 1 mit `build.sh` und `ILIAS-UPLOAD-CHECKLISTE.md`; Blatt 1 trägt 11 Punkte und
  den 21.10.2026 (Vorschlag umgesetzt, Grenze bleibt die Hälfte). Blätter 2 bis 11 stehen noch aus;
  Vorlage ist `~/Sciebo/hhu/eidl-25/exercises/`, die Nachträge 2b und 1b stehen in `../uebungen-2025/blaetter/`.
  **In ILIAS hängen an den Übungseinheiten noch die 2025er PDFs** (nachgesehen 2026-10-12), siehe Checkliste.
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

- [ ] Rest aus der Durchsicht vom 25.09. (`folien-review-2026-09-25.md`): Ablaufplan-Foliennummern in
  9 Decks (VL 1 ist am 2026-10-02 nachgezogen), fachliche Punkte in VL 5/7/9/14 (Abschnitt B), Bilder
  für VL 10/13/15 und acht zu kleine Bilder (Abschnitt C; die Briefmarken-Folie in VL 1 ist erledigt).
  Die Notizseite ist seit dem 2026-10-02 im Header geregelt (`note page` plain + `\scriptsize`) und
  gilt für alle Decks.
- [ ] Decks inhaltlich gegenlesen und im Hörsaal erproben; Folien-PDFs in ILIAS hochladen (die kopierten
  Dateien dort sind noch die von 2025/26). **VL 1 und VL 2 sind gegengelesen und umgebaut**
  (`folien-review-vl01-2026-10-02.md`, `folien-review-vl02-2026-10-02.md`); die übrigen 13 nach
  demselben Muster (Prüfliste: `~/Sciebo/hhu/PLAYBOOK-folien.md` §3): Ablaufplan gegen die
  Frame-Reihenfolge, Notizenfassung bauen, Termine und Ansagen gegen `kurs-2026-27.md` und die
  ILIAS-Konfiguration (`../../ilias/runs/ws2026-27.yaml`, der Schwesterordner neben dem Repo),
  Kapitelfehler mitsuchen.
- [ ] **Vor VL 2 am TeX-Blatt nachsehen, ob der Ugly-Code-Link von 2025 noch drin ist.** Die Notiz
  zur letzten Folie von VL 2 verweist bedingt darauf; die Markdown-Fassung von 2025 hat ihn nicht.

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
- [ ] **ruff-Befunde in den übrigen `devnotes/`-Skripten** (Inventar vom 2026-10-16, nachdem
  `make_figures.py` sauber ist): 7 FURB167, 5 EXE001 (dieselbe Sache — Shebang ohne x-Bit, in
  `check_doku.py`, `check_links.py`, `embed_figures.py`, `folienpruefliste.py`,
  `pruefliste_durchsicht.py`), 4 RUF100, 3 ISC004, 2 B023, je eines UP031, I001, BLE001.
  *Vorschlag:* die fünf `EXE001` mit einem `chmod +x` erledigen (die Shebang-Zeile behauptet
  es ohnehin), den Rest einmal durchgehen, wenn sowieso jemand in den Skripten arbeitet.
  **Nicht** `ruff format`: alle zwölf Skripte würden umgeschrieben, und Formatierung ist in
  diesem Repo keine Konvention.
- [ ] **Das HHU-Beamer-Theme fehlt auf dieser Maschine.** `slides/build.sh` scheitert mit
  „File `beamerthemehhubeamer.sty' not found“; `slides/README.md` sagt richtig, dass es unter
  `/usr/share/texmf/tex/latex/beamer/themes/` liegen muss, dort liegt aber nichts. Kopien gibt es
  in `~/Sciebo/hhu/ds2026/ds-skript/slides/hhu-beamer-theme/` und in `~/Sciebo/hhu/ds2025/slides/`.
  Am 2026-09-27 behelfsweise mit `TEXINPUTS=".:…/hhu-beamer-theme//:"` gebaut. Vor der ersten
  Sitzung am 14.10. richtig installieren, sonst lässt sich kein Deck aktualisieren.
- [ ] **`scipy` fehlt in den Hauptabhängigkeiten.** Das CNN-Kapitel schreibt
  `from scipy.signal import convolve`; in `pyproject.toml` steht scipy seit dem 2026-10-14
  nur in der Gruppe `figures`, für den Code *im Buch* kommt es weiter bloß als
  Abhängigkeit von gensim und scikit-learn mit (gefunden beim Upgrade am 2026-10-15).
  *Vorschlag:* eine Zeile `"scipy>=1.18,<2"` zu den Hauptabhängigkeiten, mit Kommentar auf
  das Kapitel — dieselbe Form wie bei `sacremoses` und `ollama`.
- [ ] **`imagemagick` ist bewusst nicht im Image.** Dieses Buch hat 45 PNG und 2 JPG und kein einziges SVG, also
  wandelt MyST nichts. Sobald ein SVG dazukommt, meldet MyST das auf stdout, und `check_pdf_build.py --myst-log`
  liest es mit — dann gehören `imagemagick` und `librsvg2-bin` ins Dockerfile (wie in EiPy).
- [ ] **Nach dem ersten Deploy mit den Veröffentlichungs-Metadaten nachsehen** (2026-10-19
  gebaut, noch nicht veröffentlicht): `curl` auf `/sitemap.xml` (kein `localhost`, 30 echte
  URLs), auf `/` (`og:image` absolut, ein `rel="canonical"`, ein `ld+json`-Block) und die
  Karte einmal in einem Link-Vorschau-Dienst ansehen. „Lokal grün“ und „veröffentlicht“ sind
  zwei verschiedene Aussagen; Rezept in `../CLAUDE.md`.
- [ ] **Die Karten-URL wechselt bei jedem Deploy.** MyST vergibt den Fingerabdruck nicht
  nach dem Inhalt: Dieselbe, byte-gleiche PNG hieß in drei Läufen `3fd4fb7a…`,
  `1b231dd7…` und `130ef50e…`, und die URL des vorigen Laufs antwortet mit 404. Eine
  Plattform, die ihre zwischengespeicherte Vorschau erneuert, greift also ins Leere, bis
  sie die Seite neu liest. *Vorschlag:* die Karte im `pages`-Job zusätzlich unter einem
  festen Namen neben die Seite kopieren (aus dem Unterordner build/ des Artefakts in
  dessen Wurzel) und `og:image` darauf zeigen lassen — eine Zeile im Job und eine in
  `tools/head_meta.py`.
- [ ] **29-mal dieselbe `og:description`.** Keine Kapiteldatei hat eine eigene
  `description:` im Frontmatter, also tragen alle 29 Kapitelseiten die Beschreibung des
  Projekts — als Suchergebnis-Text 29-mal derselbe Satz, und im JSON-LD dieselbe
  `description` je Kapitel. *Vorschlag:* je Kapitel ein Satz im Frontmatter, beim nächsten
  inhaltlichen Durchgang mitgeschrieben. Inhaltsarbeit, kein Werkzeug.
- [ ] **`freshness.py` aus ds-skript portieren** (sichtbares Datum auf der Landingpage,
  `article:modified_time` je Seite, `<lastmod>` je Sitemap-Eintrag). `inject_jsonld.py`
  liest sein Datum einstweilen selbst aus `git log`; `<lastmod>` fehlt noch ganz, und das
  ist das Signal, an dem ein Crawler entscheidet, wann er wiederkommt.
- [ ] **`vendor_assets.py` aus ds-skript portieren.** Das Theme holt KaTeX, Font-Awesome und
  das Matplotlib-Widget-CSS weiterhin von zwei CDN — drei render-blockierende Stylesheets
  von fremden Servern, und das Buch zu lesen kontaktiert damit Dritte. Dort gelöst samt
  Prüfung (`check_css_assets.py`) und Herkunftsnachweis.
- [ ] **Bildmaße und Gliederungsreservierung** (ds-en `head_meta.py`, Abschnitte 7 und 9):
  `width`/`height` je Abbildung im Markup *und* im Stylesheet, dazu eine reservierte Höhe
  für die Gliederung. Beides senkt CLS; beides hängt dort an Messungen, die hier erst
  gemacht werden müssten, bevor man Zahlen behauptet.
- `_site/sidebar_footer.md` leer, `navbar_end.md` nur „Inhaltsverzeichnis“ – wie bei EiPy; lassen.
- Logo: `logo/` enthält SVGs und Exporte; für Rocket.Chat `logo/eidl-logo-512.png`.

## Erledigt

Die Historie steht in [`erledigt.md`](erledigt.md) — abgetrennt am 2026-09-27, weil sie mit
65 erledigten gegen 24 offene Punkte die Liste unlesbar machte. Sie erklärt, warum manches
ist, wie es ist; für die Frage „was ist zu tun“ steht sie im Weg.
