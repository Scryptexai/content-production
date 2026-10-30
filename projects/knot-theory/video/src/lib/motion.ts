/**
 * motion.ts — sumbu waktu film. Semua angka di sini adalah FRAME (30 fps),
 * kecuali yang diberi akhiran detik.
 *
 * Diadaptasi dari demos/_fixtures/Polish.tsx milik video-shotcraft (Apache-2.0):
 * bezier() dan ramp() dipertahankan semantiknya supaya kurva yang sudah
 * dikalibrasi di kartu-kartu shot tetap terasa sama. Tambahan di sini:
 *  - clamp01 / mix / lerp / smooth
 *  - useCam(): kamera multiplane yang deterministik (tanpa state)
 *  - seeded(): angka acak berbenih tetap (aturan determinisme shotcraft §9)
 */

export const clamp01 = (x: number) => (x < 0 ? 0 : x > 1 ? 1 : x);
export const mix = (a: number, b: number, t: number) => a + (b - a) * t;
export const lerp = mix;
export const smooth = (t: number) => {
  const x = clamp01(t);
  return x * x * (3 - 2 * x);
};

export const bezier = (x1: number, y1: number, x2: number, y2: number) => {
  if (x1 === y1 && x2 === y2) return (t: number) => clamp01(t);
  const ax = 1 - 3 * x2 + 3 * x1;
  const bx = 3 * x2 - 6 * x1;
  const cx = 3 * x1;
  const ay = 1 - 3 * y2 + 3 * y1;
  const by = 3 * y2 - 6 * y1;
  const cy = 3 * y1;
  const sx = (u: number) => ((ax * u + bx) * u + cx) * u;
  const sy = (u: number) => ((ay * u + by) * u + cy) * u;
  const dx = (u: number) => (3 * ax * u + 2 * bx) * u + cx;
  const solve = (x: number) => {
    let u = x;
    for (let i = 0; i < 8; i++) {
      const err = sx(u) - x;
      if (Math.abs(err) < 1e-7) return u;
      const d = dx(u);
      if (Math.abs(d) < 1e-6) break;
      u -= err / d;
    }
    let lo = 0;
    let hi = 1;
    u = x;
    for (let i = 0; i < 40; i++) {
      const v = sx(u);
      if (Math.abs(v - x) < 1e-7) break;
      if (v < x) lo = u;
      else hi = u;
      u = (lo + hi) / 2;
    }
    return u;
  };
  return (t: number) => (t <= 0 ? 0 : t >= 1 ? 1 : sy(solve(t)));
};

export const EASE = {
  snappy: bezier(0.16, 1, 0.3, 1),
  out: bezier(0.22, 1, 0.36, 1),
  smooth: bezier(0.65, 0, 0.35, 1),
  swift: bezier(0.4, 0, 0.2, 1),
  exit: bezier(0.7, 0, 0.84, 0),
  anticip: bezier(0.5, -0.32, 0.25, 1),
  overshoot: bezier(0.34, 1.45, 0.64, 1),
  push: bezier(0.35, 0, 0.2, 1),
  linear: (t: number) => clamp01(t),
};

/** progres 0→1 untuk frame di dalam [start, start+dur], lalu dihaluskan */
export const ramp = (
  frame: number,
  start: number,
  dur: number,
  ease: (t: number) => number = EASE.snappy,
) => ease(clamp01((frame - start) / Math.max(1e-6, dur)));

/**
 * Angka acak berbenih tetap. Dipakai untuk debu dan getaran supaya render
 * bisa diulang persis (shotcraft §9: larangan Math.random / Date.now).
 */
export const seeded = (n: number) => {
  const x = Math.sin(n * 127.1 + 311.7) * 43758.5453;
  return x - Math.floor(x);
};

export type CamKey = {
  /** frame global film */
  f: number;
  /** titik dunia yang ditaruh di tengah bingkai */
  x: number;
  y: number;
  /** 1 = netral; >1 mendekat */
  zoom: number;
  /** rotasi bidang gambar, derajat */
  rot?: number;
  /** geser fokus lensa: 0 = tengah */
  focus?: { x: number; y: number; amount: number };
};

/**
 * Kamera multiplane. Semua objek dihitung relatif ke titik dunia ini;
 * objek dengan `depth` lebih besar bergerak lebih lambat (jauh) —
 * itu yang membuat pan terasa seperti ruang, bukan gambar yang digeser.
 */
export const camAt = (frame: number, keys: CamKey[], ease = EASE.smooth) => {
  if (keys.length === 0) return { x: 0, y: 0, zoom: 1, rot: 0, focus: { x: 0, y: 0, amount: 0 } };
  if (frame <= keys[0].f) return { ...keys[0], rot: keys[0].rot ?? 0, focus: keys[0].focus ?? { x: 0, y: 0, amount: 0 } };
  const last = keys[keys.length - 1];
  if (frame >= last.f) return { ...last, rot: last.rot ?? 0, focus: last.focus ?? { x: 0, y: 0, amount: 0 } };

  for (let i = 0; i < keys.length - 1; i++) {
    const a = keys[i];
    const b = keys[i + 1];
    if (frame >= a.f && frame <= b.f) {
      const t = ease(clamp01((frame - a.f) / Math.max(1e-6, b.f - a.f)));
      const fa = a.focus ?? { x: 0, y: 0, amount: 0 };
      const fb = b.focus ?? { x: 0, y: 0, amount: 0 };
      return {
        x: mix(a.x, b.x, t),
        y: mix(a.y, b.y, t),
        zoom: mix(a.zoom, b.zoom, t),
        rot: mix(a.rot ?? 0, b.rot ?? 0, t),
        focus: { x: mix(fa.x, fb.x, t), y: mix(fa.y, fb.y, t), amount: mix(fa.amount, fb.amount, t) },
      };
    }
  }
  return { ...last, rot: 0, focus: { x: 0, y: 0, amount: 0 } };
};

/**
 * Proyeksi satu titik dunia ke layar.
 * depth 0 = bidang objek utama, >0 = lebih jauh (bergerak lebih lambat,
 * mengecil, dan boleh diburamkan), <0 = lebih dekat ke kamera.
 */
export const project = (
  cam: { x: number; y: number; zoom: number },
  p: { x: number; y: number; z?: number },
  center: { x: number; y: number },
) => {
  const z = p.z ?? 0;
  const parallax = 1 / (1 + Math.max(-0.7, z) * 0.55);
  const scale = cam.zoom * parallax;
  return {
    sx: center.x + (p.x - cam.x) * scale,
    sy: center.y + (p.y - cam.y) * scale,
    scale,
    parallax,
  };
};
