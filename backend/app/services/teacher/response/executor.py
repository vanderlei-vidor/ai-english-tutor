from __future__ import annotations

from app.services.teacher.brain.state import (
    TeacherBrainState,
)


class TeacherResponseExecutor:
    """
    Executa o plano criado pelo Teacher Brain.

    Não toma decisões.

    Apenas executa o TeacherActionPlan.
    """

    def execute(
        self,
        brain: TeacherBrainState,
        response_json: dict,
    ) -> dict:

        action = brain.planning.action

        # ---------------------------------------
        # Chat
        # ---------------------------------------

        if action == "chat":
            response_json["teacher_action"] = "chat"

            response_json["exercise"] = ""

            return response_json

        # ---------------------------------------
        # Correction
        # ---------------------------------------

        if action == "correction":
            response_json["teacher_action"] = "correction"

            response_json["exercise"] = ""

            return response_json

        # ---------------------------------------
        # Exercise
        # ---------------------------------------

        if action == "exercise":
            response_json["teacher_action"] = "exercise"

            return response_json

        # ---------------------------------------
        # Question
        # ---------------------------------------

        if action == "question":
            response_json["teacher_action"] = "question"

            return response_json

        return response_json


teacher_response_executor = TeacherResponseExecutor()
