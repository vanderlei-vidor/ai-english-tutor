from __future__ import annotations

from .past_tense import (
    PastTenseRule,
)
from .articles import (
    ArticlesRule,
)

from .prepositions import (
    PrepositionsRule,
)

from .third_person import (
    ThirdPersonRule,
)

class ExplanationRuleRegistry:
    def __init__(self):

        self.rules = {
            "past_tense": PastTenseRule(),
            "articles": ArticlesRule(),
            "prepositions": PrepositionsRule(),
            "third_person": ThirdPersonRule(),
        }



    def get(
        self,
        skill: str,
    ):

        return self.rules.get(skill)


explanation_rule_registry = ExplanationRuleRegistry()
