from __future__ import annotations

from ..purpose_builders.question import (
    QuestionPurposeBuilder,
)

from ..models import TeachingExecution


question_builder = QuestionPurposeBuilder()


class QuestionHandler:
    def execute(
        self,
        step,
        target_skill: str | None = None,
    ) -> TeachingExecution:

        return TeachingExecution(
            step=step,
            handler="QuestionHandler",
            purpose=step.purpose,
            prompt_instruction=question_builder.build(
                step.purpose,
                target_skill=target_skill,
            ),
            wait_student=step.wait_student,
            ask_question=True,
            reveal_answer=False,
        )
