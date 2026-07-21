"""
Pedagogy Engine

Componente central da arquitetura pedagógica.

Flow:
1. Teacher Brain envia TeacherActionPlan (O QUE fazer)
2. Pedagogy Engine recebe o plan
3. Teaching Registry seleciona a estratégia ideal
4. Script Registry fornece o template de steps
5. TeachingStrategyPlan é retornado (COMO ensinar)

Important: O Brain NUNCA acessa Scripts diretamente.
Toda a orquestração fica aqui no Engine.
"""

from __future__ import annotations

from .models import (
    TeachingStrategyPlan,
)

from .registry import (
    teaching_registry,
)

from .scripts import (
    script_registry,
)


class TeachingEngine:
    """
    Pedagogy Engine - Orquestrador do ensino.

    Responsável por transformar o estado atual do professor
    em um plano pedagógico desacoplado e bem definido.

    O Teacher Brain decide O QUE fazer (TeacherActionPlan).

    O Pedagogy Engine decide COMO ensinar (TeachingStrategyPlan).

    ┌─────────────────────────────────────────────────────┐
    │          Teacher Brain (O QUE?)                     │
    │     TeacherActionPlan com contexto do aluno         │
    └────────────────┬────────────────────────────────────┘
                     │
                     ▼
    ┌─────────────────────────────────────────────────────┐
    │       Pedagogy Engine (COMO?)                       │
    │                                                      │
    │  1. Teaching Registry: Seleciona estratégia         │
    │  2. Strategy: Define parâmetros pedagógicos         │
    │  3. Script Registry: Busca template de steps        │
    │  4. TeachingStrategyPlan: Plan de execução          │
    └────────────────┬────────────────────────────────────┘
                     │
                     ▼
    ┌─────────────────────────────────────────────────────┐
    │       Lesson Manager (EXECUTAR)                     │
    │     Executa os passos do Teaching Script            │
    └─────────────────────────────────────────────────────┘
    """

    def build(
        self,
        state,
    ) -> TeachingStrategyPlan:
        """
        Constrói um plano pedagógico completo.

        Args:
            state: TeachingState com contexto atual do aluno

        Returns:
            TeachingStrategyPlan: Plano de como ensinar
        """

        # 1. Criar o plano base
        plan = TeachingStrategyPlan()

        # 2. Teaching Registry: Seleciona a estratégia ideal
        strategy = teaching_registry.select(state)

        # 3. Armazenar o tipo de estratégia no plano
        plan.strategy = strategy.__class__.__name__

        # 4. Strategy constrói os parâmetros pedagógicos
        strategy.build(state, plan)

        # 5. Script Registry: Buscar o template de steps para essa estratégia
        script_type = self._get_script_type_from_strategy(strategy)
        teaching_script = script_registry.get(script_type)

        # 6. Adicionar o script pedagógico ao plano
        plan.script = teaching_script

        return plan

    def _get_script_type_from_strategy(self, strategy):
        """
        Mapeia um objeto de estratégia para o tipo de script correspondente.

        Exemplos:
            DirectInstructionStrategy → 'direct_instruction'
            SocraticStrategy → 'socratic'
        """
        strategy_name = strategy.__class__.__name__

        # Converter: DirectInstructionStrategy → direct_instruction
        script_type = strategy_name.replace("Strategy", "").replace("Script", "")

        # CamelCase para snake_case
        import re

        script_type = re.sub(r"(?<!^)(?=[A-Z])", "_", script_type).lower()

        return script_type


teaching_engine = TeachingEngine()
