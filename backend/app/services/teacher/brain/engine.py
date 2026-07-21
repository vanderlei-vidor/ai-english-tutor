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
from app.services.teacher.prompt.builder import (
    teacher_prompt_builder,
)
from app.services.teacher.state.models import (
    TeachingState,
)

from app.services.teacher.state.memory_sync import (
    memory_state_sync,
)

from app.services.teacher.student.manager import (
    student_manager,
)
from app.services.teacher.pedagogy.engine import (
    teaching_engine,
)
from app.services.teacher.pedagogy.executor import (
    teaching_executor,
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
        state = TeachingState()

        state.memory_data = getattr(
            context,
            "memory_data",
            {},
        ) or {}

        student = student_manager.load(
            context,
        )

        state.student = student

        perception = teacher_perception_engine.perceive(
            context=context,
            state=state,
        )

        memory_state_sync.synchronize(
            state,
            context,
        )

        reflection = teacher_reflection_engine.reflect(
            perception=perception,
            state=state,
        )

        plan = teacher_planning_engine.plan(
            perception=perception,
            reflection=reflection,
            state=state,
        )

        teaching = teaching_engine.build(state,)

        lesson = lesson_manager.update(
            action_plan=plan,
            state=state,
        )

        if lesson.active:

            plan = teacher_planning_engine.apply_lesson_phase(
                plan,
                lesson,
                memory_data=state.memory_data,
            )
        execution = teaching_executor.execute(
            lesson=lesson,
            script=teaching.script,
            target_skill=plan.target_skill,
        )
        teacher_prompt = teacher_prompt_builder.build(
            plan=plan,
            execution=execution,
        )

        print()

        print("=" * 60)
        print("TEACHING EXECUTION")
        print("=" * 60)

        print("HANDLER :", execution.handler)

        print("PURPOSE :", execution.step.purpose)

        print("WAIT :", execution.wait_student)

        print("QUESTION :", execution.ask_question)

        print("REVEAL :", execution.reveal_answer)

        print()

        print(execution.prompt_instruction)

        print("=" * 60)

        return TeacherBrainState(
            state=state,
            student=student,
            perception=perception,
            reflection=reflection,
            planning=plan,
            teaching=teaching,
            execution=execution,
            lesson=lesson,
            prompt=teacher_prompt,
        )


teacher_brain = TeacherBrain()
