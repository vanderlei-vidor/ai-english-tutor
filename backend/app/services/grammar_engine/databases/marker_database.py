from __future__ import annotations

from app.services.grammar_engine.constants import MarkerCategory


MARKERS = {
    # ======================================================
    # PAST
    # ======================================================
    "yesterday": MarkerCategory.PAST,
    "ago": MarkerCategory.PAST,
    "last": MarkerCategory.PAST,
    # ======================================================
    # FUTURE
    # ======================================================
    "tomorrow": MarkerCategory.FUTURE,
    "next": MarkerCategory.FUTURE,
    # ======================================================
    # FREQUENCY
    # ======================================================
    "always": MarkerCategory.FREQUENCY,
    "usually": MarkerCategory.FREQUENCY,
    "often": MarkerCategory.FREQUENCY,
    "sometimes": MarkerCategory.FREQUENCY,
    "never": MarkerCategory.FREQUENCY,
    "every": MarkerCategory.FREQUENCY,
    # ======================================================
    # PRESENT PERFECT
    # ======================================================
    "since": MarkerCategory.PERFECT,
    # ======================================================
    # DURATION
    # ======================================================
    "for": MarkerCategory.DURATION,
}
