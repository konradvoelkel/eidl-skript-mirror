// Gradientenabstieg in einer Schlucht: L(w) = (λ₁·w₁² + λ₂·w₂²)/2 mit λ₁ = 1 und einstellbarem λ₂.
// Ein Klick in die Karte setzt den Startpunkt, Regler für die Lernrate ρ und die Streckung λ₂.
// Ein Schritt multipliziert w₁ mit 1 − ρλ₁ und w₂ mit 1 − ρλ₂, deshalb lässt sich alles, was man
// sieht, vorher ausrechnen: Zickzack ab ρ > 1/λ₂, Divergenz ab ρ > 2/λ₂. Rechts der Loss über die
// Schritte. Eingebunden im Kapitel „Gradientenabstieg“ über {anywidget}; im PDF steht statt dessen
// die Abbildung vl05-schlucht.png (dieselbe Funktion, derselbe Start). Keine Abhängigkeiten.
//
// Modell (JSON5 im Direktivenrumpf): {start: [w1, w2], rho: 0.15, lambda2: 10}

const NS = "http://www.w3.org/2000/svg";
const XB = [-5, 5];
const YB = [-3, 3];
const S = 48; // Pixel je Einheit
const BK = (XB[1] - XB[0]) * S; // Breite der Karte
const H = (YB[1] - YB[0]) * S;
const LUECKE = 40;
const BL = 220; // Breite der Loss-Kurve
const SCHRITTE = 30;
const LAMBDA1 = 1;
const NIVEAUS = [0.5, 2, 5, 10, 20, 40, 80];

const FARBEN = {
  hell: { pfad: "#006AB3", start: "#EE7F00", hoehe: "#B5CBD6", gitter: "#eeeeee", grau: "#777777" },
  dunkel: { pfad: "#5aa9e6", start: "#ffa040", hoehe: "#4a6070", gitter: "#333333", grau: "#9a9a9a" },
};

const zahl = (x, stellen = 2) =>
  (Math.abs(x) < 0.5 * 10 ** -stellen ? 0 : x).toLocaleString("de-DE", {
    minimumFractionDigits: stellen,
    maximumFractionDigits: stellen,
  });
const kx = (x) => (x - XB[0]) * S;
const ky = (y) => (YB[1] - y) * S;

function el(tag, attrs = {}, parent) {
  const e = document.createElementNS(NS, tag);
  for (const [k, val] of Object.entries(attrs)) e.setAttribute(k, val);
  if (parent) parent.appendChild(e);
  return e;
}

function render({ model, el: wurzel }) {
  const vorgabe = {
    start: [...(model.get("start") ?? [-4.5, 2])],
    rho: model.get("rho") ?? 0.15,
    lambda2: model.get("lambda2") ?? 10,
  };
  let start = [...vorgabe.start];
  let rho = vorgabe.rho;
  let lambda2 = vorgabe.lambda2;
  const uid = Math.random().toString(36).slice(2, 8);

  const box = document.createElement("div");
  box.className = "gd";
  const stil = document.createElement("style");
  stil.textContent = `
    .gd { font-family: inherit; color: inherit; margin: 1rem 0; }
    .gd svg { width: 100%; height: auto; display: block; user-select: none; }
    .gd .karte { cursor: crosshair; }
    .gd .gitter line { stroke: var(--gitter); stroke-width: 1; }
    .gd .achsen line { stroke: currentColor; stroke-width: 1; opacity: 0.5; }
    .gd .beschriftung { fill: currentColor; font-size: 15px; }
    .gd .regler { display: grid; grid-template-columns: repeat(auto-fit, minmax(16rem, 1fr));
      gap: 0.3rem 1.5rem; margin-top: 0.6rem; }
    .gd label { display: grid; grid-template-columns: 7.5rem 1fr 3.4rem; align-items: center; gap: 0.5rem;
      font-variant-numeric: tabular-nums; }
    .gd label span:last-child { text-align: right; }
    .gd input[type=range] { width: 100%; }
    .gd button { font: inherit; color: inherit; background: transparent; border: 1px solid currentColor;
      border-radius: 6px; padding: 0.2em 0.7em; cursor: pointer; margin-top: 0.5rem; }
    .gd button:hover { background: rgba(127,127,127,0.15); }
    .gd .stand { font-variant-numeric: tabular-nums; margin-top: 0.5rem; line-height: 1.6; }
    .gd .hinweis { font-size: 0.85em; opacity: 0.75; margin-top: 0.4rem; }
    .gd .hinweis a { color: inherit; }
  `;
  box.appendChild(stil);

  const B = BK + LUECKE + BL;
  const svg = el("svg", { viewBox: `0 0 ${B} ${H + 24}`, role: "img" });
  box.appendChild(svg);
  const defs = el("defs", {}, svg);
  const clip = el("clipPath", { id: `karte-${uid}` }, defs);
  el("rect", { x: 0, y: 0, width: BK, height: H }, clip);

  // Karte
  const karte = el("g", { class: "karte" }, svg);
  el("rect", { x: 0, y: 0, width: BK, height: H, fill: "transparent" }, karte);
  const gitter = el("g", { class: "gitter" }, karte);
  for (let k = XB[0]; k <= XB[1]; k++) el("line", { x1: kx(k), y1: 0, x2: kx(k), y2: H }, gitter);
  for (let k = YB[0]; k <= YB[1]; k++) el("line", { x1: 0, y1: ky(k), x2: BK, y2: ky(k) }, gitter);
  const achsen = el("g", { class: "achsen" }, karte);
  el("line", { x1: 0, y1: ky(0), x2: BK, y2: ky(0) }, achsen);
  el("line", { x1: kx(0), y1: 0, x2: kx(0), y2: H }, achsen);
  const hoehen = el("g", { "clip-path": `url(#karte-${uid})`, fill: "none", "stroke-width": 1.2 }, karte);
  const pfad = el("polyline", { fill: "none", "stroke-width": 1.8, "clip-path": `url(#karte-${uid})` }, karte);
  const punkte = el("g", { "clip-path": `url(#karte-${uid})` }, karte);
  const startPunkt = el("circle", { r: 7 }, karte);
  const minimum = el("path", { d: `M${kx(0) - 7},${ky(0)} h14 M${kx(0)},${ky(0) - 7} v14`, "stroke-width": 1.5 }, karte);
  const text = (x, y, inhalt, anker = "start", eltern = svg) => {
    const t = el("text", { x, y, class: "beschriftung", "text-anchor": anker }, eltern);
    t.textContent = inhalt;
    return t;
  };
  text(BK - 4, ky(0) - 6, "w₁", "end");
  text(kx(0) + 6, 16, "w₂");

  // Loss über die Schritte, logarithmisch
  const lx0 = BK + LUECKE;
  const lossG = el("g", {}, svg);
  el("rect", { x: lx0, y: 0, width: BL, height: H, fill: "none", stroke: "currentColor", "stroke-opacity": 0.3 }, lossG);
  const LOG = [-6, 4]; // log10 L von 10⁻⁶ bis 10⁴
  const lxs = (k) => lx0 + (k / SCHRITTE) * BL;
  const lys = (L) => {
    const l = Math.log10(Math.max(L, 10 ** LOG[0]));
    return H - ((Math.min(l, LOG[1]) - LOG[0]) / (LOG[1] - LOG[0])) * H;
  };
  const lossGitter = el("g", { class: "gitter" }, lossG);
  for (let e = LOG[0]; e < LOG[1]; e += 2) {
    el("line", { x1: lx0, y1: lys(10 ** e), x2: lx0 + BL, y2: lys(10 ** e) }, lossGitter);
    text(lx0 + BL - 4, lys(10 ** e) - 4, "10" + toHoch(String(e)), "end", lossG);
  }
  text(lx0 + 4, 16, "L nach k Schritten", "start", lossG);
  text(lx0, H + 18, "0", "start", lossG);
  text(lx0 + BL, H + 18, `k = ${SCHRITTE}`, "end", lossG);
  const lossKurve = el("polyline", { fill: "none", "stroke-width": 2 }, lossG);

  // Regler
  const regler = document.createElement("div");
  regler.className = "regler";
  box.appendChild(regler);
  // Lernrate auf einer Liste runder Werte: fein bis 0,3 (dort liegen Zickzack und Divergenz bei
  // λ₂ = 10), gröber bis 2, damit bei λ₂ = 1 auch ρ = 1 – ein Schritt ins Minimum – genau einstellbar ist
  const RHOS = [];
  for (let k = 1; k <= 60; k++) RHOS.push(k * 0.005);
  for (let k = 31; k <= 100; k++) RHOS.push(k * 0.01);
  for (let k = 21; k <= 40; k++) RHOS.push(k * 0.05);
  const rhoAus = (i) => RHOS[i];
  const rhoZu = (r) => RHOS.reduce((best, v, i) => (Math.abs(v - r) < Math.abs(RHOS[best] - r) ? i : best), 0);
  const schieber = (titel, min, max, schritt, wert, stellen, aendern, abbildung = (v) => v, umkehr = (v) => v) => {
    const lab = document.createElement("label");
    const t = document.createElement("span");
    t.innerHTML = titel;
    const inp = document.createElement("input");
    Object.assign(inp, { type: "range", min, max, step: schritt, value: umkehr(wert) });
    inp.setAttribute("aria-label", t.textContent);
    const w = document.createElement("span");
    w.textContent = zahl(wert, stellen);
    inp.addEventListener("input", () => {
      const v = abbildung(Number(inp.value));
      aendern(v);
      w.textContent = zahl(v, stellen);
      inp.setAttribute("aria-valuetext", zahl(v, stellen));
      zeichne();
    });
    lab.append(t, inp, w);
    regler.appendChild(lab);
    return { inp, w, stellen, umkehr };
  };
  const sRho = schieber("Lernrate ρ", 0, RHOS.length - 1, 1, rho, 3, (v) => { rho = v; }, rhoAus, rhoZu);
  const sLam = schieber("Streckung λ<sub>2</sub>", 1, 25, 0.5, lambda2, 1, (v) => { lambda2 = v; });

  const zurueck = document.createElement("button");
  zurueck.type = "button";
  zurueck.textContent = "Zurücksetzen";
  zurueck.addEventListener("click", () => {
    start = [...vorgabe.start];
    rho = vorgabe.rho;
    lambda2 = vorgabe.lambda2;
    for (const [s, v] of [[sRho, rho], [sLam, lambda2]]) {
      s.inp.value = s.umkehr(v);
      s.w.textContent = zahl(v, s.stellen);
    }
    zeichne();
  });
  box.appendChild(zurueck);

  const stand = document.createElement("div");
  stand.className = "stand";
  stand.setAttribute("aria-live", "polite");
  box.appendChild(stand);
  const hinweis = document.createElement("div");
  hinweis.className = "hinweis";
  hinweis.innerHTML = `Ein Klick in die Karte setzt den Startpunkt. Bei λ<sub>2</sub> = 1 sind die Höhenlinien Kreise – das ist die Schlucht nach der Standardisierung. Echte Loss-Landschaften trainierter Netze, ohne Formel: <a href="https://losslandscape.com/explorer" target="_blank" rel="noopener">Loss Landscape Explorer</a> (externe Seite).`;
  box.appendChild(hinweis);

  function farben() {
    const fb = FARBEN[document.documentElement.classList.contains("dark") ? "dunkel" : "hell"];
    box.style.setProperty("--gitter", fb.gitter);
    hoehen.setAttribute("stroke", fb.hoehe);
    pfad.setAttribute("stroke", fb.pfad);
    punkte.setAttribute("fill", fb.pfad);
    lossKurve.setAttribute("stroke", fb.pfad);
    startPunkt.setAttribute("fill", fb.start);
    minimum.setAttribute("stroke", fb.grau);
  }

  function zeichne() {
    farben();
    const lam = [LAMBDA1, lambda2];
    const L = (w) => (lam[0] * w[0] * w[0] + lam[1] * w[1] * w[1]) / 2;

    // Höhenlinien: Ellipsen mit Halbachsen sqrt(2c/λ)
    hoehen.replaceChildren();
    for (const c of NIVEAUS) {
      el("ellipse", { cx: kx(0), cy: ky(0), rx: Math.sqrt((2 * c) / lam[0]) * S, ry: Math.sqrt((2 * c) / lam[1]) * S }, hoehen);
    }

    // der Pfad: w ← w − ρ·∇L(w) = ((1 − ρλ₁)·w₁, (1 − ρλ₂)·w₂)
    const ws = [start];
    let w = start;
    for (let k = 0; k < SCHRITTE; k++) {
      w = [(1 - rho * lam[0]) * w[0], (1 - rho * lam[1]) * w[1]];
      ws.push(w);
      if (Math.abs(w[0]) > 1e4 || Math.abs(w[1]) > 1e4) break;
    }
    // gezeichnet wird nur bis zum ersten Punkt außerhalb der Karte, sonst verdeckt das Pendeln alles
    const raus = ws.findIndex((p) => p[0] < XB[0] || p[0] > XB[1] || p[1] < YB[0] || p[1] > YB[1]);
    const sichtbar = raus > 0 ? ws.slice(0, raus + 1) : ws;
    pfad.setAttribute("points", sichtbar.map((p) => `${kx(p[0]).toFixed(1)},${ky(p[1]).toFixed(1)}`).join(" "));
    punkte.replaceChildren();
    for (const p of sichtbar.slice(1)) el("circle", { cx: kx(p[0]), cy: ky(p[1]), r: 2.5 }, punkte);
    startPunkt.setAttribute("cx", kx(start[0]));
    startPunkt.setAttribute("cy", ky(start[1]));

    const Ls = ws.map(L);
    lossKurve.setAttribute("points", Ls.map((v, k) => `${lxs(k).toFixed(1)},${lys(v).toFixed(1)}`).join(" "));

    // Diagnose aus den beiden Faktoren, nicht aus dem Bild
    const f = [1 - rho * lam[0], 1 - rho * lam[1]];
    const groesster = Math.max(Math.abs(f[0]), Math.abs(f[1]));
    let urteil;
    if (groesster > 1 + 1e-9) urteil = "divergiert: ein Faktor hat Betrag größer als 1";
    else if (groesster > 1 - 1e-9) urteil = "bleibt stehen oder pendelt: ein Faktor hat Betrag genau 1";
    else if (Math.min(f[0], f[1]) < -0.1) urteil = "Zickzack: ein Faktor ist negativ, die Komponente wechselt jeden Schritt das Vorzeichen";
    else if (groesster > 0.9) urteil = "kriecht: ein Faktor liegt nahe bei 1";
    else urteil = "konvergiert zügig";
    const kritisch = 2 / Math.max(lam[0], lam[1]);
    stand.innerHTML = `Start (${zahl(start[0], 1)}; ${zahl(start[1], 1)}), <i>L</i> = ${zahl(Ls[0])};
      nach ${ws.length - 1} Schritten <i>L</i> = ${Ls[Ls.length - 1] > 1e6 ? "über 10⁶" : zahl(Ls[Ls.length - 1], Ls[Ls.length - 1] >= 1 ? 2 : 4)}<br>
      Faktoren je Schritt: <i>w</i><sub>1</sub> · ${zahl(f[0], 3)}, <i>w</i><sub>2</sub> · ${zahl(f[1], 3)} – ${urteil}<br>
      kritische Lernrate 2/λ<sub>max</sub> = ${zahl(kritisch, 3)}`;
    svg.setAttribute("aria-label", `Höhenlinienkarte mit Gradientenabstiegspfad ab (${zahl(start[0], 1)}; ${zahl(start[1], 1)}), ${urteil}`);
  }

  karte.addEventListener("click", (ev) => {
    const r = svg.getBoundingClientRect();
    const s = B / r.width;
    const x = (ev.clientX - r.left) * s;
    const y = (ev.clientY - r.top) * s;
    if (x > BK || y > H) return;
    start = [Math.round((XB[0] + x / S) * 10) / 10, Math.round((YB[1] - y / S) * 10) / 10];
    zeichne();
  });

  const beobachter = new MutationObserver(zeichne);
  beobachter.observe(document.documentElement, { attributes: true, attributeFilter: ["class"] });

  wurzel.appendChild(box);
  zeichne();
  return () => {
    beobachter.disconnect();
    box.remove();
  };
}

// 10^-6 als „10⁻⁶“
function toHoch(s) {
  const hoch = { "-": "⁻", 0: "⁰", 1: "¹", 2: "²", 3: "³", 4: "⁴", 5: "⁵", 6: "⁶", 7: "⁷", 8: "⁸", 9: "⁹" };
  return [...s].map((c) => hoch[c] ?? c).join("");
}

export default { render };
