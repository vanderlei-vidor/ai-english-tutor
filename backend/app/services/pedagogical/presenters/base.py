from __future__ import annotations

from abc import ABC, abstractmethod

from app.services.pedagogical.models import TeachingPlan
from app.services.pedagogical.lesson_models import TeachingLesson


class BaseLessonPresenter(ABC):
    @abstractmethod
    def present(
        self,
        plan: TeachingPlan,
    ) -> TeachingLesson: ...
