from __future__ import annotations

from .models import (
    TeacherPerception,
    TeacherReflection,
)

from app.services.teacher.lesson.manager import (
    lesson_manager,
)

from app.services.teacher.policies.engine import (
    teacher_policy_engine,
)


class TeacherReflectionEngine:
    def reflect(
        self,
        perception: TeacherPerception,
    ) -> TeacherReflection:

        reflection = TeacherReflection()

        lesson = lesson_manager.current()

        policy_result = teacher_policy_engine.evaluate(
            perception=perception,
            lesson=lesson,
        )

        # -----------------------------------------
        # Decisions produced by Policies
        # -----------------------------------------

        reflection.interruption_level = policy_result.interruption_level or "none"

        reflection.should_continue_lesson = False

        reflection.should_start_new_lesson = False

        reflection.should_review = policy_result.should_review or False

        reflection.teaching_reason = policy_result.reason

        # -----------------------------------------
        # Defaults (temporários)
        # -----------------------------------------

       

        

        return reflection


teacher_reflection_engine = TeacherReflectionEngine()
