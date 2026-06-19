from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .types import EnergyBreakdown, GoalWeights, RouteCandidate


@dataclass(frozen=True)
class RouteConstraints:
    min_accuracy: float = 0.0
    min_retention: float = 0.0
    min_stability: float = 0.0
    min_auditability: float = 0.0
    max_cost: float = 1.0
    max_risk: float = 1.0
    max_complexity: float = 1.0


@dataclass(frozen=True)
class EnergyRouter:
    risk_penalty: float = 0.25
    audit_penalty: float = 0.10
    complexity_penalty: float = 0.05

    def evaluate(
        self,
        route: RouteCandidate,
        goal: GoalWeights,
        constraints: RouteConstraints,
    ) -> EnergyBreakdown:
        g = goal.normalized()
        violations: list[str] = []
        if route.accuracy < constraints.min_accuracy:
            violations.append("accuracy_below_min")
        if route.retention < constraints.min_retention:
            violations.append("retention_below_min")
        if route.stability < constraints.min_stability:
            violations.append("stability_below_min")
        if route.auditability < constraints.min_auditability:
            violations.append("auditability_below_min")
        if route.cost > constraints.max_cost:
            violations.append("cost_above_max")
        if route.risk > constraints.max_risk:
            violations.append("risk_above_max")
        if route.complexity > constraints.max_complexity:
            violations.append("complexity_above_max")

        terms = {
            "accuracy_loss": g.accuracy * (1.0 - route.accuracy),
            "retention_loss": g.retention * (1.0 - route.retention),
            "cost": g.cost * route.cost,
            "stability_loss": g.stability * (1.0 - route.stability),
            "specialization_loss": g.specialization * (1.0 - route.specialization),
            "risk": self.risk_penalty * route.risk,
            "audit_loss": self.audit_penalty * (1.0 - route.auditability),
            "complexity": self.complexity_penalty * route.complexity,
        }
        total = sum(terms.values())
        return EnergyBreakdown(
            route_id=route.route_id,
            total=total,
            terms=terms,
            admissible=not violations,
            violations=tuple(violations),
        )

    def select(
        self,
        routes: Iterable[RouteCandidate],
        goal: GoalWeights,
        constraints: RouteConstraints,
    ) -> tuple[RouteCandidate | None, list[EnergyBreakdown]]:
        route_list = list(routes)
        breakdowns = [self.evaluate(route, goal, constraints) for route in route_list]
        admissible = [b for b in breakdowns if b.admissible]
        if not admissible:
            return None, breakdowns
        best = min(admissible, key=lambda b: b.total)
        selected = next(route for route in route_list if route.route_id == best.route_id)
        return selected, breakdowns
