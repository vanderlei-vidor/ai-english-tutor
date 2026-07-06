from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class GrammarConcept:
    # --------------------------------------------------
    # Identificação
    # --------------------------------------------------

    id: str

    name: str

    level: str

    skill: str

    description: str

    # --------------------------------------------------
    # Conhecimento
    # --------------------------------------------------

    prerequisites: list[str] = field(default_factory=list)

    examples: list[str] = field(default_factory=list)

    common_errors: list[str] = field(default_factory=list)

    # --------------------------------------------------
    # Pedagogia
    # --------------------------------------------------

    teaching_priority: int = 5

    exercise_difficulty: str = "easy"

    estimated_study_minutes: int = 20

    review_after_days: int = 7

    mastery_threshold: int = 90

    # --------------------------------------------------
    # Futuras relações
    # --------------------------------------------------

    related_concepts: list[str] = field(default_factory=list)

    next_concepts: list[str] = field(default_factory=list)
