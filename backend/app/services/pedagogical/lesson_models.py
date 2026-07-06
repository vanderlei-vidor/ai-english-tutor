from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class TeachingLesson:
    """
    Aula pronta para ser entregue ao aluno.
    """

    title: str

    explanation: str

    examples: list[str] = field(default_factory=list)

    tips: list[str] = field(default_factory=list)

    exercises: list[str] = field(default_factory=list)

    summary: str = ""
