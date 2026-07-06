from __future__ import annotations

from app.services.learning.models import (
    LearningProfile,
    SkillProgress,
)


class ReviewScheduler:
    """
    Responsável por decidir quais habilidades
    precisam ser revisadas.
    """

    def update(self, profile: LearningProfile) -> None:

        profile.review_queue.clear()

        for progress in profile.skill_progress.values():
            if self.should_review(progress):
                profile.review_queue.append(progress.skill)

    # --------------------------------------------------
    # Regra de revisão
    # --------------------------------------------------

    def should_review(
        self,
        progress: SkillProgress,
    ) -> bool:

        if progress.mastery < 90:
            return True

        if progress.next_review_day <= progress.last_review_day:
            return True

        return False


review_scheduler = ReviewScheduler()
