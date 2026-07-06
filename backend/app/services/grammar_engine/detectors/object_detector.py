from __future__ import annotations

from app.services.grammar_engine.detectors.base import BaseDetector
from app.services.grammar_engine.models import (
    GrammarAnalysis,
    GrammarToken,
)
from app.services.grammar_engine.constants import TokenType
from app.services.grammar_engine.databases.pronoun_database import (
    OBJECT_PRONOUNS,
)

# Importando o classificador de palavras
from app.services.grammar_engine.classifiers.word_classifier import classify_word


class ObjectDetector(BaseDetector):
    """
    Detecta o objeto simples da frase.

    Primeira versão:
        Procura o primeiro token após o verbo.

    Futuramente será expandido para:
        • noun phrases
        • articles
        • adjectives
        • compound objects
    """

    def detect(self, analysis: GrammarAnalysis) -> None:

        verb = analysis.context.verb

        if verb is None:
            return

        # Define o ponto de partida padrão logo após o verbo
        start_position = verb.position + 1

        # Se houver um artigo detectado no contexto, pula ele também
        if analysis.context.article:
            start_position = analysis.context.article.position + 1

        tokens = analysis.context.tokens

        adverb_positions = {adv.position for adv in analysis.context.adverbs}

        # Usamos o start_position dinâmico no range
        for position in range(start_position, len(tokens)):
            if position in adverb_positions:
                continue

            token = tokens[position]

            # Classifica o token atual e ignora se for uma preposição
            classification = classify_word(token)
            if classification.is_preposition:
                continue

            analysis.context.object = GrammarToken(
                text=token,
                lemma=token,
                pos=TokenType.NOUN.value,
                position=position,
            )

            return
