from __future__ import annotations

from app.services.teacher.pedagogy.models import (
    TeachingExecution,
)


class ExerciseHandler:
    def execute(
        self,
        step,
        target_skill: str | None = None,
    ) -> TeachingExecution:

        print("➡ Exercise Handler")

        return TeachingExecution(
            step=step,
            handler="ExerciseHandler",
            prompt_instruction=("Create one short exercise for the student."),
            wait_student=True,
        )
