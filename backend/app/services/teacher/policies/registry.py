from __future__ import annotations

from app.services.teacher.policies.policies.praise_policy import PraisePolicy

from .base import TeacherPolicy

from .policies.correction import (
    CorrectionPolicy,
)

from .policies.interruption import (
    InterruptionPolicy,
)

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




register_policy(
    CorrectionPolicy(),
)

register_policy(
    InterruptionPolicy(),
)

register_policy(
    PraisePolicy(),
)