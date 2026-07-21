"""
Teaching Scripts

Scripts representam templates específicos de COMO ensinar.
Cada estratégia pedagógica tem um ou mais scripts.

Importância da arquitetura:
- O Brain NUNCA fala diretamente com scripts
- Brain → Pedagogy Engine → Teaching Registry (seleciona estratégia)
- Estratégia → Script Registry (obtém template de execução)

Isso mantém tudo desacoplado e flexível.
"""

from .models import (
    TeachingScript,
    TeachingStep,
)

from .base import (
    TeachingScriptBase,
)

from .registry import (
    ScriptRegistry,
    script_registry,
)

from .direct_instruction import (
    DirectInstructionScript,
    direct_instruction_script,
)

from .guided_discovery import (
    GuidedDiscoveryScript,
    guided_discovery_script,
)

from .communicative import (
    CommunicativeScript,
    communicative_script,
)

from .minimal_hint import (
    MinimalHintScript,
    minimal_hint_script,
)

from .socratic import (
    SocraticScript,
    socratic_script,
)

__all__ = [
    # Models
    "TeachingScript",
    "TeachingStep",
    # Base
    "TeachingScriptBase",
    # Registry
    "ScriptRegistry",
    "script_registry",
    # Scripts
    "DirectInstructionScript",
    "direct_instruction_script",
    "GuidedDiscoveryScript",
    "guided_discovery_script",
    "CommunicativeScript",
    "communicative_script",
    "MinimalHintScript",
    "minimal_hint_script",
    "SocraticScript",
    "socratic_script",
]
