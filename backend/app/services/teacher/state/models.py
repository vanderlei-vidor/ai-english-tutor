from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from app.services.teacher.student.models import (
    StudentState,
)
from .skill_focus import (
    SkillFocus,
)


@dataclass(slots=True)
class TeachingState:
    # ==========================================================
    # Grammar
    # ==========================================================

    has_error: bool = False

    detected_skill: str | None = None

    target_skill: str | None = None

    skill_focus: SkillFocus = field(
        default_factory=SkillFocus,
    )

    # ==========================================================
    # Student
    # ==========================================================

    student: StudentState = field(
        default_factory=StudentState,
    )

    # ==========================================================
    # Lesson
    # ==========================================================

    lesson_active: bool = False

    lesson_goal: str = "conversation"

    lesson_phase: str = "conversation"

    lesson_step: int = 0

    lesson_total_steps: int = 0

    # ==========================================================
    # Teacher Decision
    # ==========================================================

    teacher_action: str = ""

    teacher_handler: str = ""

    teacher_purpose: str = ""

    teacher_mode: str = ""

    teacher_reason: str = ""

    response_style: str = ""

    tone: str = ""

    # Memória do aluno — usada pelo planning para exercise_type, etc.
    memory_data: dict[str, Any] = field(default_factory=dict)
