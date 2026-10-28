import React from 'react';
import {AbsoluteFill, interpolate, staticFile, useCurrentFrame} from 'remotion';
import {C, EASE, F, H, Vignette, W, ip} from './atoms';

/**
 * Bumper judul — kartu judul editorial 5 detik.
 * Versi Remotion-native dari PaperTitleCard (video-shotcraft) yang sudah
 * di-reskin ke palet film. Tidak lagi bergantung pada template eksternal.
 */
export const Bumper: React.FC = () => {
  const frame = useCurrentFrame();
  const sweep = ip(frame, [10, 60], [-40, 140], EASE);
  const rule = ip(frame, [52, 84], [0, 1], EASE);
  const sub = ip(frame, [76, 96], [0, 1]);
  const out = interpolate(frame, [140, 152], [1, 0.86], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  return (
    <AbsoluteFill style={{backgroundColor: C.bg, opacity: out}}>
      {/* tekstur kertas halus */}
      <AbsoluteFill
        style={{
          opacity: 0.32,
          backgroundImage: `url(${staticFile('images/01-skin-macro.jpg')})`,
          backgroundSize: 'cover',
          filter: 'grayscale(1) brightness(0.22) contrast(1.4)',
        }}
      />
      <AbsoluteFill
        style={{
          background: `linear-gradient(115deg, rgba(192,96,58,${0.1 * (sweep / 140)}) 0%, rgba(11,12,10,0) 55%)`,
        }}
      />
      <Vignette strength={0.72} />

      {/* persegi panjang aksen yang menyapu */}
      <div
        style={{
          position: 'absolute',
          top: 0,
          left: 0,
          width: 6,
          height: H,
          backgroundColor: C.terra,
          transform: `translateX(${sweep * 7.7}px)`,
          opacity: 0.5,
        }}
      />

      <div style={{position: 'absolute', top: 590, left: 96, right: 96}}>
        <div
          style={{
            fontFamily: F.mono,
            fontWeight: 500,
            fontSize: 24,
            letterSpacing: 8,
            color: C.gold,
            opacity: ip(frame, [18, 40], [0, 1]),
            marginBottom: 30,
          }}
        >
          SEBUAH NARASI · 3 MENIT
        </div>

        {['KULIT', 'TROPIS.'].map((word, wi) => {
          const d = 24 + wi * 16;
          return (
            <div
              key={word}
              style={{
                fontFamily: F.serif,
                fontSize: 132,
                lineHeight: 1.04,
                letterSpacing: -2,
                color: wi === 0 ? C.paper : C.terra,
                clipPath: `inset(${100 - ip(frame, [d, d + 26], [0, 100], EASE)}% 0 0 0)`,
                transform: `translateY(${ip(frame, [d, d + 30], [18, 0], EASE)}px)`,
              }}
            >
              {word}
            </div>
          );
        })}

        <div style={{height: 3, width: 300 * rule, backgroundColor: C.gold, margin: '34px 0 26px'}} />

        <div
          style={{
            fontFamily: F.sans,
            fontWeight: 600,
            fontSize: 30,
            letterSpacing: 6,
            color: C.muted,
            opacity: sub,
            transform: `translateY(${(1 - sub) * 10}px)`,
          }}
        >
          FORMULA SUBTROPIS
        </div>
      </div>

      <div
        style={{
          position: 'absolute',
          bottom: 120,
          left: 0,
          right: 0,
          textAlign: 'center',
          fontFamily: F.mono,
          fontSize: 22,
          letterSpacing: 4,
          color: C.muted,
          opacity: ip(frame, [96, 116], [0, 1]),
        }}
      >
        EPISODE 01 · KULIT &amp; IKLIM
      </div>
    </AbsoluteFill>
  );
};
