/**
 * prepare-assets.mjs — copy the local, licensed-everywhere inputs into public/.
 *
 * Fonts come from ../../.build/fonts (populated by tools/fetch_fonts.sh) and
 * narration from ../audio. Neither set is committed: SIL OFL permits
 * redistribution but the brand rule is to link to the source, not vendor the files.
 */
import fs from "node:fs";
import path from "node:path";
import url from "node:url";
import { parseSrt } from "@remotion/captions";

const here = path.dirname(url.fileURLToPath(import.meta.url));
const root = path.resolve(here, "..");
const publicDir = path.join(root, "public");

const FONTS = [
  "space-grotesk-latin-300-normal.ttf",
  "space-grotesk-latin-500-normal.ttf",
  "space-grotesk-latin-700-normal.ttf",
  "inter-latin-500-normal.ttf",
  "inter-latin-600-normal.ttf",
];
const AUDIO = ["vo_01.wav", "vo_02.wav", "vo_03.wav", "signature.wav"];

const srcFonts = path.join(root, "..", "..", ".build", "fonts");
const srcAudio = path.join(root, "..", "audio");

fs.mkdirSync(path.join(publicDir, "fonts"), { recursive: true });
fs.mkdirSync(path.join(publicDir, "audio"), { recursive: true });

// brand geometry is generated from tools/brand.py — keep the film on the same marks
const brandJson = path.join(root, "src", "brand.json");
if (!fs.existsSync(brandJson)) {
  console.error("missing src/brand.json — run: python3 ../tools/export_brand_json.py");
  process.exit(1);
}

let missing = 0;
for (const f of FONTS) {
  const from = path.join(srcFonts, f);
  if (!fs.existsSync(from)) {
    console.error(`missing font: ${f} — run: bash tools/fetch_fonts.sh && python3 tools/fix_font_names.py`);
    missing++;
    continue;
  }
  fs.copyFileSync(from, path.join(publicDir, "fonts", f));
}
for (const f of AUDIO) {
  const from = path.join(srcAudio, f);
  if (!fs.existsSync(from)) {
    console.error(`missing audio: ${f}`);
    missing++;
    continue;
  }
  fs.copyFileSync(from, path.join(publicDir, "audio", f));
}
if (missing) process.exit(1);

// captions: SRT in, typed cue table out (single source of truth)
const srtPath = path.join(root, "..", "captions", "ODDCHAPTER_PILOT_001.id.srt");
if (!fs.existsSync(srtPath)) {
  console.error(`missing subtitles: ${srtPath}`);
  process.exit(1);
}
const { captions } = parseSrt({ input: fs.readFileSync(srtPath, "utf8") });
const cues = captions.map((c) => ({
  startMs: Math.round(c.startMs),
  endMs: Math.round(c.endMs),
  text: (c.text ?? "").replace(/\s+/g, " ").trim(),
}));
fs.writeFileSync(
  path.join(root, "src", "captions.generated.json"),
  JSON.stringify(cues, null, 2) + "\n",
);

console.log(`assets: ${FONTS.length} fonts + ${AUDIO.length} audio files + ${cues.length} caption cues`);
