import { AbsoluteFill, Audio, Img, OffthreadVideo, Sequence, staticFile, useCurrentFrame, useVideoConfig, interpolate, Easing } from "remotion";
import React from "react";
import { useFonts } from "./fonts";
import { ACCENTS, CREAM, MUTED, ROSE, SAGE, LILAC } from "./palette";

export type BeatKind = "hook" | "statement" | "number" | "pair" | "note" | "close";

export type Beat = {
  kind: BeatKind;
  vo: string;
  text: string;
  screen?: string[];
  from: number;
  to: number;
};

export type ShortProps = {
  id: string;
  plate: string;
  accent: keyof typeof ACCENTS;
  beats: Beat[];
};

const EASE = Easing.bezier(0.22, 1, 0.36, 1);
const SAFE = { top: 180, bottom: 320, x: 96 };

/* ------------------------------------------------------------------ atom */
const Fade: React.FC<{ children: React.ReactNode; delay?: number }> = ({ children, delay = 0 }) => {
  const frame = useCurrentFrame();
  const o = interpolate(frame - delay, [0, 14], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: EASE,
  });
  const y = interpolate(frame - delay, [0, 22], [26, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: EASE,
  });
  return <div style={{ opacity: o, transform: `translateY(${y}px)` }}>{children}</div>;
};

const Kicker: React.FC<{ text: string }> = ({ text }) => (
  <div
    style={{
      fontFamily: "Plex Mono",
      fontSize: 30,
      letterSpacing: "0.22em",
      color: MUTED,
      textTransform: "uppercase",
      marginBottom: 34,
    }}
  >
    {text}
  </div>
);

/* ------------------------------------------------------------------ slide */
const Slide: React.FC<{ beat: Beat }> = ({ beat }) => {
  const { width } = useVideoConfig();
  const maxW = width - SAFE.x * 2;

  if (beat.kind === "number" || beat.kind === "pair") {
    const lines = beat.screen ?? [];
    return (
      <div style={{ width: maxW }}>
        <Kicker text={beat.kind === "pair" ? "dua arah" : "temuan"} />
        {lines.map((line, i) => (
          <Fade key={line} delay={8 + i * 10}>
            <div
              style={{
                fontFamily: "Plex Mono",
                fontWeight: 500,
                fontSize: line.length > 12 ? 96 : 168,
                lineHeight: 1.02,
                letterSpacing: "-0.02em",
                color: i === 0 ? ACCENTS[beat.kind === "pair" ? "sage" : "rose"] : CREAM,
                marginBottom: 18,
              }}
            >
              {line}
            </div>
          </Fade>
        ))}
        <Fade delay={26 + lines.length * 10}>
          <div
            style={{
              fontFamily: "Instrument Serif",
              fontSize: 52,
              lineHeight: 1.22,
              color: CREAM,
              marginTop: 26,
              maxWidth: maxW,
            }}
          >
            {beat.text}
          </div>
        </Fade>
      </div>
    );
  }

  if (beat.kind === "close") {
    return (
      <div style={{ width: maxW }}>
        <Fade>
          <div
            style={{
              fontFamily: "Instrument Serif",
              fontSize: 82,
              lineHeight: 1.14,
              color: CREAM,
            }}
          >
            {beat.text}
          </div>
        </Fade>
        <Fade delay={30}>
          <div
            style={{
              width: 190,
              height: 4,
              background: ROSE,
              marginTop: 54,
              borderRadius: 2,
            }}
          />
        </Fade>
      </div>
    );
  }

  // hook / statement / note
  return (
    <div style={{ width: maxW }}>
      <Fade>
        <div
          style={{
            fontFamily: "Instrument Serif",
            fontSize: beat.kind === "hook" ? 92 : 74,
            lineHeight: 1.12,
            color: CREAM,
          }}
        >
          {beat.text}
        </div>
      </Fade>
      {beat.screen?.length ? (
        <Fade delay={22}>
          <div
            style={{
              fontFamily: "Plex Mono",
              fontSize: 40,
              color: beat.kind === "note" ? LILAC : SAGE,
              letterSpacing: "0.04em",
              marginTop: 48,
            }}
          >
            {beat.screen[0]}
          </div>
        </Fade>
      ) : null}
    </div>
  );
};

/* ------------------------------------------------------------------ root */
export const KnotShort: React.FC<ShortProps> = ({ id, plate, accent, beats }) => {
  const fontsReady = useFonts();
  const { fps } = useVideoConfig();
  const total = beats.length ? beats[beats.length - 1].to : 1;

  if (!fontsReady) return <AbsoluteFill style={{ backgroundColor: "#0C1018" }} />;

  return (
    <AbsoluteFill style={{ backgroundColor: "#0C1018" }}>
      {/* plate bergerak: tidak pernah statis */}
      <OffthreadVideo
        src={staticFile(`plates/${plate}-loop.mp4`)}
        muted
        loop
        style={{
          position: "absolute",
          inset: 0,
          width: "100%",
          height: "100%",
          objectFit: "cover",
        }}
      />

      {/* vignette tipis + scrim bawah untuk teks */}
      <AbsoluteFill
        style={{
          background:
            "radial-gradient(120% 80% at 50% 42%, rgba(0,0,0,0) 38%, rgba(4,6,10,0.55) 100%)",
        }}
      />

      {beats.map((b, i) => (
        <Sequence key={i} from={b.from} durationInFrames={b.to - b.from}>
          <Audio src={staticFile(`audio/${b.vo}`)} />
          <AbsoluteFill
            style={{
              paddingTop: SAFE.top,
              paddingBottom: SAFE.bottom,
              paddingLeft: SAFE.x,
              paddingRight: SAFE.x,
              justifyContent: "center",
            }}
          >
            <Slide beat={b} />
          </AbsoluteFill>
        </Sequence>
      ))}

      {/* identitas kecil, selalu ada, di atas UI platform */}
      <div
        style={{
          position: "absolute",
          left: SAFE.x,
          top: 96,
          display: "flex",
          alignItems: "center",
          gap: 16,
          opacity: 0.72,
        }}
      >
        <Img src={staticFile("logo-mark.png")} style={{ width: 52, height: 52 }} />
        <span
          style={{
            fontFamily: "Plex Mono",
            fontSize: 26,
            letterSpacing: "0.30em",
            color: CREAM,
          }}
        >
          KNOT THEORY
        </span>
      </div>

      {/* progress garis tipis di bawah */}
      <Progress total={total} fps={fps} accent={ACCENTS[accent]} />
    </AbsoluteFill>
  );
};

const Progress: React.FC<{ total: number; fps: number; accent: string }> = ({ total, fps, accent }) => {
  const frame = useCurrentFrame();
  const p = Math.min(1, frame / Math.max(1, total));
  return (
    <div style={{ position: "absolute", left: 0, right: 0, bottom: 0, height: 4, background: "rgba(239,231,220,0.10)" }}>
      <div style={{ width: `${p * 100}%`, height: "100%", background: accent, opacity: 0.85 }} />
    </div>
  );
};
