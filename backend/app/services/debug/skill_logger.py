from __future__ import annotations

from app.services.pedagogical.analysis import PedagogicalAnalysis


class SkillLogger:
    def resolution(
        self,
        pedagogical: PedagogicalAnalysis,
    ) -> None:

        final_skill = pedagogical.detected_skill or pedagogical.target_skill

        print("======== SKILL RESOLUTION DEBUG ========")

        print(f"DETECTED SKILL:        {pedagogical.detected_skill}")

        print(f"TARGET SKILL:          {pedagogical.target_skill}")

        print(f"HAD ERROR:             {pedagogical.had_error}")

        print(f"TARGET SKILL ERROR:    {pedagogical.target_skill_error}")

        print(f"FINAL SKILL:           {final_skill}")

        print(f"CORRECTION:            {pedagogical.correction_text}")

        print("========================================")


skill_logger = SkillLogger()
