from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class TeachingStep:
    """
    Representa um único passo do roteiro pedagógico.
    """

    action: str

    wait_student: bool = False

    reveal_answer: bool = False

    ask_question: bool = False

    use_example: bool = False

    use_hint: bool = False

    finish: bool = False


@dataclass(slots=True)
class TeachingScript:
    """
    Sequência de passos que define
    como uma estratégia será executada.
    """

    name: str

    steps: list[TeachingStep] = field(
        default_factory=list,
    )

    def current_step(
        self,
        index: int,
    ) -> TeachingStep | None:

        if index >= len(self.steps):
            return None

        return self.steps[index]
