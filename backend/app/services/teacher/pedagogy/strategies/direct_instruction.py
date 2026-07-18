from __future__ import annotations

from ..base import TeachingStrategy


class DirectInstructionStrategy(
    TeachingStrategy,
):
    def matches(
        self,
        state,
    ) -> bool:

        if state.lesson_phase != "correction":
            return False

        return state.student.estimated_level in (
            "A1",
            "A2",
        )

    def build(
        self,
        state,
        plan,
    ) -> None:

        # ==========================
        # Strategy
        # ==========================

        plan.strategy = "direct_instruction"

        plan.teacher_reason = state.teacher_reason

        plan.feedback_style = "encouraging"

        plan.conversation_style = "natural"

        plan.exercise_style = "none"

        plan.wait_student = True

        # ==========================
        # Explanation
        # ==========================

        plan.explanation_style = "brief"

        plan.reveal_answer = True

        plan.use_example = False

        plan.use_analogy = False

        plan.ask_question = False

        plan.scaffolding = "none"

        plan.difficulty = "normal"
