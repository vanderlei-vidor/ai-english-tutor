from __future__ import annotations

from app.services.teacher.pedagogy.models import (
    TeachingExecution,
)
from app.services.teacher.pedagogy.purpose_builders.correction import (
    CorrectionPurposeBuilder,
)


correction_builder = CorrectionPurposeBuilder()


class CorrectionHandler:
    def execute(
        self,
        step,
        target_skill: str | None = None,
    ) -> TeachingExecution:

        print("➡ Correction Handler")

        return TeachingExecution(
            step=step,
            handler="CorrectionHandler",
            purpose=step.purpose,
            prompt_instruction=correction_builder.build(
                target_skill=target_skill,
            ),
            wait_student=False,
            reveal_answer=True,
        )
