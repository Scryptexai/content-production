import { continueRender, cancelRender, delayRender, staticFile } from "remotion";

/**
 * Local typefaces, loaded before the first frame is captured.
 * Files are copied into public/fonts by scripts/prepare-assets.mjs (they are
 * SIL OFL 1.1 and deliberately not committed to the repository).
 */
const FACES: [string, string, string, string][] = [
  ["Space Grotesk", "space-grotesk-latin-300-normal.ttf", "300", "normal"],
  ["Space Grotesk", "space-grotesk-latin-500-normal.ttf", "500", "normal"],
  ["Space Grotesk", "space-grotesk-latin-700-normal.ttf", "700", "normal"],
  ["Inter", "inter-latin-500-normal.ttf", "500", "normal"],
  ["Inter", "inter-latin-600-normal.ttf", "600", "normal"],
];

const handle = delayRender("Loading brand fonts");

Promise.all(
  FACES.map(async ([family, file, weight, style]) => {
    const face = new FontFace(family, `url(${staticFile(`fonts/${file}`)}) format('truetype')`, {
      weight,
      style,
    });
    await face.load();
    document.fonts.add(face);
  }),
)
  .then(() => continueRender(handle))
  .catch((err) => cancelRender(err));

export {};
