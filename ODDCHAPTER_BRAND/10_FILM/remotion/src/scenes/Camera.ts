import { useCurrentFrame } from "remotion";

/**
 * Camera — satu-satunya sumber gerak kamera untuk semua episode.
 *
 * Sebelum ini gerak kamera hanya ada di dalam `Photo` (episode yang punya foto).
 * Episode yang belum punya foto jatuh ke plate vektor yang cuma di-zoom 4,5 %
 * sepanjang 40 detik — jadi EP01–EP08 berdenyut tiap 3–5 detik, EP09 ke atas
 * diam. Itu yang membuat dua kelompok episode terasa dari dua kanal berbeda.
 *
 * Sekarang hitungannya di sini, dipakai `Photo` (foto) dan `PlateSegment`
 * (plate vektor). Satu bahasa gerak, dua bahan. Kalau nanti foto EP09–EP21
 * dibuat, potongannya sudah punya irama yang sama.
 *
 * Semua nilai deterministik dari frame: tidak ada Math.random, jadi render
 * ulang menghasilkan bingkai yang sama.
 */

export type CameraMode = "pushIn" | "pullOut" | "panLeft" | "panRight";

/** Dua segmen berurutan tidak pernah bergerak ke arah yang sama. */
export const MODES: CameraMode[] = ["pushIn", "pullOut", "panLeft", "panRight"];

const clamp = (v: number, a: number, b: number) => Math.min(b, Math.max(a, v));
const lerp = (f: number, from: number, to: number, a: number, b: number) =>
  a + ((clamp(f, from, to) - from) / Math.max(1e-6, to - from)) * (b - a);

export type Camera = {
  frame: number;
  mode: CameraMode;
  /** transform untuk lapisan gambar — dipakai apa adanya oleh foto dan plate */
  transform: string;
  /** opacity masuk: 3 frame dari 0,3 → 1 supaya cut terasa memukul */
  inn: number;
  /** kilau exposure; dipasang sebagai lapisan overlay */
  flicker: number;
  /** pengali kecerahan sesaat setelah cut */
  punchBright: number;
};

export const useCamera = (i: number, dur: number): Camera => {
  const frame = useCurrentFrame();
  const p = clamp(frame / Math.max(1, dur - 1), 0, 1);
  const mode = MODES[i % MODES.length];

  // skala dasar 1,06: bahan sedikit di-crop supaya tidak ada tepi kosong
  const scale =
    mode === "pullOut" || mode === "panRight" ? 1.19 - p * 0.11 : 1.06 + p * 0.13;
  const txRaw = mode === "panLeft" ? -38 + p * 76 : mode === "panRight" ? 38 - p * 76 : 0;
  const tyRaw = mode === "pushIn" ? -12 + p * 24 : mode === "pullOut" ? 12 - p * 24 : 0;

  // kamera hidup: goyang halus 1–2 px, tidak pernah nol
  const shakeX = Math.sin(frame / 6.7 + i * 1.7) * 1.6 + Math.sin(frame / 2.3 + i) * 0.6;
  const shakeY = Math.cos(frame / 8.1 + i * 2.3) * 1.4;
  const flicker = 0.015 + 0.018 * Math.sin(frame / 9.3 + i * 2.1) + 0.01 * Math.sin(frame / 2.7);

  // masuk cepat: 3 frame dari gelap + dorongan 70 px dari arah gerak
  const inn = lerp(frame, 0, 3, 0.3, 1);
  const punch = lerp(frame, 0, 7, 1, 0);
  const punchX = (mode === "panLeft" ? 70 : mode === "panRight" ? -70 : 0) * punch;
  const punchY = (mode === "pushIn" ? 60 : mode === "pullOut" ? -60 : 0) * punch;

  return {
    frame,
    mode,
    transform: `scale(${scale}) translate(${txRaw + shakeX + punchX}px, ${tyRaw + shakeY + punchY}px)`,
    inn,
    flicker,
    punchBright: 1 + 0.28 * punch,
  };
};
