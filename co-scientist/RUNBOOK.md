# Co-Scientist Runbook — your first real run (step 4)

How to actually run the Claude Code co-scientist in the Claude Code CLI and verify it works.
The orchestration logic was rehearsed end-to-end (2 rounds, live stand-ins) before this — the
findings from that rehearsal are at the bottom.

## Prerequisites
- You're in the **Claude Code CLI** (the `cs-*` subagents in `.claude/agents/` only load there;
  they can't be invoked from inside another agent harness).
- Network access for `WebSearch`/`WebFetch` (used by Generation/Reflection grounding).

## Run it
```
/co-scientist "Identify novel drug-repurposing candidates for treating pancreatic ductal adenocarcinoma (PDAC)"
```
Optional args: `n=5` (round-0 hypotheses), `rounds=3`.

**Start small for the first run:** `n=3 rounds=2`. That keeps cost and runtime low while
exercising the whole loop.

## What to check after it finishes — under `co-scientist/data/<session>/`
1. **`hypotheses.json`** — ids assigned (`h1…`), `elo` populated, offspring have
   `round_created>0` and non-empty `parents` (lineage worked).
2. **`matches.json`** — append-only; entries tagged by `round`; `winner` is a real id or `draw`.
3. **`round_log.json`** — one row per round. **Did the lead improve?** Watch whether evolved
   offspring climb above the round-0 leaders across rounds (the self-improvement signal).
4. **`overview.md`** — coherent ranked overview with rationale per hypothesis.
5. **`reviews.json`, `guidance.txt`** — reflection scores present; guidance reads sensibly and
   visibly steered the next round.

## Re-deriving Elo by hand (sanity)
```
python3 co-scientist/scripts/elo.py --session co-scientist/data/<session>
```
Idempotent — running it again must print identical standings.

## Cost & runtime expectations
- Dominant cost = **ranking calls**: round-robin is O(active²). With `ACTIVE_CAP=8` a round can
  be ~28 ranking matches. Generation/Reflection/Evolution/Meta-review add a handful each.
- A `n=3 rounds=2` run is on the order of a few dozen subagent calls. Scale up only once happy.
- Model routing (set in the agent files): opus for generation/evolution/meta-review, sonnet for
  ranking, haiku for reflection/proximity — tune for cost.

## What "success" looks like (lab-free, per the plan)
- **Behavioral:** top hypotheses are novel, specific, testable (not generic).
- **Self-improvement:** evolved offspring overtake earlier leaders across rounds.
- **Determinism:** `elo.py` reproduces the same standings from `matches.json`.
(You cannot reproduce the original wet-lab discoveries solo — that's expected.)

---

## Findings from the pre-run rehearsal (2 rounds, PDAC goal)

What the dry run confirmed and what it exposed:

**Confirmed working**
- Full loop ran: generate → reflect → tournament → Elo → meta-review → evolve → round 2.
- Lineage, cross-round `matches.json` accumulation, and idempotent Elo recompute all correct.
- **Self-improvement demonstrated:** an evolved offspring (disulfiram-copper/proteostasis)
  overtook the round-0 champion (apilimod+FASN) by naming a specific resistance/escape pathway
  and concrete readouts — exactly the intended dynamic.

**Issues found → already fixed in the skill**
- *Dedup never triggered* at the old `active ≥ 6` threshold for small runs → changed to "run
  when new hypotheses were added AND active ≥ 4."
- *Debate-mode exploded on small sets* (with ≤3 active everyone is a "top seed", so every match
  became an expensive debate) → added a size guard (active must exceed `DEBATE_SEEDS`) and a
  tie-break rule.

**Known limitations to watch on the real run (not yet fixed)**
- **Elo is relative/zero-sum**, so `top_elo` barely moves even when a better hypothesis takes
  the lead — judge progress by *which* hypothesis leads and by rank churn, not by the absolute
  top Elo number.
- **Round-robin cost** grows quadratically — fine at small scale, needs Swiss/seeded pairing
  before large runs.
- **Cold-start Elo:** new hypotheses enter at 1200 while incumbents carry their rating; strong
  newcomers still climbed, but a very strong incumbent has a head start. Acceptable for v1.
- **Output parsing:** subagents must return ONLY the fenced ```json block; the orchestrator
  should extract that block rather than assume the whole message is JSON.
