"""
Pedagogy Engine Module

Responsável por decidir COMO ensinar.

O Brain (Decision Maker) envia um TeacherActionPlan com contexto.
O Pedagogy Engine transforma em um TeachingStrategyPlan.

Flow:
    TeacherActionPlan (O QUE?)
            ↓
    Teaching Registry (Seleciona estratégia)
            ↓
    Teaching Strategy (Define parâmetros)
            ↓
    Script Registry (Busca template)
            ↓
    Teaching Script (Retorna passos)
            ↓
    TeachingStrategyPlan (COMO?)
"""

from .engine import (
    teaching_engine,
    TeachingEngine,
)

from .models import (
    TeachingStrategyPlan,
)

from .registry import (
    teaching_registry,
    TeachingRegistry,
)

from .scripts import (
    script_registry,
    ScriptRegistry,
    TeachingScript,
    TeachingStep,
)

from .strategies.implementations import (
    DirectInstructionStrategy,
    GuidedDiscoveryStrategy,
    SocraticStrategy,
    MinimalHintStrategy,
    CommunicativeStrategy,
)

__all__ = [
    # Engine
    "TeachingEngine",
    "teaching_engine",
    # Models
    "TeachingStrategyPlan",
    # Teaching Registry
    "TeachingRegistry",
    "teaching_registry",
    # Script Registry
    "ScriptRegistry",
    "script_registry",
    "TeachingScript",
    "TeachingStep",
    # Strategies
    "DirectInstructionStrategy",
    "GuidedDiscoveryStrategy",
    "SocraticStrategy",
    "MinimalHintStrategy",
    "CommunicativeStrategy",
]
