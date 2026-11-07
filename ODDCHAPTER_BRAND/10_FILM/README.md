# 10_FILM — ODDCHAPTER_PILOT_001

A real, rendered vertical film: **1080×1920, 29.2 s, 30 fps, H.264 / AAC**,
−14 LUFS, −1.5 dBTP, Indonesian narration, burned-in Indonesian captions.
It is a **brand pilot**, not an episode: it makes no factual claim, and the
diagram plate is explicitly labelled as a mechanism illustration.

| cut | file | use |
|---|---|---|
| clean | `final/ODDCHAPTER_PILOT_001_1080x1920_29s.mp4` | YouTube long-form, embeds, press |
| captioned | `final/ODDCHAPTER_PILOT_001_CAPTIONS_1080x1920_29s.mp4` | **publish master** — Shorts, Reels, TikTok |
| cover | `final/ODDCHAPTER_PILOT_001_POSTER_1080x1920.png` | thumbnail / cover frame (26.4 s) |
| subtitles | `captions/ODDCHAPTER_PILOT_001.id.srt` | source of the burned-in cues |

## Structure (29.2 s)

| time | beat | made with |
|---|---|---|
| 0.0–2.0 | monogram settles, wordmark wipes in | Remotion `interpolate` + clip-path |
| 2.0–8.0 | “Setiap minggu, satu kisah nyata…” | type scene, staggered rise |
| 8.0–14.0 | “LEBIH ANEH…” | type scene, 190 px display |
| 14.0–22.2 | stratified-lake mechanism plate | **d3** scales + `curveBasis`, SVG |
| 22.2–29.2 | end card: marks + tagline | Remotion, outlined marks |

Hard cuts only (`<Series>`). `@remotion/transitions` is installed and exercised in
the `TEST-TRANSITION` composition, then deliberately unused in the film: the brand
forbids dissolves.

## Pipeline

```
brand.py ─► src/brand.json ─┐
audio/*.wav ───────────────┤
captions/*.srt ─► cues ────┴─► Remotion composition ─► bundle ─► @sparticuz/chromium
                                                                    │
      final MP4 ◄─ ffmpeg (loudnorm −14 LUFS, AAC 192k, faststart) ◄─┘
```

```bash
cd ODDCHAPTER_BRAND/10_FILM/remotion
npm install                       # exact pins, no carets
npm run test:browser              # proves the Chromium binary works on its own
npm run dev                       # Remotion Studio on :3333
npm run preview                   # stills at key frames → output/preview_*.png
npm run render                    # still → transition test → 3 s test → both cuts
npm run validate                  # ffprobe + loudness gate, 10 checks
python3 /workspace/ODDCHAPTER_BRAND/tools/fix_font_names.py   # once per fresh sandbox
```

`npm run render` refuses to encode the full film until the 1-frame still, the
1 s transition and the 3 s test video have rendered and been probed.

## Tool status — installed / tested / integrated / used

| tool | version | installed | tested | integrated | in final render |
|---|---|---|---|---|---|
| Remotion | 4.0.541 | ✅ | ✅ | ✅ | ✅ |
| @remotion/{cli,bundler,renderer} | 4.0.541 | ✅ | ✅ | ✅ | ✅ |
| @remotion/transitions | 4.0.541 | ✅ | ✅ | ✅ (test comp) | ❌ by design |
| @remotion/captions | 4.0.541 | ✅ | ✅ (`parseSrt`) | ✅ | ✅ captions |
| React / react-dom | 18.3.1 | ✅ | ✅ | ✅ | ✅ |
| @sparticuz/chromium | 153.0.0 | ✅ | ✅ | ✅ | ✅ **rendered the film** |
| puppeteer-core | 25.16.0 | ✅ | ✅ | ✅ (browser test) | ❌ (Remotion drives the browser) |
| d3 | 7.9.2 | ✅ | ✅ | ✅ | ✅ diagram geometry |
| ffmpeg (static) | 4.x via `@ffmpeg-installer` | ✅ | ✅ | ✅ | ✅ master + loudness |
| ffprobe | 6.x via `@ffprobe-installer` | ✅ | ✅ | ✅ | ✅ validation |
| GSAP / Lottie / Lucide | — | ❌ | — | — | not needed; nothing depends on wall-clock time |
| node-canvas / sharp | — | ❌ | — | — | no raster image layers in this film |

**The browser that actually rendered this file: `@sparticuz/chromium` 153.0.8010.0**
(`HeadlessChrome/153.0.8010.0`), resolved from the npm package, run with its own
`al2023` shared libraries (`scripts/chromium.mjs` decompresses `al2023.tar.br` and
sets `LD_LIBRARY_PATH`; without them the binary exits 127 — that is the only
non-obvious step in the whole pipeline). Remotion reaches it through
`browserExecutable`, the documented option in `@remotion/renderer`.

System Chromium is **not** installed in this image and was not needed; the
documented fallback would be `--browser-executable` pointing at any Chrome ≥ 120.

## Measured output

```
container   mp4 (mov,mp4,m4a)      video  h264 · 1080×1920 · 30/1 · yuv420p
audio       aac · 48 kHz · 2 ch    duration 29.20 s
loudness    −13.99 LUFS            true peak −1.48 dBTP
size        1.2 MB (captioned cut)
```

`npm run validate` runs 10 checks and exits non-zero on any failure.

## Decisions

1. **Narration is the cut.** Cue and scene boundaries come from the measured
   speech onset/offset of each WAV (20 ms window, peak threshold), never from a
   word-count estimate.
2. **Marks are outlines, not text.** `tools/export_brand_json.py` writes the same
   geometry `tools/brand.py` uses for the SVG masters, so the film cannot drift
   from the identity.
3. **Captions come from the SRT.** `scripts/prepare-assets.mjs` parses
   `captions/*.id.srt` with `@remotion/captions`; there is no second copy of the
   cue list in code.
4. **The diagram carries its own disclaimer** — mechanism illustration, no
   event reconstruction, no numbers, because no source is cited on screen.
5. **No fonts in git.** `public/fonts` is generated; Space Grotesk and Inter are
   SIL OFL 1.1 and stay linked, not vendored.
6. **`build_film.py` is the fallback path** — a pure SVG→resvg→ffmpeg renderer for
   the same film, kept because it needs no browser. The delivered file was *not*
   made with it.

## Known limits

- The film is 29 s of brand + one explanatory plate; it is not a documentary and
  contains no sourced case. Supplying a story and sources is what unlocks a real
  episode (`tools/episode.py new <slug>`).
- The end card shows the English master tagline `REAL STORIES. UNEXPECTED
  CHAPTERS.` while the voice says the Indonesian line. Switching the on-screen
  tagline to `KISAH NYATA. DI LUAR DUGAAN.` is a one-line change in
  `tools/export_brand_json.py`, but it changes an approved brand asset — waiting
  for a decision.
- Loudness is normalised on the mixed narration, so a future music bed must be
  re-mixed before `linear=true` stays valid.
