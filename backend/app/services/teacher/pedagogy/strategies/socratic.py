from __future__ import annotations

from .base import TeachingScriptBase
from .models import (
    TeachingScript,
    TeachingStep,
)


class SocraticScript(
    TeachingScriptBase,
):
    def build(
        self,
    ) -> TeachingScript:

        return TeachingScript(
            name="socratic",
            steps=[
                TeachingStep(
                    action="question",
                    ask_question=True,
                ),
                TeachingStep(
                    action="question",
                    ask_question=True,
                ),
                TeachingStep(
                    action="wait",
                    wait_student=True,
                ),
            ],
        )
