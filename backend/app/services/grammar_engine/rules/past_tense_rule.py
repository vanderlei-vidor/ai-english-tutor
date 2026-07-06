from __future__ import annotations

from app.services.grammar_engine.constants import (
    MarkerCategory,
    Severity,
    Skill,
)
from app.services.grammar_engine.models import (
    GrammarAnalysis,
    GrammarError,
)
from app.services.grammar_engine.rules.base import BaseRule


# Verbos irregulares corretos no passado
IRREGULAR_PAST = {
    "went",
    "bought",
    "saw",
    "ate",
    "had",
    "did",
    "came",
    "made",
    "took",
    "gave",
    "found",
    "thought",
    "told",
    "became",
    "left",
}


class PastTenseRule(BaseRule):
    """
    Detecta uso incorreto do Present Simple
    quando existe um marcador de passado.
    """

    def evaluate(self, analysis: GrammarAnalysis) -> None:

        verb = analysis.context.verb

        if verb is None:
            return

        # Procura algum marcador de passado
        has_past_marker = any(
            marker.category == MarkerCategory.PAST
            for marker in analysis.context.markers
        )

        if not has_past_marker:
            return

        verb_text = verb.text.lower()

        # Verbos irregulares corretos
        if verb_text in IRREGULAR_PAST:
            return

        # Verbos regulares no passado
        if verb_text.endswith("ed"):
            return

        analysis.errors.append(
            GrammarError(
                skill=Skill.PAST_TENSE.value,
                confidence=0.98,
                severity=Severity.HIGH.value,
                explanation="A past time marker requires the verb in the Simple Past.",
                detected_by=self.name,
            )
        )
