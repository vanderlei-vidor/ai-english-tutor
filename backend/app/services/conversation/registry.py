from __future__ import annotations

from app.services.conversation.base_strategy import (
    BaseConversationStrategy,
)

# ==========================================================
# Registry interno
# ==========================================================

_STRATEGIES: list[BaseConversationStrategy] = []


def register_strategy(
    strategy: BaseConversationStrategy,
) -> None:
    """
    Registra uma estratégia de conversa.
    """

    _STRATEGIES.append(strategy)


def get_strategies() -> list[BaseConversationStrategy]:
    """
    Retorna todas as estratégias cadastradas.
    """

    return sorted(
        _STRATEGIES,
        key=lambda strategy: strategy.priority,
    )


from app.services.conversation.strategies.direct_instruction import (
    DirectInstructionStrategy,
)

register_strategy(
    DirectInstructionStrategy(),
)