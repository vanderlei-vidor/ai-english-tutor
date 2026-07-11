from __future__ import annotations

from enum import StrEnum


class LessonPhase(StrEnum):
    CONVERSATION = "conversation"

    CORRECTION = "correction"

    EXPLANATION = "explanation"

    EXAMPLE = "example"

    EXERCISE = "exercise"

    ASSESSMENT = "assessment"

    FINISHED = "finished"
