# Mitgeliefertes Site-Template

| | |
|---|---|
| Datei | `book-theme.zip`, 23,5 MB |
| Herkunft | <https://github.com/jupyter-book/myst-theme/releases/download/myst-to-react%402.1.1/book-theme.zip> |
| Abgerufen | 2026-11-27 |
| Paketversion | 2.1.1 (das `package.json` des Archivs nennt keine Fassung, die Release-Marke schon) |
| SHA-256 | `9104dd5eb5f94726cdc46e750dfcaab8332cfe55d40e91ce9db65e25d010128a` |

**Die Quelle ist seit dem 2026-11-17 das Release-Asset, nicht mehr `main.zip`.** An jedem
Release von `jupyter-book/myst-theme` hängt ein fertig gebautes `book-theme.zip`; der
Theme-Code selbst nennt diese Adresse in seiner Fehlermeldung. `main.zip` ist dagegen ein
wandernder Branch, und genau daran hing eine Ungereimtheit: Das Archiv, das hier bis dahin
lag, trug v1.3.1, obwohl am Tag des Abrufs (2026-09-25) seit vier Tagen v1.4.1 auf `main`
stand — vermutlich der Archiv-Cache von codeload, belegen lässt es sich nicht. Eine
versionsfeste Adresse kann das nicht passieren.

Das Archiv von 2.x trägt **keine Wurzelebene**: `renderer/`, `server/`, `public/`,
`template.yml` und `package.json` liegen unmittelbar darin. `install_template.py` kennt
beide Formen und unterscheidet sie an `template.yml` — liegt es im Archiv ganz oben, wird
das Entpackte selbst zum Ziel, sonst die eine Ebene darunter (`dist-book/` in 1.4.x).

**Seit dem 2026-11-27 liegt hier 2.1.1**, und die Patch-Schicht ist dafür gebaut. Was
sich gegenüber 1.4.x geändert hat und wie die Skripte darauf antworten:

| | 1.4.x | 2.x |
|---|---|---|
| Server-Bündel | `build/index.js` | `renderer/server/index.js` |
| Browser-Bündel | `public/build/**/*.js` | `renderer/client/**/*.js` |
| Zeichenketten im Bündel | `"…"` | `` `…` `` — `install_template.tolerant()` läßt beides zu |
| Abbildungen, Karte, PDF | `/build/…` | `/_public/…` — erkannt von `tools/artefakt.py` |
| Stylesheet | `build/_assets/app-*.css` (155 kB) | `_assets/root-*.css` (237 kB, `thebe-core.css` eingebacken) |
| Hydrations-Nutzlast | JSON in `window.__remixContext` | Turbo-Stream — `tools/turbostream.py` |
| Platzhalter-Origin | `http://localhost:3000` | `http://pre.render` — beide in `tools/publish_urls.py` |
| `config.json` im Artefakt | legt das Theme ab | kopiert der `myst-build`-Job dorthin |
| über dem Seitentitel | das `kind` | Brotkrumen (`aria-label="Pfad"`, eingedeutscht) |

`server/server/index.js` von 2.x bleibt unangetastet: Das ist der Express-Teil für
`myst start`, keines unserer Muster kommt darin vor, und `myst build --html` benutzt ihn
nicht. Messwerte, Verlauf und was dabei auffiel: `devnotes/build-log-2026-11-27-theme2x.md`,
die JS-Größen in `devnotes/build-log-2026-11-27-js.md`.

## Warum das hier liegt

`myst build` lädt das Site-Template bei **jedem** Lauf von GitHub nach, und zwar von
`refs/heads/main` — also von einem wandernden Branch. Zwei Folgen:

1. **Das Aussehen der Seite ist eine unversionierte Abhängigkeit.** Jeder Build nimmt,
   was gerade in fremdem `main` steht.
2. **Jeder Netzausfall bricht den Build.** In `eipy-skript` am 2026-09-24/25 dreimal in
   Folge, mit `connect ETIMEDOUT … codeload.github.com`, und der `pages`-Job wurde jedes
   Mal übersprungen.

Ein lokaler Pfad in `myst.yml` löst das nicht: `site.template` wird als Template-*Name*
gegen `api.mystmd.org` aufgelöst, und `file://`-URLs lehnt node-fetch ab (geprüft mit
mystmd 1.10.1). Was funktioniert, ist das Cache-Verzeichnis vorzubelegen — dann lädt
MyST nichts nach. Für das **tex**-Template gilt die Einschränkung nicht; das liegt
deshalb als gewöhnlicher Pfad unter `templates/tex/eidl-skript`.

## Benutzen

```sh
python _site/vendor/install_template.py   # idempotent, braucht kein Netz
myst build --html
```

Die Jobs `myst-build` und `build-pdf` in `.gitlab-ci.yml` rufen das Skript im
`before_script` auf.

## Aktualisieren

```sh
# Die Fassung aus https://github.com/jupyter-book/myst-theme/releases heraussuchen
V=2.1.1
curl -L -o _site/vendor/book-theme.zip \
  "https://github.com/jupyter-book/myst-theme/releases/download/myst-to-react%40$V/book-theme.zip"
sha256sum _site/vendor/book-theme.zip        # in die Tabelle oben eintragen
rm -rf _build/templates/site/myst/book-theme
python _site/vendor/install_template.py && myst build --html
```

Danach die Seite ansehen, bevor committet wird — ein Theme-Update kann das Layout ändern.
