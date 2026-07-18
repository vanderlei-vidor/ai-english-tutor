from __future__ import annotations

from .models import (
    StudentState,
)

from .loaders.identity_loader import (
    student_identity_loader,
)

from .loaders.statistics_loader import (
    student_statistics_loader,
)

from .loaders.mastery_loader import (
    student_mastery_loader,
)

from .loaders.preferences_loader import (
    student_preferences_loader,
)

from .loaders.review_loader import (
    student_review_loader,
)


class StudentProfileBuilder:
    """
    Constrói o StudentState.

    Cada aspecto do aluno é carregado por um Loader
    especializado, mantendo o Builder pequeno e
    fácil de evoluir.
    """

    def build(
        self,
        context,
    ) -> StudentState:

        student = StudentState()

        self._run_loaders(
            student,
            context,
        )

        student_identity_loader.load(
            student,
            context,
        )

        student_statistics_loader.load(
            student,
            context,
        )

        student_mastery_loader.load(
            student,
            context,
        )

        student_preferences_loader.load(
            student,
            context,
        )

        student_review_loader.load(
            student,
            context,
        )

        return student
    

    def _run_loaders(
        self,
        student,
        context,
    ) -> None:

        student_identity_loader.load(student, context)
        student_statistics_loader.load(student, context)
        student_mastery_loader.load(student, context)
        student_preferences_loader.load(student, context)
        student_review_loader.load(student, context)

student_profile_builder = StudentProfileBuilder()
