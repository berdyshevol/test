# Mozi — Governed Autonomy for Drug-Discovery LLM Agents

**Type:** Agentic LLM system (multi-agent, dual-layer)
**Organization:** Academic (arXiv:2603.03655)
**Year:** 2026

The most **end-to-end and implementation-complete** of the drug-discovery agent
frameworks. Design principle: *"free-form reasoning for safe tasks, structured execution
for long-horizon pipelines."* It pairs LLM flexibility with the determinism of
computational-biology tools, specifically to stop agents drifting into irreproducible
trajectories where early hallucinations compound into downstream failure.

## Two-layer architecture

### Layer A — Control Plane (governance & orchestration)

- **Supervisor–worker hierarchy** with a bounded execution loop and three decision modes:
  - **Direct** — answer simple queries immediately.
  - **Simple** — single-worker execution.
  - **Complex** — multi-step plan with a step budget **K**; "minimal necessary steps," no
    open-ended exploration.
- **Role-based tool isolation** via **hard-coded tool filtering** (not just prompting):
  - **Strict mode** (production) physically restricts each worker's tool list by role — e.g.
    a Research Worker can't touch expensive docking clusters.
  - **Permissive mode** (debugging) exposes the full toolset.
  - Workers are independent agents with **isolated context windows** (localizes tokens,
    prevents cross-worker contamination).
- **Reflection-based replanning** implemented as a **self-correction prompt** (not a separate
  critic agent), emitting one of: `SUFFICIENT_INFO` (halt early), `REPLAN` (modify remaining
  steps), or continue.
- **Auditable trajectory:** records which agent + tool + parameters produced each artifact
  (reproducibility + regulatory transparency).

### Layer B — Workflow Plane (stateful skill graphs)

- Implemented with **LangGraph** — long-horizon workflows as **cyclic graphs** with
  persistence and state management.
- Skill graphs: **nodes** = executable steps with input/output contracts; **edges** = data-flow
  dependencies; **state** = persistent artifact tracking.
- **Format Adapters** at every node's input/output programmatically validate & clean data
  (e.g. ensure PDB files are standard, side chains complete) — prevents "garbage in, garbage out."
- **Human-in-the-loop (HITL) checkpoints** gate high-uncertainty boundaries (e.g. before
  finalizing a candidate list): approve / reject / correct parameters / rollback to a prior state.

## The four canonical drug-discovery stages (the pipeline)

1. **Target Identification (TI):** entity normalization (→ MeSH/ICD), multi-source aggregation
   (PubMed, clinical trials), LLM scores/ranks targets by evidence confidence, structure
   retrieval from PDB with automated prep (PDBFixer side-chain repair, protonation).
2. **Hit Identification (HI) — parallel dual-stream:**
   - *Path A (generative):* pocket-based de novo design with **DiffSBDD**, then Tanimoto
     clustering for diversity.
   - *Path B (screening):* high-throughput virtual screening with a DL affinity model
     (**LigUnity**). Streams are fused, deduplicated, re-ranked.
3. **Hit-to-Lead (H2L):** R-group exploration (optimize side chains, keep scaffold), scaffold
   hopping (swap core, keep pharmacophores), two-tier filtration (remove **PAINS/Brenk**
   structural alerts, then **ADMET-AI** for tox/bioavailability).
4. **Lead Optimization (LO):** closed-loop multi-objective optimization with RL (**REINVENT4**),
   composite reward = predicted affinity + drug-likeness (QED) + synthetic accessibility (SAS);
   top candidates validated via **MM-GBSA**; LLM fuses quantitative scores with literature for
   final ranking.

## Data fabric & tool federation

- **Hybrid state:** *Context State* (rolling tool-output summaries for the LLM window) +
  *Artifact State* (actual SMILES lists / SDF / docking grids with lineage tracking). Keep
  these separate — don't stuff raw files into the prompt.
- **Model Context Protocol (MCP)** unifies heterogeneous tools (local Python scripts, Docker
  containers, remote cloud APIs) behind a standard discover/invoke/error-handle interface, so
  Layer A reasons about tools abstractly while Layer B handles execution.
- **Tool/model inventory** (a ready-made shopping list for any drug-discovery agent):
  - *DB & retrieval:* UniProt, PubMed, PubChem, DrugBank, Open Targets, KEGG, DGIdb.
  - *Protein prep:* PDBFixer, OpenMM. *Docking:* AutoDock Vina.
  - *Generative:* DiffSBDD, REINVENT4. *Screening/DTI:* LigUnity.
  - *ADMET:* ADMETlab 3.0, ADMET-AI. *Filters:* PAINS/Brenk.
  - *Structure/cheminformatics:* OpenBabel, RDKit. *Scoring:* MM-GBSA, AlphaFold3 (ipTM).

## Evaluation

**PharmaBench** — 88 tasks (55 from Therapeutics Data Commons, 28 from a "Human-Last Exam"
text-reasoning set, 5 auxiliary). Mozi (Qwen3-235B) hit 33/54 classification accuracy and
1.169 SMAPE regression, beating a Biomni baseline; on HLE tasks Mozi (Deepseek-V3.2) reached
21.4%. Three end-to-end case studies: Crohn's, Parkinson's, Sepsis — showing stage transitions,
error containment, and HITL.

## Why this is the best blueprint for a *production* agentic discovery system

- Clean separation of **governance (Layer A)** from **science workflow (Layer B)** — you can
  build Layer B as plain LangGraph DAGs and bolt on governance later.
- **MCP + hard-coded tool filtering** is a concrete, copyable safety pattern.
- The **four-stage skill graph** maps directly onto real drug-discovery milestones, so each
  node is independently testable.

## Sources

- [Mozi: Governed Autonomy for Drug Discovery LLM Agents — arXiv:2603.03655](https://arxiv.org/abs/2603.03655)
- [Full HTML](https://arxiv.org/html/2603.03655v1)
- [Hugging Face paper page](https://huggingface.co/papers/2603.03655)
