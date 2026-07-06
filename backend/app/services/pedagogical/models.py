from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class TeachingPlan:
    """
    Representa o plano pedagógico para ensinar um conceito.

    Este objeto é gerado pelo Pedagogical Engine e será utilizado
    posteriormente pelo LLM para construir a resposta ao aluno.
    """

    # -----------------------------------------
    # Identificação
    # -----------------------------------------

    concept_id: str

    title: str

    # -----------------------------------------
    # Conteúdo
    # -----------------------------------------

    explanation: str

    examples: list[str] = field(default_factory=list)

    exercises: list[str] = field(default_factory=list)

    # -----------------------------------------
    # Estratégia
    # -----------------------------------------

    review_after_days: int = 7

    difficulty: str = "easy"

    estimated_minutes: int = 15

    priority: int = 5

    # -----------------------------------------
    # Futuro
    # -----------------------------------------

    hints: list[str] = field(default_factory=list)

    notes: list[str] = field(default_factory=list)
