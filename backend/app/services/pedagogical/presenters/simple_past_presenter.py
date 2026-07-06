from __future__ import annotations

from app.services.pedagogical.lesson_models import TeachingLesson
from app.services.pedagogical.models import TeachingPlan
from app.services.pedagogical.presenters.base import BaseLessonPresenter


class SimplePastPresenter(BaseLessonPresenter):
    """
    Apresenta uma aula de Simple Past ao aluno.
    """

    def present(
        self,
        plan: TeachingPlan,
    ) -> TeachingLesson | None:

        if plan.concept_id != "simple_past":
            return None

        return TeachingLesson(
            title=plan.title,
            explanation=plan.explanation,
            examples=plan.examples,
            exercises=plan.exercises,
            summary=("Use the Simple Past for completed actions in the past."),
        )
