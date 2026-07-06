from __future__ import annotations

from app.services.grammar_engine.constants import TokenType
from app.services.grammar_engine.detectors.base import BaseDetector
from app.services.grammar_engine.models import (
    GrammarAnalysis,
    GrammarToken,
)
from app.services.grammar_engine.databases.auxiliary_database import (
    AUXILIARY_VERBS,
)
from app.services.grammar_engine.classifiers.word_classifier import classify_word


class AuxiliaryDetector(BaseDetector):
    """
    Detecta verbos auxiliares.

    Exemplos:

        have
        has
        had
        will
        is
        are
        was
        were
    """

    def detect(self, analysis: GrammarAnalysis) -> None:

        tokens = analysis.context.tokens

        subject = analysis.context.subject

        if subject is None:
            return

        for position in range(subject.position + 1, len(tokens)):
            token = tokens[position]

            classification = classify_word(token)

            if not classification.is_auxiliary:
                continue

            analysis.context.auxiliary = GrammarToken(
                text=token,
                lemma=token,
                pos=TokenType.VERB.value,
                position=position,
            )

            return
