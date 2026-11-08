/**
 * validate.mjs — inspect the delivered file with ffprobe and (optionally) measure
 * loudness with ffmpeg. Fails loudly; never prints "OK" for something unmeasured.
 */
import path from "node:path";
import url from "node:url";
import { execFileSync } from "node:child_process";
import ffprobeInstaller from "@ffprobe-installer/ffprobe";
import ffmpegInstaller from "@ffmpeg-installer/ffmpeg";

const here = path.dirname(url.fileURLToPath(import.meta.url));
const root = path.resolve(here, "..");
const target = process.argv[2] ?? path.join(root, "output", "ODDCHAPTER_PILOT_001.mp4");

const FFPROBE = ffprobeInstaller.path;
const FFMPEG = ffmpegInstaller.path;

const json = JSON.parse(
  execFileSync(
    FFPROBE,
    [
      "-v", "error",
      "-show_entries",
      "format=filename,format_name,duration,size,bit_rate:stream=index,codec_name,codec_type,width,height,r_frame_rate,avg_frame_rate,pix_fmt,profile,level,sample_rate,channels,channel_layout,duration,nb_frames",
      "-of", "json",
      target,
    ],
    { encoding: "utf8" },
  ),
);

const v = json.streams.find((s) => s.codec_type === "video");
const a = json.streams.find((s) => s.codec_type === "audio");
const checks = [];
const check = (name, ok, detail) => checks.push({ name, ok, detail });

check("container", json.format.format_name.includes("mp4"), json.format.format_name);
check("video codec", v?.codec_name === "h264", v?.codec_name);
check("dimensions", v?.width === 1080 && v?.height === 1920, `${v?.width}x${v?.height}`);
check("pixel format", v?.pix_fmt === "yuv420p", v?.pix_fmt);
const [fpsNum, fpsDen] = (v?.avg_frame_rate ?? "0/1").split("/").map(Number);
check("frame rate 30 fps", Math.abs(fpsNum / fpsDen - 30) < 0.01, v?.avg_frame_rate);
check("audio stream", a?.codec_name === "aac", `${a?.codec_name} ${a?.sample_rate}Hz ${a?.channels}ch`);
check("audio 48k", Number(a?.sample_rate) === 48000, a?.sample_rate);
check("duration > 20 s", Number(json.format.duration) > 20, `${Number(json.format.duration).toFixed(2)}s`);

const stderr = execFileSync("sh", ["-c", `"${FFMPEG}" -hide_banner -i "${target}" -af loudnorm=print_format=json -f null - 2>&1 || true`], {
  encoding: "utf8",
});
const m = stderr.match(/\{[^{}]*"input_i"[^{}]*\}/s);
const lufs = m ? Number(JSON.parse(m[0]).input_i) : NaN;
const tp = m ? Number(JSON.parse(m[0]).input_tp) : NaN;
check("loudness −14 ±1 LUFS", Math.abs(lufs + 14) <= 1, `${lufs} LUFS`);
check("true peak ≤ −1 dBTP", tp <= -1, `${tp} dBTP`);

let failed = 0;
console.log(`\n${path.relative(root, target)}`);
console.log(`  ${json.format.format_name} · ${(Number(json.format.size) / 1e6).toFixed(1)} MB · ${Number(json.format.duration).toFixed(2)} s\n`);
for (const c of checks) {
  if (!c.ok) failed++;
  console.log(`  ${c.ok ? "PASS" : "FAIL"}  ${c.name.padEnd(26)} ${c.detail ?? ""}`);
}
console.log(`\n${checks.length - failed}/${checks.length} checks passed`);
process.exit(failed ? 1 : 0);
