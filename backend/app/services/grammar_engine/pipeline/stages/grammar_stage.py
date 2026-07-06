from __future__ import annotations

from app.services.grammar_engine.models import GrammarAnalysis

from app.services.grammar_engine.pipeline.base import BaseStage

from app.services.grammar_engine.registry import (
    get_detectors,
    get_rules,
    get_analyzers,
)


class GrammarStage(BaseStage):
    """
    Executa toda a análise gramatical.

    Responsável por:

    • Detectores
    • Rules
    • Analyzers
    """

    def run(
        self,
        analysis: GrammarAnalysis,
    ) -> None:

        # -----------------------------
        # Detectores
        # -----------------------------

        for detector in get_detectors():
            detector.detect(analysis)

        # -----------------------------
        # Rules
        # -----------------------------

        for rule in get_rules():
            rule.evaluate(analysis)

        # -----------------------------
        # Analyzers
        # -----------------------------

        for analyzer in get_analyzers():
            analyzer.analyze(analysis)


grammar_stage = GrammarStage()
