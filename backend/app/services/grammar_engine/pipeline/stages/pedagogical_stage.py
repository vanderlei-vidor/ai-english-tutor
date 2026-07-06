from __future__ import annotations

from app.services.grammar_engine.models import GrammarAnalysis

from app.services.grammar_engine.pipeline.base import BaseStage

from app.services.pedagogical.engine import pedagogical_engine


class PedagogicalStage(BaseStage):
    def run(
        self,
        analysis: GrammarAnalysis,
    ) -> None:

        pedagogical_engine.analyze(analysis)


pedagogical_stage = PedagogicalStage()
