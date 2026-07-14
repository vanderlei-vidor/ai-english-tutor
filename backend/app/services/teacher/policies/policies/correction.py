from __future__ import annotations

from app.services.teacher.policies.base import (
    TeacherPolicy,
)

from app.services.teacher.policies.models import (
    PolicyResult,
)
from app.services.teacher.constants.interruption_levels import (
    InterruptionLevel,
)

class CorrectionPolicy(TeacherPolicy):
    @property
    def priority(self) -> int:
        return 10

    def evaluate(
        self,
        perception,
        lesson,
    ) -> PolicyResult:

        result = PolicyResult()

        # Conversa normal
        if not perception.has_error:
            result.reason = "Natural conversation."

            result.decision_strength = 10

            return result

        
        result.interruption_level = (
            InterruptionLevel.HIGH
        )

        result.decision_strength = 100

        result.reason = "Grammar error detected."

        return result
