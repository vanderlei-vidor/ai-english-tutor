from __future__ import annotations

from .base import (
    ExplanationRule,
)


class ArticlesRule(ExplanationRule):
    def skill(self) -> str:

        return "articles"

    def apply(
        self,
        brain_state,
        plan,
    ) -> None:

        plan.teacher_reason = "Articles require contextual explanation."

        plan.pedagogical_instructions.extend(
            [
                "Explain article choice naturally.",
                "Compare only the necessary article.",
            ]
        )
