from __future__ import annotations

from app.services.teacher.student.skill_selector import (
    student_skill_selector,
)


class MemoryStateSync:
    def synchronize(
        self,
        state,
        context,
    ) -> None:

        pedagogical = context.pedagogical

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

        # ==========================
        # Adaptive Target Skill
        #
        # Quando nao ha erro gramatical detectado nesta interacao,
        # o Brain seleciona a skill prioritaria via algoritmo ponderado
        # (mastery 70% + weak_skills 30%) — absorvido do
        # weighted_teaching_engine.choose_teaching_skill().
        # ==========================

        if not state.has_error:

            memory_data = getattr(
                context,
                "memory_data",
                None,
            )

            if memory_data:

                adaptive_skill = student_skill_selector.select(
                    memory_data,
                )

                if adaptive_skill:

                    state.target_skill = adaptive_skill

                    state.skill_focus.teaching = adaptive_skill


memory_state_sync = MemoryStateSync()
