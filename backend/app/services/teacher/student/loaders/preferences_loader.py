from __future__ import annotations


class StudentPreferencesLoader:
    def load(
        self,
        student,
        context,
    ) -> None:

        pedagogical = context.pedagogical

        student.learning_speed = getattr(
            pedagogical,
            "learning_speed",
            1.0,
        )

        student.learning_style = getattr(
            pedagogical,
            "learning_style",
            "",
        )

        student.preferred_examples = getattr(
            pedagogical,
            "preferred_examples",
            False,
        )


student_preferences_loader = StudentPreferencesLoader()
