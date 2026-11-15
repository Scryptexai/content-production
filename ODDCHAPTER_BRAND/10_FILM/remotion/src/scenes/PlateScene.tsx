import React from "react";
import { AbsoluteFill } from "remotion";
import { C, H, W } from "../theme";
import { useCamera } from "./Camera";
import { PlateArt, PlateKind } from "./PlateArt";

/**
 * PlateSegment — bahan vektor dengan gerak yang sama seperti foto.
 *
 * Dulu episode tanpa foto merender SATU plate untuk seluruh durasi: zoom 4,5 %
 * dalam 40 detik, praktis diam. Sementara EP01–EP08 memotong gambar tiap 3–5
 * detik dengan dorongan kamera. Dua kelompok episode jadi terasa beda kanal.
 *
 * Sekarang plate dirender per segmen, lewat `useCamera` yang sama dengan foto:
 * cut, dorongan 70 px, goyang handheld, flicker, dan garis sapuan (`Scan`).
 * Yang belum sama hanyalah bahannya — plate vektor, bukan foto — dan itu urusan
 * aset, bukan animasi.
 */

/** Garis grain: tekstur halus supaya bidang gelap tidak terlihat seperti warna datar. */
const Grain: React.FC<{ seed: number }> = ({ seed }) => {
  const rows = 44;
  return (
    <AbsoluteFill style={{ opacity: 0.05, mixBlendMode: "screen" }}>
      <svg width={W} height={rows} viewBox={`0 0 ${W} ${rows}`} preserveAspectRatio="none">
        {new Array(rows).fill(0).map((_, i) => {
          const n = Math.sin((i + 1) * 12.9898 + seed * 78.233) * 43758.5453;
          const frac = n - Math.floor(n);
          return <rect key={i} x={frac * W * 0.92} y={i} width={40 + frac * 140} height={0.55} fill={C.ivory} opacity={0.3 + frac * 0.4} />;
        })}
      </svg>
    </AbsoluteFill>
  );
};

export const PlateSegment: React.FC<{ kind: PlateKind; i: number; dur: number; lamp: number; dim: number }> = ({
  kind,
  i,
  dur,
  lamp,
  dim,
}) => {
  const cam = useCamera(i, dur);
  const horizonY = H * 0.7;

  return (
    <AbsoluteFill style={{ backgroundColor: C.ink, overflow: "hidden" }}>
      <AbsoluteFill style={{ opacity: cam.inn, transform: cam.transform }}>
        <AbsoluteFill
          style={{
            background: `radial-gradient(120% 60% at 50% ${horizonY}px, #24282E 0%, #17191D 48%, #0D0F12 100%)`,
          }}
        />
        <svg width={W} height={H} viewBox={`0 0 ${W} ${H}`} style={{ position: "absolute" }}>
          <g opacity={0.28 + 0.72 * dim}>
            <PlateArt kind={kind} lamp={lamp} />
          </g>
        </svg>
      </AbsoluteFill>
      {/* grade: sama dengan jalur foto, supaya teks selalu punya tanah */}
      <AbsoluteFill
        style={{
          background:
            "linear-gradient(180deg, rgba(13,15,18,0.62) 0%, rgba(13,15,18,0.10) 30%, rgba(13,15,18,0.22) 58%, rgba(13,15,18,0.95) 100%)",
        }}
      />
      <AbsoluteFill style={{ backgroundColor: "#0B1220", opacity: 0.16, mixBlendMode: "multiply" }} />
      <Grain seed={5 + i} />
      <AbsoluteFill style={{ backgroundColor: C.ivory, opacity: Math.max(0, cam.flicker), mixBlendMode: "overlay" }} />
    </AbsoluteFill>
  );
};
