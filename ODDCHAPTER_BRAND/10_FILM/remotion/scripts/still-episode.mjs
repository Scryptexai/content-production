/**
 * still-episode.mjs — render frame kunci dari episode mana pun untuk review.
 *
 *   node scripts/still-episode.mjs EP02 0 60 264 408 589 753
 *
 * Tanpa frame: memakai sebelas titik yang mewakili timeline episode itu
 * (frame 0 selalu ikut, karena frame 0 wajib sama dengan thumbnail).
 */
import fs from "node:fs";
import path from "node:path";
import url from "node:url";
import { bundle } from "@remotion/bundler";
import { renderStill, selectComposition } from "@remotion/renderer";
import { chromiumArgs, resolveChromium } from "./chromium.mjs";

const here = path.dirname(url.fileURLToPath(import.meta.url));
const root = path.resolve(here, "..");
const epId = process.argv[2] || "EP01";
const out = path.join(root, "output", epId.toLowerCase());
fs.mkdirSync(out, { recursive: true });

const browser = await resolveChromium();
const serveUrl = await bundle({
  entryPoint: path.join(root, "src", "index.ts"),
  publicDir: path.join(root, "public"),
});
const opts = {
  browserExecutable: browser.executablePath,
  chromiumOptions: { gl: "swangle" },
  args: chromiumArgs,
};
const composition = await selectComposition({ serveUrl, id: `ODDCHAPTER-${epId}`, ...opts });

const given = process.argv.slice(3).map(Number).filter((n) => !Number.isNaN(n));
const FRAMES = given.length
  ? given
  : [0, ...Array.from({ length: 10 }, (_, i) =>
      Math.round(composition.durationInFrames * (i + 1) / 11))];

for (const frame of FRAMES) {
  const file = path.join(out, `frame_${String(frame).padStart(4, "0")}.png`);
  await renderStill({ composition, serveUrl, output: file, frame, ...opts });
  console.log(`${path.relative(root, file)}  ${frame}f = ${(frame / composition.fps).toFixed(2)}s`);
}
console.log(`browser: ${browser.executablePath}  frames: ${composition.durationInFrames}`);
