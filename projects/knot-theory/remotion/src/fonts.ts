import { useEffect, useState } from "react";
import { staticFile } from "remotion";
import { cancelRender, continueRender, delayRender } from "remotion";

const FACES: { family: string; file: string; weight?: string; style?: string }[] = [
  { family: "Instrument Serif", file: "InstrumentSerif-Regular.ttf" },
  { family: "Instrument Serif", file: "InstrumentSerif-Italic.ttf", style: "italic" },
  { family: "Plex Mono", file: "IBMPlexMono-Regular.ttf" },
  { family: "Plex Mono", file: "IBMPlexMono-Medium.ttf", weight: "500" },
];

/** Muat font sekali; render ditahan sampai semua siap. */
export const useFonts = (): boolean => {
  const [ready, setReady] = useState(false);
  const [handle] = useState(() => delayRender("memuat font"));

  useEffect(() => {
    let alive = true;
    const load = async () => {
      try {
        await Promise.all(
          FACES.map(async (f) => {
            const face = new FontFace(
              f.family,
              `url(${staticFile(`fonts/${f.file}`)})`,
              { weight: f.weight ?? "400", style: f.style ?? "normal" }
            );
            await face.load();
            document.fonts.add(face);
          })
        );
        if (!alive) return;
        setReady(true);
        continueRender(handle);
      } catch (e) {
        cancelRender(e as Error);
      }
    };
    load();
    return () => {
      alive = false;
    };
  }, [handle]);

  return ready;
};
