from __future__ import annotations

from app.services.grammar_engine.constants import MarkerCategory
from app.services.grammar_engine.detectors.base import BaseDetector
from app.services.grammar_engine.models import (
    GrammarAnalysis,
    GrammarMarker,
)
from app.services.grammar_engine.utils import tokenize


# ==========================================================
# MARKER DATABASE
# ==========================================================

MARKERS = {
    # ---------- PAST ----------
    "yesterday": MarkerCategory.PAST,
    "ago": MarkerCategory.PAST,
    "last": MarkerCategory.PAST,
    # ---------- FUTURE ----------
    "tomorrow": MarkerCategory.FUTURE,
    "next": MarkerCategory.FUTURE,
    # ---------- FREQUENCY ----------
    "always": MarkerCategory.FREQUENCY,
    "usually": MarkerCategory.FREQUENCY,
    "often": MarkerCategory.FREQUENCY,
    "sometimes": MarkerCategory.FREQUENCY,
    "never": MarkerCategory.FREQUENCY,
    "every": MarkerCategory.FREQUENCY,
    # ---------- PERFECT ----------
    "since": MarkerCategory.PERFECT,
    # ---------- DURATION ----------
    "for": MarkerCategory.DURATION,
}


class MarkerDetector(BaseDetector):
    """
    Detecta marcadores linguísticos presentes na frase.

    Exemplo:

        yesterday
        tomorrow
        always
        since
        for
        every
    """

    def detect(self, analysis: GrammarAnalysis) -> None:

        tokens = tokenize(analysis.context.original_sentence)

        for token in tokens:
            category = MARKERS.get(token)

            if category is None:
                continue

            analysis.context.markers.append(
                GrammarMarker(
                    name=f"{category.value.upper()}_MARKER",
                    value=token,
                    category=category,
                )
            )
