from __future__ import annotations

from .strategies.implementations import (
    CommunicativeStrategy,
    DirectInstructionStrategy,
    GuidedDiscoveryStrategy,
    MinimalHintStrategy,
    SocraticStrategy,
)


class TeachingRegistry:
    def __init__(self):

        self._strategies = [
            GuidedDiscoveryStrategy(),
            DirectInstructionStrategy(),
            SocraticStrategy(),
            MinimalHintStrategy(),
            CommunicativeStrategy(),
        ]

    def select(
        self,
        state,
    ):

        print()

        print("=" * 60)
        print("PEDAGOGY REGISTRY")
        print("=" * 60)

        for strategy in self._strategies:
            matched = strategy.matches(
                state,
            )

            print(f"{strategy.__class__.__name__:<30} -> {matched}")

            if matched:
                print()

                print(
                    "SELECTED:",
                    strategy.__class__.__name__,
                )

                print("=" * 60)

                return strategy

        print()

        print("FALLBACK: CommunicativeStrategy")

        print("=" * 60)

        return CommunicativeStrategy()


teaching_registry = TeachingRegistry()
