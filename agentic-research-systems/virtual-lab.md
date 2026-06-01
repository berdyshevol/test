# The Virtual Lab (Zou / Swanson, Stanford)

**Type:** Agentic LLM system (multi-agent "research team" with human in the loop)
**Organization:** Stanford (Kyle Swanson, James Zou et al.)
**Year:** 2024 bioRxiv → 2025 *Nature* (s41586-025-09442-9)
**Foundation model(s):** OpenAI GPT models (repo currently defaults to a recent GPT)

## What it is

An AI–human research collaboration: an LLM **Principal Investigator (PI) agent** leads a team
of LLM **scientist agents** (plus a scientific-critic agent) through a series of structured
**research meetings**, with a human providing only high-level feedback (~1% of the words). It
*proposed and designed* 92 SARS-CoV-2 nanobodies; humans experimentally validated them. The
agents decide and design; humans steer occasionally and run the bench work.

## Core specification

- **Paradigm:** simulated lab "meetings" — agents converse to plan and execute research.
- **Orchestration:** a PI agent assembles a team of domain-expert agents + a critic; meetings
  produce decisions and artifacts.
- **Self-improvement / evaluation:** the **scientific critic agent** challenges proposals;
  multiple meeting rounds refine the plan.

## Agents & roles

| Agent | Role |
|-------|------|
| **PI agent** | Sets direction, assembles the team, runs the agenda |
| **Scientist agents** | Domain experts (e.g. immunologist, ML specialist, computational biologist) created on demand |
| **Scientific critic** | Challenges feasibility/validity of proposals |
| **Human researcher** | High-level agenda + occasional guidance (~1% of dialogue) |

## Control loop (meetings)

1. **Team meeting:** all agents discuss a human-posed scientific agenda; PI synthesizes a
   decision.
2. **Individual meeting:** the human (or PI) works one-on-one with a single agent on a specific
   task (e.g. write a tool script).
3. Repeat across the project; meetings produce the pipeline, code, and design choices.

## Implementation detail

- **Tech stack:** Python; open-source (`zou-group/virtual-lab`); `pip install` or clone; needs
  `OPENAI_API_KEY`. Example driver: `nanobody_design/run_nanobody_design.ipynb`.
- **Configuration:** you define the **agenda** + the **agent team** (titles/expertise/goals);
  meetings are parameterized (participants, rounds). Human input is minimal by design.
- **Nanobody design pipeline the agents built:** **ESM** (protein language model for sequence
  design) → **AlphaFold-Multimer** (complex structure prediction) → **Rosetta** (modeling /
  scoring); used to design 92 candidates.
- **Memory/state:** meeting transcripts carry context across the project.

## Validated results

- Designed **92 nanobodies**; experimentally, **two** showed improved binding to recent
  SARS-CoV-2 variants (JN.1 / KP.3) while retaining ancestral-spike binding. Published in
  *Nature* (2025). Wet-lab validation by humans.

## Implementation notes / gotchas

- The reusable idea is the **PI + dynamically-created expert agents + critic, run as meetings**
  — a very general scaffold for "assemble a team to tackle problem X."
- Most of the science lives in the *tools the agents choose* (ESM/AlphaFold/Rosetta), not the
  meeting framework itself.

## Sources

- [The Virtual Lab of AI agents designs new SARS-CoV-2 nanobodies — Nature](https://www.nature.com/articles/s41586-025-09442-9)
- [bioRxiv preprint (2024)](https://www.biorxiv.org/content/10.1101/2024.11.11.623004v1)
- [Code — zou-group/virtual-lab (GitHub)](https://github.com/zou-group/virtual-lab)
