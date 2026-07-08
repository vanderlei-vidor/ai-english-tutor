from __future__ import annotations

from app.services.conversation.analysis import (
    ConversationAnalysis,
)

from app.services.pedagogical.analysis import (
    PedagogicalAnalysis,
)

from app.services.prompt_builder.context import (
    PromptContext,
)
from app.services.prompt_builder.static.base_prompt import (
    SYSTEM_INSTRUCTION,
)
class StaticPromptBuilder:
    def build(self):

        return SYSTEM_INSTRUCTION.strip()


static_prompt_builder = StaticPromptBuilder()

class PromptBuilder:
    """
    Constrói o PromptContext que será enviado ao LLM.
    """

    def build(
        self,
        conversation_analysis: ConversationAnalysis,
        pedagogical: PedagogicalAnalysis,
    ) -> PromptContext:

        return PromptContext(
            teacher_strategy=conversation_analysis.teacher_strategy,
            teacher_action=conversation_analysis.teacher_action,
            teacher_reason=conversation_analysis.teacher_reason,
            explanation_level=conversation_analysis.explanation_level,
            confidence=conversation_analysis.confidence,
            should_teach=conversation_analysis.should_teach,
            should_review=conversation_analysis.should_review,
            should_exercise=conversation_analysis.should_exercise,
            english_level=pedagogical.estimated_level,
            target_skill=pedagogical.target_skill,
            detected_skill=pedagogical.detected_skill,
        )


prompt_builder = PromptBuilder()
