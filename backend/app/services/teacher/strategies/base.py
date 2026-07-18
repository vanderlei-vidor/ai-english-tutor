from __future__ import annotations

from abc import ABC, abstractmethod

from app.services.teacher.brain.state import (
    TeacherBrainState,
)


from app.services.teacher.state.models import (
    TeachingState,
)


class TeacherStrategy(ABC):
    @abstractmethod
    def matches(
        self,
        state: TeachingState,
    ) -> bool: ...


    @abstractmethod
    def build(
        self,
        brain_state: TeacherBrainState,
    ) -> None: ...
