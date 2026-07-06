from __future__ import annotations

from app.services.grammar_engine.models import GrammarAnalysis
from app.services.grammar_engine.pipeline.base import BaseStage

from app.services.learning.engine import learning_engine
from app.services.learning.events import LearningEvent


class LearningStage(BaseStage):
    def run(
        self,
        analysis: GrammarAnalysis,
    ) -> None:

        profile = learning_engine.get_profile()

        analysis.learning_profile = profile

        analysis.learning_events.clear()

        for error in analysis.errors:

            analysis.learning_events.append(
                LearningEvent(
                    skill=error.skill,
                    success=False,
                    confidence=error.confidence,
                    source=error.detected_by or "grammar_engine",
            )
        )
            
        for concept in analysis.concepts:

            if any(
                event.skill == concept.skill
                for event in analysis.learning_events
            ):
                continue

            analysis.learning_events.append(
                LearningEvent(
                skill=concept.skill,
                success=True,
                confidence=1.0,
                source="concept_engine",
                concept_id=concept.id,
            )
        )

        learning_engine.update_progress(
            profile,
            analysis,
        )


learning_stage = LearningStage()
