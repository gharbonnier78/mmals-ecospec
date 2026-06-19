from mmals_ecospec import ContextBelief, EcoController, EcosystemState, GoalWeights, RouteCandidate
from mmals_ecospec.adapters import RC2OAdapter
from mmals_ecospec.context import ComplexityPolicy
from mmals_ecospec.memory import CompiledRoute, SyntheticMemory, ValidityEnvelope
from mmals_ecospec.routing import EnergyRouter, RouteConstraints
from mmals_ecospec.types import ComplexityMode


def routes():
    return [
        RouteCandidate("precision", 0.98, 0.65, 0.90, 0.70, 0.50, risk=0.1),
        RouteCandidate("retention", 0.88, 0.98, 0.50, 0.92, 0.60, risk=0.1),
        RouteCandidate("cheap", 0.82, 0.80, 0.10, 0.78, 0.95, risk=0.1),
    ]


def state(context=None, drift=0.1, risk=0.1):
    return EcosystemState(
        step=0,
        latent=(0.0, 1.0),
        context=context or ContextBelief({"C1": 0.9, "C2": 0.1}),
        drift=drift,
        risk=risk,
    )


def test_belief_normalization_and_topk():
    belief = ContextBelief({"a": 2.0, "b": 1.0, "c": 0.5}).normalized()
    assert abs(sum(belief.probabilities.values()) - 1.0) < 1e-12
    assert set(belief.top_k(2).probabilities) == {"a", "b"}


def test_goals_change_selected_route():
    controller = EcoController()
    constraints = RouteConstraints(min_accuracy=0.8)
    accuracy_goal = GoalWeights(0.8, 0.05, 0.05, 0.05, 0.05)
    retention_goal = GoalWeights(0.05, 0.8, 0.05, 0.05, 0.05)
    cost_goal = GoalWeights(0.05, 0.05, 0.8, 0.05, 0.05)
    assert controller.decide(state(), accuracy_goal, routes(), constraints)[0].route_id == "precision"
    assert controller.decide(state(), retention_goal, routes(), constraints)[0].route_id == "retention"
    assert controller.decide(state(), cost_goal, routes(), constraints)[0].route_id == "cheap"


def test_hard_constraint_overrides_energy():
    router = EnergyRouter()
    selected, breakdowns = router.select(
        routes(),
        GoalWeights(0.8, 0.05, 0.05, 0.05, 0.05),
        RouteConstraints(max_cost=0.6),
    )
    assert selected is not None
    assert selected.route_id != "precision"
    precision = next(b for b in breakdowns if b.route_id == "precision")
    assert not precision.admissible
    assert "cost_above_max" in precision.violations


def test_complexity_modes():
    policy = ComplexityPolicy()
    assert policy.select(state()) is ComplexityMode.FAST
    ambiguous = state(ContextBelief({"C1": 0.52, "C2": 0.48}), drift=0.2, risk=0.1)
    assert policy.select(ambiguous) in {ComplexityMode.AMBIGUOUS, ComplexityMode.CRITICAL}
    assert policy.select(state(drift=0.8)) is ComplexityMode.CRITICAL


def test_compiled_route_envelope_and_fallback():
    compiled = CompiledRoute(
        route_id="macro",
        envelope=ValidityEnvelope(max_drift=0.2, max_risk=0.2, allowed_goal_labels=frozenset({"cost"})),
        estimated_regret=0.01,
        cost_gain=0.2,
        evidence_count=20,
    )
    memory = SyntheticMemory()
    memory.store(compiled)
    assert memory.retrieve("macro", [0.0], 0.1, 0.1, "cost") is not None
    assert memory.retrieve("macro", [0.0], 0.5, 0.1, "cost") is None
    assert memory.retrieve("macro", [0.0], 0.1, 0.1, "accuracy") is None


def test_rc2o_adapter():
    adapter = RC2OAdapter()
    candidate = adapter.from_row(
        {
            "candidate": "c1",
            "accuracy": 0.9,
            "retention": 0.8,
            "cost": 0.2,
            "stability": 0.7,
            "specialization": 0.6,
        }
    )
    assert candidate.route_id == "c1"
    assert candidate.cost == 0.2
