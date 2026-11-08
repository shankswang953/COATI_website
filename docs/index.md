# COATI

```{raw} html
<video controls playsinline preload="metadata" poster="_static/coati-intro-poster.png" style="width:100%;height:auto;border-radius:8px;background:#FAFBFD" aria-label="COATI animated introduction: from paired snapshots to coupled trajectories">
  <source src="_static/coati-intro.mp4" type="video/mp4">
  <p>Your browser does not support embedded video.</p>
</video>
```

COATI (Cross-Omics Aligned Trajectory Inference) reconstructs continuous developmental trajectories from time-indexed cell-state snapshots. A neural ODE evolves cells in a primary space such as RNA PCA, while a fixed cross-modal map projects the same trajectories into a secondary space such as ATAC LSI.

Observed distributions in both modalities constrain the learned flow. Balanced COATI conserves particle mass; unbalanced COATI additionally learns population growth or depletion. The model keeps the modalities in their own feature spaces instead of merging them into one embedding.

[Read the Model formulation and Parameters](model.md)

```python
import coati as ct

data = ct.TemporalData.from_npz("primary.npz", keys=["t0", "t1"], times=[0., 1.])
result = ct.train_vector_field(data, multimodal=False, balanced=True)
result.plot_trajectory()
```

For a self-contained CPU example, clone COATI and run [examples/run_toy.py](https://github.com/shankswang953/COATI/blob/main/examples/run_toy.py). Synthetic-data preparation is maintained in the repository examples, outside the installed package. The API above reads your prepared embeddings. Validation includes synthetic workflows and a short biological temporal-holdout tutorial; it does not establish biological superiority.

```{toctree}
:maxdepth: 2
:caption: Get started

installation
quickstart
inputs
tutorials
```

```{toctree}
:maxdepth: 2
:caption: Understand and extend

configuration
model
velocity
maps
downstream
api
validation
```
