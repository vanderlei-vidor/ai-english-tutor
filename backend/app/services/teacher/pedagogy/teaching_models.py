from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class TeachingStrategyPlan:
    """
    Plano pedagógico completo.

    Representa COMO o professor irá ensinar.
    """

    # ==========================================================
    # Estratégia
    # ==========================================================

    strategy: str = "direct_instruction"

    teacher_reason: str = ""

    # ==========================================================
    # Explicação
    # ==========================================================

    explanation_style: str = "brief"

    difficulty: str = "normal"

    scaffolding: str = "none"

    reveal_answer: bool = True

    use_example: bool = False

    use_analogy: bool = False

    ask_question: bool = False

    # ==========================================================
    # Feedback
    # ==========================================================

    feedback_style: str = "encouraging"

    conversation_style: str = "natural"

    question_style: str = "none"

    example_style: str = "none"

    exercise_style: str = "none"

    wait_student: bool = True

    # ==========================================================
    # Prompt
    # ==========================================================

    pedagogical_instructions: list[str] = field(
        default_factory=list,
    )
