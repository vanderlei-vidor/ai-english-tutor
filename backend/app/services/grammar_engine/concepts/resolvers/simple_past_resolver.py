from __future__ import annotations

from app.services.grammar_engine.concepts.base import BaseConceptResolver
from app.services.grammar_engine.concepts.concepts_db.a2.simple_past import (
    SIMPLE_PAST,
)
from app.services.grammar_engine.constants import MarkerCategory


class SimplePastResolver(BaseConceptResolver):
    def resolve(self, analysis):

        has_past_marker = any(
            marker.category == MarkerCategory.PAST
            for marker in analysis.context.markers
        )

        if not has_past_marker:
            return

        if SIMPLE_PAST not in analysis.concepts:
            analysis.concepts.append(SIMPLE_PAST)
