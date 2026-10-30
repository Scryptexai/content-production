/**
 * character.js — KARAKTER BRAND KNOT THEORY ("SIMPUL").
 *
 * Modul ini hanya menggambar. Seluruh gerak datang dari char-joints.json
 * (hasil IK Python; pijakan kaki 0,00 px). Desain bentuk bisa diganti total
 * tanpa menyentuh satu baris data gerak.
 *
 * ── ATURAN BENTUK (jangan diubah tanpa alasan tertulis) ───────────────────
 *
 * 1. KEPALA KREM. Ini yang membuat karakter terbaca pada 40 px: satu titik
 *    terang di atas badan gelap. Wajahnya tidak ada — hanya satu lensa.
 *    Tidak ada mulut, jadi tidak mungkin terbaca lipsync.
 *
 * 2. JAS LONCENG. Hem melebar ke bawah (segitiga terbalik), bukan tabung.
 *    Siluet A-line inilah yang membedakan dia dari piktogram tongkat.
 *    Hem belakang lebih panjang dan tertinggal saat berjalan.
 *
 * 3. KERAH TEGAK + SIMPUL. Kerah berdiri di belakang leher, dan simpul tali
 *    di tenggorokan. Kanal ini bicara simpul & sistem — simpul jadi identitas.
 *
 * 4. BENANG. Satu benang lilac tertinggal di belakang dengan manik krem di
 *    ujungnya. Inilah alat karakter menyentuh visual: benangnya bisa diikat
 *    ke node diagram, jadi dia bukan sekadar hiasan yang berjalan.
 *
 * 5. PALET 4 WARNA. ink · slate (jas) · krem (kepala, tangan, telapak) ·
 *    rose (lensa, lining). Sage & lilac hanya untuk aksen di scene, tidak
 *    dipakai di badan — kalau dipakai, karakter jadi mainan.
 *
 * 6. CAHAYA SELALU DARI KANAN-ATAS. Semua gradien menyala di sisi itu.
 *
 * Ukuran dalam px pada tinggi badan ±390 (rig h=430). Untuk memperbesar,
 * bungkus grup dengan transform scale — jangan ubah angka di sini.
 */

export const CT = {
  slate: "#2B3650",
  slateLit: "#6E7A94",
  slateDark: "#0B1020",
  cream: "#EFE7DC",
  creamMid: "#CFC3B0",
  creamDark: "#8E8578",
  rose: "#D98E73",
  roseLit: "#F6CBAF",
  roseDark: "#7E4534",
  sage: "#8FA98B",
  lilac: "#A79BC8",
  ink: "#05070F",
};

const NS = "http://www.w3.org/2000/svg";
const LIGHT = { x: 0.58, y: -0.81 };
let uid = 0;

/* --------------------------------------------------------------- warna */
const hex = (c) => {
  const n = parseInt(c.slice(1), 16);
  return [(n >> 16) & 255, (n >> 8) & 255, n & 255];
};
export const mix = (a, b, u) => {
  const A = hex(a), B = hex(b);
  return "#" + A.map((v, i) => Math.round(v + (B[i] - v) * u).toString(16).padStart(2, "0")).join("");
};

/* --------------------------------------------------------- geometri 2D */
const add = (a, b) => [a[0] + b[0], a[1] + b[1]];
const sub = (a, b) => [a[0] - b[0], a[1] - b[1]];
const mul = (a, s) => [a[0] * s, a[1] * s];
const len = (a) => Math.hypot(a[0], a[1]) || 1e-6;
const norm = (a) => mul(a, 1 / len(a));
const perp = (a) => [-a[1], a[0]];

function capsuleD(a, b, r1, r2, seg = 7) {
  const d = norm(sub(b, a));
  const n = perp(d);
  const pts = [];
  for (let i = 0; i <= seg; i++) {
    const th = (i / seg) * Math.PI;
    pts.push(add(a, add(mul(n, r1 * Math.cos(th)), mul(d, -r1 * Math.sin(th)))));
  }
  for (let i = 0; i <= seg; i++) {
    const th = (i / seg) * Math.PI;
    pts.push(add(b, add(mul(n, -r2 * Math.cos(th)), mul(d, r2 * Math.sin(th)))));
  }
  return "M" + pts.map((p) => p[0].toFixed(1) + " " + p[1].toFixed(1)).join("L") + "Z";
}

function smoothD(pts, closed = true) {
  const n = pts.length;
  const at = (i) => pts[closed ? (i + n) % n : Math.max(0, Math.min(n - 1, i))];
  let d = `M${pts[0][0].toFixed(1)} ${pts[0][1].toFixed(1)}`;
  const last = closed ? n : n - 1;
  for (let i = 0; i < last; i++) {
    const p0 = at(i - 1), p1 = at(i), p2 = at(i + 1), p3 = at(i + 2);
    const c1 = add(p1, mul(sub(p2, p0), 1 / 6));
    const c2 = sub(p2, mul(sub(p3, p1), 1 / 6));
    d += `C${c1[0].toFixed(1)} ${c1[1].toFixed(1)} ${c2[0].toFixed(1)} ${c2[1].toFixed(1)} ${p2[0].toFixed(1)} ${p2[1].toFixed(1)}`;
  }
  return closed ? d + "Z" : d;
}
export const curveD = (pts) => smoothD(pts, false);

/** Pita tertutup dari tulang belakang + lebar di tiap titik.
 *  Dipakai untuk ekor mantel yang menyambung ke benang: satu bentuk, bukan
 *  tempelan. Arah lebar selalu tegak lurus terhadap tulang, jadi pita tidak
 *  pernah berkerut walau tulangnya berbelok tajam. */
function ribbonD(spine, widths) {
  const L = [], R = [];
  for (let i = 0; i < spine.length; i++) {
    const a = spine[Math.max(0, i - 1)], b = spine[Math.min(spine.length - 1, i + 1)];
    const n = perp(norm(sub(b, a)));
    L.push(add(spine[i], mul(n, widths[i])));
    R.push(add(spine[i], mul(n, -widths[i])));
  }
  return smoothD([...L, ...R.reverse()]);
}

const el = (tag, attrs, parent) => {
  const e = document.createElementNS(NS, tag);
  for (const k in attrs) e.setAttribute(k, attrs[k]);
  parent.appendChild(e);
  return e;
};

/** Gradien silinder: menyala di sisi yang menghadap cahaya. */
function limbGrad(defs, base, lit = 0.5, dark = 0.66) {
  const id = `cg${++uid}`;
  const g = el("linearGradient", { id, gradientUnits: "userSpaceOnUse" }, defs);
  el("stop", { offset: "0%", "stop-color": mix(base, CT.cream, lit) }, g);
  el("stop", { offset: "24%", "stop-color": mix(base, CT.cream, lit * 0.34) }, g);
  el("stop", { offset: "56%", "stop-color": base }, g);
  el("stop", { offset: "100%", "stop-color": mix(base, CT.ink, dark) }, g);
  return { url: `url(#${id})`, node: g, base };
}

function orientGrad(gr, mid, across, ext) {
  let n = norm(across);
  if (n[0] * LIGHT.x + n[1] * LIGHT.y < 0) n = mul(n, -1);
  const g = gr.node;
  g.setAttribute("x1", (mid[0] + n[0] * ext).toFixed(1));
  g.setAttribute("y1", (mid[1] + n[1] * ext).toFixed(1));
  g.setAttribute("x2", (mid[0] - n[0] * ext).toFixed(1));
  g.setAttribute("y2", (mid[1] - n[1] * ext).toFixed(1));
}

/* ============================================================== karakter */
export class Character {
  constructor(parent) {
    const defs = el("defs", {}, parent);
    this.g = el("g", { class: "char" }, parent);
    const g = this.g;

    this.gShadow = el("g", {}, g);
    this.sh = [0, 1].map(() => ({
      soft: el("ellipse", { fill: CT.ink, opacity: 0.5 }, this.gShadow),
      hard: el("ellipse", { fill: CT.ink, opacity: 0.34 }, this.gShadow),
    }));

    const G = this.G = {
      coat: limbGrad(defs, CT.slate, 0.52, 0.70),
      coatB: limbGrad(defs, CT.slate, 0.22, 0.78),
      head: limbGrad(defs, CT.cream, 0.30, 0.46),
      legF: limbGrad(defs, "#151C2D", 0.34, 0.62),
      legB: limbGrad(defs, "#0E1421", 0.18, 0.66),
      armF: limbGrad(defs, CT.slate, 0.46, 0.74),
      armB: limbGrad(defs, CT.slate, 0.16, 0.82),
      hand: limbGrad(defs, CT.cream, 0.18, 0.40),
      handB: limbGrad(defs, mix(CT.cream, CT.slate, 0.42), 0.14, 0.5),
      collar: limbGrad(defs, "#39455F", 0.55, 0.6),
      collarF: limbGrad(defs, "#414E6B", 0.60, 0.62),
      knot: limbGrad(defs, CT.rose, 0.55, 0.5),
      train: limbGrad(defs, mix(CT.slate, CT.rose, 0.28), 0.46, 0.72),
      neckG: limbGrad(defs, CT.creamMid, 0.30, 0.52),
      visor: limbGrad(defs, "#1A2236", 0.30, 0.5),
    };

    const tg = el("linearGradient", { id: `cg${++uid}`, gradientUnits: "userSpaceOnUse" }, defs);
    el("stop", { offset: "0%", "stop-color": mix(CT.cream, CT.lilac, 0.2) }, tg);
    el("stop", { offset: "50%", "stop-color": CT.lilac }, tg);
    el("stop", { offset: "100%", "stop-color": mix(CT.rose, CT.lilac, 0.25) }, tg);
    this.threadGrad = tg;

    const lr = el("radialGradient", { id: `lens${++uid}`, cx: "36%", cy: "30%", r: "76%" }, defs);
    el("stop", { offset: "0%", "stop-color": "#FFF6EA" }, lr);
    el("stop", { offset: "22%", "stop-color": CT.roseLit }, lr);
    el("stop", { offset: "74%", "stop-color": CT.rose }, lr);
    el("stop", { offset: "100%", "stop-color": CT.roseDark }, lr);
    this.lensFill = `url(#${lr.getAttribute("id")})`;

    /* ---- benang (di belakang badan) ---- */
    this.gThread = el("g", {}, g);
    this.threadGlow = el("path", { fill: "none", stroke: CT.lilac, "stroke-width": 9,
      opacity: 0.09, "stroke-linecap": "round" }, this.gThread);
    this.thread = el("path", { fill: "none", stroke: `url(#${tg.getAttribute("id")})`,
      "stroke-width": 2.4, "stroke-linecap": "round" }, this.gThread);
    this.bead = el("circle", { r: 4.6, fill: CT.cream }, this.gThread);
    this.beadRing = el("circle", { r: 9, fill: "none", stroke: CT.lilac,
      "stroke-width": 1.2, opacity: 0.8 }, this.gThread);

    /* ---- badan ---- */
    this.gBody = el("g", {}, g);

    this.legB = el("path", { fill: G.legB.url }, this.gBody);
    this.bootB = el("path", { fill: G.legB.url }, this.gBody);
    this.soleB = el("path", { fill: mix(CT.cream, CT.ink, 0.42), opacity: 0.8 }, this.gBody);
    this.toeB = el("path", { fill: mix(CT.cream, CT.ink, 0.2), opacity: 0.8 }, this.gBody);

    this.coat = el("path", { fill: G.coat.url }, this.gBody);
    this.train = el("path", { fill: G.train.url }, this.gBody);
    this.trainFold = el("path", { fill: "none", stroke: mix(CT.slate, CT.ink, 0.45),
      "stroke-width": 1.5, opacity: 0.55, "stroke-linecap": "round" }, this.gBody);
    this.trainHi = el("path", { fill: "none", stroke: mix(CT.cream, CT.slateLit, 0.25),
      "stroke-width": 1.6, opacity: 0.35, "stroke-linecap": "round" }, this.gBody);
    this.seam = el("path", { fill: "none", stroke: mix(CT.cream, CT.slate, 0.66),
      "stroke-width": 1.6, opacity: 0.35, "stroke-linecap": "round" }, this.gBody);
    this.lapel = el("path", { fill: "none", stroke: mix(CT.cream, CT.slate, 0.28),
      "stroke-width": 4.2, opacity: 0.55, "stroke-linecap": "round" }, this.gBody);
    this.rim = el("path", { fill: "none", stroke: mix(CT.cream, CT.slateLit, 0.3),
      "stroke-width": 2.4, opacity: 0.45, "stroke-linecap": "round" }, this.gBody);

    this.legF = el("path", { fill: G.legF.url }, this.gBody);
    this.bootF = el("path", { fill: G.legF.url }, this.gBody);
    this.soleF = el("path", { fill: CT.cream, opacity: 0.98 }, this.gBody);
    this.toeF = el("path", { fill: CT.cream, opacity: 0.95 }, this.gBody);

    this.armB = el("path", { fill: G.armB.url }, this.gBody);
    this.cuffB = el("path", { fill: mix(CT.cream, CT.slate, 0.45), opacity: 0.75 }, this.gBody);
    this.handB = el("circle", { r: 9, fill: G.handB.url }, this.gBody);

    /* kerah tegak + simpul */
    this.collar = el("path", { fill: G.collar.url }, this.gBody);
    /* kepala krem */
    this.neck = el("path", { fill: G.neckG.url }, this.gBody);
    this.collarF = el("path", { fill: G.collarF.url }, this.gBody);
    this.knotRing = el("circle", { fill: "none", stroke: G.knot.url, "stroke-width": 6 }, this.gBody);
    this.knotHi = el("path", { fill: "none", stroke: CT.roseLit, "stroke-width": 1.8,
      opacity: 0.85, "stroke-linecap": "round" }, this.gBody);
    this.knotTail = el("path", { fill: "none", stroke: G.knot.url, "stroke-width": 5.4,
      "stroke-linecap": "round" }, this.gBody);
    this.headG = el("g", {}, this.gBody);
    this.headShape = el("path", { fill: G.head.url }, this.headG);
    this.visor = el("path", { fill: G.visor.url }, this.headG);
    this.visorHi = el("path", { fill: "none", stroke: mix(CT.cream, CT.slateLit, 0.25),
      "stroke-width": 1.6, opacity: 0.45, "stroke-linecap": "round" }, this.headG);
    this.headRim = el("path", { fill: "none", stroke: "#FFF9F0", "stroke-width": 3,
      opacity: 0.75, "stroke-linecap": "round" }, this.headG);
    this.lensHousing = el("circle", { fill: CT.ink, opacity: 0.92 }, this.headG);
    this.lensRing = el("circle", { fill: "none", stroke: CT.cream, "stroke-width": 2.6 }, this.headG);
    this.lens = el("circle", { fill: this.lensFill }, this.headG);
    this.glint = el("circle", { r: 3.4, fill: "#FFF8EF", opacity: 0.96 }, this.headG);
    this.glint2 = el("circle", { r: 1.5, fill: "#FFF8EF", opacity: 0.5 }, this.headG);

    this.armF = el("path", { fill: G.armF.url }, this.gBody);
    this.cuffF = el("path", { fill: CT.cream, opacity: 0.92 }, this.gBody);
    this.handF = el("circle", { r: 9.6, fill: G.hand.url }, this.gBody);
    this.handHi = el("path", { fill: "none", stroke: "#FFF9F0", "stroke-width": 1.8,
      opacity: 0.4, "stroke-linecap": "round" }, this.gBody);
  }

  /** Satu frame. `clip` = salah satu isi char-joints.json, `t` = detik. */
  draw(clip, t, opt = {}) {
    const FPS = 30;
    const n = clip.poses.length;
    const fi = Math.max(0, Math.min(n - 1, Math.round(t * FPS)));
    const p = clip.poses[fi];
    const pPrev = clip.poses[Math.max(0, fi - 4)];
    const pNext = clip.poses[Math.min(n - 1, fi + 4)];
    const alpha = opt.alpha === undefined ? 1 : opt.alpha;

    const vel = mul(sub(pNext.hip, pPrev.hip), FPS / 8);
    const speed = Math.min(1, len(vel) / 200);
    const vdir = speed > 0.02 ? norm(vel) : [1, 0];

    /* `hd` dari rig adalah arah TURUN (0° = bawah, karena _dir(0)=(0,1) di
       layar dengan y ke bawah). Arah ATAS adalah kebalikannya. Ini pernah
       salah dan seluruh anatomi lokal tergambar cermin — jangan diulang. */
    const U = [-p.hd[0], -p.hd[1]];
    const F = [-U[1], U[0]];          // menghadap kanan saat berdiri tegak
    const hip = p.hip, chest = p.chest, neck = p.neck, head = p.head;
    const armF = p.armL, armB = p.armR;
    const legF = p.legL, legB = p.legR;
    const P = (o, u, f) => [o[0] + U[0] * u + F[0] * f, o[1] + U[1] * u + F[1] * f];

    /* ------------------------------------------------ siluet: JAS LONCENG
       Hem melebar (A-line). Depan pendek, belakang panjang & tertinggal —
       bentuk inilah yang membuat satu frame masih terbaca sebagai gambar,
       bukan tongkat. */
    const lag = speed * 26;
    const bob = Math.sin(t * 8.2) * speed * 2.2;
    const shF = P(chest, -9, 25);
    const shB = P(chest, -14, -27);
    const waistF = P(hip, 12, 30);
    const waistB = P(hip, 4, -32);
    const hemF = add(P(hip, -100, 48), mul(vdir, -lag * 0.30));
    const hemSide = add(P(hip, -116, 0 + bob), mul(vdir, -lag * 0.60));
    const coatPts = [P(chest, 12, 8), shF, waistF, hemF, hemSide, P(hip, -14, -36), waistB, shB];

    /* EKOR MANTEL → BENANG. Satu garis: dari hem belakang, menjuntai, lalu
       menipis jadi benang dan berakhir di manik. Inilah identitas karakter:
       dia membawa benang dari tubuhnya sendiri, dan benang itulah yang nanti
       diikatkan ke node diagram. Saat berjalan ekornya tertinggal. */
    const root = P(hip, -96, -26);
    const wave = Math.sin(t * 2.1) * 7 + Math.sin(t * 1.3 + 1.1) * 4;
    const spine = [
      root,
      add(root, add(mul(F, -18 - lag * 0.3), mul(U, -20 + wave * 0.2))),
      add(root, add(mul(F, -40 - lag * 0.7), mul(U, -40 + wave * 0.5))),
      add(root, add(mul(F, -64 - lag * 1.0), mul(U, -52 + wave * 0.8))),
      add(root, add(mul(F, -86 - lag * 1.3), mul(U, -50 + wave * 1.1))),
    ];
    const wag = [10, 9.5, 7.5, 5, 2.6];
    this.train.setAttribute("d", ribbonD(spine, wag));
    orientGrad(this.G.train, hip, F, 120);

    // tulang ekor digambar sebagai garis halus di dalam pita: memberi lipatan
    this.trainFold.setAttribute("d", curveD(spine));
    this.trainHi.setAttribute("d", curveD(spine.map((q, i) => add(q, mul(U, wag[i] * 0.55)))));

    this.coat.setAttribute("d", smoothD(coatPts));
    orientGrad(this.G.coat, hip, F, 118);
    this.seam.setAttribute("d", curveD([P(chest, -14, 12), P(hip, 20, 24)]));
    this.seam.setAttribute("opacity", 0.20);
    this.lapel.setAttribute("d", curveD([P(chest, -4, 2), P(chest, -26, 18), P(chest, -34, 30)]));
    this.rim.setAttribute("d", curveD([shB, P(chest, 18, -20), P(hip, -34, -30), spine[1]]));
    this.rim.setAttribute("opacity", (0.32 + 0.34 * speed).toFixed(2));

    /* ------------------------------------------------------------ kaki */
    const drawLeg = (leg, path, boot, sole, tip, gLeg, rollK) => {
      const [hj, kn, an] = leg;
      path.setAttribute("d", capsuleD(hj, kn, 20.5, 15.5, 6) + capsuleD(kn, an, 15.5, 12, 6));
      orientGrad(gLeg, kn, perp(norm(sub(kn, hj))), 22);

      /* Rotasi telapak HANYA saat kaki terangkat. Sebelumnya telapak ikut
         berotasi saat menapak, sehingga ujung sepatu menembus lantai sampai
         12 px — pijakan yang benar di data jadi terlihat meleset. */
      const surf = opt.ground ? opt.ground(an) : an[1] + 19.2;
      const air = Math.max(0, surf - (an[1] + 19.2));
      const prevAn = leg === legF ? pPrev.legL[2] : pPrev.legR[2];
      const rollRaw = Math.max(-0.34, Math.min(0.40, (an[1] - prevAn[1]) * -0.10));
      const roll = rollRaw * rollK * Math.min(1, air / 14);
      const cr = Math.cos(roll), sr = Math.sin(roll);
      const foot = (dx, dy) => [an[0] + dx * cr - dy * sr, an[1] + dx * sr + dy * cr];
      const heel = foot(-14, 7), toe = foot(31, 11);
      boot.setAttribute("d", capsuleD(heel, toe, 13, 9.4, 6));
      const s1 = foot(-12, 15), s2 = foot(29, 16.5);
      sole.setAttribute("d", capsuleD(s1, s2, 4.4, 3.6, 5));
      // ujung krem: penanda kontak, sama seperti sol. Ini yang membuat kaki
      // tetap terbaca walau seluruh badan gelap di latar gelap.
      tip.setAttribute("d", capsuleD(foot(24, 8.5), foot(31, 12), 5.2, 4.2, 5));
      return an;
    };
    const anF = drawLeg(legF, this.legF, this.bootF, this.soleF, this.toeF, this.G.legF, 1.0);
    const anB = drawLeg(legB, this.legB, this.bootB, this.soleB, this.toeB, this.G.legB, 0.9);

    /* --------------------------------------------------------- bayangan */
    const shadowOf = (an, s) => {
      const ground = opt.ground ? opt.ground(an) : an[1] + 19.2;
      const air = Math.max(0, ground - (an[1] + 19.2));
      const k = 1 / (1 + air / 24);
      const cx = an[0] + 15, cy = ground + 2.5;
      s.soft.setAttribute("cx", cx.toFixed(1));
      s.soft.setAttribute("cy", cy.toFixed(1));
      s.soft.setAttribute("rx", (29 * k).toFixed(1));
      s.soft.setAttribute("ry", (6.4 * k).toFixed(1));
      s.soft.setAttribute("opacity", (0.44 * k).toFixed(2));
      s.hard.setAttribute("cx", cx.toFixed(1));
      s.hard.setAttribute("cy", cy.toFixed(1));
      s.hard.setAttribute("rx", (13 * k).toFixed(1));
      s.hard.setAttribute("ry", (3.1 * k).toFixed(1));
      s.hard.setAttribute("opacity", (0.32 * k).toFixed(2));
    };
    shadowOf(anF, this.sh[0]);
    shadowOf(anB, this.sh[1]);

    /* ---------------------------------------------------------- lengan */
    const drawArm = (arm, path, cuff, hand, hi, gr, w0, w1) => {
      const [s0, elb, wr] = arm;
      path.setAttribute("d", capsuleD(s0, elb, w0, w0 * 0.88, 6) + capsuleD(elb, wr, w0 * 0.88, w1, 6));

      orientGrad(gr, elb, perp(norm(sub(elb, s0))), 24);
      const d = norm(sub(wr, elb));
      cuff.setAttribute("d", capsuleD(sub(wr, mul(d, 10)), sub(wr, mul(d, 2.5)), w1 * 0.98, w1 * 0.98, 4));
      hand.setAttribute("cx", wr[0].toFixed(1));
      hand.setAttribute("cy", wr[1].toFixed(1));
      hand.setAttribute("r", (w1 * 1.18).toFixed(1));
      if (hi) {
        hi.setAttribute("d", curveD([
          add(wr, mul(U, w1 * 1.05)), add(wr, mul(F, w1 * 1.05)), add(wr, mul(U, -w1 * 0.9)),
        ]));
      }
    };
    // tutup bahu: lingkaran kecil di pangkal lengan. Tanpa ini, pangkal lengan
    // tampak menempel di luar badan.
    drawArm(armB, this.armB, this.cuffB, this.handB, null, this.G.armB, 12.6, 9.2);
    drawArm(armF, this.armF, this.cuffF, this.handF, this.handHi, this.G.armF, 13.4, 9.8);

    /* --------------------------------------------------- kepala & kerah */
    const th = Math.atan2(F[1], F[0]) * 180 / Math.PI;  // local +x → arah hadap
    const gaze = p.gaze || 0;

    // kerah tegak: dua sayap di belakang leher, seperti kerah mantel
    // kerah tegak HANYA di belakang leher. Versi sebelumnya punya sayap di
    // depan dan terbaca seperti paruh — jangan diulang.
    // Kerah: dua lapis. Sisi belakang (di belakang leher) + sisi depan
    // (bulan sabit yang menutup pangkal leher). Yang depan digambar setelah
    // leher, jadi leher krem hanya menyembul sedikit — itu yang membuatnya
    // terbaca sebagai turtleneck, bukan tabung.
    const collarBack = [
      P(neck, -16, -14), P(neck, -14, -30), P(neck, 10, -28),
      P(neck, 12, -14), P(neck, -2, -12),
    ];
    this.collar.setAttribute("d", smoothD(collarBack));
    orientGrad(this.G.collar, neck, F, 38);
    const collarFront = [
      P(neck, -6, -8), P(neck, 2, -14), P(neck, 10, -6),
      P(neck, 6, 12), P(neck, -4, 14), P(neck, -12, 4),
    ];
    this.collarF.setAttribute("d", smoothD(collarFront));
    orientGrad(this.G.collarF, neck, F, 26);

    // simpul di tenggorokan
    const knotC = P(neck, -16, 16);
    this.knotRing.setAttribute("cx", knotC[0].toFixed(1));
    this.knotRing.setAttribute("cy", knotC[1].toFixed(1));
    this.knotRing.setAttribute("r", 6.2);
    this.knotRing.setAttribute("stroke-width", 6);
    this.knotHi.setAttribute("d", curveD([P(knotC, 6.6, -4.5), P(knotC, 8, 0), P(knotC, 6.6, 4.5)]));
    const sw = Math.sin(t * 2.3) * 3 + speed * 7;
    this.knotTail.setAttribute("d", curveD([
      P(knotC, -5, 0), P(knotC, -16, -3 + sw * 0.4), P(knotC, -26, -1 + sw * 0.8),
    ]));

    /* Leher. Tanpa ini kepala terbaca melayang — kesalahan yang paling
       kentara saat close-up. Digambar sebelum kepala, lebih gelap dari
       kepala supaya tidak menyatu dengan wajah krem. */
    const RX = 25.0, RY = 27.5;
    // Leher digambar MASUK ke dalam kepala (bukan berhenti di bawahnya):
    // kalau berhenti, selalu ada celah dan kepala terbaca melayang.
    const neckTop = add(head, mul(U, RY * 0.10));
    this.neck.setAttribute("d", capsuleD(add(chest, mul(U, 8)), neckTop, 8.4, 8.0, 6));
    orientGrad(this.G.neckG, neck, [LIGHT.y, -LIGHT.x], 16);

    /* KEPALA: satu bentuk krem + PITA VISOR gelap melintang + satu lensa
       rose di tengah pita. Tiga elemen, tiga nilai warna berbeda — inilah
       yang membuat kepala tetap terbaca pada 40 px. Jangan menambah elemen
       lain di kepala: setiap tambahan menghapus keterbacaan pada ukuran
       kecil. */
    this.headG.setAttribute("transform",
      `translate(${head[0].toFixed(2)} ${head[1].toFixed(2)}) rotate(${th.toFixed(2)})`);
    const hdPts = [];
    for (let i = 0; i < 16; i++) {
      const a = (i / 16) * Math.PI * 2;
      const wob = 1 + 0.055 * Math.cos(a) - 0.045 * Math.sin(a);
      hdPts.push([Math.cos(a) * RX * wob, Math.sin(a) * RY * wob]);
    }
    this.headShape.setAttribute("d", smoothD(hdPts));
    orientGrad(this.G.head, head, [LIGHT.y, -LIGHT.x], 40);
    // pita visor: mengikuti lengkung kepala, jadi ujungnya menyusut
    const bandY = 1.5, bandH = 15;
    this.visor.setAttribute("d", smoothD([
      [-RX * 0.99, bandY - bandH * 0.5],
      [-RX * 0.55, bandY - bandH * 0.80],
      [RX * 0.55, bandY - bandH * 0.80],
      [RX * 0.985, bandY - bandH * 0.42],
      [RX * 0.985, bandY + bandH * 0.46],
      [RX * 0.52, bandY + bandH * 0.78],
      [-RX * 0.55, bandY + bandH * 0.78],
      [-RX * 0.99, bandY + bandH * 0.44],
    ]));
    this.visorHi.setAttribute("d", curveD([
      [-RX * 0.86, bandY - bandH * 0.42], [0, bandY - bandH * 0.66], [RX * 0.86, bandY - bandH * 0.40],
    ]));
    this.headRim.setAttribute("d", `M${-RX * 0.72} ${-RY * 0.60}A ${RX} ${RY} 0 0 1 ${RX * 0.20} ${-RY * 0.95}`);

    // lensa: satu-satunya wajah
    const lx = 8.0 + gaze * 3.2, ly = 1.5 + gaze * 0.8, LR = 10.6;
    const put = (node, r) => {
      node.setAttribute("cx", lx.toFixed(1));
      node.setAttribute("cy", ly.toFixed(1));
      node.setAttribute("r", r);
    };
    put(this.lensHousing, LR + 2.6);
    put(this.lensRing, LR + 1.1);
    put(this.lens, LR);
    put(this.glint, 3.1);
    this.glint.setAttribute("cx", (lx - LR * 0.34).toFixed(1));
    this.glint.setAttribute("cy", (ly - LR * 0.38).toFixed(1));
    put(this.glint2, 1.4);
    this.glint2.setAttribute("cx", (lx + LR * 0.34).toFixed(1));
    this.glint2.setAttribute("cy", (ly + LR * 0.28).toFixed(1));

    /* ----------------------------------------------------------- benang */
    const anchor = spine[spine.length - 1];
    const wob = Math.sin(t * 1.9) * 8;
    const tip = add(add(anchor, mul(F, -34 - speed * 22)), mul(U, 20 + wob));
    const ctrl = add(anchor, add(mul(F, -24), mul(U, -8 + wob * 0.4)));
    const d = `M${anchor[0].toFixed(1)} ${anchor[1].toFixed(1)}Q${ctrl[0].toFixed(1)} ${ctrl[1].toFixed(1)} ${tip[0].toFixed(1)} ${tip[1].toFixed(1)}`;
    this.thread.setAttribute("d", d);
    this.threadGlow.setAttribute("d", d);
    this.threadGrad.setAttribute("x1", anchor[0].toFixed(1));
    this.threadGrad.setAttribute("y1", anchor[1].toFixed(1));
    this.threadGrad.setAttribute("x2", tip[0].toFixed(1));
    this.threadGrad.setAttribute("y2", tip[1].toFixed(1));
    this.bead.setAttribute("cx", tip[0].toFixed(1));
    this.bead.setAttribute("cy", tip[1].toFixed(1));
    this.beadRing.setAttribute("cx", tip[0].toFixed(1));
    this.beadRing.setAttribute("cy", tip[1].toFixed(1));
    this.beadRing.setAttribute("r", (9 + Math.sin(t * 2.6 + 0.6) * 1.1).toFixed(2));

    this.g.setAttribute("opacity", alpha.toFixed(3));
    return { head, hand: armF[2], anchor, bead: tip, knee: legF[1], foot: legF[2] };
  }
}

export function anchors(clip, t) {
  const n = clip.poses.length;
  const p = clip.poses[Math.max(0, Math.min(n - 1, Math.round(t * 30)))];
  return {
    head: p.head, chest: p.chest, handFront: p.armL[2], handBack: p.armR[2],
    footFront: p.legL[2], footBack: p.legR[2], hip: p.hip,
  };
}
