from __future__ import annotations
from app.services.teacher.models import TeacherDecision, TeacherIntent
from app.services.teacher.strategies.base import TeacherStrategy
from app.services.pedagogical.analysis import PedagogicalAnalysis

from app.services.grammar_engine.models import GrammarAnalysis


class ConversationStrategy(TeacherStrategy):
    def matches(
        self,
        grammar: GrammarAnalysis,
        pedagogical: PedagogicalAnalysis,
    ) -> bool:

        return not grammar.has_errors

    def build(
        self,
        grammar: GrammarAnalysis,
        pedagogical: PedagogicalAnalysis,
    ) -> TeacherDecision:

        return TeacherDecision(
            intent=TeacherIntent.CONVERSATION,
            priority=10,
            teacher_action="chat",
            teacher_strategy="conversation",
            teacher_reason="Natural conversation.",
            should_teach=False,
            should_review=False,
            should_exercise=False,
            explanation_level="normal",
            confidence=1.0,
            target_skill=pedagogical.target_skill,
            detected_skill=pedagogical.detected_skill,
        )
