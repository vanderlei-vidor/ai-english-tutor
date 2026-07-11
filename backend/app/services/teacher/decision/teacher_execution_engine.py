from __future__ import annotations

from app.services.teacher.context import (
    TeacherContext,
)

from app.services.teacher.models import (
    TeacherDecision,
    TeacherIntent,
)

from app.services.teacher.brain.models import (
    TeacherActionPlan,
)


class TeacherExecutionEngine:
    def decide(
        self,
        context: TeacherContext,
        action_plan: TeacherActionPlan,
    ) -> TeacherDecision:

        if action_plan.goal == "teach":
            return TeacherDecision(
                intent=TeacherIntent.CORRECT,
                priority=action_plan.teaching_priority,
            )

        return TeacherDecision(
            intent=TeacherIntent.CONVERSATION,
            priority=action_plan.teaching_priority,
        )


teacher_execution_engine = TeacherExecutionEngine()
