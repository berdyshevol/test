# Claude Code Co-Scientist (replication)

A from-scratch rebuild of Google's AI co-scientist on **Claude Code primitives** —
subagents + an orchestrator skill + file-based memory + a small Elo script. This is
**step 3** of the discover → understand → replicate → reproduce pipeline.

Plan / rationale: [`../replication/co-scientist-claude-code-plan.md`](../replication/co-scientist-claude-code-plan.md)
Reference system: [`../agentic-research-systems/google-ai-co-scientist.md`](../agentic-research-systems/google-ai-co-scientist.md)

## Defaults chosen for v1

- **Scripts:** Python (stdlib only)
- **Memory:** flat JSON under `data/<session_id>/` (SQLite later)
- **Models:** strong model for generation / debate-ranking / meta-review; cheap model
  for reflection / single-turn ranking (routing wired in when the orchestrator lands)
- **Location:** this folder in the repo

## Layout

```
co-scientist/
├── scripts/
│   ├── elo.py          # Elo bookkeeping (pure stdlib)
│   └── test_elo.py     # unit tests — run: python test_elo.py
├── schemas/
│   └── SCHEMAS.md      # JSON shapes for hypotheses / reviews / matches
├── data/               # per-session state (gitignored except .gitkeep)
└── README.md
```

Subagents (`.claude/agents/cs-*.md`) and the orchestrator skill
(`.claude/skills/co-scientist/`) live at the repo root and arrive in Phases 1–3.

## Build status

- [x] **Phase 0** — skeleton, Elo math + tests, JSON schemas
- [x] **Phase 1** — individual subagents in `.claude/agents/cs-*.md` (Generation, Reflection,
  Ranking, Evolution, Proximity, Meta-review); frontmatter validated, Generation contract smoke-tested
- [x] **Phase 2** — orchestrator skill `.claude/skills/co-scientist/` runs one full round
  (generate → reflect → tournament → Elo); tournament→Elo path validated on a live mini-round
  (run it with `/co-scientist "<goal>"`)
- [x] **Phase 3** — multi-round loop: evolution + meta-review feedback + fresh injection +
  active-set pruning + debate-mode for top seeds + Elo-stability termination. `elo.py` made
  idempotent (recompute-from-history) so accumulating rounds don't double-count; `round_log.json`
  tracks the top-Elo trajectory (the test-time-compute signal)
- [ ] **Phase 4** — literature grounding + real dedup
- [ ] **Phase 5** — Agent SDK reproducibility harness

## Run the tests

```bash
cd co-scientist/scripts && python test_elo.py
```
