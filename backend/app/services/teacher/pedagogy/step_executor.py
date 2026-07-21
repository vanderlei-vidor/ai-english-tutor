from __future__ import annotations

from .step_handlers.correction import (
    CorrectionHandler,
)

from .step_handlers.explanation import (
    ExplanationHandler,
)

from .step_handlers.question import (
    QuestionHandler,
)

from .step_handlers.hint import (
    HintHandler,
)

from .step_handlers.example import (
    ExampleHandler,
)

from .step_handlers.exercise import (
    ExerciseHandler,
)

from .step_handlers.feedback import (
    FeedbackHandler,
)

from .step_handlers.finish import (
    FinishHandler,
)


class StepExecutor:
    def __init__(self):

        self._handlers = {
            "correction": CorrectionHandler(),
            "question": QuestionHandler(),
            "hint": HintHandler(),
            "explanation": ExplanationHandler(),
            "example": ExampleHandler(),
            "exercise": ExerciseHandler(),
            "feedback": FeedbackHandler(),
            "finish": FinishHandler(),
        }

    def get(
        self,
        action: str,
    ):

        handler = self._handlers.get(action)

        if handler is None:
            raise ValueError(f"Unknown teaching action: {action}")

        return handler


step_executor = StepExecutor()
