/**
 * browser-capability.mjs — two questions, answered with evidence:
 *
 *   A. Can this Chromium render and screenshot a real web UI?
 *      → yes; demonstrated on a live React app served on localhost (Remotion Studio).
 *
 *   B. Can it download a media file from the internet?
 *      → yes, browser-side; demonstrated against codeload.github.com (the one media
 *        host this sandbox's network allows), then the bytes are verified.
 *
 * Remote sites are also attempted so the failure mode is recorded rather than assumed.
 */
import fs from "node:fs";
import path from "node:path";
import crypto from "node:crypto";
import url from "node:url";
import puppeteer from "puppeteer-core";
import { chromiumArgs, resolveChromium } from "./chromium.mjs";

const here = path.dirname(url.fileURLToPath(import.meta.url));
const root = path.resolve(here, "..");
const out = path.join(root, "output", "browser-capability");
const dl = path.join(out, "downloads");
fs.mkdirSync(dl, { recursive: true });

const info = await resolveChromium();
// The sandbox terminates TLS with its own CA, which Chromium does not trust.
// For this diagnostic only, skip certificate validation — otherwise every
// allowlisted host fails before we can even measure reachability.
const browser = await puppeteer.launch({
  args: [...chromiumArgs, "--ignore-certificate-errors", "--allow-insecure-localhost"],
  executablePath: info.executablePath,
  headless: "shell",
  defaultViewport: { width: 1440, height: 900, deviceScaleFactor: 1 },
});
const page = await browser.newPage();

const log = (label, value) => console.log(`${label.padEnd(26)} ${value}`);

// ---------------------------------------------------------------- A. real web UI
console.log("\nA. rendering a live web application");
await page.goto("http://127.0.0.1:3333/", { waitUntil: "networkidle2", timeout: 60000 });
await new Promise((r) => setTimeout(r, 4000)); // studio hydrates + builds the preview
log("title", await page.title());
log("url", page.url());
const h1 = await page.evaluate(() => document.body.innerText.slice(0, 120).replace(/\s+/g, " "));
log("visible text", h1);
const shotA = path.join(out, "studio_1440x900.png");
await page.screenshot({ path: shotA });
log("screenshot", path.relative(root, shotA));

// desktop + phone viewport, the two shapes this project actually uses
await page.setViewport({ width: 390, height: 844, deviceScaleFactor: 2, isMobile: true, hasTouch: true });
await new Promise((r) => setTimeout(r, 1500));
const shotB = path.join(out, "studio_390x844_mobile.png");
await page.screenshot({ path: shotB });
log("screenshot (mobile)", path.relative(root, shotB));
await page.setViewport({ width: 1440, height: 900, deviceScaleFactor: 1 });

// ---------------------------------------------------------------- B. download
console.log("\nB. downloading media through the browser");
const client = await page.createCDPSession();
await client.send("Page.setDownloadBehavior", { behavior: "allow", downloadPath: dl });

const TARBALL = "https://codeload.github.com/mediaelement/mediaelement-files/tar.gz/refs/heads/master";
const started = Date.now();
let err = null;
try {
  await page.goto(TARBALL, { timeout: 90000 });
} catch (e) {
  err = String(e.message ?? e).split("\n")[0];
}
// downloads continue after navigation settles
for (let i = 0; i < 60; i++) {
  const files = fs.readdirSync(dl).filter((f) => !f.endsWith(".crdownload"));
  if (files.length) break;
  await new Promise((r) => setTimeout(r, 1000));
}
const files = fs.readdirSync(dl);
log("navigation error", err ?? "none");
log("files in download dir", JSON.stringify(files));
for (const f of files.filter((x) => !x.endsWith(".crdownload"))) {
  const p = path.join(dl, f);
  const buf = fs.readFileSync(p);
  log(`  ${f}`, `${(buf.length / 1e6).toFixed(1)} MB  sha256 ${crypto.createHash("sha256").update(buf).digest("hex").slice(0, 16)}…`);
}
log("elapsed", `${((Date.now() - started) / 1000).toFixed(1)} s`);

// ---------------------------------------------------------------- C. remote site
console.log("\nC. attempting an ordinary remote site (expected to be blocked here)");
try {
  const res = await page.goto("https://example.com/", { waitUntil: "domcontentloaded", timeout: 15000 });
  log("status", res ? res.status() : "no response");
} catch (e) {
  log("blocked", String(e.message ?? e).split("\n")[0]);
}

await browser.close();
fs.writeFileSync(path.join(out, "capability.json"), JSON.stringify({ browser: info, files }, null, 2));
console.log(`\nartifacts → ${path.relative(root, out)}`);
