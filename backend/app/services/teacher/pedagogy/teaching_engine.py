from __future__ import annotations

from .registry import (
    teaching_registry,
)

from .teaching_models import (
    TeachingStrategyPlan,
)


class TeachingEngine:
    def build(
        self,
        state,
    ) -> TeachingStrategyPlan:

        plan = TeachingStrategyPlan()

        strategy = teaching_registry.select(
            state,
        )

        strategy.build(
            state,
            plan,
        )

        return plan


teaching_engine = TeachingEngine()
