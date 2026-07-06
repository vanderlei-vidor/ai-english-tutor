from __future__ import annotations

from app.services.grammar_engine.utils import tokenize

from app.services.grammar_engine.models import (
    GrammarAnalysis,
    GrammarContext,
)

from app.services.grammar_engine.pipeline.analysis_pipeline import (
    analysis_pipeline,
)


class GrammarEngine:
    """
    Coração do Grammar Engine.

    Sua responsabilidade agora é apenas:

        1. Criar o objeto GrammarAnalysis
        2. Tokenizar a frase
        3. Executar a Analysis Pipeline
        4. Retornar o resultado
    """

    def analyze(self, sentence: str) -> GrammarAnalysis:

        analysis = GrammarAnalysis(context=GrammarContext(original_sentence=sentence))

        # -----------------------------------------
        # Pré-processamento
        # -----------------------------------------

        analysis.context.tokens = tokenize(sentence)

        # -----------------------------------------
        # Analysis Pipeline
        # -----------------------------------------

        analysis_pipeline.run(analysis)

        return analysis


grammar_engine = GrammarEngine()
