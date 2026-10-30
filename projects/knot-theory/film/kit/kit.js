/**
 * kit.js — perkakas scene untuk Knot Theory (short-form vertikal).
 *
 * Isinya lima "tipe scene" yang bisa dipakai ulang, plus tipografi kinetik.
 * Semua fungsi murni terhadap waktu: render bisa diulang, diparalelkan, dan
 * hasilnya sama.
 *
 *   KIN       tipografi kinetik (fade / pop / slide) — kecil, bukan judul
 *   dotPct    "count": angka dibangun dari objek (100 titik = 100 poin)
 *   barPair   "split": dua batang yang berubah bentuk (morph) antar nilai
 *   trefoil   "knot": simpul tiga silang dengan silang atas-bawah
 *   stairs    "climb": tangga geometris (dipakai ulang dari rig)
 *
 * Ukuran tipografi sengaja kecil. Riset sendiri (docs/FACELESS-QUALITY.md)
 * menunjukkan ambang 56 px di frame 1080: di atas itu teks menjadi subjek,
 * bukan keterangan. Di short vertikal ambangnya 44 px dari lebar 1080.
 */

export const NS = "http://www.w3.org/2000/svg";

export const el = (tag, attrs, parent) => {
  const e = document.createElementNS(NS, tag);
  if (attrs) for (const k in attrs) e.setAttribute(k, attrs[k]);
  if (parent) parent.appendChild(e);
  return e;
};

export const mix = (a, b, u) => {
  const pa = parseInt(a.slice(1), 16), pb = parseInt(b.slice(1), 16);
  const A = [(pa >> 16) & 255, (pa >> 8) & 255, pa & 255];
  const B = [(pb >> 16) & 255, (pb >> 8) & 255, pb & 255];
  return "#" + A.map((v, i) => Math.round(v + (B[i] - v) * u).toString(16).padStart(2, "0")).join("");
};

export const clamp = (x, a = 0, b = 1) => (x < a ? a : x > b ? b : x);
export const lerp = (a, b, u) => a + (b - a) * u;
export const inv = (a, b, x) => clamp((x - a) / (b - a));
export const E = {
  outQ: (u) => 1 - (1 - u) ** 2,
  inQ: (u) => u * u,
  ioQ: (u) => (u < 0.5 ? 2 * u * u : 1 - (-2 * u + 2) ** 2 / 2),
  ioC: (u) => (u < 0.5 ? 4 * u ** 3 : 1 - (-2 * u + 2) ** 3 / 2),
  outC: (u) => 1 - (1 - u) ** 3,
  outX: (u) => (u >= 1 ? 1 : 1 - 2 ** (-9 * u)),
  outB: (u, s = 1.9) => 1 + (s + 1) * (u - 1) ** 3 + s * (u - 1) ** 2,
};

export const PAL = {
  ink: "#05070F",
  ink2: "#0B1020",
  slate: "#2B3650",
  slateLit: "#6E7A94",
  cream: "#EFE7DC",
  creamDim: "#A79E90",
  rose: "#D98E73",
  roseLit: "#F2B79C",
  roseDark: "#7E4534",
  sage: "#8FA98B",
  lilac: "#A79BC8",
  muted: "#8A93A3",
};

/* ============================================================ tipografi
   Satu blok teks = satu baris. Muncul dengan `pop` di t0, bisa bergeser
   (slide) saat aktif, dan hilang di t1. Tidak ada teks yang muncul sendiri
   tanpa alasan visual — tiap baris ditempelkan ke sesuatu di scene.        */
export class KIN {
  constructor(parent, opts = {}) {
    this.g = el("g", {}, parent);
    this.font = opts.font || "Helvetica, Arial, sans-serif";
    this.lines = [];
  }

  /** Tambahkan satu baris. `at` = waktu mulai. */
  line(cfg) {
    const {
      text, at, until = 1e9, x = 0, y = 0, size = 40, weight = 400,
      color = PAL.cream, ls = 0, anchor = "start", rise = 18, easing = "pop",
      out = 0.28,
    } = cfg;
    const g = el("g", {}, this.g);
    const t = el("text", {
      x: 0, y: 0, fill: color, "font-family": this.font,
      "font-size": size, "font-weight": weight, "letter-spacing": ls,
      "text-anchor": anchor,
    }, g);
    t.textContent = text;
    const item = { g, t, at, until, x, y, rise, easing, out, size };
    this.lines.push(item);
    return item;
  }

  update(t) {
    for (const L of this.lines) {
      const a = t - L.at;
      if (a < 0 || t > L.until + L.out) {
        L.g.setAttribute("opacity", 0);
        continue;
      }
      let k = 0, dy = L.rise;
      if (L.easing === "pop") {
        k = E.outB(clamp(a / 0.42), 2.1);
        dy = L.rise * (1 - k);
      } else if (L.easing === "fade") {
        k = E.outQ(clamp(a / 0.5));
        dy = L.rise * (1 - k) * 0.4;
      } else if (L.easing === "slide") {
        k = E.outC(clamp(a / 0.38));
        dy = L.rise * (1 - k);
      }
      // keluar
      const o = t > L.until ? 1 - E.outQ(clamp((t - L.until) / L.out)) : 1;
      L.g.setAttribute("opacity", clamp(Math.min(k, o)).toFixed(3));
      L.g.setAttribute("transform",
        `translate(${L.x.toFixed(1)} ${(L.y + dy).toFixed(1)})`);
    }
  }
}

/* ============================================================ COUNT
   Angka dibangun dari objek: 100 titik = 100 poin persentase.
   `frac` mengisi titik demi titik; titik yang belum terisi tetap ada (redup),
   jadi penonton melihat PENYEBUTNYA, bukan hanya pembilangnya. Ini yang
   membedakan "count" dari sekadar angka besar.                            */
export function dotPct(parent, cfg) {
  const { cx, cy, cols = 10, rows = 10, gap = 34, r = 9, colorOn = PAL.rose,
          colorOff = "#38425C", opOff = 0.38 } = cfg;
  const n = cols * rows;
  const nodes = [];
  for (let i = 0; i < n; i++) {
    const c = i % cols, rr = Math.floor(i / cols);
    // dibaca kiri→kanan, atas→bawah
    const x = cx + (c - (cols - 1) / 2) * gap;
    const y = cy + (rr - (rows - 1) / 2) * gap;
    nodes.push({
      x, y,
      node: el("circle", { cx: x, cy: y, r, fill: colorOff, opacity: 0.5 }, parent),
      ring: el("circle", { cx: x, cy: y, r: r + 5, fill: "none",
        stroke: colorOn, "stroke-width": 1.4, opacity: 0 }, parent),
    });
  }
  let last = 0;
  return {
    nodes,
    /** frac 0..1 — jumlah titik yang menyala (boleh pecahan) */
    update(frac, t, pop = 1) {
      const full = Math.floor(frac);
      const part = frac - full;
      for (let i = 0; i < nodes.length; i++) {
        const q = nodes[i];
        if (i < full) {
          q.node.setAttribute("fill", colorOn);
          q.node.setAttribute("opacity", 1);
          q.node.setAttribute("r", (r * pop).toFixed(2));
          q.ring.setAttribute("opacity", 0);
        } else if (i === full && part > 0.02) {
          q.node.setAttribute("fill", colorOn);
          q.node.setAttribute("opacity", (0.35 + 0.65 * part).toFixed(2));
          q.node.setAttribute("r", (r * (0.55 + 0.45 * part) * pop).toFixed(2));
          q.ring.setAttribute("opacity", (0.55 * part).toFixed(2));
        } else {
          q.node.setAttribute("fill", colorOff);
          q.node.setAttribute("opacity", opOff);
          q.node.setAttribute("r", r);
          q.ring.setAttribute("opacity", 0);
        }
      }
    },
  };
}

/* ============================================================ SPLIT
   Dua batang berdampingan yang berubah PANJANG dan WARNA lewat interpolasi
   bentuk (morph), bukan potongan. Dipakai untuk membandingkan dua hasil
   studi — persis kasus "grafik turun menjadi grafik naik" di riset.        */
export function barPair(parent, cfg) {
  const { cx, cy, w = 420, h = 26, gap = 74 } = cfg;
  /* Latar batang SELALU selebar w dan berpusat di cx; yang bergerak hanya
     bagian yang terisi, tumbuh dari cx ke kiri (negatif) atau ke kanan.
     Versi pertama menaruh x = cx untuk bagian terisi, sehingga batang
     tampak bergeser dan label tidak lagi menunjuk ke batangnya. */
  const mkBar = (y, color) => {
    const g = el("g", {}, parent);
    const fill = el("rect", { x: cx - w / 2, y, width: w, height: h, rx: h / 2,
      fill: color, opacity: 0.12 }, g);
    const on = el("rect", { x: cx, y, width: 2, height: h, rx: h / 2,
      fill: color }, g);
    return { g, fill, on };
  };
  // garis nol: tempat semua batang mulai
  el("rect", { x: cx - 1, y: cy - gap / 2 - h / 2 - 18, width: 2,
    height: gap + h + 36, fill: "#4A5470", opacity: 0.55 }, parent);
  const A = mkBar(cy - gap / 2 - h / 2, PAL.rose);
  const B = mkBar(cy + gap / 2 - h / 2, PAL.sage);

  return {
    bars: [A, B],
    /** nilai 0..1 per batang; negatif = tumbuh ke kiri */
    update(a, b, t) {
      const set = (bar, v) => {
        const vv = clamp(Math.abs(v), 0, 1) * (v < 0 ? -1 : 1);
        const wid = Math.max(2, Math.abs(vv) * w);
        bar.on.setAttribute("width", wid.toFixed(1));
        bar.on.setAttribute("x", (vv < 0 ? cx - wid : cx).toFixed(1));
      };
      set(A, a);
      set(B, b);
    },
    setColors(ca, cb) {
      A.on.setAttribute("fill", ca);
      B.on.setAttribute("fill", cb);
    },
    show(k) {
      A.g.setAttribute("opacity", k);
      B.g.setAttribute("opacity", k);
    },
  };
}

/* ============================================================ KNOT
   Proyeksi trefoil: tiga busur berurutan. Tiap busur punya "casing" gelap
   lebih tebal sehingga busur yang digambar belakangan menutup busur
   sebelumnya di titik silang → terbaca sebagai anyaman, bukan cincin.
   `slip` 0..1 menarik simpul terbuka (dipakai saat temuan gagal direplikasi). */
export function trefoil(parent, cfg = {}) {
  const { cx, cy, R = 90, thick = 7, color = PAL.rose, casing = PAL.ink } = cfg;
  const SEGS = [[0.00, 2.10], [2.10, 4.20], [4.20, 6.30]];
  const pairs = SEGS.map(() => {
    const c = el("path", { fill: "none", stroke: casing, "stroke-width": thick * 2.2,
      "stroke-linecap": "round", "stroke-linejoin": "round", opacity: 0 }, parent);
    const k = el("path", { fill: "none", stroke: color, "stroke-width": thick,
      "stroke-linecap": "round", "stroke-linejoin": "round", opacity: 0 }, parent);
    return [c, k];
  });

  const TREF = (th) => [Math.sin(th) + 2 * Math.sin(2 * th), Math.cos(th) - 2 * Math.cos(2 * th)];

  return {
    /**
     * @param open 0..1 seberapa "terbuka" simpulnya (0 = terikat rapat)
     * @param spin rotasi
     * @param draw 0..1 seberapa banyak utas yang sudah tergambar
     * @param pop  skala denyut
     */
    update(open, spin, draw, pop = 1) {
      const scale = (R / 4.2) * pop;
      for (let s = 0; s < 3; s++) {
        const [c, k] = pairs[s];
        const [a0, a1] = SEGS[s];
        const span = (a1 - a0) * clamp(draw * 3 - s, 0, 1);
        if (span <= 0.001) { c.setAttribute("opacity", 0); k.setAttribute("opacity", 0); continue; }
        let d = "";
        const N = 34;
        for (let i = 0; i <= N; i++) {
          const th = a0 + span * (i / N);
          // `open` menambah jari-jari di bagian tengah busur → simpul mengendor
          const bulge = 1 + open * 0.55 * Math.sin(Math.PI * (i / N));
          const [x, y] = TREF(th + spin);
          const px = cx + x * scale * bulge;
          const py = cy + y * scale * 0.95 * bulge;
          d += `${i ? "L" : "M"}${px.toFixed(1)} ${py.toFixed(1)}`;
        }
        c.setAttribute("d", d);
        k.setAttribute("d", d);
        c.setAttribute("opacity", 1);
        k.setAttribute("opacity", 1);
      }
    },
    hide() {
      for (const [c, k] of pairs) { c.setAttribute("opacity", 0); k.setAttribute("opacity", 0); }
    },
  };
}

/* ============================================================ CLIMB
   Tangga geometris. Sama dengan rig: tapak 158, tanjakan 54, 6 anak tangga.
   Digambar dari parameternya, jadi kalau ukuran tangga di rig berubah,
   gambar ini harus diubah di satu tempat saja.                            */
export function stairs(parent, cfg) {
  const { x0, y0, tread = 158, riser = 54, n = 6, plateW = 240, thick = 38 } = cfg;
  const g = el("g", {}, parent);
  let d = `M ${x0 - 90} ${y0 + thick} L ${x0 - 90} ${y0}`;
  for (let i = 0; i < n; i++) {
    const x = x0 + i * tread, y = y0 - i * riser;
    d += ` L ${x + tread} ${y} L ${x + tread} ${y - riser}`;
  }
  const tx = x0 + n * tread, ty = y0 - n * riser;
  d += ` L ${tx + plateW} ${ty} L ${tx + plateW} ${ty + thick} L ${x0 - 90} ${y0 + thick} Z`;
  el("path", { d, fill: PAL.ink2 }, g);
  for (let i = 0; i < n; i++) {
    const x = x0 + i * tread, y = y0 - i * riser;
    el("rect", { x, y: y - 8, width: tread, height: 8, fill: "#1B2338" }, g);
    el("rect", { x, y: y - 9.6, width: tread, height: 1.8, fill: PAL.rose, opacity: 0.5 }, g);
    el("rect", { x: x + tread - 2.2, y: y - riser, width: 2.2, height: riser - 8,
      fill: "#04060C" }, g);
  }
  el("rect", { x: tx, y: ty - 8, width: plateW, height: 8, fill: "#1B2338" }, g);
  el("rect", { x: tx, y: ty - 9.6, width: plateW, height: 1.8, fill: PAL.rose, opacity: 0.5 }, g);
  return g;
}

/* ============================================================ util kamera
   Konvensi tunggal (dipakai semua scene): `cam` adalah titik DUNIA yang
   diletakkan di tengah frame. Kesalahan sebelumnya: cam diperlakukan sebagai
   offset, lalu zoom diterapkan di sekitar titik lain → subjek keluar frame
   saat zoom naik. Jangan diulang.                                          */
export function worldTransform(cam, W, H) {
  return `translate(${W / 2} ${H / 2}) scale(${cam.zoom.toFixed(4)}) `
    + `translate(${(-cam.x).toFixed(2)} ${(-cam.y).toFixed(2)})`;
}

/* ============================================================ BOARD
   "board": banyak entitas dalam satu jenjang, plus satu yang bergerak
   di antaranya. Dipakai untuk cerita promosi: satu titik naik satu baris,
   lalu baris yang ditinggalkannya meredup — karena itu yang diukur
   sesudahnya, bukan yang dinaikkan.

   Versi sebelumnya hanya ada 16:9 (scenes/promo). Di sini baris = jenjang,
   jadi board vertikal membaca atas-bawah sebagai hierarki, bukan tabel. */
export function board(parent, cfg = {}) {
  const { cx, cy, cols = 8, rows = 6, gapX = 74, gapY = 60, r = 9,
          colorOn = PAL.rose, colorOff = "#3A4560", stagger = 0.35 } = cfg;
  const nodes = [];
  const total = cols * rows;
  for (let rr = 0; rr < rows; rr++) {
    const row = [];
    for (let cc = 0; cc < cols; cc++) {
      const x = cx + (cc - (cols - 1) / 2) * gapX;
      const y = cy + (rr - (rows - 1) / 2) * gapY;
      const dot = el("circle", { cx: x, cy: y, r, fill: colorOff, opacity: 0 }, parent);
      row.push({ x, y, dot, i: rr * cols + cc, dim: 0, hi: 0 });
    }
    nodes.push(row);
  }
  const token = el("circle", { cx: 0, cy: 0, r: r + 3.4, fill: colorOn, opacity: 0 }, parent);
  const tokenRing = el("circle", { cx: 0, cy: 0, r: r + 12, fill: "none", stroke: colorOn,
    "stroke-width": 1.6, opacity: 0 }, parent);

  let reveal = 0;

  const paint = () => {
    for (const row of nodes) for (const n of row) {
      const t0 = n.i / total;
      const rev = clamp((reveal * 1.45 - t0 * 0.45));
      const base = 0.72 * rev;
      n.dot.setAttribute("opacity", (base * (1 - 0.50 * n.dim)).toFixed(3));
      n.dot.setAttribute("fill", n.hi > 0.5 ? colorOn : colorOff);
    }
  };

  return {
    nodes,
    token,
    tokenRing,
    /** 0..1 — titik muncul berurutan, bukan serentak */
    show(u) { reveal = clamp(u); paint(); },
    /** tandai satu titik sebagai "yang dipilih" */
    mark(rr, cc, k) { nodes[rr][cc].hi = clamp(k); paint(); },
    /** redam satu baris: 0..1 seberapa redup */
    dimRow(rr, k) { for (const n of nodes[rr]) n.dim = clamp(k); paint(); },
    dimAll(k) { for (const row of nodes) for (const n of row) n.dim = clamp(k); paint(); },
    /**
     * Titik terpilih naik `levels` baris. `u` 0..1 menggerakkan token di
     * sepanjang busur; titik asal dikosongkan supaya terbaca pindah,
     * bukan bertambah.
     */
    lift(cc, fromRow, toRow, u, sway = 26) {
      const a = nodes[fromRow][cc], b = nodes[toRow][cc];
      const k = E.ioC(clamp(u));
      const x = lerp(a.x, b.x, k) + Math.sin(Math.PI * k) * sway;
      const y = lerp(a.y, b.y, k);
      token.setAttribute("cx", x.toFixed(1));
      token.setAttribute("cy", y.toFixed(1));
      token.setAttribute("opacity", (k > 0.001 ? 1 : 0));
      tokenRing.setAttribute("cx", x.toFixed(1));
      tokenRing.setAttribute("cy", y.toFixed(1));
      tokenRing.setAttribute("opacity", (0.55 * Math.sin(Math.PI * clamp(u))).toFixed(3));
      a.dot.setAttribute("opacity", (0.72 * (1 - k * 0.9)).toFixed(3));
      b.dot.setAttribute("opacity", (0.72 * k).toFixed(3));
    },
    hide() {
      reveal = 0; paint();
      token.setAttribute("opacity", 0);
      tokenRing.setAttribute("opacity", 0);
    },
  };
}

/* ============================================================ THREAD
   Penghubung antara tangan karakter dan objek yang "dipegangnya".
   Aturan turunan dari EP01 (docs/SCRIPT-EP01.md, Revisi v4): objek yang
   seolah dipegang tidak boleh mengapung tanpa garis ke tangan — tanpa
   penghubung, penonton membaca objek itu sebagai logo, bukan sebagai
   sesuatu yang sedang dikerjakan karakter.                                */
export function thread(parent, cfg = {}) {
  const { color = PAL.lilac, w = 3, glowW = 12, op = 0.75, glowOp = 0.12, sag = 46 } = cfg;
  const glow = el("path", { fill: "none", stroke: color, "stroke-width": glowW,
    opacity: 0, "stroke-linecap": "round" }, parent);
  const core = el("path", { fill: "none", stroke: color, "stroke-width": w,
    opacity: 0, "stroke-linecap": "round" }, parent);
  return {
    update(ax, ay, bx, by, vis, t = 0) {
      const gx = Math.max(ay, by) + sag + 9 * Math.sin(t * 1.6);
      const mx = (ax + bx) / 2;
      const d = `M${ax.toFixed(1)} ${ay.toFixed(1)}Q${mx.toFixed(1)} ${gx.toFixed(1)} `
        + `${bx.toFixed(1)} ${by.toFixed(1)}`;
      core.setAttribute("d", d);
      glow.setAttribute("d", d);
      const v = clamp(vis);
      core.setAttribute("opacity", (op * v).toFixed(3));
      glow.setAttribute("opacity", (glowOp * v).toFixed(3));
    },
    hide() { core.setAttribute("opacity", 0); glow.setAttribute("opacity", 0); },
  };
}
