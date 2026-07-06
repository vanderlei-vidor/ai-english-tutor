from __future__ import annotations

from abc import ABC, abstractmethod

from app.services.grammar_engine.models import GrammarAnalysis


class BaseConceptResolver(ABC):
    @abstractmethod
    def resolve(self, analysis: GrammarAnalysis) -> None: ...
