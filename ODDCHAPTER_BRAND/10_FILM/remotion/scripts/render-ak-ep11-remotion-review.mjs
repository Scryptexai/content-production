/*
 * Build a non-publish review master for the Simeulue remediation.
 *
 * All visual frames are rendered by @remotion/renderer. FFmpeg is used only
 * after that render: it stream-copies the Remotion video unchanged, normalizes
 * audio, and faststarts the MP4. This script never queues or uploads a video.
 */
import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";
import url from "node:url";
import { execFileSync, spawnSync } from "node:child_process";
import { bundle } from "@remotion/bundler";
import { renderMedia, renderStill, selectComposition } from "@remotion/renderer";
import ffmpegPath from "@ffmpeg-installer/ffmpeg";
import ffprobePath from "@ffprobe-installer/ffprobe";
import { chromiumArgs, resolveChromium } from "./chromium.mjs";

const here = path.dirname(url.fileURLToPath(import.meta.url));
const remotionRoot = path.resolve(here, "..");
const repoRoot = path.resolve(remotionRoot, "..", "..", "..");
const work = path.join(repoRoot, "work", "smong-simeulue");
const publicDir = path.join(remotionRoot, "public");
const output = path.join(work, "remotion-review");
const qc = path.join(work, "qc", "remotion-review");
const provenance = path.join(repoRoot, "ODDCHAPTER_BRAND", "11_CONTENT", "06_UPLOAD", "provenance");
const FFMPEG = ffmpegPath.path;
const FFPROBE = ffprobePath.path;
const compositionId = "ODDCHAPTER-AK-EP11-REMOTION-REVIEW";
const entrypoint = "ODDCHAPTER_BRAND/10_FILM/remotion/src/index.ts";
const renderScript = "ODDCHAPTER_BRAND/10_FILM/remotion/scripts/render-ak-ep11-remotion-review.mjs";
const mapAsset = path.join(publicDir, "ak-ep11", "simeulue_topography_cc-by-sa-3.png");
const audioSource = path.join(work, "audio", "master.wav");
const audioStatic = path.join(publicDir, "audio", "ak-ep11-smong-review.wav");
const targetLufs = -15;

const assert = (condition, message) => {
  if (!condition) throw new Error(message);
};
const sha256 = (file) => crypto.createHash("sha256").update(fs.readFileSync(file)).digest("hex");
const copy = (from, to) => {
  assert(fs.existsSync(from), `asset tidak ditemukan: ${path.relative(repoRoot, from)}`);
  fs.mkdirSync(path.dirname(to), { recursive: true });
  fs.copyFileSync(from, to);
  console.log("asset ←", path.relative(repoRoot, from));
};
const run = (bin, args) => execFileSync(bin, args, { stdio: "inherit" });
const probe = (file) => JSON.parse(execFileSync(FFPROBE, [
  "-v", "error",
  "-show_entries", "format=duration,size,bit_rate:stream=codec_name,codec_type,width,height,r_frame_rate,pix_fmt,sample_rate,channels",
  "-of", "json",
  file,
], { encoding: "utf8" }));
const stream = (info, type) => info.streams.find((item) => item.codec_type === type);

const ffmpegCapture = (args) => {
  const result = spawnSync(FFMPEG, args, { encoding: "utf8", maxBuffer: 16 * 1024 * 1024 });
  assert(!result.error, `ffmpeg gagal dimulai: ${result.error}`);
  assert(result.status === 0, `ffmpeg gagal:\n${result.stderr?.slice(-1800)}`);
  return `${result.stdout || ""}${result.stderr || ""}`;
};
const loudness = (file) => {
  const text = ffmpegCapture([
    "-hide_banner", "-i", file,
    "-af", `loudnorm=I=${targetLufs}:TP=-1.5:LRA=9:print_format=json`,
    "-f", "null", "-",
  ]);
  const match = text.match(/\{[^{}]*"input_i"[^{}]*\}/s);
  assert(match, `pengukuran loudnorm tidak terbaca untuk ${path.basename(file)}`);
  return JSON.parse(match[0]);
};
const encodedVideoHash = (file) => crypto.createHash("sha256").update(execFileSync(FFMPEG, [
  "-v", "error", "-i", file, "-map", "0:v:0", "-c:v", "copy", "-f", "h264", "-",
], { maxBuffer: 16 * 1024 * 1024 })).digest("hex");
const silenceDurations = (file) => {
  const text = ffmpegCapture([
    "-hide_banner", "-i", file, "-af", "silencedetect=n=-50dB:d=0.75", "-f", "null", "-",
  ]);
  return [...text.matchAll(/silence_duration:\s*([0-9.]+)/g)].map((match) => Number(match[1]));
};

fs.mkdirSync(output, { recursive: true });
fs.mkdirSync(qc, { recursive: true });
fs.mkdirSync(provenance, { recursive: true });
assert(fs.existsSync(mapAsset), `peta berlisensi harus tersedia di repo: ${path.relative(repoRoot, mapAsset)}`);
copy(audioSource, audioStatic);

const browser = await resolveChromium();
const browserOptions = {
  browserExecutable: browser.executablePath,
  chromiumOptions: { gl: "swangle" },
  args: chromiumArgs,
};
console.log("browser:", browser.version);
console.log("bundle:", entrypoint);
const serveUrl = await bundle({ entryPoint: path.join(repoRoot, entrypoint), publicDir });
const comp = await selectComposition({ serveUrl, id: compositionId, ...browserOptions });
assert(comp.width === 1080 && comp.height === 1920 && comp.fps === 30 && comp.durationInFrames === 1065,
  `komposisi tidak sesuai kontrak 1080×1920 / 30 fps / 1065 frame: ${JSON.stringify(comp)}`);
console.log(`composition: ${comp.id} · ${comp.width}x${comp.height} · ${comp.durationInFrames} frames`);

for (const [name, frame] of Object.entries({ hook: 18, rule: 345, time: 470, langi: 720, cta: 1005 })) {
  const dest = path.join(qc, `${name}.png`);
  await renderStill({ composition: comp, serveUrl, output: dest, frame, ...browserOptions });
  console.log("still:", path.relative(repoRoot, dest));
}

const raw = path.join(output, "AK-EP11_smong-simeulue_remotion-review_raw.mp4");
await renderMedia({
  composition: comp,
  serveUrl,
  codec: "h264",
  outputLocation: raw,
  pixelFormat: "yuv420p",
  crf: 18,
  imageFormat: "png",
  ...browserOptions,
});
const rawProbe = probe(raw);
const rawVideo = stream(rawProbe, "video");
assert(rawVideo?.codec_name === "h264" && rawVideo.width === 1080 && rawVideo.height === 1920 && rawVideo.r_frame_rate === "30/1" && rawVideo.pix_fmt === "yuv420p",
  `hasil visual Remotion tidak sesuai: ${JSON.stringify(rawVideo)}`);

const measureBefore = loudness(raw);
const loudnormFilter =
  `loudnorm=I=${targetLufs}:TP=-1.5:LRA=9:measured_I=${measureBefore.input_i}:measured_TP=${measureBefore.input_tp}` +
  `:measured_LRA=${measureBefore.input_lra}:measured_thresh=${measureBefore.input_thresh}:offset=${measureBefore.target_offset}:linear=true`;
const final = path.join(output, "AK-EP11_smong-simeulue_remotion-review.mp4");
run(FFMPEG, [
  "-y", "-i", raw,
  "-map", "0:v:0", "-map", "0:a:0",
  "-c:v", "copy",
  "-af", `${loudnormFilter},aresample=48000`,
  "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2",
  "-movflags", "+faststart",
  final,
]);

const finalProbe = probe(final);
const finalVideo = stream(finalProbe, "video");
const finalAudio = stream(finalProbe, "audio");
assert(finalVideo?.codec_name === "h264" && finalVideo.width === 1080 && finalVideo.height === 1920 && finalVideo.r_frame_rate === "30/1" && finalVideo.pix_fmt === "yuv420p",
  `master video tidak sesuai: ${JSON.stringify(finalVideo)}`);
assert(finalAudio?.codec_name === "aac" && finalAudio.sample_rate === "48000" && finalAudio.channels === 2,
  `master audio tidak sesuai: ${JSON.stringify(finalAudio)}`);
assert(Number(finalProbe.format.duration) > 35 && Number(finalProbe.format.duration) < 36,
  `durasi master di luar rentang: ${finalProbe.format.duration}`);

const rawVideoHash = encodedVideoHash(raw);
const finalVideoHash = encodedVideoHash(final);
assert(rawVideoHash === finalVideoHash, "video final berubah setelah post-processing; seharusnya stream-copy dari output Remotion");
const measureAfter = loudness(final);
const finalLufs = Number(measureAfter.input_i);
assert(Math.abs(finalLufs - targetLufs) <= 0.3, `loudness ${finalLufs} LUFS, target ${targetLufs} ±0.3 LUFS`);
const silences = silenceDurations(final);
assert(silences.every((duration) => duration < 0.75), `ditemukan hening panjang: ${silences.join(", ")} detik`);

const qcReport = {
  result: "pass",
  frame_review: ["hook", "rule", "time", "langi", "cta"].map((name) => `work/smong-simeulue/qc/remotion-review/${name}.png`),
  raw_remotion_video_sha256: rawVideoHash,
  final_video_stream_sha256: finalVideoHash,
  video_stream_preserved_after_audio_container_postprocess: rawVideoHash === finalVideoHash,
  audio_loudness_lufs: finalLufs,
  audio_true_peak_db: Number(measureAfter.input_tp),
  long_silences_seconds: silences,
  technical: {
    width: finalVideo.width,
    height: finalVideo.height,
    fps: finalVideo.r_frame_rate,
    pixel_format: finalVideo.pix_fmt,
    video_codec: finalVideo.codec_name,
    audio_codec: finalAudio.codec_name,
    audio_sample_rate: finalAudio.sample_rate,
    audio_channels: finalAudio.channels,
    duration_seconds: Number(finalProbe.format.duration),
  },
};
fs.writeFileSync(path.join(qc, "qc-report.json"), `${JSON.stringify(qcReport, null, 2)}\n`);

const manifest = {
  episode: "AK-EP11-remotion-review",
  engine: "remotion",
  engine_version: "4.0.541",
  renderer: "@remotion/renderer",
  composition: compositionId,
  entrypoint,
  render_script: renderScript,
  visual_output: "work/smong-simeulue/remotion-review/AK-EP11_smong-simeulue_remotion-review_raw.mp4",
  master_output: "work/smong-simeulue/remotion-review/AK-EP11_smong-simeulue_remotion-review.mp4",
  master_sha256: sha256(final),
  size_bytes: fs.statSync(final).size,
  assets: {
    map: {
      path: "ODDCHAPTER_BRAND/10_FILM/remotion/public/ak-ep11/simeulue_topography_cc-by-sa-3.png",
      sha256: sha256(mapAsset),
      attribution: "Sadalmelik, Simeulue Topography, CC BY-SA 3.0",
    },
    audio: {
      source_path: "work/smong-simeulue/audio/master.wav",
      sha256: sha256(audioSource),
    },
  },
  browser: { engine: browser.engine, version: browser.version },
  post_render: {
    tool: "ffmpeg",
    allowed_operations: ["audio loudness normalization", "audio encode", "MP4 faststart", "container remux"],
    video_operation: "stream copy only; verified unchanged against Remotion raw output",
  },
  qc: qcReport,
  probe: finalProbe,
  publish_intent: "review-only; do not upload, queue, schedule, unlist, or delete the live video",
};
const manifestFile = path.join(provenance, "AK-EP11-remotion-review.json");
fs.writeFileSync(manifestFile, `${JSON.stringify(manifest, null, 2)}\n`);
console.log("master:", path.relative(repoRoot, final));
console.log("sha256:", manifest.master_sha256);
console.log("loudness:", `${finalLufs} LUFS · ${measureAfter.input_tp} dBTP`);
console.log("manifest:", path.relative(repoRoot, manifestFile));
