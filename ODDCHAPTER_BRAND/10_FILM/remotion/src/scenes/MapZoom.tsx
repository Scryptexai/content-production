import React from "react";
import {
  AbsoluteFill,
  Img,
  interpolate,
  staticFile,
  useCurrentFrame,
  Easing,
} from "remotion";
import { BRAND_BEZIER, H, W } from "../theme";

/**
 * MAP-ZOOM — shot peta asli dengan zoom-in ke titik kejadian
 * (koreksi pemilik22 Nov2026,00G §1b): zona berdenyut + pin titik kejadian,
 * timing dikunci ke narasi lewat zoneFrame/pointsFrame pada inputProps.
 *
 * Semua posisi dihitung dari bounds geografis (lat/lon → %), sehingga titik
 * muncul TEPAT di lokasi aslinya di peta.
 */

const ease = Easing.bezier(...BRAND_BEZIER);

export type MapZoomProps = {
  /** staticFile path, mis. "maps/ireland_location_map.svg" */
  src: string;
  natural: { w: number; h: number };
  bounds: { n: number; s: number; w: number; e: number };
  target: { lat: number; lon: number };
  fromScale?: number;
  toScale?: number;
  zoomIn?: number;
  zoomOut?: number;
  /** zona highlight (lingkaran oranye berdenyut) — px layar */
  zone?: { lat: number; lon: number; r: number };
  zoneFrame?: number;
  /** pin titik kejadian + label */
  points?: { lat: number; lon: number; label: string }[];
  pointsFrame?: number;
  /** label jarak antar pin (mis. "±3 KM") — muncul pointsFrame + distanceFrame */
  distance?: string;
  distanceFrame?: number;
  headline: string;
  sub?: string;
  credit: string;
  durationInFrames: number;
};

const norm = (b: MapZoomProps["bounds"], lat: number, lon: number) => ({
  x: (lon - b.w) / (b.e - b.w),
  y: (b.n - lat) / (b.n - b.s),
});

const NOISE =
  "data:image/svg+xml;utf8," +
  encodeURIComponent(
    `<svg xmlns="http://www.w3.org/2000/svg" width="160" height="160"><filter id="n"><feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves="2"/></filter><rect width="160" height="160" filter="url(#n)" opacity="0.55"/></svg>`,
  );

export const MapZoom: React.FC<MapZoomProps> = ({
  src,
  natural,
  bounds,
  target,
  fromScale = 1,
  toScale = 5,
  zoomIn = 20,
  zoomOut = 110,
  zone,
  zoneFrame = 120,
  points = [],
  pointsFrame = 125,
  distance,
  distanceFrame = 0,
  headline,
  sub,
  credit,
  durationInFrames,
}) => {
  const frame = useCurrentFrame();
  const dur = Math.max(2, durationInFrames);

  // ── zoom: hold → ease ke toScale → hold (drift halus sepanjang shot)
  const zBase = interpolate(frame, [zoomIn, zoomOut], [fromScale, toScale], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: ease,
  });
  const z = zBase * (1 + (frame / dur) * 0.03);

  const fit = Math.max(W / natural.w, H / natural.h);
  const S = fit * z;
  const t = norm(bounds, target.lat, target.lon);
  const focusX = W / 2;
  const focusY = H / 2 - 40;
  const left = focusX - t.x * natural.w * S;
  const top = focusY - t.y * natural.h * S;

  const screen = (lat: number, lon: number) => {
    const p = norm(bounds, lat, lon);
    return {
      x: focusX + (p.x - t.x) * natural.w * S,
      y: focusY + (p.y - t.y) * natural.h * S,
    };
  };

  const fadeIn = interpolate(frame, [0, 10], [0, 1], {
    extrapolateRight: "clamp",
  });
  const fadeOut = interpolate(frame, [dur - 9, dur - 1], [1, 0], {
    extrapolateLeft: "clamp",
  });
  const opacity = Math.min(fadeIn, fadeOut);

  const zoneIn = interpolate(frame, [zoneFrame, zoneFrame + 14], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const pulse = 1 + 0.05 * Math.sin((frame - zoneFrame) / 7);

  const pts = points.map((p) => ({ ...p, s: screen(p.lat, p.lon) }));
  const distIn = interpolate(
    frame,
    [distanceFrame, distanceFrame + 12],
    [0, 1],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" },
  );

  let line: React.ReactNode = null;
  if (distance && pts.length >= 2) {
    const a = pts[0].s;
    const b = pts[1].s;
    const len = Math.hypot(b.x - a.x, b.y - a.y);
    const ang = (Math.atan2(b.y - a.y, b.x - a.x) * 180) / Math.PI;
    line = (
      <div
        style={{
          position: "absolute",
          left: a.x,
          top: a.y,
          width: len,
          height: 0,
          borderTop: "4px dashed rgba(240,236,224,0.9)",
          transformOrigin: "0 0",
          transform: `rotate(${ang}deg)`,
          opacity: distIn,
        }}
      />
    );
  }

  return (
    <AbsoluteFill style={{ backgroundColor: "#0B0D10", opacity }}>
      {/* peta asli */}
      <Img
        src={staticFile(src)}
        style={{
          position: "absolute",
          left,
          top,
          width: natural.w * S,
          height: natural.h * S,
          filter:
            "grayscale(0.40) contrast(1.14) brightness(0.84) sepia(0.14) saturate(0.95)",
        }}
      />

      {/* vignette + grain */}
      <AbsoluteFill
        style={{
          background:
            "radial-gradient(ellipse at center, rgba(0,0,0,0) 42%, rgba(0,0,0,0.62) 100%)",
        }}
      />
      <AbsoluteFill
        style={{
          backgroundImage: `url("${NOISE}")`,
          opacity: 0.05,
          mixBlendMode: "overlay",
        }}
      />
      {/* scrim atas agar headline terbaca */}
      <div
        style={{
          position: "absolute",
          left: 0,
          top: 0,
          width: W,
          height: 380,
          background:
            "linear-gradient(180deg, rgba(11,13,16,0.88) 0%, rgba(11,13,16,0.55) 55%, rgba(11,13,16,0) 100%)",
        }}
      />

      {/* zona berdenyut */}
      {zone && zoneIn > 0 && (
        <div
          style={{
            position: "absolute",
            left: screen(zone.lat, zone.lon).x - zone.r,
            top: screen(zone.lat, zone.lon).y - zone.r,
            width: zone.r * 2,
            height: zone.r * 2,
            borderRadius: "50%",
            border: "4px solid #E8813D",
            background: "rgba(232,129,61,0.13)",
            boxShadow: "0 0 28px rgba(232,129,61,0.45)",
            opacity: zoneIn,
            transform: `scale(${pulse})`,
          }}
        />
      )}

      {/* garis jarak + pin */}
      {line}
      {pts.map((p, i) => {
        const pinIn = interpolate(
          frame,
          [pointsFrame + i * 8, pointsFrame + i * 8 + 14],
          [0, 1],
          { extrapolateLeft: "clamp", extrapolateRight: "clamp" },
        );
        return (
          <div key={p.label} style={{ opacity: pinIn }}>
            <div
              style={{
                position: "absolute",
                left: p.s.x - 11,
                top: p.s.y - 11,
                width: 22,
                height: 22,
                borderRadius: "50%",
                background: "#D82A2A",
                border: "4px solid #F0ECE0",
                boxShadow: "0 0 18px rgba(216,42,42,0.8)",
                transform: `translateY(${(1 - pinIn) * -34}px)`,
              }}
            />
            <div
              style={{
                position: "absolute",
                // pin di sisi kanan layar → label flip ke kiri (jangan kepotong)
                left: p.s.x > W * 0.58 ? p.s.x - 20 : p.s.x + 20,
                // pin kedua (mis. ujung danau) → label di BAWAH pin supaya
                // tidak menimpa label pin pertama (jarak pendek ±3 km)
                top:
                  p.s.y +
                  (i === 1
                    ? 34
                    : pts.length > 1 && i === 0
                      ? -78
                      : -46),
                padding: "10px 16px",
                background: "rgba(11,13,16,0.92)",
                border: "1px solid rgba(240,236,224,0.28)",
                color: "#F0ECE0",
                fontFamily: "Inter, sans-serif",
                fontWeight: 600,
                fontSize: 27,
                letterSpacing: "0.06em",
                whiteSpace: "nowrap",
                transform:
                  (p.s.x > W * 0.58 ? "translateX(-100%) " : "") +
                  `translateY(${(1 - pinIn) * -34}px)`,
              }}
            >
              {p.label}
            </div>
          </div>
        );
      })}

      {/* label jarak */}
      {distance && pts.length >= 2 && distIn > 0 && (
        <div
          style={{
            position: "absolute",
            left: (pts[0].s.x + pts[1].s.x) / 2,
            top: (pts[0].s.y + pts[1].s.y) / 2 - 132,
            transform: "translateX(-50%)",
            padding: "8px 14px",
            background: "#E8813D",
            color: "#0B0D10",
            fontFamily: "Inter, sans-serif",
            fontWeight: 600,
            fontSize: 30,
            letterSpacing: "0.08em",
            opacity: distIn,
          }}
        >
          {distance}
        </div>
      )}

      {/* headline */}
      <div
        style={{
          position: "absolute",
          left: 64,
          top: 120,
          width: W - 128,
          opacity: interpolate(frame, [8, 24], [0, 1], {
            extrapolateLeft: "clamp",
            extrapolateRight: "clamp",
          }),
        }}
      >
        <div
          style={{
            fontFamily: "Space Grotesk, Inter, sans-serif",
            fontWeight: 700,
            fontSize: 64,
            letterSpacing: "0.04em",
            color: "#F0ECE0",
            textTransform: "uppercase",
            lineHeight: 1.08,
          }}
        >
          {headline}
        </div>
        {sub && (
          <div
            style={{
              marginTop: 14,
              fontFamily: "Inter, sans-serif",
              fontWeight: 500,
              fontSize: 33,
              letterSpacing: "0.14em",
              color: "#E8813D",
              textTransform: "uppercase",
            }}
          >
            {sub}
          </div>
        )}
      </div>

      {/* watermark + kredit peta */}
      <div
        style={{
          position: "absolute",
          right: 56,
          top: 48,
          fontFamily: "Inter, sans-serif",
          fontWeight: 600,
          fontSize: 22,
          letterSpacing: "0.34em",
          color: "rgba(240,236,224,0.55)",
        }}
      >
        ODDCHAPTER
      </div>
      <div
        style={{
          position: "absolute",
          left: 56,
          bottom: 56,
          fontFamily: "Inter, sans-serif",
          fontWeight: 500,
          fontSize: 23,
          letterSpacing: "0.06em",
          color: "rgba(240,236,224,0.72)",
          textShadow: "0 1px 8px rgba(0,0,0,0.9)",
        }}
      >
        {credit}
      </div>
    </AbsoluteFill>
  );
};
