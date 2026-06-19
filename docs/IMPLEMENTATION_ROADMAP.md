# Implementation and Falsification Roadmap

## Phase 0 — Release contract

- Compile the paper.
- Install the Python package.
- Pass unit tests.
- Validate a generated trace against `TRACE_SCHEMA.json`.
- Demonstrate goal switching and safe abstention.

**Exit:** claim C0 only.

## Phase 1 — Frozen-backbone EcoSpec

Use a common frozen feature extractor and common host bank.

- infer a context belief;
- construct route candidates;
- switch goals A–E;
- show route changes;
- verify each change improves the intended normalized objective;
- test fast, ambiguous, and critical modes;
- compile and invalidate a synthetic macro-route.

**Exit:** claim C2 if successful.

## Phase 2 — RC2O eight-dataset offline selector

Compare:

1. fixed weighted score;
2. linear goal-conditioned energy;
3. nonlinear energy model;
4. contextual bandit;
5. future-outcome oracle.

Report admissible regret, route switching, calibration, cost, and audit completeness.

## Phase 3 — RC2O continual-learning integration

Harden baselines:

- fine-tuning;
- EWC sweep;
- SI sweep;
- LwF temperature/lambda sweep;
- replay memory-size sweep;
- PNN sanity check;
- sparse-MoE sanity check;
- joint upper bound.

Report accuracy, forgetting, minimum-task accuracy, backward transfer, memory, compute, latency, parameter count, and variance over seeds.

## Phase 4 — Sequential meta-routing

Construct a controlled environment where selecting a host changes future competence or retention.

Compare deterministic energy, bandit, RL, and model-predictive control.

**RL is rejected** if it does not improve long-horizon utility over one-step selection under matched candidate sets and constraints.

## Phase 5 — Forward-backward control

Test rapid goal switching without per-goal retraining. Compare against ordinary goal-conditioned value networks and successor-feature baselines.

## Phase 6 — Advanced geometry

Ablate in this order:

1. Euclidean/simplex baseline;
2. information-geometric distance;
3. covariance or Gram state;
4. real low-rank PSD state;
5. complex-amplitude state.

Stop when added complexity ceases to produce cost-matched value.

## Claim ladder

- **C0:** executable specification.
- **C1:** functional memory mechanism.
- **C2:** goal-responsive control.
- **C3:** sequential-control advantage.
- **C4:** geometry adds measurable value.
- **C5:** density-state representation adds measurable value.
- **C6:** general MMALS advantage across hardened benchmarks and external replication.
