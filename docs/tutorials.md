# Tutorials

Read the examples directly in the documentation. Each tutorial includes the code,
saved results and figures, with the same navigation and theme as the rest of the site.

| Tutorial | What it covers |
| --- | --- |
| [Introduction](tutorials/00_introduction.ipynb) | Prepare AnnData or arrays, align paired inputs, choose model modes and basic parameters |
| [Original Gaussian experiment](tutorials/11_gaussian_reference.ipynb) | Original NPZ files, frozen learned T, checkpoint replay and direct training |
| [Synthetic data](tutorials/syntheticdata/index.md) | Shared AnnData and frozen map, with balanced, unbalanced and balanced $C_y$-sweep Gaussian-bump experiments |
| [Splitting and growth](tutorials/03_split.ipynb) | Branching trajectories and changing population mass |
| [Input adapters](tutorials/04_inputs.ipynb) | Arrays, dictionary, NPZ, CSV and AnnData inputs |
| [Mouse gastrulation](tutorials/10_gastrulation.ipynb) | Paired data, COATI training and one UMAP flow view |
| [Held-out biological reconstruction](tutorials/06_heldout_biological.ipynb) | Optional W2 normalization, a held-out pancreas stage, 1,000 training iterations and shared UMAP reconstruction |
| [Gastrulation dynamics and mass](tutorials/07_dynamics.ipynb) | Paired gastrulation data, a 1,000-step unbalanced model, E8.5 growth and flow with supplied cell types, and incoming/outgoing/reweighting decomposition for a chosen cell type and interval |
| [Train and inspect a cross-modal map](tutorials/08_map_quality.ipynb) | Map-only gastrulation training, held-out pairs, shared ATAC UMAP and cell-type/stage consistency |
| [scMultisim](tutorials/scMultisim/index.md) | Train T and balanced COATI |
| [Lineage gene and peak dynamics](tutorials/09_lineage_features.ipynb) | Later-start NMP cohorts, terminal lineage screening, observed gene/peak decoders, quality checks and molecular curves |

```{toctree}
:hidden:

Introduction <tutorials/00_introduction>
Original Gaussian experiment <tutorials/11_gaussian_reference>
Synthetic data <tutorials/syntheticdata/index>
Splitting and growth <tutorials/03_split>
Input adapters <tutorials/04_inputs>
Mouse gastrulation <tutorials/10_gastrulation>
Held-out biological reconstruction <tutorials/06_heldout_biological>
Gastrulation dynamics and mass <tutorials/07_dynamics>
Train and inspect a cross-modal map <tutorials/08_map_quality>
Lineage gene and peak dynamics <tutorials/09_lineage_features>
scMultisim <tutorials/scMultisim/index>
```
