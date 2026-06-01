# Google AI Co-Scientist

**Type:** Agentic LLM system (multi-agent)
**Organization:** Google DeepMind / Google Research
**Year:** 2025
**Foundation model:** Gemini 2.0

## What it is

An AI "research partner" that does **not** design molecules directly. Instead it
generates, debates, and ranks *research hypotheses and proposals*, which human
scientists then validate in the lab. It explicitly emulates the scientific method.

> **Best system to clone first.** There is a faithful open-source reimplementation
> (see "Reference implementation" below) whose architecture is documented in enough
> detail to build from. The rest of this file is written as a build spec.

## Core specification

- **Paradigm:** "Generate, debate, evolve," powered by **test-time compute scaling** —
  more inference compute measurably improves hypothesis quality.
- **Orchestration:** An **asynchronous task-execution framework** with a **Supervisor
  agent** that parses the research goal, assigns work to a task queue, and allocates
  compute dynamically. A persistent context memory holds state across long reasoning runs.
- **Self-improvement:** A recursive loop driven by an Elo tournament + meta-review.

## The six specialized agents

| Agent | Input → Output | Role |
|-------|----------------|------|
| **Generation** | research goal (+ feedback) → candidate hypotheses | Proposes hypotheses via literature synthesis + domain reasoning |
| **Reflection** | hypothesis → critique/scores | "Virtual peer reviewer": validity, novelty, feasibility, evidence grounding |
| **Ranking** | hypothesis pairs → Elo updates | Runs the **tournament**: pairwise "scientific debates" |
| **Evolution** | top hypotheses → improved hypotheses | Refines/combines/reimagines winners |
| **Proximity** | hypothesis set → clusters | Embeds + clusters for diversity & dedup |
| **Meta-review** | tournament history → synthesis | Extracts recurring critique patterns; feeds them back into Generation/Evolution; writes the final overview |

- A **scientist-in-the-loop** can seed ideas and give natural-language feedback at any point.

## The control loop (generate → debate → evolve)

1. **Supervisor** parses the research goal into a plan and seeds the task queue.
2. **Generation** produces an initial batch of hypotheses (grounded by literature search).
3. **Reflection** reviews each (novelty / correctness / testability).
4. **Proximity** clusters them so the tournament compares diverse ideas, not near-dupes.
5. **Ranking** runs the **Elo tournament**:
   - Top-ranked hypotheses meet in **multi-turn scientific debates** (richer comparison).
   - Lower-ranked ones get **single-turn pairwise** comparisons (cheaper).
   - Comparison criteria: novelty, correctness, testability. Debate ordering is randomized
     to mitigate position bias.
6. **Evolution** takes tournament winners and produces improved variants (combine,
   simplify, add detail, find analogies), which re-enter the tournament.
7. **Meta-review** synthesizes critique patterns across all matches and injects guidance
   back into Generation/Evolution — this is the self-improvement signal.
8. Loop until a **termination trigger**: budget exhausted, wall-clock limit, **Elo
   stability**, or idle queue. Output: a ranked overview document.

**Why it improves with compute:** more tournament rounds + evolution cycles = higher Elo,
and higher Elo empirically correlates with correctness.

## Reference implementation (open source)

`Kaimen-Inc/Co-Scientist` — a faithful Python reimplementation. Concrete stack worth copying:

- **Language/UI:** Python 3.11–3.13, FastAPI dashboard (`co-scientist serve`, localhost:7878).
- **Persistence:** SQLite (WAL mode, idempotent migrations) across ~15 tables, including:
  `sessions`, `hypotheses`, `reviews`, `tournament_matches`, `elo_journal`, `tasks`,
  `transcripts`, `system_feedback`, `embeddings_meta`, `spans`, `events`, plus `bench_*`.
- **Vector store:** FAISS (`IndexFlatIP`) with asyncio locking + atomic save/load; embeddings
  chain Voyage → OpenAI → hash-fallback. Used by the Proximity agent for clustering/dedup.
- **Supervisor:** a durable SQLite-backed task queue with **bounded concurrency**, **task
  leasing**, dead-letter recovery, and resumption.
- **LLM abstraction:** provider-agnostic (Anthropic/Claude, OpenAI GPT/o-series, Gemini, Groq,
  Mistral, Together, Ollama, OpenRouter). Tool/function calling is mandatory. Supports thinking
  budgets, prompt caching, `reasoning_effort`, and a Batch API path for cheap ranking.
- **Prompts:** 14 **Jinja2** templates in `config/prompts/` (one per agent mode), derived from
  the paper's supplementary materials, with variable interpolation for context injection.
- **Tools:** `web_fetch`, `pubmed_search`, `arxiv_search`, `europe_pmc_search`; optional
  `web_search` via Tavily/Brave. "Science-skills" discovered via `SKILL.md` frontmatter.
- **Budgeting:** a `TokenBudget` system gives each agent a share under a global cap, with
  reservation-based accounting and a `PRICE_TABLE` for cost estimation.

Per-agent model routing example (you can use a strong model for generation/debate and a cheap
one for pairwise ranking):

```toml
[models]
generation       = "gpt-5"
reflection       = "gpt-4o"
ranking_pairwise = "gpt-4o"   # cheap, high volume
ranking_debate   = "gpt-5"    # expensive, top hypotheses only
metareview_final = "gpt-5"

[run]
budget_usd = 2.0
wall_clock = 600
```

## Validated results (each confirmed by partner wet-lab experiments)

- **Acute myeloid leukemia (cancer):** proposed existing drugs for repurposing that
  inhibited tumor cells *in vitro* at clinically relevant concentrations.
- **Liver fibrosis:** suggested epigenetic targets that showed anti-fibrotic activity and
  liver-cell regeneration in human hepatic organoids.
- **Antimicrobial resistance:** independently re-derived an unpublished mechanism of
  bacterial gene transfer (parallel in silico discovery).

## Implementation notes / gotchas

- The whole system is **model-agnostic and tool-light** — most of the engineering is the
  *orchestration* (queue, Elo bookkeeping, memory), not the science tools. Easiest entry point.
- Elo is the core trick: initialize all hypotheses at a base rating, update via pairwise
  match outcomes (an Elo K-factor), and treat rating stability as a convergence signal.
- The Proximity/embedding step matters more than it looks — without dedup, the tournament
  wastes compute comparing near-identical ideas.

## Sources

- [Towards an AI co-scientist — arXiv:2502.18864](https://arxiv.org/abs/2502.18864)
- [Full paper (PDF, ~81pp)](https://storage.googleapis.com/coscientist_paper/ai_coscientist.pdf)
- [Accelerating scientific breakthroughs with an AI co-scientist — Google Research blog](https://research.google/blog/accelerating-scientific-breakthroughs-with-an-ai-co-scientist/)
- [Co-Scientist: a multi-agent AI partner — Google DeepMind blog](https://deepmind.google/blog/co-scientist-a-multi-agent-ai-partner-to-accelerate-research/)
- [Open-source reimplementation — Kaimen-Inc/Co-Scientist (GitHub)](https://github.com/Kaimen-Inc/Co-Scientist)
