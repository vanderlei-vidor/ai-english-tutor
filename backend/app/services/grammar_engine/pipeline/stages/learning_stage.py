from __future__ import annotations

from app.services.grammar_engine.models import GrammarAnalysis
from app.services.grammar_engine.pipeline.base import BaseStage


class LearningStage(BaseStage):
    """
    Placeholder da camada de aprendizagem.

    Futuramente será responsável por:

    - recuperar o LearningProfile
    - atualizar progresso
    - recalcular mastery
    - atualizar revisões
    """

    def run(
        self,
        analysis: GrammarAnalysis,
    ) -> None:

        # Ainda não implementado.
        pass


learning_stage = LearningStage()
