# Gastrulation

The gastrulation tutorials collect biological workflows that use the prepared paired
RNA and ATAC data.

- [Mouse gastrulation](mouseGastrulation.ipynb): prepare the paired data, train COATI
  and inspect one UMAP flow view.
- [Pretrained full-data models](pretrainedModels.ipynb): load the archived balanced and
  unbalanced 20k networks and compare predicted snapshots in the original saved RNA UMAP.
- [Gastrulation dynamics and mass](gastrulationDynamics.ipynb): use the current pretrained
  20k unbalanced model for E8.5 UMAP growth and flow, then decompose NMP change into
  incoming, outgoing and reweighting.
- [Held-out distribution reconstruction](heldoutDistribution.ipynb): calculate the six
  RNA/ATAC LOSO distribution scores and compare observed E8.0/E8.5 cells with balanced
  and unbalanced predictions in one shared global RNA UMAP.
- [Off-lineage leakage](offLineageLeakage.ipynb): annotate strict LOSO endpoints from
  held-out-stage neighbours and quantify source-resolved incompatible-lineage mass.
- [NMP trajectories and Caudal-epiblast composition](nmpTrajectoryComposition.ipynb):
  load current pretrained balanced and unbalanced models, inspect RNA and ATAC
  trajectories in reproducible NMP UMAPs, and quantify the changing fate composition
  of 417 observed E7.5 Caudal-epiblast cells.

```{toctree}
:hidden:

Mouse gastrulation <mouseGastrulation>
Pretrained full-data models <pretrainedModels>
Gastrulation dynamics and mass <gastrulationDynamics>
Held-out distribution reconstruction <heldoutDistribution>
Off-lineage leakage <offLineageLeakage>
NMP trajectories and Caudal-epiblast composition <nmpTrajectoryComposition>
```
