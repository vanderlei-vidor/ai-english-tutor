from __future__ import annotations

from .models import (
    TeacherPerception,
    TeacherReflection,
    TeacherActionPlan,
)


class TeacherPlanningEngine:
    def plan(
        self,
        perception: TeacherPerception,
        reflection: TeacherReflection,
    ) -> TeacherActionPlan:

        plan = TeacherActionPlan()

        if reflection.interruption_level == "high":
            
            self._apply_teaching_plan(
                plan,
                perception,
                reflection,
            )

        else:
            self._apply_conversation_plan(
                plan,
                perception,
                reflection,
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
    ) -> None:

        plan.goal = "teach"

        plan.lesson_type = "grammar"

        plan.phase = "correction"

        plan.next_step = "correction"

        plan.target_skill = perception.detected_skill

        plan.explanation_level = "normal"

        plan.requires_exercise = False

        plan.requires_review = False

        plan.teaching_priority = 100

        plan.interruption_level = "high"

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
    ) -> None:

        plan.goal = "conversation"

        plan.lesson_type = "conversation"

        plan.phase = "conversation"

        plan.next_step = "chat"

        plan.target_skill = perception.target_skill

        plan.teaching_priority = 10

        plan.interruption_level = "low"

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


teacher_planning_engine = TeacherPlanningEngine()
