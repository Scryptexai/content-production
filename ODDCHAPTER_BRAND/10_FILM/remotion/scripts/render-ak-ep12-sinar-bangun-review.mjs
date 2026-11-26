/*
 * Build the owner-authorized AK-EP12 local review master.
 *
 * Authorization is narrow: @remotion/renderer may render one local review file
 * and its QC/provenance. This script has no Drive, Zernio, queue, schedule, or
 * upload call. All visual frames come from Remotion; FFmpeg only stream-copies
 * that video during post-render audio/container QC.
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
const work = path.join(repoRoot, "work", "sinar-bangun");
const output = path.join(work, "remotion-review");
const qc = path.join(work, "qc", "remotion-review");
const provenance = path.join(repoRoot, "ODDCHAPTER_BRAND", "11_CONTENT", "06_UPLOAD", "provenance");
const publicDir = path.join(remotionRoot, "public");
const sourceAudio = path.join(work, "vo_internal", "AK-EP12_cut-C-final-contiguous.wav");
const audioStatic = path.join(publicDir, "audio", "ak-ep12-sinar-bangun-review.wav");
const entrypoint = "ODDCHAPTER_BRAND/10_FILM/remotion/src/index.ts";
const renderScript = "ODDCHAPTER_BRAND/10_FILM/remotion/scripts/render-ak-ep12-sinar-bangun-review.mjs";
const compositionId = "ODDCHAPTER-AK-EP12-SINAR-BANGUN-PREPROD";
const targetLufs = -15;
const reuseRaw = process.argv.includes("--reuse-raw");
const FFMPEG = ffmpegPath.path;
const FFPROBE = ffprobePath.path;

const assert = (condition, message) => {
  if (!condition) throw new Error(message);
};
const sha256 = (file) => crypto.createHash("sha256").update(fs.readFileSync(file)).digest("hex");
const run = (bin, args) => execFileSync(bin, args, { stdio: "inherit" });
const copy = (from, to) => {
  assert(fs.existsSync(from), `aset tidak ditemukan: ${path.relative(repoRoot, from)}`);
  fs.mkdirSync(path.dirname(to), { recursive: true });
  fs.copyFileSync(from, to);
  console.log("asset ←", path.relative(repoRoot, from));
};
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
const silenceEvents = (file) => {
  const text = ffmpegCapture([
    "-hide_banner", "-i", file, "-af", "silencedetect=n=-50dB:d=0.10", "-f", "null", "-",
  ]);
  const events = [];
  let start = null;
  for (const match of text.matchAll(/silence_start:\s*([0-9.]+)|silence_end:\s*([0-9.]+)\s*\|\s*silence_duration:\s*([0-9.]+)/g)) {
    if (match[1] !== undefined) {
      start = Number(match[1]);
    } else {
      assert(start !== null, `silencedetect tidak memiliki awal hening untuk ${path.basename(file)}`);
      events.push({ start, end: Number(match[2]), duration: Number(match[3]) });
      start = null;
    }
  }
  assert(start === null, `silencedetect tidak memiliki akhir hening untuk ${path.basename(file)}`);
  return events;
};

fs.mkdirSync(output, { recursive: true });
fs.mkdirSync(qc, { recursive: true });
fs.mkdirSync(provenance, { recursive: true });
copy(sourceAudio, audioStatic);
assert(sha256(sourceAudio) === sha256(audioStatic), "salinan VO static tidak identik dengan take C final");

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
assert(comp.width === 1080 && comp.height === 1920 && comp.fps === 30 && comp.durationInFrames === 1260,
  `komposisi bukan review 1080×1920 / 30 fps / 1260 frame: ${JSON.stringify(comp)}`);
console.log(`composition: ${comp.id} · ${comp.width}x${comp.height} · ${comp.durationInFrames} frames`);
const reviewDuration = comp.durationInFrames / comp.fps;
const sourceDuration = Number(probe(sourceAudio).format.duration);
const plannedVisualHold = reviewDuration - sourceDuration;
assert(Math.abs(plannedVisualHold - 0.64) <= 0.02,
  `hold visual tidak sesuai rencana 0.64 dtk: ${plannedVisualHold}`);
const reviewFrames = { hook: 75, route: 200, quay: 300, timeline: 420, wave: 550, counts: 770, turn: 960, manifest: 1065, loop: 1185, hold: 1248 };
const raw = path.join(output, "AK-EP12_sinar-bangun_remotion-review_raw.mp4");

if (reuseRaw) {
  assert(fs.existsSync(raw), "--reuse-raw memerlukan raw output Remotion yang sudah ada");
  for (const name of Object.keys(reviewFrames)) {
    assert(fs.existsSync(path.join(qc, `${name}.png`)), `--reuse-raw memerlukan still QC: ${name}.png`);
  }
  console.log("reuse raw/stills from the immediately preceding Remotion render for post-render QC only");
} else {
  for (const [name, frame] of Object.entries(reviewFrames)) {
    const dest = path.join(qc, `${name}.png`);
    await renderStill({ composition: comp, serveUrl, output: dest, frame, ...browserOptions });
    console.log("still:", path.relative(repoRoot, dest));
  }
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
}
const rawProbe = probe(raw);
const rawVideo = stream(rawProbe, "video");
const rawAudio = stream(rawProbe, "audio");
assert(rawVideo?.codec_name === "h264" && rawVideo.width === 1080 && rawVideo.height === 1920 && rawVideo.r_frame_rate === "30/1" && rawVideo.pix_fmt === "yuv420p",
  `hasil visual Remotion tidak sesuai: ${JSON.stringify(rawVideo)}`);
assert(rawAudio, "output Remotion tidak mengandung audio VO");
assert(Number(rawProbe.format.duration) >= 41.9 && Number(rawProbe.format.duration) <= 42.1,
  `durasi raw di luar 42 detik: ${rawProbe.format.duration}`);

const measureBefore = loudness(raw);
const loudnormFilter =
  `loudnorm=I=${targetLufs}:TP=-1.5:LRA=9:measured_I=${measureBefore.input_i}:measured_TP=${measureBefore.input_tp}` +
  `:measured_LRA=${measureBefore.input_lra}:measured_thresh=${measureBefore.input_thresh}:offset=${measureBefore.target_offset}:linear=true`;
const final = path.join(output, "AK-EP12_sinar-bangun_remotion-review.mp4");
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
assert(Number(finalProbe.format.duration) >= 41.9 && Number(finalProbe.format.duration) <= 42.1,
  `durasi review master di luar 42 detik: ${finalProbe.format.duration}`);

const rawVideoHash = encodedVideoHash(raw);
const finalVideoHash = encodedVideoHash(final);
assert(rawVideoHash === finalVideoHash, "video final berubah setelah post-processing; seharusnya stream-copy dari output Remotion");
const measureAfter = loudness(final);
const finalLufs = Number(measureAfter.input_i);
assert(Math.abs(finalLufs - targetLufs) <= 0.3, `loudness ${finalLufs} LUFS, target ${targetLufs} ±0.3 LUFS`);
const sourceSilences = silenceEvents(sourceAudio);
const sourceTerminalSilence = sourceSilences.find((event) => sourceDuration - event.end <= 0.02);
assert(sourceTerminalSilence, "VO sumber tidak memiliki event hening terminal yang dapat diaudit");
const finalSilences = silenceEvents(final);
const finalDuration = Number(finalProbe.format.duration);
const terminalSilence = finalSilences.find((event) => finalDuration - event.end <= 0.02);
assert(terminalSilence, "master tidak memiliki event hening terminal yang dapat diaudit");
const interiorSilences = finalSilences.filter((event) => event !== terminalSilence);
const longInteriorSilences = interiorSilences.filter((event) => event.duration >= 0.75);
assert(longInteriorSilences.length === 0,
  `ditemukan hening internal panjang: ${longInteriorSilences.map((event) => event.duration).join(", ")} detik`);
const maximumAllowedTerminalSilence = sourceTerminalSilence.duration + plannedVisualHold + 0.15;
assert(terminalSilence.duration <= maximumAllowedTerminalSilence,
  `hening terminal ${terminalSilence.duration} dtk melebihi VO-tail + hold yang diizinkan ${maximumAllowedTerminalSilence} dtk`);

const qcReport = {
  result: "pass",
  rendered_by: "@remotion/renderer",
  frame_review: Object.keys(reviewFrames)
    .map((name) => `work/sinar-bangun/qc/remotion-review/${name}.png`),
  raw_remotion_video_sha256: rawVideoHash,
  final_video_stream_sha256: finalVideoHash,
  video_stream_preserved_after_audio_container_postprocess: rawVideoHash === finalVideoHash,
  audio_loudness_lufs: finalLufs,
  audio_true_peak_db: Number(measureAfter.input_tp),
  silence_qc: {
    source_terminal_silence_seconds: sourceTerminalSilence.duration,
    planned_visual_hold_seconds: plannedVisualHold,
    terminal_silence_seconds: terminalSilence.duration,
    maximum_allowed_terminal_silence_seconds: maximumAllowedTerminalSilence,
    interior_silences_seconds: interiorSilences,
    long_interior_silences_seconds: longInteriorSilences,
  },
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
  episode: "AK-EP12-sinar-bangun-remotion-review",
  authorization: "owner approved one local review render only; no distribution",
  engine: "remotion",
  engine_version: "4.0.541",
  renderer: "@remotion/renderer",
  composition: compositionId,
  entrypoint,
  render_script: renderScript,
  visual_output: "work/sinar-bangun/remotion-review/AK-EP12_sinar-bangun_remotion-review_raw.mp4",
  master_output: "work/sinar-bangun/remotion-review/AK-EP12_sinar-bangun_remotion-review.mp4",
  master_sha256: sha256(final),
  size_bytes: fs.statSync(final).size,
  assets: {
    voice: {
      source_path: "work/sinar-bangun/vo_internal/AK-EP12_cut-C-final-contiguous.wav",
      static_path: "ODDCHAPTER_BRAND/10_FILM/remotion/public/audio/ak-ep12-sinar-bangun-review.wav",
      sha256: sha256(sourceAudio),
      language: "id-ID",
      measured_duration_seconds: 41.36,
    },
    visual: {
      type: "native React/SVG/CSS data motion",
      source: "ODDCHAPTER_BRAND/10_FILM/remotion/src/scenes/SinarBangunPreprod.tsx",
      external_footage_or_photo: false,
    },
  },
  browser: { engine: browser.engine, version: browser.version },
  post_render: {
    tool: "ffmpeg",
    allowed_operations: ["audio loudness normalization", "audio encode", "MP4 faststart", "container remux"],
    video_operation: "stream copy only; verified unchanged against Remotion raw output",
  },
  qc: qcReport,
  publish_intent: "review-only; do not upload, queue, schedule, transfer to Drive, unlist, delete, or alter any live video",
};
const manifestFile = path.join(provenance, "AK-EP12-sinar-bangun-remotion-review.json");
fs.writeFileSync(manifestFile, `${JSON.stringify(manifest, null, 2)}\n`);
console.log("review master:", path.relative(repoRoot, final));
console.log("sha256:", manifest.master_sha256);
console.log("loudness:", `${finalLufs} LUFS · ${measureAfter.input_tp} dBTP`);
console.log("manifest:", path.relative(repoRoot, manifestFile));
