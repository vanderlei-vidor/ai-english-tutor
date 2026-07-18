from __future__ import annotations

from abc import ABC
from abc import abstractmethod


class TeachingStrategy(ABC):
    @abstractmethod
    def matches(
        self,
        state,
    ) -> bool: ...

    @abstractmethod
    def build(
        self,
        state,
        plan,
    ) -> None: ...
