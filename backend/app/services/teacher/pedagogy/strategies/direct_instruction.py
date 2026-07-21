from __future__ import annotations

from .base import TeachingScriptBase

from .models import (
    TeachingScript,
    TeachingStep,
)


class DirectInstructionScript(
    TeachingScriptBase,
):
    """
    Roteiro clássico de ensino.

    O professor corrige diretamente,
    explica e apresenta um exemplo.
    """

    def build(
        self,
    ) -> TeachingScript:

        return TeachingScript(
            name="direct_instruction",
            steps=[
                TeachingStep(
                    action="correction",
                    reveal_answer=True,
                ),
                TeachingStep(
                    action="explanation",
                ),
                TeachingStep(
                    action="example",
                    use_example=True,
                ),
                TeachingStep(
                    action="wait",
                    wait_student=True,
                ),
            ],
        )
