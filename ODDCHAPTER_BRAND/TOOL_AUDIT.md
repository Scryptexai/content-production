# TOOL_AUDIT.md
### ODDCHAPTER — environment and capability audit (run before any design work)

Audit date: 2026-11-06 · Host: Debian GNU/Linux 12 (bookworm), x86_64 · Shell: no GUI session
Labels: **VERIFIED** = directly tested in this session · **MISSING** = tested and absent ·
**ASSUMPTION** = inferred, not exercised

---

## 1. Summary

| Capability | Status | What is actually used |
|---|---|---|
| Programmatic vector authoring | **VERIFIED** | Python 3.11 + custom geometry library (`tools/oclib.py`) → SVG |
| SVG → PNG rasterisation | **VERIFIED** | `@resvg/resvg-js` 2.x (prebuilt Rust binary, npm) |
| Font access (licensing) | **VERIFIED** | `@fontsource/space-grotesk`, `@fontsource/inter` (both SIL OFL 1.1) |
| Text → outlines | **VERIFIED** | `fontTools` 4.68 (`SVGPen` / `TransformPen`) converting real glyph outlines |
| Image generation (exploration only) | **VERIFIED** available | Not used for any master asset |
| Inkscape / Figma | **MISSING** | Not installed, no GUI; workaround below |
| Playwright / headless browser | **MISSING** | Not installed, not needed |
| ImageMagick | **VERIFIED** (6.9.11) | Used only for QC (dimensions, alpha), **not** for SVG rendering |
| ffmpeg | **MISSING** | Motion stage only; not required for Phase 1–2 |

---

## 2. Verified detail

### 2.1 System
- `python3` 3.11.2 · `node` v22.22.3 · `npm` 10.9.8 — **VERIFIED**
- `convert` (ImageMagick 6.9.11-60 Q16) — **VERIFIED**
- `fc-list` / fontconfig user fonts: **0 fonts installed system-wide** — **VERIFIED**
  (relevant: no system font, so every type asset must carry its own font or be outlined)

### 2.2 Not installed — **MISSING**, confirmed by `command -v`
`inkscape`, `rsvg-convert`, `magick` (IM7), `ffmpeg`, `chromium`, `google-chrome`,
`playwright`, `cairosvg`, `Pillow`, `fontforge`, `optipng`, `numpy`.

### 2.3 Installed for this project — **VERIFIED** (small, no approval-level footprint)
| Package | Size class | Purpose | Where |
|---|---|---|---|
| `@resvg/resvg-js` | npm binary, ~10 MB | SVG → PNG with correct antialiasing | `ODDCHAPTER_BRAND/node_modules` (git-ignored) |
| `fontTools` + `brotli` | pip, ~5 MB | WOFF2 → TTF, glyph → path outlines | system python |
| `@fontsource/space-grotesk`, `@fontsource/inter` | npm, WOFF2 | official OFL font files | `.build/` (git-ignored) |

Nothing was purchased, no paid API was called, no external account was touched.

### 2.4 Why not ImageMagick for SVG
ImageMagick 6 delegates SVG to `rsvg-convert`, which is **MISSING** on this host. Its fallback
renderer (MSVG) does not resolve `fill-rule="evenodd"` reliably and would silently break the
LINK monogram's knockout. **VERIFIED by delegate inspection** (`convert -list delegate | grep svg`).
ImageMagick is therefore used for *inspection only* (dimensions, alpha channel), never for output.

### 2.5 Why resvg
- Renders `fill-rule`, arcs, clip paths and dashed guides exactly.
- Loads font files explicitly (`font.fontFiles`), which matters because the system has zero fonts.
- Deterministic: same SVG in → same PNG out, byte-stable enough for asset QC.

---

## 3. Font licensing position

- **Space Grotesk** and **Inter** are both SIL Open Font License 1.1 — **VERIFIED** via the
  `LICENSE` file shipped in each `@fontsource` package.
- Font binaries are **not committed** to this repository. `tools/fetch_fonts.sh` re-downloads them
  from the official package mirrors at build time, so the repo redistributes no font file.
- Logo masters contain **no font dependency**: the wordmark is converted to real glyph outlines.
  Anyone can open the SVG and edit the paths without installing a font.
- Recommended public links for the client (source of truth, not redistribution):
  `https://fonts.google.com/specimen/Space+Grotesk` · `https://fonts.google.com/specimen/Inter`

---

## 4. Missing tools and the workarounds actually used

| Missing | Consequence | Workaround used |
|---|---|---|
| Inkscape | No GUI vector editing, no "save as plain SVG" hygiene pass | SVG written by generator with explicit geometry; every file validated as XML and rendered to PNG for visual QC |
| Figma | No shared component library / no designer hand-off file | Parametric generator (`tools/`) is the component library; concepts and masters regenerate from one source of truth |
| `rsvg-convert`, `cairosvg` | No second rasteriser to cross-check | resvg is the single renderer; QC done by pixel inspection (dimensions, alpha, visual review of the exported PNG) |
| Playwright / browser | Cannot screenshot HTML/CSS comps | All layout done natively in SVG |
| Network to fonts.google.com / Pinterest | Restricted egress (allow-list: GitHub, npm, PyPI) | Fonts via npm mirrors; reference research done from the brief and category knowledge |
| Reference image | Phase 1 cannot be a true reference analysis | Documented as **UNKNOWN** in `BRAND_DIRECTION.md` §2, with a re-analysis protocol ready |

---

## 5. Reproduction instructions (VERIFIED, run end-to-end this session)

```bash
cd ODDCHAPTER_BRAND
npm install                     # @resvg/resvg-js
bash tools/fetch_fonts.sh       # OFL fonts -> .build/fonts (git-ignored)
python3 tools/build_concepts.py # writes the concept SVGs
node tools/render.mjs 01_LOGO/concepts/LOGO_CONCEPTS.svg \
     01_LOGO/concepts/LOGO_CONCEPTS.png 2600 none
```

`tools/render.mjs <in.svg> <out.png> [width] [background|none]` — `none` preserves transparency.
