/**
 * render-longform.mjs — render episode panjang (VO pemilik, timestamp pemilik).
 *
 *   node scripts/render-longform.mjs still 0 900 3600     # uji tampilan
 *   node scripts/render-longform.mjs render                # render penuh
 *
 * Alur: bundle → composition ODDCHAPTER-LONGFORM-EP01 → render PNG frames
 * (png dipakai supaya warna tidak keluar full-range seperti jalur JPEG)
 * → normalisasi loudness −14 LUFS / TP −1.5 tanpa menyentuh video → faststart.
 */
import fs from "node:fs";
import path from "node:path";
import url from "node:url";
import { execFileSync } from "node:child_process";
import { bundle } from "@remotion/bundler";
import { renderMedia, renderStill, selectComposition } from "@remotion/renderer";
import { chromiumArgs, resolveChromium } from "./chromium.mjs";
import ffmpegPath from "@ffmpeg-installer/ffmpeg";
import ffprobePath from "@ffprobe-installer/ffprobe";

const FFMPEG = ffmpegPath.path;
const FFPROBE = ffprobePath.path;
const here = path.dirname(url.fileURLToPath(import.meta.url));
const root = path.resolve(here, "..");
const outDir = path.join(root, "output", "episodes");
fs.mkdirSync(outDir, { recursive: true });

const ID = "ODDCHAPTER-LONGFORM-EP01";
const NAME = "EP01_ILLUMINATI";
const mode = process.argv[2] || "render";

const probe = (file) =>
  JSON.parse(
    execFileSync(FFPROBE, ["-v", "error", "-show_entries",
      "format=duration,size,bit_rate:stream=codec_name,codec_type,width,height,r_frame_rate,pix_fmt,sample_rate,channels",
      "-of", "json", file], { encoding: "utf8" }),
  );

// timing.generated.json (short) dibuat tools/build_timing.py dan di-ignore Git.
// Untuk render long-form tidak dibutuhkan, tetapi Root.tsx meng-import-nya:
// berkas kosong ini hanya menjaga bundler tetap jalan di sandbox baru.
const timingFile = path.join(root, "src", "timing.generated.json");
if (!fs.existsSync(timingFile)) fs.writeFileSync(timingFile, "{}\n");
const epsFile = path.join(root, "src", "episodes.generated.json");
if (!fs.existsSync(epsFile)) fs.writeFileSync(epsFile, "[]\n");

const browser = await resolveChromium();
const serveUrl = await bundle({
  entryPoint: path.join(root, "src", "index.ts"),
  publicDir: path.join(root, "public"),
});
const browserOpts = { browserExecutable: browser.executablePath, chromiumOptions: { gl: "swangle" }, args: chromiumArgs };
const composition = await selectComposition({ serveUrl, id: ID, ...browserOpts });
console.log(`composition: ${composition.id} ${composition.width}x${composition.height} ${composition.durationInFrames}f @${composition.fps}fps (${(composition.durationInFrames / composition.fps / 60).toFixed(2)} menit)`);

if (mode === "still") {
  const frames = process.argv.slice(3).map(Number);
  for (const f of frames.length ? frames : [30, 1200, 5000, 9000]) {
    const out = path.join(outDir, `still_${NAME}_${f}.png`);
    await renderStill({ composition, serveUrl, output: out, frame: f, ...browserOpts });
    console.log("still:", path.relative(root, out));
  }
  process.exit(0);
}

const range = process.argv.slice(3).map(Number).filter((n) => !Number.isNaN(n));
const raw = path.join(outDir, range.length === 2 ? `${NAME}_test.mp4` : `${NAME}_raw.mp4`);
const master = path.join(outDir, `${NAME}_1920x1080_master.mp4`);

console.log("rendering…");
const t0 = Date.now();
await renderMedia({
  composition, serveUrl, codec: "h264", outputLocation: raw,
  audioCodec: "aac", audioBitrate: "192k", videoBitrate: "7M",
  x264Preset: "medium", pixelFormat: "yuv420p", imageFormat: "jpeg",
  jpegQuality: 92, concurrency: 2,
  ...(range.length === 2 ? { frameRange: [range[0], range[1]] } : {}),
  ...browserOpts,
});
console.log(`rendered in ${((Date.now() - t0) / 1000).toFixed(0)}s → ${path.relative(root, raw)}`);

// pass akhir: JPEG keluar full-range → kembalikan ke tv; sekaligus loudness
// −14 LUFS / TP −1,5. Video di-encode sekali lagi karena range harus diubah.
execFileSync(FFMPEG, [
  "-y", "-i", raw,
  "-vf", "scale=in_range=full:out_range=tv,format=yuv420p",
  "-c:v", "libx264", "-crf", "20", "-preset", "medium", "-profile:v", "high",
  "-pix_fmt", "yuv420p",
  "-af", "loudnorm=I=-14:TP=-1.5:LRA=11",
  "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
  "-movflags", "+faststart", master,
]);

const info = probe(master);
const v = info.streams.find((s) => s.codec_type === "video");
const a = info.streams.find((s) => s.codec_type === "audio");
console.log("master     :", path.relative(root, master));
console.log(`video      : ${v.codec_name} ${v.width}x${v.height} ${v.pix_fmt} ${v.r_frame_rate}`);
console.log(`audio      : ${a.codec_name} ${a.sample_rate}Hz ${a.channels}ch`);
console.log(`duration   : ${Number(info.format.duration).toFixed(2)}s  ${(Number(info.format.size) / 1048576).toFixed(2)} MB`);
fs.writeFileSync(path.join(outDir, `${NAME}.report.json`), JSON.stringify({ browser: browser.version, ...info }, null, 2));
