import React from "react";
import {
  AbsoluteFill,
  Audio,
  Img,
  OffthreadVideo,
  Sequence,
  interpolate,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
  Easing,
} from "remotion";
import { useFonts } from "./fonts";
import { ACCENTS, CREAM, MUTED, ROSE, SAGE, LILAC } from "./palette";

/* ------------------------------------------------------------------ tipe */

export type Beat = {
  key: string;
  block: string;
  kind:
    | "stat"
    | "pair"
    | "line"
    | "word"
    | "quote"
    | "chips"
    | "bars"
    | "split"
    | "grid30"
    | "list"
    | "question";
  plate: string;
  plateFrom: number;
  light?: boolean;
  shot?: string;
  accent: keyof typeof ACCENTS | "cream";
  kicker?: string;
  big?: string;
  mid?: string;
  sub?: string[];
  who?: string;
  chips?: string[];
  items?: string[];
  pairs?: [string, string][];
  bars?: [string, number, string, string][];
  before?: string;
  after?: string;
  labelBefore?: string;
  labelAfter?: string;
  from: number;
  to: number;
};

export type Block = {
  key: string;
  vo: string;
  from: number;
  to: number;
};

export type LongProps = {
  id: string;
  tone: string;
  chapter: string;
  source: string;
  preview: boolean;
  blocks: Block[];
  beats: Beat[];
};

/* ------------------------------------------------------------------ dasar */

const EASE = Easing.bezier(0.16, 1, 0.3, 1);
const X = 132;
const TOP = 108;
const BOTTOM = 96;

type Accent = keyof typeof ACCENTS | "cream";

type Skin = {
  text: string;
  soft: string;
  muted: string;
  rose: string;
  sage: string;
  hair: string;
};

const DARK_SKIN: Skin = {
  text: CREAM,
  soft: "rgba(239,231,220,0.90)",
  muted: MUTED,
  rose: ROSE,
  sage: SAGE,
  hair: "rgba(239,231,220,0.26)",
};

const LIGHT_SKIN: Skin = {
  text: "#141821",
  soft: "rgba(20,24,33,0.86)",
  muted: "rgba(20,24,33,0.52)",
  rose: "#A85B3E",
  sage: "#4A6647",
  hair: "rgba(20,24,33,0.24)",
};

const skinOf = (light?: boolean) => (light ? LIGHT_SKIN : DARK_SKIN);
const accentOf = (a: Accent, s: Skin) => (a === "cream" ? s.text : a === "rose" ? s.rose : a === "sage" ? s.sage : LILAC);

/** masuk: naik + pudar, bertahap antar elemen */
const enter = (f: number, delay: number, dist = 26) => ({
  opacity: interpolate(f - delay, [0, 11], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: EASE,
  }),
  transform: `translateY(${interpolate(f - delay, [0, 16], [dist, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: EASE,
  })}px)`,
});

const Kicker: React.FC<{ text: string; accent: string; muted: string }> = ({ text, accent, muted }) => (
  <div style={{ display: "flex", alignItems: "center", gap: 16, marginBottom: 30 }}>
    <div style={{ width: 26, height: 4, background: accent, borderRadius: 2 }} />
    <div
      style={{
        fontFamily: "Plex Mono",
        fontSize: 25,
        letterSpacing: "0.30em",
        color: muted,
        textTransform: "uppercase",
      }}
    >
      {text}
    </div>
  </div>
);

/* ------------------------------------------------------------------ adegan */

const Scene: React.FC<{ b: Beat; s: Skin }> = ({ b, s }) => {
  const f = useCurrentFrame();
  const accent = accentOf(b.accent, s);

  if (b.kind === "stat" || b.kind === "pair") {
    const rows = b.pairs
      ? b.pairs.map(([v, l]) => ({ v, l }))
      : [{ v: b.big ?? "", l: b.mid ?? "" }];
    const biggest = rows.length > 1;
    return (
      <div>
        {b.kicker ? (
          <div style={enter(f, 0)}>
            <Kicker text={b.kicker} accent={accent} muted={s.muted} />
          </div>
        ) : null}
        {rows.map((r, i) => (
          <div key={r.l} style={{ ...enter(f, 4 + i * 6), marginBottom: biggest ? 26 : 10 }}>
            <div
              style={{
                fontFamily: "Plex Mono",
                fontSize: biggest ? 210 : 300,
                fontWeight: 500,
                lineHeight: biggest ? 0.98 : 0.9,
                letterSpacing: "-0.045em",
                color: i === 0 ? accent : s.text,
                fontVariantNumeric: "tabular-nums",
              }}
            >
              {r.v}
            </div>
            <div
              style={{
                fontFamily: "Instrument Serif",
                fontSize: biggest ? 44 : 48,
                color: s.text,
                opacity: 0.92,
                marginTop: 6,
              }}
            >
              {r.l}
            </div>
          </div>
        ))}
        {b.sub?.length ? (
          <div style={{ ...enter(f, 20, 16), marginTop: 34 }}>
            {b.sub.map((line) => (
              <div
                key={line}
                style={{
                  fontFamily: "Plex Mono",
                  fontSize: 28,
                  letterSpacing: "0.05em",
                  color: s.muted,
                }}
              >
                {line}
              </div>
            ))}
          </div>
        ) : null}
      </div>
    );
  }

  if (b.kind === "word") {
    return (
      <div style={{ ...enter(f, 0, 40) }}>
        <div
          style={{
            fontFamily: "Instrument Serif",
            fontSize: 240,
            lineHeight: 0.94,
            letterSpacing: "-0.03em",
            color: accent,
            maxWidth: 1500,
          }}
        >
          {b.big}
        </div>
      </div>
    );
  }

  if (b.kind === "quote") {
    return (
      <div style={{ maxWidth: 1450 }}>
        <div style={enter(f, 0, 34)}>
          <div
            style={{
              fontFamily: "Instrument Serif",
              fontStyle: "italic",
              fontSize: 96,
              lineHeight: 1.16,
              color: s.text,
              letterSpacing: "-0.01em",
            }}
          >
            “{b.big}”
          </div>
        </div>
        {b.who ? (
          <div
            style={{
              ...enter(f, 14, 18),
              marginTop: 40,
              display: "flex",
              alignItems: "center",
              gap: 18,
            }}
          >
            <div style={{ width: 74, height: 3, background: accent }} />
            <div
              style={{
                fontFamily: "Plex Mono",
                fontSize: 28,
                letterSpacing: "0.06em",
                color: s.muted,
              }}
            >
              {b.who}
            </div>
          </div>
        ) : null}
      </div>
    );
  }

  if (b.kind === "question") {
    return (
      <div style={{ maxWidth: 1420 }}>
        <div style={enter(f, 0, 36)}>
          <div
            style={{
              fontFamily: "Instrument Serif",
              fontSize: 140,
              lineHeight: 1.06,
              letterSpacing: "-0.025em",
              color: s.text,
            }}
          >
            {b.big}
          </div>
        </div>
        <div style={{ ...enter(f, 14, 18), marginTop: 46 }}>
          <div style={{ width: 210, height: 5, background: accent, borderRadius: 3 }} />
        </div>
      </div>
    );
  }

  if (b.kind === "chips") {
    return (
      <div>
        <div style={{ display: "flex", gap: 18, flexWrap: "wrap", maxWidth: 1400 }}>
          {(b.chips ?? []).map((c, i) => (
            <div
              key={c}
              style={{
                ...enter(f, 2 + i * 5, 18),
                fontFamily: "Plex Mono",
                fontSize: 34,
                letterSpacing: "0.04em",
                color: s.text,
                border: `1.5px solid ${s.hair}`,
                borderRadius: 999,
                padding: "18px 34px",
              }}
            >
              {c}
            </div>
          ))}
        </div>
      </div>
    );
  }

  if (b.kind === "list") {
    return (
      <div style={{ maxWidth: 1400 }}>
        {b.kicker ? (
          <div style={enter(f, 0)}>
            <Kicker text={b.kicker} accent={accent} muted={s.muted} />
          </div>
        ) : null}
        {(b.items ?? []).map((it, i) => (
          <div
            key={it}
            style={{
              ...enter(f, 6 + i * 7, 22),
              display: "flex",
              gap: 26,
              alignItems: "baseline",
              marginBottom: 30,
            }}
          >
            <div
              style={{
                fontFamily: "Plex Mono",
                fontSize: 30,
                color: accent,
                minWidth: 52,
              }}
            >
              0{i + 1}
            </div>
            <div
              style={{
                fontFamily: "Instrument Serif",
                fontSize: 72,
                lineHeight: 1.1,
                color: s.text,
              }}
            >
              {it}
            </div>
          </div>
        ))}
      </div>
    );
  }

  if (b.kind === "bars") {
    const bars = b.bars ?? [];
    return (
      <div style={{ maxWidth: 1350 }}>
        {b.kicker ? (
          <div style={enter(f, 0)}>
            <Kicker text={b.kicker} accent={accent} muted={s.muted} />
          </div>
        ) : null}
        {bars.map(([label, value, display, ac], i) => {
          const w = interpolate(f - 4 - i * 5, [0, 18], [0, Math.min(100, value * 5.6)], {
            extrapolateLeft: "clamp",
            extrapolateRight: "clamp",
            easing: EASE,
          });
          return (
            <div key={label} style={{ ...enter(f, 4 + i * 5, 18), marginBottom: 34 }}>
              <div
                style={{
                  display: "flex",
                  justifyContent: "space-between",
                  alignItems: "baseline",
                  marginBottom: 12,
                }}
              >
                <span
                  style={{ fontFamily: "Plex Mono", fontSize: 31, color: s.text, letterSpacing: "0.04em" }}
                >
                  {label}
                </span>
                <span
                  style={{
                    fontFamily: "Plex Mono",
                    fontSize: 62,
                    fontWeight: 500,
                    color: ac === "sage" ? s.sage : s.rose,
                    letterSpacing: "-0.02em",
                  }}
                >
                  {display}
                </span>
              </div>
              <div style={{ height: 14, background: s.hair, borderRadius: 7 }}>
                <div
                  style={{
                    width: `${w}%`,
                    height: "100%",
                    borderRadius: 7,
                    background: ac === "sage" ? s.sage : s.rose,
                  }}
                />
              </div>
            </div>
          );
        })}
        {b.sub?.length ? (
          <div style={{ ...enter(f, 18, 14), marginTop: 26 }}>
            {b.sub.map((line) => (
              <div key={line} style={{ fontFamily: "Plex Mono", fontSize: 28, color: s.muted }}>
                {line}
              </div>
            ))}
          </div>
        ) : null}
      </div>
    );
  }

  if (b.kind === "split") {
    const box = (label?: string, value?: string, delay = 0, accentBox = false) => (
      <div style={{ ...enter(f, delay, 22), flex: 1 }}>
        <div
          style={{
            fontFamily: "Plex Mono",
            fontSize: 25,
            letterSpacing: "0.16em",
            color: s.muted,
            textTransform: "uppercase",
            marginBottom: 14,
          }}
        >
          {label}
        </div>
        <div
          style={{
            border: `1.5px solid ${accentBox ? accent : s.hair}`,
            borderRadius: 10,
            padding: "34px 36px",
            background: accentBox ? "rgba(217,142,115,0.10)" : "transparent",
          }}
        >
          <div style={{ fontFamily: "Instrument Serif", fontSize: 62, color: CREAM }}>
            {value}
          </div>
        </div>
      </div>
    );
    return (
      <div style={{ maxWidth: 1420 }}>
        <div style={{ display: "flex", alignItems: "flex-end", gap: 30 }}>
          {box(b.labelBefore, b.before, 0, false)}
          <div style={{ ...enter(f, 8, 0), paddingBottom: 56 }}>
            <div style={{ fontFamily: "Plex Mono", fontSize: 56, color: s.rose }}>→</div>
          </div>
          {box(b.labelAfter, b.after, 4, true)}
        </div>
        {b.sub?.length ? (
          <div style={{ ...enter(f, 18, 14), marginTop: 40 }}>
            {b.sub.map((line) => (
              <div key={line} style={{ fontFamily: "Plex Mono", fontSize: 30, color: s.muted }}>
                {line}
              </div>
            ))}
          </div>
        ) : null}
      </div>
    );
  }

  if (b.kind === "grid30") {
    const cells = Array.from({ length: 100 }, (_, i) => i);
    return (
      <div style={{ display: "flex", alignItems: "center", gap: 84 }}>
        <div style={{ display: "grid", gridTemplateColumns: "repeat(10, 44px)", gap: 9 }}>
          {cells.map((i) => {
            const on = i < 30;
            const appear = interpolate(f, [2 + i * 0.22, 8 + i * 0.22], [0, 1], {
              extrapolateLeft: "clamp",
              extrapolateRight: "clamp",
            });
            return (
              <div
                key={i}
                style={{
                  width: 44,
                  height: 44,
                  borderRadius: 4,
                  background: on ? s.sage : s.hair,
                  opacity: appear,
                }}
              />
            );
          })}
        </div>
        <div>
          <div
            style={{
              ...enter(f, 8, 26),
              fontFamily: "Plex Mono",
              fontSize: 210,
              fontWeight: 500,
              letterSpacing: "-0.05em",
              color: s.sage,
              lineHeight: 0.9,
            }}
          >
            {b.big}
          </div>
          <div
            style={{
              ...enter(f, 16, 18),
              fontFamily: "Instrument Serif",
              fontSize: 52,
              color: s.text,
              marginTop: 12,
            }}
          >
            {b.mid}
          </div>
        </div>
      </div>
    );
  }

  // line (default)
  const long = (b.big ?? "").length > 34;
  return (
    <div style={{ maxWidth: 1330 }}>
      {b.kicker ? (
        <div style={enter(f, 0)}>
          <Kicker text={b.kicker} accent={accent} muted={s.muted} />
        </div>
      ) : null}
      <div style={{ ...enter(f, b.kicker ? 4 : 0, 30) }}>
        <div
          style={{
            fontFamily: "Instrument Serif",
            fontSize: long ? 112 : 138,
            lineHeight: 1.08,
            letterSpacing: "-0.022em",
            color: s.text,
          }}
        >
          {b.big}
        </div>
      </div>
      {b.sub?.length ? (
        <div style={{ ...enter(f, 12, 18), marginTop: 32 }}>
          {b.sub.map((line) => (
            <div
              key={line}
              style={{
                fontFamily: "Plex Mono",
                fontSize: 33,
                color: b.accent === "rose" ? s.rose : s.sage,
                letterSpacing: "0.03em",
                marginTop: 6,
              }}
            >
              {line}
            </div>
          ))}
        </div>
      ) : null}
    </div>
  );
};

/* ------------------------------------------------------------------ latar */

const Plate: React.FC<{ b: Beat; duration: number }> = ({ b, duration }) => {
  const f = useCurrentFrame();
  const zoom = interpolate(f, [0, duration], [1.055, 1.0], {
    extrapolateRight: "clamp",
  });
  return (
    <AbsoluteFill style={{ overflow: "hidden" }}>
      <OffthreadVideo
        src={staticFile(`backdrop/plate-${b.plate}.mp4`)}
        startFrom={b.plateFrom}
        muted
        style={{
          width: "100%",
          height: "100%",
          objectFit: "cover",
          transform: `scale(${zoom})`,
        }}
      />
      {/* jaminan keterbacaan: gelapkan sisi teks */}
      <AbsoluteFill
        style={{
          background: b.light
            ? "linear-gradient(100deg, rgba(239,231,220,0.97) 0%, rgba(239,231,220,0.90) 46%, rgba(239,231,220,0.35) 100%)"
            : "linear-gradient(100deg, rgba(8,11,18,0.90) 0%, rgba(8,11,18,0.62) 52%, rgba(8,11,18,0.10) 100%)",
        }}
      />
    </AbsoluteFill>
  );
};

/* ------------------------------------------------------------------ footage */

/**
 * Foto sebagai footage: zoom + pan pelan selama beat berjalan, jadi tidak
 * terasa seperti gambar diam. Gerakannya sengaja sangat kecil (2-8%) supaya
 * mata membaca teks, bukan menonton gerakan.
 */
const Footage: React.FC<{ shot: string; duration: number; index: number }> = ({
  shot,
  duration,
  index,
}) => {
  const f = useCurrentFrame();
  const p = interpolate(f, [0, duration], [0, 1], { extrapolateRight: "clamp" });
  // arah gerak berganti tiap beat supaya tidak monoton
  const dir = index % 4;
  const scale = 1.06 + p * (dir % 2 === 0 ? 0.07 : -0.045);
  const tx = (dir === 0 ? -1 : dir === 1 ? 1 : dir === 2 ? -0.6 : 0.6) * p * 26;
  const ty = (dir < 2 ? -1 : 1) * p * 18;
  const fade = interpolate(f, [0, 7], [0, 1], { extrapolateRight: "clamp" });

  return (
    <AbsoluteFill style={{ overflow: "hidden", backgroundColor: "#0A0D14" }}>
      <Img
        src={staticFile(`footage/${shot}.jpg`)}
        style={{
          width: "100%",
          height: "100%",
          objectFit: "cover",
          opacity: fade,
          transform: `scale(${scale}) translate(${tx}px, ${ty}px)`,
        }}
      />
      {/* scrim: gelap di kiri tempat teks, foto tetap terbaca di kanan */}
      <AbsoluteFill
        style={{
          background:
            "linear-gradient(97deg, rgba(8,11,18,0.95) 0%, rgba(8,11,18,0.88) 30%, rgba(8,11,18,0.55) 58%, rgba(8,11,18,0.18) 100%)",
        }}
      />
    </AbsoluteFill>
  );
};

/* ------------------------------------------------------------------ aside */

const Aside: React.FC<{
  block: string;
  index: number;
  total: number;
  accent: string;
  s: Skin;
}> = ({ block, index, total, accent, s }) => {
  const f = useCurrentFrame();
  const o = interpolate(f, [6, 20], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  return (
    <div style={{ position: "absolute", right: 0, top: 0, bottom: 0, width: 250, opacity: o }}>
      {/* garis vertikal tipis + label diputar */}
      <div
        style={{
          position: "absolute",
          right: 96,
          top: 120,
          bottom: 140,
          width: 1,
          background: s.hair,
        }}
      />
      <div
        style={{
          position: "absolute",
          right: 52,
          top: "50%",
          transform: "translateY(-50%) rotate(90deg)",
          transformOrigin: "center",
          fontFamily: "Plex Mono",
          fontSize: 20,
          letterSpacing: "0.42em",
          color: s.muted,
          whiteSpace: "nowrap",
        }}
      >
        BAB {block.toUpperCase()}
      </div>
      {/* nomor besar samar */}
      <div
        style={{
          position: "absolute",
          right: 96,
          bottom: 92,
          fontFamily: "Plex Mono",
          fontSize: 150,
          fontWeight: 500,
          letterSpacing: "-0.06em",
          color: accent,
          opacity: 0.09,
          lineHeight: 0.8,
        }}
      >
        {String(index).padStart(2, "0")}
      </div>
      <div
        style={{
          position: "absolute",
          right: 96,
          bottom: 66,
          fontFamily: "Plex Mono",
          fontSize: 17,
          letterSpacing: "0.2em",
          color: MUTED,
          opacity: 0.6,
        }}
      >
        /{String(total).padStart(2, "0")}
      </div>
    </div>
  );
};

/* ------------------------------------------------------------------ kerangka */

export const LongForm: React.FC<LongProps> = ({ source, preview, blocks, beats }) => {
  const ready = useFonts();
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const total = blocks.length ? blocks[blocks.length - 1].to : 1;

  if (!ready) return <AbsoluteFill style={{ backgroundColor: "#0A0D14" }} />;

  const active = beats.find((b) => frame >= b.from && frame < b.to) ?? beats[0];
  const dur = active.to - active.from;
  const local = frame - active.from;
  const skin = skinOf(active.light);

  // kilat krem 3 frame di awal tiap bab: penanda potong, bukan transisi lambat
  const blockStart = blocks.find((b) => b.key === active.block)?.from ?? -999;
  const flash = interpolate(frame - blockStart, [0, 3, 7], [0.55, 0.35, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  const showSource = frame - blockStart < fps * 4.5;

  return (
    <AbsoluteFill style={{ backgroundColor: "#0A0D14" }}>
      {/* latar per beat */}
      <Sequence key={`pl-${active.key}`} from={active.from} durationInFrames={dur}>
        {active.shot ? (
          <Footage shot={active.shot} duration={dur} index={beats.indexOf(active)} />
        ) : (
          <Plate b={active} duration={dur} />
        )}
      </Sequence>

      {/* narasi: satu klip per blok, tanpa dipotong */}
      {!preview &&
        blocks.map((b, i) => (
          <Sequence key={i} from={b.from} durationInFrames={b.to - b.from}>
            <Audio src={staticFile(`audio/${b.vo}`)} />
          </Sequence>
        ))}

      {/* isi beat */}
      <Sequence key={active.key} from={active.from} durationInFrames={dur}>
        <AbsoluteFill style={{ padding: `${TOP}px ${X}px ${BOTTOM}px ${X}px`, justifyContent: "center" }}>
          <div
            style={{
              transform: `scale(${interpolate(local, [0, dur], [1.012, 1.0], {
                extrapolateRight: "clamp",
              })})`,
              transformOrigin: "left center",
            }}
          >
            <Scene b={active} s={skin} />
          </div>
        </AbsoluteFill>
      </Sequence>

      <Aside
        block={active.block}
        index={blocks.findIndex((b) => b.key === active.block) + 1}
        total={blocks.length}
        accent={accentOf(active.accent, skin)}
        s={skin}
      />

      {/* kilat potong */}
      <AbsoluteFill style={{ background: skin.text, opacity: flash * 0.5, pointerEvents: "none" }} />

      {/* identitas: kecil, di sudut */}
      <div
        style={{
          position: "absolute",
          left: X,
          top: 46,
          display: "flex",
          alignItems: "center",
          gap: 12,
          opacity: 0.62,
        }}
      >
        <Img src={staticFile("logo-mark.png")} style={{ width: 26, height: 26 }} />
        <span
          style={{
            fontFamily: "Plex Mono",
            fontSize: 20,
            letterSpacing: "0.34em",
            color: skin.text,
          }}
        >
          KNOT THEORY
        </span>
      </div>

      {/* sumber: muncul sebentar di awal tiap bab */}
      <div
        style={{
          position: "absolute",
          left: X,
          bottom: 54,
          opacity: interpolate(showSource ? 1 : 0, [0, 1], [0, 0.55]),
        }}
      >
        <span style={{ fontFamily: "Plex Mono", fontSize: 21, letterSpacing: "0.06em", color: skin.muted }}>
          {source}
        </span>
      </div>

      {/* progres tipis */}
      <div style={{ position: "absolute", left: 0, right: 0, bottom: 0, height: 3, background: skin.hair }}>
        <div
          style={{
            width: `${Math.min(1, frame / Math.max(1, total)) * 100}%`,
            height: "100%",
            background: active.light ? "#8B7FB0" : LILAC,
            opacity: 0.8,
          }}
        />
      </div>
    </AbsoluteFill>
  );
};
