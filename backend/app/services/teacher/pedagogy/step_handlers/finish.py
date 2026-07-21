from __future__ import annotations

from app.services.teacher.pedagogy.models import (
    TeachingExecution,
)


class FinishHandler:
    def execute(
        self,
        step,
        target_skill: str | None = None,
    ) -> TeachingExecution:

        print("➡ Finish Handler")

        return TeachingExecution(
            step=step,
            handler="FinishHandler",
            prompt_instruction=("Finish this teaching step naturally."),
            finish_lesson=True,
        )
