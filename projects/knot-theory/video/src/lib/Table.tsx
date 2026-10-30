/**
 * Table.tsx — meja tempat benda diletakkan.
 *
 * Tanpa permukaan, objek foto terbaca melayang di ruang kosong. Meja ini
 * bukan latar: ia punya perspektif (garis-garis yang mengecil ke belakang),
 * kilau dari lampu, dan menerima bayangan kontak dari Photo.
 */
import React from 'react';
import { useCurrentFrame } from 'remotion';
import { C, alpha } from './theme';

export const Table: React.FC<{
  /** posisi garis belakang meja (0–1 tinggi bingkai) */
  back?: number;
  /** intensitas kilau dari lampu */
  shine?: number;
  /** pergeseran kamera untuk parallax garis */
  pan?: number;
  opacity?: number;
}> = ({ back = 0.66, shine = 0.55, pan = 0, opacity = 1 }) => {
  const frame = useCurrentFrame();
  const breathe = 1 + 0.04 * Math.sin(frame / 58);

  return (
    <div style={{ position: 'absolute', inset: 0, opacity, pointerEvents: 'none' }}>
      {/* bidang meja: lebih terang di belakang, gelap ke depan */}
      <div
        style={{
          position: 'absolute',
          left: 0,
          right: 0,
          top: `${back * 100}%`,
          bottom: 0,
          background: `linear-gradient(180deg, ${alpha('#2A3247', 0.55)} 0%, ${alpha('#141A29', 0.92)} 26%, #06080F 100%)`,
        }}
      />
      {/* kilau lampu di permukaan */}
      <div
        style={{
          position: 'absolute',
          left: 0,
          right: 0,
          top: `${back * 100 - 12}%`,
          height: '34%',
          background: `radial-gradient(ellipse 52% 60% at ${58 + pan * 4}% 12%, ${alpha(C.tungsten, 0.2 * shine * breathe)} 0%, ${alpha(C.tungsten, 0.05 * shine)} 46%, ${alpha(C.tungsten, 0)} 74%)`,
          filter: 'blur(12px)',
        }}
      />
      {/* garis perspektif: makin ke depan makin lebar & redup */}
      <div style={{ position: 'absolute', inset: 0, overflow: 'hidden' }}>
        {Array.from({ length: 9 }, (_, i) => {
          const t = i / 8;
          const y = back * 100 + Math.pow(t, 1.7) * (100 - back * 100);
          return (
            <div
              key={i}
              style={{
                position: 'absolute',
                left: '-12%',
                right: '-12%',
                top: `${y}%`,
                height: 1,
                background: `linear-gradient(90deg, ${alpha(C.cream, 0)} 0%, ${alpha(C.cream, 0.1 - 0.06 * t)} 34%, ${alpha(C.cream, 0.12 - 0.07 * t)} 62%, ${alpha(C.cream, 0)} 100%)`,
                transform: `translateY(${((pan % 1) * 40).toFixed(2)}px)`,
              }}
            />
          );
        })}
      </div>
      {/* tepi belakang meja: garis horizon tipis */}
      <div
        style={{
          position: 'absolute',
          left: 0,
          right: 0,
          top: `${back * 100}%`,
          height: 1.4,
          background: `linear-gradient(90deg, ${alpha(C.rose, 0)} 0%, ${alpha(C.rose, 0.3)} 30%, ${alpha(C.tungsten, 0.42)} 54%, ${alpha(C.rose, 0)} 100%)`,
        }}
      />
    </div>
  );
};
