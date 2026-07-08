
from __future__ import annotations

from app.services.teacher.decision import (
    TeacherDecision,
)


class TeacherLogger:
    def decision(
        self,
        decision: TeacherDecision,
    ) -> None:

        print()

        print("======== TEACHER ENGINE ========")

        print(f"ACTION:            {decision.teacher_action}")
        print(f"STRATEGY:          {decision.teacher_strategy}")
        print(f"REASON:            {decision.teacher_reason}")
        print(f"TARGET SKILL:      {decision.target_skill}")
        print(f"DETECTED SKILL:    {decision.detected_skill}")
        print(f"SHOULD TEACH:      {decision.should_teach}")
        print(f"SHOULD REVIEW:     {decision.should_review}")
        print(f"SHOULD EXERCISE:   {decision.should_exercise}")
        print(f"EXPLANATION:       {decision.explanation_level}")
        print(f"CONFIDENCE:        {decision.confidence:.2f}")

        print("================================")


teacher_logger = TeacherLogger()