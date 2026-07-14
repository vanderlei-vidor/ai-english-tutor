from __future__ import annotations

from app.services.teacher.brain.state import (
    TeacherBrainState,
)

from .memory_provider import (
    pedagogical_memory_provider,
)

from .models import (
    ExplanationPlan,
)
from .rules.registry import (
    explanation_rule_registry,
)

# Limiar de domínio considerado baixo para acionar exemplos automáticos
_LOW_MASTERY_THRESHOLD = 20


class ExplanationSelector:
    def select(
        self,
        brain_state: TeacherBrainState,
    ) -> ExplanationPlan:

        # PASSO 1: Carrega o histórico/memória do aluno usando o brain_state
        memory = pedagogical_memory_provider.load(
            brain_state,
        )

        plan = ExplanationPlan()

        # Fluxo de Inteligência Pedagógica (em ordem de aplicação de regras)
        self._apply_mastery_rules(
            plan,
            memory,
        )

        self._apply_review_rules(
            plan,
            memory,
        )

        self._apply_level_rules(
            plan,
            memory,
        )

        self._apply_skill_rules(
            brain_state,
            plan,
        )

        return plan

    def _apply_mastery_rules(
        self,
        plan: ExplanationPlan,
        memory,
    ) -> None:

        if memory.mastery < _LOW_MASTERY_THRESHOLD:
            plan.use_example = True

    def _apply_review_rules(
        self,
        plan: ExplanationPlan,
        memory,
    ) -> None:
        """Aplica regras baseadas na necessidade de revisão de conteúdos antigos."""
        pass

    def _apply_level_rules(
        self,
        plan: ExplanationPlan,
        memory,
    ) -> None:
        """Aplica regras baseadas no nível de proficiência geral do aluno (A1, B2, etc)."""
        pass

    def _apply_skill_rules(
        self,
        brain_state: TeacherBrainState,
        plan: ExplanationPlan,
    ) -> None:

        rule = explanation_rule_registry.get(
            brain_state.planning.target_skill,
        )

        if rule:
            rule.apply(
                brain_state,
                plan,
            )


explanation_selector = ExplanationSelector()
