from __future__ import annotations

from ..base import TeachingStrategy


class SocraticStrategy(
    TeachingStrategy,
):
    def matches(
        self,
        state,
    ) -> bool:

        if state.lesson_phase != "correction":
            return False

        return state.student.estimated_level in (
            "C1",
            "C2",
        )

    def build(
        self,
        state,
        plan,
    ) -> None:

        pass
