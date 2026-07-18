from __future__ import annotations


class StudentReviewLoader:
    def load(
        self,
        student,
        context,
    ) -> None:

        pedagogical = context.pedagogical

        student.review_required = getattr(
            pedagogical,
            "review_required",
            False,
        )

        student.exercise_required = getattr(
            pedagogical,
            "exercise_required",
            False,
        )


student_review_loader = StudentReviewLoader()
