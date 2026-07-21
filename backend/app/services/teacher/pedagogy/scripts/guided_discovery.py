"""
Guided Discovery Script

Template para descoberta guiada:
1. Questionar
2. Guiar pensamento
3. Deixar descobrir
4. Validar compreensão
"""

from __future__ import annotations

from .base import TeachingScriptBase
from .models import TeachingScript, TeachingStep


class GuidedDiscoveryScript(TeachingScriptBase):
    """
    Script para estratégia de descoberta guiada.

    Fluxo:
        1. Fazer perguntas para ativar conhecimento prévio
        2. Guiar o pensamento do aluno
        3. Deixar o aluno descobrir a regra/conceito
        4. Validar compreensão
    """

    @property
    def strategy_type(self) -> str:
        return "guided_discovery"

    def build(self) -> TeachingScript:

        script = TeachingScript(
            name="guided_discovery_script",
            strategy_type=self.strategy_type,
            description="Descoberta guiada com questionamento e orientação",
        )

        script.steps = [

            TeachingStep(
                action="question",
                purpose="activate_prior_knowledge",
                ask_question=True,
                wait_student=True,
            ),

            TeachingStep(
                action="question",
                purpose="guide_thinking",
                ask_question=True,
                wait_student=True,
                use_hint=True,
            ),

            TeachingStep(
                action="feedback",
                purpose="encourage_discovery",
                wait_student=True,
            ),

            TeachingStep(
                action="question",
                purpose="validate_understanding",
                ask_question=True,
            ),

            TeachingStep(
                action="finish",
                finish=True,
            ),

        ]

        return script


guided_discovery_script = GuidedDiscoveryScript()

__all__ = [
    "GuidedDiscoveryScript",
    "guided_discovery_script",
]
