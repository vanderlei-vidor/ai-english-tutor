from __future__ import annotations

from app.services.prompt_builder.context import (
    PromptContext,
)


class PromptComposer:
    """
    Responsável por transformar o PromptContext
    em um System Prompt para o LLM.
    """

    def compose(
        self,
        context: PromptContext,
    ) -> str:

        sections = [
            "# TEACHER",
            f"Teacher Strategy: {context.teacher_strategy}",
            f"Teacher Action: {context.teacher_action}",
            f"Teacher Reason: {context.teacher_reason}",
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

        return "\n".join(sections)


prompt_composer = PromptComposer()
