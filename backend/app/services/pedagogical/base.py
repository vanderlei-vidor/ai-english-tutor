from __future__ import annotations

from abc import ABC, abstractmethod

from app.services.grammar_engine.models import GrammarAnalysis
from app.services.pedagogical.models import TeachingPlan


class BaseLessonPlanner(ABC):
    """
    Todo planner é responsável por transformar
    um GrammarConcept em um TeachingPlan.
    """

    @abstractmethod
    def build(
        self,
        analysis: GrammarAnalysis,
    ) -> TeachingPlan | None: ...
