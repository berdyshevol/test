---
name: scout-research-agents
description: Research the web for NEW agentic LLM systems for scientific research (multi-agent "AI scientist" / agentic discovery systems like Google's AI co-scientist, Mozi, DrugAgent), then document each new one into the agentic-research-systems/ catalog in the house style. Use when the user wants to find, scout, discover, or catalog new agentic research systems, check for recent ones, or refresh/expand the agentic-research-systems folder. Triggers on phrases like "find new research agents", "any new agentic systems", "update the catalog", "scout for AI scientist systems".
---

# Scout Research Agents

Find newly published **agentic LLM systems for scientific research** and add them to the
local catalog at `agentic-research-systems/`, matching the existing house style.

## Scope (what counts)

This skill runs in one of two **scope modes**, chosen per run (see Step 0):

- **Field-specific** — only systems for a named field (e.g. *drug discovery / cancer*,
  *materials*, *math*). This was the catalog's original focus (cancer & antibiotics).
- **General** — any agentic LLM system for science, regardless of field.

IN scope (both modes) — **agentic LLM systems for scientific research**: multi-agent or
single-agent LLM systems that plan, use tools, and reason to do science — generate/rank
hypotheses, drive discovery pipelines, orchestrate analysis, etc. Examples already in the
catalog: Google AI co-scientist, Mozi, Robin, STELLA, Biomni, AI Scientist-v2.

OUT of scope (do NOT add as their own entries): narrow ML models with no agentic loop (e.g. a
bare property-prediction GNN), pure benchmarks, general LLM papers, marketing posts with no
technical substance. (Such a model may be *mentioned inside* an entry as a tool the agent
calls, but it does not get its own file.) In **field-specific** mode, also exclude systems
outside the chosen field.

Every entry is tagged with a **Domain** (e.g. `Drug discovery / cancer`, `Biomedical
(general)`, `ML / CS research`, `Materials`, `Chemistry`) in the index, so the catalog stays
organized in either mode.

## Workflow

Run these steps in order. **Step 0 picks the scope mode**, there is a **confirmation gate**
(step 3) before anything is written, a **cap** on how many systems are added per run, and an
**automated link-check** (step 8) before the commit.

**Per-run cap:** add at most **5 new systems** per run (default). If the user passed a number
in the skill args (e.g. "scout 3"), use that instead. If more than the cap qualify, keep the
most notable/most-cited and list the rest as "candidates for next run."

0. **Decide the scope for this run.** If the user's request or skill args already make the
   scope clear (e.g. "scout for *cancer* agents", "find *materials* science agents", "scout
   *anything* new"), use that and continue — do NOT ask. Otherwise call `AskUserQuestion` with:
   - **General** — any field of science, or
   - **Field-specific** — then capture which field (offer the catalog's original
     *drug discovery / cancer* as the recommended default, plus other common fields).
   Carry the chosen mode + field through the rest of the run; it controls what counts as
   in-scope in steps 2–6.

1. **Load the existing catalog for dedup.** Read `agentic-research-systems/index.md` and skim
   the entry files. Build an identity for each existing system — **name + aliases + arXiv id +
   repo URL + org** — not just the name. A find is a duplicate if ANY of those match. (This
   region is crowded: there are already two different "DrugAgent" papers, and STELLA vs
   BioMedAgent are distinct teams despite both being "self-evolving biomedical agents" — match
   on identity, not on a fuzzy name.)

2. **Fan-out web search.** Search several angles for *recent* systems (bias to the last
   ~12–18 months). In **field-specific** mode, focus every query on the chosen field; in
   **general** mode, spread across fields. Suggested angles — run them in parallel:
   - new arXiv / bioRxiv papers on "multi-agent LLM AI scientist" / "agentic <field> discovery"
   - lab & company announcements (DeepMind, MIT, Stanford, academic groups)
   - "autonomous hypothesis generation" / "agentic scientific discovery" + the current year
   - GitHub repos for new agentic-science frameworks
   For breadth, you MAY spawn parallel `Explore`/`general-purpose` subagents, one per angle.

3. **Build a shortlist and CONFIRM before writing.** Produce a short table of candidate NEW
   systems (name, org, year, 1-line what-it-is, primary-source URL, in/out of scope). Then
   **pause and ask the user to confirm** which to add (use `AskUserQuestion` if helpful). Do
   NOT write any files until the user confirms. Skip this gate ONLY if the user explicitly said
   "no confirmation / just add them."

4. **Fetch primary sources.** For each confirmed candidate, fetch the paper and any code repo.
   Prefer primary sources (arXiv/journal/GitHub) over blog summaries. If a publisher URL 403s,
   find an open-access mirror (PMC, arXiv HTML, project page). **Note in the file when a detail
   came only from a secondary source or could not be confirmed from the primary.**

5. **Verify before writing.** Only assert a claim if it is supported by the primary source (or
   2+ secondary sources agree). No hype, no invented numbers. Mark any unconfirmed specific
   (model name, benchmark number, agent list) with "(unconfirmed)" rather than stating it flatly.

6. **Write one file per confirmed system** using `TEMPLATE.md` in this skill folder. Filename =
   kebab-case system name, e.g. `agentic-research-systems/<system-name>.md`. Prioritize
   **implementation-level detail** (architecture, agent roles & I/O, control loop, tools/models,
   tech stack, open-source repos) — that is the point of the catalog.

7. **Update the index.** Add a row to the table in `agentic-research-systems/index.md` (next
   number, name, **domain**, type, org, year, file link). Use the entry's Domain tag and keep
   the table grouped/sorted so same-domain systems sit together (the original *drug discovery /
   cancer* cluster stays one clear section). If a new system changes the "which to base it on"
   guidance, also note it in `implementation-blueprint.md`.

8. **Link-check (automated).** Before committing, verify every internal link resolves and that
   no source URL is obviously broken. Example for internal links:
   ```bash
   cd agentic-research-systems && for f in *.md; do \
     grep -oE '\]\(\./[a-z0-9-]+\.md\)' "$f" | sed 's/](\.\///;s/)//' | \
     while read t; do [ -f "$t" ] || echo "BROKEN: $f -> $t"; done; done
   ```
   Fix anything reported before proceeding.

9. **Summarize.** Report what was NEW (added), what was already covered (skipped), what was
   left for next run (over the cap), and anything promising-but-unverified worth a human look.

10. **Commit and push to GitHub.** Stage the new/changed files, commit with a clear message
    (e.g. `Add <system> to agentic-research-systems catalog`), and push to the **current
    branch** with `git push -u origin <branch>`. On network failure, retry up to 4 times with
    exponential backoff (2s, 4s, 8s, 16s). Do NOT open a pull request unless the user asks.
    If there are no new systems to add, skip the commit and just report that the catalog is
    already up to date.

## House rules (keep the catalog consistent)

- **Implementation-first.** Favor how to *build* it: agent roles with inputs→outputs, the
  control/orchestration loop, the tool/model inventory, tech stack, and any reference repo.
- **Cite primary sources** at the bottom of every file as markdown links.
- **Honesty caveat.** These systems *propose* (candidates, targets, hypotheses) that humans
  validate — they do not autonomously cure anything. Keep that framing; never overstate results.
- **One system per file.** Disambiguate when two papers share a name (note both).
- **Flag uncertainty.** Details extracted from a README/blog/secondary source (not the primary
  paper) or that you couldn't confirm should be marked "(unconfirmed)" — don't state them flatly.
- Match the tone, headers, and table style of the existing files.

## Reference

- Template: `TEMPLATE.md` (in this skill folder).
- Catalog location: `agentic-research-systems/` at the repo root.
