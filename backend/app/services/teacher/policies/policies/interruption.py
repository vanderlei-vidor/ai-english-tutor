from __future__ import annotations

from app.services.teacher.policies.base import (
    TeacherPolicy,
)

from app.services.teacher.policies.models import (
    PolicyResult,
)


class InterruptionPolicy(TeacherPolicy):
    @property
    def priority(self) -> int:
        return 20

    def evaluate(
        self,
        perception,
        lesson,
    ) -> PolicyResult:

        result = PolicyResult()

        if lesson.active:
            result.should_interrupt = False

        return result
