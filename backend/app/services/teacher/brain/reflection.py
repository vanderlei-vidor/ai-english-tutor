from __future__ import annotations

from app.services.teacher.constants.interruption_levels import InterruptionLevel

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
from app.services.teacher.state.models import (
    TeachingState,
)

class TeacherReflectionEngine:
    def reflect(
        self,
        perception: TeacherPerception,
        state: TeachingState,
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


        reflection.interruption_level = (
            policy_result.interruption_level or InterruptionLevel.NONE
        )

        reflection.should_continue_lesson = False

        reflection.should_start_new_lesson = False

        reflection.should_review = policy_result.should_review or False

        reflection.should_praise = policy_result.should_praise or False

        reflection.teaching_reason = policy_result.reason

        # -----------------------------------------
        # Defaults (temporários)
        # -----------------------------------------

       

        

        return reflection


teacher_reflection_engine = TeacherReflectionEngine()
