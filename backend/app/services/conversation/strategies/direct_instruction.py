from __future__ import annotations

from app.services.conversation.analysis import (
    ConversationAnalysis,
)
from app.services.conversation.base_strategy import (
    BaseConversationStrategy,
)
from app.services.pedagogical.analysis import (
    PedagogicalAnalysis,
)


class DirectInstructionStrategy(BaseConversationStrategy):
    """
    Estratégia clássica de ensino.

    O professor explica diretamente o conceito,
    mostra exemplos e, quando necessário,
    propõe um exercício.

    Esta será a estratégia padrão do sistema
    durante as primeiras fases.
    """
    @property
    def priority(self) -> int:
        return 10
    
    
    @property
    def name(self) -> str:
        return "direct_instruction"

    def can_apply(
        self,
        pedagogical: PedagogicalAnalysis,
    ) -> bool:
        """
        Nesta primeira versão ela sempre pode ser utilizada.

        Futuramente outras estratégias poderão ter prioridade.
        """
        return True

    def apply(
        self,
        conversation: ConversationAnalysis,
        pedagogical: PedagogicalAnalysis,
    ) -> None:

        conversation.teacher_strategy = self.name

        # --------------------------------------------------
        # Escolha da ação do professor
        # --------------------------------------------------

        if pedagogical.needs_correction:

            conversation.teacher_action = "correction"

            conversation.teacher_reason = (
                "Student produced a grammatical error."
            )

        elif pedagogical.backend_wants_teaching:

            conversation.teacher_action = "lesson"

            conversation.teacher_reason = (
                "Backend requested a teaching opportunity."
            )

        elif pedagogical.exercise_required:

            conversation.teacher_action = "exercise"

            conversation.teacher_reason = (
                "Practice is required."
            )

        else:

            conversation.teacher_action = "chat"

            conversation.teacher_reason = (
                "Natural conversation."
            )

        # --------------------------------------------------
        # Teaching Decisions
        # --------------------------------------------------

        conversation.should_teach = (
            conversation.teacher_action
            in (
                "correction",
                "lesson",
            )
        )

        conversation.should_exercise = (
            conversation.teacher_action
            == "exercise"
        )

        conversation.should_review = False

        # --------------------------------------------------
        # Explanation
        # --------------------------------------------------

        if pedagogical.had_error:

            conversation.explanation_level = "detailed"

        else:

            conversation.explanation_level = "normal"