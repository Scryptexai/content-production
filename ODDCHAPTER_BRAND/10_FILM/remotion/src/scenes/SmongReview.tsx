import React from "react";
import {
  AbsoluteFill,
  Audio,
  Easing,
  Img,
  interpolate,
  staticFile,
  useCurrentFrame,
} from "remotion";
import { Gif } from "@remotion/gif";
import { C, H, W } from "../theme";

/**
 * AK-EP11 review remake.
 *
 * This is deliberately an animated information film, not a sequence of static
 * title cards: every section has continuous movement that carries the idea
 * forward (tide, map camera, memory thread, time line, wave propagation).
 */
const TOTAL = 1065; // 35.50s @ 30fps
const ease = Easing.bezier(0.2, 0.7, 0.2, 1);
const clamp = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;

const between = (frame: number, from: number, until: number) => frame >= from && frame < until;
const progress = (frame: number, from: number, duration: number) =>
  interpolate(frame, [from, from + duration], [0, 1], { ...clamp, easing: ease });
// Hard editorial cuts keep the energy high; only the final frames ease out.
const fade = (frame: number, from: number, until: number, length = 10) =>
  interpolate(frame, [from, until - length, until], [1, 1, 0], { ...clamp, easing: ease });

const baseText: React.CSSProperties = {
  color: C.ivory,
  fontFamily: "Space Grotesk",
  fontWeight: 700,
  letterSpacing: "-0.065em",
  lineHeight: 0.9,
};

const Credit: React.FC<{ children: React.ReactNode; dark?: boolean }> = ({ children, dark = true }) => (
  <div
    style={{
      position: "absolute",
      left: 52,
      right: 52,
      bottom: 58,
      padding: "17px 20px",
      borderTop: "1px solid rgba(228,240,235,.2)",
      background: dark ? "rgba(2, 12, 18, .7)" : "rgba(236, 245, 240, .85)",
      color: dark ? "#c1d0cf" : "#17333a",
      fontFamily: "Inter",
      fontWeight: 600,
      fontSize: 20,
      letterSpacing: "0.05em",
      textTransform: "uppercase",
      zIndex: 20,
    }}
  >
    {children}
  </div>
);

const Kicker: React.FC<{ children: React.ReactNode; x?: number; y?: number }> = ({ children, x = 66, y = 138 }) => (
  <div
    style={{
      position: "absolute",
      left: x,
      top: y,
      color: "#ec3a3a",
      fontFamily: "Inter",
      fontWeight: 700,
      letterSpacing: "0.14em",
      fontSize: 25,
      textTransform: "uppercase",
    }}
  >
    {children}
  </div>
);

const KineticTitle: React.FC<{
  lines: string[];
  from: number;
  size?: number;
  left?: number;
  top?: number;
  accentIndex?: number;
}> = ({ lines, from, size = 108, left = 62, top = 220, accentIndex = -1 }) => {
  const frame = useCurrentFrame();
  return (
    <div style={{ position: "absolute", left, top, zIndex: 8 }}>
      {lines.map((line, index) => {
        const p = progress(frame, from + index * 5, 16);
        return (
          <div
            key={line}
            style={{
              ...baseText,
              color: index === accentIndex ? "#ec3a3a" : C.ivory,
              fontSize: size,
              opacity: p,
              transform: `translateX(${(1 - p) * -100}px) skewX(${(1 - p) * -8}deg)`,
              transformOrigin: "left center",
              whiteSpace: "nowrap",
            }}
          >
            {line}
          </div>
        );
      })}
    </div>
  );
};

/** Continuous moving ocean/data backdrop. */
const OceanMotion: React.FC<{ phase?: number; danger?: boolean; light?: boolean }> = ({ phase = 0, danger = false, light = false }) => {
  const frame = useCurrentFrame();
  const drift = frame * (0.55 + phase * 0.035);
  const horizon = 700 + Math.sin((frame + phase * 30) / 40) * 24;
  const accent = danger ? "#ec3a3a" : "#4bb8bd";
  return (
    <AbsoluteFill
      style={{
        overflow: "hidden",
        background: light
          ? "linear-gradient(155deg, #dbe9e7 0%, #99c4c5 44%, #164b59 100%)"
          : "radial-gradient(1000px 780px at 105% -10%, #164f5d 0%, #092b38 38%, #051823 73%, #03111a 100%)",
      }}
    >
      <div
        style={{
          position: "absolute",
          width: 1120,
          height: 1120,
          borderRadius: 9999,
          right: -590 + Math.sin(frame / 110) * 35,
          top: -440 + Math.cos(frame / 130) * 28,
          background: danger ? "rgba(236,58,58,.22)" : "rgba(102,190,189,.16)",
          filter: "blur(1px)",
        }}
      />
      <svg width={W} height={H} viewBox={`0 0 ${W} ${H}`} style={{ position: "absolute", inset: 0 }}>
        <defs>
          <linearGradient id="waveFill" x1="0" x2="0" y1="0" y2="1">
            <stop offset="0" stopColor={accent} stopOpacity=".32" />
            <stop offset="1" stopColor="#062334" stopOpacity=".08" />
          </linearGradient>
        </defs>
        {Array.from({ length: 13 }, (_, i) => {
          const y = horizon + i * 83;
          const amp = 16 + (i % 4) * 7;
          const x = ((drift * (0.8 + i * 0.035) + i * 130) % 320) - 320;
          const opacity = 0.16 + (i % 3) * 0.07;
          return (
            <path
              key={i}
              d={`M -420 ${y} Q -160 ${y - amp} 100 ${y} T 620 ${y} T 1160 ${y} T 1680 ${y}`}
              transform={`translate(${x} 0)`}
              fill="none"
              stroke={i % 5 === 0 && danger ? "#ec3a3a" : "#7eced0"}
              strokeWidth={i % 4 === 0 ? 4 : 2}
              opacity={opacity}
            />
          );
        })}
        <path
          d={`M-100 ${horizon + 310} Q 180 ${horizon + 210} 460 ${horizon + 330} T 1120 ${horizon + 260} V 1920 H -100 Z`}
          fill="url(#waveFill)"
          opacity=".5"
        />
      </svg>
      <div
        style={{
          position: "absolute",
          inset: 0,
          opacity: light ? 0.08 : 0.18,
          background:
            "repeating-linear-gradient(90deg, rgba(255,255,255,.07) 0 1px, transparent 1px 96px), repeating-linear-gradient(0deg, rgba(255,255,255,.04) 0 1px, transparent 1px 96px)",
        }}
      />
    </AbsoluteFill>
  );
};

const TideLines: React.FC = () => {
  const frame = useCurrentFrame();
  return (
    <svg width={W} height={H} viewBox={`0 0 ${W} ${H}`} style={{ position: "absolute", inset: 0, zIndex: 3 }}>
      {Array.from({ length: 8 }, (_, index) => {
        const p = ((frame / 40 + index / 8) % 1 + 1) % 1;
        const x = 1020 - p * 1100;
        const y = 920 + index * 68 + Math.sin(frame / 17 + index) * 9;
        return (
          <g key={index} opacity={0.16 + p * 0.45} transform={`translate(${x} ${y})`}>
            <path d="M0 0 H155" stroke="#eaf4ee" strokeWidth="5" />
            <path d="M155 0 L126 -18 M155 0 L126 18" stroke="#eaf4ee" strokeWidth="5" fill="none" />
          </g>
        );
      })}
    </svg>
  );
};

const Pin: React.FC<{ x: number; y: number; label?: string; scale?: number }> = ({ x, y, label, scale = 1 }) => {
  const frame = useCurrentFrame();
  const pulse = 1 + 0.2 * (0.5 + 0.5 * Math.sin(frame / 6));
  return (
    <div style={{ position: "absolute", left: x, top: y, zIndex: 12, transform: `scale(${scale})`, transformOrigin: "center" }}>
      <div
        style={{
          width: 35,
          height: 35,
          borderRadius: 99,
          background: "#ec3a3a",
          border: "5px solid #fff8ed",
          boxShadow: `0 0 0 ${15 * pulse}px rgba(236,58,58,.18)`,
        }}
      />
      {label ? (
        <div
          style={{
            position: "absolute",
            left: 26,
            top: -20,
            padding: "12px 18px",
            background: "#ec3a3a",
            color: C.ivory,
            fontFamily: "Inter",
            fontWeight: 800,
            fontSize: 28,
            letterSpacing: "0.08em",
          }}
        >
          {label}
        </div>
      ) : null}
    </div>
  );
};

const MapWindow: React.FC<{ from: number; zoomTo?: number; label?: string; bright?: boolean }> = ({ from, zoomTo = 1.18, label, bright = false }) => {
  const frame = useCurrentFrame();
  const p = progress(frame, from, 55);
  const camera = interpolate(frame, [from, from + 145], [0.78, zoomTo], clamp);
  const x = interpolate(frame, [from, from + 145], [-100, 72], clamp);
  const scan = ((frame - from) % 75) / 75;
  return (
    <div
      style={{
        position: "absolute",
        left: 0,
        right: 0,
        top: 515,
        height: 870,
        overflow: "hidden",
        opacity: p,
        background: bright ? "#dbe7e2" : "#bed9dc",
        borderTop: "1px solid rgba(255,255,255,.7)",
        borderBottom: "1px solid rgba(255,255,255,.7)",
      }}
    >
      <Img
        src={staticFile("ak-ep11/simeulue_topography_cc-by-sa-3.png")}
        style={{
          width: "124%",
          height: "124%",
          objectFit: "contain",
          position: "absolute",
          left: x,
          top: -70,
          transform: `scale(${camera}) rotate(${-2 + Math.sin(frame / 48) * 0.55}deg)`,
          transformOrigin: "52% 30%",
          filter: "saturate(1.15) contrast(1.05)",
        }}
      />
      <div
        style={{
          position: "absolute",
          top: scan * 870 - 92,
          left: 0,
          right: 0,
          height: 92,
          background: "linear-gradient(180deg, transparent, rgba(240,255,251,.46), transparent)",
          mixBlendMode: "screen",
        }}
      />
      <svg width={W} height={870} viewBox={`0 0 ${W} 870`} style={{ position: "absolute", inset: 0 }}>
        <path d="M0 160 H1080 M0 435 H1080 M0 710 H1080 M270 0 V870 M540 0 V870 M810 0 V870" stroke="#0e5060" opacity=".18" strokeWidth="2" />
      </svg>
      {label ? <Pin x={354} y={128} label={label} /> : null}
    </div>
  );
};

const MapScene: React.FC = () => {
  const frame = useCurrentFrame();
  const from = 130;
  if (!between(frame, from, 251)) return null;
  const local = frame - from;
  const wordP = progress(frame, from + 20, 30);
  return (
    <AbsoluteFill style={{ opacity: fade(frame, from, 251) }}>
      <OceanMotion phase={2} light />
      <Kicker>Pulau di barat Aceh</Kicker>
      <KineticTitle lines={["SIMEULUE", "MENGINGAT"]} from={from + 10} size={104} top={205} accentIndex={1} />
      <div
        style={{
          position: "absolute",
          top: 398,
          left: 66,
          color: "#153d45",
          fontFamily: "Inter",
          fontWeight: 700,
          fontSize: 37,
          letterSpacing: "0.01em",
          opacity: wordP,
          transform: `translateY(${(1 - wordP) * 32}px)`,
        }}
      >
        satu kata diwariskan: <span style={{ color: "#c1262e" }}>SMONG</span>
      </div>
      <MapWindow from={from} zoomTo={1.16} label="SIMEULUE" bright />
      <div
        style={{
          position: "absolute",
          left: 70,
          top: 1432,
          padding: "16px 22px",
          background: "#0b4957",
          color: "#eaf4ee",
          fontFamily: "Inter",
          fontWeight: 800,
          letterSpacing: "0.11em",
          fontSize: 25,
          transform: `translateX(${Math.sin(local / 16) * 3}px)`,
        }}
      >
        02°30′N · 96°00′E
      </div>
      <Credit dark={false}>PETA BERGERAK · SADALMELIK · WIKIMEDIA COMMONS · CC BY-SA 3.0</Credit>
    </AbsoluteFill>
  );
};

const MemoryThread: React.FC = () => {
  const frame = useCurrentFrame();
  const from = 251;
  if (!between(frame, from, 396)) return null;
  const draw = progress(frame, from + 20, 70);
  const dots = Array.from({ length: 9 }, (_, index) => {
    const t = ((frame - from) / 45 + index / 9) % 1;
    return { x: 155 + t * 770, y: 960 + Math.sin(t * Math.PI * 2) * 120 };
  });
  return (
    <AbsoluteFill style={{ opacity: fade(frame, from, 396) }}>
      <OceanMotion phase={3} />
      <Kicker>Pesan yang hidup</Kicker>
      <KineticTitle lines={["CERITA", "DAN SYAIR"]} from={from + 5} size={120} top={214} accentIndex={1} />
      <div style={{ position: "absolute", top: 550, left: 66, right: 66, height: 720, overflow: "hidden" }}>
        <svg width="100%" height="100%" viewBox="0 0 948 720">
          <path
            d="M40 390 C190 120 330 580 475 355 S750 105 910 390"
            fill="none"
            stroke="#76d2d1"
            strokeWidth="8"
            strokeDasharray="1450"
            strokeDashoffset={1450 * (1 - draw)}
            opacity=".8"
          />
          <path
            d="M40 390 C190 120 330 580 475 355 S750 105 910 390"
            fill="none"
            stroke="#ec3a3a"
            strokeWidth="18"
            strokeDasharray="18 42"
            strokeDashoffset={-frame * 9}
            opacity=".8"
          />
          {dots.map((dot, index) => <circle key={index} cx={dot.x - 66} cy={dot.y - 550} r="11" fill="#f5eee2" />)}
        </svg>
        {[
          ["NENEK", 46, 286],
          ["ORANG TUA", 306, 475],
          ["ANAK", 670, 246],
        ].map(([label, x, y], index) => {
          const p = progress(frame, from + 34 + index * 14, 20);
          return (
            <div
              key={String(label)}
              style={{
                position: "absolute",
                left: Number(x),
                top: Number(y),
                color: C.ivory,
                fontFamily: "Inter",
                fontWeight: 800,
                letterSpacing: "0.08em",
                fontSize: 29,
                opacity: p,
                transform: `scale(${0.7 + p * 0.3})`,
              }}
            >
              {String(label)}
            </div>
          );
        })}
      </div>
      <div style={{ position: "absolute", left: 66, right: 66, top: 1372, ...baseText, fontSize: 56, color: "#d5e6e2" }}>
        dari generasi ke generasi
      </div>
      <Credit>PENGETAHUAN LISAN LINTAS GENERASI · UNESCO</Credit>
    </AbsoluteFill>
  );
};

const SignScene: React.FC = () => {
  const frame = useCurrentFrame();
  const from = 396;
  if (!between(frame, from, 532)) return null;
  const local = frame - from;
  const shake = local < 42 ? Math.sin(local * 2.3) * interpolate(local, [0, 42], [18, 0], clamp) : 0;
  const first = progress(frame, from + 8, 20);
  const second = progress(frame, from + 43, 20);
  const third = progress(frame, from + 78, 20);
  return (
    <AbsoluteFill style={{ opacity: fade(frame, from, 532) }}>
      <OceanMotion phase={4} danger />
      <Kicker>Tanda bahaya</Kicker>
      <KineticTitle lines={["JANGAN", "menebak."]} from={from} size={113} top={205} accentIndex={0} />
      <div style={{ position: "absolute", left: 0, right: 0, top: 600, height: 650, transform: `translateX(${shake}px)` }}>
        {[
          ["01", "GEMPA KUAT", first, "#ec3a3a"],
          ["02", "LAUT SURUT", second, "#67c8c5"],
          ["03", "KE TEMPAT TINGGI", third, "#f5eee2"],
        ].map(([number, text, p, color], index) => (
          <div
            key={String(number)}
            style={{
              position: "absolute",
              top: index * 188,
              left: 65,
              right: 65,
              height: 150,
              display: "flex",
              alignItems: "center",
              gap: 28,
              padding: "0 28px",
              border: `2px solid ${String(color)}`,
              background: "rgba(4,25,34,.72)",
              opacity: Number(p),
              transform: `translateX(${(1 - Number(p)) * 160}px)`,
            }}
          >
            <div style={{ color: String(color), fontFamily: "Space Grotesk", fontWeight: 700, fontSize: 56, letterSpacing: "-0.08em" }}>{String(number)}</div>
            <div style={{ color: C.ivory, fontFamily: "Space Grotesk", fontWeight: 700, fontSize: index === 2 ? 55 : 65, letterSpacing: "-0.055em" }}>{String(text)}</div>
            {index === 1 ? <TideLines /> : null}
          </div>
        ))}
      </div>
      <div style={{ position: "absolute", top: 1375, left: 66, right: 66, ...baseText, color: "#d0e1de", fontSize: 54 }}>
        baca tanda. bergerak bersama.
      </div>
      <Credit>SMONG · GEMPA KUAT → LAUT SURUT → TEMPAT TINGGI</Credit>
    </AbsoluteFill>
  );
};

const TimeAndWaveScene: React.FC = () => {
  const frame = useCurrentFrame();
  const from = 532;
  if (!between(frame, from, 729)) return null;
  const local = frame - from;
  const isWave = local >= 100;
  const count = Math.min(10, Math.max(0, Math.floor(interpolate(local, [15, 78], [0, 10], clamp))));
  const meter = progress(frame, from + 10, 80);
  return (
    <AbsoluteFill style={{ opacity: fade(frame, from, 729) }}>
      <OceanMotion phase={5} danger={isWave} />
      {!isWave ? (
        <>
          <Kicker>26 Desember 2004</Kicker>
          <KineticTitle lines={["TAK SAMPAI", "SEPULUH MENIT"]} from={from + 2} size={91} top={210} accentIndex={1} />
          <div
            style={{
              position: "absolute",
              top: 700,
              left: 67,
              ...baseText,
              color: "#ec3a3a",
              fontSize: 390,
              letterSpacing: "-0.15em",
              transform: `scale(${0.8 + meter * 0.2})`,
              transformOrigin: "left center",
            }}
          >
            {count}
          </div>
          <div style={{ position: "absolute", left: 78, right: 78, top: 1160, height: 10, background: "rgba(225,243,237,.2)" }}>
            <div style={{ height: "100%", width: `${meter * 100}%`, background: "#ec3a3a" }} />
          </div>
          <div style={{ position: "absolute", left: 78, top: 1230, color: "#cbdedb", fontFamily: "Inter", fontWeight: 700, fontSize: 35 }}>GUNCANGAN BERHENTI</div>
          <div style={{ position: "absolute", right: 78, top: 1290, color: C.ivory, fontFamily: "Inter", fontWeight: 800, fontSize: 35 }}>GELOMBANG MENCAPAI LANGI</div>
          <Credit>LANGI · MCADOO, DENGLER, PRASETYA & TITOV · 2006</Credit>
        </>
      ) : (
        <WavePropagation start={from + 100} />
      )}
    </AbsoluteFill>
  );
};

const WavePropagation: React.FC<{ start: number }> = ({ start }) => {
  const frame = useCurrentFrame();
  const local = frame - start;
  const titleP = progress(frame, start + 4, 18);
  return (
    <>
      <Kicker>Simulasi data</Kicker>
      <div style={{ position: "absolute", left: 66, top: 220, ...baseText, color: C.ivory, fontSize: 108, opacity: titleP, transform: `translateY(${(1 - titleP) * 55}px)` }}>
        GELOMBANG
      </div>
      <div style={{ position: "absolute", left: 70, top: 337, color: "#c7dcd8", fontFamily: "Inter", fontSize: 42, fontWeight: 700 }}>MENYEBAR KE PULAU</div>
      <div
        style={{
          position: "absolute",
          left: 190,
          top: 540,
          width: 700,
          height: 700,
          overflow: "hidden",
          borderRadius: 9999,
          border: "2px solid rgba(117,210,208,.48)",
          background: "#020d15",
          transform: `rotate(${Math.sin(local / 24) * 1.5}deg) scale(${0.91 + Math.sin(local / 30) * 0.018})`,
        }}
      >
        <Gif
          src={staticFile("ak-ep11/noaa_2004_tsunami_pd.gif")}
          width={700}
          height={700}
          fit="cover"
          playbackRate={1.15}
          style={{ filter: "saturate(1.16) contrast(1.08)" }}
        />
        <div style={{ position: "absolute", inset: 0, background: "radial-gradient(circle, transparent 42%, rgba(2,13,21,.48) 100%)" }} />
      </div>
      <svg width={W} height={H} viewBox={`0 0 ${W} ${H}`} style={{ position: "absolute", inset: 0 }}>
        {[0, 1, 2, 3, 4].map((index) => {
          const phase = ((local - index * 13) % 92 + 92) % 92;
          const radius = 70 + phase * 8.2;
          return <circle key={index} cx="540" cy="1040" r={radius} fill="none" stroke={index % 2 ? "#75d2d0" : "#ec3a3a"} strokeWidth="7" opacity={Math.max(0, 0.74 - phase / 120)} />;
        })}
        <circle cx="540" cy="1040" r="42" fill="#ec3a3a" />
        <circle cx="540" cy="1040" r="15" fill="#f5eee2" />
      </svg>
      <div style={{ position: "absolute", left: 80, right: 80, top: 1420, padding: "26px 30px", background: "rgba(4,21,28,.82)", border: "2px solid #ec3a3a", color: C.ivory, fontFamily: "Inter", fontWeight: 800, fontSize: 31, letterSpacing: "0.06em" }}>
        VISUALISASI DATA · BUKAN REKAMAN KEJADIAN
      </div>
      <Credit>SIMULASI REGIONAL NOAA · DOMAIN PUBLIK · BUKAN FOOTAGE LANGI</Credit>
    </>
  );
};

const LangiScene: React.FC = () => {
  const frame = useCurrentFrame();
  const from = 729;
  if (!between(frame, from, 855)) return null;
  const p = progress(frame, from + 22, 60);
  const people = Math.round(interpolate(frame, [from + 35, from + 90], [0, 800], clamp) / 10) * 10;
  return (
    <AbsoluteFill style={{ opacity: fade(frame, from, 855) }}>
      <OceanMotion phase={7} light />
      <Kicker>Langi · Utara Simeulue</Kicker>
      <KineticTitle lines={["MEREKA", "BERGERAK."]} from={from + 2} size={112} top={210} accentIndex={1} />
      <MapWindow from={from + 3} zoomTo={1.48} label="LANGI" bright />
      <div
        style={{
          position: "absolute",
          left: 54,
          right: 54,
          top: 1390,
          padding: "28px 32px 34px",
          background: "#093440",
          border: "2px solid #ec3a3a",
          opacity: p,
          transform: `translateY(${(1 - p) * 80}px)`,
        }}
      >
        <div style={{ color: "#aac9c7", fontFamily: "Inter", fontWeight: 800, letterSpacing: "0.11em", fontSize: 25 }}>DESANYA HANCUR. NAMUN …</div>
        <div style={{ ...baseText, color: "#ec3a3a", fontSize: 143, marginTop: 2, letterSpacing: "-0.11em" }}>≈{people}</div>
        <div style={{ ...baseText, color: C.ivory, fontSize: 67, marginTop: -16 }}>WARGA SELAMAT</div>
      </div>
      <Credit dark={false}>PETA: SADALMELIK · DATA LANGI: MCADOO DKK. 2006</Credit>
    </AbsoluteFill>
  );
};

const StoryToAction: React.FC = () => {
  const frame = useCurrentFrame();
  const from = 855;
  if (!between(frame, from, 970)) return null;
  const p = progress(frame, from + 6, 22);
  const flow = ((frame - from) % 55) / 55;
  return (
    <AbsoluteFill style={{ opacity: fade(frame, from, 970) }}>
      <OceanMotion phase={8} />
      <Kicker>Bukan menebak laut</Kicker>
      <KineticTitle lines={["MEREKA", "MENGINGAT."]} from={from} size={108} top={215} accentIndex={1} />
      <div style={{ position: "absolute", left: 64, right: 64, top: 760, height: 270 }}>
        <svg width="100%" height="100%" viewBox="0 0 952 270">
          <path d="M50 136 C255 34 400 236 580 135 S785 42 910 136" fill="none" stroke="#65c7c4" strokeWidth="9" opacity=".7" />
          {[0, 1, 2, 3].map((index) => {
            const t = (flow + index / 4) % 1;
            const x = 50 + 860 * t;
            const y = 136 - Math.sin(t * Math.PI * 2) * 53;
            return <circle key={index} cx={x} cy={y} r="16" fill="#ec3a3a" />;
          })}
        </svg>
      </div>
      <div style={{ position: "absolute", left: 68, top: 685, color: C.ivory, fontFamily: "Space Grotesk", fontWeight: 700, fontSize: 86, letterSpacing: "-0.07em", opacity: p }}>CERITA</div>
      <div style={{ position: "absolute", right: 66, top: 1050, color: "#ec3a3a", fontFamily: "Space Grotesk", fontWeight: 700, fontSize: 84, letterSpacing: "-0.07em", opacity: p }}>TINDAKAN</div>
      <div style={{ position: "absolute", left: 68, right: 68, top: 1290, paddingTop: 28, borderTop: "2px solid rgba(117,210,208,.52)", color: "#c8dedb", fontFamily: "Inter", fontSize: 42, fontWeight: 700, lineHeight: 1.18 }}>
        pengetahuan jadi gerakan bersama
      </div>
      <Credit>SMONG · CERITA DAN SYAIR ANTARGENERASI</Credit>
    </AbsoluteFill>
  );
};

const CtaScene: React.FC = () => {
  const frame = useCurrentFrame();
  const from = 970;
  if (!between(frame, from, TOTAL)) return null;
  const p = progress(frame, from + 2, 18);
  const orbit = frame - from;
  return (
    <AbsoluteFill style={{ opacity: fade(frame, from, TOTAL, 5) }}>
      <OceanMotion phase={10} danger />
      <div
        style={{
          position: "absolute",
          width: 600,
          height: 600,
          borderRadius: 9999,
          border: "2px solid rgba(236,58,58,.65)",
          left: 270 + Math.sin(orbit / 14) * 18,
          top: 580 + Math.cos(orbit / 14) * 18,
          transform: `scale(${0.74 + (orbit % 50) / 250})`,
        }}
      />
      <Kicker>Pertanyaan untuk rumahmu</Kicker>
      <KineticTitle lines={["SIAPA", "MENGAJARKAN", "TANDA BAHAYA?"]} from={from + 3} size={93} top={220} accentIndex={2} />
      <div
        style={{
          position: "absolute",
          left: 65,
          top: 1354,
          padding: "19px 26px",
          color: C.ivory,
          background: "#ec3a3a",
          fontFamily: "Inter",
          fontWeight: 800,
          letterSpacing: "0.09em",
          fontSize: 29,
          opacity: p,
          transform: `translateY(${(1 - p) * 35}px)`,
        }}
      >
        TULIS DI KOMENTAR
      </div>
      <Credit>SUMBER: NOAA PMEL · UNESCO · BMKG</Credit>
    </AbsoluteFill>
  );
};

const HookScene: React.FC = () => {
  const frame = useCurrentFrame();
  if (!between(frame, 0, 130)) return null;
  const stamp = progress(frame, 66, 16);
  return (
    <AbsoluteFill style={{ opacity: fade(frame, 0, 130) }}>
      <OceanMotion phase={0} danger />
      <TideLines />
      <Kicker>Simeulue · Aceh</Kicker>
      <KineticTitle lines={["SAAT LAUT", "SURUT"]} from={5} size={128} top={216} accentIndex={1} />
      <div
        style={{
          position: "absolute",
          left: 66,
          top: 560,
          color: "#d5e4df",
          fontFamily: "Inter",
          fontSize: 42,
          fontWeight: 700,
          lineHeight: 1.15,
          opacity: stamp,
          transform: `translateY(${(1 - stamp) * 50}px)`,
        }}
      >
        warga tidak menunggu{`\n`}peringatan resmi.
      </div>
      <div
        style={{
          position: "absolute",
          left: 66,
          top: 1250,
          padding: "20px 27px",
          background: "#ec3a3a",
          color: C.ivory,
          fontFamily: "Inter",
          fontWeight: 800,
          letterSpacing: "0.08em",
          fontSize: 30,
          opacity: stamp,
          transform: `translateX(${(1 - stamp) * -80}px)`,
        }}
      >
        JANGAN TUNGGU
      </div>
      <Credit>ILUSTRASI DATA BERANIMASI · BUKAN REKAMAN KEJADIAN</Credit>
    </AbsoluteFill>
  );
};

export const SmongReview: React.FC = () => (
  <AbsoluteFill>
    <Audio src={staticFile("audio/ak-ep11-smong-review.wav")} />
    <HookScene />
    <MapScene />
    <MemoryThread />
    <SignScene />
    <TimeAndWaveScene />
    <LangiScene />
    <StoryToAction />
    <CtaScene />
  </AbsoluteFill>
);
