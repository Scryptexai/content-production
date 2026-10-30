/**
 * Stage.tsx — ruangan tempat semua objek difoto ulang oleh kamera film.
 *
 * Ini pengganti "latar" biasa: bukan gambar yang ditempel di belakang objek,
 * melainkan ruang yang punya sumber cahaya, udara, dan lantai. Objek foto
 * diletakkan di dalamnya (lihat Photo.tsx), jadi bayangan, rim, dan kabut
 * saling menyambung dan objek terbaca sebagai benda di ruangan — bukan
 * potongan gambar yang ditempel.
 *
 * Lapisan, dari belakang ke depan:
 *   gradasi dinding → lampu utama (tungsten, kanan atas) → lampu isi dingin
 *   → berkas cahaya volumetrik → lantai + garis horizon → debu → vignette → grain
 */
import React from 'react';
import { AbsoluteFill, useCurrentFrame } from 'remotion';
import { C, alpha } from './theme';
import { seeded } from './motion';

export type RoomProps = {
  /** posisi lampu utama, 0–1 dari bingkai */
  keyLight?: { x: number; y: number };
  /** kekuatan lampu utama 0–1.6 */
  keyPower?: number;
  /** posisi lampu isi dingin; null = tanpa lampu isi */
  fill?: { x: number; y: number } | null;
  /** sudut berkas cahaya volumetrik (derajat) dan lebarnya */
  beam?: { angle: number; width: number; power: number } | null;
  /** tinggi garis lantai 0–1; null = tanpa lantai (ruang tanpa alas) */
  floor?: number | null;
  /** butir debu di udara */
  dust?: number;
  /** kekuatan vignette */
  vignette?: number;
  /** kekuatan grain 0–0.2 */
  grain?: number;
  /** denyut napas lampu 0–1 */
  breathe?: number;
};

export const Stage: React.FC<RoomProps & { children?: React.ReactNode }> = ({
  keyLight = { x: 0.74, y: 0.16 },
  keyPower = 1,
  fill = { x: 0.16, y: 0.92 },
  beam = { angle: -19, width: 0.52, power: 0.5 },
  floor = 0.79,
  dust = 46,
  vignette = 0.58,
  grain = 0.07,
  breathe = 0.35,
  children,
}) => {
  const frame = useCurrentFrame();
  const b = 1 + breathe * 0.06 * Math.sin(frame / 46);
  const k = keyPower * b;

  return (
    <AbsoluteFill style={{ background: C.ink, overflow: 'hidden' }}>
      {/* dinding: gelap di tepi, hangat di tempat lampu jatuh */}
      <AbsoluteFill
        style={{
          background:
            `radial-gradient(ellipse 78% 66% at ${keyLight.x * 100}% ${keyLight.y * 100}%, ${alpha(C.tungsten, 0.16 * k)} 0%, ${alpha(C.tungsten, 0.05 * k)} 34%, ${alpha(C.ink, 0)} 68%),` +
            `linear-gradient(184deg, #070A14 0%, #0A0E1B 38%, #11162A 66%, #080B14 100%)`,
        }}
      />
      {/* lampu isi dingin dari bawah kiri: memisahkan objek dari dinding */}
      {fill && (
        <AbsoluteFill
          style={{
            background: `radial-gradient(ellipse 62% 46% at ${fill.x * 100}% ${fill.y * 100}%, ${alpha(C.cool, 0.17)} 0%, ${alpha(C.cool, 0.05)} 42%, ${alpha(C.cool, 0)} 72%)`,
            mixBlendMode: 'screen',
          }}
        />
      )}
      {/* berkas cahaya volumetrik: trapesium dari lampu ke lantai */}
      {beam && (
        <AbsoluteFill style={{ opacity: beam.power * (0.85 + 0.15 * Math.sin(frame / 71)) }}>
          <div
            style={{
              position: 'absolute',
              left: `${keyLight.x * 100 - beam.width * 50}%`,
              top: `${keyLight.y * 100}%`,
              width: `${beam.width * 100}%`,
              height: '150%',
              transformOrigin: 'top center',
              transform: `rotate(${beam.angle}deg)`,
              background: `linear-gradient(180deg, ${alpha(C.tungsten, 0.18)} 0%, ${alpha(C.tungsten, 0.07)} 38%, ${alpha(C.tungsten, 0)} 88%)`,
              filter: 'blur(26px)',
            }}
          />
          <div
            style={{
              position: 'absolute',
              left: `${keyLight.x * 100 - beam.width * 22}%`,
              top: `${keyLight.y * 100}%`,
              width: `${beam.width * 44}%`,
              height: '140%',
              transformOrigin: 'top center',
              transform: `rotate(${beam.angle}deg)`,
              background: `linear-gradient(180deg, ${alpha(C.tungsten, 0.22)} 0%, ${alpha(C.tungsten, 0.06)} 46%, ${alpha(C.tungsten, 0)} 82%)`,
              filter: 'blur(12px)',
            }}
          />
        </AbsoluteFill>
      )}
      {/* lantai: satu garis horizon tipis + gradasi gelap di bawahnya */}
      {floor !== null && (
        <>
          <div
            style={{
              position: 'absolute',
              left: '-10%',
              right: '-10%',
              top: `${floor * 100 - 8}%`,
              height: '22%',
              background: `radial-gradient(ellipse 46% 52% at 50% 24%, ${alpha(C.tungsten, 0.13)} 0%, ${alpha(C.tungsten, 0)} 74%)`,
              filter: 'blur(16px)',
            }}
          />
          <div
            style={{
              position: 'absolute',
              left: 0,
              right: 0,
              top: `${floor * 100}%`,
              bottom: 0,
              background: `linear-gradient(180deg, ${alpha('#050810', 0.55)} 0%, #03050B 62%)`,
            }}
          />
          <div
            style={{
              position: 'absolute',
              left: 0,
              right: 0,
              top: `${floor * 100}%`,
              height: 1.5,
              background: `linear-gradient(90deg, ${alpha(C.rose, 0)} 0%, ${alpha(C.rose, 0.42)} 32%, ${alpha(C.tungsten, 0.5)} 58%, ${alpha(C.rose, 0)} 100%)`,
            }}
          />
        </>
      )}
      {/* debu di udara: hanya di sisi cahaya, pelan, deterministik */}
      {dust > 0 && <Dust count={dust} />}
      {children}
      {/* vignette + grain selalu paling atas */}
      <AbsoluteFill
        style={{
          pointerEvents: 'none',
          background: `radial-gradient(ellipse 68% 62% at 50% 44%, ${alpha('#000000', 0)} 28%, ${alpha('#000000', vignette * 0.45)} 74%, ${alpha('#000000', vignette)} 100%)`,
        }}
      />
      <Grain opacity={grain} />
    </AbsoluteFill>
  );
};

const Dust: React.FC<{ count: number }> = ({ count }) => {
  const frame = useCurrentFrame();
  return (
    <div style={{ position: 'absolute', inset: 0, pointerEvents: 'none' }}>
      {Array.from({ length: count }, (_, i) => {
        const z = seeded(i * 3.7 + 1);
        const size = 2 + z * z * 11;
        const x0 = seeded(i * 7.1 + 2) * 1180 - 50;
        const y0 = seeded(i * 5.3 + 3) * 1900 - 40;
        const drift = 0.16 + z * 0.5;
        const x = ((x0 + frame * drift * (0.4 + z)) % 1180 + 1180) % 1180 - 50;
        const y = ((y0 - frame * drift * 0.42) % 1980 + 1980) % 1980 - 40;
        const tw = 0.45 + 0.55 * Math.sin(frame / (18 + z * 26) + i);
        return (
          <div
            key={i}
            style={{
              position: 'absolute',
              left: x,
              top: y,
              width: size,
              height: size,
              borderRadius: '50%',
              background: `radial-gradient(circle, ${alpha(C.tungsten, 0.85)} 0%, ${alpha(C.tungsten, 0)} 72%)`,
              opacity: (0.16 + 0.5 * tw) * (0.3 + z * 0.7),
              filter: z > 0.72 ? `blur(${((z - 0.72) * 9).toFixed(1)}px)` : undefined,
            }}
          />
        );
      })}
    </div>
  );
};

const GRAIN_CACHE = new Map<number, string>();
const grainTile = (variant: number) => {
  const hit = GRAIN_CACHE.get(variant);
  if (hit) return hit;
  const svg =
    `<svg xmlns='http://www.w3.org/2000/svg' width='220' height='220'>` +
    `<filter id='g' x='0' y='0' width='100%' height='100%' color-interpolation-filters='sRGB'>` +
    `<feTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='2' seed='${variant * 13 + 5}' stitchTiles='stitch'/>` +
    `<feColorMatrix type='matrix' values='0.33 0.33 0.33 0 0 0.33 0.33 0.33 0 0 0.33 0.33 0.33 0 0 0 0 0 0 1'/>` +
    `<feComponentTransfer><feFuncR type='linear' slope='2.6' intercept='-0.8'/><feFuncG type='linear' slope='2.6' intercept='-0.8'/><feFuncB type='linear' slope='2.6' intercept='-0.8'/></feComponentTransfer>` +
    `</filter><rect width='100%' height='100%' filter='url(#g)'/></svg>`;
  const url = `url("data:image/svg+xml;utf8,${encodeURIComponent(svg)}")`;
  GRAIN_CACHE.set(variant, url);
  return url;
};

export const Grain: React.FC<{ opacity?: number }> = ({ opacity = 0.07 }) => {
  const frame = useCurrentFrame();
  const k = Math.floor(frame / 2);
  const ox = Math.floor(seeded(k * 3 + 1) * 220);
  const oy = Math.floor(seeded(k * 7 + 2) * 220);
  return (
    <AbsoluteFill
      style={{
        pointerEvents: 'none',
        opacity,
        mixBlendMode: 'overlay',
        backgroundImage: grainTile(k % 6),
        backgroundSize: '220px 220px',
        backgroundPosition: `${ox}px ${oy}px`,
      }}
    />
  );
};
