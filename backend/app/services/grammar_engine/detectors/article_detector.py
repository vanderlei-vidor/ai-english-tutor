from __future__ import annotations

from app.services.grammar_engine.detectors.base import BaseDetector
from app.services.grammar_engine.models import (
    GrammarAnalysis,
    GrammarToken,
)
from app.services.grammar_engine.constants import TokenType
from app.services.grammar_engine.databases.article_database import ARTICLES

from app.services.grammar_engine.classifiers.word_classifier import classify_word


class ArticleDetector(BaseDetector):
    """
    Detecta artigos antes do objeto.
    """

    def detect(self, analysis: GrammarAnalysis) -> None:

        verb = analysis.context.verb

        if verb is None:
            return

        tokens = analysis.context.tokens

        for position in range(verb.position + 1, len(tokens)):
            token = tokens[position]

            classification = classify_word(token)

            if not classification.is_article:
                continue

            analysis.context.article = GrammarToken(
                text=token,
                lemma=token,
                pos=TokenType.ARTICLE.value,
                position=position,
            )

            return
