import React from "react";
import { AbsoluteFill, useCurrentFrame, useVideoConfig } from "remotion";
import { C, MARGIN } from "../theme";

/**
 * Burned-in Indonesian captions for the short-form cut.
 *
 * Cue boundaries are not estimated: they are the measured speech onset/offset of
 * each narration clip (20 ms window, peak threshold) — see 10_FILM/captions/.

 * The cue table is generated from the SRT by scripts/prepare-assets.mjs, so the
 * SRT stays the single source of truth.
 */
import cues from "../captions.generated.json";

type Cue = { startMs: number; endMs: number; text: string };

export const Captions: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = (frame / fps) * 1000;

  const cue = (cues as Cue[]).find((c) => t >= c.startMs && t <= c.endMs);
  if (!cue) return null;

  // 200 ms ease-in from the cue start, no exit animation (social captions shouldn't fade out)
  const appear = Math.min(1, Math.max(0, (t - cue.startMs) / 200));

  return (
    <AbsoluteFill style={{ pointerEvents: "none" }}>
      <div
        style={{
          position: "absolute",
          left: MARGIN,
          right: MARGIN,
          top: 1360,
          display: "flex",
          justifyContent: "center",
        }}
      >
        <div
          style={{
            backgroundColor: "rgba(23,25,29,0.86)",
            padding: "18px 26px",
            maxWidth: 900,
            opacity: appear,
            transform: `translateY(${(1 - appear) * 8}px)`,
          }}
        >
          <div
            style={{
              fontFamily: "Inter",
              fontWeight: 600,
              fontSize: 42,
              lineHeight: 1.28,
              color: C.ivory,
              textAlign: "center",
              textWrap: "balance",
            }}
          >
            {cue.text}
          </div>
        </div>
      </div>
    </AbsoluteFill>
  );
};
