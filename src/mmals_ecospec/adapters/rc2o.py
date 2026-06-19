from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable, Mapping

from ..types import RouteCandidate


@dataclass(frozen=True)
class RC2OAdapter:
    """Convert RC2O-like candidate rows into EcoSpec route candidates.

    Field names are configurable because RC2O experiment outputs can evolve. Values
    are expected to have been normalised to [0, 1] by the metric evaluator.
    """

    id_field: str = "candidate"
    accuracy_field: str = "accuracy"
    retention_field: str = "retention"
    cost_field: str = "cost"
    stability_field: str = "stability"
    specialization_field: str = "specialization"
    risk_field: str = "risk"
    auditability_field: str = "auditability"
    complexity_field: str = "complexity"

    def from_row(self, row: Mapping[str, Any]) -> RouteCandidate:
        required = [
            self.id_field,
            self.accuracy_field,
            self.retention_field,
            self.cost_field,
            self.stability_field,
            self.specialization_field,
        ]
        missing = [key for key in required if key not in row]
        if missing:
            raise KeyError(f"Missing RC2O fields: {missing}")
        return RouteCandidate(
            route_id=str(row[self.id_field]),
            accuracy=float(row[self.accuracy_field]),
            retention=float(row[self.retention_field]),
            cost=float(row[self.cost_field]),
            stability=float(row[self.stability_field]),
            specialization=float(row[self.specialization_field]),
            risk=float(row.get(self.risk_field, 0.0)),
            auditability=float(row.get(self.auditability_field, 1.0)),
            complexity=float(row.get(self.complexity_field, 0.0)),
            hosts=tuple(row.get("hosts", ())),
            metadata={k: v for k, v in row.items() if k not in required},
        )

    def from_rows(self, rows: Iterable[Mapping[str, Any]]) -> list[RouteCandidate]:
        return [self.from_row(row) for row in rows]
