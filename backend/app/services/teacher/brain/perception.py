from __future__ import annotations

from .models import TeacherPerception


class TeacherPerceptionEngine:
    def perceive(
        self,
        context,
    ) -> TeacherPerception:

        perception = TeacherPerception()

        perception.has_error = context.grammar.has_errors

        perception.detected_skill = (
            context.grammar.primary_error.skill
            if context.grammar.primary_error
            else None
        )

        perception.target_skill = context.pedagogical.target_skill

        perception.current_focus = context.grammar.current_focus

        perception.estimated_level = context.pedagogical.estimated_level

        perception.needs_intervention = perception.has_error

        return perception


teacher_perception_engine = TeacherPerceptionEngine()
