from __future__ import annotations


class StudentIdentityLoader:
    def load(
        self,
        student,
        context,
    ) -> None:

        student.user_id = context.user_id


student_identity_loader = StudentIdentityLoader()
