# Beamer-Folien 2026/27

Ein Deck pro Vorlesungswoche, gebaut aus den Kapiteln des Skripts. Die Zuordnung
Woche → Kapitel steht in [`../kurs-2026-27.md`](../kurs-2026-27.md).

## Bauen

```
latexmk -lualatex "Einführung in Deep Learning 2026 VL 01 Was ist Deep Learning.tex"
```

Gebraucht wird das HHU-Beamer-Theme (`hhubeamer`) unter
`/usr/share/texmf/tex/latex/beamer/themes/` und die Schrift Source Sans Pro.

**Wenn der Bau „File `beamerthemehhubeamer.sty' not found“ meldet, obwohl die Datei da
liegt**, ist die kpathsea-Datenbank älter als das Theme. `/usr/share/texmf` ist in `TEXMF`
mit `!!` eingetragen, und das heißt: nur die Datenbank befragen, nie die Platte ansehen.
Am 2026-09-29 war `/var/lib/texmf/ls-R-TEXMFMAIN` vom 31. März, das Theme vom 11. Mai –
kein Deck baute, und `latexmk` verschleierte es, weil es bei vorhandenem PDF
„up-to-date“ meldet statt neu zu bauen. Abhilfe:

```sh
sudo mktexlsr
```

Ohne Root-Rechte behilft man sich mit einer Kopie **außerhalb** der `!!`-Bäume – ein Pfad
in `TEXINPUTS`, der in einen `!!`-Baum zeigt, hilft nämlich nicht:

```sh
cp -r /usr/share/texmf/tex/latex/beamer/themes/hhubeamer /tmp/
TEXINPUTS="/tmp/hhubeamer//:" sh build.sh
```

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
* Die PDFs sind Build-Artefakte und stehen in `.gitignore`; verteilt werden sie
  über ILIAS.
