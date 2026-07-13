from __future__ import annotations

from .base import TeacherPolicy

_POLICIES: list[TeacherPolicy] = []


def register_policy(
    policy: TeacherPolicy,
) -> None:

    _POLICIES.append(policy)


def get_policies() -> list[TeacherPolicy]:

    return sorted(
        _POLICIES,
        key=lambda policy: policy.priority,
    )


from .policies.correction import (
    CorrectionPolicy,
)

from .policies.interruption import (
    InterruptionPolicy,
)

register_policy(
    CorrectionPolicy(),
)

register_policy(
    InterruptionPolicy(),
)
