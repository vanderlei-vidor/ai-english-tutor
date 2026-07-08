from __future__ import annotations

from app.services.teacher.context import TeacherContext

from app.services.teacher.models import TeacherIntent

from app.services.teacher.strategies.conversation import (
    ConversationStrategy,
)

from app.services.teacher.strategies.correction import (
    CorrectionStrategy,
)

from app.services.teacher.strategies.base import (
    TeacherStrategy,
)


class TeacherRegistry:
    def __init__(self):

        self.strategies: list[TeacherStrategy] = [
            CorrectionStrategy(),
            ConversationStrategy(),
        ]

    def select(
        self,
        intent: TeacherIntent,
        context: TeacherContext,
    ) -> TeacherStrategy:

        for strategy in self.strategies:
            if intent == TeacherIntent.CORRECT and not isinstance(
                strategy,
                CorrectionStrategy,
            ):
                continue

            if intent != TeacherIntent.CORRECT and isinstance(
                strategy,
                CorrectionStrategy,
            ):
                continue

            if strategy.matches(
                context.grammar,
                context.pedagogical,
            ):
                return strategy

        return ConversationStrategy()


teacher_registry = TeacherRegistry()
