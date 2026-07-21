
from __future__ import annotations

from app.services.teacher.brain.state import TeacherBrainState

from .models import TeacherResponse


class TeacherResponseBuilder:
    """
    Constrói o objeto TeacherResponse
    combinando Brain + Execution + Resposta do LLM.
    """

    def build(
        self,
        brain: TeacherBrainState,
        llm_response: dict,
    ) -> TeacherResponse:

        execution = brain.execution

        response = TeacherResponse()

        # ----------------------------
        # Teaching Execution
        # ----------------------------

        response.handler = execution.handler
        response.purpose = execution.purpose
        response.target_skill = getattr(
            execution,
            "target_skill",
            brain.planning.target_skill,
        )

        response.wait_student = execution.wait_student
        response.ask_question = execution.ask_question
        response.reveal_answer = execution.reveal_answer

        # ----------------------------
        # LLM
        # ----------------------------

        response.conversation_reply = llm_response.get(
            "conversation_reply",
            "",
        )

        response.correction = llm_response.get(
            "correction",
        )

        response.explanation_pt = llm_response.get(
            "explanation_pt",
        )

        response.example = llm_response.get(
            "example",
        )

        response.exercise = llm_response.get(
            "exercise",
        )

        response.grammar_confidence = llm_response.get(
            "grammar_confidence",
            0.0,
        )

        response.needs_correction = llm_response.get(
            "needs_correction",
            False,
        )

        response.exercise_type = llm_response.get(
            "exercise_type",
        )

        return response


teacher_response_builder = TeacherResponseBuilder()