# MIT Antibiotic-Discovery Models (Halicin, Abaucin, Generative Design)

**Type:** Deep-learning discovery models (molecule-level AI)
**Organization:** MIT — Collins Lab & Barzilay Lab, Jameel Clinic / Broad Institute
**Years:** 2020 (Halicin) → 2023 (Abaucin) → 2025 (generative design)

This is the line of work behind the "AI found a new antibiotic" headlines. It evolved
from *screening* existing molecules to *generating* brand-new ones.

## 1. Halicin (2020) — a screening model

- **Architecture:** A **directed message-passing neural network** (a graph neural network).
  Molecules are treated as graphs (atoms = nodes, bonds = edges); the model learns its own
  continuous-vector representation of structure instead of using hand-crafted descriptors.
- **Training set:** ~2,500 molecules (~1,700 FDA-approved drugs + ~800 natural products),
  each labeled for whether it inhibited growth of *E. coli*.
- **Inference / screening:** The trained model screened **>100 million molecules** from the
  **ZINC15** library in **~3 days**, ranked by predicted antibacterial activity. A *separate*
  ML model predicted human-cell toxicity to filter candidates.
- **Result:** Flagged **halicin** (originally a diabetes drug candidate), which kills bacteria
  via a novel mechanism — disrupting the membrane electrochemical gradient.

## 2. Abaucin (2023)

- Same recipe, narrower target. ~7,500 molecules were screened in the lab against
  *Acinetobacter baumannii*, used to train a directed message-passing deep neural network,
  then predictions were run over the **Drug Repurposing Hub** to find structurally novel
  actives. Yielded **abaucin**.

## 3. Generative design (2025) — the architectural shift

Instead of picking molecules that already exist, the lab moved to *designing* new ones.

- **Two generative algorithms:**
  - **CReM (Chemically Reasonable Mutations)** — grows molecules by adding/replacing/deleting
    atoms and chemical groups around an active fragment (F1).
  - **F-VAE (Fragment-based Variational Autoencoder)** — builds a fragment into a full
    molecule, pretrained on **>1 million ChEMBL molecules**.
- **Scale & funnel:**
  - *N. gonorrhoeae* (Gram-negative): ~45M fragments → ML screen to ~4M → safety/novelty
    filter to ~1M → ~7M generated candidates → ~1,000 compounds → 80 for synthesis (2 made).
  - *S. aureus / MRSA* (Gram-positive): >29M generated → filtered to ~90 → 22 synthesized.
- **Results:** Two designed compounds — **NG1** (gonorrhea) and **DN1** (MRSA) — worked in
  lab and mouse models, apparently disrupting bacterial cell membranes via novel mechanisms.

## Sources

- [Artificial intelligence yields new antibiotic — MIT News, 2020 (Halicin)](https://news.mit.edu/2020/artificial-intelligence-identifies-new-antibiotic-0220)
- [Using AI, scientists find a drug to combat drug-resistant infections — MIT News, 2023 (Abaucin)](https://news.mit.edu/2023/using-ai-scientists-combat-drug-resistant-infections-0525)
- [Using generative AI, researchers design compounds that kill drug-resistant bacteria — MIT News, 2025](https://news.mit.edu/2025/using-generative-ai-researchers-design-compounds-kill-drug-resistant-bacteria-0814)
- [Deep learning-guided discovery of an antibiotic (Abaucin paper, PDF)](https://people.csail.mit.edu/tommi/papers/s41589-023-01349-8.pdf)
