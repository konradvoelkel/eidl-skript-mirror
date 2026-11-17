# Mitgeliefertes Site-Template

| | |
|---|---|
| Datei | `book-theme.zip`, 12,7 MB |
| Herkunft | <https://github.com/jupyter-book/myst-theme/releases/download/myst-to-react%401.4.1/book-theme.zip> |
| Abgerufen | 2026-11-17 |
| Paketversion | `@myst-theme/book` 1.4.1 |
| SHA-256 | `f6b6c7822821539e80dde120f6632ad77e7b6c20f5e773b5ca5d818ea529bd78` |

**Die Quelle ist seit dem 2026-11-17 das Release-Asset, nicht mehr `main.zip`.** An jedem
Release von `jupyter-book/myst-theme` hängt ein fertig gebautes `book-theme.zip`; der
Theme-Code selbst nennt diese Adresse in seiner Fehlermeldung. `main.zip` ist dagegen ein
wandernder Branch, und genau daran hing eine Ungereimtheit: Das Archiv, das hier bis dahin
lag, trug v1.3.1, obwohl am Tag des Abrufs (2026-09-25) seit vier Tagen v1.4.1 auf `main`
stand — vermutlich der Archiv-Cache von codeload, belegen lässt es sich nicht. Eine
versionsfeste Adresse kann das nicht passieren.

Das Archiv trägt eine Wurzelebene (`dist-book/` statt wie früher `book-theme-main/`);
`install_template.py` benennt die eine Ebene um und ist von dem Namen unabhängig.

**Nicht auf 2.x gehen, ohne die Patch-Schicht neu zu bauen.** Theme 2.0.0 (2026-11-10) ist
ein erklärter Bruch — React Router 8, eigener Pre-Renderer —, und das Dateilayout ändert
sich vollständig: zwei Serverbündel (`renderer/server/index.js` und
`server/server/index.js`) statt `build/index.js`, Vite-`_assets`-Chunks statt
`public/build/_shared`, `thebe-core.css` in das Hauptstylesheet eingebacken (237 kB, also
kein `<link>` mehr, den `tools/dead_css.py` herausnehmen könnte), geänderte
`build:`-Kommandos. Jeder der 38 Anker in `install_template.py` müsste neu gesetzt werden,
und `tools/dead_css.py` und `tools/thebe_gate.py` bräuchten einen anderen Ansatz.

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
V=1.4.1
curl -L -o _site/vendor/book-theme.zip \
  "https://github.com/jupyter-book/myst-theme/releases/download/myst-to-react%40$V/book-theme.zip"
sha256sum _site/vendor/book-theme.zip        # in die Tabelle oben eintragen
rm -rf _build/templates/site/myst/book-theme
python _site/vendor/install_template.py && myst build --html
```

Danach die Seite ansehen, bevor committet wird — ein Theme-Update kann das Layout ändern.
