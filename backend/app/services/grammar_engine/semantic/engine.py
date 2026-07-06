from __future__ import annotations

from app.services.grammar_engine.models import GrammarAnalysis
from app.services.grammar_engine.semantic.registry import get_relations


class SemanticEngine:
    def analyze(self, analysis: GrammarAnalysis):

        for relation in get_relations():
            relation.analyze(analysis)


semantic_engine = SemanticEngine()
