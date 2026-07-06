from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class LearningEvent:
    """
    Representa um evento produzido durante
    a análise de aprendizagem.
    """

    skill: str

    success: bool

    concept_id: str | None = None

    confidence: float = 1.0

    source: str = "grammar_engine"
