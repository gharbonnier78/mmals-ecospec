from __future__ import annotations

from dataclasses import dataclass, field
from typing import Hashable


@dataclass
class TabularGoalQ:
    """Small transparent RL extension for contract and toy experiments."""

    alpha: float = 0.2
    gamma: float = 0.95
    q: dict[tuple[Hashable, str, str], float] = field(default_factory=dict)

    def value(self, state: Hashable, goal_label: str, action: str) -> float:
        return self.q.get((state, goal_label, action), 0.0)

    def select(self, state: Hashable, goal_label: str, actions: list[str]) -> str:
        if not actions:
            raise ValueError("actions cannot be empty")
        return max(actions, key=lambda action: self.value(state, goal_label, action))

    def update(
        self,
        state: Hashable,
        goal_label: str,
        action: str,
        reward: float,
        next_state: Hashable,
        next_actions: list[str],
    ) -> None:
        current = self.value(state, goal_label, action)
        future = max((self.value(next_state, goal_label, a) for a in next_actions), default=0.0)
        target = reward + self.gamma * future
        self.q[(state, goal_label, action)] = current + self.alpha * (target - current)


@dataclass(frozen=True)
class ForwardBackwardScorer:
    """Reference dot-product interface, not a trained FB implementation."""

    def score(self, forward: list[float], goal_embedding: list[float]) -> float:
        if len(forward) != len(goal_embedding):
            raise ValueError("forward and goal_embedding must have the same dimension")
        return sum(a * b for a, b in zip(forward, goal_embedding))
