# Implementation Blueprint — Building Your Own Agentic Research System

A synthesis across all the systems in this folder, written as a starting point for an
implementation. Pick a track based on your goal.

## Which system to base it on?

| Your goal | Base it on | Why |
|-----------|-----------|-----|
| Generate & rank **research hypotheses** in any domain | **Google AI co-scientist** (+ the open-source reimpl) | Tool-light, model-agnostic, mostly orchestration. Easiest to clone. |
| **End-to-end drug discovery** (target → lead), production-grade | **Mozi** | Cleanest governance + real tool pipeline (LangGraph + MCP). |
| **Automate biomedical data analysis** from natural language | **BioMedAgent** | Self-evolving tool memory; concrete repo to fork. |
| **Find/design molecules** (antibiotics, hits) | **MIT D-MPNN + CReM/F-VAE** | The actual molecular ML; wrap as a tool your agent calls. |

## The common reference architecture

Every agentic system here is some arrangement of these six layers:

1. **Orchestrator / Supervisor** — parses the goal, plans steps, schedules work on a **durable
   task queue** with bounded concurrency, decides termination. (co-scientist: SQLite queue;
   Mozi: bounded loop with Direct/Simple/Complex modes.)
2. **Specialist agents / workers** — isolated context windows, each with a narrow role
   (generate, critique, rank, code, execute…). Route different models per role to control cost.
3. **Tool layer** — wrap external capabilities behind a uniform interface. **Use MCP** (Mozi's
   choice) so local scripts, Docker tools, and cloud APIs look the same to the planner.
4. **Memory / state** — split it:
   - *Context state* = rolling summaries that fit the LLM window.
   - *Artifact state* = real files/records (hypotheses, SMILES, SDF) in a DB, with lineage.
   - *Vector store* (FAISS) for dedup / retrieval (co-scientist Proximity, BioMedAgent MR).
5. **Evaluation / self-improvement loop** — the thing that makes it more than a pipeline:
   - co-scientist: **Elo tournament** of pairwise debates + meta-review feedback.
   - Mozi: **reflection-based replanning** (`SUFFICIENT_INFO` / `REPLAN` / continue).
   - BioMedAgent: **interactive exploration + memory retrieval**.
6. **Governance & human-in-the-loop** — role-based **tool isolation** (hard-coded, not just
   prompted), **auditable trajectories** (who/what/params per artifact), **HITL checkpoints**
   at high-uncertainty boundaries.

## A minimal hypothesis-engine loop (co-scientist style, pseudocode)

```
plan      = supervisor.parse(goal)
hyps      = generation.propose(goal, literature_search(goal))
for round in range(N):                      # until budget / Elo stable
    for h in hyps: reflection.review(h)     # novelty/correctness/testability
    clusters = proximity.cluster(embed(hyps))   # dedup
    elo = tournament(hyps)                   # pairwise debates -> Elo updates
    winners = top_k(hyps, by=elo)
    hyps += evolution.improve(winners)       # combine / simplify / analogize
    feedback = metareview(tournament_history)
    generation.bias(feedback)                # self-improvement signal
return metareview.overview(rank_by(elo))
```

## A minimal molecular-discovery tool (MIT style, pseudocode)

```
model = ensemble_DMPNN()                      # Chemprop, T=3, h=300
model.train(assay_data)                       # compound -> active/inactive
cands = model.predict(library_or_generated)   # ZINC / CReM / F-VAE output
cands = filter(cands, tox_model, novelty=tanimoto_dist > thresh)
return rank(cands)[:k]                         # hand to chemists
```

## Practical recommendations

- **Start with the co-scientist clone** even if your end goal is drug discovery — it teaches
  you the queue/Elo/memory plumbing without heavy chemistry tooling. Then swap in molecular
  tools (the MIT D-MPNN, docking, ADMET) as Mozi-style skill-graph nodes.
- **Make tools the boundary of trust.** Hard-code which agent role can call which tool. This
  is the single most important safety pattern across these papers.
- **Separate context state from artifacts.** Never feed raw SDF/PDB blobs into the prompt;
  summarize and keep files in the artifact store with lineage.
- **Budget compute explicitly** (per-agent token shares, wall-clock + cost caps, Elo-stability
  stop). Test-time compute is the lever that improves quality — but it's unbounded if you let it.
- **Add HITL gates** before anything expensive or irreversible (synthesis lists, final ranking).

## Caveat (carry it into any build)

None of these systems *cures* anything autonomously. They **propose** — candidates, targets,
molecules — that humans then validate in the lab. Design your system as a proposer with humans
on the critical path, not an autonomous decision-maker.

## See also (per-system detail)

- [Google AI co-scientist](./google-ai-co-scientist.md)
- [Mozi — governed autonomy](./mozi-governed-autonomy.md)
- [DrugAgent & BioMedAgent](./agentic-drug-discovery-frameworks.md)
- [MIT antibiotic discovery / D-MPNN](./mit-antibiotic-discovery.md)
- [AI agents in cancer & oncology](./ai-agents-cancer-oncology.md)
