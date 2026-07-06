from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class PromptContext:
    """
    Contexto estruturado que será enviado ao LLM.
    """

    student_level: str

    lesson_title: str

    explanation: str

    examples: list[str] = field(default_factory=list)

    exercises: list[str] = field(default_factory=list)

    tips: list[str] = field(default_factory=list)

    common_errors: list[str] = field(default_factory=list)

    tone: str = "friendly"

    language: str = "english"
