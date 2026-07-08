from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


# ==========================================================
# IMPORTANT
#
# Este objeto representa o estado pedagógico da conversa.
#
# Ele NÃO contém o conteúdo da aula.
#
# O conteúdo pedagógico é representado por TeachingPlan.
# ==========================================================


@dataclass(slots=True)
class PedagogicalAnalysis:
    """
    Resultado da análise pedagógica realizada sobre uma interação.

    Este objeto concentra todas as decisões pedagógicas produzidas
    pelo PedagogicalAnalysisEngine e será consumido pelas próximas
    etapas do pipeline (Conversation, LLM, Memory, etc.).
    """

    # ==========================================================
    # Advanced Structures
    # ==========================================================

    complexity_score: int = 0

    complexity_points: int = 0

    structures: list[str] = field(default_factory=list)

    advanced_structures: dict[str, int] = field(default_factory=dict)

    # ==========================================================
    # English Level
    # ==========================================================

    estimated_score: float = 0.0

    estimated_level: str = "A1"

    # ==========================================================
    # Skills
    # ==========================================================

    current_focus: str | None = None

    target_skill: str | None = None

    legacy_target_skill: str | None = None

    detected_skill: str | None = None

    fallback_skill: str | None = None

    # ==========================================================
    # Corrections
    # ==========================================================

    teacher_action: str = ""

    needs_correction: bool = False

    correction_text: str = ""

    had_error: bool = False

    target_skill_error: bool = False

    has_any_real_error: bool = False

    sanitizer_reason: str = ""

    # ==========================================================
    # Teaching Decision
    # ==========================================================

    backend_wants_teaching: bool = False

    exercise_required: bool = False

    teaching_mode: str = ""

    # ==========================================================
    # Methods
    # ==========================================================

    def load_ai_response(
        self,
        response: dict[str, Any],
    ) -> None:
        """
        Sincroniza o estado pedagógico com a resposta produzida pelo LLM.
        """

        self.legacy_target_skill = response.get("target_skill")

        self.target_skill = self.target_skill or self.legacy_target_skill

        self.teacher_action = response.get(
            "teacher_action",
            "",
        )

        self.needs_correction = response.get(
            "needs_correction",
            False,
        )

        self.correction_text = response.get(
            "correction",
            "",
        )

        self.detected_skill = response.get(
            "detected_skill",
        )
