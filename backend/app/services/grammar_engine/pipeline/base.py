from __future__ import annotations

from abc import ABC, abstractmethod

from app.services.grammar_engine.models import GrammarAnalysis


class BaseStage(ABC):
    """
    Interface base para todas as etapas da Analysis Pipeline.
    """

    @abstractmethod
    def run(
        self,
        analysis: GrammarAnalysis,
    ) -> None:
        """
        Executa a etapa da pipeline.
        """
        ...
