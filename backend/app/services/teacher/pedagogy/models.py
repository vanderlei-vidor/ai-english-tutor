from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class ExplanationPlan:
    style: str = "brief"

    reveal_answer: bool = True

    use_example: bool = False

    use_analogy: bool = False

    ask_question: bool = False

    scaffolding: str = "none"

    difficulty: str = "normal"

    teacher_reason: str = ""

    pedagogical_instructions: list[str] = field(
        default_factory=list,
    )
