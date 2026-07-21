from __future__ import annotations

from .base import TeachingScriptBase
from .models import (
    TeachingScript,
    TeachingStep,
)


class CommunicativeScript(
    TeachingScriptBase,
):
    def build(
        self,
    ) -> TeachingScript:

        return TeachingScript(
            name="communicative",
            steps=[
                TeachingStep(
                    action="conversation",
                    wait_student=True,
                ),
            ],
        )
