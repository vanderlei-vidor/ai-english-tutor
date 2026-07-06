from __future__ import annotations

from app.services.grammar_engine.constants import TokenType
from app.services.grammar_engine.detectors.base import BaseDetector
from app.services.grammar_engine.models import (
    GrammarAnalysis,
    GrammarToken,
)
from app.services.grammar_engine.utils import tokenize


class VerbDetector(BaseDetector):
    def detect(self, analysis: GrammarAnalysis) -> None:

        subject = analysis.context.subject

        if subject is None:
            return

        # Nova lógica para definir onde a busca pelo verbo deve começar
        if analysis.context.auxiliary:
            start_position = analysis.context.auxiliary.position + 1
        else:
            start_position = subject.position + 1

        tokens = tokenize(analysis.context.original_sentence)

        adverb_positions = {adv.position for adv in analysis.context.adverbs}

        # Substituímos "subject.position + 1" por "start_position"
        for position in range(start_position, len(tokens)):
            if position in adverb_positions:
                continue

            token = tokens[position]

            analysis.context.verb = GrammarToken(
                text=token,
                lemma=token,
                pos=TokenType.VERB.value,
                position=position,
            )

            return
