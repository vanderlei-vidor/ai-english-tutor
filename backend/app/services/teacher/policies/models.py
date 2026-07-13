from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class PolicyResult:
    should_interrupt: bool | None = None

    should_review: bool | None = None

    should_exercise: bool | None = None

    should_continue_lesson: bool | None = None

    should_start_new_lesson: bool | None = None

    interruption_level: str | None = None

    decision_strength: int = 0

    reason: str = ""