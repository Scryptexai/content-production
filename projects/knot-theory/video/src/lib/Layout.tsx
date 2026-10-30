/**
 * Layout.tsx — panggung vertikal dengan ZONA TETAP.
 *
 * Kenapa dipisah: pada percobaan pertama, teks dan benda sama-sama diletakkan
 * dengan angka manual, dan hasilnya bertabrakan (angka "≈ 0" menimpa baris
 * penjelas; surat suara menutupi "3–13"). Di sini setiap pita punya
 * koordinat baku dan benda TIDAK PERNAH diletakkan di pita teks:
 *
 *   y 150   kicker
 *   y 214   judul / angka utama (maks 2 baris)
 *   y 500   baris pendukung
 *   y 620–1330  ZONA BENDA (satu-satunya tempat objek foto)
 *   y 1400  baris isi (maks 2 baris)
 *   y 1560  baris aksen (serif)
 *   y 1800  sumber
 *
 * Benda boleh melewati 620–1330 sedikit, tapi tidak boleh masuk pita teks;
 * itu dijaga oleh pemanggil, bukan oleh CSS.
 */
import React from 'react';
import { AbsoluteFill, useCurrentFrame } from 'remotion';
import { C, TYPE } from './theme';
import { EASE, clamp01, ramp } from './motion';

export const ZONE = {
  kick: 150,
  head: 214,
  sub: 496,
  objTop: 610,
  objMid: 985,
  objBottom: 1336,
  body: 1452,
  accent: 1586,
  source: 1798,
  margin: 84,
} as const;

export const BODY_MAX = 942; // lebar aman 1080 − 2×69

type FrameProps = {
  kicker?: React.ReactNode;
  /** konten pita judul */
  head?: React.ReactNode;
  sub?: React.ReactNode;
  /** lapisan benda (Photo) — di belakang teks */
  stage: React.ReactNode;
  body?: React.ReactNode;
  accent?: React.ReactNode;
  source?: React.ReactNode;
  /** kilau tambahan di atas segalanya */
  overlay?: React.ReactNode;
};

export const Frame: React.FC<FrameProps> = ({ kicker, head, sub, stage, body, accent, source, overlay }) => {
  const frame = useCurrentFrame();
  return (
    <AbsoluteFill style={{ background: C.ink, overflow: 'hidden' }}>
      {/* ruang + benda */}
      <AbsoluteFill style={{ zIndex: 1 }}>{stage}</AbsoluteFill>

      {/* teks selalu di atas benda, dengan pita yang tidak pernah diduduki */}
      <AbsoluteFill style={{ zIndex: 20, pointerEvents: 'none' }}>
        {kicker && (
          <div style={{ position: 'absolute', left: 0, right: 0, top: ZONE.kick, textAlign: 'center' }}>
            {kicker}
          </div>
        )}
        {head && (
          <div
            style={{
              position: 'absolute',
              left: ZONE.margin,
              right: ZONE.margin,
              top: ZONE.head,
              textAlign: 'center',
            }}
          >
            {head}
          </div>
        )}
        {sub && (
          <div style={{ position: 'absolute', left: 64, right: 64, top: ZONE.sub, textAlign: 'center' }}>
            {sub}
          </div>
        )}
        {body && (
          <div
            style={{
              position: 'absolute',
              left: ZONE.margin,
              right: ZONE.margin,
              top: ZONE.body,
              textAlign: 'center',
            }}
          >
            {body}
          </div>
        )}
        {accent && (
          <div style={{ position: 'absolute', left: 56, right: 56, top: ZONE.accent, textAlign: 'center' }}>
            {accent}
          </div>
        )}
        {source && (
          <div style={{ position: 'absolute', left: 40, right: 40, top: ZONE.source, textAlign: 'center' }}>
            {source}
          </div>
        )}
      </AbsoluteFill>

      {overlay}
    </AbsoluteFill>
  );
};

/**
 * Banda — garis rambut horizontal yang membingkai pita teks. Memberi tulang
 * pada tata letak, dan menandai batas zona benda tanpa harus menggambar kotak.
 */
export const Rule: React.FC<{ at?: number; y: number; w?: number; opacity?: number }> = ({
  at = 0,
  y,
  w = 300,
  opacity = 0.5,
}) => {
  const frame = useCurrentFrame();
  const p = ramp(frame, at, 26, EASE.out);
  return (
    <div
      style={{
        position: 'absolute',
        left: '50%',
        top: y,
        width: w * p,
        height: 1,
        transform: 'translateX(-50%)',
        background: `linear-gradient(90deg, ${C.muted2}00 0%, ${C.muted2}${Math.round(opacity * 255).toString(16).padStart(2, '0')} 50%, ${C.muted2}00 100%)`,
        opacity: clamp01(p * 1.2),
      }}
    />
  );
};
