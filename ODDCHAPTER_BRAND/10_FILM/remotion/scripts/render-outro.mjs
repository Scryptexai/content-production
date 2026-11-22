/**
 * render-outro.mjs — render kartu akhir animasi Shorts9:16.
 *
 *   node scripts/render-outro.mjs
 *
 * Output: output/short_outro_9x16.mp4 (1080x1920,30 fps, tanpa audio, crf16).
 * Klip ini dipakai build_short_case.py (mode "outro") sebagai segmen terakhir
 * episode — menggantikan kartu hitam statis + overlay teks.
 *
 * Hanya butuh src/brand.json (python3 ../tools/export_brand_json.py) — tanpa
 * font live, tanpa audio, tanpa captions.
 */
import fs from "node:fs";
import path from "node:path";
import url from "node:url";
import { execFileSync } from "node:child_process";
import { bundle } from "@remotion/bundler";
import { renderMedia, selectComposition, renderStill } from "@remotion/renderer";
import { chromiumArgs, resolveChromium } from "./chromium.mjs";
import ffmpegPath from "@ffmpeg-installer/ffmpeg";
import ffprobePath from "@ffprobe-installer/ffprobe";

const FFMPEG = ffmpegPath.path;
const FFPROBE = ffprobePath.path;

const here = path.dirname(url.fileURLToPath(import.meta.url));
const root = path.resolve(here, "..");
const out = path.join(root, "output");
fs.mkdirSync(out, { recursive: true });

const brandJson = path.join(root, "src", "brand.json");
if (!fs.existsSync(brandJson)) {
  console.error("missing src/brand.json — run: python3 ../tools/export_brand_json.py");
  process.exit(1);
}

const probe = (file) =>
  JSON.parse(
    execFileSync(
      FFPROBE,
      ["-v", "error", "-show_entries", "format=duration,size:stream=width,height,codec_name",
       "-of", "json", file],
      { encoding: "utf8" },
    ),
  );

const browser = await resolveChromium();
console.log(`browser     : ${browser.version}`);

console.log("bundling…");
const serveUrl = await bundle({
  entryPoint: path.join(root, "src", "index.ts"),
  publicDir: path.join(root, "public"),
});

const browserOpts = { browserExecutable: browser.executablePath, chromiumOptions: { gl: "swangle" }, args: chromiumArgs };

const comp = await selectComposition({ serveUrl, id: "SHORT-OUTRO-9X16", ...browserOpts });
console.log(`composition : ${comp.id} · ${comp.width}x${comp.height} · ${comp.durationInFrames} frames @${comp.fps}`);

// still dulu — QC visual cepat sebelum render penuh
const stillPath = path.join(out, "short_outro_still.png");
await renderStill({ composition: comp, serveUrl, output: stillPath, frame: 66, ...browserOpts });
console.log(`still       : ${path.relative(root, stillPath)}`);

const outVideo = path.join(out, "short_outro_9x16.mp4");
console.log(`rendering   : ${outVideo} …`);
await renderMedia({
  composition: comp,
  serveUrl,
  codec: "h264",
  outputLocation: outVideo,
  pixelFormat: "yuv420p",
  crf: 16,
  imageFormat: "png",
  muted: true,
  ...browserOpts,
});

const p = probe(outVideo);
const v = p.streams.find((s) => s.width);
console.log(`done        : ${v.width}x${v.height} · ${Number(p.format.duration).toFixed(2)}s · ${p.format.size} B`);
