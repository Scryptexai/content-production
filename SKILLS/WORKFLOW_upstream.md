# Orchestration Workflow

1. Director reads AGENTS.md, principles and output contract.
2. Concept agent runs premise-design.
3. Character agent runs character-psychology.
4. Plot agent runs causal-structure; update story bible.
5. Dialogue agent runs natural-dialogue.
6. Cinematic agent runs cinematic-storytelling.
7. Genre agent runs genre-intelligence.
8. Pacing agent runs pacing-retention and estimates runtime.
9. Editor runs editorial-audit; iterate until release criteria met.

## Handoff JSON example
```json
{
  "story_id":"ST-001",
  "revision":1,
  "format":"short_60s",
  "genre":"horror",
  "language":"id-ID",
  "premise":"...",
  "characters":[],
  "world_rules":[],
  "beats":[],
  "script":[],
  "continuity_issues":[],
  "qa":{"status":"REVISE","scores":{}}
}
```

Never let a later agent silently overwrite established facts; log changes and rerun affected checks.
