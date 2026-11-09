# Synthetic data

The Gaussian experiments reuse exactly the same committed AnnData and frozen cross-modal
map. BranchSync is a separate five-snapshot paired branching experiment generated directly
from its original seed-42 recipe.

- [Balanced Gaussian bump](balancedGaussianbump.ipynb): synchronized and primary-only
  vector fields with conserved mass.
- [Unbalanced Gaussian bump](unbalancedGaussianbump.ipynb): the same comparison with
  terminal mass set to twice the initial mass, plus red-blue instantaneous growth along
  every trajectory.
- [Cy comparison](cyComparison.ipynb): one balanced no-sync baseline and synchronized
  runs at $C_y=0.1$, $0.5$ and $0.7$, all from the same model initialization.
- [BranchSync](BranchSync.ipynb): weak branching in the primary space, an amplified split
  in the secondary space, a freshly validated time-conditioned map and the balanced
  5,000-step comparison. The RNA-only control uses density 1 and primary PDF 100;
  BranchSync uses $C_y=0.5$, density 10, primary PDF 0.1 and secondary PDF 100.

```{toctree}
:hidden:

Balanced Gaussian bump <balancedGaussianbump>
Unbalanced Gaussian bump <unbalancedGaussianbump>
Cy comparison <cyComparison>
BranchSync <BranchSync>
```
