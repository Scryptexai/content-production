import React from "react";
import { AbsoluteFill, Easing, interpolate, useCurrentFrame, useVideoConfig } from "remotion";
import { C, BRAND_BEZIER, W } from "../theme";
import { Monogram, Wordmark } from "../components/Marks";

/**
 * 0 – 2 s. The mark arrives: monogram settles, wordmark wipes in from the left.
 * Everything is a pure function of the frame.
 */
export const Build: React.FC = () => {
  const frame = useCurrentFrame();
  const { width } = useVideoConfig();
  const ease = Easing.bezier(...BRAND_BEZIER);

  const mono = interpolate(frame, [6, 36], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: ease,
  });
  const wipe = interpolate(frame, [34, 56], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: ease,
  });

  const monoWidth = 380 * (width / W);
  const cap = 118;
  const wmWidth = (cap * 928.6) / 100;

  return (
    <AbsoluteFill style={{ backgroundColor: C.ink, alignItems: "center", justifyContent: "center" }}>
      <div
        style={{
          marginTop: -120,
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
        }}
      >
        <div style={{ opacity: mono, transform: `scale(${0.93 + 0.07 * mono})` }}>
          <Monogram width={monoWidth} />
        </div>
        <div
          style={{
            marginTop: 74,
            width: wmWidth,
            height: cap * 1.04,
            overflow: "hidden",
            display: "flex",
            justifyContent: "flex-start",
          }}
        >
          <div
            style={{
              transform: `translateX(${(wipe - 1) * wmWidth}px)`,
              clipPath: `inset(0 ${100 - wipe * 100}% 0 0)`,
            }}
          >
            <Wordmark capHeight={cap} />
          </div>
        </div>
      </div>
    </AbsoluteFill>
  );
};
