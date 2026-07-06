from __future__ import annotations

from app.services.grammar_engine.detectors.base import BaseDetector
from app.services.grammar_engine.models import (
    GrammarAnalysis,
    GrammarToken,
)
from app.services.grammar_engine.constants import TokenType
from app.services.grammar_engine.utils import tokenize
from app.services.grammar_engine.databases.adverb_database import ADVERBS
from app.services.grammar_engine.classifiers.word_classifier import classify_word


class AdverbDetector(BaseDetector):
    """
    Detecta advérbios presentes na frase.
    """

    def detect(self, analysis: GrammarAnalysis) -> None:

        tokens = tokenize(analysis.context.original_sentence)

        for position, token in enumerate(tokens):
            classification = classify_word(token)

            if not classification.is_adverb:
                continue

            analysis.context.adverbs.append(
                GrammarToken(
                    text=token,
                    lemma=token,
                    pos=TokenType.ADVERB.value,
                    position=position,
                )
            )
