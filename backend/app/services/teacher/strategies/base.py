from __future__ import annotations

from abc import ABC, abstractmethod

from app.services.teacher.brain.state import (
    TeacherBrainState,
)

from app.services.pedagogical.analysis import (
    PedagogicalAnalysis,
)

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
        brain_state: TeacherBrainState,
    ) -> None: ...
