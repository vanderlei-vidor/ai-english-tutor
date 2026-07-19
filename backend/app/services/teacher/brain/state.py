from __future__ import annotations

from dataclasses import dataclass

from app.services.teacher.student.models import StudentState
from app.services.teacher.pedagogy.teaching_models import TeachingStrategyPlan

from .models import (
    TeacherPerception,
    TeacherReflection,
    TeacherActionPlan,
)

from app.services.teacher.lesson.models import (
    LessonState,
)
from app.services.teacher.prompt.models import (
    TeacherPrompt,
)
from app.services.teacher.state.models import (
    TeachingState,
)
@dataclass(slots=True)
class TeacherBrainState:
    """
    Estado completo do cérebro do professor.

    Todas as etapas do raciocínio ficam reunidas aqui.
    """

    state: TeachingState

    student: StudentState

    perception: TeacherPerception

    reflection: TeacherReflection

    planning: TeacherActionPlan

    teaching: TeachingStrategyPlan

    lesson: LessonState

    prompt: TeacherPrompt
