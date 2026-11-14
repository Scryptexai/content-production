---
name: elevenlabs-v4-tts-script-engineering
description: Convert Indonesian narrative scripts into natural, production-ready ElevenLabs v4 voiceover text using verified audio tags, punctuation, prosody and listening QA.
---
# ElevenLabs v4 TTS Script Engineering

## Mission
Produce speech-first Indonesian scripts, not prose formatted as audio. Preserve meaning, speaker identity, causality and emotional subtext. Never claim that punctuation or a tag guarantees exact duration or intonation.

## Model gate
- Default `eleven_v4` for high-quality narrative; `eleven_v4_turbo` when latency matters.
- v4 uses square-bracket audio tags; **do not output SSML** such as `<break time="1s"/>`, `<prosody>`, or `<emphasis>`.
- v4 does not expose Style or Speed sliders. Voice choice, Stability and Similarity matter. Do not assume a tag is deterministic.
- Treat any unverified tag as experimental. Test with the selected voice.

## Workflow
1. Identify genre, audience, voice profile, speaking style, script length, speaker count and dramatic arc.
2. Convert written prose to speech-first language: short breath groups, one idea per clause, natural Indonesian diction.
3. Mark semantic beats: information, suspense, reversal, emotional reaction, resolution.
4. Use punctuation first. Comma for syntactic grouping; period for closure; question mark for genuine questions; ellipsis `…` sparingly for hesitation/suspense; em dash `—` for interruption/reversal; exclamation sparingly. No repeated punctuation decoration.
5. Apply **minimal** audio tags at local delivery changes, typically immediately before the affected phrase. Avoid tagging every sentence.
6. Spell out ambiguous numbers, dates, abbreviations and symbols in the spoken version. Keep proper names consistent.
7. Segment audio at coherent paragraph/scene boundaries. Keep a short contextual overlap in editorial metadata, not duplicated in spoken output.
8. Generate and listen. Audit pronunciation, unexpected spoken tags, pacing, accent, breathiness, emotion, sentence-final intonation, loudness and cross-chunk continuity.
9. Revise only faulty spans, regenerate and compare A/B against a plain-punctuation baseline.

## Deliverables
- `tts_script`: ONLY text and supported/tested audio tags that the TTS engine should speak or interpret.
- `direction_sheet`: separate non-spoken notes on voice, target delivery, scene, emotional progression, intended pause function and speaker.
- `qa_report`: observed problems and recommended revisions; never invent listening results.

## Hard constraints
- Never use `Speaker 1:` in single-narrator speech output unless specifically required by the chosen dialogue endpoint.
- Never embed `[music]`, camera instructions, timestamps, SFX production notes or markdown headings in spoken output.
- Never substitute a fixed-duration silence request with an unverified tag. For precise silence, insert it in audio postproduction.
- Do not whisper every scary line; contrast quiet normality and moments of threat.
- Use human reactions only when narratively motivated; a narrator's `[laughs]` is not a substitute for describing a character laughing.
- Check output against `TAG_REFERENCE.md`, `PUNCTUATION.md`, and `QA_RUBRIC.md`.
