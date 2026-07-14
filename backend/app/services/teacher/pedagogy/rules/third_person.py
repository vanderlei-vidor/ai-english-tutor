from __future__ import annotations

from .base import (
    ExplanationRule,
)


class ThirdPersonRule(ExplanationRule):
    def skill(self) -> str:

        return "third_person"

    def apply(
        self,
        brain_state,
        plan,
    ) -> None:

        plan.teacher_reason = "Third person singular requires verb agreement."

        plan.pedagogical_instructions.extend(
            [
                "Focus only on the missing third person ending.",
                "Explain the agreement briefly.",
            ]
        )
