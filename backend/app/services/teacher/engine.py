from __future__ import annotations

from app.services.teacher.context import TeacherContext
from app.services.teacher.result import (
    TeacherResult,
)
from app.services.teacher.logger import (
    teacher_logger,
)
from app.services.teacher.brain.engine import (
    teacher_brain,
)
from app.services.teacher.lesson.manager import (
    lesson_manager,
)


class TeacherEngine:
    """
    Coordena o Teacher Brain.

    O TeacherEngine não toma decisões.
    Ele apenas coordena o fluxo de pensamento
    e delega a execução ao plano produzido pelo Brain.

        Context
            ↓
        Teacher Brain (perception → reflection → planning)
            ↓
        TeacherResult (brain_state)
    """

    def decide(
        self,
        context: TeacherContext,
    ) -> TeacherResult:

        brain_state = teacher_brain.think(
            context,
        )

        teacher_logger.brain(
            brain_state,
        )

        lesson_manager.set_last_action(
            brain_state.planning.action,
        )
        lesson_manager.advance()

        return TeacherResult(
            brain=brain_state,
        )


teacher_engine = TeacherEngine()
