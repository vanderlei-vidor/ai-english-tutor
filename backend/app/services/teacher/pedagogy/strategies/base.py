from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from .models import TeachingScript


class TeachingScriptBase(ABC):
    """
    Classe base para todos os roteiros pedagógicos.
    """

    @abstractmethod
    def build(
        self,
    ) -> TeachingScript: ...
