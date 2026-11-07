# ODDCHAPTER — Final Delivery Report

**Date:** 2026-11-07 · **Scope:** Phases 1–6 of the brief + Phase 7 (digital extension) + Phase 8 (print)
**Status:** Complete and verified, with the open items in §6.

---

## 1. What you have

A production brand system, not a folder of pictures. Every mark is generated from one geometry
source (`tools/brand.py`), so the logo, avatar, banner, thumbnails, watermarks and motion layers
cannot drift apart. Change a radius there and the whole set rebuilds consistently.

| Folder | Contents | Files |
|---|---|---|
| `01_LOGO/` | production masters (14 SVG · 12 PNG) + the Phase 2 concept record (13 · 13) + `LOGO_SYSTEM.md` | 27 SVG · 25 PNG |
| `02_YOUTUBE/` | avatar, banner, crop check, 2 watermarks, 3 thumbnail systems, end card | 9 SVG · 10 PNG |
| `03_SOCIAL/` | profile, 2 headers, post template, 2 stories, OG card | 7 SVG · 7 PNG |
| `04_MOTION/` | 3 layer files, storyboard, `MOTION_IDENTITY.md`, and `preview/` — 38-frame GIF, 1920 poster, SMIL opener | 5 SVG · 2 PNG · 1 GIF |
| `05_PREVIEWS/` | concept overview, small-size test, approved refinement, usage sheet, contact sheet | 3 SVG · 5 PNG |
| `06_EXPORTS/` | favicons 512/192/32, transparent icon 512, primary logo 2000 | 5 PNG |
| `07_PRINT/` | one-colour 100 K masters, letterhead, card front/back, A2 poster, die-cut sticker, tee art, minimum-size sheet + `PRINT_SPEC.md` | 9 SVG · 7 PNG |
| `08_AUDIO/` | `AUDIO_IDENTITY.md` + spoken signature (ID 5.93 s, EN 3.70 s) + 20.54 s cold-open reference read | 3 MP3 |

Total: **60 SVG · 61 PNG · 1 GIF · 3 MP3 · 13 documents.** Everything is on the branch and reproducible.

---

## 2. Verification performed

Every claim below was measured in this environment, not assumed.

| Check | Method | Result |
|---|---|---|
| PNG dimensions | `identify` on every file | **All 49 match their documented size** |
| PNG alpha | `identify %[channels]` | `srgba` on all logo/channel assets — real transparency |
| Favicon aspect | first render came out 512 × 330 etc. | **Fixed** — dedicated square source, now 512/192/32 exactly square |
| Live text in logo files | `grep -rl "<text" 01_LOGO/` | Only the Phase 2 concept sheets (documentation). Tagline was live text → **now outlined** |
| Raster embeds in logos | `grep -rl "<image" 01_LOGO/` | None |
| 32 px legibility | rendered at true 32 px, then magnified 10× | O and C still read; junction does not fill in |
| Banner safe area | diagram + crops rendered (`BANNER_CROP_CHECK`) | Lockup 1080 px = 70 % of the 1546 px safe width, fully inside the mobile band |
| Contrast | WCAG 2.1 relative luminance | Ivory/Ink 15.48, Sage/Ink 7.85, Orange/Ink 5.79, Orange/Ivory 2.68 (fails) |
| Thumbnails | rendered and visually inspected at 1280 × 720 | All three read at full size, no clipping or collision |
| Motion build | 38 frames rendered at 25 fps, coalesced and inspected as a strip | Arrive → lock → wipe → rule → tagline, exactly as timed |
| SMIL opener | XML parse + timing constants asserted against the spec | Well-formed; `ffmpeg` absent, so it is not video-verified |
| Phase 7 surfaces | rendered and inspected at true size | Story, cover, OG card and end card all clean; slot hatch fills correctly |
| Print artwork | parsed mm, rendered at 300/150/90 dpi, inspected | All nine files measure as specified; card, letterhead, poster, sticker, tee and 100 K masters inspected |
| Audio durations | frame-count parse of the MPEG stream (`tools/audio_info.py`) | 5.93 s / 3.70 s / 20.54 s; pacing 140 words/min |
| Audio pronunciation | — | **NOT VERIFIED** — nothing here can listen; the owner must check *ODDCHAPTER* against the guide |
| Font licensing | `LICENSE` inside each `@fontsource` package | Space Grotesk + Inter = SIL OFL 1.1 |

---

## 3. The identity in one paragraph

A closed **O** and a **C** with an 84° mouth, same 13-unit stroke, overlapping by 9 units so their
edges meet in a lens — the only "turn" in the mark, and the reason it is called LINK. Ink
`#17191D` ground, Ivory `#F4F0E8` figure, Signal Orange `#F26A3D` used once per composition, Sage
`#A7B0A1` for hairlines. Space Grotesk 700 wordmark at +0.02 em, Inter 600 tagline at +0.17 em
under an orange rule. Total build in motion: 1.2 s, then a hard cut.

---

## 4. How to use it (the 60-second version)

1. **Avatar** → `02_YOUTUBE/avatar/YOUTUBE_AVATAR_800.png`
2. **Banner** → `02_YOUTUBE/banner/YOUTUBE_BANNER_2560x1440.png` (nothing to crop; the lockup is inside every device's safe area)
3. **Watermark** → `02_YOUTUBE/watermark/WATERMARK_LIGHT_150.png`
4. **Thumbnail** → open a `TEMPLATE_*` SVG, drop the still into `id="image-slot"`, retype the headline, export 1280 × 720
5. **Social** → `SOCIAL_PROFILE_1024.png`, `SOCIAL_HEADER_DARK.png`, `SOCIAL_POST_1080.svg`
6. **Everything else** → `01_LOGO/LOGO_SYSTEM.md` §2 tells you which file for which surface

---

## 5. Rebuilding

```bash
npm install                                  # resvg rasteriser (git-ignored)
pip3 install fontTools brotli                # glyph → outline conversion
bash tools/fetch_fonts.sh                    # OFL fonts → .build/ (git-ignored)
python3 tools/build_system.py                # logo + motion SVGs
python3 tools/build_channel.py               # YouTube + social SVGs
python3 tools/build_thumbs.py                # thumbnail SVGs
python3 tools/build_sheets.py                # storyboard, usage sheet, contact sheet
bash tools/render_all.sh                     # every PNG at its documented size
```

---

## 6. Open items and honest limits

| Item | State |
|---|---|
| **Original visual reference** | Never supplied. Nothing in these documents claims to measure it. The written brand spec was treated as authoritative. |
| **MP4 / Lottie** | Still not produced: this host has no `ffmpeg` and installing one was not approved. The build **is** delivered as a rendered 38-frame GIF, a 1920 poster and a self-contained SMIL file, and `tools/build_motion.py` holds the exact frame source — an editor can export a master from any of those in one step. |
| Stories / reels (1080 × 1920) | Delivered in Phase 7 as real 9:16 layouts, not crops of the square. Animated story templates are not produced (they need their own timing pass). |
| Print colour | Artwork is delivered as **mm-authored SVG**, not PDF/X. CMYK builds in `07_PRINT/PRINT_SPEC.md` are naive conversions, not ICC-managed; the spot match for Signal Orange (Pantone 1655 C / 172 C) is **UNKNOWN until proofed**. |
| Audio masters | The delivered MP3s are 24 kHz mono reference reads. A broadcast master needs a 48 kHz/24-bit re-record from the same scripts. |
| Sonic logo | Not produced — a musical mark needs a composer or a music model; the spoken signature is the substitute. |
| Font files | Deliberately not bundled (OFL prefers linking). Install Space Grotesk + Inter locally to edit the *templates*; the logo files need neither. |
| Anything uploaded | Nothing has been uploaded, published or connected to a channel account. |

---

## 7. Recommended next steps

1. Load the four channel assets and check the avatar against real videos at 100 % on a phone.
2. Approve or adjust the thumbnail headlines — the layouts are locked, the copy is a sample.
3. Commission one 8-second opener from `04_MOTION/MOTION_IDENTITY.md` (the spec is complete enough to hand to an editor without further decisions).
4. When the reference image arrives, add it to `BRAND_DIRECTION.md` §2 as an appendix; it changes nothing already built unless the owner asks for a re-derivation.
