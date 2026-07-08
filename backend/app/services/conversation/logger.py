from __future__ import annotations

from app.services.conversation.analysis import (
    ConversationAnalysis,
)
from app.services import conversation


class ConversationLogger:
    """
    Responsável por exibir todas as decisões tomadas
    pelo Conversation Engine.
    """

    def analysis(
        self,
        conversation: ConversationAnalysis,
    ) -> None:

        print()
        print("======== CONVERSATION ENGINE ========")

        print(f"TEACHER ACTION:      {conversation.teacher_action}")

        print(f"TEACHER STRATEGY:    {conversation.teacher_strategy}")

        print(f"TEACHER REASON:      {conversation.teacher_reason}")
       
        print(f"CONFIDENCE:          {conversation.confidence:.2f}")
        
        print(f"SHOULD TEACH:        {conversation.should_teach}")

        print(f"SHOULD REVIEW:       {conversation.should_review}")

        print(f"SHOULD EXERCISE:     {conversation.should_exercise}")

        print(f"EXPLANATION LEVEL:   {conversation.explanation_level}")

        print("====================================")


conversation_logger = ConversationLogger()
