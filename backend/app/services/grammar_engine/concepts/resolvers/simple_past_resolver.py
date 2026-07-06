from __future__ import annotations

from app.services.grammar_engine.concepts.base import BaseConceptResolver
from app.services.grammar_engine.concepts.concepts_db.a2.simple_past import (
    SIMPLE_PAST,
)


class SimplePastResolver(BaseConceptResolver):
    def resolve(self, analysis):

        for error in analysis.errors:
            if error.skill == "past_tense":
                analysis.concepts.append(SIMPLE_PAST)

                return
