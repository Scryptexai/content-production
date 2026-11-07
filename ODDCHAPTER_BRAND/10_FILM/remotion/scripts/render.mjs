/**
 * render.mjs — the production path.
 *
 *   bundle → static frame → test video (validated) → full pilot → ffmpeg master
 *
 * The browser is @sparticuz/chromium, resolved in scripts/chromium.mjs and handed
 * to Remotion through `browserExecutable`. Nothing renders until the 1-frame and
 * 3-second tests have passed and been probed with ffprobe.
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

const here = path.dirname(url.fileURLToPath(import.meta.url));
const root = path.resolve(here, "..");
const out = path.join(root, "output");
fs.mkdirSync(out, { recursive: true });

const FFMPEG = ffmpegPath.path;
const FFPROBE = ffprobePath.path;

const probe = (file) => {
  const raw = execFileSync(
    FFPROBE,
    [
      "-v", "error",
      "-show_entries", "format=duration,size,bit_rate:stream=codec_name,codec_type,width,height,r_frame_rate,pix_fmt,sample_rate,channels,duration",
      "-of", "json",
      file,
    ],
    { encoding: "utf8" },
  );
  return JSON.parse(raw);
};

const assert = (cond, msg) => {
  if (!cond) throw new Error(msg);
};

const main = async () => {
  const browser = await resolveChromium();
  console.log(`browser     : ${browser.engine} ${browser.version}`);
  console.log(`executable  : ${browser.executablePath}`);

  console.log("bundling…");
  const serveUrl = await bundle({
    entryPoint: path.join(root, "src", "index.ts"),
    publicDir: path.join(root, "public"),
  });

  const browserOpts = { browserExecutable: browser.executablePath, chromiumOptions: { gl: "swangle" }, args: chromiumArgs };

  // ---------------------------------------------------------------- 1. still
  const frameComp = await selectComposition({ serveUrl, id: "TEST-FRAME", ...browserOpts });
  const stillPath = path.join(out, "test_still.png");
  await renderStill({ composition: frameComp, serveUrl, output: stillPath, frame: 0, ...browserOpts });
  console.log(`still       : ${path.relative(root, stillPath)}`);

  // ------------------------------------------------- 2. transitions test (only)
  const transComp = await selectComposition({ serveUrl, id: "TEST-TRANSITION", ...browserOpts });
  const transPath = path.join(out, "test_transition.mp4");
  await renderMedia({
    composition: transComp,
    serveUrl,
    codec: "h264",
    outputLocation: transPath,
    pixelFormat: "yuv420p",
    crf: 20,
    ...browserOpts,
  });
  const tTrans = probe(transPath);
  console.log(`transition  : ${tTrans.streams[0].width}x${tTrans.streams[0].height} · ${Number(tTrans.format.duration).toFixed(2)}s`);

  // ------------------------------------------------------- 3. test video first
  const testComp = await selectComposition({ serveUrl, id: "TEST-MOTION", ...browserOpts });
  const testPath = path.join(out, "test_motion.mp4");
  await renderMedia({
    composition: testComp,
    serveUrl,
    codec: "h264",
    outputLocation: testPath,
    pixelFormat: "yuv420p",
    crf: 18,
    imageFormat: "png",
    ...browserOpts,
  });
  const t = probe(testPath);
  const tVideo = t.streams.find((s) => s.codec_type === "video");
  assert(tVideo.width === 1080 && tVideo.height === 1920, `test video is ${tVideo.width}x${tVideo.height}`);
  assert(Number(t.format.duration) > 2.5, `test video too short: ${t.format.duration}`);
  console.log(`test video  : 1080x1920 · ${Number(t.format.duration).toFixed(2)}s · OK`);

  // ------------------------------------------------------- 4. full pilot × 2
  // Two cuts of the same timeline: clean, and with burned-in Indonesian captions
  // (the captioned cut is what goes to Shorts / Reels / TikTok).
  const CUTS = [
    { id: "ODDCHAPTER-PILOT-001", file: "ODDCHAPTER_PILOT_001.mp4" },
    { id: "ODDCHAPTER-PILOT-001-CAPTIONS", file: "ODDCHAPTER_PILOT_001_CAPTIONS.mp4" },
  ];

  const films = [];
  for (const cut of CUTS) {
    const film = await selectComposition({ serveUrl, id: cut.id, ...browserOpts });
    const rawVideo = path.join(out, `raw_${cut.id}.mp4`);
    console.log(`rendering   : ${cut.id} — ${film.durationInFrames} frames @ ${film.fps} fps …`);
    let lastPct = -1;
    await renderMedia({
      composition: film,
      serveUrl,
      codec: "h264",
      outputLocation: rawVideo,
      pixelFormat: "yuv420p",
      crf: 18,
      imageFormat: "png",
      muted: false,
      onProgress: ({ progress }) => {
        const pct = Math.floor(progress * 100);
        if (pct !== lastPct && pct % 20 === 0) {
          lastPct = pct;
          console.log(`  …${pct}%`);
        }
      },
      ...browserOpts,
    });

    const stderr = execFileSync(
      "sh",
      ["-c", `"${FFMPEG}" -hide_banner -i "${rawVideo}" -af loudnorm=I=-14:TP=-1.5:LRA=7:print_format=json -f null - 2>&1 || true`],
      { encoding: "utf8" },
    );
    const m = stderr.match(/\{[^{}]*"input_i"[^{}]*\}/s);
    if (!m) throw new Error("loudnorm measurement failed:\n" + stderr.slice(-1200));
    const measured = JSON.parse(m[0]);

    const ln =
      `loudnorm=I=-14:TP=-1.5:LRA=7:measured_I=${measured.input_i}:measured_TP=${measured.input_tp}` +
      `:measured_LRA=${measured.input_lra}:measured_thresh=${measured.input_thresh}` +
      `:offset=${measured.target_offset}:linear=true`;

    const finalPath = path.join(out, cut.file);
    execFileSync(FFMPEG, [
      "-y", "-hide_banner", "-loglevel", "error",
      "-i", rawVideo,
      "-af", `${ln},aresample=48000`,
      "-c:v", "copy",
      "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2",
      "-movflags", "+faststart",
      finalPath,
    ]);
    fs.unlinkSync(rawVideo);
    films.push({ finalPath, inputLufs: measured.input_i });
    console.log(`mastered    : ${path.basename(finalPath)} (input ${measured.input_i} LUFS)`);
  }

  return { films, browser };
}

main()
  .then(({ films, browser }) => {
    const report = { cuts: [], browser: { engine: browser.engine, version: browser.version, executablePath: browser.executablePath } };
    for (const f of films) {
      const info = probe(f.finalPath);
      const v = info.streams.find((s) => s.codec_type === "video");
      const a = info.streams.find((s) => s.codec_type === "audio");
      const entry = {
        file: path.relative(root, f.finalPath),
        bytes: Number(info.format.size),
        duration: Number(info.format.duration),
        inputLufs: f.inputLufs,
        video: { codec: v.codec_name, width: v.width, height: v.height, fps: v.r_frame_rate, pix_fmt: v.pix_fmt },
        audio: { codec: a.codec_name, sample_rate: a.sample_rate, channels: a.channels },
      };
      report.cuts.push(entry);
      console.log(`\nfinal       : ${entry.file}`);
      console.log(`              ${entry.video.width}x${entry.video.height} ${entry.video.codec} ${entry.video.fps} fps · ` +
        `${entry.audio.codec} ${entry.audio.sample_rate} Hz ${entry.audio.channels}ch · ` +
        `${entry.duration.toFixed(2)}s · ${(entry.bytes / 1e6).toFixed(1)} MB`);
    }
    fs.writeFileSync(path.join(out, "render-report.json"), JSON.stringify(report, null, 2));
    console.log(`rendered by : ${browser.engine} ${browser.version}`);
  })
  .catch((err) => {
    console.error("\nRENDER FAILED:", err && err.stack ? err.stack : err);
    process.exit(1);
  });
