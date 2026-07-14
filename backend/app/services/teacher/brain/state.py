from __future__ import annotations

from dataclasses import dataclass

from app.services.teacher.response.models import TeacherResponsePlan

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

@dataclass(slots=True)
class TeacherBrainState:
    """
    Estado completo do cérebro do professor.

    Todas as etapas do raciocínio ficam reunidas aqui.
    """

    perception: TeacherPerception

    reflection: TeacherReflection

    planning: TeacherActionPlan

    lesson: LessonState
    
    response: TeacherResponsePlan

    prompt: TeacherPrompt
