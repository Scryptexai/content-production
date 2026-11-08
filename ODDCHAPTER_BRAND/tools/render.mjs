// SVG -> PNG rasteriser using @resvg/resvg-js (prebuilt binary, no system deps).
// Usage: node render.mjs in.svg out.png [width] [backgroundHex|none]
import { Resvg } from "@resvg/resvg-js";
import fs from "node:fs";
import path from "node:path";
import url from "node:url";

const __dirname = path.dirname(url.fileURLToPath(import.meta.url));
const FONTDIR = path.join(__dirname, "..", ".build", "fonts");
const fontFiles = fs.existsSync(FONTDIR)
  ? fs.readdirSync(FONTDIR).filter(f => f.endsWith(".ttf")).map(f => path.join(FONTDIR, f))
  : [];

const [inp, outp, w, bg] = process.argv.slice(2);
const svg = fs.readFileSync(inp, "utf8");
const opts = {
  fitTo: w ? { mode: "width", value: Number(w) } : { mode: "original" },
  font: { fontFiles, loadSystemFonts: false, defaultFontFamily: "Space Grotesk" },
  background: bg && bg !== "none" ? bg : undefined,
  shapeRendering: 2, textRendering: 2, imageRendering: 0,
};
const r = new Resvg(svg, opts);
const png = r.render();
fs.writeFileSync(outp, png.asPng());
const { width, height } = png;
console.log(`${outp}  ${width}x${height}  ${(png.asPng().length/1024).toFixed(1)}KB`);
