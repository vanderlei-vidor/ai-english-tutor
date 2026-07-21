from __future__ import annotations


class CorrectionPurposeBuilder:
    """
    Produz instruções de correção concretas baseadas na skill alvo.
    """

    _SKILL_CORRECTIONS: dict[str, str] = {
        "past_tense": (
            "The student used a present verb with a past time marker. "
            "Correct the verb tense and briefly explain why the past form is needed."
        ),
        "verb_usage": (
            "The student used the wrong verb collocation. "
            "Show the correct verb and explain the natural usage."
        ),
        "third_person": (
            "The student made a third-person agreement error. "
            "Correct the verb form and mention the -s / doesn't rule."
        ),
        "articles": (
            "The student missed or misused an article. "
            "Correct the sentence and explain a/an/the usage briefly."
        ),
        "prepositions": (
            "The student used the wrong preposition. "
            "Correct the collocation and give one simple example."
        ),
        "nouns": (
            "The student misused a countable/uncountable noun. "
            "Correct the form and explain why."
        ),
    }

    def build(
        self,
        target_skill: str | None = None,
    ) -> str:
        if target_skill and target_skill in self._SKILL_CORRECTIONS:
            return self._SKILL_CORRECTIONS[target_skill]

        return (
            "Correct the student's mistake clearly. "
            "Explain briefly in Portuguese why the correction is needed."
        )
