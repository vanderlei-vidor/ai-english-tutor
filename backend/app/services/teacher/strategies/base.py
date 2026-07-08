from __future__ import annotations

from abc import ABC, abstractmethod

from app.services.teacher.models import TeacherDecision
from app.services.pedagogical.analysis import PedagogicalAnalysis
from app.services.grammar_engine.models import (
    GrammarAnalysis,
)

class TeacherStrategy(ABC):
    @abstractmethod
    def matches(
        self,
        grammar: GrammarAnalysis,
        pedagogical: PedagogicalAnalysis,
    ) -> bool: ...

    @abstractmethod
    def build(
        self,
        grammar: GrammarAnalysis,
        pedagogical: PedagogicalAnalysis,
    ) -> TeacherDecision: ...
