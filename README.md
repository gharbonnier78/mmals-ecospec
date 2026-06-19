# MMALS EcoSpec 1.0

**Minimal Systemic Specification for Goal-Conditioned, Memory-Preserving Adaptive Learning**

This GitHub-ready package turns the MMALS TPUT design into an implementable contract. It unifies the existing continual-learning backbone with inferred context, latent geometry, energy-based routing, goal-conditioned control, reconstructive and synthetic memory, ecosystem-level contribution analysis, RC2O candidate traces, RL meta-routing, forward-backward control, and optional density-state research extensions.

> Use the simplest representation and control mechanism that preserves the information required for correct, stable, economical, and auditable action.

<p align="center">
  <a href="./paper/main.pdf">
    <img src="https://img.shields.io/badge/Open-Article-0B5FFF?style=for-the-badge&logo=adobeacrobatreader&logoColor=white" alt="Open PDF">
  </a>
</p>

## Deliverables

- `paper/main.tex` — full arXiv-style conceptual and mathematical specification.
- `paper/main.pdf` — compiled 20-page article.
- `paper/references.bib` — reusable BibTeX database; the paper also contains a self-contained bibliography for reliable compilation.
- `docs/SPECIFICATION.md` — concise normative engineering contract.
- `docs/RC2O_MAPPING.md` — RC2O, contextual-bandit, RL, and forward-backward correspondence.
- `docs/IMPLEMENTATION_ROADMAP.md` — staged implementation and falsification programme.
- `docs/TRACE_SCHEMA.json` — machine-readable decision-trace schema.
- `docs/CLAIM_LEDGER.md` — claim gates and current scientific status.
- `src/mmals_ecospec/` — executable reference data classes, context/mode logic, energy router, dual-memory skeleton, audit writer, RC2O adapter, RL/FB interfaces.
- `examples/toy_demo.py` — goal-switching and trace-generation demo.
- `tests/` — contract tests.
- `configs/default.yaml` — conservative feature flags.
- `notebooks/MMALS_EcoSpec_1_0_Smoke.ipynb` — notebook wrapper.

## Status

- **Specification:** v1.0 complete.
- **Reference code:** executable contract/smoke implementation, not a production training backbone.
- **Scientific status:** design specification, not evidence that the complete architecture outperforms established continual-learning or reinforcement-learning methods.
- **Compatibility:** designed as an adapter around current RC1b/v1.x/RC2O work, not a destructive rewrite.

## Quick start

```bash
python -m pip install -e .[dev]
pytest
python examples/toy_demo.py
```

Validate a generated trace:

```bash
python - <<'PY'
import json
from jsonschema import validate
schema = json.load(open('docs/TRACE_SCHEMA.json'))
trace = json.load(open('artifacts/A_accuracy_trace.json'))
validate(trace, schema)
print('trace valid')
PY
```

Compile the paper:

```bash
cd paper
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

The paper is self-contained and does not require BibTeX at compile time. `references.bib` is included for reuse in future arXiv versions.

## Architecture

```text
observation
  -> latent representation
  -> context belief
  -> adaptive complexity mode
  -> bounded route candidates
  -> goal-conditioned energy + hard constraints
  -> route / abstention
  -> execution and delayed outcome
  -> continual update
  -> reconstructive audit
  -> synthetic compilation with validity envelope and fallback
```

## Relationship to current branches

- **RC2O:** one-step transparent candidate selector and evidence backbone.
- **TPUT:** operational state-transition and control loop formalized by EcoSpec.
- **Geometry-MMALS:** diagnostics over context-route-host-memory-system state.
- **RL meta-router:** sequential extension when route choice changes future ecosystem state.
- **Forward-backward control:** later reusable-futures profile over the same typed state/action interface.
- **Quantum-inspired state:** optional ablation; diagonal probability routing is the mandatory baseline.

## License

Apache-2.0 for original code and documentation. Third-party dependencies, papers, and datasets retain their own licenses.
