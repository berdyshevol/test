---
name: scout-research-agents
description: Research the web for NEW agentic LLM systems for scientific research (multi-agent "AI scientist" / agentic discovery systems like Google's AI co-scientist, Mozi, DrugAgent), then document each new one into the agentic-research-systems/ catalog in the house style. Use when the user wants to find, scout, discover, or catalog new agentic research systems, check for recent ones, or refresh/expand the agentic-research-systems folder. Triggers on phrases like "find new research agents", "any new agentic systems", "update the catalog", "scout for AI scientist systems".
---

# Scout Research Agents

Find newly published **agentic LLM systems for scientific research** and add them to the
local catalog at `agentic-research-systems/`, matching the existing house style.

## Scope (what counts)

IN scope — **agentic LLM systems for scientific research**: multi-agent or single-agent
LLM systems that plan, use tools, and reason to do science — generate/rank hypotheses,
drive drug-discovery pipelines, orchestrate biomedical analysis, etc. Examples already in
the catalog: Google AI co-scientist, Mozi, DrugAgent, BioMedAgent.

OUT of scope (do NOT add as their own entries): narrow molecular ML models with no agentic
loop (e.g. a bare property-prediction GNN), pure benchmarks, general LLM papers, marketing
posts with no technical substance. (A molecular model may be *mentioned inside* an entry as a
tool the agent calls, but it does not get its own file.)

## Workflow

Run these steps in order. **Stop after writing files — do NOT run any git commands**
(no add/commit/push). Leave that to the user.

1. **Load the existing catalog for dedup.** Read `agentic-research-systems/index.md` and list
   the current entry files. Build a set of system names already covered. Anything you find
   that is already cataloged is NOT new — skip it (or note it as "already have it").

2. **Fan-out web search.** Search several angles for *recent* systems (bias to the last
   ~12–18 months). Suggested angles — run them in parallel:
   - new arXiv / bioRxiv papers on "multi-agent LLM AI scientist" / "agentic drug discovery"
   - lab & company announcements (DeepMind, MIT, Stanford, academic groups)
   - "autonomous hypothesis generation" / "agentic scientific discovery" + the current year
   - GitHub repos for new agentic-science frameworks
   For breadth, you MAY spawn parallel `Explore`/`general-purpose` subagents, one per angle.

3. **Fetch primary sources.** For each promising hit, fetch the paper and any code repo. Prefer
   primary sources (arXiv/journal/GitHub) over blog summaries. If a publisher URL 403s, find an
   open-access mirror (PMC, arXiv HTML, project page).

4. **Verify before writing.** Only assert a claim if it is supported by the primary source (or
   2+ secondary sources agree). No hype, no invented numbers. If a detail is unconfirmed, say so
   or omit it.

5. **Write one file per NEW system** using `TEMPLATE.md` in this skill folder. Filename =
   kebab-case system name, e.g. `agentic-research-systems/<system-name>.md`. Prioritize
   **implementation-level detail** (architecture, agent roles & I/O, control loop, tools/models,
   tech stack, open-source repos) — that is the point of the catalog.

6. **Update the index.** Add a row to the table in `agentic-research-systems/index.md` (next
   number, name, type, org, year, file link). If a new system changes the "which to base it on"
   guidance, also note it in `implementation-blueprint.md`.

7. **Stop and summarize.** Report what was NEW (added), what was already covered (skipped), and
   anything promising-but-unverified worth a human look. Do not touch git.

## House rules (keep the catalog consistent)

- **Implementation-first.** Favor how to *build* it: agent roles with inputs→outputs, the
  control/orchestration loop, the tool/model inventory, tech stack, and any reference repo.
- **Cite primary sources** at the bottom of every file as markdown links.
- **Honesty caveat.** These systems *propose* (candidates, targets, hypotheses) that humans
  validate — they do not autonomously cure anything. Keep that framing; never overstate results.
- **One system per file.** Disambiguate when two papers share a name (note both).
- Match the tone, headers, and table style of the existing files.

## Reference

- Template: `TEMPLATE.md` (in this skill folder).
- Catalog location: `agentic-research-systems/` at the repo root.
