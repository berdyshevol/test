# AI Agents in Cancer Research & Oncology

**Type:** Agentic LLM systems (survey + concrete examples)
**Organization:** Various academic groups
**Year:** 2025

## What an AI agent is (in this context)

A (semi-)autonomous system that can **sense, learn, and act upon its environment**. Equipped
with logical reasoning, an LLM can plan and orchestrate complex workflows; given the ability
to act, it becomes an **agent** that interacts with external knowledge or software and
executes task sequences with minimal or no human input.

In oncology, agents can:
- autonomously optimize drug design and development,
- propose therapeutic strategies for clinical cases,
- handle complex, multistep problems beyond previous AI generations.

## Concrete example: focal graph-enabled agent → Wnt pathway targets

When prompted to plan and execute a research program to identify a novel oncology target in
the **Wnt pathway**, a focal graph-enabled AI agent identified several potentially novel
targets — including the **eIF2 complex**. A process that traditionally spans months of
cross-functional effort was completed in **under two hours** (>400× cycle-time reduction).

## Supporting techniques in AI cancer drug discovery / repurposing

- **Data integration:** combine pharmacological data with genomic information to assess how
  genetic variation influences drug efficacy and safety (multiomics drug-response resources).
- **Network analysis:** 930 cancer cell lines annotated with multiomics data + protein–protein
  interaction networks → anticancer target priority maps (370 priority targets across 27
  cancer types).
- **Synergistic combinations:** ML models (Random Forest, XGBoost, deep neural nets, graph
  convolutional networks) trained on 496 tested drug combinations extrapolated to ~1.6M
  possible combinations.
- **Structure prediction:** AlphaFold (2024 Nobel Prize in Chemistry) accelerates target
  understanding for cancer drug development.

## Caveat

These are early-stage findings — proposed targets/candidates validated in cells, organoids,
or animal models, not approved therapies or "cures."

## Sources

- [Artificial intelligence agents in cancer research and oncology — Nature Reviews Cancer](https://www.nature.com/articles/s41568-025-00900-0)
- [AI-Based Methods for Drug Repurposing and Development in Cancer — MDPI](https://www.mdpi.com/2076-3417/15/5/2798)
- [Applications of Artificial Intelligence in Drug Repurposing — Advanced Science (Wiley)](https://advanced.onlinelibrary.wiley.com/doi/10.1002/advs.202411325)
- [AI-Driven Innovations in Oncology Drug Discovery — PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC12232943/)
