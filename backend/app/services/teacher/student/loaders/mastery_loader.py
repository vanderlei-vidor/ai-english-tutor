
"""
Temporary loader.

In future versions this loader will retrieve the
student learning profile from StudentRepository.
"""
from __future__ import annotations


class StudentMasteryLoader:
    """
    Carrega informações permanentes de domínio do aluno.

    Atualmente utiliza dados disponíveis no PedagogicalAnalysis.
    Futuramente utilizará o StudentRepository.
    """
    def load(
        self,
        student,
        context,
    ) -> None:

        pedagogical = context.pedagogical

        student.mastery = getattr(
            pedagogical,
            "mastery",
            0.0,
        )

        student.current_skill = getattr(
            pedagogical,
            "target_skill",
            "",
        )

        student.weak_skills = list(
            getattr(
                pedagogical,
                "weak_skills",
                [],
            )
        )


student_mastery_loader = StudentMasteryLoader()
