from __future__ import annotations

from app.services.grammar_engine.models import GrammarAnalysis
from app.services.grammar_engine.concepts.registry import get_resolvers


class ConceptEngine:
    def analyze(self, analysis: GrammarAnalysis):

        for resolver in get_resolvers():
            resolver.resolve(analysis)


concept_engine = ConceptEngine()
