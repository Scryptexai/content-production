# ODDCHAPTER — Logo System

**Status:** Phase 3 complete · geometry frozen since the approved LINK refinement (2026-11-06)
**Source of truth:** `tools/brand.py` — every file in this folder is generated, never hand-edited.

---

## 1. What the mark is

One geometric idea: a closed **O** ring and a **C** arc with an 84° mouth, both drawn on circular
arcs, overlapping by 9 units so the two stroke edges meet in a pointed lens. The lens is not a
symbol — it is what happens when an O and a C are drawn by the same hand on the same grid and
allowed to touch.

| Property | Value | Confidence |
|---|---|---|
| Outer radius / counter radius | 27 / 14 units | VERIFIED (in code) |
| Stroke | 13 units (= outer − counter) | VERIFIED |
| C mouth | 84° | VERIFIED |
| Centre distance | 44 units | VERIFIED |
| Monogram bounding box | 98 × 54 units | VERIFIED |
| Canvas grid | 100 × 100 units, circular arcs only | VERIFIED |

The monogram is **one path** with `fill-rule="evenodd"`, so the junction lens falls out
automatically and the shape can never be assembled incorrectly.

---

## 2. Variant matrix

| File | Colour | Background | Use |
|---|---|---|---|
| `master/MONOGRAM_MASTER.svg` | Ink | transparent | default mark, light backgrounds |
| `master/LOGO_MASTER.svg` | Ink + orange rule | transparent | default lockup, light backgrounds |
| `master/LOGO_MASTER_TAGLINE.svg` | Ink + orange rule | transparent | hero lockup, light backgrounds |
| `master/AVATAR_COMPACT.svg` | Ivory | Ink (1024²) | channel avatar at small display size |
| `master/ICON_SQUARE.svg` | Ink | transparent (1:1) | app icon / favicon source |
| `dark/*` | Ivory + orange | for Ink | video, dark UI, thumbnail plates |
| `light/*` | Ink + orange | for Ivory | print, light web |
| `monochrome/*` | single Ink | any single colour | fax, embossing, one-colour print, stamps |
| `dark/ICON_SQUARE_DARK.svg` | Ivory on Ink, 1:1 | — | favicon / app icon (background included) |

Every `.svg` has a matching `.png` at the documented pixel width. The monochrome set has **no**
tagline variant: at the sizes where mono printing survives, the tagline does not.

### Which file do I use?

- **YouTube channel art, thumbnail plates, video end cards** → `dark/`
- **Website header, invoices, light documents** → `master/` or `light/`
- **Avatar / profile picture** → `master/AVATAR_COMPACT` (already optically centred and padded)
- **Favicon, app icon, PWA icon** → `06_EXPORTS/FAVICON_*.png` (square, background baked in)
- **Anything that cannot carry colour** → `monochrome/`

---

## 3. Clear space

Clear space = **one monogram stroke = 13 units ≈ 13.3 % of the monogram height**, on every side.
For the lockup, measure from the outer edge of the monogram (left) and the last letter of the
wordmark (right). Nothing — text, frame, image edge, other logo — may enter that box.

The measured box is drawn to scale in `05_PREVIEWS/USAGE_DO_DONT.png`, row 3, panel 1.

---

## 4. Minimum sizes

| Asset | Minimum | Absolute floor | Why |
|---|---|---|---|
| Monogram | 32 px / 8 mm | 24 px | Below 24 px the junction lens fills in and it reads as a blob |
| Horizontal lockup | 240 px / 60 mm | 200 px | Wordmark stems drop below 1 px |
| Lockup with tagline | 420 px / 105 mm | 360 px | Tagline cap height falls under 3.5 px |
| Clear space | 13.3 % of monogram height | — | scales with the mark |

VERIFIED at true pixel size — see `05_PREVIEWS/SMALL_SIZE_TEST.png` and
`06_EXPORTS/FAVICON_32.png` (rendered at 32 px, not a downscale of a larger render).

**Favicon exception (documented, not accidental):** at a 32 px canvas the mark occupies 25 px of
ink width — the absolute floor. That is the smallest this identity is ever allowed to appear, and
the junction still closes cleanly there. Everything smaller is a browser's problem, not ours.

---

## 5. Colour rules

| Combination | Contrast | Allowed |
|---|---|---|
| Ivory on Ink | 15.48 : 1 | YES — default |
| Ink on Ivory | 15.48 : 1 | YES |
| Sage on Ink | 7.85 : 1 | YES — support text only |
| Orange on Ink | 5.79 : 1 | YES — rule / accent, never the wordmark |
| Orange on Ivory | 2.68 : 1 | **NO — fails WCAG AA for text** |

The orange rule under the tagline is a **graphic element**, not text. It may sit on Ivory.
The wordmark may never be orange: at that point orange stops being an accent.

Full-visual version: `05_PREVIEWS/USAGE_DO_DONT.png`.

---

## 6. Incorrect usage

Each of these is rendered, with its reason, in `05_PREVIEWS/USAGE_DO_DONT.png`:

1. Orange wordmark.
2. Any colour outside the four tokens.
3. Non-uniform scaling (the circles become ellipses — this is the most common failure).
4. Rotation.
5. Adding a symbol: play button, book, eye, camera, brain, AI spark.
6. Text or edges inside the clear space.
7. Sizes below the floor.
8. Shadows, glows, bevels, outlines, gradient fills.
9. Re-typing the wordmark in another font, or "fixing" the tracking.
10. Rebuilding the monogram from two circles plus a gap — the lens geometry is not the same thing.

---

## 7. Typography in the logo

- Wordmark: **Space Grotesk 700**, tracking **+0.02 em**, converted to outlines.
- Tagline: **Inter 600**, tracking **+0.17 em**, uppercase, converted to outlines.
- Relationship: monogram height = **1.5 ×** wordmark cap height; gap = **0.62 ×** cap height.

Both faces are SIL OFL 1.1. No font binary ships in this repository and no logo file references a
font — the outlines are baked in, so the files render identically on a machine with neither font
installed. (`tools/fetch_fonts.sh` re-downloads them into `.build/`, which is git-ignored.)

---

## 8. File conventions

- **SVG:** pure paths + `<rect>`, no `<text>`, no `<image>`, no embedded fonts, no filters.
  Verified: `grep -rl "<text" 01_LOGO/` returns only the Phase 2 concept-exploration sheets,
  which are documentation, not logos.
- **PNG:** sRGB, real alpha (transparent background), width as documented in the filename.
- **Naming:** `ASSET_VARIANT_WIDTH.png`, e.g. `LOGO_DARK_TAGLINE_2400.png`. Dimensions are always
  in the name because assets get dropped into tools that re-scale silently.

---

## 9. Regenerating

```bash
python3 tools/build_system.py     # rewrites every SVG in 01_LOGO + 04_MOTION
bash tools/render_all.sh          # re-renders every PNG at its documented size
```

Change `DIST` in `tools/brand.py` and the entire system — logo, avatar, banner, thumbnails,
watermarks, storyboard — moves together. That is the point of the build chain: geometry cannot
drift between surfaces.
