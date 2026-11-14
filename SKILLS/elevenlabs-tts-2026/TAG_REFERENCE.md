# ElevenLabs v4 Audio Tags: evidence-based reference

Source reviewed 2026-11-14:
- https://elevenlabs.io/docs/eleven-creative/playground/text-to-speech
- https://elevenlabs.io/docs/overview/capabilities/text-to-speech/best-practices
- https://elevenlabs.io/docs/help-center/product/core-capabilities/text-to-speech/how-do-audio-tags-work-with-eleven-v3-and-v4
- https://elevenlabs.io/blog/ssml-tags-explained (updated 2026-11-03)

## Documented examples (not an exhaustive or guaranteed tag vocabulary)
| Category | Examples | Use | Pitfall |
|---|---|---|---|
| Emotion | `[curious]`, `[sad]`, `[excited]`, `[angry]`, `[sarcastic]`, `[mischievously]` | Before phrase where emotion changes | Over-tagging creates exaggerated acting |
| Vocal delivery | `[whispers]`, `[whispering]`, `[shouts]`, `[shouting]`, `[slowly]`, `[rushed]` | Before the phrase with that delivery | Cannot guarantee tempo or volume |
| Reaction | `[sighs]`, `[exhales]`, `[laughs]`, `[laughs harder]`, `[starts laughing]`, `[wheezing]`, `[crying]`, `[snorts]`, `[clears throat]` | At the precise moment of a human vocal event | Can sound theatrical or insert unwanted sounds |
| Pause (documented as examples in ElevenLabs article/enhancer) | `[pause]`, `[short pause]`, `[long pause]` | When punctuation is insufficient | Not a calibrated duration; test voice/model |
| Sound effects | `[gunshot]`, `[applause]`, `[clapping]`, `[explosion]`, `[swallows]`, `[gulps]` | Only if deliberately generating effects with TTS | Prefer dedicated SFX/postproduction for mix control |
| Experimental | `[strong French accent]`, `[sings]`, `[woo]` | Specific creative need after test | Variable across voices |

## Important distinction
ElevenLabs documents an open-ended natural-language tag approach, not a fixed complete official enumeration. Some tags in examples are experimental or voice-dependent. Do not present this list as all supported tags. Descriptive tags such as `[low, gravelly voice]` are possible but should be tested.

## Unsupported v4 markup
`<break>`, `<prosody>`, `<emphasis>`, `<say-as>`, `<phoneme>`, `<voice>`, `<audio>` are NOT v4 control syntax. No exact timed break in v4 TTS input. Use punctuation/audio tags for approximate delivery and add precise silence in the editor.

## Placement examples
- `[curious] Kenapa lampu kamar itu masih menyala?`
- `[whispers] Jangan lihat ke belakang.`
- `Aku membuka pintu… [exhales] lalu mendengar napas dari dalam lemari.`
- `[sarcastic] Oh, tentu. Pasti cuma angin.`

## Decision rule
Choose punctuation alone as baseline. Add a tag only when its intended effect cannot be communicated reliably from text context and is important to performance. Test before keeping it.
