from __future__ import annotations

from app.services.teacher.strategies.conversation import (
    ConversationStrategy,
)
from app.services.teacher.strategies.correction import (
    CorrectionStrategy,
)
from app.services.pedagogical.analysis import PedagogicalAnalysis
from app.services.teacher.strategies.base import TeacherStrategy


class TeacherRegistry:
    def __init__(self):

        self.strategies: list[TeacherStrategy] = [
            CorrectionStrategy(),
            ConversationStrategy(),
        ]

    def select(
        self,
        grammar,
        pedagogical: PedagogicalAnalysis,
    ) -> TeacherStrategy:

        for strategy in self.strategies:
            if strategy.matches(
                grammar,
                pedagogical,
            ):
                return strategy

        return ConversationStrategy()


teacher_registry = TeacherRegistry()
