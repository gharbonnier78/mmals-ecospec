from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping, Sequence

from .types import GoalWeights, TraceRecord


@dataclass(frozen=True)
class ValidityEnvelope:
    max_drift: float
    max_risk: float
    allowed_goal_labels: frozenset[str] = frozenset()
    latent_min: Sequence[float] | None = None
    latent_max: Sequence[float] | None = None

    def contains(
        self,
        latent: Sequence[float],
        drift: float,
        risk: float,
        goal_label: str | None = None,
    ) -> bool:
        if drift > self.max_drift or risk > self.max_risk:
            return False
        if self.allowed_goal_labels and goal_label not in self.allowed_goal_labels:
            return False
        if self.latent_min is not None and any(x < lo for x, lo in zip(latent, self.latent_min)):
            return False
        if self.latent_max is not None and any(x > hi for x, hi in zip(latent, self.latent_max)):
            return False
        return True


@dataclass(frozen=True)
class CompiledRoute:
    route_id: str
    envelope: ValidityEnvelope
    estimated_regret: float
    cost_gain: float
    evidence_count: int
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def is_publishable(
        self,
        min_evidence: int = 10,
        max_regret: float = 0.05,
        min_cost_gain: float = 0.05,
    ) -> bool:
        return (
            self.evidence_count >= min_evidence
            and self.estimated_regret <= max_regret
            and self.cost_gain >= min_cost_gain
        )


@dataclass
class ReconstructiveMemory:
    traces: list[TraceRecord] = field(default_factory=list)

    def append(self, trace: TraceRecord) -> None:
        self.traces.append(trace)


@dataclass
class SyntheticMemory:
    compiled: dict[str, CompiledRoute] = field(default_factory=dict)

    def store(self, route: CompiledRoute) -> None:
        if not route.is_publishable():
            raise ValueError("Compiled route does not satisfy publication thresholds")
        self.compiled[route.route_id] = route

    def retrieve(
        self,
        route_id: str,
        latent: Sequence[float],
        drift: float,
        risk: float,
        goal_label: str | None = None,
    ) -> CompiledRoute | None:
        route = self.compiled.get(route_id)
        if route is None:
            return None
        if route.envelope.contains(latent, drift, risk, goal_label):
            return route
        return None
