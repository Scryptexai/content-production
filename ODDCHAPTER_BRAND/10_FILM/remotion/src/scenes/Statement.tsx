import React from "react";
import { AbsoluteFill, Easing, interpolate, useCurrentFrame } from "remotion";
import { BRAND_BEZIER, C, MARGIN } from "../theme";

const ease = Easing.bezier(...BRAND_BEZIER);

type Line = {
  text: string;
  size: number;
  weight: 300 | 500 | 700;
  color?: string;
  opacity?: number;
  tracking?: number;
  family?: "grotesk" | "inter";
  gapBefore?: number;
};

const rise = (frame: number, start: number) => {
  const t = interpolate(frame, [start, start + 16], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: ease,
  });
  return { opacity: t, transform: `translateY(${(1 - t) * 26}px)` };
};

export const Statement: React.FC<{
  eyebrow: string;
  eyebrowTracking?: number;
  lines: Line[];
}> = ({ eyebrow, eyebrowTracking = 0.22, lines }) => {
  const frame = useCurrentFrame();

  const ruleW = interpolate(frame, [0, 14], [0, 96], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: ease,
  });

  return (
    <AbsoluteFill style={{ backgroundColor: C.ink }}>
      <div style={{ position: "absolute", left: MARGIN, top: 620 }}>
        <div style={{ width: ruleW, height: 4, backgroundColor: C.orange }} />
        <div
          style={{
            ...rise(frame, 4),
            marginTop: 42,
            fontFamily: "Inter",
            fontWeight: 600,
            fontSize: 30,
            letterSpacing: `${eyebrowTracking}em`,
            color: C.sage,
            textTransform: "uppercase",
          }}
        >
          {eyebrow}
        </div>

        {lines.map((line, i) => (
          <div
            key={line.text}
            style={{
              ...rise(frame, 10 + i * 5),
              marginTop: i === 0 ? 44 : (line.gapBefore ?? 8),
              fontFamily: line.family === "inter" ? "Inter" : "Space Grotesk",
              fontWeight: line.weight,
              fontSize: line.size,
              lineHeight: 1,
              letterSpacing: `${line.tracking ?? 0}em`,
              color: line.color ?? C.ivory,
              opacity: line.opacity,
              textTransform: "uppercase",
              whiteSpace: "nowrap",
            }}
          >
            {line.text}
          </div>
        ))}
      </div>
    </AbsoluteFill>
  );
};

/** Scene 1 copy — verbatim narration, no claim the voice does not make. */
export const SCENE_1_LINES: Line[] = [
  { text: "SATU KISAH NYATA", size: 103, weight: 700 },
  { text: "YANG BERAKHIR", size: 56, weight: 300, opacity: 0.74, tracking: 0.02, gapBefore: 26 },
  { text: "JAUH DARI", size: 56, weight: 300, opacity: 0.74, tracking: 0.02 },
  { text: "DUGAAN.", size: 56, weight: 300, opacity: 0.74, tracking: 0.02 },
];

/** Scene 2 copy. */
export const SCENE_2_LINES: Line[] = [
  { text: "LEBIH", size: 190, weight: 700 },
  { text: "ANEH", size: 190, weight: 700 },
  { text: "DARIPADA YANG KITA BAYANGKAN", size: 42, weight: 300, opacity: 0.7, tracking: 0.02, gapBefore: 30 },
];
