from __future__ import annotations

from app.services.pedagogical.base import BaseLessonPlanner

from app.services.pedagogical.planners.simple_past_planner import (
    SimplePastPlanner,
)

_PLANNERS: list[BaseLessonPlanner] = [
    SimplePastPlanner(),
]


def register(planner: BaseLessonPlanner) -> None:
    _PLANNERS.append(planner)


def get_planners() -> list[BaseLessonPlanner]:
    return _PLANNERS
