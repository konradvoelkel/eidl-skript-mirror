#!/usr/bin/env python3
"""Die Verteilung „Dreiecke gegen Quadrate“: Ziehen und Rendern, **ohne torch**.

Zwei Klassen, 32x32 Graustufen. Gezogen werden nicht Pixel, sondern die erzeugenden
Größen (Drehung, Fläche, beim Dreieck drei Bögen auf dem Umkreis); gerendert wird über
die vorzeichenbehaftete Distanzfunktion des Polygons.

**Warum ein eigenes Modul?** Zwei Skripte brauchen dieselbe Verteilung, und zwar in
verschiedenen Abhängigkeitsgruppen:

* `make_formen_daten.py` trainiert damit Netze und braucht torch (Default-Gruppe),
* `make_figures.py` zeichnet damit die Beispielbilder und läuft mit
  `--only-group figures`, in der **kein** torch steckt (siehe `../CLAUDE.md`).

Deshalb steht hier nur NumPy. Wer etwas an der Verteilung ändert, ändert damit die
Abbildung `vl10-formen-beispiele` *und* die Messung in
`formen-stichprobengroesse.json` -- beide neu erzeugen.

Die Klassenbezeichnung ist `0 = Dreieck`, `1 = Quadrat`.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

DREIECK, QUADRAT = 0, 1


@dataclass(frozen=True)
class ShapeConfig:
    """Alles, was die Verteilung festlegt."""

    size: int = 32
    # Fläche in px^2, gleichverteilt und für beide Klassen identisch.
    area_min: float = 60.0
    area_max: float = 220.0
    # Kleinster Innenwinkel des Dreiecks; ohne diese Schranke entstehen Splitter, die wie
    # ein Strich aussehen und keine erkennbare Klasse mehr haben.
    min_angle_deg: float = 28.0
    stroke_min: float = 0.8
    stroke_max: float = 2.2
    p_filled: float = 0.5
    bg_max: float = 0.25
    min_contrast: float = 0.35
    margin: float = 1.0


def _ccw(poly: np.ndarray) -> np.ndarray:
    """Ecken gegen den Uhrzeigersinn ordnen (Vorzeichen der Fläche)."""
    x, y = poly[..., 0], poly[..., 1]
    a2 = np.sum(x * np.roll(y, -1, axis=-1) - np.roll(x, -1, axis=-1) * y, axis=-1)
    out = poly.copy()
    out[a2 < 0] = out[a2 < 0, ::-1]
    return out


def _skaliere_auf_flaeche(poly: np.ndarray, ziel: np.ndarray) -> np.ndarray:
    x, y = poly[..., 0], poly[..., 1]
    a = 0.5 * np.abs(np.sum(x * np.roll(y, -1, -1) - np.roll(x, -1, -1) * y, axis=-1))
    return poly * (np.sqrt(ziel / a))[:, None, None]


def sample_polygone(cfg: ShapeConfig, rng: np.random.Generator, n: int, klasse: int):
    """Ecken (n, k, 2), auf den Schwerpunkt zentriert, mit der gewünschten Fläche.

    Gezogen werden die **Parameter**, nicht Eckpunkte: Drehung gleichverteilt, Fläche
    gleichverteilt. Zwei gleichverteilte Punkte im Bild ergäben keine gleichverteilte
    Kantenrichtung, und so kennen wir zu jedem Bild die erzeugenden Größen exakt.
    """
    flaeche = rng.uniform(cfg.area_min, cfg.area_max, size=n)
    phi = rng.uniform(0, 2 * np.pi, size=n)

    if klasse == QUADRAT:
        winkel = phi[:, None] + np.arange(4) * (np.pi / 2) + np.pi / 4
        r = np.sqrt(flaeche / 2.0)[:, None]      # Umkreisradius des Quadrats, s/sqrt(2)
    else:
        # Jedes Dreieck liegt auf seinem Umkreis, ist also durch drei Bögen bestimmt, die
        # sich zu 360 Grad addieren. Der Innenwinkel an einer Ecke ist der halbe
        # gegenüberliegende Bogen; `min_angle_deg` wird damit zu einer Mindestbogenlänge.
        bmin = 2 * cfg.min_angle_deg
        boegen = np.deg2rad(bmin + (360.0 - 3 * bmin) * rng.dirichlet(np.ones(3), size=n))
        winkel = phi[:, None] + np.cumsum(boegen, axis=1)
        r = np.ones((n, 1))

    poly = np.stack([r * np.cos(winkel), r * np.sin(winkel)], axis=-1)
    poly = _skaliere_auf_flaeche(poly, flaeche)
    return _ccw(poly - poly.mean(axis=1, keepdims=True)), flaeche


def _sdf(poly: np.ndarray, grid: np.ndarray) -> np.ndarray:
    """Vorzeichenbehaftete Distanz zum Polygon, (B, G). Negativ innen, nur für konvexe."""
    a, b = poly, np.roll(poly, -1, axis=1)
    e = b - a                                              # (B, k, 2)
    w = grid[None, None, :, :] - a[:, :, None, :]          # (B, k, G, 2)
    t = np.clip(np.sum(w * e[:, :, None, :], -1) / np.sum(e * e, -1)[:, :, None], 0.0, 1.0)
    dist = np.linalg.norm(w - t[..., None] * e[:, :, None, :], axis=-1).min(axis=1)
    # Konvex und gegen den Uhrzeigersinn: innen genau dann, wenn alle Kreuzprodukte >= 0.
    cross = e[:, :, None, 0] * w[..., 1] - e[:, :, None, 1] * w[..., 0]
    return np.where(np.all(cross >= 0.0, axis=1), -dist, dist)


def sample_batch(cfg: ShapeConfig, rng: np.random.Generator, n: int):
    """n Bilder mit Labels, Klassen 50:50, in zufälliger Reihenfolge.

    Gerendert wird über die vorzeichenbehaftete Distanzfunktion: Antialiasing, Füllung
    und Strich fallen aus einer Rechnung ab, und die Strichstärke ist eine Zahl in Pixeln
    statt einer Rasterheuristik.
    """
    koord = np.arange(cfg.size) + 0.5
    gx, gy = np.meshgrid(koord, koord)
    grid = np.stack([gx.ravel(), gy.ravel()], axis=-1)

    bilder, labels = [], []
    for klasse, m in ((DREIECK, n // 2), (QUADRAT, n - n // 2)):
        if m == 0:
            continue
        poly, _ = sample_polygone(cfg, rng, m, klasse)

        # Position gleichverteilt über alle Lagen, in denen die Form ganz im Bild liegt.
        # Was nirgends hineinpasst, wird neu gezogen (bei dieser Konfiguration 4,4 % der
        # Dreiecke und kein Quadrat).
        def grenzen(p):
            return cfg.margin - p.min(axis=1), cfg.size - cfg.margin - p.max(axis=1)

        lo, hi = grenzen(poly)
        passt = np.all(hi > lo, axis=1)
        while not passt.all():
            poly[~passt], _ = sample_polygone(cfg, rng, int((~passt).sum()), klasse)
            lo, hi = grenzen(poly)
            passt = np.all(hi > lo, axis=1)
        zentrum = lo + rng.random((m, 2)) * (hi - lo)

        strich = rng.uniform(cfg.stroke_min, cfg.stroke_max, size=m)
        gefuellt = rng.random(m) < cfg.p_filled
        c_bg = rng.uniform(0.0, cfg.bg_max, size=m)
        # Die Hälfte invertiert: heller Grund, dunkle Form. Das Netz darf sich nicht auf
        # die Polarität verlassen.
        c_bg = np.where(rng.random(m) < 0.5, 1.0 - c_bg, c_bg)
        delta = cfg.min_contrast + rng.random(m) * (1.0 - cfg.min_contrast) * 0.9
        c_stroke = np.where(c_bg > 0.5, c_bg - delta, c_bg + delta)
        c_fill = c_bg + (c_stroke - c_bg) * rng.uniform(0.35, 1.0, size=m)

        sdf = _sdf(poly + zentrum[:, None, :], grid)
        innen = np.clip(0.5 - sdf, 0.0, 1.0)
        band = np.clip(0.5 - (np.abs(sdf) - strich[:, None] / 2.0), 0.0, 1.0)
        fuell = np.where(gefuellt[:, None], c_fill[:, None], c_bg[:, None])
        img = c_bg[:, None] * (1 - innen) + fuell * innen
        img = img * (1 - band) + c_stroke[:, None] * band

        bilder.append(np.clip(img, 0, 1).reshape(-1, cfg.size, cfg.size).astype(np.float32))
        labels.append(np.full(m, klasse, dtype=np.int64))

    x, y = np.concatenate(bilder), np.concatenate(labels)
    perm = rng.permutation(len(y))
    return x[perm], y[perm]


def shape_stream(cfg: ShapeConfig, seed: int, chunk: int = 256):
    """Unendlicher Generator einzelner Beispiele.

    Hier ist eine Koroutine das Naheliegende: Die Verteilung hat kein Ende, also gibt es
    keine Liste und kein `len`. Gezogen wird in Blöcken (NumPy mag Vektoren),
    herausgegeben einzeln.
    """
    rng = np.random.default_rng(seed)
    while True:
        x, y = sample_batch(cfg, rng, chunk)
        yield from zip(x, y)
