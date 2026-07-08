from __future__ import annotations

from app.services.prompt_builder.context import (
    PromptContext,
)


class PromptBuilderLogger:
    def context(
        self,
        prompt: PromptContext,
    ) -> None:

        print()

        print("======== PROMPT BUILDER ========")

        print(f"STRATEGY:          {prompt.teacher_strategy}")
        print(f"ACTION:            {prompt.teacher_action}")
        print(f"TARGET SKILL:      {prompt.target_skill}")
        print(f"LEVEL:             {prompt.english_level}")
        print(f"EXPLANATION:       {prompt.explanation_level}")

        print("================================")


prompt_builder_logger = PromptBuilderLogger()
