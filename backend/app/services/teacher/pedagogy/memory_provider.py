from __future__ import annotations

from .memory_snapshot import (
    PedagogicalMemorySnapshot,
)


class PedagogicalMemoryProvider:
    def load(
        self,
        context,
    ) -> PedagogicalMemorySnapshot:

        return PedagogicalMemorySnapshot()


pedagogical_memory_provider = PedagogicalMemoryProvider()
