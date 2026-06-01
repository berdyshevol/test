# Replicating the AI Co-Scientist in Claude Code — Deep-Dive & Build Plan

**Target system:** Google AI co-scientist (see
[../agentic-research-systems/google-ai-co-scientist.md](../agentic-research-systems/google-ai-co-scientist.md))
**Goal:** rebuild its *architecture* on Claude Code primitives, then run it and compare results.
**Status:** plan only — no code yet. This is the blueprint for step 3.

---

## 0. Where this sits in your pipeline

1. Discover ✅ (catalog of 10 systems)
2. **Understand** ← this document (how co-scientist works, mapped to Claude Code)
3. **Replicate** — build it in Claude Code from this plan
4. **Reproduce** — run it and check results

### What "same results" realistically means here
The co-scientist's headline wins (AML drug repurposing, liver-fibrosis targets) were
**wet-lab validated** — you cannot reproduce *those* without a lab. What you *can* reproduce
solo and computationally:
- the **behavior**: given a research goal, does the system produce a ranked set of plausible,
  novel, testable hypotheses?
- the **internal dynamics**: does Elo rise over rounds, and do higher-Elo hypotheses look
  better (the paper's central claim: Elo correlates with quality)?
- optionally, **gold-set recall**: the open-source reimpl ships an `paper-aml` preset with a
  drug-repurposing gold set; reproducing "does our system surface the known candidates" is a
  fair, lab-free success metric.

So define step-4 success as **behavioral + Elo-dynamics + (optional) gold-set recall**, not
"cure AML."

---

## 1. How the co-scientist works (condensed reference)

Loop: **generate → reflect → rank (Elo tournament) → evolve → meta-review → repeat** until a
termination trigger, all coordinated by a **Supervisor** over a durable task queue.

| Agent | Input → Output | Job |
|-------|----------------|-----|
| Supervisor | goal → plan + scheduled tasks | Orchestrates; allocates compute; decides stop |
| Generation | goal (+ feedback) → hypotheses | Propose hypotheses, grounded by literature search |
| Reflection | hypothesis → critique + scores | Peer-review: novelty / correctness / testability |
| Proximity | hypotheses → clusters | Embed + dedup so the tournament compares diverse ideas |
| Ranking | hypothesis pairs → Elo updates | Tournament: multi-turn debate (top) / single-turn (rest) |
| Evolution | top hypotheses → improved ones | Combine / simplify / analogize winners |
| Meta-review | tournament history → synthesis | Extract critique patterns; feed back; write final overview |

Key mechanics to preserve: **Elo tournament** (pairwise, ordering randomized), **test-time
compute scaling** (more rounds → better), **context vs artifact memory** separation, and the
**meta-review feedback** loop (the self-improvement signal).

---

## 2. Mapping to Claude Code primitives

| Co-scientist piece | Claude Code primitive | Notes |
|--------------------|------------------------|-------|
| Specialist agents | **Subagents** (`.claude/agents/*.md`) | One file per role; isolated context; own system prompt + tool set + model |
| Supervisor / loop | An **orchestrator skill** (`.claude/skills/`) the main agent runs | Drives rounds, dispatches subagents via the Agent tool, manages memory & termination |
| Literature grounding | Built-in **WebSearch / WebFetch** | Later: MCP servers for PubMed/arXiv |
| Artifact state (hypotheses, reviews, matches, Elo) | **Files** (JSON) or **SQLite** in the repo | Mirrors the open-source reimpl's 15-table schema (start with JSON) |
| Context state | Round summaries passed into prompts | Keep raw artifacts out of the prompt; pass summaries |
| Elo tournament bookkeeping | A **Python/Bash script** run via Bash | Deterministic math outside the LLM |
| Proximity / dedup | Embeddings via a small script (or skip in v1, use LLM "are these duplicates?") | FAISS later; LLM-judge first |
| Reflection / governance | Subagent + orchestrator checks (+ optional **hooks**) | |
| Headless / repeatable runs (step 4) | **Claude Agent SDK** | See §6 |

---

## 3. Proposed architecture (Claude Code v1)

```
your-coscientist/
├── .claude/
│   ├── agents/
│   │   ├── cs-generation.md      # propose hypotheses (uses WebSearch)
│   │   ├── cs-reflection.md      # critique: novelty/correctness/testability
│   │   ├── cs-ranking.md         # judge a pairwise debate, output winner + reason
│   │   ├── cs-evolution.md       # improve/combine top hypotheses
│   │   ├── cs-proximity.md       # cluster/dedup (or fold into orchestrator in v1)
│   │   └── cs-metareview.md      # synthesize patterns + final overview
│   └── skills/
│       └── co-scientist/SKILL.md # the Supervisor: runs the whole loop
├── scripts/
│   └── elo.py                    # pairwise Elo updates + standings
├── data/
│   └── <session_id>/
│       ├── hypotheses.json       # id, text, elo, status, lineage
│       ├── reviews.json
│       ├── matches.json          # pairwise results
│       └── overview.md           # final output
└── README.md
```

**Control flow (the orchestrator skill):**
1. Parse goal → create `data/<session>/` and seed config (n hypotheses, max rounds, budget).
2. **Generate**: dispatch `cs-generation` (k times or k ideas) → write `hypotheses.json`.
3. **Reflect**: for each hypothesis, dispatch `cs-reflection` → `reviews.json`.
4. **Dedup**: LLM-judge near-duplicates (v1) → mark/merge.
5. **Tournament**: pick pairs; dispatch `cs-ranking` per pair; record winner in `matches.json`;
   run `scripts/elo.py` to update ratings.
6. **Evolve**: take top-k by Elo; dispatch `cs-evolution`; add offspring to `hypotheses.json`.
7. **Meta-review**: dispatch `cs-metareview` over `matches.json` + `reviews.json`; feed its
   guidance into the next round's generation/evolution prompts.
8. **Terminate** when: rounds ≥ max, or budget hit, or Elo top-N stable across 2 rounds.
   Write `overview.md` (ranked hypotheses + rationale).

**Model routing (cost lever, mirrors the reimpl):** strong model for generation + debate
ranking + final meta-review; cheaper/faster model for pairwise ranking and reflection.

---

## 4. Build plan (phased, each phase independently testable)

- **Phase 0 — skeleton.** Repo layout, `elo.py` with unit-tested Elo math, JSON schemas.
  *Test:* feed fake match results, confirm standings update correctly.
- **Phase 1 — single agents.** Write + test each subagent in isolation (give it one input,
  inspect output quality). Start with Generation and Reflection.
  *Test:* run `cs-generation` on a goal; eyeball 5 hypotheses for plausibility.
- **Phase 2 — one full round.** Orchestrator skill runs generate → reflect → one tournament
  bracket → Elo update, no evolution yet.
  *Test:* `matches.json` + Elo populate; a sensible top hypothesis emerges.
- **Phase 3 — the loop.** Add evolution + meta-review + multi-round + termination.
  *Test:* Elo of the top hypothesis trends up over rounds; overview.md is coherent.
- **Phase 4 — grounding + dedup.** Wire WebSearch into Generation/Reflection; add real
  proximity (embeddings) if LLM-judge dedup is too weak.
- **Phase 5 — reproducibility harness (step 4).** Port to the **Claude Agent SDK** for
  headless, scripted, repeatable runs; add logging of Elo-per-round and (optional) gold-set
  recall scoring.

---

## 5. Validation design (step 4)

Run the finished system on a goal with a *known* answer set so success is measurable:
- **Behavioral:** are outputs novel + testable + on-topic? (rubric, or `cs-reflection` scores)
- **Elo dynamics:** plot top-hypothesis Elo vs round — should rise then plateau (replicates the
  paper's test-time-compute claim).
- **Gold-set recall (best lab-free proxy):** pick a goal where the literature already names
  good candidates (e.g. a drug-repurposing question), run the system, measure how many gold
  candidates it surfaces in the top-k. The open-source reimpl's `paper-aml` preset is a model
  for this.

---

## 6. Two implementation modes (and why both)

- **Native Claude Code (Phases 0–4):** orchestrator *skill* + *subagents*, driven
  interactively. Best for **understanding** and fast iteration — you watch each agent work.
- **Claude Agent SDK (Phase 5):** the same agents/loop expressed in code for **headless,
  repeatable** runs. Essential for step 4 (you need to run many times, vary compute, log
  metrics). The SDK is the right tool for reproducibility experiments.

Recommendation: build native first (you'll *understand* it by building it), then lift the
loop into the SDK once the behavior is right.

---

## 7. v1 simplifications (so you ship something runnable)

- LLM-judge dedup instead of FAISS embeddings.
- Single-turn pairwise ranking for everyone first; add multi-turn debate for top seeds later.
- JSON files instead of SQLite (swap in SQLite when state outgrows JSON).
- One literature tool (WebSearch) before adding PubMed/arXiv MCP servers.
- Fixed round count before adding Elo-stability termination.

Each simplification is a known, isolated upgrade path — nothing here blocks reaching the full
design.

---

## 8. Open decisions before coding (for step 3)

1. **Scripts language** for `elo.py` / harness — Python (recommended) vs Bash.
2. **Model routing** — which model for generation/debate vs ranking/reflection.
3. **Memory backend** — start JSON (recommended) vs go straight to SQLite.
4. **Where the project lives** — new folder in this repo vs a separate repo.

Resolve these four and Phase 0 can start.
