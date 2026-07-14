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

        match intent:

            case TeacherIntent.CORRECT:
                return CorrectionStrategy()

            case TeacherIntent.CONVERSATION:
                return ConversationStrategy()

            case _:
                return ConversationStrategy()


teacher_registry = TeacherRegistry()
