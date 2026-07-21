"""
Communicative Script

Template para abordagem comunicativa:
1. Contextualizar a situação
2. Praticar comunicação
3. Dar feedback natural
4. Encorajar fluência
"""

from __future__ import annotations

from .base import TeachingScriptBase
from .models import TeachingScript, TeachingStep


class CommunicativeScript(TeachingScriptBase):
    """
    Script para estratégia comunicativa.

    Fluxo:
        1. Contextualizar em uma situação real
        2. Praticar comunicação
        3. Dar feedback natural (não apenas correção)
        4. Encorajar continuação da prática
    """

    @property
    def strategy_type(self) -> str:
        return "communicative"

    def build(self) -> TeachingScript:
        script = TeachingScript(
            name="communicative_script",
            strategy_type=self.strategy_type,
            description="Abordagem comunicativa com contexto e prática de fala",
        )

        script.steps = [
            TeachingStep(
                action="explanation",
                purpose="set_context",
            ),
            TeachingStep(
                action="question",
                purpose="practice_communication",
                ask_question=True,
                wait_student=True,
            ),
            TeachingStep(
                action="feedback",
                purpose="provide_natural_feedback",
            ),
            TeachingStep(
                action="question",
                purpose="encourage_continuation",
                ask_question=True,
            ),
            TeachingStep(
                action="finish",
                finish=True,
            ),
        ]

        return script


communicative_script = CommunicativeScript()

__all__ = [
    "CommunicativeScript",
    "communicative_script",
]
