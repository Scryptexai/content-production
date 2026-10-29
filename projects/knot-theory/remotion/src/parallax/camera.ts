/**
 * camera.ts — model kamera untuk parallax berlapis.
 *
 * Ini menjawab kritik "Remotion + Blender bukan parallax": pipeline lama
 * merender SATU plate Blender lalu menempelkannya di belakang teks. Satu lapis
 * berarti faktor parallax = 0 — tidak ada kedalaman, hanya gambar yang diam.
 *
 * Model di sini fisik: setiap lapis punya jarak z. Kamera bergeser sejauh
 * (x, y) dan mendorong maju (zoom). Pergeseran sebuah lapis di layar:
 *
 *     p = zRef / z                      // faktor parallax
 *     tx = -camX * p * GAIN             // makin dekat → makin cepat bergeser
 *     ty = -camY * p * GAIN
 *     scale = 1 + (zoom - 1) * p * GAINS
 *
 * Rasio pergeseran antara dua lapis = z_far / z_near. Itu bisa diukur, dan
 * diukur di scripts/verify_parallax.ts.
 */

export type Camera = {
  x: number;
  y: number;
  zoom: number;
  focus: number; // jarak z yang tajam
};

export const Z_REF = 1000;
export const GAIN_X = 0.085;
export const GAIN_S = 0.42;

export const smoothstep = (t: number) => {
  const c = Math.max(0, Math.min(1, t));
  return c * c * (3 - 2 * c);
};

export const lerp = (a: number, b: number, t: number) => a + (b - a) * t;

/** Lintasan kamera sepanjang satu shot. */
/** Bidang aksi (tangga + figur). Fokus selalu di sini — bukan ditarik-tarik,
 *  karena rack focus yang salah membuat subjek ikut buram. */
export const FOCUS_Z = 360;

export const cameraAt = (t: number, dur: number): Camera => {
  const q = smoothstep(Math.min(1, t / dur));
  return {
    x: lerp(0, 78, q),
    y: lerp(-10, -46, q),
    zoom: lerp(1.0, 1.14, q),
    focus: FOCUS_Z,
  };
};

export const parallaxOf = (z: number) => Z_REF / z;

export const layerStyle = (cam: Camera, z: number, blurScale = 1) => {
  const p = parallaxOf(z);
  const tx = -cam.x * p * GAIN_X;
  const ty = -cam.y * p * GAIN_X;
  const sc = 1 + (cam.zoom - 1) * p * GAIN_S;
  // Depth of field. Subjek selalu tajam. Latar di belakang subjek lebih cepat
  // buram daripada latar depan — itu yang membuat mata tahu apa yang penting.
  let blur = 0;
  if (z > cam.focus) {
    blur = Math.max(0, Math.min(1.6, 1 - cam.focus / z) - 0.04) * 11;
  } else if (z < cam.focus) {
    blur = Math.max(0, Math.min(1.2, 1 - z / cam.focus) - 0.08) * 4.2;
  }
  blur *= blurScale;
  return {
    transform: `translate3d(${tx.toFixed(3)}px, ${ty.toFixed(3)}px, 0) scale(${sc.toFixed(4)})`,
    filter: blur > 0.25 ? `blur(${blur.toFixed(2)}px)` : undefined,
    willChange: "transform",
  };
};

/** Kabut atmosferik: lapis jauh dicampur warna horizon. */
export const hazeOf = (z: number, max = 0.62) => {
  const q = Math.max(0, Math.min(1, (z - 700) / 2600));
  return q * max;
};
