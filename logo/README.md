# Logo

`eidl-logo.svg` – Hauptlogo (Sigmoid über zwei Schichten, 512×512-Viewbox), Quelle für `site_logo.png`
und für Rocket.Chat-Kanal-Icons o.ä. `eidl-logo-512.png` ist der Export davon.

`eidl-logo-small.svg` – vereinfachte Silhouette für kleine Größen (32×32-Viewbox), Quelle für `favicon.ico`
(16/32/48 px).

Neu erzeugen (aus dem Projektverzeichnis):

```bash
inkscape logo/eidl-logo.svg --export-type=png --export-width=512 --export-filename=logo/eidl-logo-512.png
inkscape logo/eidl-logo.svg --export-type=png --export-width=180 --export-filename=site_logo.png
for s in 16 32 48; do inkscape logo/eidl-logo-small.svg --export-type=png --export-width=$s --export-filename=logo/f$s.png; done
magick logo/f16.png logo/f32.png logo/f48.png favicon.ico && rm logo/f*.png
```
