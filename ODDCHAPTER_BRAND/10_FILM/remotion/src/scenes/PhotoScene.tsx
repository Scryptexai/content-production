import React from "react";
import { AbsoluteFill, Img, interpolate, staticFile, useCurrentFrame } from "remotion";
import { C, H, W } from "../theme";
import { useCamera } from "./Camera";

/**
 * Foto adalah bahan; gerak adalah yang membuatnya video.
 *
 * Setiap gambar punya gerak kamera sendiri (push-in, tarik-out, geser kiri,
 * geser kanan) yang berjalan penuh sepanjang segmen — tidak ada satu frame pun
 * yang diam. Ditambah tiga lapis kecil yang bergerak sendiri: goyang kamera
 * handheld, flicker exposure, dan grain. Semua deterministik dari frame.
 *
 * Hitungan geraknya ada di `Camera.ts` — dipakai bersama oleh plate vektor
 * (`PlateScene.tsx`), supaya episode yang belum punya foto bergerak dengan
 * bahasa yang sama, bukan diam dengan zoom 4 %.
 */

export const Photo: React.FC<{ src: string; i: number; dur: number }> = ({ src, i, dur }) => {
  const cam = useCamera(i, dur);

  return (
    <AbsoluteFill style={{ backgroundColor: C.ink, overflow: "hidden" }}>
      <Img
        src={staticFile(src)}
        style={{
          width: "100%",
          height: "100%",
          objectFit: "cover",
          transform: cam.transform,
          filter: `saturate(0.62) contrast(1.06) brightness(${0.94 * cam.punchBright})`,
          opacity: cam.inn,
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
      <AbsoluteFill style={{ backgroundColor: C.ivory, opacity: Math.max(0, cam.flicker), mixBlendMode: "overlay" }} />
    </AbsoluteFill>
  );
};

/**
 * Frame pertama = thumbnail, persis seperti yang diunggah.
 * Frame 0 tidak punya lapisan apa pun di atasnya: kalau kanal menampilkan
 * thumbnail dari frame ini, gambarnya identik. Setelah 1,5 detik ia mendorong
 * masuk 5 % lalu hilang dalam 3 frame — jadi penonton yang datang dari thumbnail
 * merasa "masuk ke dalam gambar yang tadi saya klik".
 */
export const ThumbIntro: React.FC<{ src: string; frames: number }> = ({ src, frames }) => {
  const frame = useCurrentFrame();
  const s = frame < 2 ? 1 : 1 + Math.min(0.05, (frame / frames) * 0.05);
  const out = interpolate(frame, [frames - 3, frames], [1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  return (
    <AbsoluteFill style={{ backgroundColor: "#000000", opacity: out }}>
      <Img src={staticFile(src)} style={{ width: "100%", height: "100%", objectFit: "cover", transform: `scale(${s})` }} />
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
