# CONCEPT_NOTES.md
### ODDCHAPTER — OC monogram, Phase 2

Three directions, one construction grid. Nothing here is a final asset. The owner selects one;
Phase 3 (logo system) starts only after that decision.

- **Construction grid:** 100 × 100 units, circular arcs only, no bezier hand-tuning.
- **Source of truth:** `tools/oclib.py` — the geometry below is generated, never drawn by eye.
- **All marks in this folder are vector and editable.** No generated raster lettering was used.
- **Small-size test shown on the sheet:** 48 px, 32 px, 24 px, rendered at actual size.

| | Concept | Logic | Composition axis | Colour behaviour | Best at |
|---|---|---|---|---|---|
| 01 | **LINK** | Interlock, transparent junction | Horizontal | Single colour by construction | Headers, channel banner, watermark |
| 02 | **STACK** | Stacked ligature, colour bridge | Vertical | One accent (the joint) | Avatar, square/social profile |
| 03 | **CASCADE** | Offset axis, shallow junction | Rising diagonal | Accent on the open letter | Large display, end-cards |

---

## 01 — LINK

**Files:** `concept-01-link/` · dark · light · mono · construction · (svg + png)

### Rationale
Two equal rings of equal weight. Each passes *through* the other: at the crossing, the overlap
is knocked out, so both letters appear interrupted by the same event. The mark says "two chapters,
one continuous story" rather than "two letters next to each other". It is the most neutral and the
most flexible of the three, and the only one that is single-colour by construction.

### Geometric construction
| Parameter | Value |
|---|---|
| Grid | 100 × 100 units |
| Ring outer radius | 27 |
| Counter radius | 14 |
| Stroke weight | 13 (constant) |
| O centre | (29, 50) — closed annulus |
| C centre | (71, 50) — annulus with an 84° mouth facing right |
| Centre distance | 42 → overlap 12 units |
| Junction | intersection of both annuli, produced by `fill-rule="evenodd"` |
| Drawing box | 96 × 54 units (ratio 16 : 9), centred |

The junction is *not* a drawn lens shape. It is the mathematical intersection of two annuli, so it
recomputes exactly at any scale and can never drift out of register.

### Positive / negative space
- **Positive:** two equal masses; neither letter dominates, which reads as balanced rather than dramatic.
- **Negative:** three counters — the O's circle, the C's mouth, and the vertical lens at the junction.
  The lens is the accent of the mark: it is the only asymmetric void, and it points at the C.
- The lens is also the weakest point at small sizes (see Risks).

### Small-size readability
Best of the three. **VERIFIED** (see `05_PREVIEWS/SMALL_SIZE_TEST.png`, rendered at true pixel size
and magnified with nearest-neighbour so the pixels are honest): clean at 48, 32 and 24 px — both
counters survive and the mark still reads "OC". At 16 px the junction lens collapses into a near-solid
sliver, and the mark reads as a slightly fused "OC". It does not break, but 16 px is the floor.

### Light / dark application
- Dark ground: ivory mark. The junction lens becomes a window to Ink — it darkens the centre.
- Light ground: ink mark. The lens reads as a bright opening.
- Single colour: identical to both, because the mark is already one colour.

### Strengths
- Reads as two letters instantly, at every size tested.
- Single-colour native — works in embossing, watermark, favicon, and video lower-thirds.
- Trivially animatable: two arcs can slide together and stop, no masking.
- Horizontal proportions pair naturally with the wordmark.

### Weaknesses / risks
- Closest to a known "linked rings" device; distinctiveness depends on the 84° mouth and the exact
  overlap, so the values are not free to change.
- The junction lens is a fine, high-frequency detail: **VERIFIED** — at 16 px it closes and the mark
  becomes a near-solid block, still legible but no longer elegant.
- The C's mouth (84°) is narrower than a conventional C; at small size it reads slightly like an "O"
  with a notch.

### Lockup implication (Phase 3 preview)
The 96 : 54 box sits comfortably at cap height beside the wordmark, allowing a true horizontal lockup
without vertical compensation.

---

## 02 — STACK

**Files:** `concept-02-stack/` · dark · light · mono · construction · (svg + png)

### Rationale
The letters are stacked and joined by a single Signal Orange rule — the only colour in the mark.
It behaves like an editorial chapter break: a rule between two blocks of type. Compact, quiet,
and the only concept built for a square or circular crop from the start.

### Geometric construction
| Parameter | Value |
|---|---|
| Grid | 100 × 100 units |
| Letter outer radius | 22 |
| Counter radius | 10 |
| Stroke weight | 12 |
| O centre | (50, 23) |
| C centre | (50, 77), mouth 76° facing right |
| Junction | 40 × 9 unit rule, corner radius 4.5, sitting in the exact 10-unit gap |
| Drawing box | 44 × 98 units (ratio ≈ 1 : 2.2) |

The gap between the letters is 10 units — the rule is inset by 0.5 units at each end, so the joint is a
real space with a coloured object in it, not an overlap.

### Positive / negative space
- **Positive:** three masses in a column: disc, bar, disc. Vertical rhythm is the whole idea.
- **Negative:** two counters plus two small notches where the rule meets the letters. The notches
  give the bar the appearance of being *inserted*, which is what makes it read as a joint.
- The bar is the only element that crosses the vertical centre line, which is why it holds the mark together.

### Small-size readability
**VERIFIED** at 48 px and 32 px: clean. At 24 px the rule still reads as a separate object (the
10-unit gap between letters is ≈ 2.4 px at that size), though the letters compress. At 16 px the
orange bar starts to dominate the total height and the mark drifts toward a figure-eight reading —
**STACK should not be used below 24 px.**

### Light / dark application
- Dark ground: ivory letters, orange rule — the strongest version of the mark.
- Light ground: ink letters, orange rule — the rule loses contrast (2.68 : 1) but it is a graphic
  element, not text, so this is within the rules set in `BRAND_DIRECTION.md` §3.2.
- Single colour: the rule merges into ink; the letters still read, the joint becomes a gap.

### Strengths
- Best avatar behaviour: a vertical, self-contained block that fills a circular crop evenly.
- The orange rule is a ready-made motion device — it can draw on, wipe, or slide in.
- Nothing decorative: the accent *is* the structure.

### Weaknesses / risks
- The tall 1 : 2.2 box needs optical down-scaling in a horizontal lockup; the wordmark cannot simply
  be set at the monogram's cap height.
- Without the orange rule the mark loses its idea; in strict single colour it is two letters with a gap.
- Slight risk of reading as a figure-eight in very small favicon use. **VERIFIED** at 16 px — the
  orange bar dominates and the letterforms compress. Must not be used below 24 px.

---

## 03 — CASCADE

**Files:** `concept-03-cascade/` · dark · light · mono · construction · (svg + png)

### Rationale
Same two letters, but placed on a rising diagonal and joined at a shallow overlap, so the pair reads as
one object in motion — a chapter that hands over to the next. The accent is assigned to the *open*
letter, which gives a colour logic rather than a decoration: orange marks the opening, not the frame.

### Geometric construction
| Parameter | Value |
|---|---|
| Grid | 100 × 100 units |
| Outer radius | 27 |
| Counter radius | 14 |
| Stroke weight | 13 |
| O centre | (29, 61) |
| C centre | (72, 35), mouth 84° facing right |
| Centre distance | 50 → 4-unit overlap |
| Drawing box | 97 × 80 units, diagonal axis 28° |

### Positive / negative space
- **Positive:** two equal rings, one raised — the eye travels up-right, which is the direction the
  brand wants the audience to move.
- **Negative:** the overlap creates a narrow shared zone; because the overlap is only 4 units, the
  waists that pinch are small and the two counters stay separate — that is what keeps the letters legible
  in colour.

### Small-size readability
**VERIFIED** at 48 px and 32 px — and at 48 px it is the most instantly readable "OC" of the three.
At 24 px the two letters begin to fuse at the junction; at 16 px the mark reads as a single link
shape. **CASCADE's floor is 32 px.**

### Light / dark application
- Dark ground: orange O, ivory C. The accent sits on the *second* letter, so the composition still moves up-right.
- Light ground: orange O, ink C. Highest contrast version; the orange is a shape, never text.
- Single colour: the letters fuse into one silhouette — the reading drops to "a linked pair".
  **This is the concept's weakest state and should be avoided** (see Risks).

### Strengths
- Most distinctive silhouette of the three at large sizes (banners, end-cards, video stings).
- Colour carries meaning instead of decoration — defensible against "orange accent overload".
- The diagonal gives the motion system an obvious direction to animate along.

### Weaknesses / risks
- **Fails the single-colour requirement in spirit.** The mark depends on colour separation to read as
  two letters. Embossing, fax-grade printing, and some watermark situations would degrade it.
- Asymmetric, so it needs bespoke optical centring in every container (it is not centred by bounding box).
- At 24 px it reads as a chain link rather than "OC".

---

## Comparison and professional recommendation

| Criterion | 01 LINK | 02 STACK | 03 CASCADE |
|---|---|---|---|
| Reads "OC" at 48 px | strong | strong | good |
| Reads "OC" at 24 px | strong | good | weak |
| Single-colour integrity | **best** | good | poor |
| Avatar / circular crop | good | **best** | good |
| Horizontal lockup with wordmark | **best** | needs scaling | good |
| Distinctiveness | medium | medium-high | **high** |
| Motion simplicity | **simplest** | simple | medium |

**Recommendation (for the owner to accept or reject):** **02 STACK** if the channel's first job is
a recognisable avatar and a compact identity; **01 LINK** if the identity must survive the widest range
of reproduction (watermarks, printed material, merchandise, single-colour contexts). **03 CASCADE** is
the most striking but its single-colour weakness is a real long-term cost.

The decision is the owner's. No Phase 3 work has been started.

---

## What Phase 3 will produce from the selected concept

1. `LOGO_MASTER.svg` — horizontal lockup: monogram + ODDCHAPTER wordmark, as outlines, with
   documented construction, clear space, and minimum sizes.
2. `MONOGRAM_MASTER.svg` — standalone mark on the same grid as the concept.
3. Variants: dark, light, monochrome, compact avatar, plus a 48 px pixel-fitted cut.
4. `LOGO_SYSTEM.md` — spacing, clearance, minimum size, and incorrect-usage rules.
5. PNG exports with verified transparency and exact dimensions.
