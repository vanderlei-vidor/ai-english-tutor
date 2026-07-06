from __future__ import annotations

from app.services.grammar_engine.models import GrammarAnalysis

from app.services.grammar_engine.pipeline.stages.grammar_stage import (
    grammar_stage,
)

from app.services.grammar_engine.pipeline.stages.semantic_stage import (
    semantic_stage,
)

from app.services.grammar_engine.pipeline.stages.concept_stage import (
    concept_stage,
)

from app.services.grammar_engine.pipeline.stages.learning_stage import (
    learning_stage,
)

from app.services.grammar_engine.pipeline.stages.pedagogical_stage import (
    pedagogical_stage,
)

from app.services.grammar_engine.pipeline.stages.presentation_stage import (
    presentation_stage,
)


class AnalysisPipeline:
    """
    Executa todas as etapas da análise.

    Cada Stage possui apenas uma responsabilidade.
    """

    def run(
        self,
        analysis: GrammarAnalysis,
    ) -> None:

        grammar_stage.run(analysis)

        semantic_stage.run(analysis)

        concept_stage.run(analysis)

        learning_stage.run(analysis)

        pedagogical_stage.run(analysis)

        presentation_stage.run(analysis)


analysis_pipeline = AnalysisPipeline()
