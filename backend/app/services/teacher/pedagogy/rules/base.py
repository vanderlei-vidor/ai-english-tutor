from __future__ import annotations

from abc import ABC, abstractmethod

from app.services.teacher.brain.state import (
    TeacherBrainState,
)

from app.services.teacher.pedagogy.models import (
    ExplanationPlan,
)


class ExplanationRule(ABC):
    @abstractmethod
    def skill(self) -> str: ...

    @abstractmethod
    def apply(
        self,
        brain_state: TeacherBrainState,
        plan: ExplanationPlan,
    ) -> None: ...
