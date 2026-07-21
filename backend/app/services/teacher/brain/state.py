from __future__ import annotations

from dataclasses import dataclass

from app.services.teacher.student.models import StudentState

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
from app.services.teacher.pedagogy.models import (
    TeachingStrategyPlan,
)

from app.services.teacher.pedagogy.models import (
    TeachingStrategyPlan,
    TeachingExecution,
)

@dataclass(slots=True)
class TeacherBrainState:
    state: TeachingState

    student: StudentState

    perception: TeacherPerception

    reflection: TeacherReflection

    planning: TeacherActionPlan

    teaching: TeachingStrategyPlan
    
    execution: TeachingExecution 

    lesson: LessonState

    prompt: TeacherPrompt

    
