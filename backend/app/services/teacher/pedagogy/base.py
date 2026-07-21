from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from .models import (
    TeachingStrategyPlan,
)


class TeachingStrategy(ABC):
    """
    Classe base para todas as estratégias pedagógicas.

    Cada estratégia decide:

    - quando pode ser utilizada
    - como preencher o TeachingStrategyPlan
    """

    @abstractmethod
    def matches(
        self,
        state,
    ) -> bool:
        """
        Retorna True caso esta estratégia seja apropriada
        para o estado atual do professor.
        """
        ...

    @abstractmethod
    def build(
        self,
        state,
        plan: TeachingStrategyPlan,
    ) -> None:
        """
        Preenche o plano pedagógico.
        """
        ...
