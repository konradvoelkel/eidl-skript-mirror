// Drehung in der Ebene: v und w frei ziehen, die orthogonale Matrix A legt v auf die
// positive x-Achse. Links das Original, rechts das Bild unter A. Eingebunden im Kapitel
// „Hintergrundwissen Lineare Algebra“ über die Direktive {anywidget}; im PDF steht statt
// dessen die Abbildung la-drehung.png. Keine Abhängigkeiten, kein Netz.
//
// Modell (JSON im Direktivenrumpf): {"v": [x, y], "w": [x, y]}

const NS = "http://www.w3.org/2000/svg";
const R = 3; // sichtbarer Bereich je Achse: [-R, R]
const SIZE = 260; // Pixel je Panel (viewBox), skaliert mit der Breite
const RASTER = 0.1; // Einrasten beim Ziehen und Schrittweite der Pfeiltasten

const FARBEN = {
  hell: { v: "#006AB3", w: "#EE7F00", grau: "#777777", gitter: "#e3e3e3" },
  dunkel: { v: "#5aa9e6", w: "#ffa040", grau: "#9a9a9a", gitter: "#3a3a3a" },
};

const zahl = (x, stellen = 2) =>
  (Math.abs(x) < 0.5 * 10 ** -stellen ? 0 : x).toLocaleString("de-DE", {
    minimumFractionDigits: stellen,
    maximumFractionDigits: stellen,
  });
const norm = (a) => Math.hypot(a[0], a[1]);
const dot = (a, b) => a[0] * b[0] + a[1] * b[1];
const rund = (x) => Math.round(x / RASTER) * RASTER;
const klemme = (x) => Math.max(-R + 0.2, Math.min(R - 0.2, x));

function el(tag, attrs = {}, parent) {
  const e = document.createElementNS(NS, tag);
  for (const [k, val] of Object.entries(attrs)) e.setAttribute(k, val);
  if (parent) parent.appendChild(e);
  return e;
}

// Koordinaten: mathematisch (x nach rechts, y nach oben) zu Pixel im Panel
const px = (p) => [SIZE / 2 + (p[0] * SIZE) / (2 * R), SIZE / 2 - (p[1] * SIZE) / (2 * R)];

function panel(svg, dx, titel) {
  const g = el("g", { transform: `translate(${dx},0)` }, svg);
  const gitter = el("g", { class: "gitter" }, g);
  for (let k = -R; k <= R; k++) {
    const [a] = px([k, 0]);
    const [, b] = px([0, k]);
    el("line", { x1: a, y1: 0, x2: a, y2: SIZE }, gitter);
    el("line", { x1: 0, y1: b, x2: SIZE, y2: b }, gitter);
  }
  const achsen = el("g", { class: "achsen" }, g);
  el("line", { x1: 0, y1: SIZE / 2, x2: SIZE, y2: SIZE / 2 }, achsen);
  el("line", { x1: SIZE / 2, y1: 0, x2: SIZE / 2, y2: SIZE }, achsen);
  const t = el("text", { x: 8, y: 18, class: "titel" }, g);
  t.textContent = titel;
  return g;
}

function pfeil(g, farbe, name, opts = {}) {
  const linie = el("line", { stroke: farbe, "stroke-width": opts.breite ?? 2.5, "marker-end": `url(#${opts.marker})` }, g);
  const text = el("text", { fill: farbe, class: "name" }, g);
  text.textContent = name;
  return {
    setze(p) {
      const [x, y] = px(p);
      linie.setAttribute("x1", SIZE / 2);
      linie.setAttribute("y1", SIZE / 2);
      linie.setAttribute("x2", x);
      linie.setAttribute("y2", y);
      const n = norm(p) || 1;
      // Beschriftung neben die Spitze, aber nie über den Panelrand hinaus
      const tx = x + (12 * p[0]) / n - 6;
      const ty = y - (12 * p[1]) / n + 5;
      const xmax = SIZE - 9 * name.length - 4;
      // am rechten Rand: unter die Spitze statt über sie
      text.setAttribute("x", Math.max(4, Math.min(xmax, tx)));
      text.setAttribute("y", Math.max(16, Math.min(SIZE - 4, tx > xmax ? y + 22 : ty)));
    },
    linie,
    text,
  };
}

function render({ model, el: wurzel }) {
  let v = [...(model.get("v") ?? [2, 1])];
  let w = [...(model.get("w") ?? [-1, 2])];

  const box = document.createElement("div");
  box.className = "drehung";
  const stil = document.createElement("style");
  stil.textContent = `
    .drehung { font-family: inherit; color: inherit; margin: 1rem 0; }
    .drehung svg { width: 100%; height: auto; display: block; touch-action: none; user-select: none; }
    .drehung .gitter line { stroke: var(--gitter); stroke-width: 1; }
    .drehung .achsen line { stroke: currentColor; stroke-width: 1; opacity: 0.6; }
    .drehung .titel { fill: currentColor; font-size: 14px; }
    .drehung .name { font-size: 15px; font-style: italic; font-weight: 600; }
    .drehung .griff { cursor: grab; }
    .drehung .griff:focus { outline: none; }
    .drehung .griff:focus circle.ring { stroke: currentColor; stroke-width: 2; }
    .drehung .griff circle.ring { fill: transparent; stroke: none; }
    .drehung .werte { display: flex; flex-wrap: wrap; gap: 0.5rem 2rem; align-items: center;
      font-variant-numeric: tabular-nums; margin-top: 0.5rem; }
    .drehung .matrix { display: inline-grid; grid-template-columns: auto auto; gap: 0 1em;
      border-left: 1.5px solid currentColor; border-right: 1.5px solid currentColor;
      border-radius: 4px; padding: 0.1em 0.6em; text-align: right; vertical-align: middle; }
    .drehung .hinweis { font-size: 0.85em; opacity: 0.75; margin-top: 0.4rem; }
  `;
  box.appendChild(stil);

  const B = 2 * SIZE + 30;
  const svg = el("svg", { viewBox: `0 0 ${B} ${SIZE}`, role: "group" });
  svg.setAttribute("aria-label", "Zwei Vektoren v und w in der Ebene, links frei verschiebbar, rechts ihr Bild unter der Drehung A");
  box.appendChild(svg);

  const defs = el("defs", {}, svg);
  const uid = Math.random().toString(36).slice(2, 8); // mehrere Widgets auf einer Seite
  const marker = (id) => {
    const m = el("marker", { id: `spitze-${id}-${uid}`, viewBox: "0 0 10 10", refX: 9, refY: 5,
      markerWidth: 7, markerHeight: 7, orient: "auto-start-reverse" }, defs);
    return el("path", { d: "M0,0 L10,5 L0,10 z" }, m);
  };
  const spitzen = { v: marker("v"), w: marker("w"), grau: marker("grau") };

  const links = panel(svg, 0, "v und w");
  const rechts = panel(svg, SIZE + 30, "Av und Aw");

  const bogenL = el("path", { fill: "none", "stroke-width": 1.5 }, links);
  const bogenR = el("path", { fill: "none", "stroke-width": 1.5 }, rechts);
  const schattenV = pfeil(rechts, "", "", { marker: `spitze-grau-${uid}`, breite: 1.2 });
  const schattenW = pfeil(rechts, "", "", { marker: `spitze-grau-${uid}`, breite: 1.2 });
  const drehbogen = el("path", { fill: "none", "stroke-width": 1, "stroke-dasharray": "4 3" }, rechts);
  const pv = pfeil(links, "", "v", { marker: `spitze-v-${uid}` });
  const pw = pfeil(links, "", "w", { marker: `spitze-w-${uid}` });
  const pAv = pfeil(rechts, "", "Av", { marker: `spitze-v-${uid}` });
  const pAw = pfeil(rechts, "", "Aw", { marker: `spitze-w-${uid}` });

  // Griffe: große, unsichtbare Kreise an den Pfeilspitzen, fokussierbar für die Tastatur
  const griff = (name) => {
    const g = el("g", { class: "griff", tabindex: 0, role: "slider" }, links);
    g.setAttribute("aria-label", `Vektor ${name} verschieben (Pfeiltasten)`);
    el("circle", { r: 16, class: "ring" }, g);
    return g;
  };
  const gv = griff("v");
  const gw = griff("w");

  const werte = document.createElement("div");
  werte.className = "werte";
  werte.setAttribute("aria-live", "polite");
  box.appendChild(werte);
  const hinweis = document.createElement("div");
  hinweis.className = "hinweis";
  hinweis.textContent = "Die Pfeilspitzen von v und w lassen sich ziehen, nach Anklicken auch mit den Pfeiltasten verschieben.";
  box.appendChild(hinweis);

  // Bogen um den Ursprung von Richtung a nach Richtung b (kürzerer Weg)
  const bogen = (a, b, r) => {
    const wa = Math.atan2(a[1], a[0]);
    let d = Math.atan2(b[1], b[0]) - wa;
    d = Math.atan2(Math.sin(d), Math.cos(d));
    const p0 = px([r * Math.cos(wa), r * Math.sin(wa)]);
    const p1 = px([r * Math.cos(wa + d), r * Math.sin(wa + d)]);
    const rp = (r * SIZE) / (2 * R);
    return `M${p0[0]},${p0[1]} A${rp},${rp} 0 0 ${d > 0 ? 0 : 1} ${p1[0]},${p1[1]}`;
  };

  function farben() {
    const dunkel = document.documentElement.classList.contains("dark");
    const f = FARBEN[dunkel ? "dunkel" : "hell"];
    box.style.setProperty("--gitter", f.gitter);
    for (const [p, c] of [[pv, f.v], [pAv, f.v], [pw, f.w], [pAw, f.w], [schattenV, f.grau], [schattenW, f.grau]]) {
      p.linie.setAttribute("stroke", c);
      p.text.setAttribute("fill", c);
    }
    spitzen.v.setAttribute("fill", f.v);
    spitzen.w.setAttribute("fill", f.w);
    spitzen.grau.setAttribute("fill", f.grau);
    schattenV.linie.setAttribute("opacity", 0.35);
    schattenW.linie.setAttribute("opacity", 0.35);
    for (const b of [bogenL, bogenR, drehbogen]) b.setAttribute("stroke", f.grau);
  }

  function zeichne() {
    const n = norm(v);
    // A = (1/‖v‖) [[v1, v2], [-v2, v1]]: dreht v auf die positive x-Achse
    const A = [[v[0] / n, v[1] / n], [-v[1] / n, v[0] / n]];
    const mal = (p) => [A[0][0] * p[0] + A[0][1] * p[1], A[1][0] * p[0] + A[1][1] * p[1]];
    const Av = mal(v);
    const Aw = mal(w);

    pv.setze(v);
    pw.setze(w);
    pAv.setze(Av);
    pAw.setze(Aw);
    schattenV.setze(v);
    schattenW.setze(w);
    for (const [g, p] of [[gv, v], [gw, w]]) {
      const [x, y] = px(p);
      g.setAttribute("transform", `translate(${x},${y})`);
      g.setAttribute("aria-valuetext", `(${zahl(p[0], 1)}; ${zahl(p[1], 1)})`);
    }
    bogenL.setAttribute("d", bogen(v, w, 0.6));
    bogenR.setAttribute("d", bogen(Av, Aw, 0.6));
    drehbogen.setAttribute("d", bogen(v, Av, Math.min(n, 2.6) * 0.75));

    const winkel = (Math.acos(Math.max(-1, Math.min(1, dot(v, w) / (n * norm(w))))) * 180) / Math.PI;
    werte.innerHTML = `
      <span><i>A</i> = <span class="matrix">
        <span>${zahl(A[0][0])}</span><span>${zahl(A[0][1])}</span>
        <span>${zahl(A[1][0])}</span><span>${zahl(A[1][1])}</span></span></span>
      <span><i>v</i> = (${zahl(v[0], 1)}; ${zahl(v[1], 1)}), <i>Av</i> = (${zahl(Av[0])}; ${zahl(Av[1])})<br>
        <i>w</i> = (${zahl(w[0], 1)}; ${zahl(w[1], 1)}), <i>Aw</i> = (${zahl(Aw[0])}; ${zahl(Aw[1])})</span>
      <span><i>v</i>·<i>w</i> = ${zahl(dot(v, w))} = (<i>Av</i>)·(<i>Aw</i>) = ${zahl(dot(Av, Aw))}<br>
        Winkel θ = ${zahl(winkel, 1)}°</span>`;
  }

  // Ziehen mit Maus, Stift oder Finger
  const punkt = (ev) => {
    const r = svg.getBoundingClientRect();
    const s = (2 * SIZE + 30) / r.width;
    const x = (ev.clientX - r.left) * s;
    const y = (ev.clientY - r.top) * s;
    return [((x - SIZE / 2) * 2 * R) / SIZE, ((SIZE / 2 - y) * 2 * R) / SIZE];
  };
  const setze = (welcher, p) => {
    const q = [klemme(rund(p[0])), klemme(rund(p[1]))];
    if (norm(q) < 0.25) return; // v = 0 hat keine Richtung
    if (welcher === "v") v = q;
    else w = q;
    zeichne();
  };
  for (const [g, welcher] of [[gv, "v"], [gw, "w"]]) {
    g.addEventListener("pointerdown", (ev) => {
      ev.preventDefault();
      g.setPointerCapture(ev.pointerId);
      g.focus();
      const weiter = (e) => setze(welcher, punkt(e));
      const ende = () => {
        g.removeEventListener("pointermove", weiter);
        g.removeEventListener("pointerup", ende);
        g.removeEventListener("pointercancel", ende);
      };
      g.addEventListener("pointermove", weiter);
      g.addEventListener("pointerup", ende);
      g.addEventListener("pointercancel", ende);
    });
    g.addEventListener("keydown", (ev) => {
      const schritt = { ArrowLeft: [-1, 0], ArrowRight: [1, 0], ArrowUp: [0, 1], ArrowDown: [0, -1] }[ev.key];
      if (!schritt) return;
      ev.preventDefault();
      const p = welcher === "v" ? v : w;
      setze(welcher, [p[0] + schritt[0] * RASTER, p[1] + schritt[1] * RASTER]);
    });
  }

  const beobachter = new MutationObserver(farben);
  beobachter.observe(document.documentElement, { attributes: true, attributeFilter: ["class"] });

  wurzel.appendChild(box);
  farben();
  zeichne();
  return () => {
    beobachter.disconnect();
    box.remove();
  };
}

export default { render };
