import React from "react";
import {
  AbsoluteFill,
  Audio,
  Img,
  Sequence,
  interpolate,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
  Easing,
} from "remotion";
import { Backdrop } from "./Backdrop";
import { useFonts } from "./fonts";
import { CREAM, LILAC, MUTED, ROSE, SAGE } from "./palette";

const EASE = Easing.bezier(0.22, 1, 0.36, 1);
const M = 120; // margin aman 16:9

export type Block = {
  key: string;
  scene: string;
  kicker?: string;
  vo: string;
  from: number;
  to: number;
  [k: string]: unknown;
};

export type LongProps = {
  id: string;
  tone: string;
  chapter: string;
  source: string;
  preview?: boolean;
  blocks: Block[];
};

/* ---------------------------------------------------------------- helpers */
const rise = (frame: number, delay: number, dist = 22) => ({
  opacity: interpolate(frame - delay, [0, 16], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: EASE,
  }),
  transform: `translateY(${interpolate(frame - delay, [0, 24], [dist, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: EASE,
  })}px)`,
});

const SERIF = { fontFamily: "Instrument Serif", color: CREAM } as const;
const MONO = { fontFamily: "Plex Mono", color: MUTED } as const;

const Kicker: React.FC<{ children?: React.ReactNode; color?: string }> = ({
  children,
  color,
}) => (
  <div
    style={{
      ...MONO,
      fontSize: 22,
      letterSpacing: "0.26em",
      textTransform: "uppercase",
      color: color ?? MUTED,
      marginBottom: 22,
    }}
  >
    {children}
  </div>
);

const Headline: React.FC<{ children?: React.ReactNode; size?: number }> = ({
  children,
  size = 72,
}) => (
  <div style={{ ...SERIF, fontSize: size, lineHeight: 1.1, maxWidth: 1240 }}>
    {children}
  </div>
);

/* ---------------------------------------------------------------- scenes */
const Adegan: React.FC<{ b: any; f: number }> = ({ b, f }) => (
  <div>
    <div style={rise(f, 0)}>
      <Kicker>{b.kicker}</Kicker>
    </div>
    <div style={rise(f, 4)}>
      <Headline size={76}>{b.headline}</Headline>
    </div>
    <div style={{ display: "flex", gap: 84, marginTop: 78 }}>
      {b.stats.map((s: any, i: number) => (
        <div key={s.label} style={rise(f, 16 + i * 9)}>
          <div
            style={{
              fontFamily: "Plex Mono",
              fontWeight: 500,
              fontSize: 96,
              color: i === 0 ? ROSE : CREAM,
              letterSpacing: "-0.02em",
            }}
          >
            {s.value}
          </div>
          <div style={{ ...MONO, fontSize: 26, marginTop: 10 }}>{s.label}</div>
        </div>
      ))}
    </div>
  </div>
);

const Metode: React.FC<{ b: any; f: number }> = ({ b, f }) => (
  <div>
    <div style={rise(f, 0)}>
      <Kicker>{b.kicker}</Kicker>
    </div>
    <div style={rise(f, 4)}>
      <Headline>{b.headline}</Headline>
    </div>
    <div style={{ display: "flex", alignItems: "center", gap: 46, marginTop: 76 }}>
      <div
        style={{
          ...rise(f, 18),
          border: "1px solid rgba(239,231,220,0.22)",
          borderRadius: 6,
          padding: "34px 42px",
          minWidth: 330,
        }}
      >
        <div style={{ ...MONO, fontSize: 22, letterSpacing: "0.14em" }}>
          {b.before.t}
        </div>
        <div style={{ ...SERIF, fontSize: 54, marginTop: 8 }}>{b.before.v}</div>
      </div>
      <div style={{ ...rise(f, 26), ...MONO, fontSize: 44, color: ROSE }}>→</div>
      <div
        style={{
          ...rise(f, 30),
          border: "1px solid rgba(239,231,220,0.35)",
          borderRadius: 6,
          padding: "34px 42px",
          minWidth: 330,
          background: "rgba(239,231,220,0.05)",
        }}
      >
        <div style={{ ...MONO, fontSize: 22, letterSpacing: "0.14em" }}>
          {b.after.t}
        </div>
        <div style={{ ...SERIF, fontSize: 54, marginTop: 8 }}>{b.after.v}</div>
      </div>
    </div>
    <div style={{ ...rise(f, 44), ...MONO, fontSize: 26, marginTop: 34 }}>
      {b.note}
    </div>
  </div>
);

const Bar: React.FC<{ b: any; f: number }> = ({ b, f }) => {
  const grow = interpolate(f, [6, 14], [0.86, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: EASE,
  });
  return (
    <div>
      <div style={rise(f, 0)}>
        <Kicker>{b.kicker}</Kicker>
      </div>
      <div style={rise(f, 4)}>
        <Headline>{b.headline}</Headline>
      </div>
      <div style={{ marginTop: 78, maxWidth: 1180 }}>
        {b.bars.map((bar: any) => (
          <div key={bar.label} style={{ marginBottom: 30 }}>
            <div
              style={{
                display: "flex",
                justifyContent: "space-between",
                ...MONO,
                fontSize: 24,
                marginBottom: 12,
              }}
            >
              <span>{bar.label}</span>
              <span style={{ color: bar.accent === "sage" ? SAGE : ROSE }}>
                {bar.display}
              </span>
            </div>
            <div
              style={{
                height: 18,
                background: "rgba(239,231,220,0.10)",
                borderRadius: 9,
                overflow: "hidden",
              }}
            >
              <div
                style={{
                  width: `${Math.min(100, bar.value * 5.4) * grow}%`,
                  height: "100%",
                  background: bar.accent === "sage" ? SAGE : ROSE,
                  borderRadius: 9,
                }}
              />
            </div>
          </div>
        ))}
        <div style={{ ...rise(f, 46), ...MONO, fontSize: 24 }}>{b.footnote}</div>
      </div>
    </div>
  );
};

const Kurva: React.FC<{ b: any; f: number }> = ({ b, f }) => {
  const draw = interpolate(f, [10, 55], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: EASE,
  });
  return (
    <div>
      <div style={rise(f, 0)}>
        <Kicker>{b.kicker}</Kicker>
      </div>
      <div style={rise(f, 4)}>
        <Headline size={64}>{b.headline}</Headline>
      </div>
      <div style={{ display: "flex", alignItems: "center", gap: 60, marginTop: 60 }}>
        <svg width={820} height={330} style={{ overflow: "visible" }}>
          <line x1="0" y1="310" x2="820" y2="310" stroke="rgba(239,231,220,0.18)" />
          <line x1="0" y1="0" x2="0" y2="310" stroke="rgba(239,231,220,0.18)" />
          <path
            d="M 0 270 C 240 250, 430 170, 820 34"
            fill="none"
            stroke={CREAM}
            strokeWidth={3}
            strokeDasharray={900}
            strokeDashoffset={900 * (1 - draw)}
          />
          <path
            d="M 0 210 C 250 250, 470 290, 820 296"
            fill="none"
            stroke={ROSE}
            strokeWidth={3}
            strokeDasharray={900}
            strokeDashoffset={900 * (1 - draw)}
          />
          <text x="430" y="26" fill={CREAM} fontFamily="Plex Mono" fontSize="20">
            {b.labelA}
          </text>
          <text x="470" y="318" fill={ROSE} fontFamily="Plex Mono" fontSize="20">
            {b.labelB}
          </text>
        </svg>
        <div
          style={{
            fontFamily: "Plex Mono",
            fontWeight: 500,
            fontSize: 128,
            color: ROSE,
            letterSpacing: "-0.03em",
            ...rise(f, 40),
          }}
        >
          {b.value}
        </div>
      </div>
    </div>
  );
};

const Prediktor: React.FC<{ b: any; f: number }> = ({ b, f }) => (
  <div>
    <div style={rise(f, 0)}>
      <Kicker>{b.kicker}</Kicker>
    </div>
    <div style={rise(f, 4)}>
      <Headline size={64}>{b.headline}</Headline>
    </div>
    <div style={{ marginTop: 74, maxWidth: 1120 }}>
      {b.rows.map((r: any, i: number) => (
        <div
          key={r.label}
          style={{
            ...rise(f, 16 + i * 14),
            display: "flex",
            justifyContent: "space-between",
            alignItems: "baseline",
            padding: "26px 0",
            borderTop: "1px solid rgba(239,231,220,0.16)",
          }}
        >
          <span style={{ ...SERIF, fontSize: 44 }}>{r.label}</span>
          <span
            style={{
              fontFamily: "Plex Mono",
              fontWeight: 500,
              fontSize: 58,
              color: r.tone === "sage" ? SAGE : ROSE,
            }}
          >
            {r.value}
          </span>
        </div>
      ))}
    </div>
  </div>
);

const Kontrafaktual: React.FC<{ b: any; f: number }> = ({ b, f }) => {
  const cells = Array.from({ length: 100 }, (_, i) => i);
  return (
    <div>
      <div style={rise(f, 0)}>
        <Kicker>{b.kicker}</Kicker>
      </div>
      <div style={rise(f, 4)}>
        <Headline>{b.headline}</Headline>
      </div>
      <div style={{ display: "flex", alignItems: "center", gap: 90, marginTop: 66 }}>
        <div
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(10, 44px)",
            gap: 9,
          }}
        >
          {cells.map((i) => {
            const on = i < 30;   // 30 dari 100 kotak = "+30%"
            const appear = interpolate(f, [6 + i * 0.25, 12 + i * 0.25], [0, 1], {
              extrapolateLeft: "clamp",
              extrapolateRight: "clamp",
            });
            return (
              <div
                key={i}
                style={{
                  width: 44,
                  height: 44,
                  borderRadius: 3,
                  background: on ? SAGE : "rgba(239,231,220,0.10)",
                  opacity: on ? appear : 0.55,
                }}
              />
            );
          })}
        </div>
        <div>
          <div
            style={{
              fontFamily: "Plex Mono",
              fontWeight: 500,
              fontSize: 132,
              color: SAGE,
              letterSpacing: "-0.03em",
              ...rise(f, 14),
            }}
          >
            {b.value}
          </div>
          <div style={{ ...MONO, fontSize: 24, maxWidth: 420, marginTop: 10 }}>
            {b.note}
          </div>
        </div>
      </div>
    </div>
  );
};

const Mekanisme: React.FC<{ b: any; f: number }> = ({ b, f }) => (
  <div>
    <div style={rise(f, 0)}>
      <Kicker>{b.kicker}</Kicker>
    </div>
    <div style={rise(f, 4)}>
      <Headline>{b.headline}</Headline>
    </div>
    <div style={{ display: "flex", gap: 40, marginTop: 74 }}>
      {[b.left, b.right].map((side: any, i: number) => (
        <div
          key={side.t}
          style={{
            ...rise(f, 18 + i * 12),
            flex: 1,
            border: "1px solid rgba(239,231,220,0.20)",
            borderRadius: 6,
            padding: "40px 44px",
            background: i === 1 ? "rgba(217,142,115,0.06)" : "transparent",
          }}
        >
          <div
            style={{
              ...SERIF,
              fontSize: 58,
              color: i === 1 ? ROSE : CREAM,
            }}
          >
            {side.t}
          </div>
          <div style={{ ...MONO, fontSize: 24, marginTop: 12, lineHeight: 1.5 }}>
            {side.d}
          </div>
        </div>
      ))}
    </div>
    <div
      style={{
        ...rise(f, 46),
        ...MONO,
        fontSize: 26,
        marginTop: 30,
        color: LILAC,
      }}
    >
      {b.note}
    </div>
  </div>
);

const Kutipan: React.FC<{ b: any; f: number }> = ({ b, f }) => (
  <div style={{ maxWidth: 1260 }}>
    <div style={rise(f, 0)}>
      <Kicker>{b.kicker}</Kicker>
    </div>
    <div
      style={{
        fontFamily: "Instrument Serif",
        fontStyle: "italic",
        fontSize: 78,
        lineHeight: 1.18,
        color: CREAM,
        ...rise(f, 10),
      }}
    >
      “{b.quote}”
    </div>
    <div style={{ ...rise(f, 34), ...MONO, fontSize: 24, marginTop: 34 }}>
      {b.attrib}
    </div>
  </div>
);

const Batas: React.FC<{ b: any; f: number }> = ({ b, f }) => (
  <div>
    <div style={rise(f, 0)}>
      <Kicker color={LILAC}>{b.kicker}</Kicker>
    </div>
    <div style={rise(f, 4)}>
      <Headline size={62}>{b.headline}</Headline>
    </div>
    <div style={{ display: "flex", gap: 16, marginTop: 54, flexWrap: "wrap" }}>
      {b.chips.map((c: string, i: number) => (
        <div
          key={c}
          style={{
            ...rise(f, 18 + i * 10),
            ...MONO,
            fontSize: 24,
            color: CREAM,
            border: "1px solid rgba(239,231,220,0.25)",
            borderRadius: 999,
            padding: "12px 26px",
          }}
        >
          {c}
        </div>
      ))}
    </div>
    <div
      style={{
        ...rise(f, 48),
        marginTop: 44,
        borderLeft: `3px solid ${LILAC}`,
        paddingLeft: 22,
        maxWidth: 900,
      }}
    >
      <div style={{ ...MONO, fontSize: 20, letterSpacing: "0.2em", color: LILAC }}>
        TIDAK DIKETAHUI
      </div>
      <div style={{ ...SERIF, fontSize: 38, marginTop: 10 }}>{b.unknown}</div>
    </div>
  </div>
);

const Tanya: React.FC<{ b: any; f: number }> = ({ b, f }) => (
  <div style={{ maxWidth: 1300 }}>
    <div style={rise(f, 0)}>
      <Kicker>{b.kicker}</Kicker>
    </div>
    <div style={{ ...SERIF, fontSize: 78, lineHeight: 1.16, ...rise(f, 8) }}>
      {b.question}
    </div>
    <div
      style={{
        width: 180,
        height: 4,
        background: ROSE,
        borderRadius: 2,
        marginTop: 52,
        ...rise(f, 30),
      }}
    />
  </div>
);

const SCENES: Record<string, React.FC<any>> = {
  adegan: Adegan,
  metode: Metode,
  bar: Bar,
  kurva: Kurva,
  prediktor: Prediktor,
  kontrafaktual: Kontrafaktual,
  mekanisme: Mekanisme,
  kutipan: Kutipan,
  batas: Batas,
  tanya: Tanya,
};

/* ---------------------------------------------------------------- frame */
export const LongForm: React.FC<LongProps> = ({
  tone,
  chapter,
  source,
  preview,
  blocks,
}) => {
  const ready = useFonts();
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();
  if (!ready) return <AbsoluteFill style={{ backgroundColor: "#0C1018" }} />;

  const active = blocks.find((b) => frame >= b.from && frame < b.to) ?? blocks[0];
  const Scene = SCENES[active.scene] ?? Adegan;
  const local = frame - active.from;

  return (
    <AbsoluteFill style={{ backgroundColor: "#0C1018" }}>
      <Backdrop tone={tone} knotSize={1500} />

      {!preview &&
        blocks.map((b, i) => (
          <Sequence key={i} from={b.from} durationInFrames={b.to - b.from}>
            <Audio src={staticFile(`audio/${b.vo}`)} />
          </Sequence>
        ))}

      {/* isi adegan, dipotong keras per blok supaya tidak ada transisi lambat */}
      <Sequence key={active.key} from={active.from} durationInFrames={active.to - active.from}>
        <AbsoluteFill
          style={{
            opacity: interpolate(local, [0, 8], [0, 1], {
              extrapolateLeft: "clamp",
              extrapolateRight: "clamp",
            }),
          }}
        >
        <AbsoluteFill
          style={{
            paddingLeft: M,
            paddingRight: M,
            paddingTop: 150,
            paddingBottom: 170,
            justifyContent: "center",
          }}
        >
          <Scene b={active} f={local} />
        </AbsoluteFill>
        </AbsoluteFill>
      </Sequence>

      {/* kepala & kaki: identitas + bab + sumber */}
      <div
        style={{
          position: "absolute",
          top: 56,
          left: M,
          right: M,
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          opacity: 0.75,
        }}
      >
        <div style={{ display: "flex", alignItems: "center", gap: 16 }}>
          <Img src={staticFile("logo-mark.png")} style={{ width: 38, height: 38 }} />
          <span
            style={{
              ...MONO,
              color: CREAM,
              fontSize: 20,
              letterSpacing: "0.30em",
            }}
          >
            KNOT THEORY
          </span>
        </div>
        <span style={{ ...MONO, fontSize: 19, letterSpacing: "0.22em" }}>
          {chapter}
        </span>
      </div>

      <div
        style={{
          position: "absolute",
          bottom: 62,
          left: M,
          right: M,
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
        }}
      >
        <span style={{ ...MONO, fontSize: 17, maxWidth: 1180 }}>{source}</span>
        <span style={{ ...MONO, fontSize: 17 }}>
          {String(Math.floor(frame / fps / 60)).padStart(2, "0")}:
          {String(Math.floor(frame / fps) % 60).padStart(2, "0")}
        </span>
      </div>

      <div
        style={{
          position: "absolute",
          left: 0,
          right: 0,
          bottom: 0,
          height: 3,
          background: "rgba(239,231,220,0.10)",
        }}
      >
        <div
          style={{
            width: `${Math.min(100, (frame / durationInFrames) * 100)}%`,
            height: "100%",
            background: ROSE,
            opacity: 0.8,
          }}
        />
      </div>
    </AbsoluteFill>
  );
};
