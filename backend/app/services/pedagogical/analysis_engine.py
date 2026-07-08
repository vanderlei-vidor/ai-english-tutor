from __future__ import annotations

from app.models.user_memory import UserMemory
from app.services.grammar_engine.models import GrammarAnalysis
from app.services.level_detection import (
    calculate_complexity_points,
    detect_advanced_structures,
)
from app.services.level_estimator import (
    calculate_level_score,
    estimate_level,
)
from app.services.pedagogical.analysis import PedagogicalAnalysis


class PedagogicalAnalysisEngine:
    """
    Responsável por produzir a análise pedagógica de uma interação.

    Este engine transforma os resultados do Grammar Engine em um
    estado pedagógico que será utilizado pelas próximas etapas
    do pipeline (Sanitizer, Conversation Engine, Memory, etc.).
    """

    def analyze(
        self,
        grammar: GrammarAnalysis,
        text: str,
        user_memory: UserMemory,
    ) -> PedagogicalAnalysis:

        complexity_score, structures = detect_advanced_structures(text)
        primary_error_skill = (
            grammar.primary_error.skill
            if grammar.primary_error
            else None
        )
        target_skill = grammar.current_focus or primary_error_skill

        pedagogical = PedagogicalAnalysis(
            complexity_score=complexity_score,
            complexity_points=calculate_complexity_points(complexity_score),
            structures=structures,
            current_focus=grammar.current_focus,
            target_skill=target_skill,
            detected_skill=primary_error_skill,
            had_error=grammar.has_errors,
            target_skill_error=(
                grammar.has_errors
                and target_skill is not None
                and primary_error_skill is not None
                and target_skill == primary_error_skill
            ),
        )

        self._calculate_level(
            pedagogical=pedagogical,
            user_memory=user_memory,
        )

        return pedagogical

    def _calculate_level(
        self,
        pedagogical: PedagogicalAnalysis,
        user_memory: UserMemory,
    ) -> None:
        """
        Atualiza o nível estimado do aluno utilizando
        o histórico de estruturas avançadas.
        """

        advanced_structures = user_memory.data.get(
            "advanced_structures",
            {},
        )

        for structure in pedagogical.structures:
            advanced_structures[structure] = advanced_structures.get(structure, 0) + 1

        pedagogical.advanced_structures = advanced_structures

        pedagogical.estimated_score = calculate_level_score(advanced_structures)

        pedagogical.estimated_level = estimate_level(advanced_structures)


pedagogical_analysis_engine = PedagogicalAnalysisEngine()
