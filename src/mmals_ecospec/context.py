from __future__ import annotations

from dataclasses import dataclass
from math import exp
from typing import Mapping, Sequence

from .types import ComplexityMode, ContextBelief, EcosystemState


@dataclass(frozen=True)
class SoftmaxContextModel:
    """Minimal context model over caller-provided scores.

    Production implementations replace this adapter with an inferred-context model,
    but must preserve the ContextBelief contract.
    """

    temperature: float = 1.0

    def infer(self, scores: Mapping[str, float]) -> ContextBelief:
        if self.temperature <= 0:
            raise ValueError("temperature must be positive")
        if not scores:
            raise ValueError("scores cannot be empty")
        maximum = max(scores.values())
        weights = {k: exp((v - maximum) / self.temperature) for k, v in scores.items()}
        return ContextBelief(weights).normalized()


@dataclass(frozen=True)
class ComplexityPolicy:
    fast_entropy_max: float = 0.45
    critical_entropy_min: float = 0.95
    critical_drift_min: float = 0.6
    critical_risk_min: float = 0.6

    def select(self, state: EcosystemState) -> ComplexityMode:
        entropy = state.context.entropy()
        if (
            state.risk >= self.critical_risk_min
            or state.drift >= self.critical_drift_min
            or entropy >= self.critical_entropy_min
        ):
            return ComplexityMode.CRITICAL
        if entropy <= self.fast_entropy_max and state.risk < 0.3 and state.drift < 0.3:
            return ComplexityMode.FAST
        return ComplexityMode.AMBIGUOUS

    def support_size(self, mode: ComplexityMode, n_contexts: int) -> int:
        if mode is ComplexityMode.FAST:
            return 1
        if mode is ComplexityMode.AMBIGUOUS:
            return min(3, n_contexts)
        return n_contexts
