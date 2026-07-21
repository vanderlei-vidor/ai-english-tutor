from __future__ import annotations

from app.services.teacher.pedagogy.models import (
    TeachingExecution,
)


class HintHandler:
    def execute(
        self,
        step,
        target_skill: str | None = None,
    ) -> TeachingExecution:

        print("➡ Hint Handler")

        return TeachingExecution(
            step=step,
            handler="HintHandler",
            purpose=step.purpose,
            prompt_instruction=("Provide a subtle hint without revealing the answer."),
            wait_student=True,
            use_hint=True,
        )
