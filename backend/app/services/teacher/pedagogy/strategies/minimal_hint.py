from __future__ import annotations

from ..base import TeachingStrategy


class MinimalHintStrategy(
    TeachingStrategy,
):
    def matches(
        self,
        state,
    ) -> bool:

        return False

    def build(
        self,
        state,
        plan,
    ) -> None:

        pass
