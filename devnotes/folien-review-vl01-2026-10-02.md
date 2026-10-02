# Durchsicht des VL-1-Decks (2026-10-02)

Geprüft wurde `slides/Einführung in Deep Learning 2026 VL 01 Was ist Deep Learning.tex` vor der
ersten Sitzung am 14.10.2026: die Quelle, der gerenderte Kontaktbogen, die Notizenfassung für den
zweiten Schirm, die Zeiten gegen `transcripts/vl01-ueberblick-2025/notiz.md`, die Fakten gegen
Kapitel 01, `kurs-2026-27.md` und die ILIAS-Konfiguration (`../ilias/runs/ws2026-27.yaml`).
Alle Befunde sind **am selben Tag umgesetzt**; die Datei ist Protokoll und Muster für die
übrigen 14 Decks.

**Ausgangslage:** 23 Folien, Bau ohne zu volle Rahmen, Sprachprüfungen null, Termine und
Wochentage richtig, Ablaufplan summiert sich auf 90 Minuten. Die Dramaturgie trägt. Was fehlte,
sah im Bau nicht rot aus.

## A. Was am 14.10. schiefgegangen wäre

| | Befund | Umsetzung |
|---|---|---|
| **A1** | Die Eingangsumfrage schließt laut ILIAS-Konfiguration am 14.10. um 13:55, die Notiz zur letzten Folie sagte „bitte bis morgen“ | Notiz: „schließt um 13:55, also mit dieser Sitzung – jetzt, nicht morgen“. Alternative (Fenster verlängern) steht in `TODO.md` bei den Entscheidungen |
| **A2** | Ablaufplan in der Titelnotiz hatte Folie 7 und 8 vertauscht (Befund A4 vom 25.09., für VL 1 offen) | Zeilen in Deck-Reihenfolge: 23–26 Definition, 26–38 Semesterplan; alle Nummern nach den zwei neuen Folien nachgezogen |
| **A3** | Notizenfassung schnitt die Titelnotiz mitten in „Wenn die Zeit knapp wird“ ab (Befund A5, offen); `Overfull \vbox 34.9pt` | Im Header `\setbeamertemplate{note page}[plain]` und `\scriptsize` – gilt für alle Decks. Nachgebaut: die ganze Titelnotiz steht auf der Seite |

## B. Inhalt und Dramaturgie

| | Befund | Umsetzung |
|---|---|---|
| **B1** | Die Quizfrage (Testset bei Hyperparameterwahl) hatte in keinem Medium eine Antwort: nur in der Notiz; das Kapitel hatte keinen Validation-Split, das Glossar erklärte ihn und verlinkte auf das Kapitel, in dem das Wort nicht vorkam | Neue Folie „Training, Validation, Test“ direkt hinter der Quizfrage, Notiz „erst umblättern, wenn die Pointe gefallen ist“. Im Kapitel ein Absatz „Antwort: …“ hinter der Quizbox, wie in Kapitel 05 |
| **B2** | Keine Take-Home-Folie; die Sitzungsnotiz 2025 hat drei Take-Home-Sätze, VL 5 und VL 7 haben die Folie | Folie „Take-Home“ vor „In die Praxis“ mit den drei Sätzen |
| **B3** | Folie 2 verschwieg, dass die Note allein aus der Klausur kommt und die Klausur ohne Hilfsmittel ist (steht im Vorstellungs-Deck) | Punkt „Note: nur die Klausur, ohne Hilfsmittel“; in der Notiz Studienleistung und Korrektorin |
| **B4** | Folie 21 (2010–2015): drei Bilder bei `0.22\textheight`, keins lesbar (Befund C vom 25.09.), dazu der einzige Overfull auf einer Folie (drei Spalten zu 0.32) | Zwei Spalten: links Jahr, Name, Halbsatz, VL-Nummer; rechts nur die Wortarithmetik (`vl13-word-arithmetic.png`), das einzige der drei Bilder, das bei dieser Größe lesbar ist |
| **B5** | Folie 20 (Mark I): englische Bildunterschrift mit hartem Umbruch nach „system,“ (Waisenzeile), kein Bildnachweis auf der Folie und keiner im Repo; der Commit vom 25.09. sagt nur „aus eidl-23 übernommen“ | Deutsche Unterschrift, Nachweis in `\footnotesize` auf der Folie; Herkunft in `slides/README.md`: Cornell University Library, Digital Collections `ss:550351`. In der Notiz jetzt, was zu sehen ist: Steckbrett in der Mitte, Potentiometer rechts. **Rechtefrage offen**, siehe unten |
| **B6** | „2021 Diffusionsmodelle“: DDPM ist 2020; 2021 ist das Jahr, in dem Diffusion die GANs schlägt. Im Kapitel dieselbe Zeile | Folie „Diffusionsmodelle schlagen GANs“; Notiz und Kapitel nennen DDPM 2020 und Dhariwal/Nichol 2021 |

## C. Kleinkram

* Folie 8 „Vibe-Coding“ → „Vibecoding“ (elfmal so im Repo, so in der Wortliste).
* Folie 5 `\texttt{PyTorch}` → PyTorch; ein Name, kein Code.
* Folie 9 „dynamisch gebunden“ → „dynamisch typisiert“, auch im Kapitel – gemeint ist die
  Typprüfung zur Laufzeit.

## D. Header (alle 16 Decks)

* **`german.sty` → `babel[shorthands=off,ngerman]`.** Das Log jedes Decks sagte
  „`\language number for German undefined, default 255 used`“: `german.sty` sucht
  `\l@german`, das LuaTeX-Format kennt die Sprache nicht, und mit `\language 255` trennt
  nichts. Mit babel lädt LuaTeX die Muster beim ersten Gebrauch aus `hyph-utf8` (Log:
  „German Hyphenation Patterns (Reformed Orthography, 2006)“). **Korrektur zu meiner ersten
  Diagnose:** `dpkg` führt `texlive-lang-german` als entfernt, die Musterdateien liegen aber
  in `texmf-dist/tex/generic/hyph-utf8/` und werden gefunden – nichts nachinstallieren.
  Sichtbar wird der Unterschied auf den Notizseiten (Blocksatz), die Folien selbst sind
  zentriert und kurz.
* `\emph` in der Markenfarbe `#6f59a6` (`BRANDING.md`) statt xcolor-`purple`; das Theme bleibt
  HHU-Blau.
* `pdfsubject={deep learning}` statt „data science“ (Kopie aus dem DS-Deck).

## Gegenprobe nach dem Umbau

| | vorher | nachher |
|---|---|---|
| VL 1 | 23 Folien | 25 Folien (Auflösung, Take-Home) |
| übrige 15 Decks | 7–22 Folien | unverändert |
| zu volle Rahmen (alle Decks) | 0 | 0 |
| Overfull auf Folien, VL 1 | 1 (Folie 21) | 0 |
| Notizenfassung VL 1, Titelnotiz | abgeschnitten, `Overfull \vbox` | vollständig, kein `\vbox` |
| `folienpruefliste.py` | 0 / 0 | 0 / 0 (drei Wörter in die Folienliste: Appetithappen, Dhariwal, Nichol) |
| `sprachpruefliste.py`, Kapitel 01 | 0 Typografie | 0 Typografie, 0 unbekannte Wörter (Dhariwal, Nichol in die Buchliste) |
| `myst build --html` | ohne Warnungen | ohne Warnungen |

Die drei `Overfull \hbox` in Zeile 45 des Logs stammen aus der Ablaufplan-Tabelle in der
Titelnotiz (zu breit für die Notizspalte, Beamer rechnet sie auch ohne Notizenfassung) und
standen schon am 25.09. so da; sie sind auf keiner Folie sichtbar.

## Nicht geändert, aber gesehen

* `slides/build.sh`: die zwei bekannten Lücken (Vorstellungs-Deck nicht im Glob, „up-to-date“
  gilt als `ok`) stehen in `TODO.md` unter „Einstieg“.
* `TODO.md`, Abschnitt „Infrastruktur“, Punkt „Das HHU-Beamer-Theme fehlt auf dieser Maschine“
  ist überholt (Theme seit 2026-09-29 in `~/texmf`, steht im „Einstieg“ derselben Datei).
* **Das Mark-I-Foto liegt im öffentlichen Repo, und seine Rechte sind ungeklärt.** Die englische
  Wikipedia zeigt eine 312 × 384-Fassung desselben Fotos (`File:Mark_I_perceptron.jpeg`) mit
  Quelle Cornell University Library `ss:550351` und führt es als **urheberrechtlich geschützt,
  nur unter Fair Use** benutzt. Unsere Datei hat 1024 × 1352 px, kommt also direkt aus der
  Cornell-Sammlung; deren Katalogseite antwortet einem Skript mit 403, die Rechteangabe dort
  habe ich nicht gesehen. Entscheidung für Konrad (`TODO.md`): Rechteangabe bei Cornell im
  Browser nachsehen und eintragen, oder das Foto aus dem Repo nehmen (gitignored neben
  `transcripts/`) und nur in den Folien verwenden, oder durch das US-Navy-Foto vom Mark I bei
  Wikimedia Commons ersetzen (`330-PSA-80-60 (USN 710739)`, Public Domain als Werk der
  US-Regierung; zeigt Charles Wightman an der Maschine).
