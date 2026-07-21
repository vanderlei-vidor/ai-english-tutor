"""
Teaching Strategies - Base and Implementations

Uma estratégia pedagógica define:
1. Quando pode ser usada (matches)
2. Como preencher o TeachingStrategyPlan (build)

Cada estratégia será associada a um script pedagógico correspondente.
"""

from __future__ import annotations

from ..base import TeachingStrategy
from ..models import TeachingStrategyPlan


class DirectInstructionStrategy(TeachingStrategy):
    """
    Estratégia de Instrução Direta.

    Apropriada para:
    - Conceitos complexos
    - Alunos com baixo engajamento
    - Tempo limitado
    """

    def matches(self, state) -> bool:
        """
        Retorna True se instrução direta é apropriada.
        """
        # Conceitos complexos justificam instrução direta
        if getattr(state, "detected_skill", None) is not None:
            return True

        # Alunos com baixo engajamento precisam de instrução clara
        if hasattr(state, "student") and state.student:
            return True

        return False

    def build(self, state, plan: TeachingStrategyPlan) -> None:
        """
        Preenche o plano com parâmetros de instrução direta.
        """
        plan.explanation_style = "direct"
        plan.reveal_answer = True
        plan.use_example = True
        plan.ask_question = False
        plan.scaffolding = "low"
        plan.feedback_style = "corrective"
        plan.exercise_style = "guided_practice"
        plan.teacher_reason = "Instrução direta para conceito complexo"


class GuidedDiscoveryStrategy(TeachingStrategy):
    """
    Estratégia de Descoberta Guiada.

    Apropriada para:
    - Alunos engajados
    - Aprendizado novo e desafiador
    - Promover pensamento crítico
    """

    def matches(self, state) -> bool:
        """
        Retorna True se descoberta guiada é apropriada.
        """
        # Para descoberta guiada, aluno precisa estar engajado com o skill
        if getattr(state, "has_error", False) and getattr(
            state, "detected_skill", None
        ):
            return True

        # Aprendizado novo em contexto ativo justifica descoberta guiada
        if getattr(state, "lesson_active", False) and getattr(
            state, "skill_focus", None
        ):
            return True

        return False

    def build(self, state, plan: TeachingStrategyPlan) -> None:
        """
        Preenche o plano com parâmetros de descoberta guiada.
        """
        plan.explanation_style = "questioning"
        plan.reveal_answer = False
        plan.use_example = True
        plan.ask_question = True
        plan.scaffolding = "high"
        plan.feedback_style = "encouraging"
        plan.exercise_style = "exploration"
        plan.teacher_reason = "Descoberta guiada para aluno engajado"


class SocraticStrategy(TeachingStrategy):
    """
    Estratégia Socrática.

    Apropriada para:
    - Consolidação de conhecimento
    - Pensamento crítico
    - Alunos avançados
    """

    def matches(self, state) -> bool:
        """
        Retorna True se método socrático é apropriado.
        """
        # Consolidação de conhecimento se beneficia do socrático
        if getattr(state, "lesson_phase", "") == "consolidation":
            return True

        # Alunos com muitos erros resolvidos podem lidar com questionamento profundo
        if (
            hasattr(state, "memory_data")
            and state.memory_data.get("mastery_level", 0) > 0.7
        ):
            return True

        return False

    def build(self, state, plan: TeachingStrategyPlan) -> None:
        """
        Preenche o plano com parâmetros do método socrático.
        """
        plan.explanation_style = "questioning"
        plan.reveal_answer = False
        plan.use_example = False
        plan.ask_question = True
        plan.scaffolding = "minimal"
        plan.feedback_style = "reflective"
        plan.exercise_style = "socratic_dialogue"
        plan.teacher_reason = "Método socrático para pensamento crítico"


class MinimalHintStrategy(TeachingStrategy):
    """
    Estratégia de Dica Mínima.

    Apropriada para:
    - Alunos autônomos
    - Práticas de reforço
    - Consolidação leve
    """

    def matches(self, state) -> bool:
        """
        Retorna True se dica mínima é apropriada.
        """
        # Alunos autônomos se beneficiam de dicas mínimas
        if hasattr(state, "memory_data") and state.memory_data.get("autonomous", False):
            return True

        # Consolidação leve pode usar dicas mínimas
        if getattr(state, "lesson_phase", "") == "review":
            return True

        return False

    def build(self, state, plan: TeachingStrategyPlan) -> None:
        """
        Preenche o plano com parâmetros de dica mínima.
        """
        plan.explanation_style = "minimal"
        plan.reveal_answer = False
        plan.use_example = False
        plan.ask_question = True
        plan.scaffolding = "minimal"
        plan.feedback_style = "affirmative"
        plan.exercise_style = "independent_practice"
        plan.teacher_reason = "Dica mínima para aluno autônomo"


class CommunicativeStrategy(TeachingStrategy):
    """
    Estratégia Comunicativa.

    Apropriada para:
    - Prática de comunicação e fala
    - Interação natural
    - Fluidez

    Nota: Esta é a estratégia de fallback
    """

    def matches(self, state) -> bool:
        """
        Retorna True se abordagem comunicativa é apropriada.
        Sempre pode ser usada como fallback.
        """
        # Prática de fala justifica abordagem comunicativa
        if getattr(state, "lesson_goal", "") == "conversation":
            return True

        # Prática geral também pode usar comunicativa
        return False

    def build(self, state, plan: TeachingStrategyPlan) -> None:
        """
        Preenche o plano com parâmetros de abordagem comunicativa.
        """
        plan.explanation_style = "contextual"
        plan.reveal_answer = False
        plan.use_example = True
        plan.ask_question = True
        plan.scaffolding = "medium"
        plan.feedback_style = "natural"
        plan.conversation_style = "dialogue"
        plan.exercise_style = "communicative_practice"
        plan.teacher_reason = "Abordagem comunicativa para prática natural"


__all__ = [
    "DirectInstructionStrategy",
    "GuidedDiscoveryStrategy",
    "SocraticStrategy",
    "MinimalHintStrategy",
    "CommunicativeStrategy",
]
