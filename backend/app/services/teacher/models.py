from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class TeacherIntent(str, Enum):
    CORRECT = "correct"
    PRAISE = "praise"
    EXPLAIN = "explain"
    REVIEW = "review"
    PRACTICE = "practice"
    CONVERSATION = "conversation"
    IGNORE = "ignore"


@dataclass(slots=True)
class TeacherDecision:
    """
    Representa a decisão pedagógica final do professor.

    Durante a migração mantemos compatibilidade
    com o restante do sistema.
    """

    # ==========================
    # NOVA ARQUITETURA
    # ==========================

    intent: TeacherIntent = TeacherIntent.CONVERSATION

    priority: int = 100

    # ==========================
    # COMPATIBILIDADE
    # ==========================

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
