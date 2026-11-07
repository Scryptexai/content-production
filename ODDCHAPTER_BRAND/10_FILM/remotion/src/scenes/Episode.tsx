import React from "react";
import { AbsoluteFill, Audio, Easing, Sequence, interpolate, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { C, H, MARGIN, W } from "../theme";
import data from "../episodes.generated.json";
import { PlateArt, PlateKind } from "./PlateArt";
import timing from "../timing.generated.json";

/**
 * Episode — satu komposisi untuk semua 21 episode.
 *
 * Isi berasal dari dua file hasil generate:
 *   episodes.generated.json  (tools/content_data.py)   — teks, hook, cue, sumber
 *   timing.generated.json    (tools/build_timing.py)   — kapan tiap segmen mulai
 *
 * Tidak ada teks yang ditulis ulang di komponen ini. Kalau script berubah,
 * video ikut berubah. Kalau narasi punya durasi nyata, timing.json memakai
 * durasi itu, bukan estimasi.
 */

type Beat = { t: number; text: string };
type Ep = {
  id: string;
  day: number;
  slot: string;
  series: string;
  title: string;
  hook: string;
  beats: Beat[];
  turn: string;
  loop: string;
  cues: string[];
  durasi: number;
  plate?: PlateKind;
};
type Seg = {
  kind: "hook" | "beat" | "turn" | "loop";
  key: string;
  text: string;
  dur: number;
  start: number;
  startFrame: number;
  durFrames: number;
  cue?: string;
  quote?: string;
  verdict?: string;
  measured: boolean;
};
type Timing = {
  ep: string;
  title: string;
  series: string;
  fps: number;
  total: number;
  totalFrames: number;
  audioMeasured: boolean;
  segments: Seg[];
};

export const EPISODES = data as unknown as Ep[];
const TIMINGS = timing as unknown as Record<string, Timing>;

export const getEpisode = (id: string): Ep => {
  const e = EPISODES.find((x) => x.id === id);
  if (!e) throw new Error(`Episode ${id} tidak ada di episodes.generated.json`);
  return e;
};
export const getTiming = (id: string): Timing => {
  const t = TIMINGS[id];
  if (!t) throw new Error(`Timing ${id} tidak ada — jalankan tools/build_timing.py ${id}`);
  return t;
};

/** Daftar episode yang punya timing, untuk mendaftarkan komposisi. */
export const timedEpisodeIds = () => Object.keys(TIMINGS).sort();

const ease = Easing.bezier(0.2, 0.7, 0.2, 1);
const clamp = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;

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

/** PLATE — langit + satu bentuk dasar (PlateArt) + grain + vignette. */
const Plate: React.FC<{ lamp: number; dim: number; totalFrames: number; kind: PlateKind }> = ({ lamp, dim, totalFrames, kind }) => {
  const frame = useCurrentFrame();
  const p = interpolate(frame, [0, totalFrames], [0, 1], clamp);
  const scale = 1 + p * 0.045;
  const horizonY = H * 0.7;

  return (
    <AbsoluteFill style={{ backgroundColor: C.ink }}>
      <AbsoluteFill style={{ transform: `scale(${scale})`, background: `radial-gradient(120% 60% at 50% ${horizonY}px, #24282E 0%, #17191D 48%, #0D0F12 100%)` }} />
      <svg width={W} height={H} viewBox={`0 0 ${W} ${H}`} style={{ position: "absolute" }}>
        <g opacity={0.28 + 0.72 * dim}>
          <PlateArt kind={kind} lamp={lamp} />
        </g>
      </svg>
      <Grain seed={5} />
      <AbsoluteFill style={{ background: "linear-gradient(180deg, rgba(13,15,18,0.5) 0%, rgba(13,15,18,0) 28%, rgba(13,15,18,0) 60%, rgba(13,15,18,0.92) 100%)" }} />
    </AbsoluteFill>
  );
};

/** Satu baris teks, muncul per kata, keluar dengan clipPath. Selalu sendiri di layar. */
const Line: React.FC<{ text: string; born: number; hold: number; size?: number; color?: string; top?: number; family?: "grotesk" | "inter"; weight?: number }> = ({
  text,
  born,
  hold,
  size = 64,
  color = C.ivory,
  top = H * 0.33,
  family = "inter",
  weight = 600,
}) => {
  const frame = useCurrentFrame();
  if (frame < born || frame > born + hold) return null;
  const words = text.split(" ");
  const out = interpolate(frame, [born + hold - 9, born + hold], [0, 100], clamp);
  return (
    <div
      style={{
        position: "absolute",
        left: MARGIN,
        right: MARGIN,
        top,
        fontFamily: family === "inter" ? "Inter" : "Space Grotesk",
        fontWeight: weight,
        fontSize: size,
        lineHeight: family === "inter" ? 1.26 : 1.02,
        letterSpacing: family === "inter" ? "0.09em" : "-0.03em",
        color,
        width: W - MARGIN * 2,
        clipPath: `inset(0 ${out}% 0 0)`,
        overflowWrap: "normal",
      }}
    >
      {words.map((w, i) => {
        const p = interpolate(frame, [born + i * 2, born + i * 2 + 7], [0, 1], { ...clamp, easing: ease });
        return (
          <span
            key={i}
            style={{
              opacity: p,
              transform: `translateY(${(1 - p) * 10}px)`,
              display: "inline-block",
              marginRight: family === "inter" ? 20 : 22,
            }}
          >
            {w}
          </span>
        );
      })}
    </div>
  );
};

/** Ukuran huruf menyesuaikan panjang teks: baris panjang tidak boleh menyentuh tepi. */
const fit = (text: string, base: number) => {
  const n = text.length;
  if (n > 104) return Math.round(base * 0.62);
  if (n > 84) return Math.round(base * 0.72);
  if (n > 64) return Math.round(base * 0.84);
  return base;
};

/** Titik balik: satu kutipan besar, satu coretan, satu kalimat pembalik. */
const Turn: React.FC<{ quote: string; verdict: string; born: number; hold: number }> = ({ quote, verdict, born, hold }) => {
  const frame = useCurrentFrame();
  if (frame < born || frame > born + hold) return null;
  const q = interpolate(frame, [born + 4, born + 24], [0, 1], { ...clamp, easing: ease });
  const strike = interpolate(frame, [born + Math.round(hold * 0.42), born + Math.round(hold * 0.42) + 22], [0, 1], clamp);
  const v = interpolate(frame, [born + Math.round(hold * 0.58), born + Math.round(hold * 0.58) + 18], [0, 1], clamp);
  const outAll = interpolate(frame, [born + hold - 12, born + hold], [1, 0], clamp);

  return (
    <AbsoluteFill style={{ paddingLeft: MARGIN, paddingRight: MARGIN, justifyContent: "center", opacity: outAll }}>
      <div style={{ fontFamily: "Inter", fontWeight: 600, fontSize: 25, letterSpacing: "0.32em", color: C.sage, marginBottom: 34 }}>
        YANG SELAMA INI DIKUTIP
      </div>
      <div style={{ position: "relative", opacity: q, transform: `translateY(${(1 - q) * 14}px)` }}>
        <div style={{ fontFamily: "Space Grotesk", fontWeight: 700, fontSize: 96, lineHeight: 1.04, letterSpacing: "-0.035em", color: C.ivory }}>
          {quote}
        </div>
        <div style={{ position: "absolute", left: -8, top: "50%", height: 9, width: `calc(${strike * 100}% + 8px)`, backgroundColor: C.orange }} />
      </div>
      {verdict ? (
        <div style={{ marginTop: 56, fontFamily: "Inter", fontWeight: 600, fontSize: 44, lineHeight: 1.3, letterSpacing: "0.02em", color: C.orange, opacity: v }}>
          {verdict}
        </div>
      ) : null}
    </AbsoluteFill>
  );
};

const Footer: React.FC<{ ep: string; series: string }> = ({ ep, series }) => (
  <div style={{ position: "absolute", left: MARGIN, right: MARGIN, top: 1470 }}>
    <div style={{ height: 1, backgroundColor: C.sage, opacity: 0.32, marginBottom: 24 }} />
    <div style={{ display: "flex", justifyContent: "space-between", alignItems: "baseline" }}>
      <div style={{ fontFamily: "Space Grotesk", fontWeight: 700, fontSize: 30, letterSpacing: "0.34em", color: C.ivory }}>ODDCHAPTER</div>
      <div style={{ fontFamily: "Inter", fontWeight: 600, fontSize: 22, letterSpacing: "0.26em", color: C.sage }}>
        {series} · {ep}
      </div>
    </div>
  </div>
);

/**
 * Episode — timeline membaca timing.generated.json.
 * Semua segmen punya awal dan akhir yang eksplisit, jadi tidak ada dua blok
 * teks yang bisa hidup bersamaan.
 */
/** Caption narasi: teks segmen, durasi dari audio nyata (bukan estimasi). */
const Caption: React.FC<{ text: string; born: number; hold: number }> = ({ text, born, hold }) => {
  const frame = useCurrentFrame();
  if (frame < born || frame > born + hold) return null;
  const inn = interpolate(frame, [born, born + 6], [0, 1], clamp);
  return (
    <div
      style={{
        position: "absolute",
        left: MARGIN,
        right: MARGIN,
        bottom: 520,
        fontFamily: "Inter",
        fontWeight: 600,
        fontSize: 52,
        lineHeight: 1.32,
        letterSpacing: "0.01em",
        color: C.ivory,
        opacity: inn,
        textShadow: "0 2px 24px rgba(0,0,0,0.85)",
      }}
    >
      {text}
    </div>
  );
};

export const Episode: React.FC<{ epId?: string }> = ({ epId = "EP01" }) => {
  const frame = useCurrentFrame();
  const ep = getEpisode(epId);
  const tm = getTiming(epId);
  const totalFrames = tm.totalFrames;

  const active = tm.segments.find((s) => frame >= s.startFrame && frame < s.startFrame + s.durFrames);

  // turn dirender sebagai satu blok, bukan per segmen — dua segmen turn = satu momen
  const turnSegs = tm.segments.filter((s) => s.part === "turn");
  const turnStart = turnSegs.length ? turnSegs[0].startFrame : -1;
  const turnEnd = turnSegs.length ? turnSegs[turnSegs.length - 1].startFrame + turnSegs[turnSegs.length - 1].durFrames : -1;
  const inTurn = frame >= turnStart && frame < turnEnd;
  const turnQuote = turnSegs[0]?.quote || "";
  const turnVerdict = turnSegs[0]?.verdict || "";

  const inHook = active?.kind === "hook";
  const inLoop = active?.kind === "loop";

  // lampu: menyala di hook, meredup selama bukti, padam di loop
  const lamp = interpolate(frame, [0, totalFrames * 0.55, totalFrames * 0.8, totalFrames * 0.9], [1, 0.72, 0.4, 0], clamp);
  const dim = interpolate(frame, [0, totalFrames * 0.5, totalFrames * 0.72], [1, 1, 0.28], clamp);

  return (
    <AbsoluteFill style={{ backgroundColor: C.ink }}>
      {/* audio: satu file per segmen, ditempatkan di frame mulai yang terukur */}
      {tm.segments.map((s) => (
        <Sequence key={s.key} from={s.startFrame} durationInFrames={s.durFrames} name={s.key}>
          <Audio src={staticFile(`audio/${epId}/${s.key}.mp3`)} />
        </Sequence>
      ))}

      <Plate lamp={lamp} dim={dim} totalFrames={totalFrames} kind={(ep.plate || "tower") as PlateKind} />

      {inHook && (
        <Line text={ep.title} born={active!.startFrame + 4} hold={active!.durFrames - 4} size={fit(ep.title, 92)} family="grotesk" weight={700} top={H * 0.22} />
      )}

      {inLoop && (
        <Line text={active!.text} born={active!.startFrame + 3} hold={active!.durFrames - 3} size={fit(active!.text, 74)} family="grotesk" weight={700} top={H * 0.24} />
      )}

      {inTurn && <Turn quote={turnQuote} verdict={turnVerdict} born={turnStart} hold={turnEnd - turnStart} />}

      {/* label editorial: hanya saat beat punya cue, di bawah nomor urut */}
      {active && active.kind === "beat" && active.cue && !inTurn && (
        <Line
          text={active.cue}
          born={active.startFrame + 3}
          hold={active.durFrames - 3}
          size={40}
          top={H * 0.30}
          color={C.sage}
        />
      )}

      {/* scrim: menjaga caption tetap terbaca di atas siluet */}
      <AbsoluteFill
        style={{
          background: "linear-gradient(180deg, rgba(13,15,18,0) 58%, rgba(13,15,18,0.72) 74%, rgba(13,15,18,0.94) 100%)",
          pointerEvents: "none",
        }}
      />

      {/* caption: teks narasi, mengikuti durasi audio nyata tiap segmen */}
      {active && !inHook && !inTurn && !inLoop && (
        <Caption text={active.text} born={active.startFrame} hold={active.durFrames} />
      )}

      <div style={{ position: "absolute", left: MARGIN, top: 300, fontFamily: "Inter", fontWeight: 600, fontSize: 24, letterSpacing: "0.28em", color: C.sage, opacity: 0.8 }}>
        {String(tm.segments.filter((s) => s.startFrame <= frame).length).padStart(2, "0")} / {String(tm.segments.length).padStart(2, "0")}
      </div>

      <Footer ep={ep.id.replace("EP", "EP ")} series={ep.series} />
    </AbsoluteFill>
  );
};

export const Episode01: React.FC = () => <Episode epId="EP01" />;
