/**
 * ParallaxScene.tsx — 11 lapis kedalaman + kamera bergerak.
 *
 * Perbedaan dengan pipeline lama (satu plate Blender di belakang teks):
 * setiap lapis di sini punya z sendiri, jadi kamera yang sama menggeser
 * lapis dekat jauh lebih cepat daripada lapis jauh. Rasio pergeserannya
 * = z_jauh / z_dekat, dan itu bisa diukur.
 */
import React, { useEffect, useState } from "react";
import { AbsoluteFill, continueRender, delayRender, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { cameraAt, layerStyle } from "./camera";
import {
  Dust,
  Figure,
  Foreground,
  Grain,
  Mist,
  RidgeFar,
  RidgeNear,
  Sky,
  Stairs,
  Stars,
  STAIRS,
  Sun,
  RidgeMid,
  Vignette,
} from "./layers";

type Prim =
  | { t: "seg"; x1: number; y1: number; x2: number; y2: number; r1: number; r2: number; c: string }
  | { t: "dot"; x: number; y: number; r: number; c: string }
  | { t: "ell"; x: number; y: number; rx: number; ry: number; c: string }
  | { t: "poly"; c: string; pts: number[][] };

type FigureFile = {
  fps: number;
  frames: number;
  poses: { i: number; draw: Prim[] }[];
};

/** z setiap lapis. Angka ini yang menentukan rasio parallax. */
export const DEPTHS = {
  sky: 4000,
  stars: 3200,
  sun: 2600,
  ridgeFar: 1800,
  ridgeNear: 1300,
  ridgeMid: 900,
  mist: 780,
  stairs: 360,
  figure: 360, // figur MENEMPEL di tangga → z sama, kalau beda akan menggeser
  dust: 240,
  foreground: 90,
};

const useFigure = () => {
  const [data, setData] = useState<FigureFile | null>(null);
  const [handle] = useState(() => delayRender("memuat figure.json"));
  useEffect(() => {
    fetch(staticFile("parallax/figure.json"))
      .then((r) => r.json())
      .then((d: FigureFile) => {
        setData(d);
        continueRender(handle);
      })
      .catch(() => continueRender(handle));
  }, [handle]);
  return data;
};

/** Catatan: kabut TIDAK lagi ditumpuk sebagai kotak warna di atas lapis.
 *  Cara itu memutihkan siluet (kota jadi pilar abu-abu). Kabut sekarang
 *  dibakar ke warna isi tiap lapis — lihat layers.tsx. */
const Layer: React.FC<{
  z: number;
  cam: ReturnType<typeof cameraAt>;
  blurScale?: number;
  children: React.ReactNode;
}> = ({ z, cam, blurScale = 1, children }) => (
  <div style={{ position: "absolute", inset: 0, ...layerStyle(cam, z, blurScale) }}>
    {children}
  </div>
);

export const ParallaxScene: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();
  const t = frame / fps;
  const dur = durationInFrames / fps;
  const cam = cameraAt(t, dur);
  const fig = useFigure();

  const draw = fig ? fig.poses[Math.min(fig.poses.length - 1, frame)].draw : [];

  return (
    <AbsoluteFill style={{ backgroundColor: "#04060D", overflow: "hidden" }}>
      <Layer z={DEPTHS.sky} cam={cam}>
        <Sky />
      </Layer>
      <Layer z={DEPTHS.stars} cam={cam} blurScale={0}>
        <Stars t={t} />
      </Layer>
      <Layer z={DEPTHS.sun} cam={cam} blurScale={0}>
        <Sun />
      </Layer>
      <Layer z={DEPTHS.ridgeFar} cam={cam}>
        <RidgeFar />
      </Layer>
      <Layer z={DEPTHS.ridgeNear} cam={cam}>
        <RidgeNear />
      </Layer>
      <Layer z={DEPTHS.ridgeMid} cam={cam}>
        <RidgeMid />
      </Layer>
      <Layer z={DEPTHS.mist} cam={cam}>
        <Mist />
      </Layer>
      <Layer z={DEPTHS.stairs} cam={cam}>
        <Stairs />
      </Layer>
      <Layer z={DEPTHS.figure} cam={cam}>
        <Figure draw={draw} />
      </Layer>
      <Layer z={DEPTHS.dust} cam={cam}>
        <Dust t={t} />
      </Layer>
      <Layer z={DEPTHS.foreground} cam={cam}>
        <Foreground />
      </Layer>

      {/* lapis layar: tidak ikut parallax, memang menempel di lensa */}
      <Vignette />
      <Grain frame={frame} />
    </AbsoluteFill>
  );
};

export { STAIRS };
