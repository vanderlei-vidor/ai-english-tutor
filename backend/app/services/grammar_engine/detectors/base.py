from __future__ import annotations

from abc import ABC, abstractmethod

from app.services.grammar_engine.models import GrammarAnalysis


class BaseDetector(ABC):
    """
    Classe base para todos os Detectores do Grammar Engine.

    Responsabilidade:
        - Ler a frase.
        - Descobrir informações gramaticais.
        - Preencher o GrammarContext.

    NÃO deve:

        ✗ Detectar erros
        ✗ Escolher skill
        ✗ Corrigir frases
        ✗ Atualizar memória
        ✗ Calcular CEFR

    Todo detector deve apenas enriquecer o
    GrammarContext.
    """

    @property
    def name(self) -> str:
        """
        Nome amigável do detector.
        """
        return self.__class__.__name__

    @abstractmethod
    def detect(self, analysis: GrammarAnalysis) -> None:
        """
        Analisa a frase e adiciona informações
        ao GrammarContext.

        Nunca retorna valores.

        Todas as informações devem ser gravadas
        dentro de analysis.context.
        """
        raise NotImplementedError
