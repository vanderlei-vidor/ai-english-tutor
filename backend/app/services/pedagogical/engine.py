from __future__ import annotations

from app.services.grammar_engine.models import GrammarAnalysis
from app.services.pedagogical.registry import get_planners


class PedagogicalEngine:
    """
    Responsável por gerar planos pedagógicos
    a partir dos conceitos identificados.
    """

    def analyze(self, analysis: GrammarAnalysis) -> None:

        
        
        # Busca os planners cadastrados
        planners = get_planners()

        # Validação de segurança: se a lista estiver vazia, joga o erro
        if not planners:
            raise RuntimeError("No lesson planners have been registered.")

        # Roda o loop usando a variável que já guardou os planners
        for planner in planners:
            
            plan = planner.build(analysis)

            if plan is not None:
                analysis.teaching_plans.append(plan)

     

        


pedagogical_engine = PedagogicalEngine()
