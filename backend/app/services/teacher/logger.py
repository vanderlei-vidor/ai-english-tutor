from __future__ import annotations

from app.services.teacher.models import (
    TeacherDecision,
)


class TeacherLogger:
    def decision(
        self,
        decision: TeacherDecision,
    ) -> None:

        print()

        print("=" * 60)
        print("TEACHER ENGINE")
        print("=" * 60)

        print(f"INTENT:            {decision.intent.value}")
        print(f"ACTION:            {decision.teacher_action}")
        print(f"STRATEGY:          {decision.teacher_strategy}")
        print(f"REASON:            {decision.teacher_reason}")

        print()

        print(f"TARGET SKILL:      {decision.target_skill}")
        print(f"DETECTED SKILL:    {decision.detected_skill}")

        print()

        print(f"SHOULD TEACH:      {decision.should_teach}")
        print(f"SHOULD REVIEW:     {decision.should_review}")
        print(f"SHOULD EXERCISE:   {decision.should_exercise}")

        print()

        print(f"EXPLANATION:       {decision.explanation_level}")
        print(f"PRIORITY:          {decision.priority}")
        print(f"CONFIDENCE:        {decision.confidence:.2f}")

        print("=" * 60)


teacher_logger = TeacherLogger()
