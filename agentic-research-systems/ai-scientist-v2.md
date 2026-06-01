# The AI Scientist-v2 (Sakana AI)

**Type:** Agentic LLM system (end-to-end autonomous researcher)
**Organization:** Sakana AI
**Year:** 2025 (arXiv:2504.08066)
**Foundation model(s):** model-agnostic; defaults route Claude 3.5 Sonnet (experiments), o1-preview (write-up), GPT-4o (citations)

## What it is

A fully autonomous system that takes a research topic and produces a complete ML research
paper — generating hypotheses, designing and running experiments (it writes and executes the
code), analyzing results, and writing the manuscript. It famously had one of three
autonomously generated manuscripts exceed the human acceptance threshold at a peer-reviewed
ICLR workshop. Output is *proposed* science (limited to computational ML research); humans
still review and the system cannot run physical lab work.

## Core specification

- **Paradigm:** progressive **agentic tree search** (best-first tree search, BFTS) over
  experiment trajectories, guided by an **experiment manager agent**. No human-authored
  templates (the key advance over v1).
- **Orchestration:** parallel workers expand a search tree of experiment nodes; the manager
  decides which branches to pursue based on performance signals.
- **Self-improvement / evaluation:** built-in peer-review-style review phase; tree search
  prunes/debugs failing nodes.

## Agents & roles

| Agent | Input → Output | Role |
|-------|----------------|------|
| Ideation | topic → JSON ideas (hypotheses + experiments) | Generates structured research ideas |
| Experiment manager | idea → tree-search policy | Orchestrates BFTS; picks which nodes to expand/debug |
| Worker (×N) | node → executed experiment + results | Writes & runs experiment code in parallel paths |
| Write-up | results → manuscript | Drafts the paper (figures, citations), ~20–30 min |
| Review | manuscript → scores | Peer-review-style evaluation |

## Control loop

1. **Ideation** (`perform_ideation_temp_free.py`) → JSON of hypotheses + proposed experiments.
2. **Experiment stage:** BFTS explores experiment nodes; failing nodes are debugged up to
   `max_debug_depth` with probability `debug_prob`; Stage 1 launches `num_drafts` root trees.
3. **Write-up:** generate manuscript draft with plots + citations.
4. **Review:** score the paper. Output PDFs + a tree visualization land in a timestamped dir.

## Implementation detail

- **Tech stack:** Python; open-source (`SakanaAI/AI-Scientist-v2`). Search controlled by
  `bfts_config.yaml`.
- **Key BFTS params:** `num_workers` (parallel paths), `steps` (max nodes, e.g. 21 with 3
  concurrent expansions), `num_seeds`, `max_debug_depth`, `debug_prob`, `num_drafts`.
- **Per-role model routing** via CLI flags (`--model_writeup`, `--model_citation`,
  `--model_review`, `--model_agg_plots`); experiments default to Claude 3.5 Sonnet (~$15–20/run).
- **Run:**
  ```bash
  python launch_scientist_bfts.py \
    --load_ideas "path/to/ideas.json" \
    --model_writeup o1-preview-2024-09-12 \
    --model_citation gpt-4o-2024-11-20 \
    --model_review gpt-4o-2024-11-20
  ```
- **Outputs:** `experiments/[timestamp]/logs/0-run/unified_tree_viz.html` + final PDFs.

## Validated results

- Three fully autonomous manuscripts submitted to an ICLR 2025 workshop; **one exceeded the
  average human acceptance threshold** — first AI-generated paper to pass peer review (per the
  authors). Scope limited to computational ML research.

## Implementation notes / gotchas

- The **tree search + experiment manager** is the reusable idea: treat research as search over
  experiment nodes with debug/prune, rather than a linear pipeline.
- Strictly computational — no wet-lab. Best template if your "experiments" are code/simulations.

## Sources

- [The AI Scientist-v2 — arXiv:2504.08066](https://arxiv.org/abs/2504.08066)
- [Code — SakanaAI/AI-Scientist-v2 (GitHub)](https://github.com/SakanaAI/AI-Scientist-v2)
- [Sakana AI — The AI Scientist *v1* (the v1 line was published in Nature; **v2 above is an arXiv preprint, not in Nature**)](https://sakana.ai/ai-scientist-nature/)
