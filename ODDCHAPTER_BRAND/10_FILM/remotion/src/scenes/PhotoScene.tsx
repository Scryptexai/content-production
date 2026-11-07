import React from "react";
import { AbsoluteFill, Img, interpolate, staticFile, useCurrentFrame } from "remotion";
import { C, H, W } from "../theme";

/**
 * Foto adalah bahan; gerak adalah yang membuatnya video.
 *
 * Setiap gambar punya gerak kamera sendiri (push-in, tarik-out, geser kiri,
 * geser kanan) yang berjalan penuh sepanjang segmen — tidak ada satu frame pun
 * yang diam. Ditambah tiga lapis kecil yang bergerak sendiri: goyang kamera
 * handheld, flicker exposure, dan grain. Semua deterministik dari frame.
 *
 * `mode` dipilih dari indeks segmen supaya dua segmen berurutan tidak pernah
 * bergerak ke arah yang sama — mata butuh perubahan arah, bukan hanya perubahan
 * gambar.
 */

const MODES = ["pushIn", "pullOut", "panLeft", "panRight"] as const;
type Mode = (typeof MODES)[number];

export const Photo: React.FC<{ src: string; i: number; dur: number }> = ({ src, i, dur }) => {
  const frame = useCurrentFrame();
  const p = Math.min(1, Math.max(0, frame / Math.max(1, dur - 1)));
  const mode: Mode = MODES[i % MODES.length];

  // skala dasar 1.06: gambar 768×1376 sedikit di-crop agar tidak ada tepi kosong
  const scale =
    mode === "pullOut" || mode === "panRight" ? 1.19 - p * 0.11 : 1.06 + p * 0.13;
  const txRaw =
    mode === "panLeft" ? -38 + p * 76 : mode === "panRight" ? 38 - p * 76 : 0;
  const tyRaw = mode === "pushIn" ? -12 + p * 24 : mode === "pullOut" ? 12 - p * 24 : 0;

  // kamera hidup: goyang halus 1–2 px, tidak pernah nol
  const shakeX = Math.sin(frame / 6.7 + i * 1.7) * 1.6 + Math.sin(frame / 2.3 + i) * 0.6;
  const shakeY = Math.cos(frame / 8.1 + i * 2.3) * 1.4;
  const flicker = 0.015 + 0.018 * Math.sin(frame / 9.3 + i * 2.1) + 0.01 * Math.sin(frame / 2.7);

  // masuk cepat 3 frame dari hitam: potongan keras, bukan dissolve
  const inn = interpolate(frame, [0, 3], [0.35, 1], { extrapolateRight: "clamp" });

  return (
    <AbsoluteFill style={{ backgroundColor: C.ink, overflow: "hidden" }}>
      <Img
        src={staticFile(src)}
        style={{
          width: "100%",
          height: "100%",
          objectFit: "cover",
          transform: `scale(${scale}) translate(${txRaw + shakeX}px, ${tyRaw + shakeY}px)`,
          filter: "saturate(0.62) contrast(1.06) brightness(0.94)",
          opacity: inn,
        }}
      />
      {/* grade: langit gelap di atas, kaki gelap di bawah — teks selalu punya tanah */}
      <AbsoluteFill
        style={{
          background:
            "linear-gradient(180deg, rgba(13,15,18,0.62) 0%, rgba(13,15,18,0.10) 30%, rgba(13,15,18,0.22) 58%, rgba(13,15,18,0.95) 100%)",
        }}
      />
      {/* dingin di bayangan, bukan di seluruh gambar */}
      <AbsoluteFill style={{ backgroundColor: "#0B1220", opacity: 0.16, mixBlendMode: "multiply" }} />
      {/* flicker exposure */}
      <AbsoluteFill style={{ backgroundColor: C.ivory, opacity: Math.max(0, flicker), mixBlendMode: "overlay" }} />
    </AbsoluteFill>
  );
};

/** Bar progres: penonton tahu ini hampir selesai — dan itu yang menahan mereka. */
export const Progress: React.FC<{ frame: number; total: number }> = ({ frame, total }) => {
  const p = Math.min(1, Math.max(0, frame / Math.max(1, total - 1)));
  return (
    <div style={{ position: "absolute", left: 96, right: 96, bottom: 132, height: 3, backgroundColor: "rgba(244,240,232,0.16)" }}>
      <div style={{ width: `${p * 100}%`, height: 3, backgroundColor: C.orange, opacity: 0.85 }} />
    </div>
  );
};

/** Satu garis tipis menyapu layar sekali per segmen: gerak yang tidak mengganggu teks. */
export const Scan: React.FC<{ dur: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const p = Math.min(1, Math.max(0, frame / Math.max(1, dur)));
  return (
    <div
      style={{
        position: "absolute",
        left: 0,
        right: 0,
        top: p * H,
        height: 2,
        background: "linear-gradient(90deg, rgba(244,240,232,0) 0%, rgba(244,240,232,0.20) 22%, rgba(244,240,232,0.20) 78%, rgba(244,240,232,0) 100%)",
        opacity: 0.5,
      }}
    />
  );
};

/** Kedip di setiap potongan: 3 frame gelap membuat cut terasa, bukan patah. */
export const CutFlash: React.FC<{ age: number; strong?: boolean }> = ({ age, strong }) => {
  const peak = strong ? 0.34 : 0.16;
  const o = age < 4 ? peak * (1 - age / 4) : 0;
  return <AbsoluteFill style={{ backgroundColor: "#000000", opacity: o, pointerEvents: "none" }} />;
};

export const letterboxed = (W - 96 * 2) / W;
