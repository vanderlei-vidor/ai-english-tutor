"""
Script Registry

Gerencia todos os teaching scripts disponíveis.
Mapeia estratégias pedagógicas para seus scripts de execução.

Nota importante:
O Brain nunca acessa scripts diretamente.
O Brain fala com o Pedagogy Engine.
O Pedagogy Engine usa o Teaching Registry para selecionar estratégias.
Cada estratégia usa o Script Registry para obter seu script de execução.
"""

from __future__ import annotations

from .direct_instruction import direct_instruction_script
from .guided_discovery import guided_discovery_script
from .communicative import communicative_script
from .minimal_hint import minimal_hint_script
from .socratic import socratic_script


class ScriptRegistry:
    """
    Registry central de todos os teaching scripts.

    Cada estratégia pedagógica pode ter um ou mais scripts
    que definem como ela será executada.
    """

    def __init__(self):
        self._scripts = {
            "direct_instruction": direct_instruction_script,
            "guided_discovery": guided_discovery_script,
            "communicative": communicative_script,
            "minimal_hint": minimal_hint_script,
            "socratic": socratic_script,
        }

    def get(self, strategy_type: str):
        """
        Obtém o script para uma estratégia específica.

        Args:
            strategy_type: Tipo de estratégia (direct_instruction, socratic, etc.)

        Returns:
            TeachingScript com os passos de execução
        """
        script = self._scripts.get(strategy_type)

        if script is None:
            raise ValueError(
                f"Script não encontrado para estratégia: {strategy_type}\n"
                f"Estratégias disponíveis: {list(self._scripts.keys())}"
            )

        return script.build()

    def list_available(self) -> list[str]:
        """Lista todas as estratégias com scripts disponíveis."""
        return list(self._scripts.keys())

    def register(self, strategy_type: str, script):
        """
        Registra um novo script para uma estratégia.

        Args:
            strategy_type: Tipo de estratégia
            script: Instância de TeachingScriptBase
        """
        if strategy_type in self._scripts:
            print(f"⚠️  Script para '{strategy_type}' será sobrescrito")

        self._scripts[strategy_type] = script


# Instância global do registry
script_registry = ScriptRegistry()

__all__ = [
    "ScriptRegistry",
    "script_registry",
]
