from __future__ import annotations

from app.services.grammar_engine.models import GrammarAnalysis
from app.services.pedagogical.presenter_registry import get_presenters


class LessonPresentationEngine:
    def build(
        self,
        analysis: GrammarAnalysis,
    ) -> None:

        for presenter in get_presenters():
            for plan in analysis.teaching_plans:
                lesson = presenter.present(plan)

                if lesson is not None:
                    analysis.presented_lessons.append(lesson)


lesson_presentation_engine = LessonPresentationEngine()
