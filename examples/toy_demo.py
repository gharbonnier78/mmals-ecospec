from __future__ import annotations

from mmals_ecospec import ContextBelief, EcoController, EcosystemState, GoalWeights, RouteCandidate
from mmals_ecospec.audit import write_trace
from mmals_ecospec.routing import RouteConstraints


def candidate_routes() -> list[RouteCandidate]:
    return [
        RouteCandidate(
            route_id="H1_precision",
            accuracy=0.97,
            retention=0.68,
            cost=0.82,
            stability=0.72,
            specialization=0.55,
            risk=0.12,
            auditability=0.90,
            complexity=0.65,
            hosts=("H1",),
        ),
        RouteCandidate(
            route_id="H2_retention",
            accuracy=0.82,
            retention=0.97,
            cost=0.55,
            stability=0.91,
            specialization=0.62,
            risk=0.08,
            auditability=0.96,
            complexity=0.45,
            hosts=("H2",),
        ),
        RouteCandidate(
            route_id="H3_compiled_specialist",
            accuracy=0.79,
            retention=0.81,
            cost=0.14,
            stability=0.80,
            specialization=0.96,
            risk=0.10,
            auditability=0.78,
            complexity=0.18,
            hosts=("H3",),
        ),
    ]


def main() -> None:
    state = EcosystemState(
        step=1,
        latent=(0.2, -0.1, 0.8),
        context=ContextBelief({"C1": 0.48, "C2": 0.44, "C3": 0.08}),
        drift=0.24,
        risk=0.12,
    )
    goals = {
        "A_accuracy": GoalWeights(accuracy=0.70, retention=0.10, cost=0.05, stability=0.10, specialization=0.05),
        "B_retention": GoalWeights(accuracy=0.10, retention=0.70, cost=0.05, stability=0.10, specialization=0.05),
        "C_low_cost": GoalWeights(accuracy=0.10, retention=0.05, cost=0.70, stability=0.10, specialization=0.05),
        "E_specialization": GoalWeights(accuracy=0.10, retention=0.10, cost=0.05, stability=0.10, specialization=0.65),
    }
    constraints = RouteConstraints(min_accuracy=0.78, min_auditability=0.70, max_risk=0.25)
    controller = EcoController()

    print("MMALS EcoSpec 1.0 toy goal-switching demo")
    print("Context belief:", state.context.normalized().probabilities)
    for label, goal in goals.items():
        selected, trace = controller.decide(state, goal, candidate_routes(), constraints)
        print(f"{label:18s} -> {selected.route_id if selected else 'ABSTAIN'} ({trace.complexity_mode.value})")
        write_trace(trace, f"artifacts/{label}_trace.json")


if __name__ == "__main__":
    main()
