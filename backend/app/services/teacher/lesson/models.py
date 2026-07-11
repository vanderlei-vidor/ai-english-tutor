from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class LessonState:
    """
    Representa uma microaula ativa.

    O professor pode continuar uma aula
    por vários turnos da conversa.
    """

    active: bool = False

    goal: str = "conversation"

    lesson_type: str = "conversation"

    target_skill: str | None = None

    #current_phase: str = "conversation"
    from .phases import LessonPhase

    current_phase: LessonPhase = (
        LessonPhase.CONVERSATION
    )

    current_step: int = 0

    total_steps: int = 1

    expected_turns: int = 1

    completed: bool = False

    interruption_level: str = "none"

    completion_condition: str = ""

    last_teacher_action: str = ""

    turns_elapsed: int = 0
