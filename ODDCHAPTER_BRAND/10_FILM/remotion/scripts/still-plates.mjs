/**
 * still-plates.mjs — render 10 frame dari PLATE-GALLERY, satu per bentuk dasar.
 *   node scripts/still-plates.mjs          -> output/plates/plate_00..09.png
 */
import fs from "node:fs";
import path from "node:path";
import url from "node:url";
import { bundle } from "@remotion/bundler";
import { renderStill, selectComposition } from "@remotion/renderer";
import { chromiumArgs, resolveChromium } from "./chromium.mjs";

const here = path.dirname(url.fileURLToPath(import.meta.url));
const root = path.resolve(here, "..");
const out = path.join(root, "output", "plates");
fs.mkdirSync(out, { recursive: true });

const browser = await resolveChromium();
const serveUrl = await bundle({ entryPoint: path.join(root, "src", "index.ts"), publicDir: path.join(root, "public") });
const opts = { browserExecutable: browser.executablePath, chromiumOptions: { gl: "swangle" }, args: chromiumArgs };
const composition = await selectComposition({ serveUrl, id: "PLATE-GALLERY", ...opts });

for (let i = 0; i < composition.durationInFrames; i++) {
  const file = path.join(out, `plate_${String(i).padStart(2, "0")}.png`);
  await renderStill({ composition, serveUrl, output: file, frame: i, ...opts });
  console.log(path.relative(root, file));
}
