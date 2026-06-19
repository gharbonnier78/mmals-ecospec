from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from math import log
from typing import Any, Mapping, Sequence


class ComplexityMode(str, Enum):
    FAST = "fast"
    AMBIGUOUS = "ambiguous"
    CRITICAL = "critical"


@dataclass(frozen=True)
class GoalWeights:
    accuracy: float = 0.2
    retention: float = 0.2
    cost: float = 0.2
    stability: float = 0.2
    specialization: float = 0.2

    def __post_init__(self) -> None:
        values = self.as_tuple()
        if any(v < 0 for v in values):
            raise ValueError("Goal weights must be non-negative")
        if sum(values) <= 0:
            raise ValueError("At least one goal weight must be positive")

    def as_tuple(self) -> tuple[float, float, float, float, float]:
        return (
            self.accuracy,
            self.retention,
            self.cost,
            self.stability,
            self.specialization,
        )

    def normalized(self) -> "GoalWeights":
        total = sum(self.as_tuple())
        return GoalWeights(*(v / total for v in self.as_tuple()))


@dataclass(frozen=True)
class ContextBelief:
    probabilities: Mapping[str, float]

    def __post_init__(self) -> None:
        if not self.probabilities:
            raise ValueError("Context belief cannot be empty")
        if any(v < 0 for v in self.probabilities.values()):
            raise ValueError("Context probabilities must be non-negative")
        if sum(self.probabilities.values()) <= 0:
            raise ValueError("Context probability mass must be positive")

    def normalized(self) -> "ContextBelief":
        total = sum(self.probabilities.values())
        return ContextBelief({k: v / total for k, v in self.probabilities.items()})

    def entropy(self) -> float:
        p = self.normalized().probabilities
        return -sum(v * log(v) for v in p.values() if v > 0)

    def top_k(self, k: int) -> "ContextBelief":
        if k <= 0:
            raise ValueError("k must be positive")
        ranked = sorted(self.probabilities.items(), key=lambda item: item[1], reverse=True)[:k]
        return ContextBelief(dict(ranked)).normalized()

    def maximum(self) -> tuple[str, float]:
        return max(self.normalized().probabilities.items(), key=lambda item: item[1])


@dataclass(frozen=True)
class RouteCandidate:
    route_id: str
    accuracy: float
    retention: float
    cost: float
    stability: float
    specialization: float
    risk: float = 0.0
    auditability: float = 1.0
    complexity: float = 0.0
    hosts: Sequence[str] = field(default_factory=tuple)
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        bounded = {
            "accuracy": self.accuracy,
            "retention": self.retention,
            "cost": self.cost,
            "stability": self.stability,
            "specialization": self.specialization,
            "risk": self.risk,
            "auditability": self.auditability,
            "complexity": self.complexity,
        }
        for name, value in bounded.items():
            if not 0.0 <= value <= 1.0:
                raise ValueError(f"{name} must be in [0, 1], got {value}")


@dataclass(frozen=True)
class EnergyBreakdown:
    route_id: str
    total: float
    terms: Mapping[str, float]
    admissible: bool
    violations: Sequence[str] = field(default_factory=tuple)


@dataclass(frozen=True)
class EcosystemState:
    step: int
    latent: Sequence[float]
    context: ContextBelief
    drift: float = 0.0
    risk: float = 0.0
    budget: Mapping[str, float] = field(default_factory=dict)
    health: Mapping[str, float] = field(default_factory=dict)
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.step < 0:
            raise ValueError("step must be non-negative")
        if self.drift < 0 or self.risk < 0:
            raise ValueError("drift and risk must be non-negative")


@dataclass(frozen=True)
class TraceRecord:
    trace_id: str
    step: int
    goal: GoalWeights
    complexity_mode: ComplexityMode
    context: Mapping[str, float]
    candidate_ids: Sequence[str]
    energy: Mapping[str, float]
    selected_route_id: str | None
    abstained: bool
    violations: Mapping[str, Sequence[str]] = field(default_factory=dict)
    metadata: Mapping[str, Any] = field(default_factory=dict)
