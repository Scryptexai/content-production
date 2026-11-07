# ODDCHAPTER — Episode Production Pipeline

**Phase 11.** The brand is settled; this is how an episode gets made with it. Seven stages, each
with a gate you cannot pass by vibes, and each pointing at the knowledge file in the repo root that
governs it.

Nothing here is episode-specific. Fill the templates in `templates/` for each film.

---

## 0. The stack — which file governs what

| Stage | Governing document (repo root) | Brand asset it uses |
|---|---|---|
| Story lock | `EDITORIAL-FONDATION.md`, `STORYTELLING-FONDAMENTAL.md` | — |
| Hook | `HOOK ENGINEERING.md` | — |
| Structure & pacing | `EMOTIONAL-PACING.md`, `NARRATIVE-TENSION-&-AUDIENCE-RETENTION.md` | — |
| Voice | `AUDIO PRODUCTION.md` §3 · `08_AUDIO/AUDIO_IDENTITY.md` | `08_AUDIO/assets/` |
| Visual plan | `VISUAL-STORYTELLING.md` | `02_YOUTUBE/thumbnails/` for the promise |
| Assembly | `VIDEO_,EDITING.md` | `04_MOTION/` build + end card |
| On-screen text | `BRAND_GUIDELINES.md` §3, §8 | `09_EPISODE_KIT/onscreen/` |
| Delivery | this file §7 | `02_YOUTUBE/`, `03_SOCIAL/`, `06_EXPORTS/` |

If two documents disagree, the brand files (`BRAND_GUIDELINES.md`, `LOGO_SYSTEM.md`,
`MOTION_IDENTITY.md`, `AUDIO_IDENTITY.md`) win on anything visible or audible; the knowledge files
win on editorial judgement.

---

## 1. Story lock — gate: every claim has a source

1. One sentence: *who wanted what, what turned, and what it cost.* If you cannot write it, the film
   is not ready.
2. Evidence sheet: each factual claim → source, date, and how it was verified. **Anything without a
   source is cut, not softened.** This is the rule that keeps a "real stories" channel real.
3. Angle: the turn the audience does not expect. One per film.
4. Title candidates: 3, each ≤ 60 characters, none of them a question the film does not answer.
5. Runtime target: 6, 10 or 14 minutes. Decide now — the beat sheet depends on it.

**Gate:** an evidence sheet exists and the one-sentence pitch survives being read aloud.

---

## 2. Beat sheet — gate: the word budget matches the runtime

Use `templates/SCRIPT_BEAT_SHEET.md`. The arithmetic is fixed by the measured pacing of the brand
voice: **140 words per minute** (from the reference read, pauses included).

```
words ÷ 140 = minutes of voice-over
runtime − voice-over = the air you have for silence, B-roll and cards
```

A 10-minute episode carries roughly **1,200–1,300 words of VO**. More than that and you are
podcasting over pictures.

**Gate:** every beat has a word budget, a purpose, and a chapter number. Total = target ± 5 %.

---

## 3. Voice — gate: the read matches the profile, not just the words

Record against `AUDIO IDENTITY.md` §1–§2. Do not rewrite in the booth; if a line does not read,
it was wrong on paper — go back to stage 2.

Checks: 0.6 s of clean silence before the first word · no upward terminal on statements · the
signature is read once, at the end of the cold open, not at the top.

**Gate:** a full read exists at 48 kHz/24-bit WAV, and a spot-check against the reference read
(`08_AUDIO/assets/COLD_OPEN_SAMPLE_ID.mp3`) does not sound like a different channel.

---

## 4. Visual plan — gate: no paragraph is left without an intention

For each beat, one line: what we are looking at, and why *that* image rather than another.
- Prefer the specific object over the generic mood: the logbook, not "the sea".
- Mark which beats need a map, a document, or a re-creation, and which are pure B-roll.
- Any photo of a real person or document must be cleared — note the licence next to the file name.
- Generate nothing that could be mistaken for evidence. Re-creations are labelled on screen.

**Gate:** every VO paragraph has a visual intention; nothing is marked "figure it out in the edit".

---

## 5. Assembly — gate: the first 8 seconds earn the next 8

Cut to `VIDEO_,EDITING.md`. Brand rules that override taste:
- The opener build is 1.2 s and then a hard cut (`MOTION IDENTITY.md`). No second logo animation.
- Chapter cards come from `09_EPISODE_KIT/onscreen/CHAPTER_CARD` — one card per chapter, 1.5 s on screen, no motion needed.
- No transition that exists only to hide a weak cut.
- Silence is allowed. Music does not start under the logo build.

**Gate:** watch the first 8 seconds cold. If you would not keep watching, neither will anyone else.

---

## 6. On-screen text — gate: nothing collides, nothing is unreadable

| Element | File | Placement | Spec |
|---|---|---|---|
| Name strap | `onscreen/LOWER_THIRD_NAME.svg` | x 120, y 690–838 | 44 px name · 24 px role · 19 px label |
| Location strap | `onscreen/LOWER_THIRD_LOCATION.svg` | x 120, y 760 | 26 px, +4.2 tracking, upper |
| Chapter card | `onscreen/CHAPTER_CARD.svg` | full frame | number 340 px · title 96 px · 1.5 s |
| Subtitles | `onscreen/SUBTITLE_SAMPLE.svg` | plate y 862–1030 | Inter 500 · 42 px · max 2 lines · 90 % Ink plate |

Rules: everything inside the 120 px title-safe margin · lower thirds stay above the subtitle zone ·
one orange element per frame · never place text on a busy area without a plate.

**Gate:** pause on every text frame at 100 %. If a word touches an edge, it fails.

---

## 7. Delivery — gate: the checklist is ticked, not remembered

Copy `templates/PUBLISH_CHECKLIST.md` into the episode folder and tick it.

Technical: 1920×1080 · 25 fps · −14 LUFS integrated · −1.0 dBTP · H.264 high profile.
Metadata: title ≤ 60 characters · description with chapters starting at `00:00` · thumbnail from a
template, ≤ 4 words, one orange element · end card in the last 20 s.

**Gate:** a second person can publish from the folder without asking you a question.

---

## 7b. The gates as a command

The gates above are executable — the folder either passes or it does not:

```bash
python3 tools/episode.py new kapal-hilang --minutes 10 --chapters 3   # scaffold + word budgets
python3 tools/episode.py check ../EPISODES/EP_kapal-hilang            # run the gates
```

`new` writes the episode folder from these templates and computes the beat sheet at 140 words/min —
45 s of speech is 105 words, and the arithmetic is not left to the scriptwriter to guess.
`check` reads the folder and reports each gate:

| Gate | What it actually checks |
|---|---|
| `episode.json` | the plan exists (was it scaffolded, or improvised?) |
| evidence sheet | at least one row with claim **and** source **and** date |
| script word count | within ±5 % of the plan's VO budget |
| voice-over | a `.wav`/`.mp3` exists and its duration parses |
| thumbnail | exactly 1280 × 720 |
| subtitles | ≤ 2 lines per cue, ≤ 42 characters per line |
| master | an `.mp4` exists — **existence only**, dimensions are not verified (no `ffprobe` here) |
| metadata | a title ≤ 60 characters and chapters starting at `00:00` |

It is deliberately a *structural* check. It will pass a badly written, badly lit, badly acted film
with a perfect folder — and it says so when it passes. Use it to stop forgetting things, not to feel
finished.

Media is git-ignored (`EPISODES/**/*.mp4|mov|wav`); the script, evidence sheet and metadata stay in
version control, because those are the parts you will want to read again.

---

## 8. The timeline

| When | Stage | Output |
|---|---|---|
| T−10 d | Story lock | one-sentence pitch + evidence sheet |
| T−8 d | Beat sheet | word budgets per beat |
| T−7 d | Voice | full read, WAV |
| T−5 d | Visual plan | per-beat visual intention list |
| T−3 d | Assembly | picture lock (v1) |
| T−2 d | On-screen text | straps, cards, subtitles |
| T−1 d | Delivery | thumbnail, metadata, mix, export |
| T−0 | Publish | upload, end screen, cards, community post |

Ten days is the minimum for a 10-minute film that is actually researched. A four-day version is
possible only if the evidence sheet was already done before the clock starts.

---

## 9. Definition of done

- [ ] Evidence sheet complete; every claim sourced; nothing softened into vagueness.
- [ ] Runtime within 5 % of target; VO ≤ 1,300 words for a 10-minute cut.
- [ ] The turn lands where the beat sheet says it lands.
- [ ] The first 8 seconds survive a cold watch.
- [ ] One orange element per frame; nothing outside the safe margin.
- [ ] Audio at −14 LUFS / −1 dBTP; signature read once.
- [ ] Thumbnail, title, description and chapters written before the export, not after.
- [ ] Folder structure in §10 complete.

---

## 10. Episode folder

```
EP_<number>_<slug>/
├── 01_SCRIPT/       beat sheet, script, evidence sheet
├── 02_VO/           WAV takes, the chosen read, the mix
├── 03_ASSETS/       footage, documents, maps, re-creations (+ licence notes)
├── 04_EDIT/         project file, picture lock, subtitles
├── 05_PUBLISH/      thumbnail, metadata, end screen, exported master
└── 06_NOTES/        decisions, sources, what went wrong
```

The folder is the deliverable. If the film only exists in an editor's head, the next episode starts
from zero.
