from __future__ import annotations

from .models import TeachingBehavior


class BehaviorBuilder:
    """
    Define o comportamento esperado para cada Handler.

    Não gera texto de prompt.
    Apenas configura o comportamento pedagógico.
    """

    def build(
        self,
        execution,
    ) -> TeachingBehavior:

        behavior = TeachingBehavior()

        match execution.handler:
            # --------------------------------------------------
            # Question
            # --------------------------------------------------

            case "QuestionHandler":
                behavior.ask_question = True
                behavior.wait_student = True
                behavior.reveal_answer = False

                behavior.instructions.extend(
                    [
                        "Ask one question.",
                        "Guide reasoning.",
                    ]
                )

                behavior.constraints.extend(
                    [
                        "Never reveal the answer.",
                        "Do not correct immediately.",
                    ]
                )

            # --------------------------------------------------
            # Correction
            # --------------------------------------------------

            case "CorrectionHandler":
                behavior.reveal_answer = True

                behavior.instructions.extend(
                    [
                        "Correct the sentence.",
                        "Explain briefly.",
                    ]
                )

            # --------------------------------------------------
            # Hint
            # --------------------------------------------------

            case "HintHandler":
                behavior.wait_student = True

                behavior.instructions.extend(
                    [
                        "Give one hint.",
                    ]
                )

                behavior.constraints.extend(
                    [
                        "Do not reveal the answer.",
                    ]
                )

            # --------------------------------------------------
            # Exercise
            # --------------------------------------------------

            case "ExerciseHandler":
                behavior.ask_question = True
                behavior.wait_student = True

                behavior.instructions.extend(
                    [
                        "Generate one exercise.",
                    ]
                )

            # --------------------------------------------------
            # Feedback
            # --------------------------------------------------

            case "FeedbackHandler":
                behavior.instructions.extend(
                    [
                        "Provide encouraging feedback.",
                    ]
                )

            # --------------------------------------------------
            # Finish
            # --------------------------------------------------

            case "FinishHandler":
                behavior.instructions.extend(
                    [
                        "Finish the lesson naturally.",
                    ]
                )

            # --------------------------------------------------
            # Default
            # --------------------------------------------------

            case _:
                behavior.instructions.extend(
                    [
                        "Answer naturally.",
                    ]
                )

        return behavior


behavior_builder = BehaviorBuilder()
