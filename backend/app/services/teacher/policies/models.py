from __future__ import annotations

from dataclasses import dataclass

from app.services.teacher.constants.interruption_levels import (
    InterruptionLevel,
)


@dataclass(slots=True)
class PolicyResult:

    should_review: bool | None = None

    should_exercise: bool | None = None

    should_continue_lesson: bool | None = None

    should_start_new_lesson: bool | None = None

    should_praise: bool | None = None

    interruption_level: InterruptionLevel | None = None

    decision_strength: int = 0

    reason: str = ""

    
