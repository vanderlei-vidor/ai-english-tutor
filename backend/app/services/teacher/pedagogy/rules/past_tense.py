from __future__ import annotations

from .base import (
    ExplanationRule,
)


class PastTenseRule(ExplanationRule):
    def skill(self) -> str:

        return "past_tense"

    def apply(
        self,
        brain_state,
        plan,
    ) -> None:

        plan.use_example = True

        plan.teacher_reason = "Past tense requires a corrected example."

        plan.pedagogical_instructions.extend(
            [
                "Focus only on the past tense error.",
                "Mention the past time marker.",
            ]
        )
