from __future__ import annotations

from app.services.learning.models import LearningProfile
from app.services.learning.models import SkillProgress


class LearningEngine:
    """
    Responsável por gerenciar o estado de aprendizagem do aluno.
    """

    def __init__(self):

        self._profiles: dict[str, LearningProfile] = {}

    # --------------------------------------------------
    # Profile
    # --------------------------------------------------

    def get_profile(
        self,
        student_id: str = "anonymous",
    ) -> LearningProfile:

        if student_id not in self._profiles:
            self._profiles[student_id] = LearningProfile(
                student_id=student_id,
            )

        return self._profiles[student_id]

    # --------------------------------------------------
    # Progress
    # --------------------------------------------------

    def update_progress(
        self,
        profile: LearningProfile,
        analysis,
    ) -> None:

        for event in analysis.learning_events:
            skill = event.skill

            if skill not in profile.skill_progress:
                profile.skill_progress[skill] = SkillProgress(
                    skill=skill,
                )

            progress = profile.skill_progress[skill]

            progress.attempts += 1

            if event.success:
                progress.correct += 1
            else:
                progress.incorrect += 1

            self.update_mastery(progress)

            self.refresh_profile(profile)

    # --------------------------------------------------
    # Mastery
    # --------------------------------------------------

    def update_mastery(
        self,
        progress,
    ) -> None:

        if progress.attempts == 0:
            progress.mastery = 0.0
            return

        progress.mastery = (progress.correct / progress.attempts) * 100

    # --------------------------------------------------
    # Profile Synchronization
    # --------------------------------------------------

    def refresh_profile(
        self,
        profile: LearningProfile,
    ) -> None:

        profile.mastered_skills.clear()
        profile.weak_skills.clear()

        # Variáveis para calcular a precisão geral (Passo 4)
        total_attempts = 0
        total_correct = 0

        for progress in profile.skill_progress.values():
            total_attempts += progress.attempts
            total_correct += progress.correct

            if progress.mastery >= 90:
                profile.mastered_skills.append(
                    progress.skill,
                )

            elif progress.mastery < 60:
                profile.weak_skills.append(
                    progress.skill,
                )

        # PASSO 4: Atualiza a precisão geral (overall_accuracy)
        if total_attempts:
            profile.overall_accuracy = round(
                (total_correct / total_attempts) * 100,
                1,
            )
        else:
            profile.overall_accuracy = 0.0

        # PASSO 3: Define o foco atual do aluno baseado nas dificuldades
        if profile.weak_skills:
            profile.current_focus = profile.weak_skills[0]
        else:
            profile.current_focus = None


learning_engine = LearningEngine()
