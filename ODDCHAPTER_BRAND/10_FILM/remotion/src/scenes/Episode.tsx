import React from "react";
import { AbsoluteFill, Easing, interpolate, useCurrentFrame, useVideoConfig } from "remotion";
import { C, H, MARGIN, W } from "../theme";
import data from "../episodes.generated.json";
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

/** PLATE — langit, laut, menara. Tiga lapis vektor, satu aksen oranye. */
const Plate: React.FC<{ lamp: number; dim: number; totalFrames: number }> = ({ lamp, dim, totalFrames }) => {
  const frame = useCurrentFrame();
  const p = interpolate(frame, [0, totalFrames], [0, 1], clamp);
  const scale = 1 + p * 0.045;
  const horizonY = H * 0.70;
  const g = 0.6 + 0.4 * Math.sin(frame / 34);

  return (
    <AbsoluteFill style={{ backgroundColor: C.ink }}>
      <AbsoluteFill style={{ transform: `scale(${scale})`, background: `radial-gradient(120% 60% at 50% ${horizonY}px, #24282E 0%, #17191D 48%, #0D0F12 100%)` }} />
      <svg width={W} height={H} viewBox={`0 0 ${W} ${H}`} style={{ position: "absolute" }}>
        {new Array(9).fill(0).map((_, i) => {
          const y = horizonY + 10 + i * 15 + i * i * 1.6;
          const op = 0.20 - i * 0.021;
          return <line key={i} x1={0} y1={y} x2={W} y2={y} stroke={C.sage} strokeWidth={i === 0 ? 1.6 : 1} opacity={Math.max(0.02, op)} />;
        })}
        <g opacity={0.28 + 0.72 * dim}>
          {/* badan menara */}
          <path
            d={`M ${W / 2 - 96} ${horizonY} L ${W / 2 - 34} ${H * 0.52} L ${W / 2 + 34} ${H * 0.52} L ${W / 2 + 96} ${horizonY} Z`}
            fill="#0A0C0F"
            stroke={C.ivory}
            strokeWidth={2.2}
            strokeOpacity={0.6}
          />
          {/* volume: satu bidang terang di sisi kiri */}
          <path d={`M ${W / 2 - 96} ${horizonY} L ${W / 2 - 34} ${H * 0.52} L ${W / 2 - 6} ${H * 0.52} L ${W / 2 - 40} ${horizonY} Z`} fill={C.ivory} opacity={0.045} />
          {/* galeri + lampu */}
          <rect x={W / 2 - 48} y={H * 0.52 - 13} width={96} height={9} fill={C.ivory} opacity={0.5} />
          <rect x={W / 2 - 44} y={H * 0.52 - 62} width={88} height={49} fill="#0A0C0F" stroke={C.ivory} strokeWidth={2} strokeOpacity={0.55} />
          <path d={`M ${W / 2 - 56} ${H * 0.52 - 62} L ${W / 2} ${H * 0.52 - 112} L ${W / 2 + 56} ${H * 0.52 - 62} Z`} fill="#0A0C0F" stroke={C.ivory} strokeWidth={2} strokeOpacity={0.55} />
          {/* dua celah jendela: memberi skala manusia */}
          <rect x={W / 2 - 4} y={H * 0.56} width={8} height={26} fill={C.ivory} opacity={0.22} />
          <rect x={W / 2 - 4} y={H * 0.63} width={8} height={26} fill={C.ivory} opacity={0.16} />
          {/* berkas */}
          <path d={`M ${W / 2 - 10} ${H * 0.52 - 38} L ${0} ${H * 0.52 - 96} L ${0} ${H * 0.52 - 14} Z`} fill={C.orange} opacity={0.05 * lamp} />
          <path d={`M ${W / 2 + 10} ${H * 0.52 - 38} L ${W} ${H * 0.52 - 96} L ${W} ${H * 0.52 - 14} Z`} fill={C.orange} opacity={0.024 * lamp} />
          <circle cx={W / 2} cy={H * 0.52 - 37} r={44 * g} fill={C.orange} opacity={0.09 * lamp} />
          <circle cx={W / 2} cy={H * 0.52 - 37} r={7} fill={C.orange} opacity={lamp} />
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
        clipPath: `inset(0 ${out}% 0 0)`,
        display: "flex",
        flexWrap: "wrap",
        gap: family === "inter" ? "0 20px" : "0 22px",
      }}
    >
      {words.map((w, i) => {
        const p = interpolate(frame, [born + i * 2, born + i * 2 + 7], [0, 1], { ...clamp, easing: ease });
        return (
          <span key={i} style={{ opacity: p, transform: `translateY(${(1 - p) * 10}px)`, display: "inline-block" }}>
            {w}
          </span>
        );
      })}
    </div>
  );
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
export const Episode: React.FC<{ epId?: string }> = ({ epId = "EP01" }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const ep = getEpisode(epId);
  const tm = getTiming(epId);
  const totalFrames = tm.totalFrames;

  const active = tm.segments.find((s) => frame >= s.startFrame && frame < s.startFrame + s.durFrames);
  const idx = active ? tm.segments.indexOf(active) : -1;
  const segStart = active ? active.startFrame : 0;

  // lampu: menyala di hook, meredup sepanjang bukti, padam di loop
  const lamp = interpolate(
    frame,
    [0, totalFrames * 0.55, totalFrames * 0.78, totalFrames * 0.86],
    [1, 0.7, 0.35, 0],
    clamp,
  );
  const dim = interpolate(frame, [0, totalFrames * 0.5, totalFrames * 0.7], [1, 1, 0.3], clamp);

  return (
    <AbsoluteFill style={{ backgroundColor: C.ink }}>
      <Plate lamp={lamp} dim={dim} totalFrames={totalFrames} />

      {active?.kind === "hook" && (
        <Line text={ep.title} born={segStart + 4} hold={active.durFrames - 4} size={92} family="grotesk" weight={700} top={H * 0.24} />
      )}

      {active?.kind === "beat" && active.cue && (
        <Line text={active.cue} born={segStart + 3} hold={active.durFrames - 3} size={62} top={H * 0.33} />
      )}

      {active?.kind === "turn" && (
        <Turn quote={active.quote || ""} verdict={active.verdict || ""} born={segStart} hold={active.durFrames} />
      )}

      {active?.kind === "loop" && (
        <Line text={active.text} born={segStart + 3} hold={active.durFrames - 3} size={70} family="grotesk" weight={700} top={H * 0.26} />
      )}

      {/* nomor urut kecil, penanda posisi di seri — satu-satunya elemen tetap */}
      <div style={{ position: "absolute", left: MARGIN, top: 300, fontFamily: "Inter", fontWeight: 600, fontSize: 24, letterSpacing: "0.28em", color: C.sage, opacity: 0.8 }}>
        {String(idx + 1).padStart(2, "0")} / {String(tm.segments.length).padStart(2, "0")}
      </div>

      <Footer ep={ep.id.replace("EP", "EP ")} series={ep.series} />
    </AbsoluteFill>
  );
};

export const Episode01: React.FC = () => <Episode epId="EP01" />;
