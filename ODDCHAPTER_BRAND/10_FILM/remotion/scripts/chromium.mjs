/**
 * chromium.mjs — the single source of truth for which browser renders the film.
 *
 * @sparticuz/chromium ships a Chromium build plus an `al2023.tar.br` bundle of the
 * shared libraries that build expects (libnspr4, libnss3, ...). On a generic Linux
 * box those are not installed, so the binary exits 127. We decompress the bundle
 * ourselves and point LD_LIBRARY_PATH at it. Remotion then launches this exact
 * executable (see scripts/render.mjs), so the report can name the real renderer.
 */
import fs from "node:fs";
import path from "node:path";
import url from "node:url";
import zlib from "node:zlib";
import { execFileSync } from "node:child_process";
import chromium from "@sparticuz/chromium";

const here = path.dirname(url.fileURLToPath(import.meta.url));
const LIB_DIR = path.join(here, "..", ".chromium-libs");

export const BROWSER = {
  engine: "@sparticuz/chromium (checked-in npm binary)",
  version: null,
  executablePath: null,
  libDir: LIB_DIR,
};

/** Decompress al2023.tar.br once, then export LD_LIBRARY_PATH for child processes. */
export function ensureChromium() {
  const tarPath = path.join(here, "..", "node_modules", "@sparticuz", "chromium", "bin", "al2023.tar.br");
  const marker = path.join(LIB_DIR, "lib", "libnspr4.so");

  if (!fs.existsSync(marker)) {
    fs.mkdirSync(LIB_DIR, { recursive: true });
    const tmpTar = path.join(LIB_DIR, "al2023.tar");
    fs.writeFileSync(tmpTar, zlib.brotliDecompressSync(fs.readFileSync(tarPath)));
    execFileSync("tar", ["-xf", tmpTar, "-C", LIB_DIR]);
    fs.unlinkSync(tmpTar);
  }

  process.env.LD_LIBRARY_PATH = [LIB_DIR + "/lib", process.env.LD_LIBRARY_PATH]
    .filter(Boolean)
    .join(":");
  return LIB_DIR;
}

/** Resolve the executable, make sure it runs, and record its version. */
export async function resolveChromium() {
  ensureChromium();
  const execPath = await chromium.executablePath();
  BROWSER.executablePath = execPath;
  BROWSER.version = execFileSync(execPath, ["--version"], { encoding: "utf8" })
    .trim()
    .replace(/^Chromium\s+/, "");
  return BROWSER;
}

export const chromiumArgs = [...chromium.args, "--no-sandbox", "--disable-dev-shm-usage"];
