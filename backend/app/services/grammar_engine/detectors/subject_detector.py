from __future__ import annotations

from app.services.grammar_engine.constants import TokenType
from app.services.grammar_engine.detectors.base import BaseDetector
from app.services.grammar_engine.models import (
    GrammarAnalysis,
    GrammarToken,
)
from app.services.grammar_engine.utils import tokenize


SUBJECT_PRONOUNS = {
    "i",
    "you",
    "he",
    "she",
    "it",
    "we",
    "they",
}


class SubjectDetector(BaseDetector):
    """
    Detecta o sujeito principal da frase.

    Versão 1:

    ✔ Pronomes pessoais.

    Futuramente:

    ✔ Nomes próprios
    ✔ Noun Phrases
    ✔ Sujeitos compostos
    ✔ There is / There are
    """

    def detect(self, analysis: GrammarAnalysis) -> None:

        tokens = tokenize(analysis.context.original_sentence)

        if not tokens:
            return

        first = tokens[0]

        if first not in SUBJECT_PRONOUNS:
            return

        analysis.context.subject = GrammarToken(
            text=first,
            lemma=first,
            pos=TokenType.PRONOUN.value,
            position=0,
        )
