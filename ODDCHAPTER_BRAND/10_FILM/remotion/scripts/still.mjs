/**
 * still.mjs — render single frames from the pilot for review without encoding video.
 *   npm run preview            → output/preview_<frame>.png for a few key frames
 */
import fs from "node:fs";
import path from "node:path";
import url from "node:url";
import { bundle } from "@remotion/bundler";
import { renderStill, selectComposition } from "@remotion/renderer";
import { chromiumArgs, resolveChromium } from "./chromium.mjs";

const here = path.dirname(url.fileURLToPath(import.meta.url));
const root = path.resolve(here, "..");
const out = path.join(root, "output");
fs.mkdirSync(out, { recursive: true });

const FRAMES = [30, 110, 300, 500, 700];

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
const composition = await selectComposition({ serveUrl, id: "ODDCHAPTER-PILOT-001", ...opts });

for (const frame of FRAMES) {
  const file = path.join(out, `preview_${String(frame).padStart(4, "0")}.png`);
  await renderStill({ composition, serveUrl, output: file, frame, ...opts });
  console.log(`${path.relative(root, file)}  (frame ${frame})`);
}
console.log(`rendered by ${browser.engine} ${browser.version}`);
