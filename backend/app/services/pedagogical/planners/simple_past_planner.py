from __future__ import annotations

from app.services.pedagogical.base import BaseLessonPlanner
from app.services.pedagogical.models import TeachingPlan


class SimplePastPlanner(BaseLessonPlanner):
    def build(self, analysis):

        for concept in analysis.concepts:
            if concept.id != "simple_past":
                continue

            return TeachingPlan(
                concept_id=concept.id,
                title=concept.name,
                explanation=concept.description,
                examples=concept.examples,
                review_after_days=concept.review_after_days,
                difficulty=concept.exercise_difficulty,
                estimated_minutes=concept.estimated_study_minutes,
                priority=concept.teaching_priority,
            )

        return None
