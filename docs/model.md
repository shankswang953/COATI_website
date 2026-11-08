# Model formulation

This page follows the structure and notation of the paper's Methods section. RNA is the primary state space $\mathcal X$ and ATAC is the secondary state space $\mathcal Y$. The code can also use other primary and secondary embeddings.

## Problem setup and notation

Let $\rho_t$ and $\xi_t$ be the time-dependent population densities in $\mathcal X$ and $\mathcal Y$. Their velocity fields are $u_t$ and $v_t$, and their growth fields are $g_t$ and $h_t$. A continuously differentiable map

```{math}
\mathbf{T}:\mathcal X\times[0,1]\rightarrow\mathcal Y
```

synchronizes the two modalities. Unbalanced synchronized optimal transport is formulated as

```{math}
\begin{aligned}
\inf_{(\rho,u,g)}\;&\frac12\int_0^1\left[
c_x\int_{\mathcal X}(\alpha\lVert u_t\rVert^2+\beta g_t^2)\rho_t\,dx
+c_y\int_{\mathcal Y}(\alpha\lVert v_t\rVert^2+\beta h_t^2)\xi_t\,dy
\right]dt,\\
\text{subject to }\;&
\partial_t\rho_t+\alpha\nabla_x\!\cdot(\rho_tu_t)=\beta\rho_tg_t,\\
&\partial_t\xi_t+\alpha\nabla_y\!\cdot(\xi_tv_t)=\beta\xi_th_t,\\
&\xi_t=(\mathbf T_t)_\#\rho_t,\qquad h_t(\mathbf T_t(x))=g_t(x),\\
&v_t(\mathbf T_t(x))=D_x\mathbf T_t(x)u_t(x)
+\alpha^{-1}\partial_t\mathbf T_t(x),\\
&c_x,c_y\geq0,\qquad c_x+c_y=1.
\end{aligned}
```

The pushforward constraint maps the RNA population to the ATAC population. Corresponding RNA and ATAC trajectories carry the same mass. Balanced COATI is obtained by setting $\beta=0$ and omitting the growth and mass-matching terms.

**Code parameters.** `multimodal=True` enables the secondary space and all cross-modal losses. `balanced=True` fixes particle masses; `balanced=False` enables the growth field and mass matching. In saved engine configurations these choices are recorded as `sync_loss` and `unbalancedModel`, respectively.

## Synchronized transport objective

COATI parameterizes only the primary dynamics. For a primary trajectory $X_t(a)$, the mapped trajectory is

```{math}
Y_t(a)=\mathbf T_t(X_t(a)).
```

Writing $J_t=D_x\mathbf T_t$ and $b_t=\partial_t\mathbf T_t$, the induced secondary velocity is

```{math}
\dot Y_t(a)=\alpha J_t(X_t(a))u_t(X_t(a))+b_t(X_t(a)).
```

The joint action can therefore be evaluated in the primary space:

```{math}
\mathcal A=\int_0^1\int_{\mathcal X}
\left[
\frac{\alpha c_x}{2}\lVert u_t(x)\rVert^2
+\frac{c_y}{2\alpha}\lVert\alpha J_t(x)u_t(x)+b_t(x)\rVert^2
+\frac{\beta}{2}g_t(x)^2
\right]d\rho_t(x)\,dt.
```

This is why the secondary modality can constrain the primary neural ODE without separately parameterizing $v_t$ or $h_t$.

**Code parameters.** `secondary_weight` is $c_y$ and the implementation derives $c_x=1-c_y$. Its saved engine name is `sync_weight`. `energy_weight` (`energy_coefficient` in saved configurations) is the common kinetic-energy multiplier. Setting `secondary_weight=0` removes the secondary energy and manifold contributions, but it does not disable secondary reference matching; use `multimodal=False` for RNA-only training.

## Vector-field representation of COATI

COATI uses neural networks $u_\theta$ and $g_\theta$. It samples $B$ initial particles from $p_0=\widehat\rho_0/m_0$ and integrates

```{math}
\begin{aligned}
\frac{dX_i(t)}{dt}&=\alpha u_\theta(X_i(t),t),\\
\frac{d\log w_i(t)}{dt}&=\beta g_\theta(X_i(t),t),\\
X_i(0)&\sim p_0,\qquad w_i(0)=1/B,\\
Y_i(t)&=\mathbf T_\vartheta(X_i(t),t).
\end{aligned}
```

$X_i(t)$ is the primary state and $w_i(t)$ is its mass. The mapped particle $Y_i(t)$ retains the same mass. In balanced mode, all particles keep uniform mass.

**Code parameters.** `batch_size` ($B$; saved as `num_samples`) controls the number of particles sampled per snapshot. `dt` controls the integration step. `growth_weight` ($\beta$; saved as `alpha_growth`) controls the growth dynamics and growth-action scale in unbalanced training. `hidden_dim` and `n_layers` set the capacity of the neural vector field.

## Training loss

Let $t_0<\cdots<t_K$ be the observed times. COATI evaluates the following losses on each interval $[t_k,t_{k+1}]$.

### Primary kinetic energy

```{math}
\frac{dE_i^x(t)}{dt}
=\frac{\alpha}{2}\lVert u_\theta(X_i(t),t)\rVert^2w_i(t),
\qquad
\mathcal L_{\mathrm{energy}}^x(k)=\sum_{i=1}^B E_i^x(t_{k+1}).
```

**Code parameters.** `energy_weight` ($\lambda_E$; saved as `energy_coefficient`) multiplies this term. The implementation uses $\alpha=1$.

### Shared growth penalty

```{math}
\frac{dE_i^g(t)}{dt}=g_\theta(X_i(t),t)^2w_i(t),
\qquad
\mathcal L_{\mathrm{growth}}(k)=\sum_{i=1}^B E_i^g(t_{k+1}).
```

The growth penalty is shared because corresponding particles have the same relative growth rate in both modalities.

**Code parameters.** `growth_weight` (`alpha_growth`) sets the growth scale $\beta$. The current engine does not expose a separate public $\lambda_G$: `energy_weight` also multiplies the accumulated growth-energy term.

### Kinetic energy in the secondary space

On an integration grid $t_k=s_0<\cdots<s_L=t_{k+1}$, define $Y_i^\ell=\mathbf T_\vartheta(X_i(s_\ell),s_\ell)$. The discrete secondary energy is

```{math}
\mathcal L_{\mathrm{energy}}^y(k)
=\sum_{i=1}^B\sum_{\ell=0}^{L-1}
w_i^\ell
\frac{\lVert Y_i^{\ell+1}-Y_i^\ell\rVert^2}
{2(s_{\ell+1}-s_\ell)}.
```

For balanced COATI, $w_i^\ell=1/B$. For unbalanced COATI, the implementation uses the left-endpoint particle mass on each solver interval.

**Code parameters.** This term uses the same `energy_weight` as primary kinetic energy and is additionally multiplied by `secondary_weight`. The temporal grid is controlled by `dt`.

### Reference matching

Predicted and observed distributions are compared at the end of each interval using the debiased Sinkhorn divergence $S_\varepsilon$. With normalized predicted weights $\bar w_i(t)=w_i(t)/\sum_qw_q(t)$,

```{math}
\begin{aligned}
\mathcal L_{\mathrm{reference}}^x(k)
&=S_\varepsilon\!\left(
\{(X_i(t_{k+1}),\bar w_i(t_{k+1}))\}_{i=1}^B,
\{(x_j^{k+1},1/n_x)\}_{j=1}^{n_x}
\right),\\
\mathcal L_{\mathrm{reference}}^y(k)
&=S_\varepsilon\!\left(
\{(Y_i(t_{k+1}),\bar w_i(t_{k+1}))\}_{i=1}^B,
\{(y_j^{k+1},1/n_y)\}_{j=1}^{n_y}
\right).
\end{aligned}
```

**Code parameters.** `matching_weight` is the shared fixed $\lambda_x=\lambda_y$ and is saved as `pdf_coefficient`. Advanced configurations can instead provide `pdf_coefficient_pri` and `pdf_coefficient_sec` for separate modality-specific weights. Reference matching stays active in the secondary space whenever `multimodal=True`.

### Unbalanced mass matching

Let $r_{k+1}=L_{k+1}/L_0$ be the target total mass relative to the first stage. Each observed primary cell is assigned to its nearest predicted particle,

```{math}
\pi(j)=\operatorname*{arg\,min}_{1\leq i\leq B}
\lVert x_j^{k+1}-X_i(t_{k+1})\rVert^2,
```

which defines the target particle mass

```{math}
\widehat m_i^{k+1}
=r_{k+1}\frac1{n_x}\sum_{j=1}^{n_x}\mathbf 1\{\pi(j)=i\}.
```

The mass loss is

```{math}
\mathcal L_{\mathrm{mass}}(k)
=\sum_{i=1}^B\left(w_i(t_{k+1})-\widehat m_i^{k+1}\right)^2.
```

**Code parameters.** `mass_weight` is $\lambda_M$ and is saved as `mass_coefficient`. An explicit population-size prior can be supplied with `extra={"biological_num": [...]}`. Otherwise, the current engine uses observed snapshot counts relative to the first snapshot.

### Manifold constraint

For endpoint reference sets $\mathcal S_k^x=\mathcal B_k^x\cup\mathcal B_{k+1}^x$ and $\mathcal S_k^y=\mathcal B_k^y\cup\mathcal B_{k+1}^y$, let $d_{K_{\mathrm{nn}}}(z,\mathcal S)$ be the mean distance to the $K_{\mathrm{nn}}$ nearest reference cells. Then

```{math}
\begin{aligned}
\mathcal L_{\mathrm{manifold}}^x(k)
&=\frac1{B(L+1)}\sum_{i=1}^B\sum_{\ell=0}^{L}
\left[d_{K_{\mathrm{nn}}}(X_i(s_\ell),\mathcal S_k^x)-\delta\right]_+,\\
\mathcal L_{\mathrm{manifold}}^y(k)
&=\frac1{B(L+1)}\sum_{i=1}^B\sum_{\ell=0}^{L}
\left[d_{K_{\mathrm{nn}}}(Y_i^\ell,\mathcal S_k^y)-\delta\right]_+.
\end{aligned}
```

**Code parameters.** `manifold_weight` is $\lambda_D$ and is saved as `density_coefficient`. `extra={"density_topk": K}` sets $K_{\mathrm{nn}}$, and `extra={"density_hinge": delta}` sets the hinge threshold $\delta$. Both primary and secondary manifold penalties use this weight; the secondary term is also multiplied by `secondary_weight`.

### Total interval loss

```{math}
\begin{aligned}
\mathcal L_k={}&c_x\left[
\lambda_E\mathcal L_{\mathrm{energy}}^x(k)
+\lambda_D\mathcal L_{\mathrm{manifold}}^x(k)
\right]
+c_y\left[
\lambda_E\mathcal L_{\mathrm{energy}}^y(k)
+\lambda_D\mathcal L_{\mathrm{manifold}}^y(k)
\right]\\
&+\lambda_x\mathcal L_{\mathrm{reference}}^x(k)
+\lambda_y\mathcal L_{\mathrm{reference}}^y(k)
+\lambda_G\mathcal L_{\mathrm{growth}}(k)
+\lambda_M\mathcal L_{\mathrm{mass}}(k).
\end{aligned}
```

The implementation uses $\alpha=1$. The modality weight $c_y$ multiplies secondary kinetic energy and the secondary manifold penalty, but not secondary reference matching. Therefore, $c_y=0$ is not the RNA-only model: RNA-only training disables the secondary losses entirely.

**Code parameters.** At the complete-objective level, the main public controls are `energy_weight`, `manifold_weight`, `matching_weight`, `mass_weight`, `growth_weight` and `secondary_weight`. `multimodal` decides whether the secondary terms exist, while `balanced` decides whether growth and mass matching exist.

## Adaptive marginal matching weight

The exact marginal constraints are relaxed to

```{math}
\mathcal L_{\mathrm{reference}}^b(k;\theta)\leq\tau_{k+1}^b,
\qquad b\in\{x,y\},
```

where $\tau_k^b$ is a finite-sampling tolerance estimated from pairs of mini-batches drawn from the same observed snapshot:

```{math}
\tau_k^b=\frac1Q\sum_{q=1}^Q
S_\varepsilon(A_{k,q}^{b,1},A_{k,q}^{b,2}).
```

Each modality has one matching weight shared across intervals. With

```{math}
\Delta^b=\max_{0\leq k<K}
\left(\overline S_k^b-\tau_{k+1}^b\right),
```

the update is

```{math}
\lambda_b\leftarrow
\operatorname{clip}\left(
\lambda_b+\eta_\lambda\Delta^b,
\lambda_{\min}^b,
\lambda_{\max}^b
\right).
```

**Code parameters.** Enable this update with `extra={"adaptive_lambda": True}`. The step sizes are `eta_lambda_pri` and `eta_lambda_sec`; the bounds are `lambda_min_pri`, `lambda_max_pri`, `lambda_min_sec` and `lambda_max_sec`. These are advanced engine fields passed through `extra`.

## Sinkhorn scale preprocessing

For modality $b$ at time $t_k$, COATI estimates the median pairwise distance

```{math}
c_k^b=\operatorname{median}_{i<j}
\lVert\widetilde z_{k,i}^b-\widetilde z_{k,j}^b\rVert_2
```

and sets the Sinkhorn regularization scale to

```{math}
\varepsilon_k^b=c_\varepsilon c_k^b.
```

The paper uses $c_\varepsilon=0.05$. The scale is estimated separately for each modality and observed stage and held fixed during training.

**Code parameters.** `extra={"blur_coeff": 0.05}` sets $c_\varepsilon$. The engine name is also `blur_coeff`; the resulting stage- and modality-specific Sinkhorn scales are derived quantities rather than user-specified constants.

## Data normalization

The reduced embeddings are divided by stored modality-specific scales. For modality $b$,

```{math}
s_b=\left(
\sum_{k=0}^{K-1}
\frac{W_2^2(Z_k^b,Z_{k+1}^b)}{t_{k+1}-t_k}
\right)^{1/2},
\qquad
\widetilde Z_k^b=Z_k^b/s_b.
```

With exact $W_2$ distances, the normalized snapshots satisfy

```{math}
\sum_{k=0}^{K-1}
\frac{W_2^2(\widetilde Z_k^b,\widetilde Z_{k+1}^b)}{t_{k+1}-t_k}=1.
```

Normalization parameters are explicit inputs to training; COATI does not silently recompute them.

**Code parameters.** `primal_norm_path` and `sec_norm_path` point to the stored primary and secondary scale dictionaries. They are required when the corresponding data are supplied in the original, unnormalized feature coordinates.

## Cross-modality map

The map is trained before trajectory learning and then frozen. Secondary losses are differentiated through the frozen map with respect to predicted primary states, so they still update the trajectory network.

For the time-conditioned FiLM map, a time encoder produces $\gamma_\ell(t)$ and $\beta_\ell(t)$ for each hidden layer:

```{math}
H_{\ell+1}=\phi\!\left(
(1+\gamma_\ell(t))\odot(W_\ell H_\ell+b_\ell)+\beta_\ell(t)
\right),
```

where $\phi$ is GELU. The paired map-training objective is

```{math}
\mathcal L_{\mathrm{MSE}}
=\frac1N\sum_{i=1}^N
\lVert\mathbf T_\vartheta(q_i,t_i)-a_i\rVert_2^2.
```

COATI can train FiLM or a time-independent MLP internally, use a kernel map, or accept a pretrained PyTorch module through `T_model`.

**Code parameters.** `T_model` supplies an already trained map. `map_type` selects a built-in map, while `MapConfig(...)` controls its width, depth, time encoder, epochs and optimizer. The trained map is frozen during trajectory learning, although gradients through its input still update the trajectory network.

## Paper symbols and code parameters

The public aliases are intended for notebooks and user-facing scripts. Saved configurations retain the engine names for reproducibility.

| Paper symbol or choice | Public API | Saved/engine name | Meaning |
| --- | --- | --- | --- |
| paired or single modality | `multimodal` | `sync_loss` | Enables all secondary-space losses |
| balanced or unbalanced | `balanced` | inverse of `unbalancedModel` | Enables or disables learned particle mass |
| $c_y$ | `secondary_weight` | `sync_weight` | Secondary kinetic-energy and manifold weight |
| $c_x=1-c_y$ | derived | derived | Primary kinetic-energy and manifold weight |
| $\lambda_E$ | `energy_weight` | `energy_coefficient` | Multiplies kinetic energy; also multiplies the accumulated growth-energy term in the current engine |
| $\lambda_D$ | `manifold_weight` | `density_coefficient` | Multiplies primary and secondary manifold penalties |
| $\lambda_x,\lambda_y$ | `matching_weight` | `pdf_coefficient` | Shared fixed Sinkhorn weight |
| separate $\lambda_x,\lambda_y$ | `extra={...}` | `pdf_coefficient_pri`, `pdf_coefficient_sec` | Optional modality-specific fixed weights |
| $\lambda_M$ | `mass_weight` | `mass_coefficient` | Multiplies the unbalanced mass-matching loss |
| $\beta$ | `growth_weight` | `alpha_growth` | Growth dynamics and growth-action scale |
| $B$ | `batch_size` | `num_samples` | Particles sampled per snapshot |
| $s_{\ell+1}-s_\ell$ | `dt` | `dt` | Training integration step |
| $K_{\mathrm{nn}}$ | `extra={"density_topk": ...}` | `density_topk` | Neighbours used by the manifold penalty |
| $\delta$ | `extra={"density_hinge": ...}` | `density_hinge` | Manifold hinge threshold |
| $c_\varepsilon$ | `extra={"blur_coeff": ...}` | `blur_coeff` | Median-distance multiplier for Sinkhorn regularization |
| adaptive $\lambda_b$ | `extra={"adaptive_lambda": True}` | `adaptive_lambda` | Enables dual-ascent matching weights |
| $\eta_\lambda$ | `extra={...}` | `eta_lambda_pri`, `eta_lambda_sec` | Per-modality dual update step |
| $\lambda_{\min}^b,\lambda_{\max}^b$ | `extra={...}` | `lambda_min_pri/sec`, `lambda_max_pri/sec` | Dual-weight bounds |
| $\mathbf T_\vartheta$ | `T_model` or `map_type` | `T_model`, `map_type` | Frozen external map or built-in map choice |
| map architecture | `MapConfig(...)` | map-training fields | Width, depth, time encoder, epochs and optimizer settings |
| normalization $s_x,s_y$ | `primal_norm_path`, `sec_norm_path` | stored `scale` dictionaries | Fixed primary and secondary scales |
| $L_k$ | `extra={"biological_num": [...]}` | `biological_num` | Optional external population-size prior |

`iterations`, `learning_rate`, `hidden_dim` and `n_layers` control optimization and neural-field capacity but do not correspond to symbols in the continuous formulation.

```python
config = ct.Config(
    multimodal=True,
    balanced=False,
    secondary_weight=0.1,
    energy_weight=1.0,
    manifold_weight=10.0,
    matching_weight=100.0,
    growth_weight=1.0,
    mass_weight=1.0,
    extra={
        "adaptive_lambda": True,
        "blur_coeff": 0.05,
        "biological_num": [1.0, 4.0, 6.0, 11.0],
    },
)
```

When `biological_num` is omitted, the current engine uses each observed snapshot count relative to the first snapshot as the mass target. Use an explicit list when observed sampling depth should not be interpreted as biological population size.

See [Configuration and extension](configuration.md) for defaults and [Cross-modal maps](maps.md) for map training and externally supplied maps.
