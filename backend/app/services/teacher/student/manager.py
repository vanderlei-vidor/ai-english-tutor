from __future__ import annotations


from .profile_builder import (
    student_profile_builder,
)


class StudentManager:
    def load(
        self,
        context,
    ):

        return student_profile_builder.build(
            context,
        )


student_manager = StudentManager()