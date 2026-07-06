from __future__ import annotations

from app.services.grammar_engine.models import GrammarAnalysis
from app.services.grammar_engine.pipeline.base import BaseStage

from app.services.pedagogical.presentation_engine import (
    lesson_presentation_engine,
)


class PresentationStage(BaseStage):
    def run(
        self,
        analysis: GrammarAnalysis,
    ) -> None:

        lesson_presentation_engine.build(analysis)


presentation_stage = PresentationStage()
