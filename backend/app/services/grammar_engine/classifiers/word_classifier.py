from __future__ import annotations

from dataclasses import dataclass

from app.services.grammar_engine.databases.article_database import ARTICLES
from app.services.grammar_engine.databases.adverb_database import ADVERBS
from app.services.grammar_engine.databases.auxiliary_database import AUXILIARY_VERBS
from app.services.grammar_engine.databases.pronoun_database import OBJECT_PRONOUNS
from app.services.grammar_engine.databases.verb_database import COMMON_VERBS
from app.services.grammar_engine.databases.preposition_database import (
    ALL_PREPOSITIONS,
)

@dataclass(slots=True)
class WordClassification:
    token: str

    is_known: bool = False

    is_article: bool = False
    is_auxiliary: bool = False
    is_adverb: bool = False
    is_object_pronoun: bool = False

    # Reservado para próximas fases
    is_verb: bool = False
    is_noun: bool = False
    is_preposition: bool = False
    is_modal: bool = False
    is_preposition: bool = False


def classify_word(token: str) -> WordClassification:

    token = token.lower()

    info = WordClassification(token=token)

    if token in ARTICLES:
        info.is_article = True
        info.is_known = True

    if token in AUXILIARY_VERBS:
        info.is_auxiliary = True
        info.is_known = True

    if token in ADVERBS:
        info.is_adverb = True
        info.is_known = True

    if token in OBJECT_PRONOUNS:
        info.is_object_pronoun = True
        info.is_known = True

    if token in COMMON_VERBS:
        info.is_verb = True
        info.is_known = True

    if token in ALL_PREPOSITIONS:
        info.is_preposition = True
        info.is_known = True

    return info
