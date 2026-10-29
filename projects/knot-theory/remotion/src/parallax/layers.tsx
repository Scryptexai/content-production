/**
 * layers.tsx — 11 lapis pemandangan, masing-masing SVG penuh 1920×1080.
 *
 * Semua lapis digambar sendiri (tidak ada aset dari pihak lain). Gayanya
 * papercut: massa gelap, tepi kena cahaya, kabut di kejauhan.
 *
 * Yang penting untuk parallax BUKAN jumlah detailnya, tapi bahwa tiap lapis
 * punya jarak z sendiri dan bisa bergeser sendiri. Lihat camera.ts.
 */
import React from "react";

export const C = {
  ink: "#05070F",
  ink2: "#0B1020",
  ink3: "#1A1D32",
  hill: "#1B1D33",
  hill2: "#111424",
  town: "#0D1020",
  stone: "#0A0D17",
  stoneTop: "#2A2739",
  edge: "#E4A177",
  cream: "#EFE7DC",
  rose: "#D98E73",
  sage: "#8FA98B",
};

/** PRNG deterministik — supaya bintang dan debu tidak berkedip acak tiap render. */
export const rng = (seed: number) => {
  let s = seed >>> 0;
  return () => {
    s = (s + 0x6d2b79f5) >>> 0;
    let t = s;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
};

const SVG: React.FC<{ children: React.ReactNode }> = ({ children }) => (
  <svg
    width="100%"
    height="100%"
    viewBox="0 0 1920 1080"
    preserveAspectRatio="xMidYMid slice"
    style={{ position: "absolute", inset: 0, display: "block" }}
  >
    {children}
  </svg>
);

/* ---------------------------------------------------------------- langit */
export const Sky: React.FC = () => (
  <SVG>
    <defs>
      <linearGradient id="skyG" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0%" stopColor="#05070F" />
        <stop offset="26%" stopColor="#0B1024" />
        <stop offset="46%" stopColor="#1B1B38" />
        <stop offset="58%" stopColor="#37263F" />
        <stop offset="69%" stopColor="#5E3547" />
        <stop offset="80%" stopColor="#8E4F4E" />
        <stop offset="91%" stopColor="#C0705A" />
        <stop offset="100%" stopColor="#E09168" />
      </linearGradient>
    </defs>
    <rect width="1920" height="1080" fill="url(#skyG)" />
  </SVG>
);

/* ---------------------------------------------------------------- bintang */
export const Stars: React.FC<{ t: number }> = ({ t }) => {
  const r = rng(7);
  const pts = Array.from({ length: 170 }, () => ({
    x: r() * 1920,
    y: r() * 620,
    rr: 0.7 + r() * 1.5,
    ph: r() * 6.28,
    amp: 0.35 + r() * 0.65,
  }));
  return (
    <SVG>
      {pts.map((p, i) => {
        const fade = Math.max(0, 1 - p.y / 620);
        const tw = 0.55 + 0.45 * Math.sin(t * 1.7 + p.ph);
        const o = fade * p.amp * tw;
        if (o < 0.04) return null;
        return (
          <circle key={i} cx={p.x} cy={p.y} r={p.rr} fill="#DCE6FF" opacity={o} />
        );
      })}
    </SVG>
  );
};

/* ----------------------------------------------------------------- matahari */
export const Sun: React.FC = () => (
  <SVG>
    <defs>
      <radialGradient id="sunCore">
        <stop offset="0%" stopColor="#FFF6E2" />
        <stop offset="62%" stopColor="#FFD9A8" />
        <stop offset="100%" stopColor="#F0A46E" />
      </radialGradient>
      <radialGradient id="sunHalo">
        <stop offset="0%" stopColor="#FFC389" stopOpacity="0.55" />
        <stop offset="45%" stopColor="#E08B63" stopOpacity="0.18" />
        <stop offset="100%" stopColor="#E08B63" stopOpacity="0" />
      </radialGradient>
    </defs>
    <circle cx="1330" cy="352" r="300" fill="url(#sunHalo)" />
    <circle cx="1330" cy="352" r="74" fill="url(#sunCore)" />
  </SVG>
);

/* ------------------------------------------------------------------ bukit */
const ridge = (seed: number, baseY: number, amp: number, step: number) => {
  const r = rng(seed);
  let d = `M -200 1200 L -200 ${baseY}`;
  for (let x = -200; x <= 2120; x += step) {
    const y = baseY - Math.sin(x * 0.0021 + seed) * amp - r() * amp * 0.55;
    d += ` L ${x.toFixed(0)} ${y.toFixed(0)}`;
  }
  return d + " L 2120 1200 Z";
};

/* Jarak memudarkan warna ke arah horizon — dibakar di sini, bukan ditumpuk
   sebagai kotak "screen" (cara itu memutihkan siluet dan terlihat murah). */
export const RidgeFar: React.FC = () => (
  <SVG>
    <path d={ridge(3, 690, 104, 120)} fill="#3A3550" opacity={0.85} />
    <path d={ridge(9, 742, 66, 110)} fill="#2A2742" />
  </SVG>
);

export const RidgeMid: React.FC = () => (
  <SVG>
    <path d={ridge(15, 806, 58, 120)} fill="#1B1A30" />
  </SVG>
);

export const RidgeNear: React.FC = () => (
  <SVG>
    <path d={ridge(21, 872, 46, 130)} fill="#101120" />
  </SVG>
);

/* ------------------------------------------------------------------ kabut */
export const Mist: React.FC = () => (
  <SVG>
    <defs>
      <linearGradient id="mistG" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0%" stopColor="#DE9770" stopOpacity="0" />
        <stop offset="45%" stopColor="#D98E73" stopOpacity="0.18" />
        <stop offset="100%" stopColor="#D98E73" stopOpacity="0" />
      </linearGradient>
    </defs>
    <rect x="0" y="770" width="1920" height="150" fill="url(#mistG)" />
  </SVG>
);

/* ----------------------------------------------------------------- tangga */
/** Tangga tergantung. Geometri HARUS sama dengan export_figure.py. */
export const STAIRS = {
  x0: 430,
  y0: 940,
  tread: 158,
  riser: 54,
  n: 6,
  plateW: 240,
  thickness: 38,
};

export const Stairs: React.FC = () => {
  const { x0, y0, tread, riser, n, plateW, thickness } = STAIRS;
  const ax = x0 + n * tread;
  const ay = y0 - n * riser;

  let d = `M ${x0 - 70} ${y0 + 34} L ${x0 - 70} ${y0}`;
  for (let i = 0; i < n; i++) {
    const x = x0 + i * tread;
    const y = y0 - i * riser;
    d += ` L ${x + tread} ${y} L ${x + tread} ${y - riser}`;
  }
  d += ` L ${ax + plateW} ${ay}`;
  d += ` L ${ax + plateW} ${ay + thickness} L ${x0 - 70} ${y0 + thickness + 34} Z`;

  return (
    <SVG>
      <path d={d} fill={C.stone} />
      {Array.from({ length: n }, (_, i) => {
        const x = x0 + i * tread;
        const y = y0 - i * riser;
        return (
          <g key={i}>
            <rect x={x} y={y - 9} width={tread} height={9} fill={C.stoneTop} />
            <rect x={x} y={y - 10.4} width={tread} height={1.9} fill={C.edge} />
            <rect
              x={x + tread - 1.6}
              y={y - riser}
              width={1.6}
              height={riser - 9}
              fill="#3A3348"
            />
          </g>
        );
      })}
      <rect x={ax} y={ay - 9} width={plateW} height={9} fill={C.stoneTop} />
      <rect x={ax} y={ay - 10.4} width={plateW} height={1.9} fill={C.edge} />
    </SVG>
  );
};

/* ------------------------------------------------------------------ debu */
export const Dust: React.FC<{ t: number }> = ({ t }) => {
  const r = rng(11);
  const pts = Array.from({ length: 70 }, () => ({
    x: r() * 1920,
    y: r() * 1080,
    s: 1.2 + r() * 2.2,
    sp: 8 + r() * 22,
    ph: r() * 6.28,
  }));
  return (
    <SVG>
      {pts.map((p, i) => {
        const y = ((p.y - t * p.sp) % 1080 + 1080) % 1080;
        const x = p.x + Math.sin(t * 0.35 + p.ph) * 26;
        const o = 0.10 + 0.30 * (0.5 + 0.5 * Math.sin(t * 0.8 + p.ph));
        return (
          <circle key={i} cx={x} cy={y} r={p.s} fill="#FFE9CC" opacity={o} />
        );
      })}
    </SVG>
  );
};

/* -------------------------------------------------------------- batu depan */
/** Bingkai bawah: satu siluet bergelombang, bukan balok-balok.
 *  Balok terbaca sebagai objek tak dikenal; gelombang terbaca sebagai tanah. */
export const Foreground: React.FC = () => {
  const r = rng(5);
  let d = "M -260 1250 L -260 1060";
  for (let x = -260; x <= 2180; x += 140) {
    const y = 1046 - Math.sin(x * 0.0016) * 26 - r() * 26;
    d += ` L ${x.toFixed(0)} ${y.toFixed(0)}`;
  }
  d += " L 2180 1250 Z";
  return (
    <SVG>
      <path d={d} fill="#04050A" />
    </SVG>
  );
};

/* ------------------------------------------------------------------ figur */
type Prim =
  | { t: "seg"; x1: number; y1: number; x2: number; y2: number; r1: number; r2: number; c: string }
  | { t: "dot"; x: number; y: number; r: number; c: string }
  | { t: "ell"; x: number; y: number; rx: number; ry: number; c: string }
  | { t: "poly"; c: string; pts: number[][] };

export const Figure: React.FC<{ draw: Prim[] }> = ({ draw }) => (
  <SVG>
    {draw.map((p, i) => {
      if (p.t === "seg") {
        return (
          <line
            key={i}
            x1={p.x1}
            y1={p.y1}
            x2={p.x2}
            y2={p.y2}
            stroke={p.c}
            strokeWidth={p.r1 * 2}
            strokeLinecap="round"
          />
        );
      }
      if (p.t === "dot") {
        return <circle key={i} cx={p.x} cy={p.y} r={p.r} fill={p.c} />;
      }
      if (p.t === "ell") {
        return <ellipse key={i} cx={p.x} cy={p.y} rx={p.rx} ry={p.ry} fill={p.c} />;
      }
      return (
        <polygon
          key={i}
          points={p.pts.map((q) => q.join(",")).join(" ")}
          fill={p.c}
        />
      );
    })}
  </SVG>
);

/* --------------------------------------------------------- lapis layar */
export const Vignette: React.FC = () => (
  <div
    style={{
      position: "absolute",
      inset: 0,
      background:
        "radial-gradient(ellipse 78% 72% at 50% 46%, rgba(0,0,0,0) 42%, rgba(0,0,0,0.30) 74%, rgba(0,0,0,0.66) 100%)",
    }}
  />
);

export const Grain: React.FC<{ frame: number }> = ({ frame }) => {
  // dua lapis ubin digeser per frame: murah, tidak butuh feTurbulence tiap frame
  const ox = (frame * 37) % 256;
  const oy = (frame * 61) % 256;
  return (
    <div
      style={{
        position: "absolute",
        inset: -64,
        backgroundImage: "url(/parallax/grain.png)",
        backgroundSize: "256px 256px",
        backgroundPosition: `${ox}px ${oy}px`,
        opacity: 0.055,
        mixBlendMode: "overlay",
      }}
    />
  );
};
