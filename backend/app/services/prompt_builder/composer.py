from __future__ import annotations

from app.services.prompt_builder.context import (
    PromptContext,
)

from app.services.teacher.prompt.models import (
    TeacherPrompt,
)


class PromptComposer:
    """
    Responsável por transformar o PromptContext
    em um System Prompt para o LLM.
    """

    def compose(
        self,
        context: PromptContext,
        teacher_prompt: TeacherPrompt | None = None,
    ) -> str:

        sections = [
            "# TEACHER",
        ]

        # PASSO 7: Usar handler e purpose em vez de action
        if teacher_prompt:
            sections.append(
                f"Teaching Handler: {teacher_prompt.handler}",
            )
            sections.append(
                f"Teaching Purpose: {teacher_prompt.purpose}",
            )

        sections.extend(
            [
                "",
                "# STUDENT",
                f"English Level: {context.english_level}",
                f"Target Skill: {context.target_skill}",
                f"Detected Skill: {context.detected_skill}",
                "",
                "# CONVERSATION",
                f"Should Teach: {context.should_teach}",
                f"Should Review: {context.should_review}",
                f"Should Exercise: {context.should_exercise}",
                "",
                "# EXPLANATION",
                f"Explanation Level: {context.explanation_level}",
            ]
        )

        # PASSO 8: Nova estrutura com BEHAVIOR section
        if teacher_prompt:
            sections.append("")
            sections.append("# BEHAVIOR")

            for instruction in teacher_prompt.instructions:
                sections.append(f"{instruction}")

            if teacher_prompt.constraints:
                sections.append("")

                for constraint in teacher_prompt.constraints:
                    sections.append(f"{constraint}")

            sections.append("")
            sections.append("# PEDAGOGICAL INSTRUCTION")

        return "\n".join(
            sections,
        )


prompt_composer = PromptComposer()
