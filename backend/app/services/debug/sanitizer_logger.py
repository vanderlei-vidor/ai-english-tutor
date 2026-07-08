from __future__ import annotations

from app.services.pedagogical.analysis import PedagogicalAnalysis


class SanitizerLogger:
    def routing(
        self,
        user_text: str,
        pedagogical: PedagogicalAnalysis,
    ) -> None:

        print("======== ROUTING SANITIZER DEBUG ========")

        print(f"USER TEXT:               {user_text}")

        print(f"CORRECTION TEXT:         {pedagogical.correction_text}")

        print(f"TEACHER ACTION:          {pedagogical.teacher_action}")

        print(f"NEEDS CORRECTION:        {pedagogical.needs_correction}")

        print(f"TARGET SKILL:            {pedagogical.target_skill}")

        print(f"DETECTED SKILL:          {pedagogical.detected_skill}")

        print(f"FALLBACK SKILL:          {pedagogical.fallback_skill}")

        print(f"SANITIZER REASON:        {pedagogical.sanitizer_reason}")

        print("=========================================")

    def final(
        self,
        pedagogical: PedagogicalAnalysis,
    ) -> None:

        print("======== FINAL SANITIZED STATE ========")

        print(f"FINAL TEACHER_ACTION:     {pedagogical.teacher_action}")

        print(f"FINAL NEEDS_CORRECTION:   {pedagogical.needs_correction}")

        print(f"FINAL CORRECTION:         {pedagogical.correction_text}")

        print(f"FINAL DETECTED_SKILL:     {pedagogical.detected_skill}")

        print(f"FINAL HAD_ERROR:          {pedagogical.had_error}")

        print(f"FINAL TARGET_SKILL_ERR:   {pedagogical.target_skill_error}")

        print(f"FINAL SANITIZER_REASON:   {pedagogical.sanitizer_reason}")

        print("=======================================")


sanitizer_logger = SanitizerLogger()
