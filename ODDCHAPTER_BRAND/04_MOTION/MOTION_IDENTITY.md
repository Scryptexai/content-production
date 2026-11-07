# ODDCHAPTER — Motion Identity

**Status:** Phase 5 spec + Phase 7 delivery
**Reference sheet:** `animation_reference/ANIMATION_STORYBOARD.png` (2400 × 1680)
**Rendered proof:** `preview/OPENER_BUILD_960x540.gif` · `preview/OPENER_POSTER_1920x1080.png`

ODDCHAPTER does not do logo stings. The identity animates the way an editor cuts: something
arrives, it locks, and we leave. Total build **1.2 s**, then a **0.3 s** hold and a hard cut into
the episode. No dissolve, no zoom, no particle reveal.

---

## 1. Timing

| # | Time | State | Duration |
|---|---|---|---|
| 1 | 0 ms | Monogram scales 92 → 100 %, opacity 0 → 100 | 180 ms |
| 2 | 180 ms | Junction locks; hold | 120 ms |
| 3 | 300 ms | Wordmark wipes in left to right behind a clip path | 240 ms |
| 4 | 540 ms | Orange rule draws 0 → 100 % width | 180 ms |
| 5 | 720 ms | Tagline rises 12 px and fades in | 180 ms |
| 6 | 900 ms | Hold the finished lockup | 300 ms |
| — | 1200 ms | **Cut** to the opening scene | — |

## 2. Easing

| Element | Curve | Note |
|---|---|---|
| Monogram, wordmark, tagline | `cubic-bezier(.2, .7, .2, 1)` | decelerating, no overshoot |
| Orange rule | `linear` | it is a measurement, not a gesture |
| Nothing | `ease-in-out`, bounce, elastic | a true story does not spring |

## 3. Rules

- **Orange animates exactly once** — the rule. Nothing else changes colour during the build.
- The monogram **never** rotates, spins, pulses or draws itself in pieces; the O and the C arrive
  together because they are one shape.
- No sound design on the build. If the episode has audio, it starts after the cut.
- The end state must be **pixel-identical** to `01_LOGO/dark/LOGO_DARK_TAGLINE.svg`. If a frame of
  the render differs from the static master, the animation is wrong.
- Never stretch, squash, or animate the monogram and wordmark independently after state 3.

## 4. Layers

`svg_components/` holds the pieces an animation tool needs, each with a stable id:

| File | Contents |
|---|---|
| `monogram_layers.svg` | `#layer-o` (closed ring) and `#layer-c` (arc + mouth), same canvas, aligned |
| `wordmark_layer.svg` | `#wordmark` — outlines, origin at the baseline start |
| `tagline_layer.svg` | `#tagline` — outlines, origin at the baseline start |

All three are pure outlines, so they import into After Effects, Rive, Lottie or Anime.js without a
font install and without text-conversion artifacts.

## 5. Where it is used

| Surface | Build | Notes |
|---|---|---|
| Episode opener | full 1.2 s | then cut to scene 1 |
| End card | full lockup, static | no build — the card is already on screen |
| Shorts / vertical | monogram only, 180 ms | no wordmark under 420 px width |
| Social video watermark | static | see `02_YOUTUBE/watermark/` |

---

## 6. Delivered motion files

| File | What it is | State |
|---|---|---|
| `preview/OPENER_BUILD_960x540.gif` | the build, **38 frames at 25 fps**, rendered from this timing spec | VERIFIED — frames inspected, 960 × 540, 18 KB |
| `preview/OPENER_POSTER_1920x1080.png` | the final state at 1.2 s, full size | VERIFIED — 1920 × 1080 |
| `preview/OPENER_ANIMATED.svg` | the same build as declarative SMIL, self-contained | VERIFIED structure (well-formed, timing matches); it is **not** rendered by resvg, which does not evaluate SMIL |
| `svg_components/*.svg` | the layer sources for After Effects / Rive / Lottie | VERIFIED — outlines only, stable ids |

The GIF is the proof that the timing reads correctly at 25 fps. The SMIL file is the version you
can drop straight into a web page or hand to an editor who has no motion tool; the GIF is the
version you can send to someone who has nothing at all.

### Why there is no MP4

There is no `ffmpeg` on this machine, and installing one is outside what was approved. The GIF and
the frame sequence in `tools/build_motion.py` are the complete source of truth: any editor can
export a ProRes or H.264 master from `OPENER_ANIMATED.svg` or from the frame sequence in one step.
If an MP4 is required, the honest answer is that it needs a render box with ffmpeg — the design
decisions are all already made.

### Rebuilding

```bash
python3 tools/build_motion.py     # SMIL + poster + 38 frames + GIF
```

Change the four timing constants at the top of `tools/build_motion.py` and the GIF, the poster and
the SMIL file all move together — the same single-source rule as the static assets.
