# Beamer-Folien 2026/27

Ein Deck pro Vorlesungswoche, gebaut aus den Kapiteln des Skripts. Die Zuordnung
Woche → Kapitel steht in [`../kurs-2026-27.md`](../kurs-2026-27.md).

## Bauen

```
latexmk -lualatex "Einführung in Deep Learning 2026 VL 01 Was ist Deep Learning.tex"
```

Gebraucht wird das HHU-Beamer-Theme (`hhubeamer`) unter
`/usr/share/texmf/tex/latex/beamer/themes/` und die Schrift Source Sans Pro.

## Konventionen

* `Einführung in Deep Learning 2026 header.tex` ist der gemeinsame Header
  (Dokumentklasse, Theme, Listings-Setup) und wird von jedem Deck eingebunden.
* Bilder kommen per `\graphicspath{{../images/}}` direkt aus dem Skript – keine
  Kopien, damit eine Korrektur im Kapitel auch auf der Folie ankommt.
* **Wenig Text auf der Folie, die Ausführung in `\note{}`.** Die Folie ist der
  Gesprächsanlass; die Notizen enthalten die Dialogmuster aus den Aufzeichnungen
  2025/26 (`transcripts/*/notiz.md`, nicht im Repo), Zeitbudgets und die Fragen,
  die im Hörsaal gestellt werden.
* Fassung mit Notizen für den zweiten Schirm: im Deck die Zeile
  `\setbeameroption{show notes on second screen=right}` nach dem `\input{...header}`
  einkommentieren.
* Die PDFs sind Build-Artefakte und stehen in `.gitignore`; verteilt werden sie
  über ILIAS.
