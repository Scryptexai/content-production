import React from "react";
import { AbsoluteFill, Audio, Easing, Img, interpolate, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import data from "../longform.generated.json";
import { C, H, MARGIN, W } from "../theme";

/**
 * LongForm — episode panjang (5–11 menit) dari VO pemilik.
 *
 * Kontraknya beda dengan Episode.tsx (short):
 *   · narasi satu berkas, sudah dicampur di build_longform.py → tidak ada
 *     pemotongan audio di sini, jadi tidak mungkin meleset dari VO
 *   · gambar dipotong menurut timestamp pemilik (bukan estimasi kata)
 *   · caption adalah potongan transkrip pemilik, jadi layar tidak pernah
 *     lebih pintar dari narasi
 *
 * Yang membuat 5 menit gambar diam tidak terasa diam: kamera bergerak terus
 * (zoom + geser), grain dan scanline hidup, label bab masuk di awal segmen,
 * dan setiap potongan gambar diakhiri kedip 3 frame.
 */

type Cut = { plate: string; fit: "cover" | "contain"; start: number; end: number };
type Cap = { t0: number; t1: number; text: string };
type Seg = {
  i: number; chapter: string; start: number; end: number;
  startFrame: number; endFrame: number; cuts: Cut[]; captions: Cap[];
};
type Doc = {
  id: string; series: string; title: string; vo: string; fps: number;
  duration: number; totalFrames: number; segments: Seg[];
};

const D = data as unknown as Doc;
const ease = Easing.bezier(0.2, 0.7, 0.2, 1);
const clamp = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;

/** Foto: cover = penuhi layar, contain = kartu di atas kanvas gelap (untuk
 *  engraving, peta, sampul buku — dipotong paksa jadi 9:16 akan merusaknya). */
const Plate: React.FC<{ cut: Cut; durFrames: number; born: number }> = ({ cut, durFrames, born }) => {
  const frame = useCurrentFrame();
  const p = interpolate(frame, [0, durFrames], [0, 1], clamp);
  const zoom = cut.fit === "cover" ? 1.035 + p * 0.075 : 1.0 + p * 0.04;
  const drift = (cut.fit === "cover" ? -18 : -8) * p;
  const inOpacity = interpolate(frame, [0, 6], [0, 1], clamp);

  if (cut.fit === "contain") {
    // Engraving, peta, sampul buku, lembar arsip: jangan dipotong paksa jadi
    // 9:16. Ditampilkan sebagai "kartu arsip" — kertasnya tetap terlihat
    // sebagai kertas (itu memang scan), jadi tidak berpura-pura jadi foto.
    return (
      <AbsoluteFill style={{ backgroundColor: "#080A0C" }}>
        <div
          style={{
            position: "absolute",
            left: MARGIN,
            right: MARGIN,
            top: 300,
            height: 760,
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            opacity: inOpacity,
            transform: `scale(${zoom}) translateY(${drift}px)`,
          }}
        >
          <Img
            src={staticFile(cut.plate)}
            style={{
              maxWidth: "100%",
              maxHeight: "100%",
              objectFit: "contain",
              border: "1px solid rgba(214,222,208,0.22)",
              boxShadow: "0 30px 90px rgba(0,0,0,0.9)",
            }}
          />
        </div>
        <div
          style={{
            position: "absolute",
            left: MARGIN,
            top: 258,
            fontFamily: "Inter",
            fontWeight: 600,
            fontSize: 20,
            letterSpacing: "0.3em",
            color: C.sage,
            opacity: 0.7 * inOpacity,
          }}
        >
          ARSIP
        </div>
        <AbsoluteFill style={{ background: "radial-gradient(72% 46% at 50% 40%, rgba(0,0,0,0) 42%, rgba(0,0,0,0.78) 100%)", pointerEvents: "none" }} />
      </AbsoluteFill>
    );
  }

  return (
    <AbsoluteFill style={{ overflow: "hidden", opacity: inOpacity }}>
      <Img
        src={staticFile(cut.plate)}
        style={{
          width: "100%",
          height: "100%",
          objectFit: "cover",
          transform: `scale(${zoom}) translateY(${drift}px)`,
        }}
      />
      <AbsoluteFill
        style={{
          background:
            "linear-gradient(180deg, rgba(8,10,12,0.55) 0%, rgba(8,10,12,0.18) 26%, rgba(8,10,12,0.12) 50%, rgba(8,10,12,0.82) 84%, rgba(8,10,12,0.96) 100%)",
        }}
      />
      {/* grain: satu tile PNG 256px yang digeser — bukan gradient yang harus
          diraster ulang tiap frame (itu yang membuat render turun ke ±0,04x). */}
      <AbsoluteFill
        style={{
          opacity: 0.055,
          mixBlendMode: "screen",
          backgroundImage: `url(${staticFile("plates/EP01LF/grain.png")})`,
          backgroundSize: "256px 256px",
          transform: `translate(${(born * 7) % 256}px, ${(born * 11) % 256}px)`,
        }}
      />
    </AbsoluteFill>
  );
};

const Chapter: React.FC<{ text: string; born: number; hold: number }> = ({ text, born, hold }) => {
  const frame = useCurrentFrame();
  const inn = interpolate(frame, [born + 2, born + 14], [0, 1], { ...clamp, easing: ease });
  const out = interpolate(frame, [born + hold - 12, born + hold], [1, 0], clamp);
  if (frame < born || frame > born + hold) return null;
  return (
    <div
      style={{
        position: "absolute",
        left: MARGIN,
        top: 210,
        opacity: inn * out,
        transform: `translateY(${(1 - inn) * 12}px)`,
        maxWidth: W - MARGIN * 2,
      }}
    >
      <div style={{ width: 64, height: 3, backgroundColor: C.orange, marginBottom: 22 }} />
      <div
        style={{
          fontFamily: "Inter",
          fontWeight: 700,
          fontSize: text.length > 26 ? 34 : 42,
          letterSpacing: "0.16em",
          lineHeight: 1.24,
          color: C.ivory,
          textShadow: "0 4px 24px rgba(0,0,0,0.9)",
        }}
      >
        {text}
      </div>
    </div>
  );
};

const CaptionLine: React.FC<{ cap: Cap; born: number; hold: number }> = ({ cap, born, hold }) => {
  const frame = useCurrentFrame();
  if (frame < born || frame > born + hold) return null;
  const words = cap.text.split(" ");
  const size = cap.text.length > 52 ? 46 : cap.text.length > 34 ? 52 : 58;
  return (
    <div
      style={{
        position: "absolute",
        left: MARGIN,
        width: W - MARGIN * 2,
        bottom: 430,
        fontFamily: "Inter",
        fontWeight: 600,
        fontSize: size,
        lineHeight: 1.32,
        letterSpacing: "0.004em",
        color: C.ivory,
        textShadow: "0 3px 26px rgba(0,0,0,0.95)",
      }}
    >
      {words.map((w, i) => {
        const p = interpolate(frame, [born + i * 1.4, born + 7 + i * 1.4], [0, 1], clamp);
        return (
          <span key={i} style={{ display: "inline-block", marginRight: 14, opacity: p }}>
            {w}
          </span>
        );
      })}
    </div>
  );
};

const Progress: React.FC<{ frame: number; total: number }> = ({ frame, total }) => {
  const p = Math.min(1, frame / total);
  return (
    <div style={{ position: "absolute", left: 0, right: 0, bottom: 0, height: 6, backgroundColor: "rgba(214,222,208,0.16)" }}>
      <div style={{ width: `${p * 100}%`, height: "100%", backgroundColor: C.orange }} />
    </div>
  );
};

export const LongForm: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const seg = D.segments.find((s) => frame >= s.startFrame && frame < s.endFrame) ?? D.segments[D.segments.length - 1];
  const segFrame = frame - seg.startFrame;
  const segDur = seg.endFrame - seg.startFrame;
  const t = frame / fps;

  const cut = seg.cuts.find((c) => t >= c.start && t < c.end) ?? seg.cuts[seg.cuts.length - 1];
  const cutStart = Math.round(cut.start * fps);
  const cutDur = Math.max(1, Math.round((cut.end - cut.start) * fps));
  const cap = seg.captions.find((c) => t >= c.t0 && t < c.t1) ?? null;
  // frame global (bukan relatif segmen): komponen ini tidak dibungkus <Sequence>,
  // jadi useCurrentFrame() di dalam anak-anaknya mengembalikan frame seluruh video.
  const capStart = cap ? Math.round(cap.t0 * fps) : 0;
  const capDur = cap ? Math.max(1, Math.round((cap.t1 - cap.t0) * fps)) : 0;
  const flash = interpolate(frame - cutStart, [0, 3], [0.22, 0], clamp);

  return (
    <AbsoluteFill style={{ backgroundColor: C.ink }}>
      <Audio src={staticFile(D.vo)} />

      {/* gambar aktif satu saja: potongan tepat di batas timestamp */}
      <Plate cut={cut} durFrames={cutDur} born={frame - cutStart} />

      <AbsoluteFill style={{ backgroundColor: C.ivory, opacity: flash, mixBlendMode: "overlay", pointerEvents: "none" }} />

      <Chapter text={seg.chapter} born={seg.startFrame} hold={Math.min(segDur, Math.round(2.6 * fps))} />
      {cap ? <CaptionLine cap={cap} born={capStart} hold={capDur} /> : null}

      <div style={{ position: "absolute", left: MARGIN, top: 150, fontFamily: "Inter", fontWeight: 600, fontSize: 22, letterSpacing: "0.26em", color: C.sage, opacity: 0.75 }}>
        {String(seg.i + 1).padStart(2, "0")} / {String(D.segments.length).padStart(2, "0")} · {D.title}
      </div>

      <div style={{ position: "absolute", left: MARGIN, right: MARGIN, top: 1660 }}>
        <div style={{ height: 1, backgroundColor: C.sage, opacity: 0.3, marginBottom: 18 }} />
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "baseline" }}>
          <div style={{ fontFamily: "Space Grotesk", fontWeight: 700, fontSize: 26, letterSpacing: "0.34em", color: C.ivory }}>ODDCHAPTER</div>
          <div style={{ fontFamily: "Inter", fontWeight: 600, fontSize: 20, letterSpacing: "0.24em", color: C.sage }}>
            {D.series} · {D.id}
          </div>
        </div>
      </div>

      <Progress frame={frame} total={D.totalFrames} />
    </AbsoluteFill>
  );
};
