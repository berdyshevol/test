# Robin (FutureHouse)

**Type:** Agentic LLM system (multi-agent, end-to-end therapeutic discovery)
**Organization:** FutureHouse
**Year:** 2025 (arXiv:2505.13400)
**Foundation model(s):** built on FutureHouse's agent stack (Crow/Falcon/Finch)

## What it is

A multi-agent system that automates the key *intellectual* steps of experimental therapeutic
discovery: it generates hypotheses, proposes experiments, and analyzes the resulting data in
an iterative loop — humans only execute the physical wet-lab experiments. Robin *proposed*
ripasudil (an approved glaucoma drug) as a novel candidate for dry age-related macular
degeneration (dAMD); validation was done in the lab. It proposes, humans confirm.

## Core specification

- **Paradigm:** iterative discovery loop — hypothesis generation → experimental design →
  data analysis → next hypothesis.
- **Orchestration:** three specialized FutureHouse agents composed into the loop; outputs
  (hypotheses, experiment choices, analyses, main-text figures) generated autonomously.
- **Self-improvement / evaluation:** each experimental round's analysis feeds the next round.

## Agents & roles

| Agent | Input → Output | Role |
|-------|----------------|------|
| **Crow** | research question → literature synthesis / hypotheses | Broad literature search → therapeutic hypotheses |
| **Falcon** | hypothesis → candidate molecules + assay design | Drug-candidate evaluation & experimental design |
| **Finch** | raw experimental data → interpretation | Complex data analysis (e.g. RNA-seq) → next candidates |

## Control loop

1. **Hypothesis generation:** Crow reviews literature → therapeutic hypothesis; Falcon selects
   candidate molecules to test.
2. **Experimental design:** Robin proposes the next experiment (e.g. RNA-sequencing) to probe
   mechanism.
3. **Data analysis:** Finch analyzes outcomes, picks promising candidates → loop back.
4. Humans run the physical experiments between iterations.

## Implementation detail

- **Tools:** FutureHouse's literature/data agents (Crow = literature QA, Falcon = deep search,
  Finch = data analysis) available via the FutureHouse platform/API.
- **Worked discovery (ripasudil / dAMD):**
  - *Phase 1:* hypothesize boosting RPE phagocytosis treats dAMD; testing 10 Falcon-selected
    molecules flags Y-27632 (a ROCK inhibitor) that increases RPE phagocytosis.
  - *Phase 2:* RNA-seq (analyzed by Finch) shows Y-27632 upregulates **ABCA1** (lipid efflux),
    explaining the mechanism.
  - *Phase 3:* a second screen identifies **ripasudil** (clinically used for glaucoma) as the
    superior candidate; reported ~7.5× increase in phagocytosis.
- **Timeline:** whole project (concept → paper) in ~2.5 months by a small team.

## Validated results

- Identified **ripasudil** as a novel dAMD candidate with a clear mechanistic hypothesis
  (ROCK inhibition → ABCA1 → phagocytosis), all reasoning/analysis done by Robin; wet-lab
  done by humans. Early-stage research finding, not an approved dAMD therapy.

## Implementation notes / gotchas

- Cleanest example of an **experiment-in-the-loop** discovery agent where the bottleneck is
  human wet-lab execution between AI iterations.
- Built on a pre-existing agent platform (FutureHouse) — easier to *use* than to reimplement.

## Sources

- [Robin: a multi-agent system for automating scientific discovery — arXiv:2505.13400](https://arxiv.org/abs/2505.13400)
- [FutureHouse research announcement](https://www.futurehouse.org/research-announcements/demonstrating-end-to-end-scientific-discovery-with-robin-a-multi-agent-system)
- [MIT News — FutureHouse accelerates scientific discovery](https://news.mit.edu/2025/futurehouse-accelerates-scientific-discovery-with-ai-0630)
