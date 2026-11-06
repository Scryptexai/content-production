# ODDCHAPTER — Final Delivery Report

**Date:** 2026-11-07 · **Scope:** Phases 1–6 of the brand identity brief
**Status:** Complete and verified, with the open items in §6.

---

## 1. What you have

A production brand system, not a folder of pictures. Every mark is generated from one geometry
source (`tools/brand.py`), so the logo, avatar, banner, thumbnails, watermarks and motion layers
cannot drift apart. Change a radius there and the whole set rebuilds consistently.

| Folder | Contents | Files |
|---|---|---|
| `01_LOGO/` | monogram + lockup masters, dark/light/mono variants, tagline versions, square icon, compact avatar + `LOGO_SYSTEM.md` | 14 SVG · 12 PNG |
| `02_YOUTUBE/` | avatar, banner, crop check, 2 watermarks, 3 thumbnail systems | 9 SVG · 11 PNG |
| `03_SOCIAL/` | profile, 2 headers, post template | 4 SVG · 4 PNG |
| `04_MOTION/` | 3 layer files + storyboard + `MOTION_IDENTITY.md` | 4 SVG · 1 PNG |
| `05_PREVIEWS/` | concept overview, small-size test, approved refinement, usage sheet, contact sheet | 8 |
| `06_EXPORTS/` | favicons 512/192/32, transparent icon 512, primary logo 2000 | 5 PNG |

Total: **46 SVG · 49 PNG · 11 documents.** Everything is on the branch and reproducible.

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
| Animated files (MP4 / Lottie) | **Not produced.** The storyboard and layer SVGs are the specification; rendering an animation needs a motion tool or a build step that is outside this package's toolchain. |
| Stories / reels (1080 × 1920) | Not produced — derive from the 1080 square rather than improvising safe areas. |
| Print-ready PDF / CMYK | Not produced. The SVGs are the print source; convert to CMYK at the printer's profile and test the orange (`#F26A3D` sits outside CMYK gamut and will shift). |
| Font files | Deliberately not bundled (OFL prefers linking). Install Space Grotesk + Inter locally to edit the *templates*; the logo files need neither. |
| Anything uploaded | Nothing has been uploaded, published or connected to a channel account. |

---

## 7. Recommended next steps

1. Load the four channel assets and check the avatar against real videos at 100 % on a phone.
2. Approve or adjust the thumbnail headlines — the layouts are locked, the copy is a sample.
3. Commission one 8-second opener from `04_MOTION/MOTION_IDENTITY.md` (the spec is complete enough to hand to an editor without further decisions).
4. When the reference image arrives, add it to `BRAND_DIRECTION.md` §2 as an appendix; it changes nothing already built unless the owner asks for a re-derivation.
