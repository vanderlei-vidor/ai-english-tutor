from __future__ import annotations

from .base import TeachingScriptBase
from .models import (
    TeachingScript,
    TeachingStep,
)


class MinimalHintScript(
    TeachingScriptBase,
):
    def build(
        self,
    ) -> TeachingScript:

        return TeachingScript(
            name="minimal_hint",
            steps=[
                TeachingStep(
                    action="hint",
                    use_hint=True,
                ),
                TeachingStep(
                    action="wait",
                    wait_student=True,
                ),
            ],
        )
