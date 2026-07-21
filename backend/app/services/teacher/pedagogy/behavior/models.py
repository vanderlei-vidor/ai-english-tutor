from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class TeachingBehavior:
    instructions: list[str] = field(
        default_factory=list,
    )

    constraints: list[str] = field(
        default_factory=list,
    )

    reveal_answer: bool = False

    wait_student: bool = True

    ask_question: bool = False
