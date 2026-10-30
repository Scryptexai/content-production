/**
 * Type.tsx — tipografi film. Teks di sini selalu KETERANGAN, bukan subjek:
 * serif untuk pernyataan, mono untuk label & sumber, sans untuk badan.
 *
 * Mekanik masuknya mengikuti kartu tipografi shotcraft (paper-title-card /
 * type-entrance-moves): per kata naik dari balik garis, bukan fade serentak;
 * angka memakai roll per digit (digit-roll) supaya nilai terasa "dihitung".
 */
import React from 'react';
import { useCurrentFrame } from 'remotion';
import { C, TYPE, alpha, tracking } from './theme';
import { EASE, clamp01, ramp, seeded } from './motion';

type RevealProps = {
  text: string;
  /** frame lokal saat mulai */
  at: number;
  /** durasi masuk per kata */
  each?: number;
  gap?: number;
  size?: number;
  color?: string;
  serif?: boolean;
  italic?: boolean;
  weight?: number;
  caps?: boolean;
  mono?: boolean;
  align?: 'left' | 'center' | 'right';
  lineHeight?: number;
  /** keluar: frame lokal mulai keluar */
  outAt?: number;
  outDur?: number;
  style?: React.CSSProperties;
};

export const Reveal: React.FC<RevealProps> = ({
  text,
  at,
  each = 13,
  gap = 4,
  size = TYPE.body,
  color = C.cream,
  serif = false,
  italic = false,
  weight = serif ? 400 : 500,
  caps = false,
  mono = false,
  align = 'left',
  lineHeight,
  outAt,
  outDur = 12,
  style,
}) => {
  const frame = useCurrentFrame();
  const words = text.split(/(\s+)/);
  const outT = outAt === undefined ? 0 : EASE.exit(clamp01((frame - outAt) / outDur));
  let k = 0;
  return (
    <div
      style={{
        display: 'block',
        textAlign: align,
        fontFamily: serif ? '"Instrument Serif", Georgia, serif' : mono ? '"JetBrains Mono", monospace' : 'Inter, sans-serif',
        fontSize: size,
        fontWeight: weight,
        fontStyle: italic ? 'italic' : undefined,
        color,
        letterSpacing: tracking(size, caps),
        textTransform: caps ? 'uppercase' : undefined,
        lineHeight: lineHeight ?? (serif ? 1.06 : 1.28),
        ...style,
      }}
    >
      {words.map((w, i) => {
        if (/^\s+$/.test(w)) return <span key={i}>{w}</span>;
        const idx = k++;
        const p = EASE.snappy(clamp01((frame - at - idx * gap) / each));
        return (
          <span
            key={i}
            style={{
              display: 'inline-block',
              overflow: 'hidden',
              verticalAlign: 'top',
              padding: '0.04em 0.01em 0.17em',
              margin: '-0.04em -0.01em -0.17em',
            }}
          >
            <span
              style={{
                display: 'inline-block',
                transform: `translateY(${((1 - p) * 108 - outT * 108).toFixed(2)}%)`,
                opacity: clamp01(p * 1.4) * (1 - outT),
              }}
            >
              {w}
            </span>
          </span>
        );
      })}
    </div>
  );
};

/** label kecil di atas judul + garis tipis yang tumbuh */
export const Kicker: React.FC<{
  text: string;
  at: number;
  color?: string;
  x?: number;
  y?: number;
  align?: 'left' | 'center';
  rule?: boolean;
  width?: number;
}> = ({ text, at, color = C.muted, align = 'center', rule = true, width = 74 }) => {
  const frame = useCurrentFrame();
  const p = ramp(frame, at, 22, EASE.out);
  const r = ramp(frame, at + 6, 20, EASE.out);
  return (
    <div
      style={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: align === 'center' ? 'center' : 'flex-start',
        gap: 18,
        opacity: p,
        transform: `translateY(${((1 - p) * 10).toFixed(2)}px)`,
      }}
    >
      {rule && align === 'center' && (
        <div style={{ width: width * r, height: 1, background: alpha(color, 0.6) }} />
      )}
      <div
        style={{
          fontFamily: '"JetBrains Mono", monospace',
          fontSize: TYPE.label,
          letterSpacing: '0.24em',
          textTransform: 'uppercase',
          color,
          whiteSpace: 'nowrap',
        }}
      >
        {text}
      </div>
      {rule && (
        <div style={{ width: width * r, height: 1, background: alpha(color, 0.6) }} />
      )}
    </div>
  );
};

/** angka besar dengan roll per digit (digit-roll) */
export const RollNumber: React.FC<{
  value: string;
  at: number;
  size?: number;
  color?: string;
  serif?: boolean;
  align?: 'left' | 'center' | 'right';
  dur?: number;
}> = ({ value, at, size = TYPE.display, color = C.rose, serif = true, align = 'center', dur = 26 }) => {
  const frame = useCurrentFrame();
  const p = EASE.out(clamp01((frame - at) / dur));
  const chars = Array.from(value);
  return (
    <div
      style={{
        display: 'flex',
        justifyContent: align === 'center' ? 'center' : align === 'right' ? 'flex-end' : 'flex-start',
        gap: '0.02em',
        fontFamily: serif ? '"Instrument Serif", Georgia, serif' : 'Inter, sans-serif',
        fontSize: size,
        fontWeight: serif ? 400 : 700,
        color,
        lineHeight: 0.92,
        letterSpacing: '-0.02em',
        fontVariantNumeric: 'tabular-nums',
        opacity: clamp01(p * 3),
      }}
    >
      {chars.map((ch, i) => {
        const local = clamp01((p - i * 0.04) / 0.55);
        const isDigit = /[0-9]/.test(ch);
        return (
          <span key={i} style={{ display: 'inline-block', overflow: 'hidden', height: size * 0.95 }}>
            <span
              style={{
                display: 'inline-block',
                transform: `translateY(${((1 - EASE.out(local)) * (isDigit ? 62 : 18)).toFixed(2)}%)`,
                opacity: clamp01(local * 1.6),
              }}
            >
              {ch}
            </span>
          </span>
        );
      })}
    </div>
  );
};

/** garis sumber di dasar bingkai */
export const Source: React.FC<{ text: string; at: number; y?: number; color?: string; size?: number }> = ({
  text,
  at,
  color = C.muted2,
  size = TYPE.source,
}) => {
  const frame = useCurrentFrame();
  const p = ramp(frame, at, 26, EASE.out);
  return (
    <div
      style={{
        fontFamily: '"JetBrains Mono", monospace',
        fontSize: size,
        letterSpacing: '0.06em',
        color,
        opacity: p * 0.92,
        textAlign: 'center',
        transform: `translateY(${((1 - p) * 8).toFixed(1)}px)`,
      }}
    >
      {text}
    </div>
  );
};

/** huruf yang bergerak sedikit mengikuti getaran kamera (untuk stempel akhir) */
export const Jitter: React.FC<{ frame: number; amount?: number; children: React.ReactNode }> = ({
  frame,
  amount = 1.6,
  children,
}) => {
  const x = (seeded(frame * 1.7) - 0.5) * amount;
  const y = (seeded(frame * 2.3 + 9) - 0.5) * amount;
  return <div style={{ transform: `translate(${x.toFixed(2)}px, ${y.toFixed(2)}px)` }}>{children}</div>;
};
