# ODDCHAPTER — Brand Identity System

**REAL STORIES. UNEXPECTED CHAPTERS.**
*KISAH NYATA. DI LUAR DUGAAN.*

This folder is the production home of the ODDCHAPTER visual identity. It is a working system,
not a folder of pictures: every mark is generated from one geometry source, and every export can
be rebuilt from that source.

---

## Where the project stands

| Phase | Deliverable | Status |
|---|---|---|
| 1 | `BRAND_DIRECTION.md` — direction & reference analysis | **Complete** — built from the written spec; no reference image exists (owner confirmed) |
| 2 | `01_LOGO/concepts/` — three OC monogram concepts | **Complete** — **concept 01 LINK approved 2026-11-06** |
| 2.5 | `01_LOGO/REFINEMENT_NOTES.md` + refined masters | **Approved** — centre distance 44, stroke 13 |
| 3 | `01_LOGO/LOGO_SYSTEM.md`, variant matrix, `06_EXPORTS/` | **Complete** — 14 SVG · 12 PNG · favicons square and verified |
| 4 | `02_YOUTUBE/`, `03_SOCIAL/`, thumbnails | **Complete** — 12 channel/social assets at platform sizes |
| 5 | `04_MOTION/MOTION_IDENTITY.md`, `04_MOTION/` | **Complete** — storyboard + 3 layer files |
| 6 | `BRAND_GUIDELINES.md`, `05_PREVIEWS/` sheets | **Complete** — usage sheet + contact sheet |
| 7 | Extended surfaces + motion delivery | **Complete** — stories, OG card, end card; rendered 38-frame build + SMIL |
| 8 | Print & physical applications | **Complete** — 9 mm-authored artworks + `07_PRINT/PRINT_SPEC.md` |
| 9 | Audio identity | **Complete** — voice auditioned, spoken signature delivered + `08_AUDIO/AUDIO_IDENTITY.md` |

Full verification table and open items: **`FINAL_DELIVERY_REPORT.md`**.

---

## Structure

```
ODDCHAPTER_BRAND/
├── README.md                    ← this file
├── BRAND_DIRECTION.md           Phase 1 — direction, colour ratios, contrast, risks
├── BRAND_GUIDELINES.md          Phase 6 — colour, type, layout, photography, voice
├── FINAL_DELIVERY_REPORT.md     what shipped, how it was verified, what is open
├── TOOL_AUDIT.md                environment + licensing audit
├── package.json                 build tooling (@resvg/resvg-js), not a shipped package
├── tools/
│   ├── brand.py                 ← single source of truth: geometry + lockup + tagline
│   ├── oclib.py                 primitives, tokens, glyph → outline conversion
│   ├── build_system.py          every SVG in 01_LOGO + 04_MOTION
│   ├── build_channel.py         avatar, banner, watermark, social
│   ├── build_thumbs.py          the three thumbnail systems
│   ├── build_sheets.py          storyboard, usage sheet, contact sheet
│   ├── build_extra.py           Phase 7: stories, OG card, end card
│   ├── build_motion.py          Phase 7: frames, GIF, poster, SMIL opener
│   ├── build_print.py           Phase 8: mm-authored print artwork
│   ├── audio_info.py            MP3 duration parser (no ffprobe on this host)
│   ├── build_concepts.py        Phase 2 record (kept for history)
│   ├── build_link.py            Phase 2.5 refinement preview
│   ├── render_all.sh            re-renders every PNG at its documented size
│   ├── render.mjs               SVG → PNG (resvg)
│   └── fetch_fonts.sh           OFL fonts → .build/ (never committed)
├── 01_LOGO/
│   ├── LOGO_SYSTEM.md           ← variant matrix, clear space, minimum sizes, do/don't
│   ├── REFINEMENT_NOTES.md      Phase 2.5 spec
│   ├── master/  dark/  light/  monochrome/     production SVGs + PNGs
│   └── concepts/                Phase 2 record of the three directions
├── 02_YOUTUBE/  avatar · banner · watermark · thumbnails · end_card   + README.md
├── 03_SOCIAL/   profile · post_templates · stories · link_preview     + README.md
├── 04_MOTION/   MOTION_IDENTITY.md · svg_components · animation_reference · preview
├── 05_PREVIEWS/ concept overview · small-size test · approved refinement · usage sheet · contact sheet
├── 06_EXPORTS/  favicons (512/192/32) · transparent icon · primary logo 2000
├── 07_PRINT/    PRINT_SPEC.md · one_colour · stationery · poster · merch · previews
└── 08_AUDIO/    AUDIO_IDENTITY.md · assets/ (signature ID + EN, cold-open read)
```

---

## Brand tokens (fixed — do not drift)

| Token | HEX | Role |
|---|---|---|
| Ink | `#17191D` | primary dark / ground |
| Ivory | `#F4F0E8` | primary light / figure |
| Signal Orange | `#F26A3D` | accent only (≤ 8 % of any composition) |
| Sage | `#A7B0A1` | support: rules, captions, dividers |

Type: **Space Grotesk** (display) · **Inter** (body). Both SIL OFL 1.1.
Geometry grid: **100 × 100 units**, circular arcs only.
Mark: outer 27 · counter 14 · stroke 13 · mouth 84° · centre distance 44 · box 98 × 54 units.

---

## Rebuilding everything

```bash
cd ODDCHAPTER_BRAND
npm install                       # resvg rasteriser (git-ignored)
pip3 install fontTools brotli     # glyph outlines
bash tools/fetch_fonts.sh         # OFL fonts → .build/fonts (git-ignored)
python3 tools/build_system.py     # logo + motion
python3 tools/build_channel.py    # YouTube + social
python3 tools/build_thumbs.py     # thumbnails
python3 tools/build_sheets.py     # sheets
python3 tools/build_extra.py      # stories, OG card, end card
python3 tools/build_motion.py     # 38 frames → GIF + poster + SMIL
python3 tools/build_print.py      # print artwork (mm) + previews
bash tools/render_all.sh          # every PNG at its documented size (chains the above)
```

Change `DIST` in `tools/brand.py` and every asset — logo, avatar, banner, thumbnail, watermark,
storyboard — moves together. That is what keeps the geometry from drifting between surfaces.

---

## Decisions log

| # | Decision | Reason | Status |
|---|---|---|---|
| 1 | Marks built as parametric SVG, never generated raster | Brief requirement; scalability and editability | Done |
| 2 | Wordmark = real Space Grotesk Bold outlines via fontTools | No font dependency in masters, no distorted type | Done |
| 3 | resvg instead of ImageMagick for rendering | ImageMagick's SVG delegate is missing on this host; resvg honours `fill-rule` | Done |
| 4 | No font binaries committed | OFL: prefer linking over redistribution | Done |
| 5 | Orange limited to one accent per asset | Brief: "accent, not dominant" | Done |
| 6 | Three concepts differ by *junction behaviour and axis*, not decoration | Keeps the choice strategic rather than cosmetic | Done |
| 7 | Owner approved 01 LINK; tagline English only | Owner decision 2026-11-06 | Locked |
| 8 | Refinement: centre distance 42 → 44 | Junction pinched at 42; 44 lets both letters read while staying interlocked | Approved |
| 9 | Tagline set in Ink/Ivory, orange used only as the rule above it | Orange on Ivory measures 2.68 : 1 — graphic only, never text | Applied |
| 10 | Favicons render from a dedicated 1:1 source, not the wide monogram | Rendering a 98 × 54 mark at a square width produced 512 × 330 | Fixed |
| 11 | Tagline converted to outlines | No live `<text>` in any logo file — it rendered as tofu where Inter was absent | Fixed |
| 12 | Banner lockup fixed at 1080 px (70 % of the 1546 px safe width) | Survives every device crop without a separate mobile asset | Applied |
| 13 | Thumbnails are layouts with an `id="image-slot"` group | The photo has to be swappable without touching the grid | Applied |
| 14 | Template copy stays live text; logo copy does not | Editors must retype headlines; nobody should retype the logo | Applied |
| 15 | Motion: 1.2 s build, one orange animation, hard cut | No logo stings; the identity behaves like an edit | Documented |
| 16 | No MP4/Lottie produced | Outside this toolchain; the storyboard + layers are the spec | Open, documented |
| 17 | Square assets centre the monogram on its *ink*, not its 98-unit box | The C mouth carves the box's right edge; box-centring left the mark visibly off-centre | Applied |
| 18 | Motion delivered as GIF + SMIL + poster, not MP4 | No ffmpeg on this host and installing one was not approved; the frame source is in the repo | Done, MP4 open |
| 19 | Story/vertical assets are separate layouts, not crops | A 9:16 crop of a 16:9 band leaves the headline in the platform's UI zone | Applied |
| 20 | Hatch segments for image slots are computed inside the box | The naive full-plane hatch crashes resvg on tall canvases | Fixed |
| 21 | Print artwork is authored in millimetres, never pixels | A printer needs physical measurements; `210mm` cannot be misread as 72 dpi | Applied |
| 22 | Poster headline is outlined and auto-fitted to the margin | The first render overflowed the trim — live text cannot be size-checked by eye | Fixed |
| 23 | One-colour masters are true 100 % K, not brand Ink | Ink `#17191D` is a four-colour build; stamps, foil and screen print need one plate | Applied |
| 24 | Brand voice is auditioned, not assumed | The brand docs fix the *profile*, not the person; the owner picks the voice | Done |
| 25 | Spoken signature, not a sonic logo | A musical mark needs a composer or a music model — neither is in this toolchain | Documented |
| 26 | Delivered MP3s are reference quality (24 kHz mono) | Enough to judge timing and tone; masters must be re-recorded at 48 kHz | Open |

---

## Notes on honesty and limits

- **No reference image was supplied** for Phase 1. `BRAND_DIRECTION.md` §2 defines exactly how that
  analysis will be added when the file arrives. Nothing was invented to fill the gap.
- Every claim marked **VERIFIED** was tested in this environment (rendered, measured or parsed).
  Claims marked **LIKELY / ASSUMPTION / UNKNOWN** say so.
- Small-size behaviour was tested at true pixel size, then magnified — see
  `05_PREVIEWS/SMALL_SIZE_TEST.png` and `06_EXPORTS/FAVICON_32.png`.
- **Logo files contain no text elements, no raster and no embedded fonts** — pure paths plus rects,
  so they open identically anywhere. *Documentation* sheets (`LOGO_CONCEPTS.svg`,
  `*-construction.svg`, storyboard, crop check) and the *editable templates* (thumbnails, social
  post) deliberately use live text; their PNGs are the reliable view.
- Nothing here has been uploaded, published or connected to any external channel account.
