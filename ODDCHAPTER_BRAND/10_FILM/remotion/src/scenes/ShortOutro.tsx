import React from "react";
import { AbsoluteFill, Easing, interpolate, useCurrentFrame } from "remotion";
import { BRAND_BEZIER, C, FPS } from "../theme";
import { Monogram, Tagline, Wordmark } from "../components/Marks";

/**
 * ShortOutro — kartu akhir animasi untuk Shorts9:16 (paket video build_short_case).
 *
 * Dipakai sebagai segmen terakhir video: monogram masuk → wordmark → garis
 * oranye → tagline → tahan → fade ke hitam. Kredit/label tetap lewat ASS di
 * atas klip ini (satu baris kecil di bawah), jadi komposisi ini hanya berisi
 * lockup merek.
 *
 * Render: node scripts/render-outro.mjs
 *   -> output/short_outro_9x16.mp4 (1080x1920,30 fps, tanpa audio)
 */

const ease = Easing.bezier(...BRAND_BEZIER);

export const OUTRO_FRAMES = 150; // 5,00 s @30 fps

export const ShortOutro: React.FC = () => {
  const frame = useCurrentFrame();

  // monogram: masuk dengan scale + overshoot halus
  const mark = interpolate(frame, [6, 30], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: ease,
  });
  // "breathing" sangat pelan selama tahan
  const breathe = interpolate(frame, [30, 136], [1, 1.015], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: Easing.inOut(Easing.quad),
  });
  const word = interpolate(frame, [26, 48], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: ease,
  });
  const rule = interpolate(frame, [46, 58], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: ease,
  });
  const tag = interpolate(frame, [56, 74], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: ease,
  });
  // fade rapi ke hitam di8 detik terakhir klip
  const out = interpolate(frame, [OUTRO_FRAMES - 12, OUTRO_FRAMES - 1], [1, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: Easing.in(Easing.quad),
  });

  return (
    <AbsoluteFill
      style={{ backgroundColor: C.ink, alignItems: "center", justifyContent: "center" }}
    >
      <div
        style={{
          marginTop: -220,
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          opacity: out,
        }}
      >
        <div
          style={{
            opacity: mark,
            transform: `scale(${(0.88 + 0.12 * mark) * breathe})`,
          }}
        >
          <Monogram width={340} />
        </div>
        <div
          style={{
            marginTop: 88,
            opacity: word,
            transform: `translateY(${(1 - word) * 18}px)`,
          }}
        >
          <Wordmark capHeight={104} />
        </div>
        <div
          style={{
            marginTop: 64,
            width: 148 * rule,
            height: 5,
            backgroundColor: C.orange,
            transform: `scaleX(${rule})`,
          }}
        />
        <div
          style={{
            marginTop: 46,
            opacity: tag,
            transform: `translateY(${(1 - tag) * 10}px)`,
          }}
        >
          <Tagline width={660} />
        </div>
      </div>

      {/* baris kredit kecil tetap milik ASS — di sini hanya jaga proporsi ruang */}
      <div style={{ position: "absolute", top: 0, left: 0, width: 1, height: 1 }} />
    </AbsoluteFill>
  );
};
