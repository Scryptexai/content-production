import React from "react";
import { AbsoluteFill, OffthreadVideo, staticFile } from "remotion";

/**
 * Latar = video yang sudah dibakar (make_backdrop_loop.py), diputar lurus
 * tanpa `loop`.
 *
 * Catatan penting dari uji render: `<OffthreadVideo loop>` di versi ini
 * membeku di frame pertama (selisih antar frame 0,000). Karena itu siklus
 * 24 dtk diulang di berkasnya (loop-<tone>-long.mp4, 240 dtk) dan komponen
 * ini memutar lurus. Biayanya tetap ±0,3–0,4 dtk/frame, jauh di bawah
 * 1,6 dtk/frame kalau latar digambar sebagai lapisan gambar ber-animasi.
 */
export const Backdrop: React.FC<{ tone?: string; knotSize?: number }> = ({
  tone = "ink",
}) => (
  <AbsoluteFill style={{ backgroundColor: "#0B0F17" }}>
    <OffthreadVideo
      src={staticFile(`backdrop/loop-${tone}-long.mp4`)}
      muted
      style={{ width: "100%", height: "100%", objectFit: "cover" }}
    />
  </AbsoluteFill>
);
