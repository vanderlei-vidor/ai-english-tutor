"""
Teaching Strategies Module

Estratégias pedagógicas que definem COMO ensinar.

Cada estratégia:
1. Herda de TeachingStrategy
2. Implementa matches(state) - para seleção
3. Implementa build(state, plan) - para preencher parâmetros

Nota: Os arquivos antigos (direct_instruction.py, socratic.py, etc.)
contêm os SCRIPTS (templates de execução), não as STRATEGIES.
As STRATEGIES estão em implementations.py.
"""

from .implementations import (
    DirectInstructionStrategy,
    GuidedDiscoveryStrategy,
    SocraticStrategy,
    MinimalHintStrategy,
    CommunicativeStrategy,
)

__all__ = [
    "DirectInstructionStrategy",
    "GuidedDiscoveryStrategy",
    "SocraticStrategy",
    "MinimalHintStrategy",
    "CommunicativeStrategy",
]
