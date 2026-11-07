# ODDCHAPTER — Audio Identity

**Phase 9** · the last untouched dimension. The identity has a mark, a grid, a palette, a motion
build and a print system. This is how it sounds.

This document does **not** replace `../AUDIO PRODUCTION.md` — that file is the production manual
for voice, music, SFX, ambience and silence. This file takes its voice profile from there and turns
it into brand assets: a spoken signature, a set of recorded reference reads, and the rules for
using them.

---

## 1. The voice, in one line

**A person explaining something they found genuinely strange — not a presenter announcing it.**

The full profile is `AUDIO PRODUCTION.md` §3. The parts that are brand, not episode:

| Property | Brand decision |
|---|---|
| Language | Natural Indonesian (bahasa Indonesia, no regional accent forced) |
| Character | Mature, credible, conversational |
| Pace | Measured — the pause is part of the sentence, not a mistake |
| Emotion | Expressive, controlled. Never theatrical, never outraged |
| Register | Not a newsreader. Not an ad. Not a motivational speaker |
| Recording feel | Close, dry, unprocessed — a room, not a studio booth |

Everything else (per-category delivery for relationship / political / viral subjects) stays in
`AUDIO PRODUCTION.md` §4.

---

## 2. The spoken signature

Two forms. Both are **spoken**, never sung, and both sit on silence — no music bed underneath.

### 2.1 Indonesian — used on air

> **"Kisah nyata. Di luar dugaan. Ini ODDCHAPTER."**

- Measured duration: **5.93 s** (target was 4.5–5.5 s — the extra is the pause after each
  full stop). If a tighter cut is needed, trim the silence, never the words.
- Delivery: first two lines flat and factual, a half-beat between them; the name lands on a
  slightly lower pitch and is **not** emphasised with volume.
- `Di luar dugaan` is the turn — do not smile on it, do not dramatise it.

### 2.2 English — used on the English lockup and for international cuts

> **"Real stories. Unexpected chapters."**

- Measured duration: **3.70 s**.
- Same rule: the turn is in the words, not in the delivery.

### 2.3 Pronunciation

| Written | Spoken |
|---|---|
| ODDCHAPTER | *od-CHAP-ter* (English stress, four syllables collapsed to three) |
| REAL STORIES | *real STO-ries*, no rising terminal |
| KISAH NYATA | *KI-sah NYA-ta*, even stress, no Javanese vowel lengthening |
| DI LUAR DUGAAN | *di lu-AR du-GA-an*, the final syllable is short |

The name is English and stays English even inside an Indonesian sentence — the same way the
wordmark is not translated.

---

## 3. Where audio is allowed

| Surface | Audio | Spec |
|---|---|---|
| Opener (after the 1.2 s build) | spoken signature | 5 s, silence under the mark, voice enters **after** the cut |
| Cold open | narration | no music for the first 15 s |
| Episode body | narration + music + ambience | `AUDIO PRODUCTION.md` §2 |
| End card | none, or the Indonesian signature if the episode ends quiet | never a second signature inside 30 s |
| Shorts / vertical | narration only, no signature | a 5 s signature in a 30 s short is a waste |

Hard rules, same spirit as the visual system:

1. **No music sting under the logo build.** The build is 1.2 s of quiet geometry; a sting turns the
   brand into a trailer.
2. **One signature per episode.** Not at the open and again at the end.
3. **No "subscribe" read.** The end card carries that visually.
4. **Silence is a brand asset.** A minimum of 0.6 s of clean silence before the first word of any
   read — it is what makes the voice sound like it has arrived rather than started.

---

## 4. Mix targets (YouTube)

| Element | Target |
|---|---|
| Programme integrated | −14 LUFS (platform normalises to this; deliver at target, don't fight it) |
| True peak | −1.0 dBTP |
| Narration | −16 LUFS short-term, dry, no reverb, high-pass at 80 Hz |
| Music under narration | −18 to −22 LUFS, sidechain nothing — write the arrangement instead |
| SFX | never louder than the narration syllable it lands on |
| Signature | −16 LUFS, same room as the narration |

These are working targets, not measurements: nothing in this package has been mixed to them yet.
The one real measurement is pacing — **140 words per minute**, taken from the reference read with
its natural pauses included. Write to that number: a 5-minute episode is roughly 700 words.

---

## 5. Delivered audio

| File | Script | Status |
|---|---|---|
| `assets/SIGNATURE_ID.mp3` | Kisah nyata. Di luar dugaan. Ini ODDCHAPTER. | **5.93 s** · 8 words · 24 kHz mono, ~32 kbps |
| `assets/SIGNATURE_EN.mp3` | Real stories. Unexpected chapters. | **3.70 s** · 4 words · same format |
| `assets/COLD_OPEN_SAMPLE_ID.mp3` | 48-word cold-open reference read | **20.54 s** · 140 words/min |

Durations were measured from the MPEG stream itself (frame count × samples per frame), not
guessed — `tools/audio_info.py` prints the numbers above and there is no `ffprobe` on this host.

### Two honest caveats about these files

1. **They are reference quality, not masters.** 24 kHz mono at ~32 kbps is enough to judge timing,
   tone and whether the script works. It is not enough to put on a channel. For broadcast, re-record
   the same scripts at 48 kHz / 24-bit WAV — the scripts above are the master, the MP3s are the
   casting reference.
2. **They have not been checked by ear here.** Timing is measured and correct; pronunciation is
   not verified. Listen specifically for *ODDCHAPTER* (§2.3) — a TTS voice may stress it differently
   from the guide, and no tool in this environment can hear it.

Reads are generated from the exact scripts above, so any producer can re-record them with a human
VO and land on the same timing. The script is the source of truth, not the file.

### Voice record

| Field | Value |
|---|---|
| Voice id | `voice-00` (Arena audition, selected by the owner) |
| Language | Indonesian |
| Use case | narration |
| Registered | Arena voice audition, 2026-11-07 |
| Reference read | `COLD_OPEN_SAMPLE_ID.mp3` — 140 words/min |

---

## 6. What this is not

- **Not a sonic logo.** A musical identity (three notes, a motif, a sound mark) needs a composer or
  a music model; neither exists in this toolchain. The spoken signature is the honest substitute and
  it is the part that carries meaning.
- **Not a finished mix.** No music has been produced or licensed.
- **Not a studio master.** See the caveats in §5.
- **Not a casting decision made for you.** The voice is auditioned, not assumed — the brand docs
  specify the profile, not the person.
