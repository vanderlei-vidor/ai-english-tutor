from __future__ import annotations

from abc import ABC, abstractmethod

from app.services.grammar_engine.models import GrammarAnalysis


class BaseSemanticRelation(ABC):
    """
    Classe base para todas as relações semânticas.
    """

    @abstractmethod
    def analyze(self, analysis: GrammarAnalysis) -> None: ...
