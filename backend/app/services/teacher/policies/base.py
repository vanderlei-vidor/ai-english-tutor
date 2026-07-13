from __future__ import annotations

from abc import ABC
from abc import abstractmethod


class TeacherPolicy(ABC):
    @property
    def priority(self) -> int:
        return 100

    @abstractmethod
    def evaluate(
        self,
        perception,
        lesson,
    ):
        """
        Avalia apenas UMA decisão pedagógica.

        Nunca modifica objetos.

        Apenas retorna um resultado.
        """
        raise NotImplementedError
