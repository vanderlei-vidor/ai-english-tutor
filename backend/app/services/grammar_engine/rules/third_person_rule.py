from __future__ import annotations

from app.services.grammar_engine.models import (
    GrammarAnalysis,
    GrammarError,
)
from app.services.grammar_engine.rules.base import BaseRule
from app.services.grammar_engine.constants import (
    Skill,
    Severity,
)


THIRD_PERSON_SUBJECTS = {
    "he",
    "she",
    "it",
}


class ThirdPersonRule(BaseRule):
    """
    Detecta erro de terceira pessoa do singular.

    Exemplos:

        ❌ She work every day.
        ✅ She works every day.

        ❌ He like pizza.
        ✅ He likes pizza.
    """

    def evaluate(self, analysis: GrammarAnalysis) -> None:

        subject = analysis.context.subject
        verb = analysis.context.verb

        auxiliary = analysis.context.auxiliary

        if auxiliary is not None:
            return

        if subject is None or verb is None:
            return

        if subject.text.lower() not in THIRD_PERSON_SUBJECTS:
            return

        verb_text = verb.text.lower()

        # Verbos auxiliares válidos
        if verb_text in {
            "is",
            "has",
            "does",
            "was",
        }:
            return

        # Já está flexionado corretamente
        if verb_text.endswith("s") or verb_text.endswith("es"):
            return

        analysis.errors.append(
            GrammarError(
                skill=Skill.THIRD_PERSON.value,
                confidence=0.98,
                severity=Severity.HIGH.value,
                explanation="Third person singular verbs require -s or -es.",
                detected_by=self.name,
            )
        )
