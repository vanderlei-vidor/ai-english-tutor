from __future__ import annotations

from .models import TeacherPerception
from app.services.teacher.state.models import (
    TeachingState,
)

class TeacherPerceptionEngine:
    def perceive(
        self,
        context,
        state: TeachingState,
    ) -> TeacherPerception:

        perception = TeacherPerception()

        has_grammar_error = context.grammar.has_errors
        known_error = context.known_error

        perception.has_error = (
            has_grammar_error
            or known_error is not None
        )

        # ==========================
        # Detected Skill
        # ==========================

        if has_grammar_error:
            perception.detected_skill = (
                context.grammar.primary_error.skill
                if context.grammar.primary_error
                else None
            )
        elif known_error:
            perception.detected_skill = known_error.get("skill")
        else:
            perception.detected_skill = None

        # ==========================
        # Teaching Skill
        # ==========================

        if has_grammar_error:
            perception.target_skill = perception.detected_skill

        elif known_error:
            perception.target_skill = known_error.get("skill")

        else:
            perception.target_skill = context.pedagogical.target_skill

        perception.current_focus = context.grammar.current_focus

        perception.estimated_level = context.pedagogical.estimated_level

        perception.needs_intervention = perception.has_error

        state.has_error = perception.has_error

        state.detected_skill = perception.detected_skill

        state.target_skill = perception.target_skill

        state.skill_focus.detected = perception.detected_skill

        state.skill_focus.teaching = perception.target_skill

        return perception


teacher_perception_engine = TeacherPerceptionEngine()
