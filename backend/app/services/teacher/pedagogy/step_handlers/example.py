from __future__ import annotations

from app.services.teacher.pedagogy.models import (
    TeachingExecution,
)


class ExampleHandler:
    def execute(
        self,
        step,
        target_skill: str | None = None,
    ) -> TeachingExecution:

        print("➡ Example Handler")

        return TeachingExecution(
            step=step,
            handler="ExampleHandler",
            prompt_instruction=("Provide one simple example using the grammar rule."),
            reveal_answer=True,
            use_example=True,
        )
