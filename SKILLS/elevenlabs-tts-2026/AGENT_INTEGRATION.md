# Agent integration

1. Copy folder into `skills/elevenlabs-v4-tts-script-engineering/`.
2. Add to root `AGENTS.md`:
   `For all ElevenLabs v4 narration/dialogue, load skills/elevenlabs-v4-tts-script-engineering/SKILL.md and its reference files. Produce separate spoken script, non-spoken direction sheet, and QA checklist. Never use SSML for v4.`
3. Production sequence: story draft -> spoken-language rewrite -> emotional beat map -> minimal tags -> pronunciation pass -> TTS rendering -> listening QA -> targeted revision -> final audio.
4. Keep `tts_script.txt` strictly free of stage directions, scene labels, Markdown, timestamps and SFX notes.
5. For multiple characters, prefer dialogue endpoint or per-speaker audio generation rather than assuming a single narration request switches speakers correctly.
6. Version-control model ID, voice ID, settings, script, tag revisions and QA observations for reproducibility.
