from __future__ import annotations

from app.services.teacher.context import TeacherContext

from app.services.teacher.decision.engine import (
    teacher_decision_engine,
)

from app.services.teacher.registry import (
    teacher_registry,
)

from app.services.teacher.models import (
    TeacherDecision,
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
    ) -> TeacherDecision:

        decision = teacher_decision_engine.decide(
            context,
        )

        strategy = teacher_registry.select(
            intent=decision.intent,
            context=context,
        )

        teacher_decision = strategy.build(
            context.grammar,
            context.pedagogical,
        )

        print()
        print("=" * 60)
        print("TEACHER BRAIN")
        print("=" * 60)
        print(f"Intent  : {teacher_decision.intent.value}")
        print(f"Strategy: {strategy.__class__.__name__}")
        print("=" * 60)

        return teacher_decision


teacher_engine = TeacherEngine()
