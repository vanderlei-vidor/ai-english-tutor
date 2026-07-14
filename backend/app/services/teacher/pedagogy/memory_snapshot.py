from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class PedagogicalMemorySnapshot:
    mastery: int = 0

    attempts: int = 0

    review_needed: bool = False

    exercise_needed: bool = False

    last_skill: str | None = None

    confidence: float = 1.0
