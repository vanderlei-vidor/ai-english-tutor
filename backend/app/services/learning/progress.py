from __future__ import annotations
import profile

from app.services.learning.models import (
    LearningProfile,
    SkillProgress,
)


class ProgressManager:
    """
    Responsável por atualizar o progresso do aluno.

    Não decide qual conteúdo ensinar.
    Não gera aulas.
    Não conversa com IA.

    Apenas mantém o LearningProfile consistente.
    """

    # --------------------------------------------------
    # Recupera (ou cria) uma SkillProgress
    # --------------------------------------------------

    def get_skill(
        self,
        profile: LearningProfile,
        skill: str,
    ) -> SkillProgress:

        if skill not in profile.skill_progress:
            profile.skill_progress[skill] = SkillProgress(skill=skill)

        return profile.skill_progress[skill]

    # --------------------------------------------------
    # Registrar um acerto
    # --------------------------------------------------

    def register_success(
        self,
        profile: LearningProfile,
        skill: str,
    ) -> None:

        progress = self.get_skill(profile, skill)

        progress.attempts += 1
        progress.correct += 1
        progress.streak += 1

    # --------------------------------------------------
    # Registrar um erro
    # --------------------------------------------------

    def register_error(
        self,
        profile: LearningProfile,
        skill: str,
        sentence: str,
    ) -> None:

        progress = self.get_skill(profile, skill)

        progress.attempts += 1
        progress.incorrect += 1
        progress.streak = 0

        progress.recent_errors.append(sentence)

        # Mantém apenas os últimos 10 erros

        progress.recent_errors = progress.recent_errors[-10:]

    # --------------------------------------------------
    # Aula concluída
    # --------------------------------------------------

    def register_lesson(
        self,
        profile: LearningProfile,
        skill: str,
    ) -> None:

        progress = self.get_skill(profile, skill)

        progress.completed_lessons += 1

        profile.total_lessons += 1

    # --------------------------------------------------
    # Exercício concluído
    # --------------------------------------------------

    def register_exercise(
        self,
        profile: LearningProfile,
        skill: str,
    ) -> None:

        progress = self.get_skill(profile, skill)

        progress.completed_exercises += 1

        profile.total_exercises += 1

    def register_sentence(
        self,
        profile: LearningProfile,
    ) -> None:

        profile.total_sentences += 1


progress_manager = ProgressManager()
