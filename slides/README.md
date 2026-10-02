# Beamer-Folien 2026/27

Ein Deck pro Vorlesungswoche, gebaut aus den Kapiteln des Skripts. Die Zuordnung
Woche → Kapitel steht in [`../kurs-2026-27.md`](../kurs-2026-27.md).

## Bauen

```
latexmk -lualatex "Einführung in Deep Learning 2026 VL 01 Was ist Deep Learning.tex"
```

Gebraucht wird das HHU-Beamer-Theme (`hhubeamer`) unter
`/usr/share/texmf/tex/latex/beamer/themes/` und die Schrift Source Sans Pro. Die deutsche
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
* Fassung mit Notizen für den zweiten Schirm: im Deck die Zeile
  `\setbeameroption{show notes on second screen=right}` nach dem `\input{...header}`
  einkommentieren.
* Fassung mit Notizen: Die Notizseite ist im Header ohne Vorschaubild und in `\scriptsize`
  eingestellt, weil Beamer Notizen nicht paginiert und die Titelnotiz von VL 1 (Ablaufplan
  plus Kürzungsregeln) sonst mitten im Satz abbricht. Wer eine Notiz schreibt, die länger ist
  als die von VL 1, baut die Notizenfassung einmal und sieht nach.
* **Bildnachweise** für Fotos, die nicht aus `devnotes/make_figures.py` stammen: Das Foto des
  Mark I Perceptron (`images/vl01-mark-i-perceptron.jpg`, VL 1, 1024 × 1352 px) stammt vom
  Cornell Aeronautical Laboratory; die Vorlage liegt in den Digital Collections der Cornell
  University Library, Katalognummer `ss:550351`
  (<https://digital.library.cornell.edu/catalog/ss:550351>). Die englische Wikipedia nutzt
  eine kleine Fassung desselben Fotos als `File:Mark_I_perceptron.jpeg` **unter Fair Use**
  und führt es als urheberrechtlich geschützt. Das Foto war schon in den Folien 2023 und
  2025; die Herkunft stand bis zum 2026-10-02 nirgends, und die Rechtefrage für das
  öffentliche Repository ist offen (`devnotes/TODO.md`).
* Die PDFs sind Build-Artefakte und stehen in `.gitignore`; verteilt werden sie
  über ILIAS. Dasselbe gilt für alles andere, was der Bau erzeugt – `.aux`, `.nav`,
  `.snm`, `.toc`, `.out`, `.vrb` und Verwandte gehören nicht ins Repo.
