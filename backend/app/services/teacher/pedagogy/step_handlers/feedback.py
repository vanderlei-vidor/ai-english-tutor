from __future__ import annotations

from app.services.teacher.pedagogy.models import (
    TeachingExecution,
)


class FeedbackHandler:
    def execute(
        self,
        step,
        target_skill: str | None = None,
    ) -> TeachingExecution:

        print("➡ Feedback Handler")

        return TeachingExecution(
            step=step,
            handler="FeedbackHandler",
            purpose=step.purpose,
            prompt_instruction=("Provide encouraging feedback."),
        )
