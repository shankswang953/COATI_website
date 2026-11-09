# Gastrulation

The gastrulation tutorials collect biological workflows that use the prepared paired
RNA and ATAC data.

- [Mouse gastrulation](mouseGastrulation.ipynb): prepare the paired data, train COATI
  and inspect one UMAP flow view.
- [Pretrained full-data models](pretrainedModels.ipynb): load the archived balanced and
  unbalanced 20k networks and compare predicted snapshots in the original saved RNA UMAP.
- [Held-out distribution reconstruction](heldoutDistribution.ipynb): calculate the six
  RNA/ATAC LOSO distribution scores and compare observed E8.0/E8.5 cells with balanced
  and unbalanced predictions in one shared global RNA UMAP.

```{toctree}
:hidden:

Mouse gastrulation <mouseGastrulation>
Pretrained full-data models <pretrainedModels>
Held-out distribution reconstruction <heldoutDistribution>
```
