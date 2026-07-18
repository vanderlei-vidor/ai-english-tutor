from __future__ import annotations


class MemoryStateSync:
    def synchronize(
        self,
        state,
        pedagogical,
    ) -> None:

        student = state.student

        student.mastery = getattr(
            pedagogical,
            "mastery",
            0.0,
        )

        student.estimated_level = getattr(
            pedagogical,
            "estimated_level",
            "",
        )

        student.review_required = getattr(
            pedagogical,
            "requires_review",
            False,
        )

        student.exercise_required = getattr(
            pedagogical,
            "exercise_required",
            False,
        )

        # ==========================
        # Skill Focus
        # ==========================

        state.skill_focus.recommended = getattr(
            pedagogical,
            "target_skill",
            None,
        )

        weak_skills = getattr(
            pedagogical,
            "weak_skills",
            [],
        )

        state.skill_focus.weakest = weak_skills[0] if weak_skills else None


memory_state_sync = MemoryStateSync()
