from __future__ import annotations

from app.services.teacher.decision import (
    TeacherDecision,
)

from app.services.pedagogical.analysis import (
    PedagogicalAnalysis,
)

from app.services.teacher.registry import (
    teacher_registry,
)
from app.services.grammar_engine.models import (
    GrammarAnalysis,
)


class TeacherEngine:
    """
    Responsável apenas por selecionar
    a estratégia pedagógica adequada.

    Toda a inteligência fica nas Strategies.
    """

    def decide(
        self,
        grammar: GrammarAnalysis,
        pedagogical: PedagogicalAnalysis,
    ) -> TeacherDecision:

        strategy = teacher_registry.select(
            grammar,
            pedagogical,
        )

        decision = strategy.build(
            grammar,
            pedagogical,
        )

        print(f"🎯 TEACHER STRATEGY SELECTED: {strategy.__class__.__name__}")

        return decision


teacher_engine = TeacherEngine()
