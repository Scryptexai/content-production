/**
 * chromium-test.mjs — independent proof that the Sparticuz Chromium binary works
 * before any of it is wired into Remotion.
 *
 * Steps: load binary → launch headless → open a local HTML page → screenshot →
 * verify the screenshot is a real image → close → report path + version.
 */
import fs from "node:fs";
import path from "node:path";
import url from "node:url";
import puppeteer from "puppeteer-core";
import { chromiumArgs, resolveChromium } from "./chromium.mjs";

const here = path.dirname(url.fileURLToPath(import.meta.url));
const outDir = path.join(here, "..", "output", "chromium-test");
fs.mkdirSync(outDir, { recursive: true });

const log = (...a) => console.log(...a);
let browser;

try {
  // 1 — load the binary (libraries from the bundled al2023 layer)
  const info = await resolveChromium();
  const execPath = info.executablePath;
  log("1. binary path      :", execPath);
  log("   exists           :", fs.existsSync(execPath));
  log("   size (MB)        :", (fs.statSync(execPath).size / 1e6).toFixed(1));
  log("   reported version :", info.version);
  log("   lib dir          :", info.libDir);

  // 2 — launch headless
  const t0 = Date.now();
  browser = await puppeteer.launch({
    args: chromiumArgs,
    defaultViewport: { width: 1080, height: 1920, deviceScaleFactor: 1 },
    executablePath: execPath,
    headless: "shell",
  });
  log("2. launched         :", `${Date.now() - t0} ms`);
  log("   browser version  :", await browser.version());

  // 3 — a real local page (file://, no network)
  const page = await browser.newPage();
  const html = path.join(outDir, "probe.html");
  fs.writeFileSync(
    html,
    `<!doctype html><html><head><meta charset="utf-8"><style>
      html,body{margin:0;background:#17191D;color:#F4F0E8;font-family:monospace}
      .wrap{display:flex;flex-direction:column;align-items:center;justify-content:center;height:1920px;gap:24px}
      h1{font-family:sans-serif;font-size:96px;letter-spacing:.02em;margin:0}
      .bar{width:520px;height:8px;background:#F26A3D}
      p{color:#A7B0A1;font-size:28px;letter-spacing:.18em}
    </style></head><body><div class="wrap">
      <div class="bar"></div><h1>ODDCHAPTER</h1>
      <p>CHROMIUM RENDER PROBE · 1080×1920</p></div></body></html>`,
  );
  const t1 = Date.now();
  await page.goto(url.pathToFileURL(html).href, { waitUntil: "load" });
  log("3. loaded local page:", `${Date.now() - t1} ms`, "|", await page.title() || "(untitled)");

  // 4 — render a test image
  const shot = path.join(outDir, "probe_1080x1920.png");
  await page.screenshot({ path: shot, type: "png" });
  const b = fs.readFileSync(shot);
  const w = b.readUInt32BE(16);
  const h = b.readUInt32BE(20);
  log("4. screenshot       :", shot);
  log("   png dims         :", `${w}x${h}`, "|", `${(b.length / 1024).toFixed(1)} KB`);
  if (w !== 1080 || h !== 1920) throw new Error(`unexpected dims ${w}x${h}`);

  // 5 — close
  await browser.close();
  browser = null;
  log("5. closed cleanly   : true");

  fs.writeFileSync(
    path.join(outDir, "result.json"),
    JSON.stringify(
      { ok: true, engine: info.engine, version: info.version, executablePath: execPath, dims: [w, h] },
      null,
      2,
    ),
  );
  log("\nRESULT: Sparticuz Chromium launches, renders and closes locally.");
} catch (err) {
  if (browser) await browser.close().catch(() => {});
  console.error("FAILED:", err && err.stack ? err.stack : err);
  process.exit(1);
}
