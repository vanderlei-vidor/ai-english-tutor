from __future__ import annotations

from app.services.teacher.strategies.base import (
    TeacherStrategy,
)

from app.services.teacher.brain.state import (
    TeacherBrainState,
)

from app.services.teacher.pedagogy.explanation_selector import (
    explanation_selector,
)

from app.services.teacher.pedagogy.models import (
    ExplanationPlan,
)


class CorrectionStrategy(TeacherStrategy):
    def matches(
        self,
        grammar,
        pedagogical,
    ):

        return grammar.has_errors

    def build(
        self,
        brain_state,
    ):

        prompt = brain_state.prompt

        if prompt is None:
            return

        plan = explanation_selector.select(
            brain_state,
        )

        self._enrich_prompt(
            brain_state,
            plan,
        )

    def _enrich_prompt(
        self,
        brain_state: TeacherBrainState,
        explanation_plan: ExplanationPlan,
    ) -> None:

        prompt = brain_state.prompt

        # =====================================================
        # Todas as instruções pedagógicas vêm das ExplanationRules
        # =====================================================

        prompt.instructions.extend(
            explanation_plan.pedagogical_instructions
        )

        # =====================================================
        # Flags pedagógicas
        # =====================================================

        if explanation_plan.use_example:

            prompt.instructions.append(
                "Give one corrected example."
            )

        if explanation_plan.ask_question:

            prompt.instructions.append(
                "Ask the student to try again before revealing the answer."
            )

        if explanation_plan.use_analogy:

            prompt.instructions.append(
                "Explain using a simple analogy."
            )
