import React from 'react';
import {AbsoluteFill, Easing, interpolate, useCurrentFrame} from 'remotion';
import {Bg, C, EASE, F, H, Kicker, Num, Rule, Scrim, Vignette, W, Words, ip} from './atoms';

/* ------------------------------------------------------------------ kit */

const FPS = 30;

/** Band gelap untuk blok teks (pengganti scrim lokal di render.py) */
const Band: React.FC<{top: number; bottom: number; a?: number; feather?: number}> = ({
  top,
  bottom,
  a = 0.62,
  feather = 90,
}) => (
  <div
    style={{
      position: 'absolute',
      top: top - feather,
      height: bottom - top + feather * 2,
      left: 0,
      right: 0,
      background: `linear-gradient(to bottom, rgba(11,12,10,0) 0%, rgba(11,12,10,${a}) ${feather}px, rgba(11,12,10,${a}) ${
        bottom - top + feather
      }px, rgba(11,12,10,0) 100%)`,
    }}
  />
);

const Overlay: React.FC<{a: number}> = ({a}) => (
  <AbsoluteFill style={{backgroundColor: `rgba(11,12,10,${a})`}} />
);

const Svg: React.FC<{children: React.ReactNode}> = ({children}) => (
  <svg
    width={W}
    height={H}
    viewBox={`0 0 ${W} ${H}`}
    style={{position: 'absolute', top: 0, left: 0}}
  >
    {children}
  </svg>
);

const Arrow: React.FC<{
  x: number;
  y0: number;
  y1: number;
  color: string;
  p: number;
  width?: number;
}> = ({x, y0, y1, color, p, width = 7}) => {
  if (p <= 0) return null;
  const end = y0 + (y1 - y0) * p;
  const head = 16;
  const dir = y1 < y0 ? -1 : 1;
  return (
    <g opacity={p}>
      <line x1={x} y1={y0} x2={x} y2={end - dir * head * 0.9} stroke={color} strokeWidth={width} />
      {p > 0.8 && (
        <polygon
          points={`${x},${end} ${x - head},${end - dir * head} ${x + head},${end - dir * head}`}
          fill={color}
        />
      )}
    </g>
  );
};

/** Label kecil ber-tracking (setara label() di render.py) */
const Label: React.FC<{
  children: React.ReactNode;
  top: number;
  color?: string;
  size?: number;
  delay?: number;
  tracking?: number;
}> = ({children, top, color = C.gold, size = 26, delay = 0.2, tracking = 0.2}) => (
  <Kicker color={color} y={top} size={size} delay={delay * FPS}>
    <span style={{letterSpacing: size * tracking}}>{children}</span>
  </Kicker>
);

/* ------------------------------------------------------------------ 01 */
export const Scene01: React.FC<{dur: number}> = ({dur}) => {
  const frame = useCurrentFrame();
  const cut = 8 * FPS;
  const cold = frame < cut;

  return (
    <AbsoluteFill style={{backgroundColor: C.bg}}>
      {cold ? (
        <Bg src="images/02-cold-window.jpg" dur={cut} from={1.04} to={1.1} ty={10} bright={0.82} />
      ) : (
        <Bg
          src="images/03-tropical-window.jpg"
          dur={dur - cut}
          from={1.1}
          to={1.02}
          ty={-10}
          bright={0.9}
        />
      )}
      <Scrim top={cold ? 0.55 : 0.3} bottom={cold ? 0.7 : 0.55} />
      <Vignette strength={0.5} />

      {cold ? (
        <>
          <Num delay={0.5 * FPS} top={498} size={196}>
            12°C
          </Num>
          <Label top={834} color={C.paper} size={25} delay={0.7} tracking={0.16}>
            SUHU RATA-RATA · EROPA
          </Label>
        </>
      ) : (
        <>
          <Band top={1060} bottom={1350} a={0.72} />
          <Label top={1078} size={26} delay={0.1} tracking={0.24}>
            KOTA INI
          </Label>
          <Words text="JAKARTA" delay={0.25 * FPS} size={132} top={1120} letter={2} />
          <Label top={1310} color={C.paper} size={26} delay={0.55} tracking={0.1}>
            27–30°C · KELEMBAPAN 74–84%
          </Label>
        </>
      )}
    </AbsoluteFill>
  );
};

/* ------------------------------------------------------------------ 02 */
const StatRow: React.FC<{
  name: string;
  num: string;
  unit: string;
  top: number;
  at: number;
  last?: boolean;
}> = ({name, num, unit, top, at}) => {
  const frame = useCurrentFrame();
  const a = ip(frame, [at, at + 11], [0, 1]);
  const ty = ip(frame, [at, at + 14], [18, 0]);
  const bar = ip(frame, [at + 2, at + 26], [0, 1], EASE);
  return (
    <div style={{position: 'absolute', top, left: 120, right: 120, opacity: a, transform: `translateY(${ty}px)`}}>
      <div style={{fontFamily: F.sans, fontWeight: 600, fontSize: 24, letterSpacing: 5, color: C.muted}}>
        {name}
      </div>
      <div style={{display: 'flex', alignItems: 'flex-end', marginTop: 14}}>
        <span
          style={{
            fontFamily: F.mono,
            fontWeight: 600,
            fontSize: 150,
            lineHeight: 1,
            color: C.paper,
            letterSpacing: -4,
          }}
        >
          {num}
        </span>
        <span
          style={{
            fontFamily: F.sans,
            fontWeight: 800,
            fontSize: 40,
            color: C.terra,
            marginLeft: 16,
            marginBottom: 22,
          }}
        >
          {unit}
        </span>
      </div>
      <div style={{marginTop: 24, height: 1, width: 840 * bar, backgroundColor: 'rgba(255,255,255,0.13)'}} />
    </div>
  );
};

export const Scene02: React.FC<{dur: number}> = ({dur}) => (
  <AbsoluteFill style={{backgroundColor: C.bg}}>
    <Bg src="images/03-tropical-window.jpg" dur={dur} from={1.06} to={1} ty={6} bright={0.85} />
    <Overlay a={0.6} />
    <Vignette strength={0.45} />
    <Label top={248} size={26} tracking={0.22}>
      JAKARTA · DATA IKLIM
    </Label>
    <Rule y={308} delay={0.4 * FPS} width={700} thickness={3} />
    <StatRow name="SUHU" num="27–30" unit="°C" top={470} at={0.9 * FPS} />
    <StatRow name="KELEMBAPAN" num="74–84" unit="%" top={800} at={2.4 * FPS} />
    <StatRow name="INDEKS UV" num="11" unit="EXTREME" top={1130} at={4.4 * FPS} last />
    <Label top={1700} color={C.muted} size={21} delay={5.4} tracking={0.12}>
      SUMBER: BMKG / WEATHER2TRAVEL / BRITANNICA
    </Label>
  </AbsoluteFill>
);

/* ------------------------------------------------------------------ 03 */
export const Scene03: React.FC<{dur: number}> = () => (
  <AbsoluteFill style={{backgroundColor: C.bg}}>
    <Bg src="images/01-skin-macro.jpg" dur={321} from={1.08} to={1.02} ty={6} bright={0.86} />
    <Overlay a={0.47} />
    <Band top={580} bottom={1090} a={0.66} />
    <Vignette strength={0.5} />
    <Words text="BUKAN" size={130} top={612} delay={0.25 * FPS} />
    <Words text="DETAIL KECIL." size={130} top={760} color={C.terra} delay={0.75 * FPS} />
    <Rule y={950} delay={1.5 * FPS} width={620} thickness={3} />
    <Words
      text="dua lingkungan. dua kimia."
      size={46}
      top={1006}
      font={F.sans}
      weight={500}
      letter={0.2}
      delay={2 * FPS}
      per={3}
    />
  </AbsoluteFill>
);

/* ------------------------------------------------------------------ 04 */
export const Scene04: React.FC<{dur: number}> = ({dur}) => (
  <AbsoluteFill style={{backgroundColor: C.bg}}>
    <Bg src="images/04-glycerin-drop.jpg" dur={dur} from={1.1} to={1.02} ty={-8} bright={0.9} />
    <Band top={280} bottom={1010} a={0.62} />
    <Vignette strength={0.45} />
    <Label top={298} size={28} tracking={0.2}>
      BAHAN 01
    </Label>
    <Words text="HUMEKTAN" size={142} top={372} delay={0.5 * FPS} letter={-2} />
    <Rule y={568} delay={1.1 * FPS} width={640} thickness={3} color={C.terra} />
    <Words
      text="gliserin · asam hialuronat"
      size={44}
      top={628}
      font={F.sans}
      weight={400}
      delay={1.4 * FPS}
      per={3}
    />
    <Words
      text="menarik air"
      size={62}
      top={754}
      font={F.sans}
      weight={800}
      color={C.teal}
      delay={2.6 * FPS}
      per={3.4}
    />
    <Words
      text="dari mana?"
      size={96}
      top={892}
      color={C.gold}
      italic
      delay={7.2 * FPS}
      per={4}
    />
  </AbsoluteFill>
);

/* ------------------------------------------------------------------ 05 */
const Panel: React.FC<{
  x0: number;
  x1: number;
  acc: string;
  title: string;
  rh: string;
  at: number;
  up: boolean;
  lines: [string, string][];
}> = ({x0, x1, acc, title, rh, at, up, lines}) => {
  const frame = useCurrentFrame();
  const p = ip(frame, [at, at + 24], [0, 1], EASE);
  const ys = 1120;
  return (
    <>
      <Svg>
        <rect
          x={x0}
          y={470}
          width={x1 - x0}
          height={820}
          rx={20}
          fill={`rgba(17,19,16,${0.86 * p})`}
          stroke={acc}
          strokeWidth={3}
          opacity={p}
        />
        <rect x={x0} y={494} width={8} height={72} fill={acc} opacity={p} />
        <line x1={x0 + 30} y1={ys} x2={x1 - 30} y2={ys} stroke={C.paper} strokeWidth={3} opacity={0.55 * p} />
        {[0, 1, 2].map((i) => {
          const d = at + 15 + i * 6.6;
          const p2 = ip(frame, [d, d + 20], [0, 1], EASE);
          const ax = x0 + 105 + i * 100;
          return up ? (
            <Arrow key={i} x={ax} y0={ys - 20} y1={820 - i * 18} color={acc} p={p2} />
          ) : (
            <Arrow key={i} x={ax} y0={820 + i * 18} y1={ys - 20} color={acc} p={p2} />
          );
        })}
      </Svg>

      <div style={{position: 'absolute', left: x0 + 34, top: 504, opacity: p}}>
        <div style={{fontFamily: F.sans, fontWeight: 800, fontSize: 30, letterSpacing: 3, color: acc}}>
          {title}
        </div>
        <div style={{fontFamily: F.mono, fontWeight: 600, fontSize: 56, color: C.paper, marginTop: 4}}>
          {rh}
        </div>
      </div>

      <div
        style={{
          position: 'absolute',
          left: x0 + 30,
          top: 780,
          fontFamily: F.sans,
          fontSize: 28,
          color: C.paper,
          opacity: 0.86 * p,
        }}
      >
        {up ? 'air dari udara' : 'air dari kulit'}
      </div>

      <div
        style={{
          position: 'absolute',
          left: x0 + 30,
          top: ys + 14,
          fontFamily: F.sans,
          fontSize: 24,
          color: C.muted,
          opacity: p,
        }}
      >
        permukaan kulit
      </div>

      <div style={{position: 'absolute', left: x0 + 30, top: ys + 68, opacity: p}}>
        {lines.map(([txt, col], i) => (
          <div
            key={i}
            style={{
              fontFamily: F.sans,
              fontWeight: col === C.paper ? 400 : 800,
              fontSize: 30,
              lineHeight: '46px',
              color: col,
            }}
          >
            {txt}
          </div>
        ))}
      </div>
    </>
  );
};

export const Scene05: React.FC<{dur: number}> = ({dur}) => (
  <AbsoluteFill style={{backgroundColor: C.bg}}>
    <Bg src="images/01-skin-macro.jpg" dur={dur} from={1.05} to={1} bright={0.7} />
    <Overlay a={0.82} />
    <Label top={198} size={25} tracking={0.22}>
      HUMEKTAN · DUA KONDISI
    </Label>
    <Panel
      x0={70}
      x1={510}
      acc={C.teal}
      title="LEMBAP"
      rh="80% RH"
      at={1.0 * FPS}
      up={false}
      lines={[
        ['→ lengket,', C.terra],
        ['   tidak menguap', C.paper],
      ]}
    />
    <Panel
      x0={570}
      x1={1010}
      acc={C.terra}
      title="KERING"
      rh="40% RH"
      at={7.6 * FPS}
      up
      lines={[
        ['→ makin kering', C.terra],
        ['   di ruang ber-AC', C.paper],
      ]}
    />
    <Words
      text="bahan yang sama. dua hasil."
      size={60}
      top={1436}
      delay={16.6 * FPS}
      per={4}
    />
  </AbsoluteFill>
);

/* ------------------------------------------------------------------ 06 */
export const Scene06: React.FC<{dur: number}> = ({dur}) => {
  const frame = useCurrentFrame();
  const p = ip(frame, [10 * FPS, 10 * FPS + 27], [0, 1], EASE);
  const ytop = 780;
  return (
    <AbsoluteFill style={{backgroundColor: C.bg}}>
      <Bg src="images/05-petrolatum.jpg" dur={dur} from={1.02} to={1.1} ty={-8} bright={0.88} />
      <Band top={240} bottom={650} a={0.6} />
      <Vignette strength={0.5} />
      <Label top={258} size={28}>
        BAHAN 02
      </Label>
      <Words text="OKLUSIF" size={150} top={322} delay={0.5 * FPS} letter={-2} />
      <Words
        text="petrolatum · minyak mineral · lilin"
        size={40}
        top={518}
        font={F.sans}
        delay={1.3 * FPS}
        per={3}
      />
      <Rule y={600} delay={2 * FPS} width={620} thickness={3} color={C.terra} />

      {p > 0 && (
        <>
          <Svg>
            <rect
              x={70}
              y={ytop - 60}
              width={940}
              height={430}
              rx={22}
              fill="rgba(15,17,14,0.92)"
              stroke="rgba(192,96,58,0.55)"
              strokeWidth={2}
              opacity={p}
            />
            <rect x={100} y={ytop + 6} width={880} height={46} rx={8} fill={C.terra} opacity={p} />
            <rect x={100} y={ytop + 52} width={880} height={252} fill="#231D18" opacity={p} />
            {[240, 430, 620, 810].map((ax, i) => {
              const d = 10.6 * FPS + i * 4.5;
              const p2 = ip(frame, [d, d + 18], [0, 1], EASE);
              return <Arrow key={ax} x={ax} y0={ytop + 240} y1={ytop + 92} color={C.gold} p={p2} width={5} />;
            })}
          </Svg>
          <div
            style={{
              position: 'absolute',
              left: 100,
              top: ytop - 46,
              fontFamily: F.sans,
              fontWeight: 800,
              fontSize: 23,
              letterSpacing: 4,
              color: C.terra,
              opacity: p,
            }}
          >
            LAPISAN OKLUSIF
          </div>
          <div
            style={{position: 'absolute', left: 104, top: ytop + 240, fontFamily: F.sans, fontSize: 25, color: C.muted, opacity: p}}
          >
            kulit
          </div>
          <div
            style={{
              position: 'absolute',
              left: 100,
              top: ytop + 330,
              fontFamily: F.sans,
              fontSize: 28,
              color: C.paper,
              opacity: 0.95 * p,
            }}
          >
            keringat tidak bisa keluar · panas terperangkap
          </div>
        </>
      )}

      <Band top={1200} bottom={1430} a={0.55} feather={110} />
      <Words text="kamu menyebutnya breakout." size={64} top={1244} delay={17.5 * FPS} per={4} />
      <Words text="padahal itu cuaca." size={64} top={1338} color={C.terra} delay={19 * FPS} per={4} />
    </AbsoluteFill>
  );
};

/* ------------------------------------------------------------------ 07 */
export const Scene07: React.FC<{dur: number}> = ({dur}) => {
  const frame = useCurrentFrame();
  const p = ip(frame, [8.5 * FPS, 8.5 * FPS + 54], [0, 1], EASE);
  const p2 = ip(frame, [14 * FPS, 14 * FPS + 30], [0, 1], EASE);
  const gx0 = 140;
  const gx1 = 940;
  const gy0 = 1250;
  const gy1 = 780;

  const pts: string[] = [];
  const n = 60;
  for (let i = 0; i <= n; i++) {
    const u = i / n;
    const x = gx0 + u * (gx1 - gx0);
    const y = gy0 - ((Math.exp(2 * u) - 1) / (Math.exp(2) - 1)) * (gy0 - gy1);
    pts.push(`${x.toFixed(1)},${y.toFixed(1)}`);
  }

  return (
    <AbsoluteFill style={{backgroundColor: C.bg}}>
      <Bg src="images/06-heat-car.jpg" dur={dur} from={1.1} to={1} ty={4} bright={0.72} />
      <Overlay a={0.66} />
      <Vignette strength={0.5} />
      <Label top={228} size={26} tracking={0.22}>
        PANAS · KIMIA
      </Label>
      <Num top={280} size={250} color={C.terra} delay={0.6 * FPS}>
        ×2
      </Num>
      <Words
        text="setiap +10°C, laju reaksi berlipat dua"
        size={40}
        top={636}
        font={F.sans}
        delay={1.6 * FPS}
        per={2.6}
      />

      {p > 0 && (
        <>
          <Svg>
            <line x1={gx0} y1={gy0} x2={gx1 + 20} y2={gy0} stroke={C.paper} strokeWidth={2} opacity={0.4} />
            <line x1={gx0} y1={gy0} x2={gx0} y2={gy1 - 30} stroke={C.paper} strokeWidth={2} opacity={0.4} />
            <polyline
              points={pts.join(' ')}
              fill="none"
              stroke={C.gold}
              strokeWidth={6}
              strokeLinecap="round"
              pathLength={1}
              strokeDasharray={1}
              strokeDashoffset={1 - p}
            />
            {[
              [0.0, '25°'],
              [0.55, '30°'],
              [0.85, '40°'],
            ].map(([u, lab]) => {
              const x = gx0 + (u as number) * (gx1 - gx0);
              return (
                <g key={lab as string} opacity={p > 0.5 ? 1 : 0}>
                  <line x1={x} y1={gy0} x2={x} y2={gy0 + 12} stroke={C.paper} strokeWidth={2} opacity={0.4} />
                  <text
                    x={x - 18}
                    y={gy0 + 44}
                    fill={C.paper}
                    opacity={0.9}
                    fontFamily={F.mono}
                    fontSize={26}
                  >
                    {lab}
                  </text>
                </g>
              );
            })}
          </Svg>
          <div
            style={{
              position: 'absolute',
              left: gx0 - 10,
              top: gy1 - 48,
              fontFamily: F.sans,
              fontSize: 24,
              color: C.muted,
            }}
          >
            laju
          </div>
          <div
            style={{
              position: 'absolute',
              left: 0,
              right: 150,
              top: gy0 - 46,
              textAlign: 'right',
              fontFamily: F.sans,
              fontSize: 24,
              color: C.muted,
            }}
          >
            suhu penyimpanan →
          </div>
        </>
      )}

      {p2 > 0 && (
        <>
          <Svg>
            <rect x={120} y={1400} width={760 * p2} height={4} fill="rgba(255,255,255,0.16)" />
            <rect x={120} y={1500} width={960 * p2} height={4} fill={C.gold} opacity={0.75} />
          </Svg>
          <div
            style={{
              position: 'absolute',
              left: 120,
              top: 1352,
              fontFamily: F.sans,
              fontWeight: 600,
              fontSize: 24,
              letterSpacing: 3,
              color: C.muted,
              opacity: p2,
            }}
          >
            ZONA UJI STABILITAS
          </div>
          <div style={{position: 'absolute', left: 120, top: 1408, opacity: p2}}>
            <span style={{fontFamily: F.sans, fontWeight: 800, fontSize: 28, color: C.paper}}>II&nbsp; EROPA</span>
            <span style={{fontFamily: F.mono, fontWeight: 500, fontSize: 34, color: C.muted, marginLeft: 150}}>
              25°C / 60%
            </span>
          </div>
          <div style={{position: 'absolute', left: 120, top: 1508, opacity: p2}}>
            <span style={{fontFamily: F.sans, fontWeight: 800, fontSize: 28, color: C.gold}}>
              IVb&nbsp; INDONESIA
            </span>
            <span style={{fontFamily: F.mono, fontWeight: 600, fontSize: 34, color: C.paper, marginLeft: 82}}>
              30°C / 75%
            </span>
          </div>
        </>
      )}

      <Words text="di dalam mobil: 40°C+" size={52} top={1682} font={F.sans} weight={800} color={C.terra} delay={24.5 * FPS} per={5} />
    </AbsoluteFill>
  );
};

/* ------------------------------------------------------------------ 08 */
export const Scene08: React.FC<{dur: number}> = ({dur}) => {
  const frame = useCurrentFrame();
  const p = ip(frame, [1.2 * FPS, 1.2 * FPS + 66], [0, 1], EASE);
  const cx = 540;
  const cy = 830;
  const r = 250;
  const arc = (from: number, to: number) => {
    const x0 = cx + r * Math.cos(Math.PI + Math.PI * from);
    const y0 = cy + r * Math.sin(Math.PI + Math.PI * from);
    const x1 = cx + r * Math.cos(Math.PI + Math.PI * to);
    const y1 = cy + r * Math.sin(Math.PI + Math.PI * to);
    const large = to - from > 0.5 ? 1 : 0;
    return `M ${x0} ${y0} A ${r} ${r} 0 ${large} 1 ${x1} ${y1}`;
  };
  const col = p < 0.55 ? C.teal : p < 0.8 ? C.gold : C.terra;
  const p3 = ip(frame, [15.6 * FPS, 15.6 * FPS + 21], [0, 1], EASE);

  return (
    <AbsoluteFill style={{backgroundColor: C.bg}}>
      <Bg src="images/07-uv-sun.jpg" dur={dur} from={1.04} to={1.12} ty={6} bright={0.85} />
      <Scrim top={0.55} bottom={0.82} mid={0.3} />
      <Vignette strength={0.55} />
      <Label top={248} size={26} tracking={0.24}>
        ULTRAVIOLET
      </Label>

      <Svg>
        <path d={arc(0, 1)} fill="none" stroke="rgba(255,255,255,0.16)" strokeWidth={14} strokeLinecap="round" />
        {p > 0 && <path d={arc(0, p)} fill="none" stroke={col} strokeWidth={14} strokeLinecap="round" />}
        <circle cx={cx} cy={cy} r={8} fill={C.paper} opacity={0.35} />
      </Svg>

      <Num top={614} size={206} delay={2.6 * FPS}>
        11
      </Num>
      <Label top={922} color={C.terra} size={38} delay={2.7} tracking={0.28}>
        EXTREME
      </Label>

      <Words text="SPF mengukur UVB." size={58} top={1000} font={F.sans} weight={800} delay={5.2 * FPS} per={4} />
      <Words
        text="UVA yang membuat menua dan bercak."
        size={44}
        top={1086}
        font={F.sans}
        delay={9 * FPS}
        per={3}
      />
      <Words
        text="dan UVA tidak berubah sepanjang tahun."
        size={40}
        top={1176}
        font={F.sans}
        color={C.paper}
        delay={12.5 * FPS}
        per={2.6}
      />

      {p3 > 0 && (
        <>
          <Svg>
            <rect
              x={120}
              y={1300}
              width={840}
              height={200}
              rx={14}
              fill="rgba(201,162,39,0.07)"
              stroke={C.gold}
              strokeWidth={3}
              opacity={p3}
            />
          </Svg>
          <Num top={1332} size={96} color={C.gold} delay={15.6 * FPS}>
            PA++++
          </Num>
          <div
            style={{
              position: 'absolute',
              top: 1466,
              left: 0,
              right: 0,
              textAlign: 'center',
              fontFamily: F.sans,
              fontWeight: 600,
              fontSize: 26,
              letterSpacing: 4,
              color: C.paper,
              opacity: p3,
            }}
          >
            BUKAN KEMEWAHAN — SYARAT MINIMUM
          </div>
        </>
      )}
    </AbsoluteFill>
  );
};

/* ------------------------------------------------------------------ 09 */
const ChangeItem: React.FC<{
  num: string;
  head: string;
  body: string;
  top: number;
  at: number;
}> = ({num, head, body, top, at}) => {
  const frame = useCurrentFrame();
  const a = ip(frame, [at, at + 13], [0, 1]);
  const ty = ip(frame, [at, at + 16], [20, 0]);
  const line = ip(frame, [at, at + 24], [0, 1], EASE);
  return (
    <div style={{position: 'absolute', top, left: 100, right: 120, opacity: a, transform: `translateY(${ty}px)`}}>
      <div style={{display: 'flex', alignItems: 'baseline'}}>
        <span style={{fontFamily: F.mono, fontWeight: 600, fontSize: 62, color: C.gold, width: 110}}>{num}</span>
        <span style={{fontFamily: F.sans, fontWeight: 800, fontSize: 46, letterSpacing: 1, color: C.paper}}>
          {head}
        </span>
      </div>
      <div
        style={{
          marginLeft: 210,
          fontFamily: F.sans,
          fontSize: 34,
          lineHeight: '46px',
          color: C.muted,
          whiteSpace: 'pre-line',
          marginTop: 4,
        }}
      >
        {body}
      </div>
      <div style={{marginTop: 22, marginLeft: 0, height: 2, width: 860 * line, backgroundColor: 'rgba(255,255,255,0.12)'}} />
    </div>
  );
};

export const Scene09: React.FC<{dur: number}> = ({dur}) => (
  <AbsoluteFill style={{backgroundColor: C.bg}}>
    <Bg src="images/08-serum-bottle.jpg" dur={dur} from={1.02} to={1.1} bright={0.78} />
    <Overlay a={0.6} />
    <Vignette strength={0.5} />
    <Label top={228} size={26} tracking={0.22}>
      YANG BERUBAH
    </Label>
    <ChangeItem
      num="01"
      head="TEKSTUR"
      body={'gel · essence · water-break\nbukan krim tebal'}
      top={330}
      at={1.2 * FPS}
    />
    <ChangeItem
      num="02"
      head="URUTAN"
      body={'humektan di kulit lembap\nlalu emolien ringan'}
      top={660}
      at={11 * FPS}
    />
    <ChangeItem
      num="03"
      head="PENYIMPANAN"
      body={'lemari, bukan kamar mandi\nvitamin C: botol gelap, tertutup'}
      top={990}
      at={21 * FPS}
    />
    <Band top={1360} bottom={1560} a={0.5} feather={110} />
    <Words text="oksigen, bukan matahari," size={52} top={1396} delay={27.5 * FPS} per={4} />
    <Words text="yang membunuh vitamin C." size={52} top={1468} color={C.terra} delay={28.4 * FPS} per={4} />
  </AbsoluteFill>
);

/* ------------------------------------------------------------------ 10 */
export const Scene10: React.FC<{dur: number}> = ({dur}) => {
  const frame = useCurrentFrame();
  const src = ip(frame, [6.4 * FPS, 6.4 * FPS + 21], [0, 1]);
  return (
  <AbsoluteFill style={{backgroundColor: C.bg}}>
    <Bg src="images/03-tropical-window.jpg" dur={dur} from={1.06} to={1} bright={0.8} />
    <Overlay a={0.62} />
    <Band top={520} bottom={1020} a={0.72} />
    <Band top={1540} bottom={1760} a={0.6} feather={120} />
    <Vignette strength={0.55} />
    <Words text="KULIT TROPIS." size={96} top={556} delay={0.3 * FPS} letter={1} />
    <Words text="FORMULA TROPIS." size={96} top={676} color={C.terra} delay={1.2 * FPS} letter={1} />
    <Rule y={898} delay={2.4 * FPS} width={620} thickness={3} />
    <Words
      text="kotamu mana?"
      size={64}
      top={952}
      font={F.sans}
      weight={800}
      color={C.gold}
      delay={4.6 * FPS}
      per={4}
    />
    <div
      style={{
        position: 'absolute',
        top: 1616,
        left: 0,
        right: 0,
        textAlign: 'center',
        fontFamily: F.sans,
        fontSize: 26,
        lineHeight: '42px',
        color: C.muted,
        opacity: src,
      }}
    >
      Sumber: WHO TRS 953 · ASEAN Stability Guideline
      <br />
      ICH Q1A(R2) zona iklim · data iklim Jakarta 2026
    </div>
  </AbsoluteFill>
  );
};
