from __future__ import annotations

from .step_executor import (
    step_executor,
)


class TeachingExecutor:
    """
    Executa o passo atual do Teaching Script.
    """

    def execute(
        self,
        lesson,
        script,
        target_skill: str | None = None,
    ):

        step = script.current_step(
            lesson.current_step,
        )

        handler = step_executor.get(
            step.action,
        )

        print()

        print("=" * 60)
        print("TEACHING EXECUTOR")
        print("=" * 60)

        print("STEP :", lesson.current_step)

        print("ACTION:", step.action)

        print("HANDLER:", handler.__class__.__name__)

        print("=" * 60)

        return handler.execute(
            step,
            target_skill=target_skill,
        )


teaching_executor = TeachingExecutor()
