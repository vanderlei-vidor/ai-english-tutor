from __future__ import annotations

from app.services.pedagogical.lesson_models import TeachingLesson
from app.services.pedagogical.prompt.prompt_models import PromptContext


class PromptContextBuilder:
    """
    Converte uma TeachingLesson em um PromptContext,
    que será utilizado posteriormente pelo LLM.
    """

    def build(
        self,
        lesson: TeachingLesson,
        student_level: str = "A2",
    ) -> PromptContext:

        return PromptContext(
            student_level=student_level,
            lesson_title=lesson.title,
            explanation=lesson.explanation,
            examples=lesson.examples,
            exercises=lesson.exercises,
            tips=lesson.tips,
        )


prompt_context_builder = PromptContextBuilder()
