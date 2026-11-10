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

For a short biological example, clone COATI and run [examples/gastrulation/train_balanced.py](https://github.com/shankswang953/COATI/blob/main/examples/gastrulation/train_balanced.py). Dataset-specific preparation is maintained in the repository examples, outside the installed package. The API above reads your prepared embeddings. Validation includes synthetic workflows and biological temporal-holdout tutorials; it does not establish biological superiority.

## Basic workflow

COATI uses time-indexed primary embeddings, such as RNA PCA, and can optionally
synchronize them with paired secondary embeddings, such as ATAC LSI. A typical
analysis prepares the embeddings and time labels, trains or loads the cross-modal
map, fits the vector field, and then performs trajectory inference and downstream
analysis. Reusable downstream tools are available under `coati.downstream`.

Install the package and run a short end-to-end example:

```bash
git clone https://github.com/shankswang953/COATI.git
cd COATI
python -m pip install -e '.[notebooks,visualization]'
python -m examples.gastrulation.train_balanced \
  --iterations 200 \
  --output outputs/gastrulation-balanced-smoke
```

For a guided biological workflow:

```bash
python -m jupyter lab notebooks/00_introduction.ipynb
```

## References

1. Wang, J., Zhao, Y., Nie, Q. and Cang, Z. [Synchronized Optimal Transport Reconstructs Coupled Transcriptomic and Chromatin Dynamics](https://arxiv.org/abs/2611.08853). arXiv:2611.08853, 2026.
2. Cang, Z., Wang, J., Wei, X. and Zhao, Y. [Synchronization of Unbalanced Dynamical Optimal Transport across Multiple Spaces](https://arxiv.org/abs/2602.18725). arXiv:2602.18725, 2026.
3. Cang, Z. and Zhao, Y. [Synchronized Optimal Transport for Joint Modeling of Dynamics Across Multiple Spaces](https://doi.org/10.1137/24M1667555). *SIAM Journal on Applied Mathematics* 85(1), 341–365, 2025.

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
maps
downstream
api
```
