from __future__ import annotations

from .models import TeacherResponsePlan

from app.services.teacher.brain.models import (
    TeacherActionPlan,
)


class TeacherResponsePlanner:
    """
    Camada temporaria de compatibilidade.

    A decisao de resposta ja vive no TeacherActionPlan. Enquanto
    brain.response existir, este adaptador apenas copia os campos.
    """

    def create_response_plan(
        self,
        action_plan: TeacherActionPlan,
    ) -> TeacherResponsePlan:

        return TeacherResponsePlan(
            teaching_mode=action_plan.teaching_mode,
            action=action_plan.action,
            response_style=action_plan.response_style,
            tone=action_plan.tone,
            explanation_level=action_plan.explanation_level,
            generate_example=action_plan.generate_example,
            generate_exercise=action_plan.generate_exercise,
            ask_question=action_plan.ask_question,
            wait_for_student=action_plan.wait_for_student,
            finish_lesson=action_plan.finish_lesson,
        )


teacher_response_planner = TeacherResponsePlanner()
