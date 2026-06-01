# Biomni (Stanford)

**Type:** Agentic LLM system (general-purpose, single generalist agent)
**Organization:** Stanford (SNAP / Zou-adjacent groups)
**Year:** 2025 (bioRxiv 2025.05.30.656746)
**Foundation model(s):** Claude (default `claude-sonnet-4`); configurable (OpenAI/Azure/Gemini/Groq/Bedrock); plus a specialized Biomni-R0 (32B Qwen, RL-tuned)

## What it is

A general-purpose biomedical AI agent that autonomously executes a wide range of research
tasks — gene prioritization, drug repurposing, rare-disease diagnosis, microbiome analysis,
molecular cloning, single-cell analysis, protocol design — from a single natural-language
request, with no task-specific prompt tuning. It *proposes and executes analyses*; humans
review outputs (and it runs LLM-generated code, so sandboxing matters).

## Core specification

- **Paradigm:** generalist agent = **LLM reasoning + retrieval-augmented planning +
  code-based execution**, with iterative self-correction.
- **Orchestration:** single agent that plans, retrieves relevant tools/knowledge, generates
  and runs Python, then refines.
- **Self-improvement / evaluation:** iterative refinement loop; evaluated on Biomni-Eval1.

## Agents & roles

| Component | Input → Output | Role |
|-----------|----------------|------|
| Reasoning core (LLM) | NL task → plan | Decomposes the biomedical task |
| Retrieval-augmented planner | plan → contextualized plan | Pulls relevant data/tools/know-how before acting |
| Code executor | plan step → results | Generates + runs Python (full privileges) |

(Single generalist agent rather than a fixed multi-agent committee.)

## Control loop

1. User calls `agent.go("<biomedical task>")`.
2. LLM reasons over biomedical context → plan.
3. Retrieve relevant knowledge/tools/protocols (RAG).
4. Generate + execute Python code.
5. Iteratively self-correct until the task is complete; return results.

## Implementation detail

- **Tech stack:** Python; open-source (`snap-stanford/Biomni`); `pip install biomni`.
- **Environment / tools:** an **~11 GB data lake** of integrated biomedical datasets +
  knowledge bases (auto-downloaded on first init), bundled biomedical software packages, a
  curated **"know-how" library** of protocols, and **MCP** support for adding external tools.
- **Memory/state:** retrieval over the data lake + know-how library; code runs in the host env.
- **Models:** primary Claude via Anthropic API; **Biomni-R0** is a 32B Qwen reasoning model
  RL-optimized for the domain.
- **Run:**
  ```python
  from biomni.agent import A1
  agent = A1(path='./data', llm='claude-sonnet-4-20250514')
  agent.go("Plan a CRISPR screen to identify genes that regulate ...")
  ```
- **Governance / gotcha:** executes LLM-generated code with **full system privileges** —
  the authors explicitly warn to run it sandboxed/isolated in production.

## Validated results

- **LAB-Bench:** 74.4% DbQA, 81.9% SeqQA — reported to outperform human experts on those.
- Demonstrated end-to-end on wearable-sensor analysis, scRNA-seq/ATAC-seq pipelines, and
  autonomous lab-protocol design. (Benchmarks/in-silico; not clinical outcomes.)

## Implementation notes / gotchas

- Closest thing to a "do-anything biomedical analyst." The big engineering lift is the **data
  lake + tool environment**, not the agent loop.
- Sandbox the code executor before pointing it at anything sensitive.

## Sources

- [Biomni: A General-Purpose Biomedical AI Agent — bioRxiv](https://www.biorxiv.org/content/10.1101/2025.05.30.656746v1)
- [Code — snap-stanford/Biomni (GitHub)](https://github.com/snap-stanford/Biomni)
- [Project site](https://biomni.stanford.edu)
