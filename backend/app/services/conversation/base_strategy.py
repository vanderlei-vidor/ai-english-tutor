from abc import ABC, abstractmethod

from app.services.conversation.analysis import (
    ConversationAnalysis,
)
from app.services.pedagogical.analysis import (
    PedagogicalAnalysis,
)


class BaseConversationStrategy(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        raise NotImplementedError
    
    @property
    def priority(self) -> int:
        """
        Quanto maior a prioridade,
        mais cedo esta estratégia será considerada.
        """
        return 100

    @abstractmethod
    def can_apply(
        self,
        pedagogical: PedagogicalAnalysis,
    ) -> bool:
        raise NotImplementedError

    @abstractmethod
    def apply(
        self,
        conversation: ConversationAnalysis,
        pedagogical: PedagogicalAnalysis,
    ) -> None:
        raise NotImplementedError
    
    
