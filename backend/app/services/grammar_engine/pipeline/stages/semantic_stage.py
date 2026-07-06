from __future__ import annotations

from app.services.grammar_engine.models import GrammarAnalysis

from app.services.grammar_engine.pipeline.base import BaseStage

from app.services.grammar_engine.semantic.engine import semantic_engine


class SemanticStage(BaseStage):
    def run(
        self,
        analysis: GrammarAnalysis,
    ) -> None:

        semantic_engine.analyze(analysis)


semantic_stage = SemanticStage()
