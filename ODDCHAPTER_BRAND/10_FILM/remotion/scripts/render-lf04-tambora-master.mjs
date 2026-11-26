/*
 * Render the authorized LF04 Tambora 16:9 master from the sealed LF04
 * composition. Visual frames are exclusively produced by @remotion/renderer;
 * FFmpeg is restricted to audio normalization, audio encode, faststart, and
 * stream-copying the already-rendered H.264 video into the delivery container.
 *
 *   node scripts/render-lf04-tambora-master.mjs --preflight
 *   node scripts/render-lf04-tambora-master.mjs
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
const work = path.join(repoRoot, "work", "tambora");
const output = path.join(work, "remotion-master");
const qc = path.join(work, "qc", "remotion-master");
const provenance = path.join(repoRoot, "ODDCHAPTER_BRAND", "11_CONTENT", "06_UPLOAD", "provenance");
const publicDir = path.join(remotionRoot, "public");
const sourceAudio = path.join(work, "vo_internal", "LF04_Tambora_voice-09_contiguous.wav");
const audioStatic = path.join(publicDir, "audio", "LF04", "lf04_tambora_voice-09.wav");
const inputDoc = path.join(remotionRoot, "src", "longform.lf04.generated.json");
const platesDir = path.join(publicDir, "lf04");
const entrypoint = "ODDCHAPTER_BRAND/10_FILM/remotion/src/index.ts";
const renderScript = "ODDCHAPTER_BRAND/10_FILM/remotion/scripts/render-lf04-tambora-master.mjs";
const renderFps = Number(process.env.LF04_RENDER_FPS || 30);
if (![6, 30].includes(renderFps)) throw new Error(`LF04_RENDER_FPS must be 6 or 30, got ${renderFps}`);
const compositionId = renderFps === 6
  ? "ODDCHAPTER-LONGFORM-LF04-TAMBORA-6FPS"
  : "ODDCHAPTER-LONGFORM-LF04-TAMBORA";
const targetLufs = -15;
const preflight = process.argv.includes("--preflight");
const assemble = process.argv.includes("--assemble");
const partFlag = process.argv.indexOf("--part");
const partNumber = partFlag === -1 ? null : Number(process.argv[partFlag + 1]);
const reuseRaw = process.argv.includes("--reuse-raw");
// Seven contiguous bounded jobs keep every Remotion invocation well below the
// sandbox command limit. Each frame is still rendered by Remotion; FFmpeg only
// concatenates the already-encoded H.264 elementary streams without re-encoding.
const PART_RANGES = [
  [0, 2890], [2891, 5781], [5782, 8672], [8673, 11563],
  [11564, 14454], [14455, 17345], [17346, 20230],
];
// PNG preserves range naturally but is prohibitively slow in this constrained
// renderer. JPEG capture is much faster; its full→TV range correction is made
// explicitly and disclosed below. Remotion remains the only frame renderer.
const imageFormat = process.env.LF04_IMAGE_FORMAT || "jpeg";
if (!["png", "jpeg"].includes(imageFormat)) throw new Error(`LF04_IMAGE_FORMAT invalid: ${imageFormat}`);
const requiresRangeCorrection = imageFormat === "jpeg";
const requiresTemporalExpansion = renderFps !== 30;
const requiresVideoPostprocess = requiresRangeCorrection || requiresTemporalExpansion;
const FFMPEG = ffmpegPath.path;
const FFPROBE = ffprobePath.path;

const assert = (condition, message) => {
  if (!condition) throw new Error(message);
};
const sha256 = (file) => crypto.createHash("sha256").update(fs.readFileSync(file)).digest("hex");
const run = (bin, args) => execFileSync(bin, args, { stdio: "inherit" });
const relative = (file) => path.relative(repoRoot, file).replaceAll(path.sep, "/");
const copy = (from, to) => {
  assert(fs.existsSync(from), `aset tidak ditemukan: ${relative(from)}`);
  fs.mkdirSync(path.dirname(to), { recursive: true });
  fs.copyFileSync(from, to);
  console.log("asset ←", relative(from));
};
const probe = (file, countFrames = false) => JSON.parse(execFileSync(FFPROBE, [
  "-v", "error",
  ...(countFrames ? ["-count_frames"] : []),
  "-show_entries", "format=duration,size,bit_rate:stream=codec_name,codec_type,width,height,r_frame_rate,avg_frame_rate,pix_fmt,sample_rate,channels,channel_layout,nb_read_frames,nb_frames",
  "-of", "json",
  file,
], { encoding: "utf8" }));
const stream = (info, type) => info.streams.find((item) => item.codec_type === type);
const ffmpegCapture = (args) => {
  const result = spawnSync(FFMPEG, args, { encoding: "utf8", maxBuffer: 32 * 1024 * 1024 });
  assert(!result.error, `ffmpeg gagal dimulai: ${result.error}`);
  assert(result.status === 0, `ffmpeg gagal:\n${result.stderr?.slice(-2800)}`);
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
], { maxBuffer: 64 * 1024 * 1024 })).digest("hex");
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
const treeHash = (dir) => {
  const files = fs.readdirSync(dir).filter((name) => name.endsWith(".svg")).sort();
  const hash = crypto.createHash("sha256");
  for (const name of files) {
    hash.update(name);
    hash.update(fs.readFileSync(path.join(dir, name)));
  }
  return { count: files.length, sha256: hash.digest("hex") };
};

const doc = JSON.parse(fs.readFileSync(inputDoc, "utf8"));
assert(doc.id === "LF04-TAMBORA-1815", `dokumen LF04 salah: ${doc.id}`);
assert(doc.totalFrames === 20231 && doc.fps === 30 && doc.width === 1920 && doc.height === 1080,
  `parameter LF04 salah: ${JSON.stringify({ fps: doc.fps, width: doc.width, height: doc.height, frames: doc.totalFrames })}`);
const expectedRenderFrames = renderFps === 30 ? doc.totalFrames : Math.round(doc.duration * renderFps);
// A 6-fps production frame expands to five 30-fps delivery frames. The
// authored document is 20,231 frames, while its 6-fps proxy is necessarily
// rounded to 4,046 frames (20,230 expanded frames). Clone the final authored
// Remotion frame once, rather than shortening the delivery by one frame.
const baseDeliveryFrames = renderFps === 30 ? expectedRenderFrames : expectedRenderFrames * 30 / renderFps;
const terminalFramePadding = doc.totalFrames - baseDeliveryFrames;
assert(Number.isInteger(baseDeliveryFrames) && Number.isInteger(terminalFramePadding)
  && terminalFramePadding >= 0 && terminalFramePadding <= 1,
  `6→30 delivery frame mapping invalid: ${JSON.stringify({ expectedRenderFrames, baseDeliveryFrames, terminalFramePadding })}`);
const expectedDeliveryFrames = doc.totalFrames;
assert(doc.segments.length === 22, `expected 22 diagram scenes, got ${doc.segments.length}`);
if (renderFps === 30) {
  assert(PART_RANGES[0][0] === 0 && PART_RANGES.at(-1)?.[1] === doc.totalFrames - 1,
    `part ranges do not cover LF04's first/final frame`);
  assert(PART_RANGES.every((range, index) => index === 0 || range[0] === PART_RANGES[index - 1][1] + 1)
    && PART_RANGES.reduce((total, [start, end]) => total + end - start + 1, 0) === doc.totalFrames,
    "part ranges overlap or omit LF04 frames");
} else {
  assert(partNumber === null && !assemble, "6-fps master uses one bounded full render, not 30-fps part assembly");
}
assert(!preflight || (!assemble && partNumber === null && !reuseRaw), "--preflight cannot be combined with --assemble, --part, or --reuse-raw");
assert(!assemble || partNumber === null, "--assemble cannot be combined with --part");
assert(!reuseRaw || (!assemble && partNumber === null), "--reuse-raw is only valid for the complete pre-rendered raw file");
assert(partNumber === null || (Number.isInteger(partNumber) && partNumber >= 1 && partNumber <= PART_RANGES.length),
  `--part must be 1 through ${PART_RANGES.length}`);
assert(doc.segments.every((item, i) => item.i === i && item.layout === "diagram" && item.captions.length > 0),
  "timing scene/caption LF04 tidak lengkap");
assert(fs.existsSync(sourceAudio), `VO tidak ada: ${relative(sourceAudio)}`);
assert(fs.existsSync(platesDir) && fs.readdirSync(platesDir).filter((name) => name.endsWith(".svg")).length === 67,
  "67 plate SVG LF04 tidak ditemukan");

fs.mkdirSync(output, { recursive: true });
fs.mkdirSync(qc, { recursive: true });
fs.mkdirSync(provenance, { recursive: true });
copy(sourceAudio, audioStatic);
assert(sha256(sourceAudio) === sha256(audioStatic), "salinan VO public tidak identik dengan sumber kontigu");

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
assert(comp.width === 1920 && comp.height === 1080 && comp.fps === renderFps && comp.durationInFrames === expectedRenderFrames,
  `komposisi LF04 tidak sesuai dokumen: ${JSON.stringify(comp)}`);
console.log(`composition: ${comp.id} · ${comp.width}x${comp.height} · ${comp.durationInFrames} frames`);

const stillTimes = {
  opening_layers: 36 / 30,
  evidence_chain: 1390 / 30,
  delayed_news: 3200 / 30,
  caldera: 6280 / 30,
  strata: 7470 / 30,
  doro_bente: 9570 / 30,
  artifacts: 11230 / 30,
  aerosol: 12760 / 30,
  attribution: 15710 / 30,
  likelihood: 16920 / 30,
  evidence_return: 19050 / 30,
  closing_question: 20080 / 30,
};
const stillFrames = Object.fromEntries(Object.entries(stillTimes)
  .map(([name, seconds]) => [name, Math.round(seconds * renderFps)]));
// Still QC is a separate, passed preflight. Per-part workers skip it so their
// bounded render budget is spent only on new frames.
if (partNumber === null && !assemble) {
  for (const [name, frame] of Object.entries(stillFrames)) {
    assert(frame >= 0 && frame < comp.durationInFrames, `frame QC di luar komposisi: ${name}=${frame}`);
    const dest = path.join(qc, `${name}.png`);
    await renderStill({ composition: comp, serveUrl, output: dest, frame, ...browserOptions });
    console.log("still:", relative(dest));
  }
}

if (preflight) {
  const report = {
    result: "pass",
    kind: "preflight",
    composition: comp.id,
    technical: { width: comp.width, height: comp.height, fps: comp.fps, duration_frames: comp.durationInFrames },
    voice: { source: relative(sourceAudio), sha256: sha256(sourceAudio) },
    svg_plates: treeHash(platesDir),
    frame_review: Object.keys(stillFrames).map((name) => relative(path.join(qc, `${name}.png`))),
  };
  fs.writeFileSync(path.join(qc, "preflight.json"), `${JSON.stringify(report, null, 2)}\n`);
  console.log("preflight pass:", relative(path.join(qc, "preflight.json")));
  process.exit(0);
}

const rawFull = path.join(output, "LF04_tambora_remotion_raw.mp4");
const part = partNumber === null ? null : {
  number: partNumber,
  start: PART_RANGES[partNumber - 1][0],
  end: PART_RANGES[partNumber - 1][1],
};
const raw = part
  ? path.join(output, `LF04_tambora_remotion_part-${String(part.number).padStart(2, "0")}-of-${PART_RANGES.length}.mp4`)
  : rawFull;
const final = path.join(output, "LF04_tambora_1920x1080_master.mp4");

if (assemble) {
  const parts = PART_RANGES.map((_, index) => path.join(output,
    `LF04_tambora_remotion_part-${String(index + 1).padStart(2, "0")}-of-${PART_RANGES.length}.mp4`));
  for (const [index, file] of parts.entries()) {
    assert(fs.existsSync(file), `part ${index + 1} belum ada: ${relative(file)}`);
    const info = probe(file, true);
    const video = stream(info, "video");
    const [start, end] = PART_RANGES[index];
    assert(Number(video?.nb_read_frames || video?.nb_frames) === end - start + 1,
      `jumlah frame part ${index + 1} salah`);
  }
  const list = path.join(output, "LF04_tambora_remotion_parts.concat.txt");
  fs.writeFileSync(list, parts.map((file) => `file '${file.replaceAll("'", "'\\\\''")}'`).join("\n") + "\n");
  console.log(`stream-copy concat ${parts.length} Remotion chunks…`);
  run(FFMPEG, ["-y", "-f", "concat", "-safe", "0", "-i", list, "-map", "0:v:0", "-c:v", "copy", "-an", "-movflags", "+faststart", rawFull]);
} else if (reuseRaw) {
  assert(fs.existsSync(raw), `--reuse-raw memerlukan hasil Remotion: ${relative(raw)}`);
  console.log(`reuse completed Remotion raw visual → ${relative(raw)}`);
} else {
  console.log(part
    ? `rendering Remotion part ${part.number}/${PART_RANGES.length}: frames ${part.start}–${part.end}…`
    : "rendering 22 original SVG information-design scenes…");
  const t0 = Date.now();
  await renderMedia({
    composition: comp,
    serveUrl,
    codec: "h264",
    audioCodec: "aac",
    audioBitrate: "192k",
    outputLocation: raw,
    pixelFormat: "yuv420p",
    crf: 19,
    x264Preset: "medium",
    imageFormat,
    ...(imageFormat === "jpeg" ? { jpegQuality: 88 } : {}),
    concurrency: Number(process.env.LF04_CONCURRENCY || 2),
    ...(part ? { frameRange: [part.start, part.end] } : {}),
    ...browserOptions,
  });
  console.log(`rendered in ${((Date.now() - t0) / 1000).toFixed(0)}s → ${relative(raw)}`);
}

const rawProbe = probe(raw, true);
const rawVideo = stream(rawProbe, "video");
const expectedRawPixFmt = imageFormat === "jpeg" ? "yuvj420p" : "yuv420p";
assert(rawVideo?.codec_name === "h264" && rawVideo.width === 1920 && rawVideo.height === 1080
  && rawVideo.r_frame_rate === `${renderFps}/1` && rawVideo.pix_fmt === expectedRawPixFmt,
  `hasil visual Remotion tidak sesuai: ${JSON.stringify(rawVideo)}`);
const rawFrames = Number(rawVideo.nb_read_frames || rawVideo.nb_frames);
if (part) {
  const expectedFrames = part.end - part.start + 1;
  assert(rawFrames === expectedFrames, `frame part ${part.number} salah: ${rawFrames} bukan ${expectedFrames}`);
  assert(Math.abs(Number(rawProbe.format.duration) - expectedFrames / doc.fps) <= 0.20,
    `durasi part ${part.number} salah: ${rawProbe.format.duration}`);
  const partReport = {
    result: "pass", kind: "remotion-frame-chunk", part: part.number,
    frame_range_inclusive: [part.start, part.end], frames: rawFrames,
    duration_seconds: Number(rawProbe.format.duration), output: relative(raw),
  };
  fs.writeFileSync(path.join(qc, `part-${String(part.number).padStart(2, "0")}.json`), `${JSON.stringify(partReport, null, 2)}\n`);
  console.log(`part ${part.number}/${PART_RANGES.length} pass: ${rawFrames} frames`);
  process.exit(0);
}
assert(rawFrames === expectedRenderFrames, `frame raw salah: ${rawFrames} bukan ${expectedRenderFrames}`);
assert(Math.abs(Number(rawProbe.format.duration) - doc.duration) <= 0.20,
  `durasi raw tidak sama dengan VO: ${rawProbe.format.duration} vs ${doc.duration}`);

const measureBefore = loudness(sourceAudio);
const loudnormFilter =
  `loudnorm=I=${targetLufs}:TP=-1.5:LRA=9:measured_I=${measureBefore.input_i}:measured_TP=${measureBefore.input_tp}` +
  `:measured_LRA=${measureBefore.input_lra}:measured_thresh=${measureBefore.input_thresh}:offset=${measureBefore.target_offset}:linear=true`;
run(FFMPEG, [
  "-y", "-i", raw, "-i", sourceAudio,
  "-map", "0:v:0", "-map", "1:a:0",
  ...(requiresVideoPostprocess
    ? ["-vf", [
        ...(requiresTemporalExpansion ? ["fps=30"] : []),
        ...(terminalFramePadding ? [`tpad=stop_mode=clone:stop=${terminalFramePadding}`] : []),
        ...(requiresRangeCorrection ? ["scale=in_range=full:out_range=tv", "format=yuv420p"] : []),
      ].join(","), "-frames:v", String(expectedDeliveryFrames), "-c:v", "libx264", "-crf", "19", "-preset", "medium", "-profile:v", "high", "-pix_fmt", "yuv420p"]
    : ["-c:v", "copy"]),
  "-af", loudnormFilter,
  "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2",
  "-movflags", "+faststart",
  final,
]);

const finalProbe = probe(final, true);
const finalVideo = stream(finalProbe, "video");
const finalAudio = stream(finalProbe, "audio");
assert(finalVideo?.codec_name === "h264" && finalVideo.width === 1920 && finalVideo.height === 1080 && finalVideo.r_frame_rate === "30/1" && finalVideo.pix_fmt === "yuv420p",
  `master final tidak sesuai: ${JSON.stringify(finalVideo)}`);
assert(finalAudio?.codec_name === "aac" && finalAudio.sample_rate === "48000" && finalAudio.channels === 2,
  `audio master tidak sesuai: ${JSON.stringify(finalAudio)}`);
const finalFrames = Number(finalVideo.nb_read_frames || finalVideo.nb_frames);
assert(finalFrames === expectedDeliveryFrames, `frame master salah: ${finalFrames} bukan ${expectedDeliveryFrames}`);
assert(Math.abs(Number(finalProbe.format.duration) - doc.duration) <= 0.20,
  `durasi master tidak sama dengan VO: ${finalProbe.format.duration} vs ${doc.duration}`);
ffmpegCapture(["-v", "error", "-i", final, "-f", "null", "-"]);

const rawVideoHash = encodedVideoHash(raw);
const finalVideoHash = encodedVideoHash(final);
if (!requiresVideoPostprocess) {
  assert(rawVideoHash === finalVideoHash,
    "visual final berubah setelah postprocess; video harus stream-copy langsung dari output Remotion");
}
const measureAfter = loudness(final);
const finalLufs = Number(measureAfter.input_i);
assert(Math.abs(finalLufs - targetLufs) <= 0.35, `loudness ${finalLufs} LUFS, target ${targetLufs} ±0.35 LUFS`);
const finalSilences = silenceEvents(final);
const terminalSilence = finalSilences.find((event) => Number(finalProbe.format.duration) - event.end <= 0.04) ?? null;
const interiorSilences = finalSilences.filter((event) => event !== terminalSilence);
const longInteriorSilences = interiorSilences.filter((event) => event.duration >= 1.25);
assert(longInteriorSilences.length === 0,
  `ditemukan hening internal ≥1.25 dtk: ${longInteriorSilences.map((event) => event.duration.toFixed(3)).join(", ")}`);
assert(!terminalSilence || terminalSilence.duration <= 1.25,
  `hening terminal ${terminalSilence.duration.toFixed(3)} dtk terlalu panjang`);

const qcReport = {
  result: "pass",
  rendered_by: "@remotion/renderer",
  review_method: "12 stills rendered by Remotion across all seven acts; decode, stream hash, timing, audio, loudness and silence checks passed",
  frame_review: Object.keys(stillFrames).map((name) => relative(path.join(qc, `${name}.png`))),
  raw_remotion_video_sha256: rawVideoHash,
  final_video_stream_sha256: finalVideoHash,
  visual_frame_provenance: "all raster frames originated in @remotion/renderer; the 6-fps production mode duplicates exact Remotion frames to 30 fps without interpolation, including one terminal-frame clone required to preserve the authored 20,231-frame delivery length; JPEG mode only corrects its declared full-range color encoding to delivery TV range",
  remotion_render_fps: renderFps,
  delivery_fps: 30,
  temporal_expansion: requiresTemporalExpansion
    ? `exact frame duplication 6fps→30fps; ${terminalFramePadding} terminal authored-frame clone; no interpolation`
    : "none",
  terminal_frame_padding: terminalFramePadding,
  image_format: imageFormat,
  full_to_tv_range_correction_applied: requiresRangeCorrection,
  video_stream_preserved_after_audio_container_postprocess: !requiresVideoPostprocess && rawVideoHash === finalVideoHash,
  audio_loudness_lufs: finalLufs,
  audio_true_peak_db: Number(measureAfter.input_tp),
  silence_qc: {
    threshold: "-50dB / 0.10s",
    long_interior_threshold_seconds: 1.25,
    terminal_silence_seconds: terminalSilence?.duration ?? 0,
    interior_silences_seconds: interiorSilences,
    long_interior_silences_seconds: longInteriorSilences,
  },
  technical: {
    width: finalVideo.width,
    height: finalVideo.height,
    fps: finalVideo.r_frame_rate,
    frames: finalFrames,
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
  episode: "LF04-tambora",
  authorization: "owner approved full production and unlisted distribution after QC",
  engine: "remotion",
  engine_version: "4.0.541",
  renderer: "@remotion/renderer",
  composition: compositionId,
  entrypoint,
  render_script: renderScript,
  input_document: relative(inputDoc),
  visual_output: relative(raw),
  master_output: relative(final),
  master_sha256: sha256(final),
  size_bytes: fs.statSync(final).size,
  assets: {
    voice: {
      voice_id: "voice-09",
      language: "id-ID",
      source_path: relative(sourceAudio),
      static_path: relative(audioStatic),
      sha256: sha256(sourceAudio),
      measured_duration_seconds: doc.duration,
      time_stretched: false,
      note: "Opening synthesized as two minimal TTS-safe paraphrase chunks after original wording was content-filtered; evidence meaning unchanged and documented in VISUAL_PROVENANCE.md.",
    },
    visual: {
      type: "original SVG / React data motion",
      source: "ODDCHAPTER_BRAND/10_FILM/remotion/public/lf04/",
      count: treeHash(platesDir).count,
      tree_sha256: treeHash(platesDir).sha256,
      external_footage_or_photo: false,
      ethical_boundary: "No victim imagery, photorealistic disaster reenactment, unverified archive scan, single casualty count, or global-uniform climate graphic.",
    },
  },
  browser: { engine: browser.engine, version: browser.version },
  post_render: {
    tool: "ffmpeg",
    allowed_operations: ["Remotion H.264 stream concat", "exact frame duplication to 30 fps", "single terminal-frame clone to authored delivery length", "JPEG full-to-TV-range delivery correction", "audio loudness normalization", "audio encode", "MP4 faststart", "container remux"],
    video_operation: requiresVideoPostprocess
      ? "Remotion output is re-encoded only for exact 6fps→30fps frame duplication, its one-frame terminal clone required for the authored delivery length, and/or JPEG full-to-TV-range conversion; no visual content is created outside Remotion and no interpolation is used"
      : "seven @remotion/renderer frame chunks concatenated by stream copy; final video stream-copied unchanged from that raw visual assembly",
  },
  qc: qcReport,
  publish_intent: "Owner-authorized YouTube upload only after this passed QC; visibility must remain unlisted.",
};
const manifestFile = path.join(provenance, "LF04-tambora-remotion-master.json");
fs.writeFileSync(manifestFile, `${JSON.stringify(manifest, null, 2)}\n`);
console.log("master:", relative(final));
console.log("sha256:", manifest.master_sha256);
console.log("loudness:", `${finalLufs} LUFS · ${measureAfter.input_tp} dBTP`);
console.log("provenance:", relative(manifestFile));
