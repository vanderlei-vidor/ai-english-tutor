from __future__ import annotations

from app.services.grammar_engine.concepts.base import BaseConceptResolver

_RESOLVERS: list[BaseConceptResolver] = []


def register(resolver: BaseConceptResolver):

    _RESOLVERS.append(resolver)


def get_resolvers():

    return _RESOLVERS
from app.services.grammar_engine.concepts.resolvers.simple_past_resolver import (
    SimplePastResolver,
)

_RESOLVERS = [
    SimplePastResolver(),
]