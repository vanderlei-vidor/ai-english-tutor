from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class TeacherResponsePlan:
    """
    Plano de resposta do professor.

    Define COMO o professor irá responder.
    """

    teaching_mode: str = "conversation"

    action: str = "chat"

    response_style: str = "natural"

    tone: str = "friendly"

    explanation_level: str = "normal"

    generate_example: bool = False

    generate_exercise: bool = False

    ask_question: bool = False

    wait_for_student: bool = True

    finish_lesson: bool = False
