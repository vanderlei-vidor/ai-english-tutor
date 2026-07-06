from __future__ import annotations

from app.services.learning.models import (
    LearningProfile,
    SkillProgress,
)


class MasteryEngine:
    """
    Calcula o nível de domínio (Mastery)
    de cada habilidade do aluno.
    """

    # --------------------------------------------------
    # Calcula a porcentagem de domínio
    # --------------------------------------------------

    def calculate(
        self,
        progress: SkillProgress,
    ) -> float:

        if progress.attempts == 0:
            return 0.0

        return round(
            (progress.correct / progress.attempts) * 100,
            1,
        )

    # --------------------------------------------------
    # Atualiza uma habilidade
    # --------------------------------------------------

    def update_skill(
        self,
        profile: LearningProfile,
        skill: str,
    ) -> None:

        progress = profile.skill_progress[skill]

        progress.mastery = self.calculate(progress)

    # --------------------------------------------------
    # Atualiza todas as habilidades
    # --------------------------------------------------

    def update_profile(
        self,
        profile: LearningProfile,
    ) -> None:

        if not profile.skill_progress:
            return

        # Limpa as listas antigas para recalcular do zero com os dados novos
        profile.mastered_skills.clear()
        profile.weak_skills.clear()

        total = 0.0

        for skill in profile.skill_progress.values():
            skill.mastery = self.calculate(skill)
            total += skill.mastery

            # Classifica a habilidade de acordo com o nível de domínio
            if skill.mastery >= 90:
                profile.mastered_skills.append(skill.skill)
            elif skill.mastery < 70:
                profile.weak_skills.append(skill.skill)

        profile.overall_accuracy = round(
            total / len(profile.skill_progress),
            1,
        )

        # Define automaticamente o foco atual baseado nas fraquezas
        if profile.weak_skills:
            profile.current_focus = profile.weak_skills[0]
        else:
            profile.current_focus = None


mastery_engine = MasteryEngine()
