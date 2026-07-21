from __future__ import annotations

from .base import TeachingScriptBase
from .models import (
    TeachingScript,
    TeachingStep,
)


class GuidedDiscoveryScript(
    TeachingScriptBase,
):
    def build(
        self,
    ) -> TeachingScript:

        return TeachingScript(
            name="guided_discovery_script",
            strategy_type="guided_discovery",
            steps=[
                TeachingStep(
                    action="question",
                    purpose="activate_prior_knowledge",
                ),
                TeachingStep(
                    action="question",
                    purpose="guide_thinking",
                ),
                TeachingStep(
                    action="feedback",
                    purpose="encourage_discovery",
                ),
                TeachingStep(
                    action="question",
                    purpose="validate_understanding",
                ),
                TeachingStep(
                    action="finish",
                ),
            ],
        )
