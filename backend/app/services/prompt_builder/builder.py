from __future__ import annotations


from app.services.pedagogical.analysis import (
    PedagogicalAnalysis,
)

from app.services.prompt_builder.context import (
    PromptContext,
)
from app.services.teacher.brain.state import (
    TeacherBrainState,
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
        brain: TeacherBrainState,
        pedagogical: PedagogicalAnalysis,
    ) -> PromptContext:

        action_plan = brain.planning
        execution = brain.execution

        return PromptContext(
            teacher_strategy=action_plan.teaching_mode,
            teacher_action=action_plan.action,
            teacher_handler=execution.handler,
            teacher_purpose=execution.purpose,
            teacher_reason=action_plan.teacher_reason,
            explanation_level=action_plan.explanation_level,
            confidence=action_plan.confidence,
            should_teach=action_plan.should_teach,
            should_review=action_plan.should_review,
            should_exercise=action_plan.should_exercise,
            english_level=brain.student.estimated_level,
            target_skill=brain.state.skill_focus.teaching,
            detected_skill=brain.state.skill_focus.detected,
        )


prompt_builder = PromptBuilder()
