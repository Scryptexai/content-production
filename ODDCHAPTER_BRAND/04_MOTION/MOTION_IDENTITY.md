# ODDCHAPTER — Motion Identity

**Status:** Phase 5 complete · reference only (no animations published)
**Reference sheet:** `animation_reference/ANIMATION_STORYBOARD.png` (2400 × 1680)

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
