/**
 * Main.tsx — rangkaian film 60 detik + desain bunyi.
 *
 * Sambungan antar shot: potongan keras di dalam ruang yang sama (lampu, debu,
 * lantai tidak berubah), ditambah satu kilat cahaya 3 frame di titik potong.
 * Itulah bahasa "shot-transitions" shotcraft: potongan dibaca sebagai
 * perpindahan mata, bukan sebagai proyek baru.
 *
 * Bunyi: BGM hanya satu lapis rendah (bed) supaya tidak menutupi mikro-SFX.
 * Setiap aksi punya bunyi: benda mendarat, kaca berhenti, angka mendarat.
 */
import React from 'react';
import { AbsoluteFill, Audio, Sequence, staticFile, useCurrentFrame } from 'remotion';
import { C, alpha } from './lib/theme';
import { clamp01, ramp } from './lib/motion';
import { Shot1, Shot2, Shot3, Shot4, Shot5, Shot6 } from './shots';

export const DURATION = 1800;

const SHOTS = [
  { from: 0, dur: 300, C: Shot1 },
  { from: 300, dur: 320, C: Shot2 },
  { from: 620, dur: 360, C: Shot3 },
  { from: 980, dur: 320, C: Shot4 },
  { from: 1300, dur: 300, C: Shot5 },
  { from: 1600, dur: 200, C: Shot6 },
];

/** potongan: satu kilat cahaya tipis tepat di titik sambung */
const CUTS = [300, 620, 980, 1300, 1600];

/**
 * Peta bunyi. Nilai volume sudah dikalibrasi untuk campuran SFX-only:
 * impact 0,42 · whoosh 0,30 · snap 0,26 · click 0,20 · soft 0,24.
 */
type Sfx = { at: number; file: string; vol: number };
const SFX: Sfx[] = [
  // 01 — lampu teater menyala, kliping ditemukan
  { at: 14, file: 'transition-soft', vol: 0.26 },
  { at: 32, file: 'click-camera', vol: 0.2 },
  { at: 166, file: 'whoosh-fast', vol: 0.3 },
  { at: 232, file: 'transition-soft', vol: 0.22 },

  // 02 — kotak mendarat, lima surat suara masuk, angka turun
  { at: 334, file: 'transition-snap', vol: 0.3 },
  { at: 360, file: 'impact-cine', vol: 0.3 },
  { at: 418, file: 'swoosh-quick', vol: 0.22 },
  { at: 450, file: 'swoosh-quick', vol: 0.2 },
  { at: 482, file: 'swoosh-quick', vol: 0.2 },
  { at: 514, file: 'swoosh-quick', vol: 0.19 },
  { at: 546, file: 'swoosh-quick', vol: 0.18 },
  { at: 364, file: 'impact-cine', vol: 0.34 },

  // 03 — kaca pembesar berhenti tiga kali, lalu grid runtuh
  { at: 648, file: 'click-camera', vol: 0.22 },
  { at: 712, file: 'click-camera', vol: 0.2 },
  { at: 788, file: 'click-camera', vol: 0.2 },
  { at: 856, file: 'whoosh-fast', vol: 0.32 },
  { at: 868, file: 'transition-soft', vol: 0.24 },

  // 04 — simpul muncul, lalu mengendor
  { at: 986, file: 'transition-soft', vol: 0.24 },
  { at: 1002, file: 'click-camera', vol: 0.16 },
  { at: 1128, file: 'impact-cine', vol: 0.3 },

  // 05 — poster menyusun diri, pertanyaan mendarat
  { at: 1302, file: 'whoosh-fast', vol: 0.3 },
  { at: 1352, file: 'transition-snap', vol: 0.2 },
  { at: 1420, file: 'impact-cine', vol: 0.32 },

  // 06 — kunci merek
  { at: 1602, file: 'transition-snap', vol: 0.24 },
  { at: 1628, file: 'impact-cine', vol: 0.3 },
  { at: 1658, file: 'transition-soft', vol: 0.2 },
];

const Flash: React.FC = () => {
  const frame = useCurrentFrame();
  let v = 0;
  for (const c of CUTS) {
    const d = frame - c;
    if (d >= -1 && d <= 4) v = Math.max(v, 1 - Math.abs(d) / 3);
  }
  if (v <= 0) return null;
  return (
    <AbsoluteFill
      style={{
        pointerEvents: 'none',
        background: `radial-gradient(ellipse 70% 50% at 50% 42%, ${alpha(C.tungsten, 0.16 * v)} 0%, ${alpha(C.tungsten, 0)} 70%)`,
        mixBlendMode: 'screen',
        zIndex: 50,
      }}
    />
  );
};

/** gelap total di 1 frame titik potong: menyembunyikan sambungan kamera */
const Dip: React.FC = () => {
  const frame = useCurrentFrame();
  let v = 0;
  for (const c of CUTS) {
    const d = frame - c;
    if (d >= 0 && d <= 2) v = Math.max(v, 1 - d / 3);
  }
  if (v <= 0) return null;
  return (
    <AbsoluteFill
      style={{ pointerEvents: 'none', background: `rgba(2,3,7,${(0.34 * v).toFixed(3)})`, zIndex: 49 }}
    />
  );
};

export const Film: React.FC = () => {
  const frame = useCurrentFrame();
  // fade masuk dan keluar seluruh film
  const fin = ramp(frame, 0, 16, (t) => t);
  const fout = 1 - ramp(frame, DURATION - 24, 24, (t) => t);

  return (
    <AbsoluteFill style={{ background: C.ink }}>
      {SHOTS.map(({ from, dur, C: Shot }) => (
        <Sequence key={from} from={from} durationInFrames={dur} name={`shot-${from}`}>
          <Shot />
        </Sequence>
      ))}

      <Dip />
      <Flash />

      {/* BGM: satu lapis rendah. Turun 40% di bawah tiap impact supaya SFX terbaca. */}
      <Audio
        src={staticFile('audio/bgm/bed.mp3')}
        volume={(f) => {
          const base = 0.30 * clamp01(f / 45) * (1 - clamp01((f - (DURATION - 60)) / 60));
          let duck = 1;
          for (const s of SFX) {
            if (s.file !== 'impact-cine') continue;
            const d = f - s.at;
            if (d > -6 && d < 26) duck = Math.min(duck, 0.55 + 0.45 * clamp01(Math.abs(d) / 20));
          }
          return base * duck;
        }}
      />

      {SFX.map((s, i) => (
        <Sequence key={i} from={s.at} durationInFrames={90} name={`sfx-${s.file}-${s.at}`}>
          <Audio src={staticFile(`audio/sfx/${s.file}.mp3`)} volume={s.vol} />
        </Sequence>
      ))}

      <AbsoluteFill style={{ background: '#000', opacity: 1 - Math.min(fin, fout), zIndex: 60 }} />
    </AbsoluteFill>
  );
};
