from __future__ import annotations

from .base import (
    ExplanationRule,
)


class PrepositionsRule(ExplanationRule):
    def skill(self) -> str:

        return "prepositions"

    def apply(
        self,
        brain_state,
        plan,
    ) -> None:

        plan.teacher_reason = "Prepositions depend on context."

        plan.pedagogical_instructions.extend(
            [
                "Focus only on the incorrect preposition.",
                "Avoid explaining verb tense.",
            ]
        )
