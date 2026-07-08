from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class ConversationAnalysis:
    """
    Representa a estratégia de conversa escolhida
    pelo professor para esta interação.

    Este objeto é produzido pelo ConversationEngine
    e utilizado posteriormente pelo LLM para construir
    a resposta ao aluno.
    """

    # --------------------------------------------------
    # Teacher Decision
    # --------------------------------------------------

    teacher_action: str = "chat"

    teacher_strategy: str = "normal"

    teacher_reason: str = ""

    confidence: float = 1.0

    # --------------------------------------------------
    # Teaching
    # --------------------------------------------------

    should_teach: bool = False

    should_review: bool = False

    should_exercise: bool = False

    # --------------------------------------------------
    # Conversation
    # --------------------------------------------------

    explanation_level: str = "normal"
