from __future__ import annotations

from app.services.teacher.pedagogy.behavior.builder import (
    behavior_builder,
)

from .models import (
    TeacherPrompt,
)


class TeacherPromptBuilder:
    def build(
        self,
        plan,
        execution,
    ) -> TeacherPrompt:

        prompt = TeacherPrompt()

        prompt.mode = plan.teaching_mode
        prompt.tone = plan.tone
        prompt.style = plan.response_style
        prompt.goal = plan.goal
        prompt.target_skill = plan.target_skill
        prompt.explanation_level = plan.explanation_level
        prompt.generate_example = execution.use_example
        prompt.generate_exercise = plan.generate_exercise

        prompt.handler = execution.handler
        prompt.purpose = execution.step.purpose

        # PASSO 4: Integrar BehaviorBuilder
        behavior = behavior_builder.build(
            execution,
        )

        prompt.instructions.extend(
            behavior.instructions,
        )

        prompt.constraints.extend(
            behavior.constraints,
        )

        prompt.ask_question = behavior.ask_question
        prompt.wait_student = behavior.wait_student

        if execution.prompt_instruction:
            prompt.execution_instructions.append(
                execution.prompt_instruction,
            )

        if prompt.execution_instructions:
            prompt.instructions = prompt.execution_instructions + prompt.instructions

        return prompt


teacher_prompt_builder = TeacherPromptBuilder()
