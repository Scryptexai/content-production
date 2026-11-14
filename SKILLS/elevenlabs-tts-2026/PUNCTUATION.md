# Indonesian Spoken-Text Punctuation & Prosody

These are editorial heuristics, not fixed acoustic laws.

| Symbol | Typical function | Example | Caution |
|---|---|---|---|
| `,` | Short syntactic grouping | `Saat pintunya terbuka, semua orang diam.` | Don't comma-splice every 3 words |
| `.` | Complete thought, natural reset | `Aku mematikan lampu. Suaranya berhenti.` | Too many short sentences sound robotic |
| `…` | Hesitation, withheld reveal, weight | `Tapi yang berdiri di sana… bukan ibuku.` | Overuse makes every line melodramatic |
| `—` | Abrupt turn, interruption, correction | `Aku mau berteriak—tapi suaraku hilang.` | Not a guaranteed exact pause |
| `?` | Actual question | `Siapa yang mengetuk pintu itu?` | Rhetorical questions need context |
| `!` | Genuine shock/command | `Keluar!` | Frequent exclamations force shouting |
| Paragraph break | Scene/idea boundary | New paragraph at a reveal | TTS generation may not give consistent pause |
| CAPITALS | Occasional emphasis | `Dia bilang JANGAN buka pintunya.` | Can produce unnatural shouting or spelling |

## Spoken Indonesian
- Prefer `Aku dengar sesuatu dari dapur` over `Terdengar sebuah suara yang berasal dari arah dapur` when first-person conversational voice is intended.
- Avoid redundant intensifiers (`sangat`, `begitu`, `benar-benar`) and generic horror filler.
- Write `pukul tiga lewat tujuh menit` rather than `03:07` if pronunciation matters.
- Distinguish narration from dialogue through context or separate speaker generation.
- Vary sentence length: medium for setup, short for impact, longer when breath/flow supports reflection.
- Use silence strategically: precise durations belong in editing timeline, not inferred from commas.

## Anti-pattern
BAD: `[whispers] Malam itu... aku... berjalan... perlahan... dan... mendengar... suara...`
BETTER: `Malam itu aku pulang lebih lambat dari biasanya. Gangnya sepi. Tapi dari rumah kosong di ujung jalan… ada suara orang menyanyi.`
