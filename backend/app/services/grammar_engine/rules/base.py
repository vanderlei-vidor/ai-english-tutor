from __future__ import annotations

from abc import ABC, abstractmethod

from app.services.grammar_engine.models import GrammarAnalysis


class BaseRule(ABC):
    """
    Classe base para todas as regras gramaticais.

    Responsabilidade:

        - Ler o GrammarContext preenchido pelos Detectores.
        - Identificar erros gramaticais.
        - Adicionar GrammarError ao GrammarAnalysis.

    NÃO deve:

        ✗ Detectar sujeito
        ✗ Detectar verbos
        ✗ Fazer parsing da frase
        ✗ Atualizar memória
        ✗ Escolher a skill principal

    As Rules apenas interpretam o GrammarContext.
    """

    @property
    def name(self) -> str:
        """
        Nome amigável da Rule.
        """
        return self.__class__.__name__

    @abstractmethod
    def evaluate(self, analysis: GrammarAnalysis) -> None:
        """
        Avalia o GrammarContext e adiciona
        GrammarError(s), quando necessário.

        Nunca retorna valores.

        As alterações devem ser feitas diretamente
        dentro do objeto GrammarAnalysis.
        """
        raise NotImplementedError
