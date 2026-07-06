from __future__ import annotations

from app.services.grammar_engine.semantic.base import BaseSemanticRelation

_RELATIONS: list[BaseSemanticRelation] = []


def register(relation: BaseSemanticRelation):

    _RELATIONS.append(relation)


def get_relations():

    return _RELATIONS
