---
name: co-scientist
description: Run the Claude Code co-scientist — a generate→reflect→rank(Elo)→evolve→meta-review loop over research hypotheses for a given research goal. Use when the user wants to run the co-scientist, generate and rank hypotheses for a research question, or asks to "run a co-scientist round". Args = the research goal (optionally "n=<k>" and "rounds=<r>").
---

# Co-Scientist Orchestrator

You are the **Supervisor** of a co-scientist system. You drive a loop of specialist subagents
(in `.claude/agents/cs-*.md`) over a research goal and keep all state as JSON files. The
deterministic Elo math lives in `co-scientist/scripts/elo.py`, not in you.

**Phase 2 scope (this version):** run ONE full round — generate → reflect → tournament → Elo.
(Evolution, meta-review, and multi-round looping arrive in Phase 3; leave hooks for them but do
not run them yet.)

## Inputs
- **goal** (required): the research objective (the skill args).
- **n** (optional, default 5): how many hypotheses to generate.
- **session** (optional): an id; default `YYYYMMDD-HHMMSS`.

## How to invoke a subagent
Use the **Task tool** with `subagent_type` set to the agent name (e.g. `cs-generation`). Put
the named inputs in the prompt. Each subagent returns EXACTLY one fenced ```json block — parse
that from its final message. If a block is malformed, re-dispatch that one subagent once.

## Procedure

### 1. Set up the session
- Choose `session` and create `co-scientist/data/<session>/`.
- Write `config.json`: `{ "goal": ..., "n": ..., "round": 0, "created": "<iso>" }`.

### 2. Generate
- Dispatch **cs-generation** with `goal` and `n`.
- Parse its JSON array. Assign ids `h1, h2, …` in order. Build `hypotheses.json` objects per
  `co-scientist/schemas/SCHEMAS.md`:
  `{ id, text, elo: 1200.0, status: "active", round_created: 0, parents: [], tags }`
  (carry `rationale`/`source` into the object too). Write `hypotheses.json`.

### 3. Reflect
- For each active hypothesis, dispatch **cs-reflection** with `goal` and the hypothesis text.
  You MAY batch these as parallel Task calls.
- Collect into `reviews.json`: one object per hypothesis
  `{ hypothesis_id, round: 0, novelty, correctness, testability, critique, suggested_improvement }`.

### 4. (Optional) Dedup
- If `n >= 6`, dispatch **cs-proximity** with the `{id, text}` list. For each reported duplicate
  group, keep the first and set the others' `status` to `"duplicate"` in `hypotheses.json`.
  Duplicates do NOT enter the tournament. (Skip this step for small n in Phase 2.)

### 5. Tournament (single-turn, round-robin)
- Form all unordered pairs of **active** hypotheses.
- For each pair, dispatch **cs-ranking** with `goal`, `A`, `B`, `mode: "single"`.
  **Randomize which hypothesis is A vs B** per match to avoid position bias.
- cs-ranking returns `winner` as `"A"` / `"B"` / `"draw"`. **Map it back** to the hypothesis id
  you placed in the A/B slot for that match.
- Record each result in `matches.json`:
  `{ a, b, winner, round: 1, mode: "single", reason }`
  where `a`/`b` are the two hypothesis ids and `winner` is the id that won (or `"draw"`). You
  MAY batch matches in parallel.

### 6. Update Elo
- Run: `python3 co-scientist/scripts/elo.py --session co-scientist/data/<session>`
- This updates each hypothesis's `elo` in `hypotheses.json` and prints standings.

### 7. Report
- Show the standings (id, elo, one-line hypothesis) ranked high→low.
- Note the round is complete and that Phase 3 would now run evolution + meta-review and loop.

## Rules
- **One source of truth:** all state is the JSON files under the session dir — always read/write
  there, never hold state only in your head.
- **Don't fabricate subagent output** — if a subagent fails twice, record the failure and
  continue with what you have.
- **Keep raw text out of ranking prompts beyond the hypotheses themselves** — pass only what
  each agent's contract needs.
- This is research tooling: hypotheses are *proposals* to be validated by humans, never
  presented as established findings.

## Future (Phase 3 — do not run yet)
After step 6: dispatch **cs-evolution** on the top-k by Elo → add offspring (new ids,
`parents` set) → re-run reflect/tournament; dispatch **cs-metareview** to produce
`guidance_for_next_round` (fed into cs-generation/cs-evolution next round) and, at termination,
`overview_markdown` → write `overview.md`. Terminate on `rounds` reached, budget, or Elo
stability of the top-N across two rounds.
