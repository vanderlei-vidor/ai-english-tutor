from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class TeacherResponse:
    """
    Resposta produzida pelo Teacher Engine.

    Este objeto representa a resposta pedagógica
    antes de ser serializada para JSON.
    """

    # Execução pedagógica

    handler: str = ""

    purpose: str = ""

    target_skill: str = ""

    wait_student: bool = False

    ask_question: bool = False

    reveal_answer: bool = False

    # Conteúdo produzido pelo LLM

    conversation_reply: str = ""

    correction: str | None = None

    explanation_pt: str | None = None

    example: str | None = None

    exercise: str | None = None

    grammar_confidence: float = 0.0

    needs_correction: bool = False

    exercise_type: str | None = None
