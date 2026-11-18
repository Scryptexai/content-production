import React from "react";
import {
  AbsoluteFill, Audio, Easing, Img, OffthreadVideo, interpolate, staticFile,
  useCurrentFrame, useVideoConfig,
} from "remotion";
import data from "../longform.generated.json";
import { C } from "../theme";

/**
 * LongForm 16:9 — hybrid footage + diagram, versi 3.
 *
 * Aturan yang dipakai (permintaan pemilik, 17 Nov 2026):
 *   · kanvas 16:9 (1920×1080)
 *   · footage Coverr penuh layar untuk bab naratif
 *   · bab struktural memakai ANIMASI DIAGRAM: kartu berisi foto, garis penghubung
 *     digambar bertahap, label muncul satu per satu
 *   · foto tidak pernah penuh layar — selalu di dalam kartu
 *   · kartu bab & interstitial tetap: VO diam, yang berbunyi sfx + musik
 *   · musik mengalir sepanjang video (diurus build_longform.py)
 */

type Cap = { t0: number; t1: number; text: string };
type FootCut = { clip: string; start: number; end: number; offset: number; motion: number };
type DgCard = { plate: string; label: string; sub: string; num: number };
type Diagram = { style?: "cards" | "timeline"; title?: string; kicker?: string; cards: DgCard[] };
type Seg = {
  i: number; chapter: string; start: number; end: number; startFrame: number;
  layout: "footage" | "diagram"; captions: Cap[]; footage?: FootCut[]; diagram?: Diagram;
};
type Card = {
  type: "chapter" | "interstitial"; num: number; kicker: string; title: string;
  sub: string; start: number; end: number; dur: number;
};
type Doc = {
  id: string; series: string; title: string; vo: string; fps: number;
  duration: number; totalFrames: number; cards: Card[]; segments: Seg[];
};

const D = data as unknown as Doc;

const W = 1920;
const H = 1080;
const MX = 104; // margin kiri-kanan
const TOP = 64;
const BOT = 96;

const ease = Easing.bezier(0.2, 0.7, 0.2, 1);
const easeOut = Easing.bezier(0.16, 1, 0.3, 1);
const clamp = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;
const p = (f: number, a: number, b: number, e: (t: number) => number = easeOut) =>
  interpolate(f, [a, b], [0, 1], { ...clamp, easing: e });

/* ───────────────────────── lapisan atmosfer ───────────────────────── */

const Grain: React.FC<{ frame: number }> = ({ frame }) => (
  <>
    {Array.from({ length: 12 }).map((_, i) => {
      const x = (i * 173 + frame * 0.7) % W;
      const y = H - ((frame * 1.3 + i * 191) % (H + 200));
      const r = 1 + ((i * 5) % 3) * 0.7;
      return (
        <div key={i} style={{
          position: "absolute", left: x, top: y, width: r, height: r, borderRadius: "50%",
          backgroundColor: C.ivory, opacity: 0.05 + (i % 4) * 0.03, pointerEvents: "none",
        }} />
      );
    })}
  </>
);

// Dua gradient ini dulu dihitung ulang tiap frame dan menghabiskan waktu render
// di rasterisasi software. Sekarang satu PNG statis (tools/bake_overlay.py).
const Scrim: React.FC = () => (
  <Img
    src={staticFile("overlay/scrim.png")}
    style={{ position: "absolute", inset: 0, width: "100%", height: "100%", pointerEvents: "none" }}
  />
);

/* ───────────────────────────── footage ───────────────────────────── */

const Footage: React.FC<{ cut: FootCut; born: number; durFrames: number }> = ({ cut, born, durFrames }) => {
  const prog = Math.min(1, born / Math.max(1, durFrames));
  const m = cut.motion % 4;
  const scale = m === 2 ? 1.14 - prog * 0.05 : 1.06 + prog * 0.05;
  const tx = m === 1 ? -22 + prog * 44 : m === 3 ? 18 - prog * 36 : 0;
  const flicker = 1 - 0.02 * ((Math.sin(born * 0.9) + 1) / 2);
  return (
    <AbsoluteFill style={{ overflow: "hidden", backgroundColor: "#07090B" }}>
      {/* grade (saturate/contrast/brightness) sudah dibakar ke klip oleh
          tools/bake_overlay.py — lihat catatan di sana soal biaya filter CSS */}
      <OffthreadVideo
        src={staticFile(cut.clip)}
        trimBefore={Math.round(cut.offset * D.fps)}
        muted
        style={{
          width: "100%", height: "100%", objectFit: "cover", opacity: flicker,
          transform: `scale(${scale}) translateX(${tx}px)`,
        }}
      />
      <Img
        src={staticFile("overlay/sweep.png")}
        style={{
          position: "absolute", top: 0, left: 0, width: 900, height: H, pointerEvents: "none",
          transform: `translateX(${((born * 3.4) % 2600) - 600}px)`,
        }}
      />
    </AbsoluteFill>
  );
};

/* ─────────────────────── diagram: kartu berfoto ─────────────────────── */

const DiagramScene: React.FC<{ seg: Seg; born: number; durFrames: number }> = ({ seg, born, durFrames }) => {
  const dg = seg.diagram!;
  const n = Math.max(1, dg.cards.length);
  const drift = Math.min(1, born / Math.max(1, durFrames));
  const zIn = 1 + drift * 0.035;
  const isTimeline = dg.style === "timeline";

  // Kartu tidak muncul berbarengan: kemunculannya disebar ke 45% durasi segmen,
  // lalu sorotan bergilir tiap 6 detik supaya diagram 40 detik tetap bergerak
  // bersama narasi (bukan gambar diam yang menunggu VO selesai).
  const totalF = Math.max(1, durFrames);
  const revealSpan = isTimeline
    ? Math.min(4.5 * D.fps, Math.max(30, totalF * 0.4))
    : Math.min(9 * D.fps, Math.max(40, totalF * 0.4));
  const focusEvery = Math.max(4, Math.round((6 * D.fps)));
  const focusIdx = Math.floor(born / focusEvery) % n;

  const cardW = isTimeline ? 470 : 366;
  const cardH = isTimeline ? 358 : 396;
  const gap = isTimeline ? 96 : 64;
  const totalW = n * cardW + (n - 1) * gap;
  const startX = (W - totalW) / 2;
  // kartu harus berhenti di atas blok caption (±780) supaya label kartu tidak
  // tertimpa teks narasi — di 16:9 caption memakai lebar 1040 px di bawah kiri.
  const baseY = isTimeline ? 372 : 352;

  return (
    <AbsoluteFill style={{ backgroundColor: "#080A0C", overflow: "hidden" }}>
      {/* latar: garis tipis seperti kertas grafik + cahaya hangat */}
      <AbsoluteFill style={{ opacity: 0.22 }}>
        {Array.from({ length: 13 }).map((_, i) => (
          <div key={`h${i}`} style={{ position: "absolute", left: 0, right: 0, top: i * 90, height: 1, backgroundColor: C.sage, opacity: 0.13 }} />
        ))}
        {Array.from({ length: 22 }).map((_, i) => (
          <div key={`v${i}`} style={{ position: "absolute", top: 0, bottom: 0, left: i * 90, width: 1, backgroundColor: C.sage, opacity: 0.09 }} />
        ))}
      </AbsoluteFill>
      <AbsoluteFill style={{ background: "radial-gradient(58% 50% at 50% 46%, rgba(196,106,52,0.14) 0%, rgba(8,10,12,0) 68%)" }} />

      {/* judul diagram */}
      <div style={{ position: "absolute", left: MX, top: TOP + 118, opacity: p(born, 4, 26) }}>
        <div style={{ fontFamily: "Inter", fontWeight: 700, fontSize: 19, letterSpacing: "0.32em", color: C.orange }}>
          {dg.kicker || "STRUKTUR"}
        </div>
        <div style={{ fontFamily: "Space Grotesk", fontWeight: 700, fontSize: 52, letterSpacing: "-0.02em", color: C.ivory, marginTop: 8 }}>
          {dg.title || seg.chapter}
        </div>
      </div>

      {/* garis penghubung antar kartu (digambar bertahap) */}
      {!isTimeline ? (
        <svg width={W} height={H} style={{ position: "absolute", inset: 0 }}>
          {dg.cards.slice(1).map((_, k) => {
            const x1 = startX + (k + 1) * cardW + k * gap;
            const x2 = x1 + gap;
            const len = gap;
            const g = p(born, 34 + k * 12, 62 + k * 12, ease);
            return (
              <g key={k}>
                <line x1={x1} y1={baseY + cardH / 2} x2={x1 + len * g} y2={baseY + cardH / 2}
                  stroke={C.orange} strokeWidth={2.4} opacity={0.85} />
                <circle cx={x1 + len * g} cy={baseY + cardH / 2} r={4} fill={C.orange} opacity={g} />
              </g>
            );
          })}
        </svg>
      ) : (
        <svg width={W} height={H} style={{ position: "absolute", inset: 0 }}>
          <line x1={startX} y1={baseY + cardH + 26} x2={startX + totalW} y2={baseY + cardH + 26}
            stroke={C.sage} strokeWidth={2} opacity={0.35 * p(born, 10, 40, ease)} />
        </svg>
      )}

      {/* kartu berisi foto */}
      {dg.cards.map((c, k) => {
        const inAt = 10 + (revealSpan * k) / n;
        const e = p(born, inAt, inAt + 22);
        const focused = k === focusIdx;
        const dim = e * (focused ? 1 : 0.72);
        const rot = (k % 2 === 0 ? -1 : 1) * (2.2 - e * 1.2);
        return (
          <div key={k} style={{
            position: "absolute",
            left: startX + k * (cardW + gap),
            top: baseY,
            width: cardW,
            transform: `translateY(${(1 - e) * 70}px) scale(${0.94 + e * 0.06}) rotate(${rot}deg) scale(${zIn * (focused ? 1.025 : 1)})`,
            opacity: dim,
            transition: "opacity 240ms linear",
          }}>
            <div style={{
              width: cardW, height: cardH, backgroundColor: "#12151A",
              border: focused ? "1px solid rgba(196,106,52,0.95)" : "1px solid rgba(214,222,208,0.28)",
              boxShadow: "0 26px 60px rgba(0,0,0,0.72)",
              overflow: "hidden", position: "relative",
            }}>
              <Img src={staticFile(c.plate)} style={{ width: "100%", height: "100%", objectFit: "cover", filter: "brightness(1.08) saturate(0.95)" }} />
              <AbsoluteFill style={{ background: "linear-gradient(180deg, rgba(6,8,10,0) 30%, rgba(6,8,10,0.80) 58%, rgba(6,8,10,0.97) 78%, rgba(6,8,10,0.99) 100%)" }} />
              <div style={{ position: "absolute", left: 0, right: 0, bottom: 0, height: 132, backgroundColor: "rgba(8,10,12,0.62)", borderTop: "1px solid rgba(196,106,52,0.35)" }} />
              {/* pin kertas */}
              <div style={{
                position: "absolute", left: 18, top: 18, width: 12, height: 12, borderRadius: "50%",
                backgroundColor: C.orange, boxShadow: "0 0 0 4px rgba(8,10,12,0.6)",
                opacity: (focused ? 0.75 : 0.35) + 0.25 * Math.abs(Math.sin(born / 22 + k)),
              }} />
              <div style={{ position: "absolute", left: 22, right: 22, bottom: 22 }}>
                <div style={{ fontFamily: "Inter", fontWeight: 700, fontSize: 15, letterSpacing: "0.26em", color: C.orange, opacity: 0.95, marginBottom: 6 }}>
                  {String(c.num).padStart(2, "0")}
                </div>
                <div style={{ fontFamily: "Space Grotesk", fontWeight: 700, fontSize: isTimeline ? 33 : 28, lineHeight: 1.12, color: C.ivory }}>
                  {c.label}
                </div>
                {c.sub ? (
                  <div style={{ fontFamily: "Inter", fontWeight: 500, fontSize: 18, lineHeight: 1.3, color: "#C3CBB9", marginTop: 6 }}>
                    {c.sub}
                  </div>
                ) : null}
              </div>
            </div>
          </div>
        );
      })}

      <Grain frame={born} />
    </AbsoluteFill>
  );
};

/* ─────────────────────── kartu bab & interstitial ─────────────────────── */

const ChapterCard: React.FC<{ card: Card; born: number; durFrames: number }> = ({ card, born, durFrames }) => {
  const enter = p(born, 0, 15);
  const exit = interpolate(born, [durFrames - 12, durFrames], [0, 1], clamp);
  const typed = Math.max(0, Math.min(card.title.length, Math.floor((born - 14) * 2.1)));
  const rule = p(born, 24, 42, ease);
  return (
    <AbsoluteFill style={{ backgroundColor: "#07090B" }}>
      <AbsoluteFill style={{ background: "radial-gradient(56% 46% at 42% 46%, rgba(196,106,52,0.18) 0%, rgba(7,9,11,0) 64%)" }} />
      <div style={{
        position: "absolute", right: 60, top: 120, fontFamily: "Space Grotesk", fontWeight: 700,
        fontSize: 420, lineHeight: 0.8, color: C.ivory, opacity: 0.05 * enter, letterSpacing: "-0.06em",
      }}>
        {String(card.num || "").padStart(2, "0")}
      </div>

      <div style={{
        position: "absolute", left: 150, top: 330, width: 1010,
        transform: `translateY(${(1 - enter) * 120}px) rotate(${-3.4 + enter * 1.6}deg)`,
        opacity: 1 - exit, filter: "drop-shadow(0 28px 54px rgba(0,0,0,0.8))",
      }}>
        <div style={{
          backgroundColor: "#EDE7D6", padding: "48px 52px 54px",
          clipPath: "polygon(0% 1.6%, 5% 0%, 20% 1.4%, 36% 0%, 54% 1.5%, 70% 0%, 86% 1.3%, 100% 0%, 100% 97%, 90% 100%, 74% 97.8%, 58% 100%, 42% 97.6%, 25% 100%, 9% 97.4%, 0% 100%)",
        }}>
          <div style={{ display: "flex", alignItems: "center", gap: 14, opacity: p(born, 8, 20), marginBottom: 16 }}>
            <div style={{ width: 34, height: 2, backgroundColor: "#B4501F" }} />
            <div style={{ fontFamily: "Inter", fontWeight: 700, fontSize: 19, letterSpacing: "0.26em", color: "#7C6A4F" }}>{card.kicker}</div>
          </div>
          <div style={{ fontFamily: "Space Grotesk", fontWeight: 700, fontSize: card.title.length > 26 ? 60 : 76, lineHeight: 1.04, letterSpacing: "-0.03em", color: "#141210" }}>
            {card.title.slice(0, typed)}
            <span style={{ opacity: born % 16 < 8 ? 0.5 : 0 }}>|</span>
          </div>
          <div style={{ marginTop: 22, height: 4, width: `${rule * 100}%`, maxWidth: 520, backgroundColor: "#B4501F" }} />
          {card.sub ? (
            <div style={{ marginTop: 18, fontFamily: "Inter", fontWeight: 500, fontSize: 23, color: "#5E5445", opacity: rule }}>{card.sub}</div>
          ) : null}
        </div>
      </div>
      <Grain frame={born} />
    </AbsoluteFill>
  );
};

const Interstitial: React.FC<{ card: Card; born: number; durFrames: number }> = ({ card, born, durFrames }) => {
  const draw = p(born, 3, 28, ease);
  const nl = interpolate(born, [26, 44], [-200, 0], { ...clamp, easing: easeOut });
  const nr = interpolate(born, [26, 44], [200, 0], { ...clamp, easing: easeOut });
  const q = p(born, 42, 56);
  const kick = p(born, 50, 66);
  const out = interpolate(born, [durFrames - 10, durFrames], [1, 0], clamp);
  const dash = 1100;
  return (
    <AbsoluteFill style={{ backgroundColor: "#06080A", opacity: out }}>
      <AbsoluteFill style={{ background: "radial-gradient(50% 46% at 50% 50%, rgba(180,80,31,0.16) 0%, rgba(6,8,10,0) 66%)" }} />
      <svg width={W} height={H} style={{ position: "absolute", inset: 0 }}>
        <polygon points={`${W / 2},230 ${W / 2 + 230},620 ${W / 2 - 230},620`} fill="none"
          stroke={C.ivory} strokeWidth={3} strokeDasharray={dash} strokeDashoffset={dash * (1 - draw)} opacity={0.85} />
        <ellipse cx={W / 2} cy={520} rx={66} ry={32} fill="none" stroke={C.orange} strokeWidth={3}
          strokeDasharray={460} strokeDashoffset={460 * (1 - draw)} />
        <circle cx={W / 2} cy={520} r={13} fill={C.orange} opacity={draw * 0.95} />
        <line x1={W / 2 - 250} y1={520 + (draw * 120 - 60)} x2={W / 2 + 250} y2={520 + (draw * 120 - 60)}
          stroke={C.ivory} strokeWidth={1.5} opacity={0.18} />
      </svg>
      <div style={{ position: "absolute", left: 210, top: 300, fontFamily: "Space Grotesk", fontWeight: 700, fontSize: 118, color: C.ivory, opacity: 0.9, transform: `translateX(${nl}px)` }}>1776</div>
      <div style={{ position: "absolute", right: 210, top: 300, fontFamily: "Space Grotesk", fontWeight: 700, fontSize: 118, color: C.ivory, opacity: 0.9, transform: `translateX(${nr}px)` }}>2026</div>
      <div style={{ position: "absolute", left: 0, right: 0, top: 668, textAlign: "center", fontFamily: "Space Grotesk", fontWeight: 700, fontSize: 84, color: C.orange, opacity: q, transform: `scale(${0.75 + q * 0.25})` }}>?</div>
      <div style={{ position: "absolute", left: 0, right: 0, top: 800, textAlign: "center", fontFamily: "Inter", fontWeight: 700, fontSize: 25, letterSpacing: "0.32em", color: C.sage, opacity: kick }}>{card.title}</div>
      <Grain frame={born} />
    </AbsoluteFill>
  );
};

/* ───────────────────────── teks konten ───────────────────────── */

const CAP_W = 1040;

const Caption: React.FC<{ cap: Cap; born: number; hold: number }> = ({ cap, born, hold }) => {
  const frame = useCurrentFrame();
  if (frame < born || frame > born + hold) return null;
  const words = cap.text.split(" ");
  const size = cap.text.length > 66 ? 40 : cap.text.length > 48 ? 44 : 50;
  return (
    <div style={{
      position: "absolute", left: MX, bottom: BOT + 66, width: CAP_W,
      fontFamily: "Inter", fontWeight: 600, fontSize: size, lineHeight: 1.28,
      color: C.ivory, textShadow: "0 3px 22px rgba(0,0,0,0.95)",
    }}>
      {words.map((w, i) => {
        const t0 = born + i * 1.2;
        const e = interpolate(frame, [t0, t0 + 7], [0, 1], clamp);
        return (
          <span key={i} style={{
            display: "inline-block", marginRight: 11, opacity: e,
            transform: `translateY(${(1 - e) * 7}px)`,
            color: /\d/.test(w) ? C.orange : C.ivory,
          }}>{w}</span>
        );
      })}
    </div>
  );
};

const ChapterTag: React.FC<{ text: string; born: number; hold: number }> = ({ text, born, hold }) => {
  const frame = useCurrentFrame();
  if (frame < born || frame > born + hold) return null;
  const e = interpolate(frame, [born, born + 12], [0, 1], clamp);
  const o = interpolate(frame, [born + hold - 10, born + hold], [1, 0], clamp);
  return (
    <div style={{ position: "absolute", left: MX, top: TOP + 6, opacity: e * o, transform: `translateX(${(1 - e) * -12}px)` }}>
      <div style={{ width: 38, height: 2, backgroundColor: C.orange, marginBottom: 12 }} />
      <div style={{ fontFamily: "Inter", fontWeight: 700, fontSize: 21, letterSpacing: "0.26em", color: C.ivory }}>{text}</div>
    </div>
  );
};

/* ─────────────────────────────── root ─────────────────────────────── */

export const LongForm: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = frame / fps;

  const card = D.cards.find((c) => t >= c.start && t < c.end);
  const seg = D.segments.find((s) => t >= s.start && t < s.end);

  const cut = seg?.footage?.find((c) => t >= c.start && t < c.end) ?? seg?.footage?.[seg.footage.length - 1];
  const cap = seg ? seg.captions.find((c) => t >= c.t0 && t < c.t1) ?? null : null;

  const segBorn = seg ? frame - seg.startFrame : 0;
  const cutBorn = cut ? frame - Math.round(cut.start * fps) : 0;
  const flash = cut ? interpolate(cutBorn, [0, 4], [0.14, 0], clamp) : 0;

  return (
    <AbsoluteFill style={{ backgroundColor: C.ink }}>
      <Audio src={staticFile(D.vo)} />

      {card ? (
        card.type === "interstitial" ? (
          <Interstitial card={card} born={frame - Math.round(card.start * fps)} durFrames={Math.round(card.dur * fps)} />
        ) : (
          <ChapterCard card={card} born={frame - Math.round(card.start * fps)} durFrames={Math.round(card.dur * fps)} />
        )
      ) : null}

      {seg && seg.layout === "diagram" && seg.diagram ? (
        <>
          <DiagramScene seg={seg} born={segBorn} durFrames={seg.endFrame - seg.startFrame} />
          <AbsoluteFill style={{ background: "linear-gradient(180deg, rgba(8,10,12,0.72) 0%, rgba(8,10,12,0.12) 16%, rgba(8,10,12,0) 38%, rgba(8,10,12,0.55) 74%, rgba(8,10,12,0.95) 100%)", pointerEvents: "none" }} />
          <ChapterTag text={seg.chapter} born={seg.startFrame} hold={Math.round(2.2 * fps)} />
          {cap ? <Caption cap={cap} born={Math.round(cap.t0 * fps)} hold={Math.max(1, Math.round((cap.t1 - cap.t0) * fps))} /> : null}
        </>
      ) : null}

      {seg && seg.layout === "footage" && cut ? (
        <>
          <Footage cut={cut} born={cutBorn} durFrames={Math.max(1, Math.round((cut.end - cut.start) * fps))} />
          <Scrim />
          <ChapterTag text={seg.chapter} born={seg.startFrame} hold={Math.round(2.2 * fps)} />
          {cap ? <Caption cap={cap} born={Math.round(cap.t0 * fps)} hold={Math.max(1, Math.round((cap.t1 - cap.t0) * fps))} /> : null}
          {flash > 0.002 ? <AbsoluteFill style={{ backgroundColor: C.ivory, opacity: flash, pointerEvents: "none" }} /> : null}
        </>
      ) : null}

      {/* identitas kanal + progres */}
      {!card ? (
        <div style={{ position: "absolute", right: MX, top: TOP + 6, textAlign: "right" }}>
          <div style={{ fontFamily: "Space Grotesk", fontWeight: 700, fontSize: 24, letterSpacing: "0.34em", color: C.ivory, opacity: 0.92 }}>ODDCHAPTER</div>
          <div style={{ fontFamily: "Inter", fontWeight: 600, fontSize: 17, letterSpacing: "0.24em", color: C.sage, marginTop: 8, opacity: 0.8 }}>
            {D.series} · {D.id} · {String(seg ? seg.i + 1 : 0).padStart(2, "0")}/{D.segments.length}
          </div>
        </div>
      ) : null}

      <div style={{ position: "absolute", left: 0, right: 0, bottom: 0, height: 5, backgroundColor: "rgba(214,222,208,0.14)" }}>
        <div style={{ width: `${Math.min(1, frame / D.totalFrames) * 100}%`, height: "100%", backgroundColor: C.orange }} />
      </div>
    </AbsoluteFill>
  );
};
