/**
 * shots/index.tsx — enam shot film 60 detik.
 *
 * Aturan tata letak (lib/Layout.tsx):
 *   teks  : 150–500 dan 1402–1790
 *   benda : 610–1336  ← tinggi benda WAJIB dihitung lewat lib/objects.ts
 *
 * Koordinat `at` adalah koordinat DUNIA dengan pusat (0,0) = titik tengah zona
 * benda. Pada zoom 1 dan kamera (0,0), dunia (0,0) jatuh tepat di layar
 * (540, 985). Artinya rentang aman untuk y adalah ±330 (zona 655 px), dan
 * untuk x ±470.
 */
import React from 'react';
import { AbsoluteFill, useCurrentFrame } from 'remotion';
import { C, TYPE, alpha } from '../lib/theme';
import { EASE, camAt, clamp01, mix, ramp, type CamKey } from '../lib/motion';
import { Stage } from '../lib/Stage';
import { Table } from '../lib/Table';
import { GroundRipple, Photo, Silhouette, type Cam } from '../lib/Photo';
import { Kicker, Reveal, RollNumber, Source } from '../lib/Type';
import { Frame, ZONE } from '../lib/Layout';
import { fitW } from '../lib/objects';

const W = 1080;
const CENTER = { x: W / 2, y: ZONE.objMid };

const useCam = (keys: CamKey[], ease = EASE.smooth): Cam => {
  const frame = useCurrentFrame();
  const c = camAt(frame, keys, ease);
  return { x: c.x, y: c.y, zoom: c.zoom };
};

/* ══════════════════════════════════════════════════ 01 · KLIPING 1916 */

export const Shot1: React.FC = () => {
  const frame = useCurrentFrame();
  const cam = useCam([
    { f: 0, x: 22, y: 34, zoom: 0.95 },
    { f: 96, x: 12, y: 20, zoom: 1.0 },
    { f: 176, x: -2, y: 2, zoom: 1.05 },
    { f: 300, x: -18, y: -14, zoom: 1.12 },
  ], EASE.push);

  const sweep = EASE.smooth(clamp01((frame - 76) / 88));
  const lock = ramp(frame, 164, 22, EASE.snappy);
  const keyLight = { x: mix(0.2, 0.58, sweep), y: mix(0.1, 0.24, sweep) };
  const lightOn = ramp(frame, 10, 28, EASE.out);

  const lift = 0.24 + 0.14 * EASE.out(clamp01((frame - 150) / 70));
  const bob = Math.sin(frame / 44) * 3.4;

  return (
    <Frame
      kicker={<Kicker text="Knot Theory · Episode 01" at={26} color={C.muted} />}
      head={<Reveal text="1916" at={50} size={TYPE.mega} serif align="center" each={16} />}
      sub={<Reveal text="Pesisir New Jersey" at={88} size={58} serif italic color={C.cream2} align="center" />}
      body={
        <Reveal
          text="Empat orang tewas diserang hiu."
          at={190}
          size={TYPE.body + 4}
          color={C.cream}
          align="center"
          each={12}
        />
      }
      source={<Source text="Serangan hiu, 1–12 Juli 1916" at={218} />}
      stage={
        <Stage
          keyLight={keyLight}
          keyPower={0.3 + 0.95 * lightOn}
          beam={{ angle: -16, width: 0.44, power: 0.2 + 0.3 * lock }}
          floor={null}
          dust={50}
          vignette={0.58}
        >
          <Table back={0.705} pan={frame * 0.06} shine={0.7} />
          {/* sirip: benda jauh di belakang, ikut kabur */}
          <Photo
            src="fin"
            w={fitW('fin', 560)}
            at={{ x: 250, y: -20, z: 0.55 }}
            cam={cam}
            center={CENTER}
            rz={-9}
            lift={0.8}
            dim={0.6}
            blur={8}
            rim={0.26}
            shadow={0.2}
            behind
            opacity={0.55 * ramp(frame, 24, 40, EASE.out)}
          />
          {/* kliping: benda utama. tinggi 640 → lebar 596, aman di zona. */}
          <Photo
            src="newspaper"
            w={fitW('newspaper', 690)}
            at={{ x: -6, y: 6 + bob, z: 0 }}
            cam={cam}
            center={CENTER}
            rx={15}
            ry={-17 + 6 * EASE.out(clamp01((frame - 50) / 240))}
            rz={-3}
            lift={lift}
            rim={0.7}
            shadow={0.75}
            sheen={ramp(frame, 180, 52, EASE.linear)}
            opacity={ramp(frame, 4, 22, EASE.out)}
          />
          <GroundRipple
            at={{ x: -6, y: 330 }}
            cam={cam}
            center={CENTER}
            progress={ramp(frame, 172, 42, EASE.linear)}
            size={620}
          />
        </Stage>
      }
    />
  );
};

/* ══════════════════════════════════════════════════ 02 · KOTAK SUARA */

/* Surat suara: x dijaga di ±250 dunia (≈ ±270 px layar) supaya tidak pernah
   keluar bingkai; semuanya jatuh ke mulut kotak di sekitar (0, -30). */
/* Surat suara: mulai DI DALAM zona (y ≥ -250 dunia) supaya ujung atasnya
   tidak pernah masuk pita angka (layar y 496). Satu tabrakan teks-benda
   sudah cukup untuk merusak satu shot. */
const BALLOTS = [
  { at: 112, from: -196, to: -92, h: 186, rot: -16 },
  { at: 142, from: 182, to: 88, h: 178, rot: 13 },
  { at: 172, from: -126, to: -32, h: 172, rot: 6 },
  { at: 202, from: 130, to: 38, h: 168, rot: -10 },
  { at: 232, from: -38, to: -8, h: 164, rot: 3 },
];

export const Shot2: React.FC = () => {
  const frame = useCurrentFrame();
  const cam = useCam([
    { f: 0, x: 0, y: 16, zoom: 1.0 },
    { f: 120, x: 6, y: 4, zoom: 1.0 },
    { f: 240, x: -8, y: -4, zoom: 1.03 },
    { f: 320, x: -16, y: -14, zoom: 1.08 },
  ], EASE.smooth);

  /* Kotak sudah ada di frame 0 — shot tidak boleh dibuka dengan layar kosong.
     Yang bergerak adalah surat suara dan angka, bukan kehadiran bendanya. */
  const boxDrop = 1;
  const boxY = -30;
  const land = ramp(frame, 48, 34, EASE.linear);

  return (
    <Frame
      kicker={<Kicker text="Pemilu · 7 November 1916" at={0} />}
      head={
        <div style={{ marginTop: -14 }}>
          <Reveal text="Suara turun" at={4} size={TYPE.h1} serif align="center" each={14} />
        </div>
      }
      sub={<RollNumber value="3–13" at={30} size={176} color={C.rose} align="center" dur={30} />}
      body={
        <Reveal
          text="poin di kota pantai, dibanding kabupaten lain"
          at={96}
          size={TYPE.body}
          color={C.cream2}
          align="center"
          each={8}
        />
      }
      accent={
        <Reveal text="Bukan karena kebijakannya." at={214} size={TYPE.h3 + 2} serif color={C.cream} align="center" each={13} />
      }
      source={<Source text="Achen & Bartels, Democracy for Realists, 2016 · bab 5" at={124} />}
      stage={
        <Stage
          keyLight={{ x: 0.62, y: 0.16 }}
          keyPower={1.06}
          beam={{ angle: -14, width: 0.42, power: 0.34 }}
          floor={null}
          dust={38}
          vignette={0.56}
        >
          <Table back={0.715} pan={frame * 0.05} shine={0.6} />
          <Silhouette src="ballot-box" w={fitW('ballot-box', 610)} at={{ x: -4, y: 300 }} cam={cam} center={CENTER} squash={0.24} opacity={0.6} blur={20} />
          <Photo
            src="ballot-box"
            w={fitW('ballot-box', 610)}
            at={{ x: -4, y: boxY, z: 0 }}
            cam={cam}
            center={CENTER}
            rz={-1.4}
            lift={0.22}
            rim={0.75}
            shadow={0.8}
            opacity={1}
          />
          <GroundRipple at={{ x: -4, y: 320 }} cam={cam} center={CENTER} progress={land} size={560} />

          {/* surat suara jatuh ke celah kotak */}
          {BALLOTS.map((b, i) => {
            if (frame < b.at - 4) return null;
            const p = clamp01((frame - b.at) / 26);
            const drop = 1 - EASE.snappy(p);
            const y = -196 + (1 - drop) * 176;
            const x = mix(b.from, b.to, EASE.out(clamp01((frame - b.at) / 26)));
            return (
              <Photo
                key={i}
                src="ballots"
                w={fitW('ballots', b.h)}
                at={{ x, y, z: -0.06 - i * 0.01 }}
                cam={cam}
                center={CENTER}
                rz={b.rot + 12 * (1 - p)}
                ry={12 * drop}
                lift={0.2 + 0.9 * drop}
                rim={0.5}
                shadow={0.42}
                blur={7 * drop}
                opacity={(1 - clamp01((frame - b.at - 18) / 10)) * 0.97}
              />
            );
          })}
        </Stage>
      }
    />
  );
};

/* ══════════════════════════════════════════════════ 03 · UJI ULANG */

const GRID = 10;
const DOT_GAP = 60;

export const Shot3: React.FC = () => {
  const frame = useCurrentFrame();
  const cam = useCam([
    { f: 0, x: 0, y: 22, zoom: 1.04 },
    { f: 110, x: -14, y: 4, zoom: 0.99 },
    { f: 250, x: 14, y: -6, zoom: 1.02 },
    { f: 360, x: 0, y: 0, zoom: 1.08 },
  ], EASE.smooth);

  const stops = [
    { f: 18, x: -150, y: -110 },
    { f: 86, x: 110, y: 20 },
    { f: 140, x: -90, y: 96 },
    { f: 194, x: 40, y: -60 },
  ];
  const loupe = (() => {
    let x = stops[0].x;
    let y = stops[0].y;
    for (let i = 0; i < stops.length - 1; i++) {
      const a = stops[i];
      const b = stops[i + 1];
      if (frame >= a.f) {
        const t = EASE.smooth(clamp01((frame - a.f) / (b.f - a.f)));
        x = mix(a.x, b.x, t);
        y = mix(a.y, b.y, t);
      }
    }
    return { x, y };
  })();

  const collapse = ramp(frame, 246, 36, EASE.exit);
  const oneUp = ramp(frame, 218, 26, EASE.overshoot);
  const gridIn = ramp(frame, -18, 20, EASE.out);

  return (
    <Frame
      kicker={<Kicker text="2018 · uji ulang 1872–2012" at={8} />}
      head={<Reveal text="Setiap angka diperiksa lagi." at={22} size={TYPE.h2} serif align="center" each={13} />}
      sub={<Reveal text="hampir nol" at={212} size={104} serif italic color={C.rose} align="center" each={14} />}
      body={
        <Reveal
          text="Sepuluh cara menguji, satu tampak berarti."
          at={256}
          size={TYPE.body}
          color={C.cream}
          align="center"
          each={9}
        />
      }
      accent={<Reveal text="Itu pun bisa kebetulan." at={300} size={TYPE.h3} serif color={C.roseLit} align="center" each={11} />}
      source={<Source text="Fowler & Hall, 2018 · replikasi serangan hiu" at={272} />}
      stage={
        <Stage
          keyLight={{ x: 0.56, y: 0.22 }}
          keyPower={0.9}
          fill={{ x: 0.2, y: 0.88 }}
          beam={{ angle: -20, width: 0.32, power: 0.22 }}
          floor={null}
          dust={24}
          vignette={0.6}
        >
          <Table back={0.705} pan={frame * 0.04} shine={0.4} />
          {/* bidang data 100 titik, dalam perspektif meja */}
          <div
            style={{
              position: 'absolute',
              left: CENTER.x,
              top: CENTER.y + 40,
              transform: `translate(-50%, -50%) scale(${cam.zoom}) perspective(1200px) rotateX(15deg)`,
              width: (GRID - 1) * DOT_GAP + 130,
              height: (GRID - 1) * DOT_GAP + 130,
              opacity: gridIn,
            }}
          >
            {Array.from({ length: GRID * GRID }, (_, i) => {
              const col = i % GRID;
              const row = Math.floor(i / GRID);
              const x = col * DOT_GAP - ((GRID - 1) * DOT_GAP) / 2;
              const y = row * DOT_GAP - ((GRID - 1) * DOT_GAP) / 2;
              const near = clamp01(1 - Math.hypot(x - loupe.x, y - loupe.y) / 240);
              const isTest = i % 10 === 0;
              const hero = i === 40;
              const appear = ramp(frame, -26 + (col + row) * 1.4, 16, EASE.out);
              const heroLit = hero ? oneUp : 0;
              const gone = collapse * (isTest && !hero ? 1 : 0);
              const op = (0.22 + 0.6 * near) * appear * (1 - gone * 0.9) + heroLit * 0.4;
              const size = 19 + 15 * near + heroLit * 11;
              const fill = hero && heroLit > 0.2 ? C.rose : isTest ? C.cream : C.slate2;
              return (
                <div
                  key={i}
                  style={{
                    position: 'absolute',
                    left: '50%',
                    top: '50%',
                    width: size,
                    height: size,
                    marginLeft: x - size / 2,
                    marginTop: y - size / 2,
                    borderRadius: '50%',
                    background: fill,
                    opacity: clamp01(op),
                    boxShadow:
                      near > 0.4 || heroLit > 0.4
                        ? `0 0 ${(12 + 28 * near).toFixed(1)}px ${alpha(hero ? C.rose : C.cream, 0.55 * Math.max(near, heroLit))}`
                        : undefined,
                  }}
                />
              );
            })}
          </div>

          {/* kaca pembesar mengikuti titik yang sedang diperiksa */}
          <Photo
            src="magnifier"
            w={fitW('magnifier', 400)}
            at={{ x: loupe.x * 0.45, y: loupe.y * 0.45 + 40, z: -0.1 }}
            cam={cam}
            center={CENTER}
            rz={-12}
            ry={10}
            lift={0.9}
            rim={0.55}
            shadow={0.4}
            opacity={ramp(frame, -10, 16, EASE.out)}
          />
        </Stage>
      }
    />
  );
};

/* ══════════════════════════════════════════════════ 04 · SIMPUL */

export const Shot4: React.FC = () => {
  const frame = useCurrentFrame();
  const cam = useCam([
    { f: 0, x: 0, y: 0, zoom: 1.0 },
    { f: 140, x: -12, y: -8, zoom: 1.1 },
    { f: 260, x: 8, y: 8, zoom: 1.02 },
    { f: 320, x: 16, y: -2, zoom: 1.14 },
  ], EASE.push);

  const slip = ramp(frame, 152, 100, EASE.smooth);
  const spin = -8 + frame * 0.1;
  const stretch = 1 + 0.09 * slip;
  const bob = Math.sin(frame / 50) * 6;
  const glow = 0.35 + 0.55 * Math.sin(Math.PI * clamp01((frame - 118) / 180));

  return (
    <Frame
      kicker={<Kicker text="Yang tersisa" at={12} />}
      head={<Reveal text="Bukan angkanya." at={26} size={TYPE.h1} serif align="center" each={15} />}
      accent={<Reveal text="Tapi cara kita menilai." at={176} size={TYPE.h2} serif color={C.roseLit} align="center" each={14} />}
      source={<Source text="Tafsiran, bukan temuan" at={210} />}
      stage={
        <Stage
          keyLight={{ x: 0.5, y: 0.26 }}
          keyPower={1.1}
          fill={{ x: 0.5, y: 0.94 }}
          beam={{ angle: 0, width: 0.26, power: 0.44 }}
          floor={null}
          dust={30}
          vignette={0.6}
        >
          <div
            style={{
              position: 'absolute',
              left: CENTER.x,
              top: CENTER.y + bob,
              width: 820 * cam.zoom,
              height: 820 * cam.zoom,
              transform: 'translate(-50%, -50%)',
              borderRadius: '50%',
              background: `radial-gradient(circle, ${alpha(C.rose, 0.15 * glow)} 0%, ${alpha(C.rose, 0.05 * glow)} 44%, ${alpha(C.rose, 0)} 72%)`,
              filter: 'blur(22px)',
            }}
          />
          {/* simpul 640 tinggi → 568 lebar, di tengah zona */}
          <Photo
            src="thread-knot"
            w={fitW('thread-knot', 720)}
            at={{ x: 0, y: 6 + bob, z: 0 }}
            cam={cam}
            center={CENTER}
            rz={spin * 0.3}
            ry={spin}
            rx={5}
            lift={0.95}
            rim={0.6}
            rimColor={C.roseLit}
            shadow={0.3}
            opacity={ramp(frame, 4, 22, EASE.out)}
            style={{ scale: `${stretch.toFixed(3)}` }}
          />
          <GroundRipple
            at={{ x: 0, y: 372 }}
            cam={cam}
            center={CENTER}
            progress={ramp(frame, 152, 64, EASE.linear)}
            size={720}
            color={C.roseLit}
          />
        </Stage>
      }
    />
  );
};

/* ══════════════════════════════════════════════════ 05 · POSTER */

export const Shot5: React.FC = () => {
  const frame = useCurrentFrame();
  const cam = useCam([
    { f: 0, x: 0, y: 6, zoom: 1.1 },
    { f: 130, x: 0, y: 0, zoom: 1.0 },
    { f: 300, x: -4, y: -6, zoom: 0.97 },
  ], EASE.push);

  const bob = Math.sin(frame / 58) * 3;
  /* Semua benda sudah ada di frame 0 (poster), lalu masing-masing hanya
     naik beberapa piksel sebagai "napas" — bukan muncul dari kosong. */
  const rise = (i: number) => 1 - 0.0 * i + 0.0 * ramp(frame, i * 8, 30, EASE.out);

  return (
    <Frame
      kicker={<Kicker text="Yang diukur" at={24} />}
      body={
        <Reveal
          text="Kalau yang menghukum tak bisa dikendalikan,"
          at={52}
          size={TYPE.body + 2}
          color={C.cream}
          align="center"
          each={9}
        />
      }
      accent={
        <Reveal
          text="apa yang sebenarnya kita nilai?"
          at={116}
          size={TYPE.h3 + 6}
          serif
          color={C.roseLit}
          align="center"
          each={11}
        />
      }
      source={<Source text="Pertanyaan, bukan kesimpulan" at={150} />}
      stage={
        <Stage
          keyLight={{ x: 0.58, y: 0.2 }}
          keyPower={1.0}
          fill={{ x: 0.22, y: 0.9 }}
          beam={{ angle: -17, width: 0.46, power: 0.3 }}
          floor={null}
          dust={42}
          vignette={0.56}
        >
          <Table back={0.705} pan={frame * 0.04} shine={0.55} />
          {/* poster: enam benda, semua berukuran < zona, saling menumpuk
              dengan urutan berbeda supaya terbaca rak benda, bukan grid */}
          <Photo src="fin" w={fitW('fin', 470)} at={{ x: 268, y: -104, z: 0.42 }} cam={cam} center={CENTER} rz={12} lift={0.6} dim={0.55} blur={6} rim={0.24} shadow={0.2} behind opacity={0.85} />
          <Photo src="newspaper" w={fitW('newspaper', 420)} at={{ x: -246, y: -66 + bob, z: 0.18 }} cam={cam} center={CENTER} ry={-18} rz={-9} lift={0.3} dim={0.3} blur={2.4} rim={0.4} shadow={0.5} opacity={rise(0)} />
          <Photo src="ballots" w={fitW('ballots', 300)} at={{ x: -214, y: 168, z: 0 }} cam={cam} center={CENTER} rz={-14} lift={0.26} rim={0.45} shadow={0.5} opacity={rise(1)} />
          <Photo src="magnifier" w={fitW('magnifier', 236)} at={{ x: 18, y: 214, z: -0.04 }} cam={cam} center={CENTER} rz={-26} lift={0.28} rim={0.42} shadow={0.45} opacity={rise(2)} />
          <Photo src="ballot-box" w={fitW('ballot-box', 360)} at={{ x: 252, y: 132, z: 0.02 }} cam={cam} center={CENTER} rz={5} lift={0.22} rim={0.58} shadow={0.62} opacity={rise(3)} />
          <Photo src="thread-knot" w={fitW('thread-knot', 350)} at={{ x: 2, y: -6 + bob * 1.2, z: -0.12 }} cam={cam} center={CENTER} rz={-5} ry={frame * 0.2} lift={0.85} rim={0.62} rimColor={C.roseLit} shadow={0.32} opacity={rise(0)} />
        </Stage>
      }
    />
  );
};

/* ══════════════════════════════════════════════════ 06 · OUTRO */

export const Shot6: React.FC = () => {
  const frame = useCurrentFrame();
  const settle = ramp(frame, 0, 40, EASE.out);
  const mark = ramp(frame, 10, 30, EASE.overshoot);
  const tag = ramp(frame, 34, 26, EASE.out);

  return (
    <AbsoluteFill style={{ background: C.ink }}>
      <Stage
        keyLight={{ x: 0.5, y: 0.26 }}
        keyPower={0.5 * (1 - 0.55 * settle)}
        fill={null}
        beam={{ angle: -8, width: 0.22, power: 0.12 }}
        floor={null}
        dust={18}
        vignette={0.72}
        grain={0.06}
      >
        <Photo
          src="thread-knot"
          w={fitW('thread-knot', 470)}
          at={{ x: 0, y: -180, z: 0.2 }}
          cam={{ x: 0, y: 0, zoom: 1 }}
          center={CENTER}
          ry={frame * 0.14}
          rz={-4}
          lift={0.85}
          rim={0.5}
          rimColor={C.roseLit}
          shadow={0.18}
          dim={0.08}
          opacity={0.52 * (0.45 + 0.55 * settle)}
        />
      </Stage>

      <div
        style={{
          position: 'absolute',
          left: 0,
          right: 0,
          top: 1120,
          textAlign: 'center',
          opacity: clamp01(mark * 1.3),
          transform: `scale(${(0.95 + 0.05 * mark).toFixed(3)})`,
        }}
      >
        <div
          style={{
            fontFamily: '"Instrument Serif", Georgia, serif',
            fontSize: 142,
            lineHeight: 0.94,
            letterSpacing: '-0.025em',
            color: C.cream,
          }}
        >
          Knot Theory
        </div>
        <div
          style={{
            marginTop: 26,
            fontFamily: '"JetBrains Mono", monospace',
            fontSize: 25,
            letterSpacing: '0.34em',
            textTransform: 'uppercase',
            color: C.rose,
            opacity: tag,
          }}
        >
          satu angka · satu sumber
        </div>
      </div>

      <div style={{ position: 'absolute', left: 30, right: 30, top: 1650, opacity: tag * 0.95 }}>
        <Source text="Achen & Bartels 2016 · Fowler & Hall 2018" at={0} size={21} />
      </div>
      <div style={{ position: 'absolute', left: 30, right: 30, top: 1702, opacity: tag * 0.75 }}>
        <Source text="episode berikutnya · siapa yang naik" at={0} size={21} color={C.muted2} />
      </div>
    </AbsoluteFill>
  );
};
