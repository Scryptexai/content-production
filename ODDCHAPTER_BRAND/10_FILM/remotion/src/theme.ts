import brand from "./brand.json";

export const C = brand.colors;
export const W = 1080;
export const H = 1920;
export const FPS = 30;

/** Timeline in frames @ 30 fps — the cut is fixed, the audio is placed against it. */
export const T = {
  build: { from: 0, dur: 60 }, //    0.00 –  2.00
  scene1: { from: 60, dur: 180 }, //  2.00 –  8.00
  scene2: { from: 240, dur: 180 }, // 8.00 – 14.00
  plate: { from: 420, dur: 246 }, // 14.00 – 22.20
  end: { from: 666, dur: 210 }, //  22.20 – 29.20
  total: 876,
};

/** Narration placement, in seconds of the final cut. */
export const VO = {
  vo1: 69 / FPS, //  2.30
  vo2: 249 / FPS, // 8.30
  vo3: 426 / FPS, // 14.20
  signature: 672 / FPS, // 22.40
};

export const MARGIN = 96;

/** Royal-Blue easing is forbidden here; everything uses the brand's .2 .7 .2 1 */
export const BRAND_BEZIER = [0.2, 0.7, 0.2, 1] as const;
