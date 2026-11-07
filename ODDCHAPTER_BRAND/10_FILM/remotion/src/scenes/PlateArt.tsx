import React from "react";
import { interpolate, useCurrentFrame } from "remotion";
import { C, H, W } from "../theme";

/**
 * PlateArt — satu bahasa visual, sepuluh bentuk dasar.
 *
 * Semua episode memakai aturan yang sama: latar gelap, garis rambut sage,
 * siluet ivory tipis, dan SATU aksen oranye yang mewakili satu benda penting
 * di episode itu (lampu, retakan, jendela, satu titik kosong). Bentuk dasar
 * dipilih dari `plate` di content_data.py — bukan digambar per episode, supaya
 * 21 episode tetap terlihat satu keluarga.
 *
 * Semua deterministik: `useCurrentFrame()` + interpolate. Tidak ada random.
 */

export type PlateKind = "tower" | "vessel" | "shelter" | "road" | "paper" | "signal" | "plume" | "water" | "dial" | "ridge";

const HORIZON = H * 0.7;

/** garis rambut horizontal: laut, tanah, lantai */
const Hair: React.FC<{ y: number; n?: number; step?: number; op?: number }> = ({ y, n = 9, step = 15, op = 0.2 }) => (
  <>
    {new Array(n).fill(0).map((_, i) => (
      <line
        key={i}
        x1={0}
        y1={y + 10 + i * step + i * i * 1.6}
        x2={W}
        y2={y + 10 + i * step + i * i * 1.6}
        stroke={C.sage}
        strokeWidth={i === 0 ? 1.6 : 1}
        opacity={Math.max(0.02, op - i * 0.021)}
      />
    ))}
  </>
);

const S: React.FC<{ d: string; o?: number; w?: number; fill?: string; stroke?: string }> = ({ d, o = 0.55, w = 2.2, fill = "#0A0C0F", stroke = C.ivory }) => (
  <path d={d} fill={fill} stroke={stroke} strokeWidth={w} strokeOpacity={o} />
);

const Tower: React.FC<{ lamp: number }> = ({ lamp }) => {
  const cx = W / 2;
  const g = 0.6 + 0.4 * Math.sin(useCurrentFrame() / 34);
  return (
    <>
      <Hair y={HORIZON} />
      <S d={`M ${cx - 96} ${HORIZON} L ${cx - 34} ${H * 0.52} L ${cx + 34} ${H * 0.52} L ${cx + 96} ${HORIZON} Z`} o={0.6} />
      <path d={`M ${cx - 96} ${HORIZON} L ${cx - 34} ${H * 0.52} L ${cx - 6} ${H * 0.52} L ${cx - 40} ${HORIZON} Z`} fill={C.ivory} opacity={0.045} />
      <rect x={cx - 48} y={H * 0.52 - 13} width={96} height={9} fill={C.ivory} opacity={0.5} />
      <rect x={cx - 44} y={H * 0.52 - 62} width={88} height={49} fill="#0A0C0F" stroke={C.ivory} strokeWidth={2} strokeOpacity={0.55} />
      <S d={`M ${cx - 56} ${H * 0.52 - 62} L ${cx} ${H * 0.52 - 112} L ${cx + 56} ${H * 0.52 - 62} Z`} />
      <rect x={cx - 4} y={H * 0.56} width={8} height={26} fill={C.ivory} opacity={0.22} />
      <rect x={cx - 4} y={H * 0.63} width={8} height={26} fill={C.ivory} opacity={0.16} />
      <path d={`M ${cx - 10} ${H * 0.52 - 38} L ${0} ${H * 0.52 - 96} L ${0} ${H * 0.52 - 14} Z`} fill={C.orange} opacity={0.05 * lamp} />
      <path d={`M ${cx + 10} ${H * 0.52 - 38} L ${W} ${H * 0.52 - 96} L ${W} ${H * 0.52 - 14} Z`} fill={C.orange} opacity={0.024 * lamp} />
      <circle cx={cx} cy={H * 0.52 - 37} r={44 * g} fill={C.orange} opacity={0.09 * lamp} />
      <circle cx={cx} cy={H * 0.52 - 37} r={7} fill={C.orange} opacity={lamp} />
    </>
  );
};

/** Kapal: lambung, dua tiang, satu lentera. Dipakai EP03. */
const Vessel: React.FC<{ lamp: number }> = ({ lamp }) => {
  const cx = W / 2;
  const y = HORIZON - 30;
  const fy = HORIZON + 64;
  return (
    <>
      <Hair y={HORIZON + 44} n={7} step={17} op={0.16} />
      <S d={`M ${cx - 236} ${y} L ${cx + 236} ${y} L ${cx + 176} ${fy} L ${cx - 176} ${fy} Z`} o={0.62} w={2.4} />
      <line x1={cx - 236} y1={y} x2={cx + 236} y2={y} stroke={C.ivory} strokeWidth={3} strokeOpacity={0.5} />
      {/* tiang */}
      <line x1={cx - 96} y1={y} x2={cx - 96} y2={y - 430} stroke={C.ivory} strokeWidth={2} strokeOpacity={0.5} />
      <line x1={cx + 74} y1={y} x2={cx + 74} y2={y - 340} stroke={C.ivory} strokeWidth={2} strokeOpacity={0.42} />
      <line x1={cx - 168} y1={y - 300} x2={cx - 24} y2={y - 300} stroke={C.ivory} strokeWidth={1.6} strokeOpacity={0.32} />
      <line x1={cx + 18} y1={y - 240} x2={cx + 130} y2={y - 240} stroke={C.ivory} strokeWidth={1.6} strokeOpacity={0.26} />
      {/* tali */}
      <line x1={cx - 96} y1={y - 430} x2={cx - 236} y2={y} stroke={C.sage} strokeWidth={1} strokeOpacity={0.2} />
      <line x1={cx - 96} y1={y - 430} x2={cx + 236} y2={y} stroke={C.sage} strokeWidth={1} strokeOpacity={0.2} />
      {/* lentera di tiang depan */}
      <circle cx={cx - 96} cy={y - 442} r={26} fill={C.orange} opacity={0.1 * lamp} />
      <circle cx={cx - 96} cy={y - 442} r={6} fill={C.orange} opacity={lamp} />
    </>
  );
};

/** Tempat berlindung: tenda dengan tali pasak, satu sisi terbuka dari dalam. */
const Shelter: React.FC<{ lamp: number }> = ({ lamp }) => {
  const cx = W / 2;
  const base = HORIZON + 46;
  const apex = H * 0.5;
  const halfW = 286;
  return (
    <>
      <Hair y={base} n={6} step={16} op={0.14} />
      {/* tali pasak: yang membuat segitiga ini tenda, bukan gunung */}
      <line x1={cx} y1={apex} x2={cx - halfW - 96} y2={base} stroke={C.sage} strokeWidth={1.4} strokeOpacity={0.28} />
      <line x1={cx} y1={apex} x2={cx + halfW + 96} y2={base} stroke={C.sage} strokeWidth={1.4} strokeOpacity={0.28} />
      <S d={`M ${cx - halfW} ${base} L ${cx} ${apex} L ${cx + halfW} ${base} Z`} o={0.55} w={2.4} />
      {/* pintu: dua panel kain yang terlipat keluar */}
      <path d={`M ${cx - 74} ${base} L ${cx} ${apex + 96} L ${cx + 74} ${base} Z`} fill="#0A0C0F" stroke={C.ivory} strokeWidth={1.6} strokeOpacity={0.34} />
      {/* sisi kanan disobek dari dalam */}
      <path d={`M ${cx + 74} ${base} L ${cx + 148} ${base} L ${cx + 58} ${apex + 150} Z`} fill={C.orange} opacity={0.06 + 0.06 * lamp} />
      <line x1={cx + 74} y1={base} x2={cx + 58} y2={apex + 150} stroke={C.orange} strokeWidth={2} strokeOpacity={0.5} />
      <line x1={cx + 148} y1={base} x2={cx + 58} y2={apex + 150} stroke={C.orange} strokeWidth={2} strokeOpacity={0.32} />
      {/* lampu di dalam tenda, menyala dari balik kain */}
      <circle cx={cx - 6} cy={base - 62} r={54} fill={C.orange} opacity={0.05 * lamp} />
    </>
  );
};

/** Jalan, jalur, atau lapangan: garis perspektif menuju satu titik. */
const Road: React.FC<{ lamp: number }> = ({ lamp }) => {
  const cx = W / 2;
  const hz = H * 0.55;
  return (
    <>
      <Hair y={HORIZON} n={8} step={15} op={0.17} />
      <line x1={cx - 30} y1={hz} x2={cx - 300} y2={H} stroke={C.ivory} strokeWidth={2} strokeOpacity={0.34} />
      <line x1={cx + 30} y1={hz} x2={cx + 300} y2={H} stroke={C.ivory} strokeWidth={2} strokeOpacity={0.34} />
      {/* jejak / garis tengah putus-putus */}
      {new Array(7).fill(0).map((_, i) => {
        const t0 = i / 7;
        const t1 = t0 + 0.055;
        const y0 = hz + (H - hz) * t0 ** 1.7;
        const y1 = hz + (H - hz) * t1 ** 1.7;
        const w0 = 6 + 40 * t0;
        return <rect key={i} x={cx - w0 / 2} y={y0} width={w0} height={Math.max(3, y1 - y0)} fill={C.sage} opacity={0.1 + 0.1 * t0} />;
      })}
      {/* satu titik di ufuk: tujuan yang tidak masuk akal */}
      <circle cx={cx} cy={hz} r={34} fill={C.orange} opacity={0.08 * (0.6 + 0.4 * lamp)} />
      <circle cx={cx} cy={hz} r={6} fill={C.orange} opacity={0.55 + 0.45 * lamp} />
    </>
  );
};

/** Kertas: lembar miring, garis tulis, satu kata dilingkari. */
const Paper: React.FC<{ lamp: number }> = ({ lamp }) => {
  const cx = W / 2;
  const top = H * 0.3;
  const w = 520;
  const h = 700;
  return (
    <>
      <g transform={`rotate(-4 ${cx} ${top + h / 2})`}>
        <rect x={cx - w / 2} y={top} width={w} height={h} fill="#101318" stroke={C.ivory} strokeWidth={2} strokeOpacity={0.42} />
        {new Array(12).fill(0).map((_, i) => (
          <line key={i} x1={cx - w / 2 + 48} y1={top + 96 + i * 44} x2={cx + w / 2 - 48 - (i % 4) * 60} y2={top + 96 + i * 44} stroke={C.sage} strokeWidth={2} strokeOpacity={0.16} />
        ))}
        {/* dua kata yang tidak bisa dijelaskan */}
        <rect x={cx - 130} y={top + 96 + 44 * 4 - 26} width={260} height={4} fill={C.orange} opacity={0.35 + 0.4 * lamp} />
      </g>
    </>
  );
};

/** Sinyal: busur konsentris dari satu titik + satu garis datar. */
const Signal: React.FC<{ lamp: number }> = ({ lamp }) => {
  const cx = W / 2;
  const cy = H * 0.46;
  return (
    <>
      <Hair y={HORIZON} n={5} step={14} op={0.12} />
      {new Array(6).fill(0).map((_, i) => (
        <circle key={i} cx={cx} cy={cy} r={70 + i * 74} fill="none" stroke={C.sage} strokeWidth={1.4} strokeOpacity={Math.max(0.03, 0.3 - i * 0.045)} />
      ))}
      <circle cx={cx} cy={cy} r={10} fill={C.orange} opacity={0.35 + 0.65 * lamp} />
      <circle cx={cx} cy={cy} r={46} fill={C.orange} opacity={0.05 * lamp} />
      {/* garis datar: tidak ada jawaban */}
      <line x1={96} y1={HORIZON + 120} x2={W - 96} y2={HORIZON + 120} stroke={C.ivory} strokeWidth={2} strokeOpacity={0.38} />
      <line x1={96} y1={HORIZON + 120} x2={96 + (W - 192) * (0.2 + 0.8 * lamp)} y2={HORIZON + 120} stroke={C.orange} strokeWidth={2} strokeOpacity={0.5} />
    </>
  );
};

/** Gunung: kerucut, kolom abu vertikal, satu garis pijar. */
const Plume: React.FC<{ lamp: number }> = ({ lamp }) => {
  const cx = W / 2;
  const base = HORIZON + 60;
  const summit = H * 0.52;
  return (
    <>
      <Hair y={base} n={6} step={15} op={0.13} />
      <S d={`M ${cx - 320} ${base} L ${cx - 40} ${summit} L ${cx + 40} ${summit} L ${cx + 340} ${base} Z`} o={0.5} w={2.4} />
      <path d={`M ${cx - 40} ${summit} L ${cx + 40} ${summit} L ${cx + 26} ${summit + 22} L ${cx - 26} ${summit + 22} Z`} fill={C.orange} opacity={0.08 + 0.16 * lamp} />
      {/* kolom abu */}
      <path
        d={`M ${cx - 44} ${summit} C ${cx - 120} ${summit - 240} ${cx + 60} ${summit - 420} ${cx - 10} ${H * 0.16}`}
        fill="none"
        stroke={C.ivory}
        strokeWidth={26}
        strokeOpacity={0.05}
        strokeLinecap="round"
      />
      <path
        d={`M ${cx - 30} ${summit} C ${cx - 90} ${summit - 220} ${cx + 70} ${summit - 380} ${cx + 20} ${H * 0.18}`}
        fill="none"
        stroke={C.sage}
        strokeWidth={2}
        strokeOpacity={0.22}
      />
    </>
  );
};

/** Air: permukaan tenang, refleksi terbalik dari satu bentuk. */
const Water: React.FC<{ lamp: number }> = ({ lamp }) => {
  const cx = W / 2;
  const y = H * 0.58;
  return (
    <>
      {new Array(14).fill(0).map((_, i) => (
        <line key={i} x1={0} y1={y + i * 26 + i * i * 0.8} x2={W} y2={y + i * 26 + i * i * 0.8} stroke={C.sage} strokeWidth={i === 0 ? 2.4 : 1} opacity={Math.max(0.02, 0.26 - i * 0.017)} />
      ))}
      {/* tebing di belakang danau: bentuk yang jatuh ke air */}
      <path d={`M 0 ${y} L 0 ${y - 300} L ${cx - 120} ${y - 60} L ${cx} ${y} Z`} fill="#0E1116" stroke={C.ivory} strokeWidth={1.4} strokeOpacity={0.18} />
      <path d={`M ${W} ${y} L ${W} ${y - 300} L ${cx + 140} ${y - 60} L ${cx} ${y} Z`} fill="#0E1116" stroke={C.ivory} strokeWidth={1.4} strokeOpacity={0.18} />
      {/* refleksi: segitiga terbalik, memudar ke bawah */}
      <path d={`M ${cx - 210} ${y} L ${cx} ${y + 300} L ${cx + 210} ${y} Z`} fill={C.ivory} opacity={0.03} />
      {/* garis pijar di permukaan */}
      <line x1={cx - 150} y1={y} x2={cx + 150} y2={y} stroke={C.orange} strokeWidth={2} strokeOpacity={0.2 + 0.35 * lamp} />
      <circle cx={cx} cy={y - 6} r={5} fill={C.orange} opacity={0.4 + 0.5 * lamp} />
    </>
  );
};

/** Dial: satu lingkaran bertakik, satu jarum berhenti di satu angka. */
const Dial: React.FC<{ lamp: number }> = ({ lamp }) => {
  const cx = W / 2;
  const cy = H * 0.47;
  const r = 260;
  const ticks = new Array(60).fill(0).map((_, i) => {
    const a = (i / 60) * Math.PI * 2;
    const long = i % 5 === 0;
    return (
      <line
        key={i}
        x1={cx + Math.sin(a) * r}
        y1={cy - Math.cos(a) * r}
        x2={cx + Math.sin(a) * (r - (long ? 22 : 10))}
        y2={cy - Math.cos(a) * (r - (long ? 22 : 10))}
        stroke={C.ivory}
        strokeWidth={long ? 2 : 1}
        strokeOpacity={long ? 0.45 : 0.2}
      />
    );
  });
  const handAngle = -0.9;
  return (
    <>
      {ticks}
      <circle cx={cx} cy={cy} r={r} fill="none" stroke={C.ivory} strokeWidth={2} strokeOpacity={0.28} />
      <line x1={cx} y1={cy} x2={cx + Math.sin(handAngle) * (r - 40)} y2={cy - Math.cos(handAngle) * (r - 40)} stroke={C.ivory} strokeWidth={4} strokeOpacity={0.7} />
      <line x1={cx} y1={cy} x2={cx + Math.sin(0.4) * (r - 110)} y2={cy - Math.cos(0.4) * (r - 110)} stroke={C.ivory} strokeWidth={2} strokeOpacity={0.4} />
      <circle cx={cx} cy={cy} r={9} fill={C.ivory} opacity={0.6} />
      {/* satu angka yang berbahaya: bercak oranye */}
      <circle cx={cx + Math.sin(-0.9) * (r - 46)} cy={cy - Math.cos(-0.9) * (r - 46)} r={16} fill={C.orange} opacity={0.12 * lamp} />
    </>
  );
};

/** Punggung bukit: tiga lapis, satu tiang berdiri, satu sosok. */
const Ridge: React.FC<{ lamp: number }> = ({ lamp }) => {
  const cx = W / 2;
  return (
    <>
      <Hair y={HORIZON + 90} n={5} step={16} op={0.1} />
      <path d={`M 0 ${H * 0.62} C ${W * 0.22} ${H * 0.5} ${W * 0.34} ${H * 0.58} ${W * 0.52} ${H * 0.54} C ${W * 0.72} ${H * 0.5} ${W * 0.86} ${H * 0.58} ${W} ${H * 0.55} L ${W} ${H} L 0 ${H} Z`} fill="#0E1116" stroke={C.ivory} strokeWidth={1.4} strokeOpacity={0.22} />
      <path d={`M 0 ${H * 0.68} C ${W * 0.3} ${H * 0.6} ${W * 0.5} ${H * 0.66} ${W * 0.72} ${H * 0.63} C ${W * 0.86} ${H * 0.61} ${W * 0.94} ${H * 0.64} ${W} ${H * 0.63} L ${W} ${H} L 0 ${H} Z`} fill="#0A0C0F" stroke={C.ivory} strokeWidth={1.4} strokeOpacity={0.16} />
      {/* tiang */}
      <line x1={cx} y1={H * 0.6} x2={cx} y2={H * 0.44} stroke={C.ivory} strokeWidth={3} strokeOpacity={0.5} />
      <line x1={cx - 52} y1={H * 0.5} x2={cx + 52} y2={H * 0.5} stroke={C.ivory} strokeWidth={2.4} strokeOpacity={0.4} />
      <circle cx={cx} cy={H * 0.44} r={16} fill={C.orange} opacity={0.08 * lamp} />
      <circle cx={cx} cy={H * 0.44} r={4} fill={C.orange} opacity={lamp} />
    </>
  );
};

export const PlateArt: React.FC<{ kind: PlateKind; lamp: number }> = ({ kind, lamp }) => {
  switch (kind) {
    case "vessel":
      return <Vessel lamp={lamp} />;
    case "shelter":
      return <Shelter lamp={lamp} />;
    case "road":
      return <Road lamp={lamp} />;
    case "paper":
      return <Paper lamp={lamp} />;
    case "signal":
      return <Signal lamp={lamp} />;
    case "plume":
      return <Plume lamp={lamp} />;
    case "water":
      return <Water lamp={lamp} />;
    case "dial":
      return <Dial lamp={lamp} />;
    case "ridge":
      return <Ridge lamp={lamp} />;
    case "tower":
    default:
      return <Tower lamp={lamp} />;
  }
};
