# Agentic Drug-Discovery Frameworks (DrugAgent & BioMedAgent)

**Type:** Agentic LLM systems (multi-agent)
**Organization:** Various academic groups
**Years:** 2024–2026

A 2024–2026 wave of LLM **multi-agent** systems applies the "AI scientist" idea to
drug-discovery pipelines, including oncology. This file covers **DrugAgent** and
**BioMedAgent**; **Mozi** (the most complete) has its own file:
[mozi-governed-autonomy.md](./mozi-governed-autonomy.md).

## Common architecture (the pattern they share)

- **LLM reasoning/planning core** — plans and orchestrates multistep workflows.
- **External tools** — molecular docking, property predictors, biological databases, code exec.
- **Memory** — to carry state across steps (and, increasingly, to self-improve).
- **Reflection / critique loop** — self-evaluation of intermediate results.
- Often a **supervisor → worker hierarchy** with **ReAct-style** "reason + act" loops.

---

## DrugAgent — note: two different papers share this name

### Variant A — Planner/Instructor (arXiv:2411.15692, "Automating AI-aided Drug Discovery Programming")
A **two-agent** system that automates the *ML-programming* side of drug discovery:

- **LLM Planner** — *Idea Generation* (derive K candidate solutions from the task) then
  *Exploration* (dispatch ideas, revise from success/failure reports).
- **LLM Instructor** — turns an idea into executable code; performs standard ML actions
  (read/edit scripts, run code) and injects domain knowledge from three curated doc types:
  (1) data acquisition/preprocessing, (2) molecule/protein encodings (fingerprints, graphs),
  (3) domain models (**ChemBERTa** for molecules, **ESM** for proteins).
- **Control flow:** Planner → Instructor → evaluation feedback → Planner refinement → repeat
  to an iteration limit.
- **Worked example (DTI on DAVIS):** inputs = SMILES + protein sequence; drug featurized with
  **ECFP4**, protein with **CT** encoding, **Random Forest** over concatenated features.
  Reported +4.92% ROC-AUC vs. a ReAct baseline.

### Variant B — Coordinator + specialist agents (arXiv:2408.13378, "Multi-Agent LLM Reasoning for DTI")
A genuine **multi-agent** design for drug-target interaction reasoning:

- **Coordinator** managing three specialists:
  - **Knowledge Graph Agent** — queries DrugBank, CTD, DGIdb, STITCH.
  - **Search Agent** — web search engines.
  - **AI Agent** — deep-learning DTI models.

> If someone says "DrugAgent," confirm which paper they mean — the architectures are different.

---

## BioMedAgent — self-evolving multi-agent data analyst

Lets biomedical users run analyses from **natural language**, no coding required. Hit a **77%
success rate** on the BioMed-AQA benchmark (327 tasks).

**Agents**
- **Planner** — task decomposition / workflow planning.
- **Coder** — generates & refines analysis code.
- **Executor** — runs code, manages tool invocations.
- **Tool Manager** — tool perception, capability matching, chain-of-thought tool selection;
  manages both local containerized tools and web APIs.

**Self-evolving memory (the distinctive bit)**
- **Interactive Exploration (IE)** — learn from execution results, refine strategies via
  feedback loops.
- **Memory Retrieval (MR)** — store successful execution patterns, retrieve them for future
  tasks. Continuous improvement **without retraining**; toolset adapts over time.

**Tool integration**
- Tools declared in `tool_info.json` (name, description, params, outputs); auto-discovered.
- Local tools (e.g. `cel2matrix`, `survival_curve`, `t_test`) run in **Docker**; web tools via API.
- Tool Manager orchestrates dependencies + data flow → sequential/conditional chaining.

**Stack & layout (from the repo)**
- Python 3.10, GPT-4o-mini primary, **Redis** for caching/state, Docker for tool isolation.
- Modules: `agent.py` (multi-agent logic), `config.py`, `utils.py`, `tool/`, `server/`,
  `lab/`, `data/`, `scripts/`.
- Run: `conda create -n BioMedAgent python=3.10` → `pip install -r requirements.txt` →
  `export OPENAI_API_KEY=...` → `python demo.py --task statistics`.
- Control flow: NL task → Planner decomposes → Tool Manager selects tools → Coder writes code
  → Executor runs → memory logs outcome → interpretable report.

---

## Reported efficiency gain (the headline number)

A focal graph-enabled agent reasoning from literature through to executable automation code
completed in **under two hours** a process that traditionally spans months — a **>400×**
cycle-time reduction.

## Sources

- [DrugAgent (Planner/Instructor) — arXiv:2411.15692](https://arxiv.org/html/2411.15692v2)
- [DrugAgent (Coordinator/multi-agent DTI) — arXiv:2408.13378](https://arxiv.org/pdf/2408.13378)
- [BioMedAgent — Nature Biomedical Engineering](https://www.nature.com/articles/s41551-026-01634-6)
- [BioMedAgent source code (GitHub)](https://github.com/BOBQWERA/BioMedAgent)
- [AI Agents in Drug Discovery (review) — arXiv:2510.27130](https://arxiv.org/pdf/2510.27130)
- [A Framework for Autonomous AI-Driven Drug Discovery — bioRxiv](https://www.biorxiv.org/content/10.1101/2024.12.17.629024.full.pdf)
