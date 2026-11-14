# TTS Listening QA & Revision Protocol

## Mandatory A/B test
A: punctuation-only baseline. B: selective tags. Same voice/model/settings; compare at matched loudness. Never assume B is better.

## Score 0–5 each
1. Natural Indonesian diction and conversational cadence
2. Syntactic phrasing and breath groups
3. Emotion appropriate to the story (not overacted)
4. Pauses and dramatic reveals
5. Pronunciation of names, numbers, abbreviations
6. Cross-segment continuity of voice and intensity
7. Clarity and listener comprehension
8. Absence of unwanted vocalizations, spoken markup or sound effects

Release gate: no item below 4 after human listening. This is an internal quality target, not a measured ElevenLabs standard.

## Failure mapping
- Monotone: strengthen context and contrast, test voice; do not spray emotion tags.
- Overacting: remove tags and excessive ellipses/exclamation marks.
- Awkward stops: restore grammatical punctuation and complete thought groups.
- Mispronunciation: rewrite numbers/symbols, consistent phonetic spelling where appropriate.
- Tag spoken aloud: verify model ID and tag syntax, remove/replace offending tag.
- Exact pause needed: add silence in post-production, not fake SSML for v4.
- Abrupt chunk transitions: regenerate at sentence/scene boundary and apply appropriate audio crossfade/room tone.

## Agent output audit
- Confirm model: `eleven_v4` or `eleven_v4_turbo`.
- Report which tags were used, where, and why.
- Report uncertain/unverified tags as experimental.
- Do not claim to have heard an audio render unless audio was supplied or actually generated and reviewed.
