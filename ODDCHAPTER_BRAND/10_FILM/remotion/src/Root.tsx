import React from "react";
import { AbsoluteFill, Composition, Easing, interpolate, useCurrentFrame } from "remotion";
import { TransitionSeries, springTiming } from "@remotion/transitions";
import { slide } from "@remotion/transitions/slide";
import "./fonts";
import { Film } from "./Film";
import { Captions } from "./scenes/Captions";
import { Episode } from "./scenes/Episode";
import timingJson from "./timing.generated.json";
import { BRAND_BEZIER, C, FPS, H, T, W } from "./theme";
import { Monogram, Wordmark } from "./components/Marks";

const ease = Easing.bezier(...BRAND_BEZIER);

/** One static frame — proves the browser can rasterise type and the marks. */
const FilmCaptioned: React.FC = () => (
  <>
    <Film />
    <Captions />
  </>
);

const TestFrame: React.FC = () => (
  <AbsoluteFill style={{ backgroundColor: C.ink, alignItems: "center", justifyContent: "center" }}>
    <Monogram width={360} />
    <div style={{ marginTop: 64 }}>
      <Wordmark capHeight={92} />
    </div>
    <div
      style={{
        marginTop: 48,
        fontFamily: "Inter",
        fontWeight: 500,
        fontSize: 26,
        letterSpacing: "0.24em",
        color: C.sage,
      }}
    >
      STATIC FRAME TEST
    </div>
  </AbsoluteFill>
);

/** One animated scene + one transition — the pre-flight video. */
const TestMotion: React.FC = () => {
  const frame = useCurrentFrame();
  const p = interpolate(frame, [0, 30], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: ease,
  });
  return (
    <AbsoluteFill style={{ backgroundColor: C.ink, alignItems: "center", justifyContent: "center" }}>
      <div style={{ opacity: p, transform: `scale(${0.9 + 0.1 * p})` }}>
        <Monogram width={420} />
      </div>
      <div
        style={{
          marginTop: 60,
          fontFamily: "Space Grotesk",
          fontWeight: 700,
          fontSize: 64,
          color: C.ivory,
          opacity: p,
          letterSpacing: "0.02em",
        }}
      >
        RENDER TEST
      </div>
      <div
        style={{
          marginTop: 26,
          fontFamily: "Inter",
          fontWeight: 500,
          fontSize: 24,
          letterSpacing: "0.22em",
          color: C.sage,
          opacity: p,
        }}
      >
        CHROMIUM · REMOTION · 1080×1920
      </div>
    </AbsoluteFill>
  );
};

const Card: React.FC<{ bg: string; label: string }> = ({ bg, label }) => (
  <AbsoluteFill style={{ backgroundColor: bg, alignItems: "center", justifyContent: "center" }}>
    <div style={{ fontFamily: "Space Grotesk", fontWeight: 700, fontSize: 90, color: C.ink }}>{label}</div>
  </AbsoluteFill>
);

/**
 * TransitionSeries is installed and tested here, then deliberately *not* used in
 * the film: the brand cuts hard between scenes and forbids dissolves.
 */
const TestTransition: React.FC = () => (
  <TransitionSeries>
    <TransitionSeries.Sequence durationInFrames={22}>
      <Card bg={C.ivory} label="A" />
    </TransitionSeries.Sequence>
    <TransitionSeries.Transition presentation={slide()} timing={springTiming({ config: { damping: 200 }, durationInFrames: 14 })} />
    <TransitionSeries.Sequence durationInFrames={22}>
      <Card bg={C.sage} label="B" />
    </TransitionSeries.Sequence>
  </TransitionSeries>
);

export const RemotionRoot: React.FC = () => (
  <>
    <Composition
      id="ODDCHAPTER-PILOT-001"
      component={Film}
      durationInFrames={T.total}
      fps={FPS}
      width={W}
      height={H}
    />
    <Composition
      id="ODDCHAPTER-PILOT-001-CAPTIONS"
      component={FilmCaptioned}
      durationInFrames={T.total}
      fps={FPS}
      width={W}
      height={H}
    />
    {(Object.keys(timingJson) as string[]).map((epId) => (
      <Composition
        key={epId}
        id={`ODDCHAPTER-${epId}`}
        component={Episode}
        defaultProps={{ epId }}
        durationInFrames={(timingJson as any)[epId].totalFrames}
        fps={FPS}
        width={W}
        height={H}
      />
    ))}
    <Composition id="TEST-FRAME" component={TestFrame} durationInFrames={1} fps={FPS} width={W} height={H} />
    <Composition id="TEST-MOTION" component={TestMotion} durationInFrames={FPS * 3} fps={FPS} width={W} height={H} />
    <Composition id="TEST-TRANSITION" component={TestTransition} durationInFrames={30} fps={FPS} width={W} height={H} />
  </>
);
