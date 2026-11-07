/**
 * render-episode.mjs — render satu episode dari komposisi ODDCHAPTER-EPxx.
 *
 *   node scripts/render-episode.mjs EP01
 *
 * Alur: bundle → pilih komposisi → render (h264 + aac) → normalisasi loudness
 * → faststart → probe. Browser: @sparticuz/chromium lewat browserExecutable.
 */
import fs from "node:fs";
import path from "node:path";
import url from "node:url";
import { execFileSync } from "node:child_process";
import { bundle } from "@remotion/bundler";
import { renderMedia, selectComposition } from "@remotion/renderer";
import { chromiumArgs, resolveChromium } from "./chromium.mjs";
import ffmpegPath from "@ffmpeg-installer/ffmpeg";
import ffprobePath from "@ffprobe-installer/ffprobe";

const FFMPEG = ffmpegPath.path;
const FFPROBE = ffprobePath.path;

const here = path.dirname(url.fileURLToPath(import.meta.url));
const root = path.resolve(here, "..");
const outDir = path.join(root, "output", "episodes");
fs.mkdirSync(outDir, { recursive: true });

const epId = process.argv[2] || "EP01";

const probe = (file) =>
  JSON.parse(
    execFileSync(
      FFPROBE,
      ["-v", "error", "-show_entries",
       "format=duration,size,bit_rate:stream=codec_name,codec_type,width,height,r_frame_rate,pix_fmt,sample_rate,channels",
       "-of", "json", file],
      { encoding: "utf8" },
    ),
  );

const browser = await resolveChromium();
console.log(`browser    : ${browser.engine} ${browser.version}`);
console.log(`executable : ${browser.executablePath}`);

const serveUrl = await bundle({
  entryPoint: path.join(root, "src", "index.ts"),
  publicDir: path.join(root, "public"),
});
const browserOpts = { browserExecutable: browser.executablePath, chromiumOptions: { gl: "swangle" }, args: chromiumArgs };
const composition = await selectComposition({ serveUrl, id: `ODDCHAPTER-${epId}`, ...browserOpts });
console.log(`composition: ${composition.id} ${composition.width}x${composition.height} ${composition.durationInFrames}f @${composition.fps}fps`);

const rawFile = path.join(outDir, `${epId}_raw.mp4`);
const master = path.join(outDir, `${epId}_1080x1920_master.mp4`);

console.log("rendering…");
const t0 = Date.now();
await renderMedia({
  composition,
  serveUrl,
  codec: "h264",
  outputLocation: rawFile,
  audioCodec: "aac",
  audioBitrate: "192k",
  videoBitrate: "8M",
  x264Preset: "medium",
  pixelFormat: "yuv420p",
  concurrency: 2,
  imageFormat: "jpeg",
  jpegQuality: 92,
  ...browserOpts,
});
console.log(`rendered in ${((Date.now() - t0) / 1000).toFixed(0)}s → ${path.relative(root, rawFile)}`);

// normalisasi loudness + faststart, satu pass (target −14 LUFS, TP −1.5)
execFileSync(FFMPEG, [
  "-y", "-i", rawFile,
  "-af", "loudnorm=I=-14:TP=-1.5:LRA=11",
  "-c:v", "copy",
  "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
  "-movflags", "+faststart",
  master,
]);

const info = probe(master);
const v = info.streams.find((s) => s.codec_type === "video");
const a = info.streams.find((s) => s.codec_type === "audio");
console.log("master     :", path.relative(root, master));
console.log(`video      : ${v.codec_name} ${v.width}x${v.height} ${v.pix_fmt} ${v.r_frame_rate}`);
console.log(`audio      : ${a.codec_name} ${a.sample_rate}Hz ${a.channels}ch`);
console.log(`duration   : ${Number(info.format.duration).toFixed(2)}s  ${(Number(info.format.size) / 1048576).toFixed(2)} MB`);
fs.writeFileSync(path.join(outDir, `${epId}.report.json`), JSON.stringify({ epId, browser: browser.version, executable: browser.executablePath, ...info }, null, 2));
