import React from "react";
import { AbsoluteFill, Easing, interpolate, useCurrentFrame } from "remotion";
import { BRAND_BEZIER, C, W } from "../theme";
import { Monogram, Tagline, Wordmark } from "../components/Marks";

const ease = Easing.bezier(...BRAND_BEZIER);

export const EndCard: React.FC = () => {
  const frame = useCurrentFrame();

  const mark = interpolate(frame, [0, 22], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: ease,
  });
  const word = interpolate(frame, [14, 34], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: ease,
  });
  const rule = interpolate(frame, [34, 46], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: ease,
  });
  const tag = interpolate(frame, [44, 60], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: ease,
  });
  // last 10 frames settle to ink so the file does not end on a hard stop
  const out = interpolate(frame, [200, 210], [1, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  return (
    <AbsoluteFill style={{ backgroundColor: C.ink, alignItems: "center", justifyContent: "center" }}>
      <div style={{ marginTop: -170, display: "flex", flexDirection: "column", alignItems: "center", opacity: out }}>
        <div style={{ opacity: mark, transform: `scale(${0.94 + 0.06 * mark})` }}>
          <Monogram width={300 * (W / W)} />
        </div>
        <div style={{ marginTop: 84, opacity: word, transform: `translateY(${(1 - word) * 14}px)` }}>
          <Wordmark capHeight={96} />
        </div>
        <div
          style={{
            marginTop: 62,
            width: 120 * rule,
            height: 4,
            backgroundColor: C.orange,
          }}
        />
        <div style={{ marginTop: 44, opacity: tag, transform: `translateY(${(1 - tag) * 10}px)` }}>
          <Tagline width={620} />
        </div>
      </div>
    </AbsoluteFill>
  );
};
