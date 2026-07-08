from __future__ import annotations

from typing import Any

from app.services.correction_validator import (
    analyze_correction_validity,
    is_real_correction_by_skill,
)
from app.services.pedagogical.analysis import PedagogicalAnalysis


class PedagogicalSanitizer:
    """
    Responsável por validar e sanitizar
    a resposta pedagógica produzida pelo LLM.
    """

    def sanitize(
        self,
        pedagogical: PedagogicalAnalysis,
        user_text: str,
        ai_response: dict,
    ) -> None:
        
        initial_target_skill_error = is_real_correction_by_skill(
            correction=pedagogical.correction_text,
            target_skill=pedagogical.target_skill,
        )

        self._analyze(
            pedagogical,
            user_text,
        )

        self._preserve_grammar_confirmed_error(
            pedagogical,
        )

        self._remove_false_corrections(
            pedagogical,
            ai_response,
        )

        self._resolve_fallback_skill(
            pedagogical,
            user_text,
            ai_response,
            initial_target_skill_error,
        )

        self._sync_ai_response(
            pedagogical,
            ai_response,
        )

        self._calculate_error_state(
            pedagogical,
            initial_target_skill_error,
        )

    def _analyze(
        self,
        pedagogical: PedagogicalAnalysis,
        user_text: str,
    ) -> None:

        sanitizer_analysis = analyze_correction_validity(
            user_text=user_text,
            correction=pedagogical.correction_text,
            teacher_action=pedagogical.teacher_action,
            needs_correction=pedagogical.needs_correction,
            target_skill=pedagogical.target_skill,
            detected_skill=pedagogical.detected_skill,
        )

        pedagogical.sanitizer_reason = sanitizer_analysis["reason"]
        pedagogical.has_any_real_error = sanitizer_analysis["is_real_error"]

    def _preserve_grammar_confirmed_error(
        self,
        pedagogical: PedagogicalAnalysis,
    ) -> None:
        """
        O sanitizer pode bloquear falsos positivos do LLM, mas nao deve apagar
        um erro ja confirmado pelo Grammar Engine na skill alvo.
        """
        if pedagogical.had_error and pedagogical.target_skill_error:
            pedagogical.has_any_real_error = True
            pedagogical.sanitizer_reason = "grammar_confirmed_error"

    def _remove_false_corrections(
        self,
        pedagogical: PedagogicalAnalysis,
        ai_response: dict[str, Any],
    ) -> None:

        if (
            pedagogical.teacher_action == "correction"
            and not pedagogical.has_any_real_error
        ):
            print(
                f"WARNING: SANITIZER CONVERTED TO SUCCESS -> "
                f"reason={pedagogical.sanitizer_reason}"
            )

            ai_response["teacher_action"] = "chat"
            ai_response["needs_correction"] = False
            ai_response["correction"] = "Correct! ✨"
            ai_response["conversation_reply"] = "Correct! ✨"
            ai_response["detected_skill"] = None

    def _resolve_fallback_skill(
        self,
        pedagogical: PedagogicalAnalysis,
        user_text: str,
        ai_response: dict[str, Any],
        initial_target_skill_error: bool,
    ) -> None:
        """
        Método reservado para a resolução de habilidades secundárias/fallback.
        """
        # Nota: Mantido conforme a chamada do seu fluxo original
        if not pedagogical.has_any_real_error:
            return

        detected_skill = ai_response.get("detected_skill")
        target_skill = pedagogical.target_skill

        if (
            detected_skill
            and target_skill
            and detected_skill != target_skill
        ):
            pedagogical.fallback_skill = detected_skill
            ai_response["fallback_skill"] = detected_skill

    def _sync_ai_response(
        self,
        pedagogical: PedagogicalAnalysis,
        ai_response: dict[str, Any],
    ) -> None:
        """
        Garante que as mutações feitas no dicionário ai_response
        refletem instantaneamente de volta no objeto PedagogicalAnalysis.
        """
        pedagogical.load_ai_response(ai_response)

    def _calculate_error_state(
        self,
        pedagogical: PedagogicalAnalysis,
        initial_target_skill_error: bool,
    ) -> None:
        """
        Consolida o estado final usado por memória, XP e logs.
        """
        grammar_had_error = pedagogical.had_error
        pedagogical.had_error = grammar_had_error or pedagogical.has_any_real_error

        detected_skill = pedagogical.detected_skill
        target_skill = pedagogical.target_skill

        pedagogical.target_skill_error = pedagogical.had_error and (
            pedagogical.target_skill_error
            or initial_target_skill_error
            or (
                detected_skill is not None
                and target_skill is not None
                and detected_skill == target_skill
            )
        )


pedagogical_sanitizer = PedagogicalSanitizer()
