// Perzeptronregel zum Anfassen: Trenngerade w·x + b = 0 ziehen, Punkte färben sich mit;
// „Ein Schritt“ nimmt den nächsten falsch klassifizierten Punkt und zeigt das Update
// w_neu = w + ρ·(y − f(x))·x mit dem Bias-Trick x = (1, x₁, x₂). Ein Klick auf einen Punkt
// tauscht sein Label. Eingebunden im Kapitel „Das Perzeptron trainieren“ über {anywidget};
// im PDF steht statt dessen die Abbildung vl02-perceptron-updates.png. Keine Abhängigkeiten.
//
// Modell (JSON5 im Direktivenrumpf): {w: [w0, w1, w2], rho: 0.05}, w0 ist der Bias.

const NS = "http://www.w3.org/2000/svg";
const XB = [-5, 5]; // sichtbarer Bereich wie in der Abbildung
const YB = [-4, 4];
const S = 50; // Pixel je Einheit (viewBox)
const B = (XB[1] - XB[0]) * S;
const H = (YB[1] - YB[0]) * S;

// Dieselben 60 Punkte wie in der Abbildung, auf zwei Stellen gerundet:
// make_blobs(60, centers=[(-2, -1), (2, 1)], cluster_std=1.0, random_state=3) in
// devnotes/make_figures.py (vl02_perceptron_updates). Mit Start w = (0, -1, 1) und ρ = 0,05
// ergeben drei Epochen dieselben Fehlerraten wie dort (nachgerechnet 2026-11-03).
const DATEN = [[-1.90, -2.86, 0], [0.98, 1.90, 1], [1.80, 2.77, 1], [2.68, 0.14, 1], [0.63, 1.24, 1], [-1.37, -1.16, 0], [-2.80, -3.42, 0], [-2.55, -2.55, 0], [-1.12, 0.71, 0], [1.33, 1.15, 1], [-0.51, -2.12, 0], [1.98, 0.11, 1], [-3.19, -1.21, 0], [-2.04, -1.48, 0], [2.64, 1.25, 1], [-3.24, -1.63, 0], [2.15, -0.06, 1], [1.17, 2.34, 1], [-2.77, -1.23, 0], [1.41, 0.48, 1], [1.58, 1.72, 1], [-0.21, -0.56, 0], [1.31, 1.49, 1], [-2.92, -2.02, 0], [-0.99, -0.15, 0], [-2.87, -0.97, 0], [1.92, 1.56, 1], [-2.28, -1.35, 0], [-3.62, -0.35, 0], [-4.25, -1.27, 0], [-2.08, -1.63, 0], [2.48, 1.68, 1], [3.23, 1.15, 1], [-3.31, -0.12, 0], [-0.88, -1.13, 0], [-1.02, -2.10, 0], [-0.89, 0.12, 0], [1.85, 2.77, 1], [-2.60, -1.59, 0], [-1.25, 0.98, 0], [2.44, 2.94, 1], [-1.15, -2.86, 0], [1.48, 0.81, 1], [2.61, 0.16, 1], [1.47, 0.27, 1], [-2.36, -2.74, 0], [1.43, 0.89, 1], [-0.92, 0.03, 1], [2.87, -0.29, 1], [1.70, 3.16, 1], [0.60, 2.39, 1], [-0.51, -0.76, 0], [-3.02, -1.71, 0], [2.65, 1.31, 1], [3.05, 2.33, 1], [-1.95, -1.40, 0], [2.15, 2.17, 1], [-2.60, -2.91, 0], [1.04, 1.38, 1], [2.85, 1.49, 1]];

const FARBEN = {
  hell: { eins: "#EE7F00", null: "#006AB3", fehler: "#BE0A26", linie: "#BE0A26", grau: "#777777",
    gitter: "#e3e3e3", flaeche: "rgba(238,127,0,0.08)" },
  dunkel: { eins: "#ffa040", null: "#5aa9e6", fehler: "#ff5a6e", linie: "#ff5a6e", grau: "#9a9a9a",
    gitter: "#3a3a3a", flaeche: "rgba(255,160,64,0.10)" },
};

const zahl = (x, stellen = 2) =>
  (Math.abs(x) < 0.5 * 10 ** -stellen ? 0 : x).toLocaleString("de-DE", {
    minimumFractionDigits: stellen,
    maximumFractionDigits: stellen,
  });
const vek = (v, stellen = 2) => `(${v.map((x) => zahl(x, stellen)).join("; ")})`;
const px = (p) => [(p[0] - XB[0]) * S, (YB[1] - p[1]) * S];
const klemme = (p) => [Math.max(XB[0] + 0.1, Math.min(XB[1] - 0.1, p[0])), Math.max(YB[0] + 0.1, Math.min(YB[1] - 0.1, p[1]))];

function el(tag, attrs = {}, parent) {
  const e = document.createElementNS(NS, tag);
  for (const [k, val] of Object.entries(attrs)) e.setAttribute(k, val);
  if (parent) parent.appendChild(e);
  return e;
}

function render({ model, el: wurzel }) {
  const start = [...(model.get("w") ?? [0, -1, 1])];
  let rho = model.get("rho") ?? 0.05;
  const uid = Math.random().toString(36).slice(2, 8);

  // Zustand: w = (w0, w1, w2) mit w0 = b; Anker A liegt auf der Geraden und trägt den Griff
  let w, anker, zeiger, updates, letztes, labels;
  const f = (x) => (w[0] + w[1] * x[0] + w[2] * x[1] > 0 ? 1 : 0);
  const n2 = () => w[1] * w[1] + w[2] * w[2];
  // A auf die Gerade projizieren (nach einem Update liegt sie woanders)
  const projiziereAuf = (ww, a) => {
    const t = (ww[0] + ww[1] * a[0] + ww[2] * a[1]) / (ww[1] * ww[1] + ww[2] * ww[2]);
    return [a[0] - t * ww[1], a[1] - t * ww[2]];
  };
  const projiziere = (a) => projiziereAuf(w, a);
  function zuruecksetzen() {
    w = [...start];
    labels = DATEN.map((d) => d[2]);
    anker = projiziere([0, 0]);
    zeiger = 0;
    updates = 0;
    letztes = null;
  }
  zuruecksetzen();

  const box = document.createElement("div");
  box.className = "perzeptron";
  const stil = document.createElement("style");
  stil.textContent = `
    .perzeptron { font-family: inherit; color: inherit; margin: 1rem 0; }
    .perzeptron svg { width: 100%; height: auto; display: block; touch-action: none; user-select: none; }
    .perzeptron .gitter line { stroke: var(--gitter); stroke-width: 1; }
    .perzeptron .achsen line { stroke: currentColor; stroke-width: 1; opacity: 0.5; }
    .perzeptron .punkt { cursor: pointer; }
    .perzeptron .griff { cursor: grab; }
    .perzeptron .griff:focus { outline: none; }
    .perzeptron .griff circle.ring { fill: transparent; stroke: none; }
    .perzeptron .griff:focus circle.ring { stroke: currentColor; stroke-width: 2; }
    .perzeptron .name { font-size: 17px; font-style: italic; font-weight: 600; }
    .perzeptron .leiste { display: flex; flex-wrap: wrap; gap: 0.5rem; align-items: center; margin-top: 0.6rem; }
    .perzeptron button, .perzeptron select { font: inherit; color: inherit; background: transparent;
      border: 1px solid currentColor; border-radius: 6px; padding: 0.2em 0.7em; cursor: pointer; }
    .perzeptron button:hover { background: rgba(127,127,127,0.15); }
    .perzeptron .stand { font-variant-numeric: tabular-nums; margin-top: 0.5rem; line-height: 1.6; }
    .perzeptron .hinweis { font-size: 0.85em; opacity: 0.75; margin-top: 0.4rem; }
  `;
  box.appendChild(stil);

  const svg = el("svg", { viewBox: `0 0 ${B} ${H}`, role: "group" });
  svg.setAttribute("aria-label", "60 Datenpunkte zweier Klassen und die Trenngerade des Perzeptrons; Gerade und Normalenvektor w lassen sich verschieben");
  box.appendChild(svg);
  const defs = el("defs", {}, svg);
  const clip = el("clipPath", { id: `rahmen-${uid}` }, defs);
  el("rect", { x: 0, y: 0, width: B, height: H }, clip);
  const m = el("marker", { id: `spitze-${uid}`, viewBox: "0 0 10 10", refX: 9, refY: 5,
    markerWidth: 6, markerHeight: 6, orient: "auto-start-reverse" }, defs);
  const spitze = el("path", { d: "M0,0 L10,5 L0,10 z" }, m);
  const m2 = el("marker", { id: `spitze-u-${uid}`, viewBox: "0 0 10 10", refX: 9, refY: 5,
    markerWidth: 6, markerHeight: 6, orient: "auto-start-reverse" }, defs);
  const spitzeU = el("path", { d: "M0,0 L10,5 L0,10 z" }, m2);

  const gitter = el("g", { class: "gitter" }, svg);
  for (let k = XB[0]; k <= XB[1]; k++) { const [a] = px([k, 0]); el("line", { x1: a, y1: 0, x2: a, y2: H }, gitter); }
  for (let k = YB[0]; k <= YB[1]; k++) { const [, b] = px([0, k]); el("line", { x1: 0, y1: b, x2: B, y2: b }, gitter); }
  const achsen = el("g", { class: "achsen" }, svg);
  const o = px([0, 0]);
  el("line", { x1: 0, y1: o[1], x2: B, y2: o[1] }, achsen);
  el("line", { x1: o[0], y1: 0, x2: o[0], y2: H }, achsen);

  const zeichnung = el("g", { "clip-path": `url(#rahmen-${uid})` }, svg);
  const flaeche = el("polygon", {}, zeichnung);
  const alteLinie = el("line", { "stroke-width": 1.5, "stroke-dasharray": "6 4" }, zeichnung);
  const linie = el("line", { "stroke-width": 2.5 }, zeichnung);
  const punkte = el("g", {}, svg);
  const marke = el("circle", { r: 11, fill: "none", "stroke-width": 2.5 }, svg);
  const wPfeil = el("line", { "stroke-width": 2.5, "marker-end": `url(#spitze-${uid})` }, svg);
  const uPfeil = el("line", { "stroke-width": 1.5, "stroke-dasharray": "3 2", "marker-end": `url(#spitze-u-${uid})` }, svg);
  const wName = el("text", { class: "name" }, svg);
  wName.textContent = "w";

  const formen = DATEN.map((d, i) => {
    const [x, y] = px(d);
    const g = el("g", { class: "punkt", transform: `translate(${x},${y})` }, punkte);
    const kreis = el("circle", { r: 5 }, g);
    const quadrat = el("rect", { x: -4.5, y: -4.5, width: 9, height: 9 }, g);
    const fehler = el("circle", { r: 8, fill: "none", "stroke-width": 1.8 }, g);
    const titel = el("title", {}, g);
    g.addEventListener("click", () => {
      labels[i] = 1 - labels[i];
      letztes = null;
      zeichne();
    });
    return { kreis, quadrat, fehler, titel };
  });

  const griff = (beschriftung) => {
    const g = el("g", { class: "griff", tabindex: 0, role: "slider" }, svg);
    g.setAttribute("aria-label", beschriftung);
    el("circle", { r: 16, class: "ring" }, g);
    const sichtbar = el("circle", { r: 6, "stroke-width": 2 }, g);
    return { g, sichtbar };
  };
  const gA = griff("Trenngerade parallel verschieben (Pfeiltasten)");
  const gW = griff("Normalenvektor w drehen und strecken (Pfeiltasten)");

  const leiste = document.createElement("div");
  leiste.className = "leiste";
  const knopf = (text, aktion) => {
    const b = document.createElement("button");
    b.type = "button";
    b.textContent = text;
    b.addEventListener("click", aktion);
    leiste.appendChild(b);
    return b;
  };
  knopf("Ein Schritt", () => { schritt(); zeichne(); });
  knopf("Eine Epoche", () => {
    // ein voller Durchgang ab der aktuellen Stelle, wie in der Abbildung
    for (let k = 0; k < DATEN.length; k++) schritt(true);
    zeichne();
  });
  knopf("Zurücksetzen", () => { zuruecksetzen(); zeichne(); });
  const rhoWahl = document.createElement("label");
  rhoWahl.innerHTML = "Lernrate ρ = ";
  const sel = document.createElement("select");
  for (const r of [0.05, 0.2, 1]) {
    const opt = document.createElement("option");
    opt.value = r;
    opt.textContent = zahl(r);
    if (r === rho) opt.selected = true;
    sel.appendChild(opt);
  }
  sel.addEventListener("change", () => { rho = Number(sel.value); });
  rhoWahl.appendChild(sel);
  leiste.appendChild(rhoWahl);
  box.appendChild(leiste);

  const stand = document.createElement("div");
  stand.className = "stand";
  stand.setAttribute("aria-live", "polite");
  box.appendChild(stand);
  const hinweis = document.createElement("div");
  hinweis.className = "hinweis";
  hinweis.textContent = "Gerade am runden Griff verschieben, w an der Spitze drehen. Ein Klick auf einen Punkt tauscht sein Label. Dreimal „Eine Epoche“ ab dem Start ergibt die Abbildung oben.";
  box.appendChild(hinweis);

  // Ein Schritt der Perzeptronregel. Ohne Epoche: zum nächsten falschen Punkt springen.
  // In der Epoche: genau den nächsten Punkt nehmen, richtig oder falsch.
  function schritt(inEpoche = false) {
    const N = DATEN.length;
    for (let k = 0; k < (inEpoche ? 1 : N); k++) {
      const j = (zeiger + k) % N;
      const x = [DATEN[j][0], DATEN[j][1]];
      const y = labels[j];
      const fx = f(x);
      if (fx === y) {
        if (inEpoche) zeiger = (j + 1) % N;
        continue;
      }
      const alt = [...w];
      const altAnker = anker;
      const faktor = rho * (y - fx);
      w = [w[0] + faktor, w[1] + faktor * x[0], w[2] + faktor * x[1]];
      if (n2() < 1e-9) w = alt; // w = 0 hat keine Gerade
      anker = projiziere(anker);
      zeiger = (j + 1) % N;
      updates++;
      letztes = { j, x, y, fx, alt, altAnker, faktor };
      return;
    }
    if (!inEpoche) letztes = { fertig: true };
  }

  function farben() {
    const fb = FARBEN[document.documentElement.classList.contains("dark") ? "dunkel" : "hell"];
    box.style.setProperty("--gitter", fb.gitter);
    flaeche.setAttribute("fill", fb.flaeche);
    linie.setAttribute("stroke", fb.linie);
    alteLinie.setAttribute("stroke", fb.grau);
    wPfeil.setAttribute("stroke", fb.linie);
    spitze.setAttribute("fill", fb.linie);
    uPfeil.setAttribute("stroke", fb.grau);
    spitzeU.setAttribute("fill", fb.grau);
    wName.setAttribute("fill", fb.linie);
    marke.setAttribute("stroke", "currentColor");
    for (const h of [gA, gW]) {
      h.sichtbar.setAttribute("fill", fb.linie);
      h.sichtbar.setAttribute("stroke", "white");
    }
    return fb;
  }

  // Gerade w0 + w1 x + w2 y = 0 als langes Segment durch den Anker
  function geradeSetzen(linieEl, ww, a) {
    const n = Math.hypot(ww[1], ww[2]);
    const d = [-ww[2] / n, ww[1] / n];
    const p = px([a[0] - 30 * d[0], a[1] - 30 * d[1]]);
    const q = px([a[0] + 30 * d[0], a[1] + 30 * d[1]]);
    linieEl.setAttribute("x1", p[0]); linieEl.setAttribute("y1", p[1]);
    linieEl.setAttribute("x2", q[0]); linieEl.setAttribute("y2", q[1]);
  }

  function zeichne() {
    const fb = farben();
    const n = Math.sqrt(n2());
    const d = [-w[2] / n, w[1] / n];
    const e = [w[1] / n, w[2] / n];
    const ecken = [
      [anker[0] - 30 * d[0], anker[1] - 30 * d[1]],
      [anker[0] + 30 * d[0], anker[1] + 30 * d[1]],
      [anker[0] + 30 * d[0] + 30 * e[0], anker[1] + 30 * d[1] + 30 * e[1]],
      [anker[0] - 30 * d[0] + 30 * e[0], anker[1] - 30 * d[1] + 30 * e[1]],
    ];
    flaeche.setAttribute("points", ecken.map((c) => px(c).join(",")).join(" "));
    geradeSetzen(linie, w, anker);

    let fehler = 0;
    DATEN.forEach((dd, i) => {
      const y = labels[i];
      const falsch = f(dd) !== y;
      if (falsch) fehler++;
      const fo = formen[i];
      fo.kreis.style.display = y === 1 ? "" : "none";
      fo.quadrat.style.display = y === 0 ? "" : "none";
      fo.kreis.setAttribute("fill", fb.eins);
      fo.quadrat.setAttribute("fill", fb.null);
      fo.fehler.setAttribute("stroke", falsch ? fb.fehler : "none");
      fo.titel.textContent = `x = ${vek([dd[0], dd[1]])}, y = ${y}, f(x) = ${f(dd)}${falsch ? ", falsch" : ""} (Klick tauscht das Label)`;
    });

    const pA = px(anker);
    const spitzeW = [anker[0] + w[1], anker[1] + w[2]];
    const pW = px(spitzeW);
    wPfeil.setAttribute("x1", pA[0]); wPfeil.setAttribute("y1", pA[1]);
    wPfeil.setAttribute("x2", pW[0]); wPfeil.setAttribute("y2", pW[1]);
    wName.setAttribute("x", pW[0] + 8); wName.setAttribute("y", pW[1] - 6);
    gA.g.setAttribute("transform", `translate(${pA[0]},${pA[1]})`);
    gW.g.setAttribute("transform", `translate(${pW[0]},${pW[1]})`);
    gW.g.setAttribute("aria-valuetext", `w = ${vek([w[1], w[2]])}`);
    gA.g.setAttribute("aria-valuetext", `b = ${zahl(w[0])}`);

    let text = "";
    if (letztes && !letztes.fertig) {
      const { j, x, y, fx, alt, altAnker, faktor } = letztes;
      const pp = px(x);
      marke.setAttribute("cx", pp[0]); marke.setAttribute("cy", pp[1]);
      marke.style.display = "";
      alteLinie.style.display = "";
      geradeSetzen(alteLinie, alt, altAnker);
      // der Zuwachs ρ(y − f(x))·(x₁, x₂) als Pfeil an der alten Spitze von w
      const altSpitze = [altAnker[0] + alt[1], altAnker[1] + alt[2]];
      const a1 = px(altSpitze);
      const a2 = px([altSpitze[0] + faktor * x[0], altSpitze[1] + faktor * x[1]]);
      uPfeil.setAttribute("x1", a1[0]); uPfeil.setAttribute("y1", a1[1]);
      uPfeil.setAttribute("x2", a2[0]); uPfeil.setAttribute("y2", a2[1]);
      uPfeil.style.display = "";
      text = `Punkt ${j + 1}: <i>x</i> = ${vek(x)}, <i>y</i> = ${y}, <i>f</i>(<i>x</i>) = ${fx}, also<br>
        <i>w</i><sub>neu</sub> = <i>w</i> + ρ·(<i>y</i> − <i>f</i>(<i>x</i>))·(1; <i>x</i><sub>1</sub>; <i>x</i><sub>2</sub>)
        = ${vek(alt)} ${faktor > 0 ? "+" : "−"} ${zahl(Math.abs(faktor))}·(1; ${zahl(x[0])}; ${zahl(x[1])}) = ${vek(w)}<br>`;
    } else {
      marke.style.display = "none";
      alteLinie.style.display = "none";
      uPfeil.style.display = "none";
      if (letztes && letztes.fertig) text = "Kein Punkt ist falsch klassifiziert – die Regel hält an.<br>";
    }
    text += `<i>w</i> = (<i>w</i><sub>0</sub>; <i>w</i><sub>1</sub>; <i>w</i><sub>2</sub>) = ${vek(w)}, `
      + `falsch klassifiziert: ${fehler} von ${DATEN.length} (${zahl((100 * fehler) / DATEN.length, 0)} %), Updates bisher: ${updates}`;
    stand.innerHTML = text;
  }

  // Ziehen: Anker verschiebt die Gerade parallel, die Spitze setzt (w1, w2)
  const punktAus = (ev) => {
    const r = svg.getBoundingClientRect();
    const s = B / r.width;
    return [XB[0] + ((ev.clientX - r.left) * s) / S, YB[1] - ((ev.clientY - r.top) * s) / S];
  };
  const setzeAnker = (p) => {
    anker = klemme(p);
    w[0] = -(w[1] * anker[0] + w[2] * anker[1]);
    letztes = null;
    zeichne();
  };
  const setzeSpitze = (p) => {
    const q = klemme(p);
    const neu = [q[0] - anker[0], q[1] - anker[1]];
    if (Math.hypot(neu[0], neu[1]) < 0.2) return;
    w = [-(neu[0] * anker[0] + neu[1] * anker[1]), neu[0], neu[1]];
    letztes = null;
    zeichne();
  };
  for (const [h, setze, wo] of [[gA, setzeAnker, () => anker], [gW, setzeSpitze, () => [anker[0] + w[1], anker[1] + w[2]]]]) {
    h.g.addEventListener("pointerdown", (ev) => {
      ev.preventDefault();
      h.g.setPointerCapture(ev.pointerId);
      h.g.focus({ preventScroll: true });
      const weiter = (e) => setze(punktAus(e));
      const ende = () => {
        h.g.removeEventListener("pointermove", weiter);
        h.g.removeEventListener("pointerup", ende);
        h.g.removeEventListener("pointercancel", ende);
      };
      h.g.addEventListener("pointermove", weiter);
      h.g.addEventListener("pointerup", ende);
      h.g.addEventListener("pointercancel", ende);
    });
    h.g.addEventListener("keydown", (ev) => {
      const dd = { ArrowLeft: [-0.1, 0], ArrowRight: [0.1, 0], ArrowUp: [0, 0.1], ArrowDown: [0, -0.1] }[ev.key];
      if (!dd) return;
      ev.preventDefault();
      const p = wo();
      setze([p[0] + dd[0], p[1] + dd[1]]);
    });
  }

  const beobachter = new MutationObserver(zeichne);
  beobachter.observe(document.documentElement, { attributes: true, attributeFilter: ["class"] });

  wurzel.appendChild(box);
  zeichne();
  return () => {
    beobachter.disconnect();
    box.remove();
  };
}

export default { render };
