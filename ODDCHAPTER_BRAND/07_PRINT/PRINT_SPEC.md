# ODDCHAPTER — Print Specification

**Phase 8** · every file here is authored in **millimetres** (`viewBox` in mm, 1 unit = 1 mm).
A printer gets measurements, not pixels. Open any SVG and the width reads `210mm`, not `2480px`.

---

## 1. Files

| File | Trim | Canvas (incl. bleed) | Notes |
|---|---|---|---|
| `stationery/BUSINESS_CARD_FRONT_91x61.svg` | 85 × 55 mm | 91 × 61 mm | Ink field, lockup 66 mm wide |
| `stationery/BUSINESS_CARD_BACK_91x61.svg` | 85 × 55 mm | 91 × 61 mm | Ivory, monogram 11 mm, tagline |
| `stationery/LETTERHEAD_A4_210x297.svg` | A4 | A4 (no bleed needed) | Ivory field, footer rule at 258 mm |
| `poster/POSTER_A2_420x594.svg` | 420 × 594 mm | 426 × 600 mm | headline is outlined, not live text |
| `merch/STICKER_DIECUT_75mm.svg` | Ø 75 mm | 81 × 81 mm | die line on `id="die-line"`, magenta |
| `merch/TEE_ART_A3_297x420.svg` | A3 print area | A3 | one colour, chest placement at 150 mm |
| `one_colour/LOGO_100K.svg` | — | 150 × 26.6 mm | single ink, 100 % K, lockup 140 mm wide |
| `one_colour/MONOGRAM_100K.svg` | — | 38 × 24.5 mm | single ink, 100 % K, monogram 30 mm |
| `PRINT_SCALE_TEST.svg` | — | 180 × 90 mm | print at 100 % to check minimum sizes |

**Bleed** is 3 mm on every edge of the card, poster and sticker. **Trim is never drawn** into the
artwork — the printer's marks are added at output. The sticker is the one exception: its die line
must be a separate spot layer, which is why it carries `id="die-line"`. Delete that group or
convert it to a die layer before sending; do not let it print.

---

## 2. Colour

Process builds below are converted from the brand HEX values with a naive recipe (no ICC profile).
They are **starting points to proof, not a press-ready colour-managed match**.

| Token | HEX | CMYK build | Print note |
|---|---|---|---|
| Ink | `#17191D` | 21 / 14 / 0 / 89 | For large solid areas use a **rich black 60 / 50 / 40 / 100** — a 21/14/0/89 build looks grey and blotchy over a full card. For small text use **100 K only**. |
| Ivory | `#F4F0E8` | 0 / 2 / 5 / 4 | The warm cast is the point; on uncoated stock it will go slightly creamier. Good. |
| Signal Orange | `#F26A3D` | 0 / 56 / 75 / 5 | **Out of CMYK gamut.** Process will print duller and redder. Options: accept the shift, or match a spot ink and proof it. |
| Sage | `#A7B0A1` | 5 / 0 / 9 / 31 | Only ever hairlines, captions, dividers. Never body text at small size. |
| One colour | `#000000` | 0 / 0 / 0 / 100 | Stamps, foils, single-ink merch, faxes, embroidery thread match. |

**Spot colour for the orange** — candidates to proof, not verified matches: *Pantone 1655 C* and
*Pantone 172 C*. Neither was measured against a physical swatch here (no spectrophotometer, no
Pantone library in this environment). Treat this as LIKELY and settle it on a drawdown with your
printer. If a spot is not possible, the process build above is what the job gets.

**Rules**

- Never place the orange wordmark on paper; the logo is Ink or Ivory, the orange is one rule or one
  chip. Same rule as screen — see `01_LOGO/LOGO_SYSTEM.md` §5.
- Total ink coverage: keep the Ink field under 320 %. The rich black above sits at 250 %.
- Reverse type (Ivory on Ink) below 8 pt needs a coated stock or it fills in.

---

## 3. Minimum sizes (print)

| Asset | Minimum | Floor |
|---|---|---|
| Monogram | 8 mm | 6 mm |
| Horizontal lockup | 60 mm | 50 mm |
| Lockup with tagline | 105 mm | 90 mm |
| Clear space | 13.3 % of the monogram height | — |

`PRINT_SCALE_TEST.svg` is the only meaningful test: print it at **100 %**, no scaling, and look at
the 8 mm mark at arm's length. At 5 mm the junction lens closes into a blob — that mark is on the
sheet, labelled, so you can see it rather than take my word for it.

---

## 4. Stock (suggestions, to confirm with the printer)

| Item | Suggested stock | Why |
|---|---|---|
| Business card | 400–600 gsm uncoated, or 350 gsm triplex | The Ink field wants body; uncoated keeps it editorial rather than corporate |
| Letterhead | 100–120 gsm uncoated | It has to take a pen and a printer without cockling |
| Poster | 170–200 gsm uncoated | Matte holds the Ink field; gloss would turn it into an ad |
| Sticker | 6-year outdoor vinyl, matte laminate | The Ink circle shows scratches on gloss |
| Tee | 180–220 gsm cotton, one-colour screen print | 100 K only; a plastisol white underbase would kill the line weight |

Finishing: blind emboss or deboss the monogram only — **never** the wordmark or tagline (the
letterforms are too fine below 0.4 mm relief). Foil: match the monogram only.

---

## 5. Verification performed here

| Check | Method | Result |
|---|---|---|
| Physical dimensions | parse `viewBox` + `width`/`height` in mm on every file | correct, mm-authored |
| Bleed | canvas − trim = 3 mm per edge (card, poster, sticker) | VERIFIED |
| Type sizes | quoted in points, converted at 0.352778 mm/pt in code | VERIFIED |
| Poster headline fit | outlined and auto-fitted to the margin (first render overflowed the trim — fixed) | VERIFIED |
| Minimum-size sheet | rendered and inspected; 5 mm labelled TOO SMALL | VERIFIED |
| Colour | naive RGB→CMYK conversion, computed here | values above; **not** ICC-managed |
| Spot Pantone match | — | **UNKNOWN** — must be proofed |

Previews: `previews/*_PREVIEW.png` — card and sticker at 300 dpi, letterhead at 150 dpi, A2 at ~90 dpi (screen review only). They are
for review on screen; the SVG is the master and the printer's RIP does the real output.

---

## 6. Rebuilding

```bash
python3 tools/build_print.py
bash tools/render_all.sh        # also re-renders the print previews
```

Typography inside print artwork: display lines are **outlined** (`fit_size()` + `outline()` in
`tools/build_print.py`), body and caption lines are **live text** so the studio can edit names,
addresses and dates without redrawing. Same rule as the digital templates.
