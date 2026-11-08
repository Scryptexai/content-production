# REFINEMENT_NOTES.md
### ODDCHAPTER — approved concept 01 LINK — refinement preview

**Status: refinement preview — awaiting owner approval.**
No YouTube, social, thumbnail or motion asset has been produced. This document covers the
monogram and the horizontal lockup only.

---

## 1. What was approved

| Item | Decision | Source |
|---|---|---|
| Monogram direction | **01 LINK** (interlock, transparent junction) | Owner, 2026-11-06 |
| Tagline in the lockup | **English only** — REAL STORIES. UNEXPECTED CHAPTERS. | Owner, 2026-11-06 |
| Phase 1 basis | The written brief (no reference image exists) | Owner, 2026-11-06 |
| Colour, type, direction | Unchanged from the brief | Brief |

---

## 2. What changed in the drawing — one parameter

| Parameter | Approved concept | Refined | Note |
|---|---|---|---|
| Outer radius | 27 u | 27 u | unchanged |
| Counter radius | 14 u | 14 u | unchanged |
| Stroke | 13 u | 13 u | unchanged |
| C mouth | 84° | 84° | unchanged |
| **Centre distance** | **42 u** | **44 u** | **the only change** |
| Junction lens width | 12 u | 10 u | consequence of the above |

**Reason.** At 42 units the tips of the junction lens came within 1 unit of the counters. At display
sizes this read as a pinch; at small sizes it closed into a grey blob. Moving the centres apart by
2 units relaxes the junction, lets each letter read as a complete shape, and keeps the interlock —
the lens is still the only place where the two rings pass through each other.

**Reversible:** one constant (`DIST`) in `tools/build_link.py`. Nothing else about the concept
was redesigned. No new direction was introduced.

---

## 3. Lockup specification (current proposal)

| Property | Value | Note |
|---|---|---|
| Wordmark | ODDCHAPTER, Space Grotesk Bold, +0.02 em tracking, uppercase | outlines, no font dependency |
| Cap height | 36 units (reference) | everything else derives from it |
| Monogram height | 1.5 × cap height | optically centred on the cap height |
| Gap, monogram → wordmark | 0.62 × cap height | not less than 0.5 × cap |
| Tagline | Inter SemiBold, 0.235 × cap, +0.17 em tracking | cap height ≥ 24 px to stay legible |
| Tagline rule | Signal Orange, full wordmark width, 0.035 × cap thick | the only accent in the lockup |
| Tagline colour | same as the wordmark (Ink on Ivory · Ivory on Ink) | **not** orange — orange fails 2.68 : 1 on Ivory |
| Clear space | 1 × stroke (13 monogram units) on all sides | measured from the lockup bounding box |

**Colour of the lockup itself:** the mark and wordmark are monochrome. The single point of orange is
the rule above the tagline, or nothing at all in the version without a tagline. This keeps Signal
Orange inside the ≤ 8 % rule set in `BRAND_DIRECTION.md` §3.2.

---

## 4. Minimum sizes (verified by rendering)

| Context | Minimum | Note |
|---|---|---|
| Monogram, digital | 32 px high | 24 px is the hard floor; the junction lens closes below that |
| Monogram, print | 8 mm wide | |
| Horizontal lockup, digital | 240 px wide | the wordmark needs ≥ 14 px cap height |
| Horizontal lockup with tagline | 420 px wide | tagline needs ≥ 8 px cap height |

These are starting values, not limits invented for comfort — they come from the rendered size ladder
in `05_PREVIEWS/LINK_REFINEMENT.png` §D.

---

## 5. Files produced for this preview

| Path | What it is |
|---|---|
| `01_LOGO/master/LINK_MONOGRAM_MASTER.svg` | monogram, single colour, transparent, clear space built into the canvas |
| `01_LOGO/master/LINK_PRIMARY_HORIZONTAL.svg` | monogram + wordmark |
| `01_LOGO/master/LINK_PRIMARY_HORIZONTAL_TAGLINE.svg` | monogram + wordmark + tagline + accent rule |
| `01_LOGO/dark/…` | same three, on Ink |
| `01_LOGO/light/…` | same, on Ivory |
| `01_LOGO/monochrome/…` | single-colour versions |
| `05_PREVIEWS/LINK_REFINEMENT.svg` · `.png` | the approval sheet (what changed, construction, lockups, sizes) |

All are vector. The wordmark is outlined; no font is required to open or edit them.

---

## 6. Known limitations

- **VERIFIED** — the monogram is one path with `fill-rule="evenodd"`. Some very old or non-compliant
  SVG converters ignore that rule and would fill the letters solid. Every PNG in this project is
  rendered with resvg, which honours it; if a third-party platform mistakes the fill, use the PNG.
- **VERIFIED** — below 24 px the junction lens disappears. This is inherent to the concept, not a
  defect to be fixed by weight changes.
- **ASSUMPTION** — the 1.5 × cap / 0.62 × cap lockup proportions were tuned against Space Grotesk
  Bold only. If the wordmark is ever re-set in another weight, the gap should be re-tuned.
- **UNKNOWN** — final platform constraints (YouTube avatar crop behaviour on TV surfaces) are
  addressed in Phase 4, not here.

---

## 7. On approval, Phase 3 produces

1. `LOGO_SYSTEM.md` — full usage rules, clear space, minimum sizes, incorrect usage.
2. Pixel-fitted 48 px and 32 px cuts of the monogram (true hinting-free redraw at small sizes).
3. Complete variant matrix: dark / light / monochrome / reversed / avatar-locked.
4. `06_EXPORTS/` — PNG at exact platform dimensions, transparent where required.
5. Phase 4 begins: YouTube avatar 800 × 800, banner 2560 × 1440, watermark, three thumbnail systems.
