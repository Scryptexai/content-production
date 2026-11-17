import React from "react";
import { AbsoluteFill, Audio, Easing, Img, interpolate, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import data from "../longform.generated.json";
import { C, H, MARGIN, W } from "../theme";

/**
 * LongForm — episode panjang dari VO pemilik, versi 2 (berjeda).
 *
 * Keluhan pemilik atas v1: "terasa seperti baca koran tanpa jeda". Karena itu
 * narasi sekarang DIPOTONG di keheningan (`build_longform.py`) dan di antara
 * potongan ada:
 *   · kartu bab  — secarik kertas masuk, judul diketik, sfx kertas, VO diam
 *   · interstitial — di detik ±15: ikon digambar, dua tahun beradu, tanda tanya
 *
 * Yang membuat gambar terasa hidup (bukan foto diam):
 *   1. lima preset gerak kamera (push-in, drift, push-out+rotasi, sweep, handheld)
 *   2. lapisan debu yang naik pelan, deterministik per frame
 *   3. kilau cahaya menyapu plate + flicker proyektor ±2%
 *   4. caption muncul per kata, angka/tahun diberi warna oranye
 *   5. kedip 3 frame tiap ganti plate, dan scrim atas-bawah supaya teks aman
 */

type Cut = { plate: string; fit: "cover" | "contain"; start: number; end: number; motion: number };
type Cap = { t0: number; t1: number; text: string };
type Seg = {
  i: number; chapter: string; start: number; end: number;
  startFrame: number; endFrame: number; plates: Cut[]; captions: Cap[];
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
const ease = Easing.bezier(0.2, 0.7, 0.2, 1);
const easeOut = Easing.bezier(0.16, 1, 0.3, 1);
const clamp = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;

/* ─────────────────────────── lapisan hidup ─────────────────────────── */

const Dust: React.FC<{ frame: number; dense?: number }> = ({ frame, dense = 14 }) => (
  <AbsoluteFill style={{ pointerEvents: "none" }}>
    {Array.from({ length: dense }).map((_, i) => {
      const x = ((i * 137 + frame * 0.55) % 1080);
      const y = 1920 - (((frame * 1.1 + i * 211) % 2100));
      const r = 1 + ((i * 7) % 3) * 0.6;
      return (
        <div
          key={i}
          style={{
            position: "absolute", left: x, top: y, width: r, height: r, borderRadius: "50%",
            backgroundColor: C.ivory, opacity: 0.05 + ((i % 4) * 0.035),
          }}
        />
      );
    })}
  </AbsoluteFill>
);

const Scrims: React.FC = () => (
  <>
    <AbsoluteFill
      style={{
        background:
          "linear-gradient(180deg, rgba(8,10,12,0.86) 0%, rgba(8,10,12,0.35) 12%, rgba(8,10,12,0.05) 26%, rgba(8,10,12,0.06) 48%, rgba(8,10,12,0.78) 80%, rgba(8,10,12,0.97) 100%)",
        pointerEvents: "none",
      }}
    />
    <AbsoluteFill
      style={{
        background: "radial-gradient(76% 52% at 50% 46%, rgba(0,0,0,0) 44%, rgba(0,0,0,0.72) 100%)",
        pointerEvents: "none",
      }}
    />
  </>
);

/* ───────────────────────────── plate ───────────────────────────── */

const Plate: React.FC<{ cut: Cut; born: number; durFrames: number }> = ({ cut, born, durFrames }) => {
  const p = Math.min(1, Math.max(0, born / Math.max(1, durFrames)));
  const m = cut.motion % 5;
  let scale = 1.05 + p * 0.07;
  let x = 0, y = 0, rot = 0;
  if (m === 1) { scale = 1.11 - p * 0.04; x = -34 + p * 68; }
  if (m === 2) { scale = 1.17 - p * 0.09; rot = -0.7 + p * 1.1; }
  if (m === 3) { scale = 1.09; x = 26 - p * 52; }
  if (m === 4) {
    scale = 1.06 + p * 0.09;
    x = Math.sin(born / 9) * 5;
    y = Math.cos(born / 7) * 4;
  }
  const sweep = ((born * 3.2) % 2600) - 500;
  const flicker = 1 - 0.022 * ((Math.sin(born * 0.83) + 1) / 2);

  if (cut.fit === "contain") {
    return (
      <AbsoluteFill style={{ backgroundColor: "#080A0C" }}>
        <div
          style={{
            position: "absolute", left: MARGIN, right: MARGIN, top: 300, height: 780,
            display: "flex", alignItems: "center", justifyContent: "center",
            transform: `scale(${scale}) translate(${x / 3}px, ${y / 3}px) rotate(${rot / 2}deg)`,
          }}
        >
          <Img src={staticFile(cut.plate)} style={{ maxWidth: "100%", maxHeight: "100%", objectFit: "contain", border: "1px solid rgba(214,222,208,0.22)" }} />
        </div>
        <div style={{ position: "absolute", left: MARGIN, top: 258, fontFamily: "Inter", fontWeight: 600, fontSize: 20, letterSpacing: "0.3em", color: C.sage, opacity: 0.7 }}>
          ARSIP
        </div>
        <AbsoluteFill style={{ background: "radial-gradient(72% 46% at 50% 40%, rgba(0,0,0,0) 40%, rgba(0,0,0,0.8) 100%)", pointerEvents: "none" }} />
        <Dust frame={born} dense={9} />
      </AbsoluteFill>
    );
  }

  return (
    <AbsoluteFill style={{ overflow: "hidden" }}>
      <Img
        src={staticFile(cut.plate)}
        style={{
          width: "100%", height: "100%", objectFit: "cover",
          transform: `scale(${scale}) translate(${x}px, ${y}px) rotate(${rot}deg)`,
          opacity: flicker,
        }}
      />
      {/* kilau menyapu: satu pita diagonal yang bergerak, bukan gradient statis */}
      <AbsoluteFill
        style={{
          background: "linear-gradient(102deg, rgba(255,248,230,0) 42%, rgba(255,248,230,0.11) 50%, rgba(255,248,230,0) 58%)",
          transform: `translateX(${sweep}px)`,
          pointerEvents: "none",
        }}
      />
      <Dust frame={born} />
    </AbsoluteFill>
  );
};

/* ───────────────────────────── kartu ───────────────────────────── */

const ChapterCard: React.FC<{ card: Card; born: number; durFrames: number }> = ({ card, born, durFrames }) => {
  const enter = interpolate(born, [0, 14], [0, 1], { ...clamp, easing: easeOut });
  const exit = interpolate(born, [durFrames - 12, durFrames], [0, 1], clamp);
  const paperY = interpolate(enter, [0, 1], [230, 0]);
  const paperRot = interpolate(enter, [0, 1], [-4.5, -1.6]);
  const kicker = interpolate(born, [8, 20], [0, 1], clamp);
  const typed = Math.max(0, Math.min(card.title.length, Math.floor((born - 16) * 1.9)));
  const rule = interpolate(born, [26, 44], [0, 1], { ...clamp, easing: ease });
  const numP = interpolate(born, [10, 30], [0, 1], { ...clamp, easing: ease });

  return (
    <AbsoluteFill style={{ backgroundColor: "#07090B" }}>
      <AbsoluteFill style={{ background: "radial-gradient(70% 46% at 50% 42%, rgba(196,106,52,0.16) 0%, rgba(7,9,11,0) 62%)" }} />
      <div style={{ position: "absolute", right: -40, top: 210, fontFamily: "Space Grotesk", fontWeight: 700, fontSize: 420, lineHeight: 0.8, color: C.ivory, opacity: 0.05 * numP, letterSpacing: "-0.06em" }}>
        {String(card.num || "").padStart(2, "0")}
      </div>

      <div
        style={{
          position: "absolute", left: MARGIN - 10, right: MARGIN - 10, top: 560,
          transform: `translateY(${paperY}px) rotate(${paperRot}deg)`,
          opacity: 1 - exit,
          filter: "drop-shadow(0 30px 60px rgba(0,0,0,0.75))",
        }}
      >
        <div
          style={{
            backgroundColor: "#EDE7D6", padding: "54px 44px 60px",
            clipPath:
              "polygon(0% 2%, 4% 0%, 18% 1.5%, 33% 0%, 52% 1.6%, 68% 0%, 85% 1.4%, 100% 0%, 100% 96%, 92% 100%, 76% 97.6%, 60% 100%, 44% 97.4%, 26% 100%, 10% 97.6%, 0% 100%)",
          }}
        >
          <div style={{ display: "flex", alignItems: "center", gap: 14, opacity: kicker, marginBottom: 18 }}>
            <div style={{ width: 34, height: 2, backgroundColor: "#B4501F" }} />
            <div style={{ fontFamily: "Inter", fontWeight: 700, fontSize: 20, letterSpacing: "0.26em", color: "#7C6A4F" }}>
              {card.kicker}
            </div>
          </div>
          <div style={{ fontFamily: "Space Grotesk", fontWeight: 700, fontSize: card.title.length > 26 ? 62 : 76, lineHeight: 1.02, letterSpacing: "-0.03em", color: "#141210" }}>
            {card.title.slice(0, typed)}
            <span style={{ opacity: born % 16 < 8 ? 0.55 : 0 }}>|</span>
          </div>
          <div style={{ marginTop: 26, height: 4, width: `${rule * 100}%`, maxWidth: 420, backgroundColor: "#B4501F" }} />
          {card.sub ? (
            <div style={{ marginTop: 22, fontFamily: "Inter", fontWeight: 500, fontSize: 24, letterSpacing: "0.02em", color: "#5E5445", opacity: rule }}>
              {card.sub}
            </div>
          ) : null}
        </div>
      </div>

      <div style={{ position: "absolute", left: MARGIN, right: MARGIN, top: 1660, opacity: 0.9 }}>
        <div style={{ height: 1, backgroundColor: C.sage, opacity: 0.3, marginBottom: 18 }} />
        <div style={{ display: "flex", justifyContent: "space-between" }}>
          <div style={{ fontFamily: "Space Grotesk", fontWeight: 700, fontSize: 26, letterSpacing: "0.34em", color: C.ivory }}>ODDCHAPTER</div>
          <div style={{ fontFamily: "Inter", fontWeight: 600, fontSize: 20, letterSpacing: "0.24em", color: C.sage }}>{D.series} · {D.id}</div>
        </div>
      </div>
      <Dust frame={born} dense={10} />
    </AbsoluteFill>
  );
};

const Interstitial: React.FC<{ card: Card; born: number; durFrames: number }> = ({ card, born, durFrames }) => {
  const draw = interpolate(born, [4, 30], [0, 1], { ...clamp, easing: ease });
  const scan = interpolate(born, [26, 44], [-160, 160], clamp);
  const numL = interpolate(born, [30, 48], [-260, 0], { ...clamp, easing: easeOut });
  const numR = interpolate(born, [30, 48], [260, 0], { ...clamp, easing: easeOut });
  const q = interpolate(born, [46, 60], [0, 1], { ...clamp, easing: easeOut });
  const kick = interpolate(born, [54, 70], [0, 1], clamp);
  const out = interpolate(born, [durFrames - 10, durFrames], [1, 0], clamp);
  const dash = 1200;

  return (
    <AbsoluteFill style={{ backgroundColor: "#06080A", opacity: out }}>
      <AbsoluteFill style={{ background: "radial-gradient(60% 40% at 50% 44%, rgba(180,80,31,0.14) 0%, rgba(6,8,10,0) 66%)" }} />
      <div style={{ position: "absolute", left: 0, right: 0, top: 760, height: 300, display: "flex", alignItems: "center", justifyContent: "center" }}>
        <svg width={520} height={420} viewBox="0 0 520 420">
          <polygon points="260,30 500,390 20,390" fill="none" stroke={C.ivory} strokeWidth={3} strokeDasharray={dash} strokeDashoffset={dash * (1 - draw)} opacity={0.85} />
          <ellipse cx={260} cy={300} rx={76} ry={38} fill="none" stroke={C.orange} strokeWidth={3} strokeDasharray={500} strokeDashoffset={500 * (1 - draw)} opacity={0.9} />
          <circle cx={260} cy={300} r={15} fill={C.orange} opacity={draw * 0.9} />
          <line x1={40} y1={300 + scan} x2={480} y2={300 + scan} stroke={C.ivory} strokeWidth={1.5} opacity={0.25 * (1 - Math.abs(scan) / 200)} />
        </svg>
      </div>

      <div style={{ position: "absolute", left: MARGIN, top: 500, fontFamily: "Space Grotesk", fontWeight: 700, fontSize: 132, color: C.ivory, opacity: 0.92, transform: `translateX(${numL}px)` }}>1776</div>
      <div style={{ position: "absolute", right: MARGIN, top: 500, fontFamily: "Space Grotesk", fontWeight: 700, fontSize: 132, color: C.ivory, opacity: 0.92, transform: `translateX(${numR}px)` }}>2026</div>
      <div style={{ position: "absolute", left: 0, right: 0, top: 1330, textAlign: "center", fontFamily: "Space Grotesk", fontWeight: 700, fontSize: 96, color: C.orange, opacity: q, transform: `scale(${0.7 + q * 0.3})` }}>?</div>
      <div style={{ position: "absolute", left: MARGIN, right: MARGIN, top: 1470, textAlign: "center", fontFamily: "Inter", fontWeight: 700, fontSize: 26, letterSpacing: "0.3em", color: C.sage, opacity: kick }}>
        {card.title}
      </div>
      <Dust frame={born} dense={16} />
    </AbsoluteFill>
  );
};

/* ─────────────────────────── teks konten ─────────────────────────── */

const CaptionLine: React.FC<{ cap: Cap; born: number; hold: number }> = ({ cap, born, hold }) => {
  const frame = useCurrentFrame();
  if (frame < born || frame > born + hold) return null;
  const words = cap.text.split(" ");
  const size = cap.text.length > 58 ? 46 : cap.text.length > 40 ? 52 : 58;
  return (
    <div style={{ position: "absolute", left: MARGIN, width: W - MARGIN * 2, bottom: 400, fontFamily: "Inter", fontWeight: 600, fontSize: size, lineHeight: 1.3, letterSpacing: "0.004em", color: C.ivory, textShadow: "0 3px 26px rgba(0,0,0,0.95)" }}>
      {words.map((w, i) => {
        const t0 = born + i * 1.3;
        const p = interpolate(frame, [t0, t0 + 7], [0, 1], clamp);
        const isNum = /\d/.test(w);
        const scale = 1 + (1 - p) * 0.06;
        return (
          <span key={i} style={{ display: "inline-block", marginRight: 13, opacity: p, transform: `translateY(${(1 - p) * 8}px) scale(${scale})`, color: isNum ? C.orange : C.ivory }}>
            {w}
          </span>
        );
      })}
    </div>
  );
};

const ChapterTag: React.FC<{ text: string; born: number; hold: number }> = ({ text, born, hold }) => {
  const frame = useCurrentFrame();
  if (frame < born || frame > born + hold) return null;
  const p = interpolate(frame, [born, born + 12], [0, 1], clamp);
  const out = interpolate(frame, [born + hold - 10, born + hold], [1, 0], clamp);
  return (
    <div style={{ position: "absolute", left: MARGIN, top: 236, opacity: p * out, transform: `translateX(${(1 - p) * -14}px)` }}>
      <div style={{ width: 40, height: 2, backgroundColor: C.orange, marginBottom: 14 }} />
      <div style={{ fontFamily: "Inter", fontWeight: 700, fontSize: 24, letterSpacing: "0.24em", color: C.ivory }}>{text}</div>
    </div>
  );
};

const Progress: React.FC<{ frame: number; total: number }> = ({ frame, total }) => (
  <div style={{ position: "absolute", left: 0, right: 0, bottom: 0, height: 6, backgroundColor: "rgba(214,222,208,0.16)" }}>
    <div style={{ width: `${Math.min(1, frame / total) * 100}%`, height: "100%", backgroundColor: C.orange }} />
  </div>
);

/* ─────────────────────────────── root ─────────────────────────────── */

export const LongForm: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = frame / fps;

  const card = D.cards.find((c) => t >= c.start && t < c.end);
  const seg = D.segments.find((s) => t >= s.start && t < s.end);

  const content = !card && seg ? seg : null;
  const cut = content ? (content.plates.find((c) => t >= c.start && t < c.end) ?? content.plates[content.plates.length - 1]) : null;
  const cutStart = cut ? Math.round(cut.start * fps) : 0;
  const cutDur = cut ? Math.max(1, Math.round((cut.end - cut.start) * fps)) : 1;
  const cap = content ? (content.captions.find((c) => t >= c.t0 && t < c.t1) ?? null) : null;
  const flash = content ? interpolate(frame - cutStart, [0, 4], [0.16, 0], clamp) : 0;

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

      {content && cut ? (
        <>
          <Plate cut={cut} born={frame - cutStart} durFrames={cutDur} />
          <Scrims />
          <ChapterTag text={content.chapter} born={content.startFrame} hold={Math.round(2.4 * fps)} />
          {cap ? <CaptionLine cap={cap} born={Math.round(cap.t0 * fps)} hold={Math.max(1, Math.round((cap.t1 - cap.t0) * fps))} /> : null}
          {flash > 0.002 ? <AbsoluteFill style={{ backgroundColor: C.ivory, opacity: flash, pointerEvents: "none" }} /> : null}
          <div style={{ position: "absolute", left: MARGIN, top: 150, fontFamily: "Inter", fontWeight: 600, fontSize: 21, letterSpacing: "0.26em", color: C.sage, opacity: 0.8 }}>
            {String(content.i + 1).padStart(2, "0")} / 17 · {D.title}
          </div>
          <div style={{ position: "absolute", left: MARGIN, right: MARGIN, top: 1660 }}>
            <div style={{ height: 1, backgroundColor: C.sage, opacity: 0.3, marginBottom: 18 }} />
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "baseline" }}>
              <div style={{ fontFamily: "Space Grotesk", fontWeight: 700, fontSize: 26, letterSpacing: "0.34em", color: C.ivory }}>ODDCHAPTER</div>
              <div style={{ fontFamily: "Inter", fontWeight: 600, fontSize: 20, letterSpacing: "0.24em", color: C.sage }}>{D.series} · {D.id}</div>
            </div>
          </div>
        </>
      ) : null}

      <Progress frame={frame} total={D.totalFrames} />
    </AbsoluteFill>
  );
};
