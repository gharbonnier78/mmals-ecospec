# RC2O, RL, and Forward-Backward Correspondence

## RC2O as the first operational profile

RC2O already supplies the closest existing implementation boundary for EcoSpec:

| RC2O | EcoSpec |
|---|---|
| candidate trace | typed route candidate |
| metric evaluator | normalized measurement map |
| protocol verifier | hard constraints and evaluation contract |
| claim verifier | claim ledger |
| selected candidate | committed route/action |
| regime row | context belief and health state |
| post-hoc evaluation | delayed transition outcome |
| CSV/JSON artifact | reconstructive trace |

The initial selector remains:

```text
selected = admissible candidate with minimum goal-conditioned energy
```

## Contextual-bandit interpretation

When a selected candidate has no relevant effect on future candidate quality, host competence, memory, or drift, RC2O is a contextual bandit. The reward is the negative measured route energy after delayed metrics become available.

## Sequential RL extension

RL is justified when route selection changes:

- future host competence and specialization;
- retention and forgetting;
- memory availability;
- future cost or latency;
- route-graph topology;
- future uncertainty and exploration value.

The action remains the same typed route object. The only conceptual change is that the controller optimizes discounted or constrained future utility instead of one-step energy.

## Forward-backward extension

Forward-backward representations become a later profile over the same state/action interface:

- forward representation: reachable future ecosystem effects under a route;
- backward representation: embedding of desired future states, goals, or utility support;
- latent goal code: derived from the current MMALS objective;
- policy: route action aligned with the goal embedding.

This extension is not required before the sequential RL environment and delayed-outcome trace are stable.

## Goal A–E mapping

| Goal | EcoSpec field | Typical route pressure |
|---|---|---|
| A accuracy | `GoalWeights.accuracy` | predictive quality |
| B retention | `GoalWeights.retention` | old-function preservation |
| C cost | `GoalWeights.cost` | latency, compute, memory, energy |
| D stability | `GoalWeights.stability` | drift and robustness |
| E specialization | `GoalWeights.specialization` | ecosystem contribution and diversity |

## Integration steps

1. Normalize existing RC2O candidate metrics to declared `[0, 1]` scales.
2. Convert each candidate row with `RC2OAdapter`.
3. Apply protocol constraints before energy ranking.
4. Write the selected route and every rejected candidate to the reconstructive trace.
5. Ingest delayed CL outcomes as transition labels.
6. Add a bandit/RL policy only after the deterministic selector is reproducible.
