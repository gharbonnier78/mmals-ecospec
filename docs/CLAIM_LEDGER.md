# Claim Ledger Starter

| Claim ID | Claim | Required evidence | Current status |
|---|---|---|---|
| C0 | EcoSpec is executable and auditable | package tests, smoke trace, schema validation | supported by this release |
| C1 | Functional state is a better memory object than route identity | route-only vs latent/output functional ablation | prior internal evidence; revalidate in current backbone |
| C2 | Goal changes produce useful route changes | goals A–E, fixed candidates, target-metric improvement | not yet established by this specification |
| C3 | Sequential RL improves ecosystem utility | delayed-effect environment and matched one-step control | open |
| C4 | Geometry improves diagnosis or control | Euclidean/simplex controls and held-out intervention tests | open |
| C5 | Density-state memory adds value | diagonal/covariance/PSD/complex ablation under equal cost | open |
| C6 | MMALS broadly outperforms established methods | hardened baselines, multiple benchmarks, independent replication | blocked |

A claim verifier should return one of:

- `supported`;
- `provisional`;
- `blocked`;
- `contradicted`;
- `not_tested`.
