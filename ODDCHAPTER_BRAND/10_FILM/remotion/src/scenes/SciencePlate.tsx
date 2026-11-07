import React, { useMemo } from "react";
import { AbsoluteFill, Easing, interpolate, useCurrentFrame } from "remotion";
import * as d3 from "d3";
import { BRAND_BEZIER, C, MARGIN } from "../theme";

/**
 * The explanatory beat: a stratified lake, gas held in solution at depth, and a
 * degassing pipe. Every number here is a *shape*, not a measurement — the plate
 * is labelled as a mechanism illustration so it cannot be read as a reconstruction
 * of a specific event. Geometry is generated with d3 (scales + curve), animated
 * frame by frame.
 */

const ease = Easing.bezier(...BRAND_BEZIER);

const X0 = 100;
const X1 = 980;
const SURFACE = 760;
const BOTTOM = 1320;

/** Deterministic PRNG so every render of frame N is identical. */
const mulberry32 = (seed: number) => () => {
  seed |= 0;
  seed = (seed + 0x6d2b79f5) | 0;
  let t = Math.imul(seed ^ (seed >>> 15), 1 | seed);
  t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
  return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
};

const useDiagram = () => {
  return useMemo(() => {
    const rnd = mulberry32(19860421);

    // bathymetry: a steep-sided basin, flat-ish floor
    const profile = [
      [X0, SURFACE - 40],
      [X0 + 10, SURFACE + 120],
      [X0 + 70, 1010],
      [X0 + 190, 1150],
      [X0 + 330, 1225],
      [540, BOTTOM],
      [X1 - 330, 1225],
      [X1 - 190, 1150],
      [X1 - 70, 1010],
      [X1 - 10, SURFACE + 120],
      [X1, SURFACE - 40],
    ] as [number, number][];

    const line = d3.line().curve(d3.curveBasis);
    const basin = `${line(profile)!} L ${X1} ${SURFACE} L ${X0} ${SURFACE} Z`;

    // gas held in solution: denser and heavier near the floor
    const dots = d3.range(64).map((i) => {
      const depthT = Math.pow(rnd(), 0.55); // 0 top → 1 bottom
      const y = SURFACE + 120 + depthT * (BOTTOM - SURFACE - 190);
      const inset = 70 + (1 - depthT) * 190;
      const x = X0 + inset + rnd() * (X1 - X0 - inset * 2);
      return { x, y, r: 3.4 + rnd() * 3.2, order: i / 64 };
    });

    // gas leaving the pipe, above the water line
    const plume = d3.range(26).map(() => ({
      dx: (rnd() - 0.5) * 150,
      delay: rnd() * 0.6,
      r: 5 + rnd() * 12,
      drift: (rnd() - 0.5) * 60,
    }));

    const scaleDepth = d3
      .scaleLinear()
      .domain([0, 1])
      .range([SURFACE + 120, BOTTOM - 40]);

    return { basin, dots, plume, scaleDepth };
  }, []);
};

export const SciencePlate: React.FC = () => {
  const frame = useCurrentFrame();
  const { basin, dots, plume } = useDiagram();

  const head = interpolate(frame, [4, 20], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: ease,
  });
  const outline = interpolate(frame, [16, 46], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: ease,
  });
  const strata = interpolate(frame, [40, 70], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const gas = interpolate(frame, [64, 170], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: ease,
  });
  const pipe = interpolate(frame, [70, 160], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: ease,
  });
  const vent = interpolate(frame, [150, 200], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  const pipeX = 604;
  const pipeTop = SURFACE - 40;
  const pipeBottom = BOTTOM - 14;
  const pipeHeight = (pipeBottom - pipeTop) * pipe;

  const label = (x: number, y: number, text: string, align: "start" | "end" = "start") => (
    <text
      x={x}
      y={y}
      fill={C.sage}
      fontFamily="Inter"
      fontWeight={500}
      fontSize={23}
      letterSpacing="0.06em"
      textAnchor={align}
      opacity={0.9}
    >
      {text}
    </text>
  );

  return (
    <AbsoluteFill style={{ backgroundColor: C.ink }}>
      <div
        style={{
          position: "absolute",
          left: MARGIN,
          top: 430,
          opacity: head,
          transform: `translateY(${(1 - head) * 18}px)`,
        }}
      >
        <div
          style={{
            fontFamily: "Inter",
            fontWeight: 600,
            fontSize: 26,
            letterSpacing: "0.28em",
            color: C.sage,
          }}
        >
          DIAGRAM MEKANISME
        </div>
        <div
          style={{
            marginTop: 26,
            fontFamily: "Space Grotesk",
            fontWeight: 700,
            fontSize: 62,
            letterSpacing: "0.005em",
            color: C.ivory,
          }}
        >
          DANAU BERSTRATIF
        </div>
      </div>

      <svg width={1080} height={1920} style={{ position: "absolute", inset: 0 }}>
        <defs>
          <clipPath id="basin">
            <path d={basin} />
          </clipPath>
        </defs>

        {/* water body */}
        <path
          d={basin}
          fill="rgba(167,176,161,0.055)"
          stroke={`rgba(167,176,161,${0.5 * outline})`}
          strokeWidth={2}
          strokeDasharray={2600}
          strokeDashoffset={2600 * (1 - outline)}
        />

        {/* stratification lines, clipped to the water body */}
        <g clipPath="url(#basin)" opacity={strata}>
          {[920, 1070, 1220].map((y) => (
            <line
              key={y}
              x1={X0 - 10}
              x2={X1 + 10}
              y1={y}
              y2={y}
              stroke="rgba(167,176,161,0.34)"
              strokeWidth={1.5}
              strokeDasharray="7 9"
            />
          ))}
        </g>

        {/* surface */}
        <line
          x1={X0 - 24}
          x2={X1 + 24}
          y1={SURFACE}
          y2={SURFACE}
          stroke={C.ivory}
          strokeOpacity={0.55 * outline}
          strokeWidth={2}
        />

        {/* gas in solution */}
        <g clipPath="url(#basin)">
          {dots.map((d, i) => {
            const on = interpolate(gas, [d.order * 0.8, d.order * 0.8 + 0.2], [0, 1], {
              extrapolateLeft: "clamp",
              extrapolateRight: "clamp",
            });
            const bob = Math.sin((frame / 18 + i) * 1.7) * 1.6;
            return (
              <circle
                key={i}
                cx={d.x}
                cy={d.y + bob}
                r={d.r}
                fill={C.ivory}
                opacity={on * 0.5}
              />
            );
          })}
        </g>

        {/* degassing pipe */}
        {pipe > 0 && (
          <>
            <rect
              x={pipeX - 7}
              y={pipeBottom - pipeHeight}
              width={14}
              height={pipeHeight}
              fill={C.orange}
            />
            <rect
              x={pipeX - 7}
              y={pipeBottom - pipeHeight}
              width={14}
              height={Math.min(16, pipeHeight)}
              fill={C.ivory}
              opacity={0.9 * vent}
            />
          </>
        )}

        {/* venting gas above the surface */}
        {vent > 0 &&
          plume.map((p, i) => {
            const t = interpolate(
              vent,
              [p.delay * 0.4, Math.min(1, p.delay * 0.4 + 0.6)],
              [0, 1],
              { extrapolateLeft: "clamp", extrapolateRight: "clamp" },
            );
            const y = pipeTop - t * 130;
            return (
              <circle
                key={i}
                cx={pipeX + p.dx * (0.4 + t * 0.9) + p.drift * t}
                cy={y}
                r={p.r * (0.6 + t * 0.9)}
                fill={C.ivory}
                opacity={(1 - t) * 0.55 * vent}
              />
            );
          })}

        {/* leaders + labels */}
        <g opacity={gas}>
          <line x1={196} x2={330} y1={1252} y2={1292} stroke={C.sage} strokeOpacity={0.5} strokeWidth={1.5} />
          {label(196, 1300, "gas terlarut di dasar")}
        </g>
        <g opacity={pipe}>
          <line x1={612} x2={690} y1={1298} y2={1318} stroke={C.sage} strokeOpacity={0.5} strokeWidth={1.5} />
          {label(694, 1338, "pipa degassing")}
        </g>
        <g opacity={strata}>
          {label(X0 - 24, SURFACE - 26, "permukaan", "start")}
        </g>
      </svg>

      {/* disclosure, kept next to the title: this plate explains a mechanism,
          it does not reconstruct an event. */}
      <div
        style={{
          position: "absolute",
          left: MARGIN,
          right: MARGIN,
          top: 560,
          fontFamily: "Inter",
          fontWeight: 500,
          fontSize: 23,
          lineHeight: 1.45,
          letterSpacing: "0.02em",
          color: C.sage,
          opacity: 0.82 * head,
        }}
      >
        Ilustrasi mekanisme, bukan rekonstruksi peristiwa. Skala dan angka tidak
        ditampilkan karena tidak ada sumber yang dikutip pada tayangan ini.
      </div>
    </AbsoluteFill>
  );
};
