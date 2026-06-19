from __future__ import annotations

from dataclasses import dataclass, field
from uuid import uuid4

from .context import ComplexityPolicy
from .memory import ReconstructiveMemory
from .routing import EnergyRouter, RouteConstraints
from .types import EcosystemState, GoalWeights, RouteCandidate, TraceRecord


@dataclass
class EcoController:
    router: EnergyRouter = field(default_factory=EnergyRouter)
    complexity_policy: ComplexityPolicy = field(default_factory=ComplexityPolicy)
    reconstructive_memory: ReconstructiveMemory = field(default_factory=ReconstructiveMemory)

    def decide(
        self,
        state: EcosystemState,
        goal: GoalWeights,
        routes: list[RouteCandidate],
        constraints: RouteConstraints | None = None,
    ) -> tuple[RouteCandidate | None, TraceRecord]:
        constraints = constraints or RouteConstraints()
        mode = self.complexity_policy.select(state)
        selected, breakdowns = self.router.select(routes, goal, constraints)
        trace = TraceRecord(
            trace_id=str(uuid4()),
            step=state.step,
            goal=goal.normalized(),
            complexity_mode=mode,
            context=state.context.normalized().probabilities,
            candidate_ids=tuple(route.route_id for route in routes),
            energy={b.route_id: b.total for b in breakdowns},
            selected_route_id=selected.route_id if selected else None,
            abstained=selected is None,
            violations={b.route_id: tuple(b.violations) for b in breakdowns if b.violations},
            metadata={"drift": state.drift, "risk": state.risk},
        )
        self.reconstructive_memory.append(trace)
        return selected, trace
