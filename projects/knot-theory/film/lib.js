/**
 * lib.js — pustaka animasi untuk film Knot Theory.
 *
 * Pendekatan ini diambil dari `mg-styles-15` (Vincentwei1021, MIT): satu
 * halaman HTML yang bisa menggambar frame untuk waktu berapa pun
 * (`window.renderAt(t)`), lalu headless Chrome menangkap tiap frame.
 *
 * Alasannya praktis, bukan selera: di mesin 2-core yang sama,
 *   Remotion (React + webpack + OffthreadVideo): 23 mnt untuk 300 frame
 *   halaman + render.mjs                      : 27 dtk untuk 300 frame
 * Selisih 51x. Untuk 3 menit video, itu bedanya 7 jam vs 8 menit.
 *
 * Semua fungsi di sini murni terhadap `t` — tidak ada state yang bergantung
 * pada frame sebelumnya, supaya render bisa diulang dan diparalelkan.
 */

export const NS = "http://www.w3.org/2000/svg";

/** Pembuat elemen SVG. */
export const mk = (root) => (tag, attrs, parent) => {
  const e = document.createElementNS(NS, tag);
  if (attrs) for (const k in attrs) e.setAttribute(k, attrs[k]);
  (parent || root).appendChild(e);
  return e;
};

/* ------------------------------------------------------------------ easing */
export const clamp = (x, a = 0, b = 1) => (x < a ? a : x > b ? b : x);
export const lerp = (a, b, u) => a + (b - a) * u;
export const inv = (a, b, x) => clamp((x - a) / (b - a));

export const E = {
  inQ: (u) => u * u,
  outQ: (u) => 1 - (1 - u) ** 2,
  ioQ: (u) => (u < 0.5 ? 2 * u * u : 1 - (-2 * u + 2) ** 2 / 2),
  inC: (u) => u ** 3,
  outC: (u) => 1 - (1 - u) ** 3,
  ioC: (u) => (u < 0.5 ? 4 * u ** 3 : 1 - (-2 * u + 2) ** 3 / 2),
  outQt: (u) => 1 - (1 - u) ** 4,
  outX: (u) => (u >= 1 ? 1 : 1 - 2 ** (-10 * u)),
  outB: (u, s = 1.70158) => 1 + (s + 1) * (u - 1) ** 3 + s * (u - 1) ** 2,
};

/** Bezier kubik — kurva overshoot klasik motion graphics. */
export const bezier = (x1, y1, x2, y2) => {
  const cx = 3 * x1, bx = 3 * (x2 - x1) - cx, ax = 1 - cx - bx;
  const cy = 3 * y1, by = 3 * (y2 - y1) - cy, ay = 1 - cy - by;
  const sx = (t) => ((ax * t + bx) * t + cx) * t;
  const sy = (t) => ((ay * t + by) * t + cy) * t;
  const dx = (t) => (3 * ax * t + 2 * bx) * t + cx;
  return (u) => {
    if (u <= 0) return 0;
    if (u >= 1) return 1;
    let t = u;
    for (let i = 0; i < 10; i++) {
      const d = dx(t);
      if (Math.abs(d) < 1e-6) break;
      t = clamp(t - (sx(t) - u) / d);
    }
    return sy(t);
  };
};
export const POP = bezier(0.34, 1.56, 0.64, 1);

/** Spring teredam bentuk tertutup — lebih hidup dari ease biasa. */
export const spring = (t, f = 2.4, z = 0.42) => {
  if (t <= 0) return 0;
  const w = 2 * Math.PI * f, a = z * w, b = w * Math.sqrt(1 - z * z);
  return 1 - Math.exp(-a * t) * (Math.cos(b * t) + (a / b) * Math.sin(b * t));
};

export const springV = (t, f = 2.4, z = 0.42) => {
  if (t <= 0) return 0;
  const w = 2 * Math.PI * f, a = z * w, b = w * Math.sqrt(1 - z * z);
  return Math.exp(-a * t) * ((w * w) / b) * Math.sin(b * t);
};

/** Pop dengan squash & stretch dari kecepatan spring. */
export const pop = (t, t0, f = 2.4, z = 0.42, amt = 0.12, pin = 0.9) => {
  const tt = t - t0;
  let s = spring(tt, f, z);
  let k = clamp((springV(tt, f, z) / (2 * Math.PI * f)) * amt * 2, -0.3, 0.3);
  const w = E.ioQ(inv(pin * 0.7, pin, tt));
  return [lerp(s, 1, w), lerp(k, 0, w)];
};

export const hump = (u) => 4 * u * (1 - u);

/* ------------------------------------------------------------------ kamera */
/** Faktor parallax dan gaya transform satu lapis. */
export const ZREF = 1000;
export const GAIN_X = 0.085;
export const GAIN_S = 0.42;

export const camStyle = (cam, z, focusZ = 360, blurK = 1) => {
  const p = ZREF / z;
  const tx = -cam.x * p * GAIN_X;
  const ty = -cam.y * p * GAIN_X;
  const sc = 1 + (cam.zoom - 1) * p * GAIN_S;
  let blur = 0;
  if (z > focusZ) blur = Math.max(0, Math.min(1.6, 1 - focusZ / z) - 0.04) * 11;
  else if (z < focusZ) blur = Math.max(0, Math.min(1.2, 1 - z / focusZ) - 0.08) * 4.2;
  blur *= blurK;
  return {
    transform: `translate(${tx.toFixed(2)} ${ty.toFixed(2)}) translate(960 540) scale(${sc.toFixed(4)}) translate(-960 -540)`,
    filter: blur > 0.25 ? `blur(${blur.toFixed(2)}px)` : "none",
  };
};

/* -------------------------------------------------------------------- PRNG */
export const rng = (seed) => {
  let a = seed >>> 0;
  return () => {
    a = (a + 0x6d2b79f5) >>> 0;
    let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
};

/* ------------------------------------------------------------------- warna */
export const C = {
  ink: "#05070F",
  stone: "#0A0D17",
  stoneTop: "#2A2739",
  edge: "#E4A177",
  cream: "#EFE7DC",
  rose: "#D98E73",
  sage: "#8FA98B",
  lilac: "#A79BC8",
  muted: "#8A93A3",
};
