from __future__ import annotations

from app.services.teacher.context import (
    TeacherContext,
)

from app.services.teacher.models import (
    TeacherDecision,
    TeacherIntent,
)


class TeacherDecisionEngine:
    def decide(
        self,
        context: TeacherContext,
    ) -> TeacherDecision:

        if context.grammar.has_errors:
            return TeacherDecision(
                intent=TeacherIntent.CORRECT,
                priority=100,
            )

        return TeacherDecision(
            intent=TeacherIntent.CONVERSATION,
            priority=10,
        )


teacher_decision_engine = TeacherDecisionEngine()
