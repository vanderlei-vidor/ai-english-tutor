from __future__ import annotations

from app.services.pedagogical.presenters.base import BaseLessonPresenter

from app.services.pedagogical.presenters.simple_past_presenter import (
    SimplePastPresenter,
)

_PRESENTERS: list[BaseLessonPresenter] = [
    SimplePastPresenter(),
]


def register(presenter: BaseLessonPresenter):

    _PRESENTERS.append(presenter)


def get_presenters():

    return _PRESENTERS
