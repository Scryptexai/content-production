import React from "react";
import { AbsoluteFill, Audio, Easing, interpolate, staticFile, useCurrentFrame } from "remotion";
import { C, H, W } from "../theme";

/**
 * AK-EP12 pre-production visual proof.
 *
 * Every visible element is native Remotion SVG/CSS/data motion — no stock image,
 * likeness, casualty image, or reconstruction treated as documentary footage.
 * The reviewed local renderer script supplies the approved C VO at the static path
 * below; no external media, likeness, or reconstruction is introduced.
 */
// 41.36 s is the measured, approved-C Indonesian VO. Nineteen frames keep a
// 0.64 s visual closing hold, so the silent planning composition is 42.0 s.
export const AK_EP12_PREPROD_FRAMES = 1260; // 42 s at 30 fps

const ease = Easing.bezier(0.2, 0.7, 0.2, 1);
const clamp = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;

const inScene = (frame: number, from: number, until: number, edge = 10) => {
  if (frame < from || frame >= until) return 0;
  const inn = interpolate(frame, [from, from + edge], [0, 1], { ...clamp, easing: ease });
  const out = interpolate(frame, [until - edge, until], [1, 0], { ...clamp, easing: ease });
  return Math.min(inn, out);
};

const rise = (frame: number, from: number, amount = 36) => {
  const p = interpolate(frame, [from, from + 18], [0, 1], { ...clamp, easing: ease });
  return { opacity: p, transform: `translateY(${(1 - p) * amount}px)` };
};

const Label: React.FC<{ children: React.ReactNode; top?: number; color?: string }> = ({ children, top = 110, color = C.orange }) => (
  <div
    style={{
      position: "absolute",
      top,
      left: 62,
      color,
      fontFamily: "Inter",
      fontWeight: 800,
      letterSpacing: "0.14em",
      fontSize: 25,
      textTransform: "uppercase",
    }}
  >
    {children}
  </div>
);

const Footer: React.FC<{ source: string }> = ({ source }) => (
  <div
    style={{
      position: "absolute",
      left: 62,
      right: 62,
      bottom: 52,
      borderTop: "1px solid rgba(240,236,224,.24)",
      paddingTop: 16,
      display: "flex",
      justifyContent: "space-between",
      color: "rgba(240,236,224,.72)",
      fontFamily: "Inter",
      fontWeight: 700,
      fontSize: 18,
      letterSpacing: "0.09em",
    }}
  >
    <span>ODDCHAPTER · AK-EP12</span>
    <span>{source}</span>
  </div>
);

/** Moving ledger grid and deterministic person-data dots, never human likenesses. */
const DataField: React.FC<{ density?: number; danger?: boolean }> = ({ density = 50, danger = false }) => {
  const frame = useCurrentFrame();
  const shift = (frame * 0.42) % 96;
  return (
    <AbsoluteFill style={{ overflow: "hidden", background: C.ink }}>
      <div
        style={{
          position: "absolute",
          inset: 0,
          opacity: 0.24,
          background:
            `repeating-linear-gradient(90deg, transparent 0 95px, rgba(198,206,190,.24) 96px), ` +
            `repeating-linear-gradient(0deg, transparent 0 95px, rgba(198,206,190,.18) 96px)`,
          transform: `translate(${-shift}px, ${shift * 0.3}px)`,
        }}
      />
      {Array.from({ length: density }, (_, i) => {
        const x = 80 + ((i * 151) % 920) + Math.sin(frame / 25 + i) * 10;
        const y = 280 + ((i * 113) % 1240) + Math.cos(frame / 32 + i * 1.7) * 13;
        const r = 4 + (i % 4) * 2;
        return <div key={i} style={{ position: "absolute", left: x, top: y, width: r * 2, height: r * 2, borderRadius: 99, background: danger && i % 7 === 0 ? C.orange : C.sage, opacity: 0.13 + (i % 5) * 0.06 }} />;
      })}
      <div style={{ position: "absolute", inset: 0, background: "linear-gradient(180deg, rgba(8,10,12,.1), rgba(8,10,12,.74))" }} />
    </AbsoluteFill>
  );
};

const BigNumber: React.FC<{ number: string; caption: string; from: number; accent?: boolean }> = ({ number, caption, from, accent = false }) => {
  const frame = useCurrentFrame();
  const p = interpolate(frame, [from, from + 22], [0, 1], { ...clamp, easing: ease });
  const pulse = 1 + 0.025 * Math.sin(frame / 8);
  return (
    <div style={{ position: "absolute", left: 60, right: 60, top: 510, ...rise(frame, from, 80) }}>
      <div style={{ fontFamily: "Space Grotesk", fontWeight: 700, fontSize: 330, letterSpacing: "-0.105em", color: accent ? C.orange : C.ivory, lineHeight: 0.76, transform: `scale(${(0.86 + p * 0.14) * pulse})`, transformOrigin: "left center" }}>
        {number}
      </div>
      <div style={{ marginTop: 62, fontFamily: "Inter", fontWeight: 800, fontSize: 29, letterSpacing: "0.14em", color: C.sage, textTransform: "uppercase" }}>{caption}</div>
    </div>
  );
};

const RouteMap: React.FC<{ from: number }> = ({ from }) => {
  const frame = useCurrentFrame();
  const p = interpolate(frame, [from + 12, from + 75], [0, 1], { ...clamp, easing: ease });
  const boatX = 170 + p * 720;
  return (
    <svg width={W} height={H} viewBox={`0 0 ${W} ${H}`} style={{ position: "absolute", inset: 0 }}>
      <path d="M130 1170 C350 1020 638 1260 930 1050" fill="none" stroke="rgba(198,206,190,.28)" strokeWidth="4" strokeDasharray="13 18" />
      <path d="M130 1170 C350 1020 638 1260 930 1050" fill="none" stroke={C.sage} strokeWidth="5" strokeDasharray="850" strokeDashoffset={850 * (1 - p)} />
      <circle cx="130" cy="1170" r="15" fill={C.orange} />
      <circle cx="930" cy="1050" r="15" fill={C.sage} />
      <text x="130" y="1230" fill={C.ivory} fontFamily="Inter" fontSize="24" fontWeight="800" letterSpacing="3">SIMANINDO</text>
      <text x="730" y="1110" fill={C.ivory} fontFamily="Inter" fontSize="24" fontWeight="800" letterSpacing="3">TIGARAS</text>
      <g transform={`translate(${boatX} ${1145 + Math.sin(frame / 8) * 11}) rotate(${Math.sin(frame / 11) * 5})`}>
        <path d="M-35 12 H35 L18 34 H-20 Z" fill={C.ivory} />
        <path d="M-4 12 V-34 L19 12 Z" fill={C.orange} />
      </g>
    </svg>
  );
};

const Timeline: React.FC<{ from: number }> = ({ from }) => {
  const frame = useCurrentFrame();
  const p = interpolate(frame, [from + 5, from + 90], [0, 1], { ...clamp, easing: ease });
  const x = 120 + p * 840;
  return (
    <svg width={W} height={H} viewBox={`0 0 ${W} ${H}`} style={{ position: "absolute", inset: 0 }}>
      <line x1="120" x2="960" y1="940" y2="940" stroke="rgba(240,236,224,.42)" strokeWidth="3" />
      <line x1="120" x2={x} y1="940" y2="940" stroke={C.orange} strokeWidth="11" />
      <circle cx={x} cy="940" r="20" fill={C.orange} />
      <text x="116" y="860" fill={C.ivory} fontFamily="Space Grotesk" fontSize="102" fontWeight="700">16.50</text>
      <text x="686" y="860" fill={C.ivory} fontFamily="Space Grotesk" fontSize="102" fontWeight="700" opacity={p}>17.10</text>
      <text x="120" y="1010" fill={C.sage} fontFamily="Inter" fontSize="25" fontWeight="800" letterSpacing="4">BERANGKAT</text>
      <text x="687" y="1010" fill={C.orange} fontFamily="Inter" fontSize="25" fontWeight="800" letterSpacing="4" opacity={p}>TERBALIK</text>
    </svg>
  );
};

const WaveAndHull: React.FC<{ from: number }> = ({ from }) => {
  const frame = useCurrentFrame();
  const p = interpolate(frame, [from + 8, from + 80], [0, 1], { ...clamp, easing: ease });
  const tilt = interpolate(frame, [from + 38, from + 118], [0, 42], clamp);
  const waveX = -1180 + p * 1400;
  return (
    <svg width={W} height={H} viewBox={`0 0 ${W} ${H}`} style={{ position: "absolute", inset: 0 }}>
      {Array.from({ length: 7 }, (_, i) => {
        const y = 1170 + i * 75;
        return <path key={i} d={`M${waveX - i * 70} ${y} Q ${waveX + 170} ${y - 74} ${waveX + 340} ${y} T ${waveX + 680} ${y} T ${waveX + 1020} ${y}`} fill="none" stroke={i === 1 ? C.orange : "#6da7ad"} strokeWidth={i === 1 ? 11 : 4} opacity={0.22 + i * 0.06} />;
      })}
      <g transform={`translate(540 1080) rotate(${tilt})`}>
        <path d="M-245 42 H250 L166 156 H-184 Z" fill="#e6eee9" />
        <path d="M-118 42 V-130 H112 V42" fill="none" stroke="#e6eee9" strokeWidth="16" />
        <path d="M-42 -130 V-250 H54 V-130" fill="none" stroke={C.orange} strokeWidth="13" />
      </g>
    </svg>
  );
};

const CountCards: React.FC<{ from: number }> = ({ from }) => {
  const frame = useCurrentFrame();
  const p = interpolate(frame, [from + 15, from + 52], [0, 1], { ...clamp, easing: ease });
  const second = interpolate(frame, [from + 70, from + 105], [0, 1], { ...clamp, easing: ease });
  const small = [
    ["21", "SELAMAT", C.sage],
    ["3", "MENINGGAL", C.ivory],
    ["164", "HILANG", C.orange],
  ] as const;
  return (
    <>
      <div style={{ position: "absolute", top: 430, left: 62, right: 62, display: "flex", justifyContent: "space-between", alignItems: "center", opacity: p }}>
        <div style={{ fontFamily: "Space Grotesk", fontWeight: 700, fontSize: 205, color: C.ivory, letterSpacing: "-0.09em" }}>45</div>
        <div style={{ width: 180, height: 4, background: C.orange, transform: `scaleX(${p})`, transformOrigin: "left" }} />
        <div style={{ fontFamily: "Space Grotesk", fontWeight: 700, fontSize: 205, color: C.orange, letterSpacing: "-0.09em" }}>188</div>
      </div>
      <div style={{ position: "absolute", top: 650, left: 70, right: 70, display: "flex", gap: 14, opacity: second, transform: `translateY(${(1 - second) * 40}px)` }}>
        {small.map(([number, label, color], i) => (
          <div key={number} style={{ flex: 1, height: 250, border: `2px solid ${color}`, padding: 24, background: "rgba(8,10,12,.66)", transform: `translateY(${Math.sin(frame / 9 + i) * 7}px)` }}>
            <div style={{ fontFamily: "Space Grotesk", fontWeight: 700, fontSize: number === "164" ? 92 : 112, letterSpacing: "-0.08em", color }}>{number}</div>
            <div style={{ marginTop: 28, fontFamily: "Inter", fontWeight: 800, fontSize: 18, letterSpacing: "0.12em", color: C.ivory }}>{label}</div>
          </div>
        ))}
      </div>
    </>
  );
};

const ManifestPage: React.FC<{ from: number }> = ({ from }) => {
  const frame = useCurrentFrame();
  const p = interpolate(frame, [from + 5, from + 42], [0, 1], { ...clamp, easing: ease });
  const sweep = ((frame - from) % 85) / 85;
  return (
    <div style={{ position: "absolute", left: 84, right: 84, top: 400, height: 760, background: C.ivory, color: C.ink, opacity: p, transform: `rotate(${(1 - p) * -8}deg) translateY(${(1 - p) * 70}px)`, overflow: "hidden", boxShadow: "0 30px 80px rgba(0,0,0,.42)" }}>
      <div style={{ padding: "56px 52px", fontFamily: "Inter", fontWeight: 800, fontSize: 24, letterSpacing: "0.13em" }}>REKOMENDASI KESELAMATAN</div>
      <div style={{ margin: "0 52px", height: 4, background: C.orange }} />
      {["MANIFEST", "SEBELUM", "BERANGKAT"].map((line, i) => <div key={line} style={{ margin: "37px 52px 0", fontFamily: "Space Grotesk", fontWeight: 700, fontSize: 92, lineHeight: 0.88, letterSpacing: "-0.07em", opacity: interpolate(frame, [from + 18 + i * 8, from + 38 + i * 8], [0, 1], clamp) }}>{line}</div>)}
      <div style={{ position: "absolute", top: sweep * 760 - 140, left: 0, right: 0, height: 140, background: "linear-gradient(180deg, transparent, rgba(198,102,42,.24), transparent)" }} />
    </div>
  );
};

/**
 * Review-only data-motion composition. The owner separately approved one local
 * Remotion review render with the measured C VO; it is not an approved public
 * master and must not be transferred, queued, scheduled, uploaded, or published.
 */
export const SinarBangunPreprod: React.FC = () => {
  const frame = useCurrentFrame();
  // Measured-C cue layout (30 fps), followed by a 19-frame visual hold:
  // 5.30 / 2.90 / 3.60 / 4.10 / 5.00 / 9.27 / 3.50 / 3.80 / 4.53 seconds.
  const scenes = [
    [0, 159], [159, 246], [246, 354], [354, 477], [477, 627],
    [627, 905], [905, 1010], [1010, 1124], [1124, AK_EP12_PREPROD_FRAMES],
  ] as const;
  return (
    <AbsoluteFill style={{ overflow: "hidden", background: C.ink }}>
      <Audio src={staticFile("audio/ak-ep12-sinar-bangun-review.wav")} />
      <DataField density={56} danger={frame >= 477 && frame < 627} />

      <AbsoluteFill style={{ opacity: inScene(frame, ...scenes[0]) }}>
        <Label>Danau Toba · data posko</Label>
        <BigNumber number="188" caption="VERIFIKASI HARI KE-9 · BUKAN MANIFEST" from={12} accent />
        <Footer source="KNKT I.2.2" />
      </AbsoluteFill>

      <AbsoluteFill style={{ opacity: inScene(frame, ...scenes[1]) }}>
        <Label>Angka yang datang terlambat</Label>
        <RouteMap from={159} />
        <div style={{ position: "absolute", left: 62, right: 62, top: 330, ...rise(frame, 177) }}>
          <div style={{ fontFamily: "Space Grotesk", fontWeight: 700, fontSize: 101, lineHeight: 0.88, letterSpacing: "-0.075em", color: C.ivory }}>KAPAN ANGKA INI ADA?</div>
          <div style={{ marginTop: 36, fontFamily: "Inter", fontWeight: 700, fontSize: 25, letterSpacing: "0.12em", color: C.sage }}>SIMANINDO → TIGARAS</div>
        </div>
        <Footer source="KNKT I.1" />
      </AbsoluteFill>

      <AbsoluteFill style={{ opacity: inScene(frame, ...scenes[2]) }}>
        <Label>Dermaga · sebelum berangkat</Label>
        {Array.from({ length: 23 }, (_, i) => {
          const x = 120 + (i % 6) * 152;
          const y = 620 + Math.floor(i / 6) * 128;
          const lift = Math.max(0, frame - 266 - i * 2) * -1.6;
          return <div key={i} style={{ position: "absolute", left: x, top: y + lift, width: 58, height: 58, borderRadius: 99, border: `3px solid ${i > 17 ? C.orange : C.sage}`, opacity: 0.48 + (i % 3) * 0.14 }} />;
        })}
        <div style={{ position: "absolute", top: 1318, left: 62, right: 62, fontFamily: "Space Grotesk", fontWeight: 700, fontSize: 78, lineHeight: 0.9, letterSpacing: "-0.07em", color: C.ivory, ...rise(frame, 271) }}>KITA KIRA 188<br />DIHITUNG DI DERMAGA.</div>
        <Footer source="KNKT I.1" />
      </AbsoluteFill>

      <AbsoluteFill style={{ opacity: inScene(frame, ...scenes[3]) }}>
        <Label>18 Juni 2018 · dua puluh menit</Label>
        <Timeline from={354} />
        <div style={{ position: "absolute", top: 1200, left: 62, right: 62, ...rise(frame, 399) }}>
          <div style={{ fontFamily: "Inter", fontWeight: 800, fontSize: 24, letterSpacing: "0.14em", color: C.sage }}>DARI DERMAGA KE GELOMBANG</div>
          <div style={{ marginTop: 25, fontFamily: "Space Grotesk", fontWeight: 700, fontSize: 82, lineHeight: 0.9, letterSpacing: "-0.07em", color: C.ivory }}>30 MENIT RUTE NORMAL.</div>
        </div>
        <Footer source="KNKT I.1" />
      </AbsoluteFill>

      <AbsoluteFill style={{ opacity: inScene(frame, ...scenes[4]) }}>
        <Label>Gelombang dari kiri · diagram</Label>
        <WaveAndHull from={477} />
        <div style={{ position: "absolute", top: 410, left: 62, right: 62, ...rise(frame, 497) }}>
          <div style={{ fontFamily: "Space Grotesk", fontWeight: 700, fontSize: 150, lineHeight: 0.8, letterSpacing: "-0.095em", color: C.orange }}>1,5–2 M</div>
          <div style={{ marginTop: 48, fontFamily: "Inter", fontWeight: 800, fontSize: 24, letterSpacing: "0.15em", color: C.sage }}>GELOMBANG · BUKAN ARSIP KEJADIAN</div>
        </div>
        <Footer source="KNKT I.1" />
      </AbsoluteFill>

      <AbsoluteFill style={{ opacity: inScene(frame, ...scenes[5]) }}>
        <Label>Dokumen dan posko</Label>
        <CountCards from={627} />
        <div style={{ position: "absolute", top: 1228, left: 72, right: 72, fontFamily: "Inter", fontWeight: 800, fontSize: 21, color: C.sage, letterSpacing: "0.11em", textAlign: "center", ...rise(frame, 735) }}>45 · RINGKASAN HASIL KNKT &nbsp;&nbsp; 188 · VERIFIKASI POSKO</div>
        <Footer source="KNKT · RILIS HASIL" />
      </AbsoluteFill>

      <AbsoluteFill style={{ opacity: inScene(frame, ...scenes[6]) }}>
        <Label>Kalimat tandatangan</Label>
        <BigNumber number="188" caption="BUKAN ANGKA KAPAL. IA ANGKA POSKO." from={919} accent />
        <div style={{ position: "absolute", top: 1010, left: 62, right: 62, fontFamily: "Inter", fontWeight: 800, color: C.sage, fontSize: 22, letterSpacing: "0.14em", textAlign: "center", ...rise(frame, 945) }}>HASIL VERIFIKASI PADA HARI KESEMBILAN</div>
        <Footer source="KNKT I.2.2" />
      </AbsoluteFill>

      <AbsoluteFill style={{ opacity: inScene(frame, ...scenes[7]) }}>
        <Label>Yang seharusnya ada sebelum berangkat</Label>
        <ManifestPage from={1010} />
        <div style={{ position: "absolute", left: 62, right: 62, top: 1240, textAlign: "center", ...rise(frame, 1040) }}>
          <div style={{ fontFamily: "Space Grotesk", fontWeight: 700, fontSize: 69, lineHeight: 0.92, letterSpacing: "-0.065em", color: C.ivory }}>MANIFEST<br />SEBELUM BERANGKAT.</div>
        </div>
        <Footer source="REKOMENDASI KNKT" />
      </AbsoluteFill>

      <AbsoluteFill style={{ opacity: inScene(frame, ...scenes[8]) }}>
        <Label>Penutup · kembali ke angka</Label>
        <BigNumber number="188" caption="HITUNG 188 SEBELUM BERANGKAT." from={1134} accent />
        <div style={{ position: "absolute", left: 62, right: 62, top: 1170, textAlign: "center", ...rise(frame, 1156) }}>
          <div style={{ fontFamily: "Space Grotesk", fontWeight: 700, fontSize: 65, lineHeight: 0.92, letterSpacing: "-0.065em", color: C.ivory }}>HITUNG 188<br />ATAU CARI?</div>
        </div>
        <Footer source="KNKT I.2.2 · REKOMENDASI KNKT" />
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
