# <System Name>

**Type:** Agentic LLM system (multi-agent / single-agent)
**Organization:** <lab / company / arXiv id>
**Year:** <year>
**Foundation model(s):** <e.g. Gemini 2.0 / GPT-4o / Qwen3 / model-agnostic>

## What it is

<2–4 sentences: what the system does, what it outputs (hypotheses? candidate molecules?
analysis?), and whether a human validates the output. Keep the "proposes, doesn't cure" framing.>

## Core specification

- **Paradigm:** <e.g. generate-debate-evolve / supervisor-worker / ReAct loop>
- **Orchestration:** <how work is scheduled; queue / planner / control loop>
- **Self-improvement / evaluation:** <Elo tournament / reflection-replanning / memory, if any>

## Agents & roles

| Agent | Input → Output | Role |
|-------|----------------|------|
| <name> | <in> → <out> | <what it does> |
| ... | ... | ... |

## Control loop

<Numbered steps of how a run proceeds, start to termination. Include the termination
condition (budget / wall-clock / convergence / human gate).>

## Implementation detail

<The most important section. Cover as available:>
- **Tech stack / framework:** <language, LangGraph / FastAPI / MCP / DB / vector store ...>
- **Tools & models invoked:** <databases, docking, property predictors, generative models ...>
- **Memory / state:** <context vs artifact state; vector store; persistence>
- **Governance / HITL:** <tool isolation, audit trail, human checkpoints, if any>
- **Reference implementation:** <open-source repo + how to run, if one exists>
- **Config / model routing example:** <short snippet if useful>

## Validated results

<Concrete, sourced outcomes — what was tested and confirmed (in vitro / in silico / benchmark
scores). No hype; cite where each result comes from.>

## Implementation notes / gotchas

<Optional: what's easy vs hard to reproduce, key tricks, pitfalls.>

## Sources

- [<primary paper> — arXiv/journal](<url>)
- [<code repo>](<url>)
- [<secondary> ](<url>)
