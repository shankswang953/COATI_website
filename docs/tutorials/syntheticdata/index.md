# Synthetic data

The two experiments reuse exactly the same committed AnnData and frozen cross-modal map.
This keeps the geometry fixed while changing only whether population mass is conserved.

- [Balanced Gaussian bump](balancedGaussianbump.ipynb): synchronized and primary-only
  vector fields with conserved mass.
- [Unbalanced Gaussian bump](unbalancedGaussianbump.ipynb): the same comparison with
  terminal mass set to twice the initial mass, plus red-blue instantaneous growth along
  every trajectory.

```{toctree}
:hidden:

Balanced Gaussian bump <balancedGaussianbump>
Unbalanced Gaussian bump <unbalancedGaussianbump>
```
