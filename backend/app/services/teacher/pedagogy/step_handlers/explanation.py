from __future__ import annotations

from app.services.teacher.pedagogy.models import (
    TeachingExecution,
)


class ExplanationHandler:
    def execute(
        self,
        step,
        target_skill: str | None = None,
    ) -> TeachingExecution:

        print("➡ Explanation Handler")

        return TeachingExecution(
            step=step,
            handler="ExplanationHandler",
            prompt_instruction=("Explain the grammar rule clearly."),
            reveal_answer=True,
        )
