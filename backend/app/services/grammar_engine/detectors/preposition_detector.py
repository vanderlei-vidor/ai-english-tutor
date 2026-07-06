from __future__ import annotations

from app.services.grammar_engine.detectors.base import BaseDetector
from app.services.grammar_engine.models import (
    GrammarAnalysis,
    GrammarToken,
)
from app.services.grammar_engine.constants import TokenType
from app.services.grammar_engine.classifiers.word_classifier import classify_word


class PrepositionDetector(BaseDetector):
    """
    Detecta todas as preposições da sentença.
    """

    def detect(self, analysis: GrammarAnalysis) -> None:

        tokens = analysis.context.tokens

        analysis.context.prepositions.clear()

        for position, token in enumerate(tokens):
            classification = classify_word(token)

            if not classification.is_preposition:
                continue

            analysis.context.prepositions.append(
                GrammarToken(
                    text=token,
                    lemma=token,
                    pos=TokenType.PREPOSITION.value,
                    position=position,
                )
            )
