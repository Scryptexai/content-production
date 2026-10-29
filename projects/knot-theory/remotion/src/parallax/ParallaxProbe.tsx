/**
 * ParallaxProbe.tsx — uji terkontrol untuk parallax.
 *
 * Tiga penanda kontras tinggi di tiga kedalaman berbeda. Kalau parallax benar,
 * pergeseran penanda harus berbanding terbalik dengan jaraknya, dan rasionya
 * harus sama dengan rasio z. Ini yang membuktikan "berlapis" bukan klaim.
 */
import React from "react";
import { AbsoluteFill, useCurrentFrame, useVideoConfig } from "remotion";
import { cameraAt, layerStyle } from "./camera";

const Mark: React.FC<{ x: number; y: number; color: string; size: number }> = ({
  x,
  y,
  color,
  size,
}) => (
  <>
    <div
      style={{
        position: "absolute",
        left: x - size,
        top: y - size / 6,
        width: size * 2,
        height: size / 3,
        background: color,
      }}
    />
    <div
      style={{
        position: "absolute",
        left: x - size / 6,
        top: y - size,
        width: size / 3,
        height: size * 2,
        background: color,
      }}
    />
  </>
);

export const ParallaxProbe: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();
  const cam = cameraAt(frame / fps, durationInFrames / fps);

  const LAYERS = [
    { z: 3200, y: 200, c: "#FF3B30" }, // jauh
    { z: 1800, y: 480, c: "#34C759" }, // tengah
    { z: 900, y: 760, c: "#0A84FF" },  // dekat
    { z: 360, y: 940, c: "#FFD60A" },  // bidang aksi
  ];

  return (
    <AbsoluteFill style={{ backgroundColor: "#0A0A12" }}>
      {LAYERS.map((L) => (
        <div
          key={L.z}
          style={{ position: "absolute", inset: 0, ...layerStyle(cam, L.z, 0) }}
        >
          <Mark x={960} y={L.y} color={L.c} size={44} />
        </div>
      ))}
    </AbsoluteFill>
  );
};
