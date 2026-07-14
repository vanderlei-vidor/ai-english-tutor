from __future__ import annotations

from .perception import (
    teacher_perception_engine,
)

from .reflection import (
    teacher_reflection_engine,
)

from .planning import (
    teacher_planning_engine,
)
from .state import (
    TeacherBrainState,
)
from app.services.teacher.lesson.manager import (
    lesson_manager,
)
from app.services.teacher.response.planner import (
    teacher_response_planner,
)
from app.services.teacher.prompt.builder import (
    teacher_prompt_builder,
)

class TeacherBrain:
    """
    Cérebro do Professor.

    Observa.

    Reflete.

    Planeja.

    Ainda não executa.
    """

    def think(
        self,
        context,
    ):

        perception = teacher_perception_engine.perceive(
            context,
        )

        reflection = teacher_reflection_engine.reflect(
            perception,
        )

        plan = teacher_planning_engine.plan(
            perception,
            reflection,
        )

        lesson = lesson_manager.update(
            plan,
        )

        if lesson.active:

            plan = teacher_planning_engine.apply_lesson_phase(
                plan,
                lesson,
            )

        response = teacher_response_planner.create_response_plan(
            plan,
        )
        teacher_prompt = teacher_prompt_builder.build(
            plan,
        )

        return TeacherBrainState(
            perception=perception,
            reflection=reflection,
            planning=plan,
            lesson=lesson,
            response=response,
            prompt=teacher_prompt,
        )


teacher_brain = TeacherBrain()
