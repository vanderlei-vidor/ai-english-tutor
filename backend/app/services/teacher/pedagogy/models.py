"""
Pedagogy Engine Models
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .scripts.models import (
        TeachingScript,
        TeachingStep,
    )


@dataclass(slots=True)
class TeachingStrategyPlan:
    """
    Plano pedagógico produzido pelo Pedagogy Engine.
    """

    strategy: str = ""

    explanation_style: str = ""

    reveal_answer: bool = False

    use_example: bool = False

    use_analogy: bool = False

    ask_question: bool = False

    scaffolding: str = ""

    difficulty: str = ""

    feedback_style: str = ""

    conversation_style: str = ""

    exercise_style: str = ""

    wait_student: bool = True

    teacher_reason: str = ""

    script: TeachingScript | None = None


@dataclass(slots=True)
class TeachingExecution:
    """
    Resultado da execução do passo atual do roteiro.
    """

    step: TeachingStep

    handler: str = ""

    purpose: str = ""

    prompt_instruction: str = ""

    wait_student: bool = False

    reveal_answer: bool = False

    ask_question: bool = False

    use_example: bool = False

    use_hint: bool = False

    finish_lesson: bool = False


__all__ = [
    "TeachingStrategyPlan",
    "TeachingExecution",
]
