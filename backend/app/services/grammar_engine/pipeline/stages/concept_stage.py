from __future__ import annotations

from app.services.grammar_engine.models import GrammarAnalysis

from app.services.grammar_engine.pipeline.base import BaseStage

from app.services.grammar_engine.concepts.engine import concept_engine


class ConceptStage(BaseStage):
    def run(
        self,
        analysis: GrammarAnalysis,
    ) -> None:

        concept_engine.analyze(analysis)


concept_stage = ConceptStage()
