from __future__ import annotations

from app.services.teacher.models import (
    TeacherDecision,
    TeacherIntent,
)

from app.services.teacher.strategies.base import TeacherStrategy

from app.services.pedagogical.analysis import (
    PedagogicalAnalysis,
)

from app.services.grammar_engine.models import (
    GrammarAnalysis,
)


class CorrectionStrategy(TeacherStrategy):
    def matches(
        self,
        grammar: GrammarAnalysis,
        pedagogical,
    ):

        return grammar.has_errors

    def build(
        self,
        grammar: GrammarAnalysis,
        pedagogical: PedagogicalAnalysis,
    ) -> TeacherDecision:

        return TeacherDecision(
            # Nova arquitetura
            intent=TeacherIntent.CORRECT,
            priority=100,
            # Compatibilidade
            teacher_action="correction",
            teacher_strategy="direct_instruction",
            teacher_reason="Grammar error detected.",
            should_teach=True,
            should_review=False,
            should_exercise=False,
            explanation_level="normal",
            confidence=1.0,
            target_skill=pedagogical.target_skill,
            detected_skill=pedagogical.detected_skill,
        )
