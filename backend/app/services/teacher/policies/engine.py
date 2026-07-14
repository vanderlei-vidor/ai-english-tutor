from __future__ import annotations

from .models import (
    PolicyResult,
)

from .registry import (
    get_policies,
)


class TeacherPolicyEngine:
    def evaluate(
        self,
        perception,
        lesson,
    ) -> PolicyResult:

        policy_result = PolicyResult()

        for policy in get_policies():
            result = policy.evaluate(
                perception,
                lesson,
            )

            if result.should_review is not None:
                policy_result.should_review = result.should_review

            if result.should_exercise is not None:
                policy_result.should_exercise = result.should_exercise

            if result.reason:
                policy_result.reason = result.reason

            if result.should_praise is not None:

                policy_result.should_praise = (
                    result.should_praise
                )

            if result.interruption_level is not None:

                policy_result.interruption_level = (
                    result.interruption_level
                )

            if result.decision_strength > policy_result.decision_strength:

                policy_result.decision_strength = (
                    result.decision_strength
                )

        return policy_result


teacher_policy_engine = TeacherPolicyEngine()
