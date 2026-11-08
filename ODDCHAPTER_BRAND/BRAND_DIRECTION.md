# BRAND_DIRECTION.md
### ODDCHAPTER — Phase 1: Brand Reference Analysis & Direction

**Status:** Phase 1 complete, confirmed against the written specification.
Phase 2 delivered; **concept 01 LINK approved** (2026-11-06). Refinement preview awaiting approval.
**Owner of final decisions:** project owner
**Prepared by:** Brand Design & Visual Identity Engineering

---

## 0. Approved specification (authoritative)

Confirmed by the project owner on 2026-11-06. Where anything in this document disagrees with this
table, this table wins.

| Field | Approved value | Confidence |
|---|---|---|
| Brand | ODDCHAPTER | **VERIFIED** — supplied |
| Category | real-storytelling media | **VERIFIED** — supplied |
| Visual direction | modern minimal | **VERIFIED** — supplied |
| Logo direction | OC monogram | **VERIFIED** — supplied |
| Selected concept | **01 LINK** | **VERIFIED** — owner decision |
| Ink | `#17191D` | **VERIFIED** — supplied |
| Ivory | `#F4F0E8` | **VERIFIED** — supplied |
| Signal Orange | `#F26A3D` | **VERIFIED** — supplied |
| Sage | `#A7B0A1` | **VERIFIED** — supplied |
| Primary type | Space Grotesk | **VERIFIED** — supplied and font files inspected |
| Secondary type | Inter | **VERIFIED** — supplied and font files inspected |
| Primary tagline | REAL STORIES. UNEXPECTED CHAPTERS. | **VERIFIED** — supplied |
| Indonesian tagline | KISAH NYATA. DI LUAR DUGAAN. | **VERIFIED** — supplied; kept out of the primary lockup by owner decision |
| Reference image | **does not exist** | **VERIFIED** — owner confirmed it is not available |

Confidence labels used throughout: **VERIFIED** (inspected or tested in this environment) ·
**LIKELY** (well supported, not fully proven) · **ASSUMPTION** (working assumption, correctable) ·
**UNKNOWN** (requires the owner).

---

## 1. Inputs and provenance

| Input | Status | Note |
|---|---|---|
| Brand brief (positioning, promise, taglines, palette, type, logo direction) | **VERIFIED** — supplied in full | Treated as the authoritative source. |
| ODDCHAPTER visual reference image | **UNKNOWN — not received** | No image file exists in the repository or the working session. See §2. |
| Existing brand assets (previous logos, templates) | **UNKNOWN** | None found in the repository. |
| Channel / audience data (existing videos, competitors) | **UNKNOWN** | Not supplied; not required for Phase 1–2. |

> **There is no reference image in this workspace.** I did not invent one and I did not
> describe an image I have not seen. Everything below is derived from the written brief plus
> category observation, and every statement that would normally come from the reference image
> is labelled **ASSUMPTION** until the file is supplied.

---

## 2. Reference-image protocol (when the file arrives)

When the reference is provided, this document is revised with a real analysis, in this order:

1. **Extract the palette actually used** — sample HEX values, compare against Ink / Ivory /
   Signal Orange / Sage, and record drift.
2. **Measure the monogram** — cap-height ratio, stroke weight, counter size, optical balance.
3. **Diagnose before recreating** — list what breaks at small size, what reads as another
   category (horror, gaming, generic AI), what is decorative rather than structural.
4. **Decide what to keep, what to rebuild** — a reference is a *direction*, never a master.

Until then, §3 is the working direction.

---

## 3. Direction extracted from the approved brief

### 3.1 Brand personality, translated into design rules

| Perception target | Design consequence |
|---|---|
| Modern | No bevels, no drop shadows, no gradients, no outlines. Flat geometry only. |
| Intelligent | Generous negative space; one idea per asset; typographic hierarchy does the work. |
| Curious | Asymmetry and open forms are allowed; perfect symmetry is not required. |
| Editorial | Rules, margins, captions, and a strict grid — magazine logic, not poster logic. |
| Cinematic | High contrast, dark-first compositions, colour used as a single accent. |
| Credible | No horror iconography, no sensational effects, no fake "premium" shine. |
| Memorable | One repeatable silhouette that survives a 48 px circle. |

### 3.2 Colour relationships (the rule that keeps the brand from drifting)

Colour is the fastest way this brand could go wrong. Signal Orange is an **accent**, not a
palette. Working ratios for any single composition:

| Role | Token | HEX | Target share of a composition |
|---|---|---|---|
| Ground | Ink | `#17191D` | **65 – 80 %** (dark-first) |
| Text / figure | Ivory | `#F4F0E8` | **15 – 25 %** |
| Accent | Signal Orange | `#F26A3D` | **≤ 8 %** — one accent per frame |
| Support | Sage | `#A7B0A1` | **0 – 10 %** — lines, captions, dividers only |

Rules:
- Orange never fills a background, never sets body copy, never appears twice as a focal point.
- Sage never competes with orange in the same composition; choose one.
- Light variants invert ground and figure (Ivory ground, Ink figure) and keep the same accent discipline.
- **VERIFIED** contrast, computed with the WCAG 2.1 relative-luminance formula
  (`tools/` calculation, HEX values from the brief):

| Pair | Ratio | Permitted use |
|---|---|---|
| Ivory on Ink | 15.48 : 1 | Body text, all sizes |
| Ink on Ivory | 15.48 : 1 | Body text, all sizes |
| Sage on Ink | 7.85 : 1 | Captions, dividers, secondary labels |
| Orange on Ink | 5.79 : 1 | Headline-size text and graphics only |
| Orange on Ivory | 2.68 : 1 | **Graphics only — never text** |
| Sage on Ivory | 1.97 : 1 | **Hairlines and support shapes only — never text** |

  The two failing pairs are the practical reason Sage never carries words on a light ground,
  and why the accent on light backgrounds is used as a shape, not a caption colour.

### 3.3 Typography direction

- **Space Grotesk** — display, wordmark, titles, numbers. Geometric, slightly odd terminals; the
  "odd" in ODDCHAPTER is carried here, not by decoration.
- **Inter** — body, captions, UI, subtitles. Neutral, highly legible at small sizes.
- Locked behaviours: wordmark always uppercase, tracked (≈ +0.02 em at monogram scale),
  never condensed, never outlined, never on a curved path.
- **VERIFIED** — both families were fetched from official OFL packages and inspected;
  the ODDCHAPTER wordmark used in Phase 2 is generated from real Space Grotesk Bold glyph
  outlines, not traced or imitated.

### 3.4 Composition and hierarchy

- **Hierarchy:** monogram → wordmark → tagline → story content. Nothing in that chain may
  compete with the level above it.
- **Grid:** 100-unit construction grid for the monogram; 8 px baseline for layout; 12-column
  logic for thumbnails and banners.
- **Contrast:** one dominant subject per frame; secondary elements at ≤ 40 % of the dominant mass.
- **Density:** maximum one text block plus one logo per thumbnail; no stacked labels.

---

## 4. Category risks this direction is designed to avoid

Each is a real failure mode for "real-storytelling" channels. **LIKELY** — based on category
observation, not on a supplied reference.

| Failure mode | How it looks | Guardrail in this system |
|---|---|---|
| Horror-channel drift | Red/black, distressed type, eyes, hands, film grain | Orange, not red; clean geometry; no symbols of fear |
| Generic AI-channel look | Neon gradient meshes, glow, 3D chrome letters | Flat 4-colour system; no gradients or glows permitted |
| Gaming / esports | Angular aggressive marks, over-outlined type | Circular geometry, no outlines, no skewed type |
| Children's animation | Rounded blobs, saturated multi-colour | One accent only; strict palette count |
| Tech-startup | Blue gradients, abstract "network" dots | No blue in the palette; no generic tech motifs |
| Classroom / presentation | Bullet-point slides, clip-art icons | Editorial layout logic; no clip-art, no icon sets |
| Over-templated thumbnails | Same layout on every video | Three structurally different thumbnail systems (Phase 4) |

---

## 5. Monogram direction brief (input to Phase 2)

Derived from §3, and used as the scoring criteria for the three concepts:

1. Geometric construction — describable with radii, centres and angles.
2. Clear silhouette at 48 × 48 px and inside a circular crop.
3. The O and the C must be **structurally joined** (shared geometry, shared gap, or a real
   junction) — never two letters simply placed next to each other.
4. Single-colour capable; no gradient, outline or raster dependency.
5. Simple enough to animate in under 1.5 s without a bespoke rig.
6. Works without the wordmark, and works as an 800 px avatar.

**Explicitly excluded:** books, eyes, brains, AI symbols, cameras, horror symbols, decorative
gradients, excessive outlines.

---

## 6. Open questions for the owner

| # | Question | Why it matters | Default if unanswered |
|---|---|---|---|
| 1 | Where is the reference image? | Phase 1 re-analysis | Continue from brief |
| 2 | Indonesian tagline in the logo lockup, or English primary only? | Lockup design in Phase 3 | English primary, Indonesian in end-cards |
| 3 | Final channel name spelling/casing on platform | Wordmark lockup | ODDCHAPTER, all caps |
| 4 | Will the brand use photography, illustration, or archive material in thumbnails? | Phase 4 image treatment | Assume mixed, design for both |

**UNKNOWN** items are not blocking Phase 2; they become blocking at Phase 3 (lockup) and Phase 4 (thumbnails).
