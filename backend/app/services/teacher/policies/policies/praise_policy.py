from __future__ import annotations

from app.services.teacher.policies.base import (
    TeacherPolicy,
)

from app.services.teacher.policies.models import (
    PolicyResult,
)


class PraisePolicy(TeacherPolicy):
    @property
    def priority(self) -> int:
        return 30

    def evaluate(
        self,
        perception,
        lesson,
    ) -> PolicyResult:

        result = PolicyResult()

        if perception.has_error:
            return result

        result.should_praise = True

        result.reason = "Student answered correctly."

        return result
