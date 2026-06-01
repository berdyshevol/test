# AI Research Agents for Drug & Cancer Discovery — Index

A catalog of discoveries on how AI "research agents" find antibiotics and cancer
remedies. Each entry links to a detailed spec file in this folder.

> **Scope note:** Two distinct kinds of system are covered here:
> 1. **Deep-learning discovery models** — narrow AI that screens or *designs* molecules.
> 2. **Agentic LLM "AI scientists"** — systems of language-model agents that generate,
>    debate, and rank *hypotheses* like a research team.

| # | Discovery | Type | Organization | Year | File |
|---|-----------|------|--------------|------|------|
| 1 | Google AI co-scientist | Agentic LLM (multi-agent) | Google DeepMind / Research | 2025 | [google-ai-co-scientist.md](./google-ai-co-scientist.md) |
| 2 | MIT antibiotic-discovery models (Halicin, Abaucin, generative) | Deep-learning discovery model | MIT (Collins/Barzilay, Jameel Clinic) | 2020–2025 | [mit-antibiotic-discovery.md](./mit-antibiotic-discovery.md) |
| 3 | Mozi — governed autonomy for drug discovery | Agentic LLM (dual-layer) | Academic (arXiv) | 2026 | [mozi-governed-autonomy.md](./mozi-governed-autonomy.md) |
| 4 | DrugAgent & BioMedAgent frameworks | Agentic LLM (multi-agent) | Various (academic) | 2024–2026 | [agentic-drug-discovery-frameworks.md](./agentic-drug-discovery-frameworks.md) |
| 5 | AI agents in cancer research & oncology | Agentic LLM (survey + examples) | Various (academic) | 2025 | [ai-agents-cancer-oncology.md](./ai-agents-cancer-oncology.md) |

### Building one yourself

| Doc | What it gives you |
|-----|-------------------|
| **[implementation-blueprint.md](./implementation-blueprint.md)** | Cross-system reference architecture, a "which system to base it on" table, pseudocode for both a hypothesis engine and a molecular-discovery tool, and practical build recommendations. |

Each per-system file now includes an **implementation-level section** (architecture, agent
roles & I/O, control loop, tools/models, tech stack, and — where available — open-source
reference repos and config examples) so the systems can be reimplemented.

## How to read this collection

- **Discovery models** (entry 2) work at the *molecule level*: represent molecules as
  graphs → predict or generate structure → screen by predicted activity/toxicity →
  synthesize and test. The intelligence lives in the GNN/VAE, not in any "reasoning" loop.
- **Agentic AI scientists** (entries 1, 3, 4, 5) work at the *hypothesis level*: an LLM is
  wrapped in a loop of **plan → call tools/literature → critique → rank → refine**, usually
  split across specialized agents coordinated by a supervisor, with a tournament/Elo or
  reflection mechanism standing in for peer review. Humans (or robotic labs) still do the
  wet-lab testing.

## Important caveat

None of these systems has produced a *cure* for cancer. What is verified is narrower:
agents propose **drug-repurposing candidates and novel targets** that then show activity in
cells/organoids/mice, and discovery models design **antibiotics** that work in animal
models. These are early-stage research findings, not approved therapies.

---
*Compiled 2026-06-01 via multi-source web research.*
