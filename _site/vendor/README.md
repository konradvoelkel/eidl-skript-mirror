# Mitgeliefertes Site-Template

| | |
|---|---|
| Datei | `book-theme.zip`, 13 MB |
| Herkunft | <https://github.com/myst-templates/book-theme/archive/refs/heads/main.zip> |
| Abgerufen | 2026-09-25 (dasselbe Archiv wie in `eipy-skript`) |
| Paketversion | `@myst-theme/book` 1.3.1 |
| SHA-256 | `9ce315ec6cfe3d96f99f2c2d96e07ee4bd076b896da97178c10e32f883077bea` |

Vor dem Einlegen geprüft: Das Archiv trägt dieselbe Themeversion (1.3.1), die dieses
Repo bis dahin bei jedem Build von GitHub geladen hat — das Aussehen der Seite ändert
sich durch das Mitliefern also nicht.

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
curl -L -o _site/vendor/book-theme.zip \
  https://github.com/myst-templates/book-theme/archive/refs/heads/main.zip
sha256sum _site/vendor/book-theme.zip        # in die Tabelle oben eintragen
rm -rf _build/templates/site/myst/book-theme
python _site/vendor/install_template.py && myst build --html
```

Danach die Seite ansehen, bevor committet wird — ein Theme-Update kann das Layout ändern.
