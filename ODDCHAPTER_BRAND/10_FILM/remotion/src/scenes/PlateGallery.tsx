import React from "react";
import { AbsoluteFill, useCurrentFrame } from "remotion";
import { C, H, MARGIN, W } from "../theme";
import { PlateArt, PlateKind } from "./PlateArt";

/**
 * PlateGallery — 10 frame, 10 bentuk dasar. Satu-satunya cara memeriksa apakah
 * semua plate masih satu keluarga sebelum 21 episode dirender.
 *
 *   node scripts/still-plates.mjs   ->  output/plates/plate_00..09.png
 */

export const KINDS: PlateKind[] = ["tower", "vessel", "shelter", "road", "paper", "signal", "plume", "water", "dial", "ridge"];

export const PlateGallery: React.FC = () => {
  const frame = useCurrentFrame();
  const kind = KINDS[Math.min(frame, KINDS.length - 1)];
  return (
    <AbsoluteFill style={{ backgroundColor: C.ink }}>
      <AbsoluteFill style={{ background: `radial-gradient(120% 60% at 50% ${H * 0.7}px, #24282E 0%, #17191D 48%, #0D0F12 100%)` }} />
      <svg width={W} height={H} viewBox={`0 0 ${W} ${H}`} style={{ position: "absolute" }}>
        <PlateArt kind={kind} lamp={1} />
      </svg>
      <AbsoluteFill style={{ background: "linear-gradient(180deg, rgba(13,15,18,0.5) 0%, rgba(13,15,18,0) 28%, rgba(13,15,18,0) 60%, rgba(13,15,18,0.92) 100%)" }} />
      <div style={{ position: "absolute", left: MARGIN, bottom: 240, fontFamily: "Space Grotesk", fontWeight: 700, fontSize: 210, letterSpacing: "-0.04em", color: C.orange }}>
        {String(Math.min(frame, KINDS.length - 1) + 1).padStart(2, "0")}
      </div>
      <div style={{ position: "absolute", left: MARGIN, bottom: 190, fontFamily: "Inter", fontWeight: 600, fontSize: 30, letterSpacing: "0.3em", color: C.sage }}>
        {kind.toUpperCase()}
      </div>
    </AbsoluteFill>
  );
};
