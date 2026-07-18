from __future__ import annotations


class StudentStatisticsLoader:
    def load(
        self,
        student,
        context,
    ) -> None:

        student.total_attempts = 0

        student.correct_answers = 0

        student.incorrect_answers = 0

        student.total_study_time = 0

        student.average_response_time = 0.0

        student.average_sentence_length = 0.0


student_statistics_loader = StudentStatisticsLoader()
