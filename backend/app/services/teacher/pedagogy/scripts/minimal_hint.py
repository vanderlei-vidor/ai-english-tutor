"""
Minimal Hint Script

Template para abordagem de dica mínima:
1. Questionar sem revelar
2. Fornecer dica bem pequena
3. Deixar aluno resolver
4. Validar solução
"""

from __future__ import annotations

from .base import TeachingScriptBase
from .models import TeachingScript, TeachingStep


class MinimalHintScript(TeachingScriptBase):
    """
    Script para estratégia de dica mínima.

    Fluxo:
        1. Colocar a questão
        2. Fornecer dica bem pequena
        3. Deixar o aluno resolver sozinho
        4. Validar e elogiar a solução
    """

    @property
    def strategy_type(self) -> str:
        return "minimal_hint"

    def build(self) -> TeachingScript:
        script = TeachingScript(
            name="minimal_hint_script",
            strategy_type=self.strategy_type,
            description="Abordagem de dica mínima para autonomia",
        )

        script.steps = [
            TeachingStep(
                action="question",
                purpose="pose_question",
                ask_question=True,
                wait_student=True,
            ),
            TeachingStep(
                action="hint",
                purpose="provide_minimal_hint",
                use_hint=True,
            ),
            TeachingStep(
                action="question",
                purpose="student_solves",
                ask_question=True,
                wait_student=True,
            ),
            TeachingStep(
                action="feedback",
                purpose="validate_and_praise",
                reveal_answer=True,
            ),
            TeachingStep(
                action="finish",
                finish=True,
            ),
        ]

        return script


minimal_hint_script = MinimalHintScript()

__all__ = [
    "MinimalHintScript",
    "minimal_hint_script",
]
