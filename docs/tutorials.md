# Tutorials

Read the examples directly in the documentation. Each tutorial includes the code,
saved results and figures, with the same navigation and theme as the rest of the site.

| Tutorial | What it covers |
| --- | --- |
| [Introduction](tutorials/00_introduction.ipynb) | Prepare AnnData or arrays, align paired inputs, choose model modes and basic parameters |
| [Synthetic data](tutorials/syntheticdata/index.md) | Gaussian-bump comparisons and BranchSync on five paired branching snapshots |
| [Gastrulation](tutorials/gastrulation/index.md) | Train paired models, load pretrained 20k networks, inspect NMP trajectories and composition, and evaluate E8.0/E8.5 LOSO reconstruction |
| [Palate](tutorials/palate/index.md) | Evaluate balanced and unbalanced strict LOSO reconstruction at E13.5 and E14.0 in RNA and ATAC |
| [Gastrulation dynamics and mass](tutorials/gastrulation/gastrulationDynamics.ipynb) | Current pretrained 20k unbalanced model, E8.5 UMAP growth and flow, and NMP incoming/outgoing/reweighting decomposition |
| [Off-lineage leakage](tutorials/gastrulation/offLineageLeakage.ipynb) | Source-resolved incompatible-lineage mass from strict E8.0/E8.5 LOSO predictions using held-out-stage 5-NN annotations |
| [NMP trajectories and composition](tutorials/gastrulation/nmpTrajectoryComposition.ipynb) | Pretrained balanced and unbalanced RNA/ATAC trajectories, followed by mass-aware Caudal-epiblast fate composition |
| [scMultisim](tutorials/scMultisim/index.md) | Train T and balanced COATI |
| [Lineage gene and peak dynamics](tutorials/09_lineage_features.ipynb) | Later-start NMP cohorts, terminal lineage screening, observed gene/peak decoders, quality checks and molecular curves |

```{toctree}
:hidden:

Introduction <tutorials/00_introduction>
Synthetic data <tutorials/syntheticdata/index>
Gastrulation <tutorials/gastrulation/index>
Palate <tutorials/palate/index>
Lineage gene and peak dynamics <tutorials/09_lineage_features>
scMultisim <tutorials/scMultisim/index>
```
