from __future__ import annotations

from .models import TeacherResponse


class TeacherResponseSerializer:
    """
    Serializa TeacherResponse
    para o formato JSON enviado ao Flutter.
    """

    def serialize(
        self,
        response: TeacherResponse,
    ) -> dict:

        return {
            # Nova arquitetura
            "teacher_handler": response.handler,
            "teacher_purpose": response.purpose,
            "wait_student": response.wait_student,
            "ask_question": response.ask_question,
            "reveal_answer": response.reveal_answer,
            # Compatibilidade temporária
            "teacher_action": response.handler,
            # Conteúdo
            "target_skill": response.target_skill,
            "conversation_reply": response.conversation_reply,
            "correction": response.correction,
            "explanation_pt": response.explanation_pt,
            "example": response.example,
            "exercise": response.exercise,
            "exercise_type": response.exercise_type,
            "grammar_confidence": response.grammar_confidence,
            "needs_correction": response.needs_correction,
        }


teacher_response_serializer = TeacherResponseSerializer()
