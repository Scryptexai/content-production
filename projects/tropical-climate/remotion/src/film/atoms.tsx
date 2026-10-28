import React, {useEffect, useState} from 'react';
import {
  AbsoluteFill,
  Easing,
  Img,
  continueRender,
  delayRender,
  interpolate,
  staticFile,
  useCurrentFrame,
} from 'remotion';
import {FONT_CSS, FONT_SPECS} from './fonts';

// ---------------------------------------------------------------- tokens
export const C = {
  bg: '#0B0C0A',
  paper: '#EDE4D3',
  muted: '#8B8577',
  terra: '#C0603A',
  teal: '#2E5F5B',
  gold: '#C9A227',
  ink: '#12140F',
};

export const F = {
  serif: 'DMSerif, Georgia, serif',
  sans: 'Inter, system-ui, sans-serif',
  mono: 'PlexMono, ui-monospace, monospace',
};

export const W = 1080;
export const H = 1920;

export const EASE = Easing.bezier(0.22, 1, 0.36, 1);
export const EASE_IO = Easing.bezier(0.65, 0, 0.35, 1);

/** clamp-interpolate dengan easing default */
export const ip = (
  frame: number,
  range: [number, number],
  out: [number, number],
  easing: (t: number) => number = EASE,
) =>
  interpolate(frame, range, out, {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
    easing,
  });

// ---------------------------------------------------------------- background
export const Bg: React.FC<{
  src: string;
  dur: number;
  from?: number;
  to?: number;
  tx?: number;
  ty?: number;
  bright?: number;
  blur?: number;
}> = ({src, dur, from = 1.02, to = 1.1, tx = 0, ty = 0, bright = 1, blur = 0}) => {
  const frame = useCurrentFrame();
  const scale = ip(frame, [0, dur], [from, to], EASE_IO);
  const dx = ip(frame, [0, dur], [0, tx], EASE_IO);
  const dy = ip(frame, [0, dur], [0, ty], EASE_IO);
  return (
    <AbsoluteFill style={{overflow: 'hidden', backgroundColor: C.bg}}>
      <Img
        src={staticFile(src)}
        style={{
          width: '100%',
          height: '100%',
          objectFit: 'cover',
          transform: `scale(${scale}) translate(${dx}px, ${dy}px)`,
          filter: `brightness(${bright})${blur ? ` blur(${blur}px)` : ''}`,
        }}
      />
    </AbsoluteFill>
  );
};

/** Gradien gelap untuk keterbacaan + vignette */
export const Scrim: React.FC<{top?: number; bottom?: number; mid?: number; color?: string}> = ({
  top = 0,
  bottom = 0,
  mid = 0,
  color = '11,12,10',
}) => (
  <AbsoluteFill
    style={{
      background: [
        top ? `linear-gradient(to bottom, rgba(${color},${top}) 0%, rgba(${color},0) 46%)` : '',
        bottom ? `linear-gradient(to top, rgba(${color},${bottom}) 0%, rgba(${color},0) 52%)` : '',
        mid
          ? `linear-gradient(to bottom, rgba(${color},0) 26%, rgba(${color},${mid}) 44%, rgba(${color},${mid}) 66%, rgba(${color},0) 84%)`
          : '',
      ]
        .filter(Boolean)
        .join(','),
    }}
  />
);

/** Vignette lembut di semua sisi */
export const Vignette: React.FC<{strength?: number}> = ({strength = 0.55}) => (
  <AbsoluteFill
    style={{
      background: `radial-gradient(ellipse 78% 62% at 50% 46%, rgba(0,0,0,0) 38%, rgba(0,0,0,${strength}) 100%)`,
    }}
  />
);

// ---------------------------------------------------------------- type
export const Kicker: React.FC<{
  children: React.ReactNode;
  delay?: number;
  color?: string;
  y?: number;
  size?: number;
}> = ({children, delay = 0, color = C.gold, y = 200, size = 26}) => {
  const frame = useCurrentFrame();
  const o = ip(frame, [delay, delay + 12], [0, 1]);
  const ty = ip(frame, [delay, delay + 14], [10, 0]);
  return (
    <div
      style={{
        position: 'absolute',
        top: y,
        left: 0,
        right: 0,
        textAlign: 'center',
        fontFamily: F.sans,
        fontWeight: 600,
        fontSize: size,
        letterSpacing: size * 0.22,
        color,
        opacity: o,
        transform: `translateY(${ty}px)`,
      }}
    >
      {children}
    </div>
  );
};

/** Kata muncul satu per satu: opacity + translateY */
export const Words: React.FC<{
  text: string;
  delay?: number;
  per?: number;
  size?: number;
  font?: string;
  color?: string;
  italic?: boolean;
  weight?: number;
  align?: 'left' | 'center';
  left?: number;
  right?: number;
  top?: number;
  lineHeight?: number;
  letter?: number;
  maxWidth?: number;
}> = ({
  text,
  delay = 0,
  per = 2.6,
  size = 120,
  font = F.serif,
  color = C.paper,
  italic = false,
  weight = 400,
  align = 'center',
  left = 70,
  right = 70,
  top = 0,
  lineHeight = 1.06,
  letter = -1,
  maxWidth,
}) => {
  const frame = useCurrentFrame();
  const words = text.split(' ');
  return (
    <div
      style={{
        position: 'absolute',
        top,
        left: align === 'center' ? left : left,
        width: maxWidth ?? `calc(100% - ${left + right}px)`,
        display: 'flex',
        flexWrap: 'wrap',
        justifyContent: align === 'center' ? 'center' : 'flex-start',
        gap: `0 ${size * 0.24}px`,
        fontFamily: font,
        fontWeight: weight,
        fontStyle: italic ? 'italic' : 'normal',
        fontSize: size,
        lineHeight,
        letterSpacing: letter,
        color,
      }}
    >
      {words.map((w, i) => {
        const d = delay + i * per;
        const o = ip(frame, [d, d + 10], [0, 1]);
        const ty = ip(frame, [d, d + 13], [size * 0.22, 0]);
        return (
          <span key={i} style={{opacity: o, transform: `translateY(${ty}px)`, display: 'inline-block'}}>
            {w}
          </span>
        );
      })}
    </div>
  );
};

/** Garis aksen yang tumbuh dari tengah */
export const Rule: React.FC<{
  delay?: number;
  y: number;
  width?: number;
  thickness?: number;
  color?: string;
  dur?: number;
}> = ({delay = 0, y, width = 620, thickness = 3, color = C.gold, dur = 16}) => {
  const frame = useCurrentFrame();
  const p = ip(frame, [delay, delay + dur], [0, 1]);
  return (
    <div
      style={{
        position: 'absolute',
        top: y,
        left: '50%',
        width: width * p,
        height: thickness,
        marginLeft: -(width * p) / 2,
        backgroundColor: color,
      }}
    />
  );
};

/** Angka besar monospace */
export const Num: React.FC<{
  children: React.ReactNode;
  delay?: number;
  size?: number;
  color?: string;
  top?: number;
  align?: 'center' | 'left';
  left?: number;
}> = ({children, delay = 0, size = 200, color = C.paper, top = 0, align = 'center', left = 120}) => {
  const frame = useCurrentFrame();
  const p = ip(frame, [delay, delay + 16], [0, 1]);
  const ty = ip(frame, [delay, delay + 20], [size * 0.12, 0]);
  return (
    <div
      style={{
        position: 'absolute',
        top,
        left: align === 'center' ? 0 : left,
        right: align === 'center' ? 0 : undefined,
        textAlign: align,
        fontFamily: F.mono,
        fontWeight: 600,
        fontSize: size,
        lineHeight: 0.92,
        letterSpacing: -size * 0.04,
        color,
        opacity: p,
        transform: `translateY(${ty}px)`,
      }}
    >
      {children}
    </div>
  );
};


/**
 * Memasang @font-face dan menahan frame sampai glyph siap.
 * Handle selalu dilepas (finally + timeout pengaman 8 dtk), jadi render tidak
 * pernah gagal karena font.
 */
export const FontGate: React.FC = () => {
  const [handle] = useState(() => delayRender('fonts'));
  useEffect(() => {
    let done = false;
    const finish = () => {
      if (done) return;
      done = true;
      continueRender(handle);
    };
    const safety = setTimeout(finish, 8000);
    Promise.all(FONT_SPECS.map((spec) => document.fonts.load(spec)))
      .then(() => document.fonts.ready)
      .catch(() => undefined)
      .finally(() => {
        clearTimeout(safety);
        finish();
      });
    return () => clearTimeout(safety);
  }, [handle]);
  return <style dangerouslySetInnerHTML={{__html: FONT_CSS}} />;
};
