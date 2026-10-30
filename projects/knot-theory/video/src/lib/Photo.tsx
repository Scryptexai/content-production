/**
 * Photo.tsx — objek foto (PNG hasil chroma key) sebagai ELEMEN di dalam scene.
 *
 * Ini bagian yang diminta: foto tidak dipakai sebagai latar. Setiap foto
 * adalah benda yang diletakkan di ruang yang sama dengan kamera, jadi ia
 * punya:
 *   - parallax sendiri (depth): jauh = bergerak lebih lambat & mengecil
 *   - bayangan kontak di lantai/bidang di bawahnya, melebar saat benda naik
 *   - rim light hangat di tepi (mengikuti alfa foto, bukan kotaknya)
 *   - penyelarasan warna (grade) supaya tidak terlihat ditempel
 *   - defocus untuk benda yang jauh dari bidang fokus
 *
 * Semua nilai adalah fungsi murni dari frame: render bisa diulang persis.
 */
import React from 'react';
import { Img, staticFile } from 'remotion';
import { C, alpha } from './theme';
import { clamp01, project } from './motion';

export type Cam = { x: number; y: number; zoom: number; rot?: number };

export type PhotoProps = {
  /** nama berkas tanpa ekstensi, di public/objects/ */
  src: string;
  /** ukuran lebar dalam px pada skala kamera 1 */
  w: number;
  /** posisi dunia relatif titik tengah panggung */
  at: { x: number; y: number; z?: number };
  cam: Cam;
  center: { x: number; y: number };
  /** rotasi benda, derajat */
  rx?: number;
  ry?: number;
  rz?: number;
  /** 0 = menempel, 1 = melayang tinggi (bayangan melebar & memudar) */
  lift?: number;
  opacity?: number;
  /** blur defokus px */
  blur?: number;
  /** peredupan untuk benda yang jauh (0–1) */
  dim?: number;
  /** kekuatan rim light 0–1 */
  rim?: number;
  /** bayangan kontak 0–1 */
  shadow?: number;
  /** true = benda di belakang bidang fokus (tidak menutupi teks) */
  behind?: boolean;
  /** warna rim; default tungsten */
  rimColor?: string;
  /** kilau sekali jalan 0–1 (mis. saat objek mendarat) */
  sheen?: number;
  style?: React.CSSProperties;
};

export const Photo: React.FC<PhotoProps> = ({
  src,
  w,
  at,
  cam,
  center,
  rx = 0,
  ry = 0,
  rz = 0,
  lift = 0.4,
  opacity = 1,
  blur = 0,
  dim = 0,
  rim = 0.5,
  shadow = 0.55,
  behind = false,
  rimColor = C.tungsten,
  sheen = 0,
  style,
}) => {
  const p = project(cam, at, center);
  const width = w * p.scale;
  const url = staticFile(`objects/${src}.png`);

  // Bayangan kontak: makin tinggi benda, makin lebar, pudar, dan bergeser
  // menjauhi arah lampu (lampu dari kanan atas → bayangan ke kiri bawah).
  const shW = width * (0.72 + 0.34 * lift);
  const shH = Math.max(16, width * 0.1) * (1 + 0.55 * lift);
  const shA = shadow * (0.62 - 0.34 * lift);

  return (
    <div
      style={{
        position: 'absolute',
        left: p.sx,
        top: p.sy,
        width,
        transform: `translate(-50%, -50%) rotateZ(${rz}deg)`,
        transformOrigin: '50% 50%',
        opacity,
        zIndex: behind ? 1 : 5,
        pointerEvents: 'none',
        ...style,
      }}
    >
      {/* bayangan kontak di bidang di bawah benda */}
      {shadow > 0.01 && (
        <div
          style={{
            position: 'absolute',
            left: '50%',
            top: '58%',
            width: shW,
            height: shH,
            transform: `translate(${-50 - 4 * lift}%, ${-30 + 26 * lift}%) rotate(-3deg)`,
            background: `radial-gradient(ellipse 50% 50% at 50% 50%, ${alpha('#000000', shA)} 0%, ${alpha('#000000', shA * 0.45)} 45%, ${alpha('#000000', 0)} 78%)`,
            filter: 'blur(9px)',
          }}
        />
      )}

      {/* benda: satu gambar, satu filter warna, satu drop-shadow */}
      <Img
        src={url}
        style={{
          display: 'block',
          width: '100%',
          height: 'auto',
          transform: `perspective(1400px) rotateX(${rx}deg) rotateY(${ry}deg)`,
          filter:
            // Grade tunggal untuk semua objek: hijau ballot box dan biru fin ditarik
            // ke arah hangat film ini, jadi enam foto berbeda terbaca satu keluarga.
            `brightness(${(1 - 0.42 * dim).toFixed(3)}) contrast(1.1) ` +
            `saturate(${(0.74 - 0.2 * dim).toFixed(3)}) sepia(0.34) hue-rotate(-9deg) ` +
            `drop-shadow(${(6 + 10 * lift).toFixed(1)}px ${(14 + 26 * lift).toFixed(1)}px ${(10 + 20 * lift).toFixed(1)}px rgba(0,0,0,${(0.42 - 0.12 * lift).toFixed(2)}))` +
            (blur > 0.2 ? ` blur(${blur.toFixed(2)}px)` : ''),
        }}
      />

      {/* rim light: mengikuti alfa foto, bukan kotaknya */}
      {rim > 0.01 && (
        <div
          style={{
            position: 'absolute',
            inset: 0,
            background: `linear-gradient(${118 + rz * 0.3}deg, ${alpha(rimColor, 0.85 * rim)} 0%, ${alpha(rimColor, 0.25 * rim)} 26%, ${alpha(rimColor, 0)} 54%)`,
            WebkitMaskImage: `url(${url})`,
            WebkitMaskSize: '100% 100%',
            maskImage: `url(${url})`,
            maskSize: '100% 100%',
            mixBlendMode: 'screen',
            transform: `perspective(1400px) rotateX(${rx}deg) rotateY(${ry}deg)`,
          }}
        />
      )}

      {/* sheen: satu sapuan cahaya yang lewat sekali (dipakai saat benda mendarat) */}
      {sheen > 0.01 && (
        <div
          style={{
            position: 'absolute',
            inset: 0,
            background: `linear-gradient(102deg, ${alpha('#FFFFFF', 0)} ${Math.max(0, sheen * 120 - 26)}%, ${alpha('#FFF3DF', 0.55 * (1 - Math.abs(sheen - 0.5) * 1.6))} ${sheen * 120}%, ${alpha('#FFFFFF', 0)} ${Math.min(100, sheen * 120 + 22)}%)`,
            WebkitMaskImage: `url(${url})`,
            WebkitMaskSize: '100% 100%',
            maskImage: `url(${url})`,
            maskSize: '100% 100%',
            mixBlendMode: 'soft-light',
          }}
        />
      )}
    </div>
  );
};

/**
 * Silhouette — versi gelap dari foto yang sama, dipakai sebagai bayangan
 * jauh di lantai (bukan bayangan kontak yang kecil). Dipakai di shot lantai.
 */
export const Silhouette: React.FC<{
  src: string;
  w: number;
  at: { x: number; y: number; z?: number };
  cam: Cam;
  center: { x: number; y: number };
  squash?: number;
  opacity?: number;
  blur?: number;
}> = ({ src, w, at, cam, center, squash = 0.42, opacity = 0.4, blur = 14 }) => {
  const p = project(cam, at, center);
  const url = staticFile(`objects/${src}.png`);
  return (
    <div
      style={{
        position: 'absolute',
        left: p.sx,
        top: p.sy,
        width: w * p.scale,
        transform: `translate(-50%, -50%) scaleY(${-squash})`,
        opacity,
        filter: `blur(${blur}px) brightness(0)`,
        zIndex: 2,
        pointerEvents: 'none',
      }}
    >
      <Img src={url} style={{ display: 'block', width: '100%' }} />
    </div>
  );
};

/** gelombang lingkaran di lantai: dipakai saat benda mendarat */
export const GroundRipple: React.FC<{
  at: { x: number; y: number; z?: number };
  cam: Cam;
  center: { x: number; y: number };
  progress: number;
  size?: number;
  color?: string;
}> = ({ at, cam, center, progress, size = 420, color = C.tungsten }) => {
  const p = project(cam, at, center);
  const k = clamp01(progress);
  if (k <= 0 || k >= 1) return null;
  const w = size * p.scale * (0.4 + k * 1.5);
  return (
    <div
      style={{
        position: 'absolute',
        left: p.sx,
        top: p.sy,
        width: w,
        height: w * 0.2,
        transform: 'translate(-50%, -50%)',
        border: `2px solid ${alpha(color, 0.5 * (1 - k))}`,
        borderRadius: '50%',
        filter: `blur(${(1 + 4 * k).toFixed(1)}px)`,
        pointerEvents: 'none',
        zIndex: 3,
      }}
    />
  );
};
