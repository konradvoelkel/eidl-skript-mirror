# Beamer-Folien 2026/27

Ein Deck pro Vorlesungswoche, gebaut aus den Kapiteln des Skripts. Die Zuordnung
Woche → Kapitel steht in [`../kurs-2026-27.md`](../kurs-2026-27.md). Was für die Decks
*aller* HHU-Kurse gilt (Header, Bau, Notizenfassung, Prüfliste vor dem Upload), steht in
`~/Sciebo/hhu/PLAYBOOK-folien.md`; hier steht, was nur dieses Repo betrifft.

## Bauen

```
latexmk -lualatex "Einführung in Deep Learning 2026 VL 01 Was ist Deep Learning.tex"
```

Bequemer ist `./build.sh` – mit einer `.tex` als Argument baut es dieses Deck, ohne Argument
alle, und es meldet je Deck die Seitenzahl und die Zahl der zu vollen Rahmen
(`Overfull \vbox`). Mit `--notizen` als erstem Argument baut es statt der Folien die
**Notizenfassung** (siehe unten). Steht dort **„Rahmen NICHT geprueft"**, gehört das LaTeX-Log nicht zum
vorhandenen PDF – dann hilft `latexmk -g`, das den Lauf erzwingt. Das Skript liest die Zahl
nämlich aus dem LaTeX-Log neben der `.tex` und nicht aus der Ausgabe von latexmk: Ist das PDF
aktuell, startet latexmk LaTeX gar nicht erst, und in seiner Ausgabe steht dann kein einziges
`Overfull` – bis zum 2026-11-04 meldete das Skript in dieser Lage „0 zu volle Rahmen" für ein
PDF mit einem überfüllten Rahmen. Die ganze Geschichte samt der Fallen beim Reparieren:
`~/Sciebo/hhu/PLAYBOOK-folien.md` §2.4.

Gebraucht wird das HHU-Beamer-Theme (`hhubeamer`) unter
`/usr/share/texmf/tex/latex/beamer/themes/` und die Schrift **Source Sans 3**
(seit 2026-11-04; davor Source Sans Pro 2.021 — Adobe hat die Familie 2021
umbenannt, aktuell 3.052). `fontspec` sucht nach dem *Familiennamen*, der jetzt
„Source Sans 3“ lautet; lokal liegen die OTF in `~/.fonts/SourceSans3`, im
CI-Image kommt sie aus dem Debian-Paket `fonts-adobe-sourcesans3`. Beide Fassungen
stehen unter der SIL OFL. Die deutsche
Silbentrennung kommt über `babel` (Header); LuaTeX lädt die Trennmuster beim ersten Gebrauch
aus `hyph-utf8`, das zu jedem texlive gehört. Bis zum 2026-10-02 lud der Header das veraltete
`german.sty`, das im LuaTeX-Format keine deutsche Sprache fand – kein Deck trennte Silben, und
das Log sagte es nur in einer Zeile („\language number for German undefined“).

**Wenn der Bau „File `beamerthemehhubeamer.sty' not found“ meldet, obwohl die Datei da
liegt**, ist die kpathsea-Datenbank älter als das Theme. `/usr/share/texmf` ist in `TEXMF`
mit `!!` eingetragen, und das heißt: nur die Datenbank befragen, nie die Platte ansehen.
Am 2026-09-29 war `/var/lib/texmf/ls-R-TEXMFMAIN` vom 31. März, das Theme vom 11. Mai –
kein Deck baute, und `latexmk` verschleierte es, weil es bei vorhandenem PDF
„up-to-date“ meldet statt neu zu bauen. Abhilfe:

```sh
sudo mktexlsr
```

**Ohne Root-Rechte** legt man das Theme in den eigenen Baum. `~/texmf` steht in `TEXMF`
**ohne** `!!`, wird also live durchsucht und braucht gar keine Datenbank:

```sh
mkdir -p ~/texmf/tex/latex
cp -r /usr/share/texmf/tex/latex/beamer/themes/hhubeamer ~/texmf/tex/latex/hhubeamer
```

So ist es auf dieser Maschine seit dem 2026-09-29 eingerichtet. Zwei Dinge dazu: Die
Kopie **verdeckt** eine spätere Systemversion des Themes – wer das Theme aktualisiert,
aktualisiert auch diese Kopie oder löscht sie. Und ein Pfad in `TEXINPUTS`, der in einen
`!!`-Baum zeigt, hilft *nicht*: Die Sperre gilt nach Pfadpräfix, nicht nach Suchreihenfolge.

## Konventionen

* `Einführung in Deep Learning 2026 header.tex` ist der gemeinsame Header
  (Dokumentklasse, Theme, Listings-Setup) und wird von jedem Deck eingebunden.
* Bilder kommen per `\graphicspath{{../images/}}` direkt aus dem Skript – keine
  Kopien, damit eine Korrektur im Kapitel auch auf der Folie ankommt.
* **Wenig Text auf der Folie, die Ausführung in `\note{}`.** Die Folie ist der
  Gesprächsanlass; die Notizen enthalten die Dialogmuster aus den Aufzeichnungen
  2025/26 (`transcripts/*/notiz.md`, nicht im Repo), Zeitbudgets und die Fragen,
  die im Hörsaal gestellt werden.
* **Übungsblätter ohne Nummer** nennen („Übungsblatt“, „eine Übungsaufgabe“, „das nächste Blatt“),
  auf Folien wie in Notizen. Die Zuordnung Blatt ↔ Woche kann sich noch verschieben
  (`devnotes/TODO.md`); Nummern in den Decks wären dann falsch, ohne dass es jemand merkt.
* Der Header ersetzt die Frametitle-Vorlage des Themes durch eine Kopie mit Breitenbegrenzung
  (lange Titel brechen vor dem Logo um) und setzt Source Sans Pro als Sans-Schrift (das Theme lädt
  `helvet`, das unter LuaTeX nicht existiert). Titel trotzdem unter etwa 45 Zeichen halten.
* **Fassung mit Notizen für den zweiten Schirm:** `./build.sh --notizen` baut sie nach
  `notizen/` (gitignored), ohne das Deck anzufassen – gebaut wird eine Kopie mit
  einkommentierter Zeile `\setbeameroption{show notes on second screen=right}`. Von Hand
  geht es auch, indem man diese Zeile im Deck selbst einkommentiert; dann **überschreibt**
  der Lauf allerdings genau das PDF, das nach ILIAS geht, denn die Notizenfassung heißt
  gleich. Deshalb der eigene Ordner. Alle 15 Decks tragen die Zeile auskommentiert; fehlt
  sie, sagt das Skript das.
* **Nur die Notizen**, ohne Folienbild, zum Lesen vorher:

  ```sh
  latexmk -lualatex -pretex='\PassOptionsToClass{notes=only}{beamer}' -usepretex \
    -outdir=notizen "Einführung in Deep Learning 2026 VL 04 Logistische Regression.tex"
  ```

  Die Option muss als *Klassen*-Option kommen; `show notes on second screen` ist eine
  Dokument-Option und lässt sich so **nicht** setzen (sie braucht die Kopie oben).
* Fassung mit Notizen: Die Notizseite ist im Header ohne Vorschaubild und in `\scriptsize`
  eingestellt, weil Beamer Notizen nicht paginiert und die Titelnotiz von VL 1 (Ablaufplan
  plus Kürzungsregeln) sonst mitten im Satz abbricht. Wer eine Notiz schreibt, die länger ist
  als die von VL 1, baut die Notizenfassung einmal und sieht nach.
* **Bildnachweise** für Fotos, die nicht aus `devnotes/make_figures.py` stammen: Das Foto
  des Mark I Perceptron auf Folie „1958: gebaut, nicht simuliert“
  (`images/vl01-mark-i-perceptron-navy.jpg`, 1800 × 1409 px) ist eine Aufnahme der **U.S.
  Navy** vom 24. Juni 1960, veröffentlicht vom National Museum of the U.S. Navy
  ([Wikimedia Commons](https://commons.wikimedia.org/wiki/File:330-PSA-80-60_(USN_710739)_(20897323365).jpg),
  Flickr-Original `330-PSA-80-60 (USN 710739)`). Als Werk von Bediensteten der US-Regierung
  im Dienst ist sie in den USA gemeinfrei; Commons führt sie unter *Public Domain Mark*.
  Sie zeigt die Kamera mit dem Cornell-C vor dem Fotozellenraster.
* **Vorher stand dort ein anderes Foto** (`vl01-mark-i-perceptron.jpg`, der geöffnete
  Schrank mit dem Drahtbündel) aus den Digital Collections der Cornell University Library,
  Katalognummer `ss:550351`. Dessen Rechteangabe lautet dort wörtlich „For information
  regarding copyright for this image, send inquiries to rarerepro@cornell.edu“ — Cornell
  erteilt also **keine** Lizenz und macht keine Aussage zur Nachnutzung; das Bild stammt aus
  den *Cornell University News Service records*, einer Sammlung der Universität, nicht aus
  einer Bundesbehörde. Die englische Wikipedia nutzt dieselbe Aufnahme nur **unter Fair
  Use** und führt sie als geschützt. Am 2026-11-04 nachgesehen und ersetzt, weil die Decks
  öffentlich ausgeliefert werden sollen. Wer das Originalfoto trotzdem will, fragt bei
  `rarerepro@cornell.edu` an. **Im Git-Verlauf liegt die alte Datei weiter**; sie aus der
  Historie zu entfernen hieße, die gespiegelten Repositories neu zu schreiben.
* Die PDFs sind Build-Artefakte und stehen in `.gitignore`; verteilt werden sie
  über ILIAS **und seit dem 2026-11-04 über die Website**: Der Job `build-slides`
  baut sie im CI, `pages` legt sie als `/folien/vl01.pdf` … `/folien/vl15.pdf` ab
  (kurze Adressen, weil die Kapitel sie mit `#page=` verlinken). Das Theme kommt
  dafür aus der **Paketregistry** des Projekts in das Image — es darf nicht ins
  Repository, weil es keinen Lizenzvermerk hat und das HHU-Logo enthält, und der
  GitHub-Spiegel ist öffentlich. Fehlt das Paket, scheitert nur `build-slides`
  (mit `allow_failure`), und die Meldung sagt, was zu tun ist. Dasselbe gilt für alles andere, was der Bau erzeugt – `.aux`, `.nav`,
  `.snm`, `.toc`, `.out`, `.vrb` und Verwandte gehören nicht ins Repo.
