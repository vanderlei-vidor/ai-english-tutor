from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class PromptContext:
    """
    Contexto completo enviado ao LLM.

    O Prompt Builder consolida informações das
    diversas Engines do sistema para que o modelo
    de IA apenas execute a estratégia definida pelo backend.
    """

    # ==================================================
    # Teacher
    # ==================================================

    teacher_strategy: str = ""

    teacher_action: str = ""

    teacher_handler: str = ""

    teacher_purpose: str = ""

    teacher_reason: str = ""

    explanation_level: str = "normal"

    confidence: float = 1.0

    # ==================================================
    # Student
    # ==================================================

    english_level: str = "A1"

    target_skill: str | None = None

    detected_skill: str | None = None

    # ==================================================
    # Conversation
    # ==================================================

    should_teach: bool = False

    should_review: bool = False

    should_exercise: bool = False

    # ==================================================
    # Future
    # ==================================================

    metadata: dict = field(default_factory=dict)
