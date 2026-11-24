import React from "react";
import {
  AbsoluteFill,
  Audio,
  Easing,
  Img,
  interpolate,
  staticFile,
  useCurrentFrame,
} from "remotion";
import { C, H, W } from "../theme";

const TOTAL = 1065; // 35.50 s @ 30 fps; matches the measured AK-EP11 review VO.
const ease = Easing.bezier(0.2, 0.7, 0.2, 1);
const clamp = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;

const sceneOpacity = (frame: number, from: number, until: number) =>
  interpolate(frame, [from, from + 8, until - 8, until], [0, 1, 1, 0], {
    ...clamp,
    easing: ease,
  });

const Backdrop: React.FC<{ accent?: boolean }> = ({ accent = false }) => {
  const frame = useCurrentFrame();
  const drift = Math.sin(frame / 80) * 34;
  return (
    <AbsoluteFill
      style={{
        background:
          "radial-gradient(900px 900px at 115% 18%, #124d59 0%, #092b3a 34%, #061924 68%, #04131f 100%)",
        overflow: "hidden",
      }}
    >
      <div
        style={{
          position: "absolute",
          width: 1160,
          height: 1160,
          left: -630 + drift,
          top: 930,
          borderRadius: "50%",
          background: "rgba(1, 56, 73, .52)",
        }}
      />
      <div
        style={{
          position: "absolute",
          width: 860,
          height: 860,
          right: -440 - drift * 0.3,
          top: -260,
          borderRadius: "50%",
          background: accent ? "rgba(216, 42, 42, .16)" : "rgba(37, 96, 108, .25)",
        }}
      />
      <WaveField />
      <div
        style={{
          position: "absolute",
          inset: 0,
          background:
            "repeating-linear-gradient(0deg, rgba(255,255,255,.018) 0 1px, transparent 1px 12px)",
          opacity: 0.46,
        }}
      />
    </AbsoluteFill>
  );
};

const WaveField: React.FC = () => {
  const frame = useCurrentFrame();
  return (
    <svg width={W} height={H} viewBox={`0 0 ${W} ${H}`} style={{ position: "absolute", inset: 0, opacity: 0.52 }}>
      {Array.from({ length: 12 }, (_, i) => {
        const y = 740 + i * 72;
        const amp = 20 + (i % 3) * 9;
        const shift = ((frame * (0.45 + (i % 4) * 0.07) + i * 64) % 260) - 130;
        return (
          <path
            key={i}
            d={`M-180 ${y} Q 80 ${y - amp} 340 ${y} T 860 ${y} T 1280 ${y}`}
            transform={`translate(${shift} 0)`}
            fill="none"
            stroke={i % 4 === 0 ? "rgba(216,42,42,.24)" : "rgba(111,190,198,.22)"}
            strokeWidth={i % 3 === 0 ? 4 : 2}
          />
        );
      })}
    </svg>
  );
};

const Kicker: React.FC<{ children: React.ReactNode }> = ({ children }) => (
  <div
    style={{
      color: "#d82a2a",
      fontFamily: "Inter",
      fontWeight: 600,
      letterSpacing: "0.14em",
      fontSize: 27,
      textTransform: "uppercase",
    }}
  >
    {children}
  </div>
);

const Headline: React.FC<{ children: React.ReactNode; size?: number; color?: string }> = ({
  children,
  size = 126,
  color = C.ivory,
}) => (
  <div
    style={{
      color,
      fontFamily: "Space Grotesk",
      fontWeight: 700,
      fontSize: size,
      letterSpacing: "-0.065em",
      lineHeight: 0.91,
      whiteSpace: "pre-line",
    }}
  >
    {children}
  </div>
);

const Source: React.FC<{ children: React.ReactNode }> = ({ children }) => (
  <div
    style={{
      position: "absolute",
      left: 62,
      right: 62,
      bottom: 70,
      padding: "19px 24px",
      borderTop: "1px solid rgba(240,236,224,.17)",
      color: "#b6c9ca",
      fontFamily: "Inter",
      fontWeight: 500,
      fontSize: 21,
      letterSpacing: "0.04em",
      background: "rgba(1,10,15,.56)",
    }}
  >
    {children}
  </div>
);

const Scene: React.FC<{ from: number; until: number; children: React.ReactNode; accent?: boolean }> = ({
  from,
  until,
  children,
  accent,
}) => {
  const frame = useCurrentFrame();
  if (frame < from || frame >= until) return null;
  const opacity = sceneOpacity(frame, from, until);
  const rise = interpolate(frame, [from, from + 12], [36, 0], { ...clamp, easing: ease });
  return (
    <AbsoluteFill style={{ opacity }}>
      <Backdrop accent={accent} />
      <div style={{ position: "absolute", inset: 0, transform: `translateY(${rise}px)` }}>{children}</div>
    </AbsoluteFill>
  );
};

const MapCard: React.FC<{ marker?: boolean; zoom?: number }> = ({ marker = false, zoom = 1 }) => {
  const frame = useCurrentFrame();
  const pulse = 1 + 0.14 * (0.5 + 0.5 * Math.sin(frame / 8));
  return (
    <div
      style={{
        position: "absolute",
        left: 65,
        right: 65,
        top: 470,
        height: 768,
        padding: 24,
        background: "#efeee6",
        boxShadow: "0 28px 70px rgba(0,0,0,.36)",
        overflow: "hidden",
      }}
    >
      <Img
        src={staticFile("ak-ep11/simeulue_topography_cc-by-sa-3.png")}
        style={{ width: "100%", height: "100%", objectFit: "contain", transform: `scale(${zoom})` }}
      />
      {marker ? (
        <>
          <div
            style={{
              position: "absolute",
              left: 292,
              top: 77,
              width: 36,
              height: 36,
              borderRadius: 999,
              background: "#d82a2a",
              border: "5px solid #f0ece0",
              transform: `scale(${pulse})`,
              boxShadow: "0 0 0 16px rgba(216,42,42,.17)",
            }}
          />
          <div
            style={{
              position: "absolute",
              left: 324,
              top: 60,
              padding: "12px 18px",
              background: "#d82a2a",
              color: C.ivory,
              fontFamily: "Inter",
              fontWeight: 700,
              fontSize: 34,
              letterSpacing: "0.05em",
            }}
          >
            LANGI
          </div>
        </>
      ) : null}
    </div>
  );
};

const Step: React.FC<{ n: string; text: string; y: number; from: number }> = ({ n, text, y, from }) => {
  const frame = useCurrentFrame();
  const p = interpolate(frame, [from, from + 14], [0, 1], { ...clamp, easing: ease });
  return (
    <div
      style={{
        position: "absolute",
        left: 72,
        right: 72,
        top: y,
        height: 162,
        display: "flex",
        alignItems: "center",
        gap: 36,
        padding: "0 36px",
        borderRadius: 22,
        border: "2px solid rgba(133,202,205,.35)",
        background: "rgba(10,54,65,.74)",
        opacity: p,
        transform: `translateX(${(1 - p) * 80}px)`,
      }}
    >
      <div
        style={{
          width: 88,
          height: 88,
          borderRadius: 99,
          background: "#d82a2a",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          fontFamily: "Space Grotesk",
          fontWeight: 700,
          fontSize: 45,
          color: C.ivory,
        }}
      >
        {n}
      </div>
      <div style={{ fontFamily: "Space Grotesk", fontWeight: 700, fontSize: 67, color: C.ivory, letterSpacing: "-0.05em" }}>
        {text}
      </div>
    </div>
  );
};

const Pulse: React.FC = () => {
  const frame = useCurrentFrame();
  return (
    <svg width={W} height={H} viewBox={`0 0 ${W} ${H}`} style={{ position: "absolute", inset: 0 }}>
      {[0, 1, 2, 3].map((i) => {
        const p = ((frame - i * 12) % 54) / 54;
        const r = 80 + Math.max(0, p) * 480;
        return <circle key={i} cx={540} cy={1030} r={r} fill="none" stroke="#d82a2a" strokeWidth={5} opacity={Math.max(0, 0.52 - p * 0.5)} />;
      })}
    </svg>
  );
};

export const SmongReview: React.FC = () => {
  const frame = useCurrentFrame();
  const heroScale = interpolate(frame, [0, 25], [0.94, 1], { ...clamp, easing: ease });
  return (
    <AbsoluteFill>
      <Audio src={staticFile("audio/ak-ep11-smong-review.wav")} />

      <Scene from={0} until={130} accent>
        <div style={{ position: "absolute", left: 72, top: 164, transform: `scale(${heroScale})`, transformOrigin: "left top" }}>
          <Kicker>Simeulue · Aceh</Kicker>
          <div style={{ height: 38 }} />
          <Headline>SAAT LAUT{`\n`}SURUT</Headline>
          <div style={{ marginTop: 48, fontFamily: "Inter", fontWeight: 600, fontSize: 44, color: "#b6c9ca", lineHeight: 1.26 }}>
            warga tidak menunggu{`\n`}peringatan resmi.
          </div>
        </div>
        <div style={{ position: "absolute", left: 72, top: 747, padding: "22px 28px", background: "#d82a2a", color: C.ivory, fontFamily: "Inter", fontWeight: 700, fontSize: 35, letterSpacing: "0.08em" }}>
          JANGAN TUNGGU
        </div>
        <Source>ILUSTRASI DATA · BUKAN REKAMAN KEJADIAN</Source>
      </Scene>

      <Scene from={130} until={251}>
        <div style={{ position: "absolute", left: 72, top: 132 }}>
          <Kicker>Pulau di barat Aceh</Kicker>
          <div style={{ height: 30 }} />
          <Headline size={103}>SIMEULUE</Headline>
          <div style={{ marginTop: 18, fontFamily: "Inter", fontWeight: 600, fontSize: 42, color: "#b6c9ca" }}>satu kata diwariskan: <span style={{ color: "#d82a2a" }}>SMONG</span></div>
        </div>
        <MapCard />
        <Source>PETA: SADALMELIK · WIKIMEDIA COMMONS · CC BY-SA 3.0</Source>
      </Scene>

      <Scene from={251} until={396}>
        <div style={{ position: "absolute", left: 72, top: 138 }}>
          <Kicker>Smong</Kicker>
          <div style={{ height: 30 }} />
          <Headline size={94}>SATU URUTAN{`\n`}YANG DIINGAT</Headline>
        </div>
        <Step n="1" text="GEMPA KUAT" y={520} from={267} />
        <Step n="2" text="LAUT SURUT" y={736} from={300} />
        <Step n="3" text="KE BUKIT" y={952} from={333} />
        <Source>PENGETAHUAN LISAN LINTAS GENERASI · UNESCO</Source>
      </Scene>

      <Scene from={396} until={532} accent>
        <div style={{ position: "absolute", left: 72, top: 138 }}>
          <Kicker>26 Desember 2004</Kicker>
          <div style={{ height: 30 }} />
          <Headline size={102}>WAKTUNYA{`\n`}KURANG DARI</Headline>
        </div>
        <div style={{ position: "absolute", left: 72, top: 630, fontFamily: "Space Grotesk", fontSize: 372, letterSpacing: "-0.12em", color: "#d82a2a", fontWeight: 700 }}>10</div>
        <div style={{ position: "absolute", left: 560, top: 820, fontFamily: "Space Grotesk", fontSize: 105, letterSpacing: "-0.07em", color: C.ivory, fontWeight: 700 }}>MENIT</div>
        <div style={{ position: "absolute", left: 78, top: 1110, right: 78, height: 5, background: "rgba(181,216,217,.55)" }} />
        <div style={{ position: "absolute", left: 76, top: 1180, fontFamily: "Inter", fontWeight: 600, fontSize: 42, color: "#b6c9ca" }}>guncangan berhenti</div>
        <div style={{ position: "absolute", left: 76, top: 1242, fontFamily: "Inter", fontWeight: 700, fontSize: 42, color: C.ivory }}>gelombang mencapai Langi</div>
        <Source>MCADOO, DENGLER, PRASETYA & TITOV · 2006</Source>
      </Scene>

      <Scene from={532} until={624} accent>
        <Pulse />
        <div style={{ position: "absolute", left: 72, top: 152 }}>
          <Kicker>Simulasi data</Kicker>
          <div style={{ height: 26 }} />
          <Headline size={106}>GELOMBANG{`\n`}MENYEBAR</Headline>
        </div>
        <div style={{ position: "absolute", left: 92, right: 92, top: 780, padding: 40, background: "rgba(4,25,35,.78)", border: "1px solid rgba(216,42,42,.65)" }}>
          <div style={{ fontFamily: "Inter", fontWeight: 700, fontSize: 35, letterSpacing: "0.08em", color: "#d82a2a" }}>LANGI · UTARA SIMEULUE</div>
          <div style={{ marginTop: 24, fontFamily: "Space Grotesk", fontWeight: 700, fontSize: 74, lineHeight: 1.0, letterSpacing: "-0.055em", color: C.ivory }}>KURANG DARI{`\n`}SEPULUH MENIT</div>
        </div>
        <Source>VISUALISASI DATA · BUKAN REKAMAN KEJADIAN</Source>
      </Scene>

      <Scene from={624} until={855}>
        <div style={{ position: "absolute", left: 72, top: 128 }}>
          <Kicker>Pulau di barat Aceh</Kicker>
          <div style={{ height: 24 }} />
          <Headline size={94}>LANGI · UTARA{`\n`}SIMEULUE</Headline>
        </div>
        <MapCard marker zoom={1.06} />
        <div style={{ position: "absolute", left: 72, right: 72, top: 1288, padding: "34px 38px", border: "2px solid rgba(216,42,42,.66)", background: "rgba(4,18,28,.86)" }}>
          <div style={{ fontFamily: "Inter", fontWeight: 600, fontSize: 42, color: "#b6c9ca" }}>DESANYA HANCUR.</div>
          <div style={{ display: "flex", alignItems: "flex-end", gap: 28, marginTop: 8 }}>
            <div style={{ fontFamily: "Space Grotesk", fontSize: 146, fontWeight: 700, letterSpacing: "-0.1em", color: "#d82a2a" }}>≈800</div>
            <div style={{ marginBottom: 22, fontFamily: "Space Grotesk", fontSize: 76, fontWeight: 700, lineHeight: 0.92, letterSpacing: "-0.07em", color: C.ivory }}>WARGA{`\n`}SELAMAT</div>
          </div>
        </div>
        <Source>PETA: SADALMELIK · DATA LANGI: MCADOO DKK. 2006</Source>
      </Scene>

      <Scene from={855} until={970}>
        <div style={{ position: "absolute", left: 72, top: 170 }}>
          <Kicker>Bukan menebak laut</Kicker>
          <div style={{ height: 30 }} />
          <Headline size={102}>MEREKA{`\n`}MENGINGAT</Headline>
        </div>
        <div style={{ position: "absolute", left: 72, right: 72, top: 720, padding: 50, border: "2px solid rgba(137,204,206,.38)", background: "rgba(10,54,65,.7)" }}>
          <div style={{ fontFamily: "Space Grotesk", fontSize: 100, fontWeight: 700, letterSpacing: "-0.07em", color: C.ivory }}>CERITA</div>
          <div style={{ margin: "12px 0", fontFamily: "Space Grotesk", fontSize: 106, fontWeight: 700, color: "#d82a2a" }}>→</div>
          <div style={{ fontFamily: "Space Grotesk", fontSize: 100, fontWeight: 700, letterSpacing: "-0.07em", color: C.ivory }}>TINDAKAN</div>
        </div>
        <Source>SMONG · CERITA DAN SYAIR ANTARGENERASI</Source>
      </Scene>

      <Scene from={970} until={TOTAL} accent>
        <div style={{ position: "absolute", left: 72, top: 164 }}>
          <Kicker>Pertanyaan terakhir</Kicker>
          <div style={{ height: 34 }} />
          <Headline size={102}>SIAPA YANG{`\n`}MENGAJARKAN{`\n`}TANDA BAHAYA?</Headline>
        </div>
        <div style={{ position: "absolute", left: 74, bottom: 270, fontFamily: "Inter", fontWeight: 700, fontSize: 34, letterSpacing: "0.08em", color: "#d82a2a" }}>TULIS DI KOMENTAR</div>
        <Source>SUMBER: NOAA PMEL · UNESCO · BMKG</Source>
      </Scene>
    </AbsoluteFill>
  );
};
