/**
 * render-mapzoom.mjs — render shot peta asli zoom-in ke lokasi kejadian.
 *
 *   node scripts/render-mapzoom.mjs <job.json>
 *
 * job.json:
 * {
 *   "name": "drumherg_1928",
 *   "props": { ...MapZoomProps (src, bounds, target, zone, points, ...) }
 * }
 *
 * Output: output/map_<name>.mp4 (1080x1920,30 fps, tanpa audio, crf16).
 * Peta asli di-sync dari assets/maps/ → public/maps/ sebelum bundling;
 * src/brand.json dibuat dulu bila belum ada (dibutuhkan theme.ts).
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
const root = path.resolve(here, ".."); // ODDCHAPTER_BRAND/10_FILM/remotion
const repo = path.resolve(root, "..", "..", ".."); // repo root (remotion→10_FILM→ODDCHAPTER_BRAND→root)
const out = path.join(root, "output");
fs.mkdirSync(out, { recursive: true });

const jobPath = process.argv[2];
if (!jobPath) {
  console.error("usage: node scripts/render-mapzoom.mjs <job.json>");
  process.exit(1);
}
const job = JSON.parse(fs.readFileSync(jobPath, "utf8"));
if (!job?.name || !job?.props) {
  console.error("job.json harus memuat { name, props }");
  process.exit(1);
}

// brand.json (dibutuhkan src/theme.ts)
const brandJson = path.join(root, "src", "brand.json");
if (!fs.existsSync(brandJson)) {
  execFileSync(
    "python3",
    [path.join(repo, "ODDCHAPTER_BRAND", "tools", "export_brand_json.py")],
    { stdio: "inherit" },
  );
}

// sync peta asli: assets/maps → public/maps
const mapsSrc = path.join(repo, "assets", "maps");
const mapsDst = path.join(root, "public", "maps");
fs.mkdirSync(mapsDst, { recursive: true });
for (const f of fs.readdirSync(mapsSrc)) {
  if (f === "SOURCES.json") continue;
  const s = path.join(mapsSrc, f);
  const d = path.join(mapsDst, f);
  if (!fs.existsSync(d) || fs.statSync(s).mtimeMs > fs.statSync(d).mtimeMs) {
    fs.copyFileSync(s, d);
    console.log("maps ←", f);
  }
}

const probe = (file) =>
  JSON.parse(
    execFileSync(
      FFPROBE,
      [
        "-v", "error",
        "-show_entries", "format=duration,size:stream=width,height",
        "-of", "json", file,
      ],
      { encoding: "utf8" },
    ),
  );

const browser = await resolveChromium();
console.log("browser     :", browser.version);

console.log("bundling…");
const serveUrl = await bundle({
  entryPoint: path.join(root, "src", "index.ts"),
  publicDir: path.join(root, "public"),
});

const browserOpts = {
  browserExecutable: browser.executablePath,
  chromiumOptions: { gl: "swangle" },
  args: chromiumArgs,
};

const comp = await selectComposition({
  serveUrl,
  id: "MAP-ZOOM",
  inputProps: job.props,
  ...browserOpts,
});
const dur = Math.min(
  comp.durationInFrames,
  job.props.durationInFrames ?? comp.durationInFrames,
);
console.log(
  `composition : ${comp.id} · ${comp.width}x${comp.height} · ${dur} frames`,
);

// still QC di frame titik kejadian (zoneFrame ± kecil)
const stillFrame = Math.min(
  dur - 2,
  Math.max(0, (job.props.zoneFrame ?? 60) + 20),
);
const stillPath = path.join(out, `map_${job.name}_still.png`);
await renderStill({
  composition: comp,
  serveUrl,
  output: stillPath,
  frame: stillFrame,
  inputProps: job.props,
  ...browserOpts,
});
console.log("still       :", path.relative(root, stillPath), "@ frame", stillFrame);

const outVideo = path.join(out, `map_${job.name}.mp4`);
console.log("rendering   :", outVideo, "…");
await renderMedia({
  composition: comp,
  serveUrl,
  codec: "h264",
  outputLocation: outVideo,
  pixelFormat: "yuv420p",
  crf: 16,
  imageFormat: "png",
  muted: true,
  frameRange: [0, dur - 1],
  inputProps: job.props,
  ...browserOpts,
});

const p = probe(outVideo);
const v = p.streams.find((s) => s.width);
console.log(
  `done        : ${v.width}x${v.height} · ${Number(p.format.duration).toFixed(2)}s · ${p.format.size} B`,
);
