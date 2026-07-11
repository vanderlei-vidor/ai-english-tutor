from __future__ import annotations

from .models import (
    TeacherPerception,
    TeacherReflection,
)


class TeacherReflectionEngine:
    def reflect(
        self,
        perception: TeacherPerception,
    ) -> TeacherReflection:

        reflection = TeacherReflection()

        if perception.has_error:
            reflection.should_interrupt = True

            reflection.teaching_reason = "Grammar error detected."

            return reflection

        reflection.should_continue_lesson = False

        reflection.teaching_reason = "Natural conversation."

        return reflection


teacher_reflection_engine = TeacherReflectionEngine()
