# MIT Antibiotic-Discovery Models (Halicin, Abaucin, Generative Design)

**Type:** Deep-learning discovery models (molecule-level AI)
**Organization:** MIT — Collins Lab & Barzilay Lab, Jameel Clinic / Broad Institute
**Years:** 2020 (Halicin) → 2023 (Abaucin) → 2025 (generative design)

This is the line of work behind the "AI found a new antibiotic" headlines. It evolved
from *screening* existing molecules to *generating* brand-new ones.

> **Note on "agentic":** This line is NOT an LLM agent system — it's a supervised
> property-prediction model plus generative chemistry. But it is the actual engine that
> *finds the molecules*, so any agentic discovery system (e.g. the co-scientist or Mozi)
> would call exactly these kinds of models as tools. Worth implementing as a **tool** your
> agent can invoke.

## 1. Halicin (2020) — a screening model

- **Architecture:** A **directed message-passing neural network (D-MPNN)**, implemented in
  the open-source **Chemprop** package. Molecules are graphs (atoms = nodes, bonds = edges);
  the model learns its own continuous representation instead of fixed descriptors.
- **Training set:** ~2,500 molecules (~1,700 FDA-approved drugs + ~800 natural products),
  each labeled for whether it inhibited growth of *E. coli*.
- **Inference / screening:** Screened **>100 million molecules** from the **ZINC15** library
  in **~3 days**, ranked by predicted antibacterial activity. A *separate* ML model predicted
  human-cell toxicity to filter candidates.
- **Result:** Flagged **halicin** (originally a diabetes drug candidate), which kills bacteria
  via a novel mechanism — disrupting the membrane electrochemical gradient.

## 2. Abaucin (2023)

- Same recipe, narrower target. ~7,500 molecules were screened in the lab against
  *Acinetobacter baumannii*, used to train a D-MPNN, then predictions were run over the
  **Drug Repurposing Hub** to find structurally novel actives. Yielded **abaucin**.

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

## Implementation detail: the D-MPNN (Chemprop) you'd actually build

This is the reusable core of the 2020/2023 work. Chemprop is open source (`chemprop/chemprop`).

**Input featurization**
- *Atom features* (one-hot unless noted): atomic number, # bonds, formal charge, chirality,
  H count, hybridization, aromaticity, atomic mass (scaled ÷100).
- *Bond features:* bond type, conjugation, ring membership, stereo (cis/trans).
- *Directed edges:* initial directed-edge feature = concat(features of bond's first atom,
  undirected bond features).

**Message passing (the "directed" trick)**
- Run **T iterations** (default **3**). Each directed edge has a hidden state of size **h**
  (default **300**), initialized by a linear layer on the edge features.
- Update: each directed edge's hidden state ← function of messages from neighboring *incoming*
  directed edges, **excluding the reverse edge** (prevents messages bouncing back — the key
  difference from a vanilla MPNN; improves stability).
- Per-atom aggregation: concat(initial atom features, sum of incoming directed-edge hidden
  states) → atom embedding.

**Readout + head**
- Molecule embedding = aggregate atom embeddings (sum / scaled-sum / **mean** default).
  Optionally concatenate global molecular features (e.g. RDKit descriptors).
- Feed-forward head (default **2** layers × **300** neurons) → output. Binary activity uses
  sigmoid; multiclass uses softmax.

**Training / hyperparameters (defaults)**
- Optimizer Adam; LR warms 1e-4 → 1e-3 over 2 epochs, then exponential decay; batch size 50;
  ~30 epochs; dropout + early stopping available.
- **Ensembling** (`--ensemble_size n`) and Bayesian hyperparameter search (hidden size, depth,
  dropout, FFN layers) are built in and were used to squeeze out performance.

**How to use it as an antibiotic finder (the pipeline)**
1. Assemble a labeled assay set (compound → grows/doesn't-grow against your pathogen).
2. Train an ensemble D-MPNN classifier on it.
3. Predict over a huge enumerated library (ZINC, Drug Repurposing Hub).
4. Filter by a *separate* toxicity model + structural novelty (Tanimoto distance from training).
5. Hand the top-ranked, novel, low-tox candidates to chemists for synthesis + assay.

To go *generative* (2025): replace step 3's fixed library with CReM/F-VAE generation around
known-active fragments, then run the same predict → filter → synthesize funnel.

## Sources

- [Artificial intelligence yields new antibiotic — MIT News, 2020 (Halicin)](https://news.mit.edu/2020/artificial-intelligence-identifies-new-antibiotic-0220)
- [Using AI, scientists find a drug to combat drug-resistant infections — MIT News, 2023 (Abaucin)](https://news.mit.edu/2023/using-ai-scientists-combat-drug-resistant-infections-0525)
- [Using generative AI, researchers design compounds that kill drug-resistant bacteria — MIT News, 2025](https://news.mit.edu/2025/using-generative-ai-researchers-design-compounds-kill-drug-resistant-bacteria-0814)
- [Deep learning-guided discovery of an antibiotic (Abaucin paper, PDF)](https://people.csail.mit.edu/tommi/papers/s41589-023-01349-8.pdf)
- [Chemprop: A Machine Learning Package for Chemical Property Prediction — J. Chem. Inf. Model. (PMC)](https://pmc.ncbi.nlm.nih.gov/articles/PMC10777403/)
- [Chemprop source code (GitHub)](https://github.com/chemprop/chemprop)
