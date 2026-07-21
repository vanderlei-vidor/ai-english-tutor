from __future__ import annotations

from app.services.skill_score_service import (
    calculate_skill_scores,
    get_highest_priority_skill,
)


class StudentSkillSelector:
    """
    Seleciona a skill pedagógica prioritária com base
    em pontuação normalizada entre:
      - dificuldade atual (skill_mastery) — peso 70%
      - histórico acumulado de erros (weak_skills) — peso 30%

    Absorvido do weighted_teaching_engine.py + skill_score_service.py.
    """

    def select(
        self,
        memory_data: dict,
    ) -> str | None:

        skill_scores = calculate_skill_scores(
            memory_data,
        )

        if not skill_scores:
            return "past_tense"

        return get_highest_priority_skill(
            memory_data,
        ) or "past_tense"


student_skill_selector = StudentSkillSelector()
