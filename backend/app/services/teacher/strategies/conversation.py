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


class ConversationStrategy(TeacherStrategy):
    def matches(
        self,
        grammar,
        pedagogical,
    ) -> bool:

        return not grammar.has_errors

    def build(
        self,
        brain_state: TeacherBrainState,
    ) -> None:

        pass