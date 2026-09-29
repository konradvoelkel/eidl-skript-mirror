# Branding – eidlbook

Beschlossen 2026-09-22, gemeinsam mit den anderen fünf Projekten (bubatzkarte,
laberampel, autokorrektur, datasciencebook, eidlbook, eipybook). Die Ledger-Fassung
steht in `~/files/personal/orga/boxes-ledger.html` § Farbsystem.

## Die Farbe dieses Projekts

| Rolle | Wert | OKLCH |
|---|---|---|
| Marke | `#6f59a6` | `oklch(0.52 0.12 295)` |
| Fläche hell (Badges, Hinweise) | `#efebff` | `oklch(0.95 0.03 295)` |
| Akzent im Dunkelmodus | `#b39ef2` | `oklch(0.75 0.12 295)` |

Weiße Schrift auf der Markenfarbe erfüllt WCAG AA (5.8:1). Farbton 295° – violett.

**Warum dieser Farbton:** Das dritte Buch der Reihe, am weitesten von Blau entfernt und trotzdem kühl.

**Für dieses Projekt zu beachten:** HHU-Hausfarben bleiben die Abbildungsfarben (devnotes/make_figures.py, _site/custom-style.css). Achtung: Laberampel lag bisher bei oklch(… 288) und damit fast auf diesem Farbton – deshalb ist Laberampel im System nach Magenta gerückt.

## Die Regel dahinter

Alle sechs Projekte teilen Helligkeit und Buntheit und unterscheiden sich nur im
Farbton. Gearbeitet wird in OKLCH, weil dort gleiche L- und C-Werte auch gleich hell
und gleich bunt *aussehen* – in HSL tun sie das nicht.

- `L = 0.52` ist die Helligkeit, bei der weiße Schrift gerade AA erreicht (4.5:1).
- `C = 0.12` ist so bunt, wie sRGB es bei dieser Helligkeit für *jeden* Farbton kann.
- Die Farbtöne stehen mindestens 40° auseinander; darunter liest sich der Unterschied
  als Fehler statt als Absicht.
- Rot/Gelb/Grün sind in Oberflächen Signalfarben. Wo eine App sie als Signal braucht,
  ist ihre Marke keiner dieser drei Töne.

| Projekt | Farbton | Marke |
|---|---|---|
| bubatzkarte | 150° grün | `#287c42` |
| datasciencebook | 195° petrol | `#007d7e` |
| eipybook | 250° blau | `#286cab` |
| **eidlbook** | 295° violett | `#6f59a6` |
| laberampel | 345° magenta | `#984979` |
| autokorrektur | 55° orange | `#9c5313` |

Varianten werden abgeleitet, nicht erfunden: heller Grund `oklch(0.95 0.03 H)`,
Dunkelmodus-Akzent `oklch(0.75 0.12 H)`, immer derselbe Farbton H.

**Wenn etwas nicht passt:** L oder C für *alle sechs* ändern, nie einen einzelnen
Hexwert nachbessern. Sonst zerfällt das System in sechs Einzelfarben.

`oklch()` ist seit 2023 in allen Browsern nativ; in CSS direkt so schreiben, die
Hexwerte sind nur der Fallback für Android, LaTeX und Bildbearbeitung.
