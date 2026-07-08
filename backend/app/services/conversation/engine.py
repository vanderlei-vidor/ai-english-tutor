from __future__ import annotations

from app.services.conversation.analysis import (
    ConversationAnalysis,
)
from app.services.conversation.registry import (
    get_strategies,
)
from app.services.pedagogical.analysis import (
    PedagogicalAnalysis,
)
from app.services.teacher.models import (
    TeacherDecision,
)

class ConversationEngine:
    """
    Responsável por decidir como o professor
    deve conduzir a conversa.

    O Engine não contém regras pedagógicas.

    Ele apenas encontra a primeira estratégia
    capaz de lidar com a situação atual.
    """

    def analyze(
        self,
        pedagogical: PedagogicalAnalysis,
        teacher_decision: TeacherDecision,
    ) -> ConversationAnalysis:

        conversation = ConversationAnalysis()

        self._apply_teacher_decision(
            conversation,
            teacher_decision,
        )

       # strategies = get_strategies()

       # if not strategies:
       #     raise RuntimeError("No conversation strategies have been registered.")

        #for strategy in strategies:
         #   if strategy.can_apply(pedagogical):
          #      strategy.apply(
          #          conversation,
          #          pedagogical,
         #       )

        #       break

        return conversation
    
    def _apply_teacher_decision(
        self,
        conversation: ConversationAnalysis,
        teacher: TeacherDecision,
    ) -> None:

        conversation.teacher_action = teacher.teacher_action

        conversation.teacher_strategy = teacher.teacher_strategy

        conversation.teacher_reason = teacher.teacher_reason

        conversation.should_teach = teacher.should_teach

        conversation.should_review = teacher.should_review

        conversation.should_exercise = teacher.should_exercise

        conversation.explanation_level = teacher.explanation_level

        conversation.confidence = teacher.confidence


conversation_engine = ConversationEngine()
