from __future__ import annotations

from app.services.conversation.analysis import (
    ConversationAnalysis,
)
from app.services.pedagogical.analysis import (
    PedagogicalAnalysis,
)


class TeacherDecision:
    """
    Responsável por decidir a ação do professor.

    Esta classe concentra as regras de decisão
    utilizadas pelas estratégias de conversa.
    """

    def decide(
        self,
        conversation: ConversationAnalysis,
        pedagogical: PedagogicalAnalysis,
    ) -> None:

        if pedagogical.needs_correction:
            conversation.teacher_action = "correction"

            conversation.teacher_reason = "Student produced a grammatical error."

            return

        if pedagogical.backend_wants_teaching:
            conversation.teacher_action = "lesson"

            conversation.teacher_reason = "Teaching opportunity detected."

            return

        if pedagogical.exercise_required:
            conversation.teacher_action = "exercise"

            conversation.teacher_reason = "Practice is required."

            return

        conversation.teacher_action = "chat"

        conversation.teacher_reason = "Natural conversation."


teacher_decision = TeacherDecision()
