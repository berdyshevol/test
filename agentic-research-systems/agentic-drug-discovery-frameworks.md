# Agentic Drug-Discovery Frameworks (DrugAgent, Mozi, BioMedAgent)

**Type:** Agentic LLM systems (multi-agent)
**Organization:** Various academic groups
**Years:** 2024–2026

A 2024–2026 wave of LLM **multi-agent** systems applies the "AI scientist" idea to
drug-discovery pipelines, including oncology.

## Common architecture

The recurring pattern across these frameworks:

- **LLM reasoning/planning core** — plans and orchestrates multistep workflows.
- **External tools** — molecular docking, property predictors, biological databases,
  code execution.
- **Memory** — to carry state across steps.
- **Reflection / critique loop** — self-evaluation of intermediate results.
- Often a **supervisor → worker hierarchy** (governed autonomy).

ReAct-style "reason + act" loops let agents sense their environment, call software/data,
and execute task sequences with minimal human input.

## Named frameworks

| Framework | What it is |
|-----------|------------|
| **DrugAgent** | Multi-agent LLM framework that fuses ML programming with biomedical expertise, systematically checking where domain knowledge is needed before deploying specialized tools. |
| **Mozi** | Dual-layer "governed autonomy": a **Control Plane** (supervisor-worker governance) + a **Workflow Plane** covering canonical stages from Target Identification → Lead Optimization. |
| **BioMedAgent** | Self-evolving multi-agent framework that learns to use bioinformatics tools and chain them into executable workflows for autonomous biomedical data tasks. |

## Reported efficiency gain

By autonomously reasoning from literature through to executable automation code, one agent
completed a process that traditionally spans months of cross-functional effort in **under
two hours** — a >400× reduction in cycle time.

## Sources

- [DrugAgent: Automating AI-aided Drug Discovery Programming through LLM Multi-Agent Collaboration — arXiv:2411.15692](https://arxiv.org/html/2411.15692v2)
- [Mozi: Governed Autonomy for Drug Discovery LLM Agents — arXiv:2603.03655](https://arxiv.org/pdf/2603.03655)
- [Empowering AI data scientists with a self-evolving multi-agent LLM framework (BioMedAgent) — Nature Biomedical Engineering](https://www.nature.com/articles/s41551-026-01634-6)
- [AI Agents in Drug Discovery — arXiv:2510.27130](https://arxiv.org/pdf/2510.27130)
- [A Framework for Autonomous AI-Driven Drug Discovery — bioRxiv](https://www.biorxiv.org/content/10.1101/2024.12.17.629024.full.pdf)
