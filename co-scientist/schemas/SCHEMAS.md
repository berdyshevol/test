# Data schemas (v1, JSON)

The orchestrator keeps all state as JSON files under `co-scientist/data/<session_id>/`.
v1 uses flat JSON (easy to inspect/diff); swap to SQLite later if state outgrows it.

## `hypotheses.json` — list of hypothesis objects

```json
[
  {
    "id": "h1",
    "text": "Repurpose <drug X> for <condition Y> because <mechanism>.",
    "elo": 1200.0,
    "status": "active",
    "round_created": 0,
    "parents": [],
    "tags": ["drug-repurposing"]
  }
]
```

| field | type | meaning |
|-------|------|---------|
| `id` | string | stable unique id (`h1`, `h2`, …) |
| `text` | string | the hypothesis itself |
| `elo` | number | current Elo rating (seeded at 1200) |
| `status` | enum | `active` \| `evolved` \| `duplicate` \| `pruned` |
| `round_created` | int | which round produced it |
| `parents` | string[] | ids it was evolved/combined from (lineage) |
| `tags` | string[] | free-form labels |

## `reviews.json` — Reflection agent output

```json
[
  {
    "hypothesis_id": "h1",
    "round": 0,
    "novelty": 4,
    "correctness": 3,
    "testability": 5,
    "critique": "Plausible mechanism; cite prior X; testable via assay Z."
  }
]
```

Scores are 1–5. `critique` is free text fed back to Evolution / Meta-review.

## `matches.json` — pairwise tournament results (input to `elo.py`)

```json
[
  { "a": "h1", "b": "h2", "winner": "h1", "round": 1, "mode": "single", "reason": "..." }
]
```

| field | type | meaning |
|-------|------|---------|
| `a`, `b` | string | hypothesis ids in the pair |
| `winner` | string | `a`'s id, `b`'s id, or `"draw"` |
| `round` | int | tournament round |
| `mode` | enum | `single` (single-turn) \| `debate` (multi-turn, for top seeds) |
| `reason` | string | the Ranking agent's justification |

## `overview.md` — final human-readable output

Written by the Meta-review agent at termination: ranked hypotheses with Elo, the
strongest rationale for each, and recurring critique themes across the tournament.
