from __future__ import annotations

from .strategies.direct_instruction import (
    DirectInstructionStrategy,
)

from .strategies.guided_discovery import (
    GuidedDiscoveryStrategy,
)
from .strategies.communicative import (
    CommunicativeStrategy,
)

class TeachingRegistry:
    def __init__(self):

        self._strategies = [
            GuidedDiscoveryStrategy(),
            DirectInstructionStrategy(),
            CommunicativeStrategy(),
        ]



    def select(
        self,
        state,
    ):
        
        print()
        print("=" * 60)
        print("TESTING TEACHING STRATEGIES")
        print("=" * 60)

        for strategy in self._strategies:

            result = strategy.matches(state)

            print(
                strategy.__class__.__name__,
                "->",
                result,
            )

            if result:

                print()

                print(
                    "SELECTED:",
                    strategy.__class__.__name__,
                )

                return strategy

        print()

        print("DEFAULT")

        return CommunicativeStrategy()



teaching_registry = TeachingRegistry()
