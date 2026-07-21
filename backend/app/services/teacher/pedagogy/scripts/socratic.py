"""
Socratic Script

Template para método socrático:
1. Questionar superficialmente
2. Questionar profundamente
3. Guiar a contradição
4. Levar à conclusão
"""

from __future__ import annotations

from .base import TeachingScriptBase
from .models import TeachingScript, TeachingStep


class SocraticScript(TeachingScriptBase):
    """
    Script para estratégia socrática.

    Fluxo:
        1. Começar com perguntas simples
        2. Aprofundar as questões
        3. Guiar o aluno a reconhecer contradições
        4. Levar o aluno à conclusão correta
    """

    @property
    def strategy_type(self) -> str:
        return "socratic"

    def build(self) -> TeachingScript:
        script = TeachingScript(
            name="socratic_script",
            strategy_type=self.strategy_type,
            description="Método socrático com questionamento progressivo",
        )

        script.steps = [
            TeachingStep(
                action="question",
                purpose="initial_question",
                ask_question=True,
                wait_student=True,
            ),
            TeachingStep(
                action="question",
                purpose="deepen_question",
                ask_question=True,
                wait_student=True,
            ),
            TeachingStep(
                action="question",
                purpose="guide_contradiction",
                ask_question=True,
                wait_student=True,
            ),
            TeachingStep(
                action="question",
                purpose="lead_to_conclusion",
                ask_question=True,
            ),
            TeachingStep(
                action="finish",
                finish=True,
            ),
        ]

        return script


socratic_script = SocraticScript()

__all__ = [
    "SocraticScript",
    "socratic_script",
]
