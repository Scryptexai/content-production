/**
 * still-ep01.mjs — render frame kunci EP01 untuk review sebelum encode.
 *   node scripts/still-ep01.mjs 30 100 300 ...
 * Tanpa argumen: sepuluh frame yang mewakili setiap bagian timeline.
 */
import fs from "node:fs";
import path from "node:path";
import url from "node:url";
import { bundle } from "@remotion/bundler";
import { renderStill, selectComposition } from "@remotion/renderer";
import { chromiumArgs, resolveChromium } from "./chromium.mjs";

const here = path.dirname(url.fileURLToPath(import.meta.url));
const root = path.resolve(here, "..");
const out = path.join(root, "output", "ep01");
fs.mkdirSync(out, { recursive: true });

const args = process.argv.slice(2).map(Number).filter((n) => !Number.isNaN(n));
const FRAMES = args.length ? args : [30, 100, 300, 450, 700, 900, 1000, 1300, 1400, 1600];

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
const composition = await selectComposition({ serveUrl, id: "ODDCHAPTER-EP01", ...opts });

for (const frame of FRAMES) {
  const file = path.join(out, `frame_${String(frame).padStart(4, "0")}.png`);
  await renderStill({ composition, serveUrl, output: file, frame, ...opts });
  console.log(`${path.relative(root, file)}  ${frame}f = ${(frame / composition.fps).toFixed(2)}s`);
}
console.log(`browser: ${browser.executablePath}`);
