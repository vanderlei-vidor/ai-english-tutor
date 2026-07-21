from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class TeachingStep:
    action: str

    purpose: str = ""

    wait_student: bool = False
    reveal_answer: bool = False
    ask_question: bool = False
    use_example: bool = False
    use_hint: bool = False
    finish: bool = False


@dataclass(slots=True)
class TeachingScript:
    name: str

    strategy_type: str

    steps: list[TeachingStep] = field(
        default_factory=list,
    )

    description: str = ""

    def current_step(
        self,
        index: int,
    ) -> TeachingStep | None:

        if index < 0:
            return None

        if index >= len(self.steps):
            return None

        return self.steps[index]

    def has_next_step(
        self,
        index: int,
    ) -> bool:

        return index + 1 < len(self.steps)

    def total_steps(
        self,
    ) -> int:

        return len(self.steps)


__all__ = [
    "TeachingStep",
    "TeachingScript",
]
