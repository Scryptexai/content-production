/**
 * browser-probe.mjs — is this Chromium a real, general-purpose browser with
 * internet access, or only a rasteriser for local pages?
 *
 * Opens a list of real sites, records the outcome per URL, and screenshots each
 * one (including failure pages, which is the interesting case here).
 */
import fs from "node:fs";
import path from "node:path";
import url from "node:url";
import puppeteer from "puppeteer-core";
import { chromiumArgs, resolveChromium } from "./chromium.mjs";

const here = path.dirname(url.fileURLToPath(import.meta.url));
const outDir = path.join(here, "..", "output", "browser-probe");
fs.mkdirSync(outDir, { recursive: true });

const TARGETS = [
  ["example", "https://example.com/"],
  ["wikipedia", "https://id.wikipedia.org/wiki/Danau_Nyos"],
  ["wikimedia-commons", "https://commons.wikimedia.org/wiki/Category:Videos_of_lakes"],
  ["archive-org", "https://archive.org/details/nasa_techdoc_19930072988"],
  ["nasa", "https://images.nasa.gov/"],
];

const info = await resolveChromium();
console.log(`browser: ${info.engine} ${info.version}\n`);

const browser = await puppeteer.launch({
  args: chromiumArgs,
  executablePath: info.executablePath,
  headless: "shell",
  defaultViewport: { width: 1280, height: 800, deviceScaleFactor: 1 },
});

const page = await browser.newPage();
const results = [];

for (const [name, target] of TARGETS) {
  const started = Date.now();
  let status = null;
  let error = null;
  try {
    const response = await page.goto(target, { waitUntil: "domcontentloaded", timeout: 20000 });
    status = response ? response.status() : null;
  } catch (err) {
    error = String(err.message ?? err).split("\n")[0];
  }
  let title = "";
  try {
    title = await page.title();
  } catch {
    /* page may be dead */
  }
  const file = path.join(outDir, `${name}.png`);
  try {
    await page.screenshot({ path: file, type: "png" });
  } catch (err) {
    error = error ?? String(err.message ?? err).split("\n")[0];
  }
  const row = { name, target, status, title, ms: Date.now() - started, error, screenshot: fs.existsSync(file) ? path.relative(path.join(here, ".."), file) : null };
  results.push(row);
  console.log(
    `${row.name.padEnd(18)} ${String(row.status ?? "—").padEnd(4)} ${String(row.ms).padStart(6)}ms  ` +
      `${(row.title || "").slice(0, 46).padEnd(46)} ${row.error ? "ERR: " + row.error : ""}`,
  );
}

// what does the browser think it can reach?
const probe = await page.evaluate(async () => {
  const out = {};
  try {
    const r = await fetch("https://example.com/", { mode: "cors" });
    out.fetchExample = r.status;
  } catch (e) {
    out.fetchExample = "blocked: " + String(e.message);
  }
  return out;
});
console.log("\nin-page fetch:", JSON.stringify(probe));

await browser.close();
fs.writeFileSync(path.join(outDir, "results.json"), JSON.stringify({ browser: info, results }, null, 2));
console.log(`\nwrote ${path.relative(path.join(here, ".."), path.join(outDir, "results.json"))}`);
