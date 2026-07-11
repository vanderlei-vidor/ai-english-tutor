from __future__ import annotations

from app.services.teacher.context import TeacherContext

from app.services.teacher.decision.teacher_execution_engine import (
    teacher_execution_engine,
)

from app.services.teacher.registry import (
    teacher_registry,
)

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
    Ele apenas coordena o fluxo.

        Context
            ↓
        Decision Engine
            ↓
        Registry
            ↓
        Strategy
            ↓
        TeacherDecision
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

        decision = teacher_execution_engine.decide(
            context=context,
            action_plan=brain_state.planning,
        )

        strategy = teacher_registry.select(
            intent=decision.intent,
            context=context,
        )

        teacher_decision = strategy.build(
            brain_state,
        )

        



        print()
        print("=" * 60)
        print("TEACHER BRAIN")
        print("=" * 60)
        print(f"Intent  : {teacher_decision.intent.value}")
        print(f"Strategy: {strategy.__class__.__name__}")
        print("=" * 60)

        lesson_manager.set_last_action(
            brain_state.planning.action,
        )

        

        lesson_manager.advance()

        return TeacherResult(
            brain=brain_state,
        )


teacher_engine = TeacherEngine()
