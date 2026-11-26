# Prüfung der Auslieferung, 2026-11-26

Kein vierter Audit, sondern eine Gegenprobe: Greifen die Änderungen vom 2026-11-17 und
2026-11-22 auf der veröffentlichten Seite, und sind die offenen Punkte aus
`seo-audit-2026-11-18.md` noch offen? Gemessen wurde an
`https://eidl-skript-131e30.pages.cs.uni-duesseldorf.de`, teils mit `curl` an der
ausgelieferten Datei, teils im Browser nach der Hydration.

## 1. Was nachweislich greift

**Der Hydrations-Wächter hält.** Nach 2,5 Sekunden im Browser stehen auf
`/autoencoder/` noch: `<title>`, `meta[name=description]`, `link[rel=canonical]` auf die
eigene Adresse, 10 `og:`-Tags, 2 `twitter:`-Tags, `<style id="bildmasse">` und der
JSON-LD-Block. Nichts davon hat React beim Übernehmen weggeräumt. Der Wächter selbst steht
im ausgelieferten Kopf und führt `script[type="application/ld+json"]`,
`style[id="bildmasse"]` und `style[id="gliederungsplatz"]` in seiner Liste.

**Das JSON-LD ist inhaltlich da, nicht nur syntaktisch.** Geparst statt gegrept:

| Seite | `@graph` | Typen |
|---|---|---|
| Startseite | 3 | `Book`+`LearningResource` (mit `about`: fünf `Thing`), dazu die beiden Schwesterbücher |
| Kapitel | 2 | `Chapter`+`LearningResource` mit `isPartOf`, `BreadcrumbList` |
| Glossar | 3 | zusätzlich `DefinedTermSet` mit **69** `DefinedTerm` |

**WebP wird wirklich ausgeliefert.** Im Netzwerkprotokoll der Autoencoder-Seite steht keine
einzige PNG- oder JPEG-Anfrage; alle acht Bilder sind WebP, sechs der sieben Abbildungen
tragen `loading="lazy"`, die erste bleibt eager. Die `<picture>`-Elemente überleben die
Hydration samt `srcset` mit `1x`/`2x`.

**Die Markdown-Auslieferung steht.** `/autoencoder/index.md` antwortet 200 mit
`text/markdown; charset=utf-8`, 18.922 Bytes, und die Bildadressen darin sind absolut. Sie
zeigen auf die PNG-Fassungen, nicht auf die WebP — für einen Abnehmer, der die Datei ohne
Browser liest, ist das die robustere Wahl.

## 2. Was offen war — und was am 2026-11-27 daraus wurde

**Die `302` ist eine `302`.** Nachgemessen an `/perzeptron-trainieren` und `/autoencoder`
ohne Schrägstrich: beide `302`, Ziel jeweils die Adresse mit Schrägstrich. Der Stand aus
`seo-audit-2026-11-18.md` §18.1 gilt also weiter, einschließlich der am 2026-11-22
nachgelesenen Aussicht.

*Ausprobiert am 2026-11-27, und damit beantwortet: nein.* Die eine Frage, die ohne Server
nicht zu klären war, lautete: Greift eine eigene Regel vor der eingebauten Weiterleitung?
Ein `tools/redirects.py` hat dafür ein `_redirects` mit 32 Zeilen der Form
`/autoencoder /autoencoder/ 301` ins Artefakt gelegt. Nach dem Deploy:

| gemessen | Ergebnis |
|---|---|
| `/_redirects` | `200` — und zwar nicht die Datei, sondern GitLabs eigener Prüfbericht: „32 rules / rule 1: valid / rule 2: valid …“ |
| `/autoencoder`, `/perzeptron-trainieren`, `/faltung-cnn` | weiterhin `302` |

Das ist mehr als ein stummes Scheitern: GitLab **liest** die Datei und hält jede der 32
Regeln für gültig — und leitet trotzdem temporär weiter. Die eingebaute Auflösung
mehrdeutiger Adressen geht also vor, und `_redirects` kann daran nichts ändern. Damit ist
an dieser Stelle nichts mehr zu machen, solange gitlab-org/gitlab#565802 offen ist; das
Skript ist wieder draußen, der CI-Schritt und die Zeile in der Werkzeugtabelle ebenfalls.
Was bleibt, ist `trailing_slash.py`, das dafür sorgt, daß wenigstens kein interner Link in
die Weiterleitung läuft.

**Die `prf`-Kästen haben weiterhin keine Rolle.** Auf der Seite zur linearen Algebra, der
mit den meisten davon, stehen 18 `div.myst-proof-body`, 18 `myst-proof-header` — und null
`role`, null `aria-labelledby`. Die vier `role="note"` der Seite gehören zu den gewöhnlichen
Hinweiskästen.

*Erledigt am 2026-11-27.* Sie bekommen jetzt `role="group"` mit `aria-labelledby` auf die
Kopfzeile. Warum das bis hierher liegengeblieben ist, stellte sich beim Hinsehen heraus: Die
Kopfzeile hat keine `id` — und der `identifier` des Kastens, aus dem man eine bauen würde,
ist bei **allen 48** leer (nachgezählt: null `myst-proof`-Kästen mit `id` im ganzen Buch).
Der Name muss also aus etwas kommen, das wirklich da ist, und das sind `kind` und
`enumerator`: `prf-<kind>-<enumerator>-titel`, je Seite eindeutig, weil alle 48 Köpfe eine
Nummer tragen und kein Kopf zweimal auf derselben Seite steht.

Dafür waren zwei Eingriffe in `_site/vendor/install_template.py` nötig, weil die beiden
Stellen im Bündel verschiedene Variablen sehen: Der Container kennt nur `id`, `className`
und `children` und reicht jetzt unbekannte Props durch; die Renderstelle kennt `kind` und
`enumerator` und setzt damit Rolle, Beschriftung und die `id` der Kopfzeile. Beide Regeln
greifen im Server- wie in den Browser-Bündeln gleich oft, die gepatchten Bündel bestehen
`node --check`, und ein zweiter Lauf des Skripts ändert nichts mehr.

*Nachgemessen nach Pipeline #186611, im Browser und nach der Hydration:* 18 Elemente mit
`role="group"` auf der Seite zur linearen Algebra, 18 `aria-labelledby`, **kein einziger
toter Verweis**. Die Namen, die ein Screenreader daraus vorliest, sind „Definition 1
(Vektor)“, „Definition 2 (Hadamard-Produkt)“, „Beispiel 1 (Skalarprodukt)“ — also genau die
Kopfzeile. Auf der Analysis-Seite sind es 13, bei der logistischen Regression 4.

Nebenbei fiel auf, daß der Kommentar im Skript die beiden `{id:…}`-Kästen falsch benannte:
Es sind nicht „die zwei prf-Fassungen", sondern der prf-Kasten und der Exercise-Kasten. Die
Rolle bekommt nur der prf-Kasten, weil nur dessen Renderstelle die Props mitgibt.

## 3. Neu gefunden: Preload und `srcset` widersprechen sich

Der Browser lädt die **erste Abbildung jeder Kapitelseite zweimal**.

`tools/head_meta.py` entfernt die Bild-Preloads der lazy gewordenen Abbildungen und
**behält** bewußt eines: das der ersten Abbildung, weil sie das LCP-Element ist (die
Begründung steht im Kopf des Skripts). `tools/webp.py` läuft danach (`.gitlab-ci.yml`:
`head_meta` Zeile 384, `image_dims` 419, `webp` 446) und macht aus derselben Abbildung ein
`<picture>` mit `srcset="…@1x.webp 1x, ….webp 2x"`. Das Preload weiß davon nichts: Es nennt
weiter die große Datei und trägt kein `imagesrcset`. Ergebnis auf einem Bildschirm mit
Pixelverhältnis 1:

1. Der Vorab-Scanner holt wegen des Preloads die **2x**-Datei.
2. Nach dem Layout wertet der Browser das `<picture>` aus und holt die **1x**-Datei.

Beobachtet auf `/autoencoder/`: `vl06-autoencoder-sch-….webp` (47.688 B) und danach
`vl06-autoencoder-sch-…@1x.webp` (19.436 B) — 67.124 B statt 19.436 B, und das Preload, das
das LCP beschleunigen soll, holt eine Datei, die die Seite nicht anzeigt.

Betroffen sind **19 der 33 Seiten** der Sitemap, nämlich alle, deren erste Abbildung breit
genug für eine zweite Fassung ist:

| Seite | 2x (vergeudet) | 1x (gebraucht) |
|---|---|---|
| `faltung-cnn` | 92.644 B | 28.588 B |
| `was-ist-deep-learning` | 54.196 B | 26.330 B |
| `autoencoder` | 47.688 B | 19.436 B |
| `perzeptron-trainieren` | 40.782 B | 24.270 B |
| `logistische-regression` | 40.180 B | 26.318 B |
| `variational-autoencoder` | 38.242 B | 16.924 B |
| `adversarial-attacks-polysemie` | 32.608 B | 19.486 B |
| `netze-von-hand` | 27.834 B | 13.038 B |
| `word2vec` | 25.682 B | 13.608 B |
| `universelle-approximation` | 25.428 B | 11.892 B |
| `gradientenabstieg` | 25.426 B | 13.626 B |
| `aktivierungsfunktionen` | 22.844 B | 13.676 B |
| `rnn` | 16.762 B | 8.918 B |
| `neuron-perzeptron` | 16.124 B | 7.444 B |
| `gans` | 15.950 B | 7.592 B |
| `latente-raeume-geometrisch` | 13.890 B | 8.992 B |
| `representation-learning-graphen` | 12.644 B | 7.300 B |
| `backpropagation` | 7.930 B | 3.624 B |
| `autograd-berechnungsgraph` | 6.132 B | 8.282 B |
| **Summe** | **562.986 B** | **279.344 B** |

Über alle Seiten gerechnet sind das 563 kB, die niemand anzeigt. Pro Seitenaufruf trifft es
den Leser einmal, und zwar genau an der Stelle, die die Ladezeit bestimmt. Die letzte Zeile
ist die Ausnahme, die die Regel zeigt: Dort ist die 2x-Datei kleiner als die 1x-Datei, das
Preload schadet also nicht — ein Hinweis, daß die Skalierung dieser einen Abbildung nicht
aufgeht.

`hintergrundwissen-lineare-algebra` hat vier `<picture>`, ist aber nicht betroffen: Die
erste Abbildung dort ist zu schmal für eine zweite Fassung.

**Behoben am selben Tag.** `tools/webp.py` hat eine Funktion `preload_srcset` bekommen:
Wo eine Abbildung ein `<picture>` mit zwei Größen bekommt, trägt das zugehörige
`<link rel="preload" as="image">` jetzt `imagesrcset` mit demselben Wert wie das
`<source>`. Das `href` bleibt daneben stehen — Browser vor Safari 17.2 und Firefox 115
kennen `imagesrcset` nicht und sollen weiter etwas vorladen. Ein `imagesizes` braucht es
nicht, die Deskriptoren sind `1x`/`2x` und nicht `w`.

Gegen die 32 heute geholten Seiten gerechnet: Die Funktion faßt genau 19 Preloads an, das
Logo bleibt unberührt, ein zweiter Lauf ändert nichts mehr, und die `<picture>` bleiben
Zeichen für Zeichen gleich. `webp.py --check` hat dieselbe Prüfung bekommen und meldete
vor der Änderung 19 Beanstandungen und danach keine — dieselbe Zahl, die die Messung oben
unabhängig ergeben hat.

**Woran man merkt, daß es nicht gewirkt hat:** Im Netzwerkprotokoll einer Kapitelseite
stehen nach dem Deploy immer noch zwei Anfragen auf denselben Bildnamen, eine mit und eine
ohne `@1x`. Im `pages`-Job schlägt `webp.py --check` dann schon vorher an.

**Nachgemessen am 2026-11-27, nach Pipeline #186609.** Alle 32 Seiten der Sitemap noch
einmal geholt: 19 Bild-Preloads tragen jetzt `imagesrcset`, keiner zeigt mehr ohne auf eine
Datei, die daneben als 2x angeboten wird. Im Browser, frischer Tab, Pixelverhältnis 1, auf
der Seite zur Faltung — der vorher schlimmsten mit 92,6 kB: **zwei** WebP-Anfragen, das
Logo und `vl10-blur-edges-…@1x.webp`. Die 2x-Datei wird nicht mehr geholt.
