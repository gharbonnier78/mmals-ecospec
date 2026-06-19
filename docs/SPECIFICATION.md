# MMALS EcoSpec 1.0 — Engineering Contract

## Purpose

EcoSpec defines one implementable MMALS system model across continual learning, geometry, energy routing, TPUT control, RC2O, reinforcement learning, forward-backward control, dual memory, and audit.

The mandatory rule is:

> Use the simplest representation and control mechanism that preserves the information required for correct, stable, economical, and auditable action.

## Six normative axioms

1. **Systemic contribution** — evaluate every element by its effect on the complete MMALS ecosystem.
2. **Functional memory** — preserve route-conditioned function, not route identity alone.
3. **Deferred commitment** — retain a sparse set of relevant hypotheses until action requires commitment.
4. **Sufficient simplicity** — use the lowest complexity that satisfies performance, retention, stability, cost, risk, and audit constraints.
5. **Goal-conditioned control** — change goals through a declared utility interface, not through architecture rewrites.
6. **Earned complexity** — every extension must reduce to a simpler control and demonstrate incremental cost-matched value.

## Mandatory ecosystem state

```text
EcosystemState = {
  observation reference,
  latent representation,
  context belief,
  route/host/memory graph,
  reconstructive memory state,
  synthetic memory state,
  goal,
  health/drift state,
  budgets and hard constraints,
  audit and claim-ledger state
}
```

## Mandatory TPUT loop

```text
observe
  -> represent
  -> infer context belief
  -> select complexity mode
  -> propose bounded candidate routes
  -> evaluate energy and hard constraints
  -> commit or abstain
  -> execute
  -> observe delayed outcome
  -> update permitted models and health
  -> store reconstructive evidence
  -> compile/invalidate synthetic memory
  -> verify claims
```

## Complexity modes

- **Fast:** low uncertainty, low drift/risk, valid compiled route.
- **Ambiguous:** sparse multi-context or multi-route support.
- **Critical:** expanded evidence, hard constraints, full audit, safe abstention or human gate.

## Route candidate contract

Each route declares:

- context support;
- active host set and coalition structure;
- medium transformations;
- memory retrieval and update;
- predicted accuracy, retention, cost, stability, specialization, risk, auditability, and complexity;
- model/configuration versions;
- provenance and protocol identifiers.

## Goal-conditioned energy

Metrics are normalized before weighting. Accuracy, retention, stability, specialization, and auditability are higher-is-better; cost, risk, and complexity are lower-is-better. Hard constraints are evaluated before route ranking.

## Dual memory

### Reconstructive memory

Stores sufficient evidence to reproduce, explain, or contest a decision.

### Synthetic memory

Stores validated prototypes, low-rank summaries, policies, or compiled macro-routes. Every compiled route has a validity envelope and a fallback pointer to reconstructive execution.

## Required reduction paths

```text
multi-hypothesis -> top-1
RL -> one-step energy selection
forward-backward -> learned value/energy
information geometry -> Euclidean/simplex baseline
density state -> diagonal probability routing
synthetic macro-route -> reconstructive route proposal
```

## Scientific status

This specification is a design baseline. It is not evidence that the complete MMALS system outperforms established continual-learning or reinforcement-learning methods.
