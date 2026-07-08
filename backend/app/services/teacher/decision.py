from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class TeacherDecision:
    """
    Representa a decisão pedagógica final do professor.

    Nenhuma outra camada deve decidir como ensinar.
    Todas consomem este objeto.
    """

    teacher_action: str = "chat"

    teacher_strategy: str = "direct_instruction"

    teacher_reason: str = ""

    should_teach: bool = False

    should_review: bool = False

    should_exercise: bool = False

    explanation_level: str = "normal"

    confidence: float = 1.0

    target_skill: str | None = None

    detected_skill: str | None = None
