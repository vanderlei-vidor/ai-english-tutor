from __future__ import annotations

from .direct_instruction import (
    DirectInstructionScript,
)

from .guided_discovery import (
    GuidedDiscoveryScript,
)

from .communicative import (
    CommunicativeScript,
)

from .minimal_hint import (
    MinimalHintScript,
)

from .socratic import (
    SocraticScript,
)


class ScriptRegistry:
    def __init__(self):

        self._scripts = {
            "direct_instruction": DirectInstructionScript(),
            "guided_discovery": GuidedDiscoveryScript(),
            "communicative": CommunicativeScript(),
            "minimal_hint": MinimalHintScript(),
            "socratic": SocraticScript(),
        }

    def get(
        self,
        strategy_name: str,
    ):

        return self._scripts.get(
            strategy_name,
            DirectInstructionScript(),
        )


script_registry = ScriptRegistry()
