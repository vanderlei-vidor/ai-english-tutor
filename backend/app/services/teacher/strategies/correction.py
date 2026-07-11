from __future__ import annotations

from app.services.teacher.models import (
    TeacherDecision,
    TeacherIntent,
)

from app.services.teacher.strategies.base import (
    TeacherStrategy,
)

from app.services.teacher.brain.state import (
    TeacherBrainState,
)


class CorrectionStrategy(TeacherStrategy):
    def matches(
        self,
        grammar,
        pedagogical,
    ):

        return grammar.has_errors

    def build(
        self,
        brain_state: TeacherBrainState,
    ) -> TeacherDecision:

        return TeacherDecision(
            intent=TeacherIntent.CORRECT,
            priority=100,
            confidence=1.0,
        )
