"""
Base class for Teaching Scripts
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from .models import TeachingScript


class TeachingScriptBase(ABC):
    """
    Classe base para todos os scripts pedagógicos.

    Um script é o template de COMO executar uma estratégia.
    Cada estratégia pode ter múltiplos scripts diferentes.

    Exemplos:
        - DirectInstructionScript: aula tradicional
        - SocraticScript: questionamento socrático
        - CommunicativeScript: prática de comunicação
    """

    @property
    @abstractmethod
    def strategy_type(self) -> str:
        """Tipo de estratégia (direct_instruction, socratic, etc.)"""
        ...

    @abstractmethod
    def build(self) -> TeachingScript:
        """
        Constrói e retorna o script de ensino.
        """
        ...

    def matches(self, state) -> bool:
        """
        Verifica se este script é apropriado para o estado atual.
        Por padrão, todos os scripts são apropriados.
        Override para adicionar lógica de seleção.
        """
        return True


__all__ = [
    "TeachingScriptBase",
]
