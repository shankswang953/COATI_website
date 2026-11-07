# Installation

Use Python 3.10 or newer in a fresh environment. COATI is an independent
package: its training engine is included, and the original TraInf repositories
are not required.

## Install directly from GitHub

```bash
python -m pip install "coati-trajectory[visualization] @ git+https://github.com/shankswang953/COATI.git"
```

This installs COATI plus AnnData and UMAP support. For training only, omit
`[visualization]`; add `notebooks` to the extras if you use Jupyter. Import the
package as `coati`. The distribution name is `coati-trajectory`; it is not yet
published on PyPI.

## Editable installation and notebooks

Clone the repository to obtain the example scripts and notebook files:

```bash
git clone https://github.com/shankswang953/COATI.git
cd COATI
python -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[notebooks,visualization]'
```

On Windows activate with `.venv\Scripts\activate`. For training only, install `-e .`. AnnData and notebook support are optional extras; the core numerical dependencies install with the package. Import name: `coati`. Distribution name: `coati-trajectory`. No PyPI release is currently assumed.

## CPU and GPU

The public default is `device="cpu"`. Use `Config(device="cuda:0")` for a compatible CUDA environment, or `device="mps"` explicitly on supported Macs. `device="auto"` preserves the original CUDA/MPS/CPU selection. Only CPU has been checked in this release.

## Website source

Website source, assets and publishing tools are maintained separately in
[COATI_website](https://github.com/shankswang953/COATI_website).
See that repository for local preview instructions. They are not part of the
COATI package installation.

## Existing conda environments

Prefer the fresh environment above. Mixed conda/pip OpenMP runtimes can conflict on macOS. COATI does not set `KMP_DUPLICATE_LIB_OK`, change global tensor defaults or silently select a different solver to mask environment issues.

For the AnnData/UMAP velocity tutorial:

```bash
python -m pip install -e '.[visualization,notebooks]'
```

UMAP fitting is optional: plotting an existing embedding only needs the base
plotting dependencies and AnnData if that input type is used.
