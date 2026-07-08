from __future__ import annotations

from app.services.prompt_builder.static.base_prompt import (
    SYSTEM_INSTRUCTION,
)


class StaticPromptBuilder:
    """
    Responsável por fornecer o Prompt Base.
    """

    def build(
        self,
    ) -> str:

        return SYSTEM_INSTRUCTION.strip()


static_prompt_builder = StaticPromptBuilder()
