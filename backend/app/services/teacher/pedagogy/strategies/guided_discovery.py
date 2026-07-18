from __future__ import annotations

from ..base import TeachingStrategy


class GuidedDiscoveryStrategy(
    TeachingStrategy,
):
    def matches(
        self,
        state,
    ) -> bool:
        
        print(
            "LEVEL:",
            repr(state.student.estimated_level),
        )

        print(
            "PHASE:",
            repr(state.lesson_phase),
        )

        if state.lesson_phase != "correction":
            return False

        return state.student.estimated_level in (
            "B1",
            "B2",
        )

    def build(
        self,
        state,
        plan,
    ):

        plan.strategy = "guided_discovery"

        plan.teacher_reason = state.teacher_reason

        plan.feedback_style = "encouraging"

        plan.conversation_style = "interactive"

        plan.exercise_style = "guided"

        plan.explanation_style = "guided"

        plan.reveal_answer = False

        plan.ask_question = True

        plan.use_example = False

        plan.use_analogy = False

        plan.scaffolding = "medium"

        plan.difficulty = "normal"

        plan.wait_student = True
