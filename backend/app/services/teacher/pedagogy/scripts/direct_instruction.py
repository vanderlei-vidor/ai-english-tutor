"""
Direct Instruction Script

Template para ensino direto:
1. Apresentar conceito
2. Fornecer exemplos
3. Exercitar
4. Feedback
"""

from __future__ import annotations

from .base import TeachingScriptBase
from .models import TeachingScript, TeachingStep


class DirectInstructionScript(TeachingScriptBase):
    """
    Script para estratégia de instrução direta.

    Fluxo:
        1. Apresentar o conceito/regra
        2. Dar exemplos práticos
        3. Pedir ao aluno para exercitar
        4. Dar feedback
    """

    @property
    def strategy_type(self) -> str:
        return "direct_instruction"

    def build(self) -> TeachingScript:
        script = TeachingScript(
            name="direct_instruction_script",
            strategy_type=self.strategy_type,
            description="Instrução direta com apresentação, exemplos e prática",
        )

        script.steps = [
            TeachingStep(
                action="explanation",
                purpose="present_concept",
            ),
            TeachingStep(
                action="example",
                purpose="show_examples",
                use_example=True,
            ),
            TeachingStep(
                action="exercise",
                purpose="practice_exercise",
                ask_question=True,
                wait_student=True,
            ),
            TeachingStep(
                action="feedback",
                purpose="provide_feedback",
                reveal_answer=True,
            ),
            TeachingStep(
                action="finish",
                finish=True,
            ),
        ]

        return script


direct_instruction_script = DirectInstructionScript()

__all__ = [
    "DirectInstructionScript",
    "direct_instruction_script",
]
