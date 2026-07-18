from __future__ import annotations

from ..base import TeachingStrategy


class CommunicativeStrategy(
    TeachingStrategy,
):
    def matches(
        self,
        state,
    ) -> bool:

        return state.lesson_phase in (
            "conversation",
            "praise",
        )

    def build(
        self,
        state,
        plan,
    ) -> None:

        # ==========================
        # Strategy
        # ==========================

        plan.strategy = "communicative"

        plan.teacher_reason = state.teacher_reason

        plan.feedback_style = "encouraging"

        plan.conversation_style = "natural"

        plan.exercise_style = "none"

        plan.wait_student = True

        # ==========================
        # Explanation
        # ==========================

        plan.explanation_style = "none"

        plan.reveal_answer = False

        plan.use_example = False

        plan.use_analogy = False

        plan.ask_question = False

        plan.scaffolding = "none"

        plan.difficulty = "normal"
