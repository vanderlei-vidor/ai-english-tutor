from __future__ import annotations

from .models import (
    TeacherPerception,
    TeacherReflection,
    TeacherActionPlan,
)
from app.services.teacher.constants.interruption_levels import (
    InterruptionLevel,
)
from app.services.teacher.state.models import (
    TeachingState,
)

class TeacherPlanningEngine:
    def plan(
        self,
        perception: TeacherPerception,
        reflection: TeacherReflection,
        state: TeachingState,
    ) -> TeacherActionPlan:

        plan = TeacherActionPlan()

        if (
            reflection.interruption_level
            is InterruptionLevel.HIGH
        ):

            self._apply_teaching_plan(
                plan,
                perception,
                reflection,
                state,
            )

        elif reflection.should_praise:

            self._apply_praise_plan(
                plan,
                perception,
                reflection,
                state,
            )

        else:

            self._apply_conversation_plan(
                plan,
                perception,
                reflection,
                state,
            )

        self._sync_state(
            state,
            plan,
        )   

        return plan
    # ==========================================================
    # Teaching
    # ==========================================================

    def _apply_teaching_plan(
        self,
        plan: TeacherActionPlan,
        perception: TeacherPerception,
        reflection: TeacherReflection,
        state: TeachingState,
    ) -> None:

        plan.goal = "teach"

        plan.lesson_type = "grammar"

        plan.phase = "correction"

        plan.next_step = "correction"

        plan.target_skill = (
            state.skill_focus.detected
        )

        state.skill_focus.teaching = (
            plan.target_skill
        )

        plan.explanation_level = "normal"

        plan.requires_exercise = False

        plan.requires_review = False

        plan.teaching_priority = 100

        plan.interruption_level = InterruptionLevel.HIGH

        plan.conversation_policy = "pause"

        plan.review_policy = "none"

        plan.exercise_policy = "none"

        plan.expected_turns = 5

        plan.completion_condition = "student_understands_correction"

        plan.teacher_reason = reflection.teaching_reason

        plan.should_teach = True

        plan.should_review = False

        plan.should_exercise = False

        plan.confidence = 1.0

        self._apply_response_decision(
            plan,
            phase=plan.phase,
        )

    # ==========================================================
    # Conversation
    # ==========================================================

    def _apply_conversation_plan(
        self,
        plan: TeacherActionPlan,
        perception: TeacherPerception,
        reflection: TeacherReflection,
        state: TeachingState,
    ) -> None:

        plan.goal = "conversation"

        plan.lesson_type = "conversation"

        plan.phase = "conversation"

        plan.next_step = "chat"

        plan.target_skill = state.target_skill

        plan.teaching_priority = 10

        plan.interruption_level = InterruptionLevel.LOW

        plan.conversation_policy = "continue"

        plan.explanation_level = "normal"

        plan.requires_exercise = False

        plan.requires_review = False

        plan.review_policy = "none"

        plan.exercise_policy = "none"

        plan.expected_turns = 1

        plan.completion_condition = ""

        plan.teacher_reason = reflection.teaching_reason

        plan.should_teach = False

        plan.should_review = False

        plan.should_exercise = False

        plan.confidence = 1.0

        self._apply_response_decision(
            plan,
            phase=plan.phase,
        )

    # ==========================================================
    # Lesson
    # ==========================================================

    def apply_lesson_phase(
        self,
        plan: TeacherActionPlan,
        lesson,
    ) -> TeacherActionPlan:

        phase = self._phase_value(
            lesson.current_phase,
        )

        plan.phase = phase

        self._apply_response_decision(
            plan,
            phase=phase,
        )

        return plan

    # ==========================================================
    # Response
    # ==========================================================

    def _apply_response_decision(
        self,
        plan: TeacherActionPlan,
        phase: str,
    ) -> None:

        plan.generate_example = False

        plan.generate_exercise = False

        plan.ask_question = False

        plan.wait_for_student = True

        plan.finish_lesson = False

        match phase:
            case "correction":
                plan.teaching_mode = "correct"

                plan.action = "correction"

                plan.response_style = "natural"

                plan.tone = "friendly"

                plan.explanation_level = "short"

            case "explanation":
                plan.teaching_mode = "teach"

                plan.action = "explanation"

                plan.response_style = "teacher"

                plan.tone = "friendly"

                plan.explanation_level = "normal"

                plan.ask_question = True

            case "example":
                plan.teaching_mode = "teach"

                plan.action = "example"

                plan.response_style = "teacher"

                plan.tone = "friendly"

                plan.generate_example = True

            case "exercise":
                plan.teaching_mode = "coach"

                plan.action = "exercise"

                plan.response_style = "teacher"

                plan.tone = "friendly"

                plan.generate_exercise = True

                plan.ask_question = True

            case "assessment":
                plan.teaching_mode = "evaluate"

                plan.action = "assessment"

                plan.response_style = "teacher"

                plan.tone = "friendly"

                plan.ask_question = True

                plan.finish_lesson = True

            case "finished":
                plan.teaching_mode = "conversation"

                plan.action = "chat"

                plan.response_style = "natural"

                plan.tone = "friendly"

                plan.finish_lesson = True

            case "praise":

                plan.teaching_mode = "conversation"

                plan.action = "praise"

                plan.response_style = "natural"

                plan.tone = "friendly"

                plan.explanation_level = "normal"

            case _:
                plan.teaching_mode = "conversation"

                plan.action = "chat"

                plan.response_style = "natural"

                plan.tone = "friendly"

                plan.explanation_level = "normal"

            

        plan.teacher_strategy = plan.teaching_mode

        plan.teacher_action = plan.action

        plan.should_teach = plan.goal == "teach"

        plan.should_review = plan.requires_review

        plan.should_exercise = plan.generate_exercise

    def _phase_value(
        self,
        phase,
    ) -> str:

        return getattr(
            phase,
            "value",
            phase,
        )
    

    def _apply_praise_plan(
        self,
        plan: TeacherActionPlan,
        perception: TeacherPerception,
        reflection: TeacherReflection,
        state: TeachingState,
    ) -> None:

        plan.goal = "conversation"

        plan.lesson_type = "conversation"

        plan.phase = "praise"

        plan.next_step = "praise"

        plan.target_skill = perception.target_skill

        plan.teaching_priority = 20

        plan.interruption_level = (
            InterruptionLevel.NONE
        )

        plan.conversation_policy = "continue"

        plan.teacher_reason = (
            reflection.teaching_reason
        )

        plan.celebrate_success = True

        plan.should_teach = False

        plan.should_review = False

        plan.should_exercise = False

        plan.confidence = 1.0

        self._apply_response_decision(
            plan,
            phase=plan.phase,
        )


    def _sync_state(
        self,
        state: TeachingState,
        plan: TeacherActionPlan,
    ) -> None:

        state.teacher_action = plan.action

        state.teacher_mode = plan.teaching_mode

        state.teacher_reason = plan.teacher_reason

        state.response_style = plan.response_style

        state.tone = plan.tone

        state.lesson_goal = plan.goal

        state.lesson_phase = plan.phase

teacher_planning_engine = TeacherPlanningEngine()
