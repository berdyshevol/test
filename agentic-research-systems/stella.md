# STELLA (Princeton / Stanford)

**Type:** Agentic LLM system (multi-agent, self-evolving)
**Organization:** Princeton University & Stanford University
**Year:** 2025 (arXiv:2507.02004 / bioRxiv 2025.07.01.662467)
**Foundation model(s):** Claude 4 Sonnet (Dev + Tool Creation agents); Gemini 2.5 Pro (Manager + Critic)

## What it is

A self-evolving biomedical research agent that overcomes the "fixed toolset" bottleneck: it
**writes and integrates its own new bioinformatics tools** as it works, and distills
successful workflows into reusable reasoning templates — so it gets better with use. It
*proposes* therapeutic targets and designs (validated downstream/in silico); humans confirm.

## Core specification

- **Paradigm:** multi-agent reasoning + **self-evolution** via two growing assets: an evolving
  **Template Library** (reasoning strategies) and a dynamic **Tool Ocean** (executable tools).
- **Orchestration:** Manager plans a "Reasoning Pathway"; Dev executes; Critic evaluates; Tool
  Creation fills capability gaps.
- **Self-improvement / evaluation:** successful workflows → new templates; Critic feedback →
  new tools. Performance scales with compute budget (HLE accuracy ~doubled 14%→26% with trials).

## Agents & roles

| Agent | Input → Output | Role |
|-------|----------------|------|
| **Manager** | research goal → Reasoning Pathway | Decomposes the goal into a strategic step plan |
| **Dev** | step → results | Creates a self-contained **conda env**, writes & runs Python (e.g. `diff_analysis.py`) |
| **Critic** | intermediate result → feedback | Quality check; flags "correct but not actionable" results |
| **Tool Creation** | capability gap → new tool | Searches resources, then builds/tests/integrates tools into the Tool Ocean |

## Control loop

1. Manager receives the goal → builds a **Reasoning Pathway** (guided by the Template Library).
2. Dev executes each step in an isolated conda environment (real bioinformatics code).
3. Critic assesses results; on gaps, Tool Creation finds or **builds** a new tool.
4. Iterate; on success, the workflow is distilled into a **new reasoning template** for reuse.

## Implementation detail

- **Tech stack:** Python; Dev agent spins up **self-contained conda environments** per task.
- **Tool Ocean (3 categories):**
  - *Databases:* PubMed, ClinVar, Protein Data Bank (PDB).
  - *Foundation models:* AlphaFold 3 (structure), scGPT (single-cell), ESM3 (protein LM).
  - *Custom tools:* network analysis + bespoke data-integration scripts the agent writes.
- **Self-evolution mechanisms:** Template Library (distilled reasoning workflows) + Tool Ocean
  (Tool Creation Agent autonomously identifies/tests/integrates new tools).
- **Model routing:** Dev + Tool Creation = Claude 4 Sonnet; Manager + Critic = Gemini 2.5 Pro.

## Validated results

- Identified multiple **novel therapeutic targets for AML and melanoma**; designed enzymes
  with ~3× efficiency over wild type (in-silico / downstream validation).
- Benchmarks: **~26%** Humanity's Last Exam: Biomedicine (up to +8 vs next best), **54%**
  LAB-Bench DBQA (SOTA), **63%** LAB-Bench LitQA (52%→63% as budget scales 1×→9×).

## Implementation notes / gotchas

- The standout idea is **agents that build their own tools** — if you want an agent that isn't
  capped by a predefined toolset, this is the reference design.
- Note: distinct from "BioMedAgent" (Nature Biomed Eng) despite both being self-evolving
  biomedical multi-agent systems — different papers/teams.

## Sources

- [STELLA: Self-Evolving LLM Agent for Biomedical Research — arXiv:2507.02004](https://arxiv.org/abs/2507.02004)
- [Full HTML](https://arxiv.org/html/2507.02004v1)
- [bioRxiv](https://www.biorxiv.org/content/10.1101/2025.07.01.662467v1)
