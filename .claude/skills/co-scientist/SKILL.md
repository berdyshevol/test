---
name: co-scientist
description: Run the Claude Code co-scientist — a generate→reflect→rank(Elo)→evolve→meta-review loop over research hypotheses for a given research goal. Use when the user wants to run the co-scientist, generate and rank hypotheses for a research question, or asks to "run a co-scientist round". Args = the research goal (optionally "n=<k>" and "rounds=<r>").
---

# Co-Scientist Orchestrator

You are the **Supervisor** of a co-scientist system. You drive a multi-round loop of specialist
subagents (in `.claude/agents/cs-*.md`) over a research goal and keep all state as JSON files.
The deterministic Elo math lives in `co-scientist/scripts/elo.py`, not in you.

The loop is **generate → reflect → tournament(Elo) → evolve → meta-review**, repeated for
several rounds. More rounds = more refinement (this is the "test-time compute" lever): the
Meta-review feedback and the Evolution offspring should make later rounds better.

## Inputs
- **goal** (required): the research objective (the skill args).
- **n** (optional, default 5): hypotheses generated in round 0.
- **rounds** (optional, default 3): max number of rounds.
- **session** (optional): an id; default `YYYYMMDD-HHMMSS`.

## Tunables (sensible defaults)
- `TOP_K_EVOLVE = 3` — how many top hypotheses Evolution improves each round.
- `FRESH_PER_ROUND = 2` — fresh hypotheses Generation adds in rounds ≥ 1 (injects new ideas).
- `ACTIVE_CAP = 8` — max hypotheses allowed into a tournament (prune the rest by Elo).
- `DEBATE_SEEDS = 3` — the top seeds' matches use `mode:"debate"` (multi-turn); others `single`.

## How to invoke a subagent
Use the **Task tool** with `subagent_type` = the agent name (e.g. `cs-generation`). Put the
named inputs in the prompt. Each subagent returns EXACTLY one fenced ```json block — parse it
from the final message. If a block is malformed, re-dispatch that one subagent once.

## State files (under `co-scientist/data/<session>/`, see `co-scientist/schemas/SCHEMAS.md`)
- `config.json` — run config.
- `hypotheses.json` — all hypotheses (ids, elo, status, lineage). **Elo carries across rounds.**
- `reviews.json` — Reflection output (append; tag each with its round).
- `matches.json` — **append-only FULL tournament history**. `elo.py` recomputes ratings from it.
- `round_log.json` — one row per round: `{round, top_id, top_elo, n_active, n_total}`.
- `guidance.txt` — latest Meta-review guidance, fed into next round.
- `overview.md` — final ranked overview (written at termination).

## Procedure

### Setup
- Choose `session`; create the dir; write `config.json` = `{goal, n, rounds, created}`.
- Initialize `matches.json` = `[]`, `round_log.json` = `[]`.

### Round loop — for `round` = 0, 1, … up to `rounds-1`:

**1. Populate candidates**
- If `round == 0`: dispatch **cs-generation** (`goal`, `n`). Assign ids `h1…`. Create
  `hypotheses.json` objects (`elo:1200`, `status:"active"`, `round_created:0`, `parents:[]`).
- If `round >= 1`:
  - dispatch **cs-evolution** (`goal`, `top` = the `TOP_K_EVOLVE` active hypotheses by Elo,
    `feedback` = `guidance.txt`). Add offspring as new ids (`elo:1200`, `status:"active"`,
    `round_created:round`, `parents` set from the contract).
  - dispatch **cs-generation** (`goal`, `n=FRESH_PER_ROUND`, `existing` = all current texts,
    `feedback` = `guidance.txt`). Add as new ids.

**2. Reflect** — dispatch **cs-reflection** (`goal`, hypothesis) for every hypothesis **new
this round**; append to `reviews.json` with `round`. (May batch in parallel.)

**3. Dedup** — dispatch **cs-proximity** on the active `{id,text}` list whenever new
hypotheses were added this round AND active count ≥ 4 (evolution offspring often paraphrase
their parents, so dedup matters even for small sets). For each duplicate group keep the
highest-Elo member and set the others' `status:"duplicate"`.

**4. Select the active set** — active = status `active`. If `> ACTIVE_CAP`, keep the top
`ACTIVE_CAP` by Elo and set the rest to `status:"pruned"` (selection pressure).

**5. Tournament** — all unordered pairs of active hypotheses. For each pair dispatch
**cs-ranking** (`goal`, `A`, `B`, `mode`). Use `mode:"debate"` only when the active set is
**larger than** `DEBATE_SEEDS` AND **both** members are among the top `DEBATE_SEEDS` by Elo;
otherwise `mode:"single"`. (Without the size guard, small sets where everyone is a "top seed"
would make every match an expensive debate.) Break Elo ties by lower hypothesis-id number.
**Randomize A/B order** per match. Map the returned `"A"/"B"/"draw"` back to ids. **Append**
each result to `matches.json` with `round`. (May batch in parallel.)

> **Cost note:** round-robin is O(active²) ranking calls — at `ACTIVE_CAP=8` that's 28 matches
> per round. Keep `ACTIVE_CAP` and `rounds` modest, or switch to Swiss/seeded pairing for large
> sets (a future optimization).

**6. Update Elo** — run:
`python3 co-scientist/scripts/elo.py --session co-scientist/data/<session>`
(idempotent: recomputes all ratings from the full `matches.json`).

**7. Meta-review** — dispatch **cs-metareview** (`goal`, `ranked` = active by Elo, `reviews`,
`matches` = this round's, `final` = (this is the last round OR termination triggered)). Write
its `guidance_for_next_round` to `guidance.txt`. If `final`, write `overview_markdown` to
`overview.md`.

**8. Round log** — append `{round, top_id, top_elo, n_active, n_total}` to `round_log.json`.

**9. Termination check** — stop the loop early if `round >= 1` AND the **top-3 ids and their
order are unchanged** from the previous round AND the top Elo moved `< 5` points. (Elo has
stabilized — more compute won't help.) Otherwise continue.

### After the loop
- Ensure a **final** Meta-review + `overview.md` exist (run step 7 with `final:true` if the loop
  ended without one).
- Report: the standings (id, elo, one-line hypothesis), the path to `overview.md`, and the Elo
  trajectory of the top hypothesis from `round_log.json` (this shows the test-time-compute effect).

## Rules
- **One source of truth:** all state is the JSON files — always read/write there.
- **Elo persists across rounds; never reset it.** New hypotheses start at 1200.
- **`matches.json` is append-only;** `elo.py` is the only thing that computes ratings.
- **Don't fabricate subagent output** — if a subagent fails twice, log it and continue.
- Research tooling only: hypotheses are *proposals* for humans to validate, never presented as
  established findings.
