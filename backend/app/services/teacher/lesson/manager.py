from __future__ import annotations

from .models import LessonState

from .phases import LessonPhase

from app.services.teacher.brain.models import (
    TeacherActionPlan,
)

_PHASE_TRANSITIONS = {
    LessonPhase.CORRECTION: LessonPhase.EXPLANATION,
    LessonPhase.EXPLANATION: LessonPhase.EXAMPLE,
    LessonPhase.EXAMPLE: LessonPhase.EXERCISE,
    LessonPhase.EXERCISE: LessonPhase.ASSESSMENT,
    LessonPhase.ASSESSMENT: LessonPhase.FINISHED,
}

class LessonManager:
    """
    Gerencia o ciclo de vida de uma microaula.
    """

    def update(
        self,
        action_plan: TeacherActionPlan,
    ) -> LessonState:
        
        # ---------------------------------------------------------
        # Conversation mode
        # ---------------------------------------------------------

        if action_plan.goal != "teach":

            self.finish()

            return self.lesson

        if not self.lesson.active:
            self.lesson.active = True

            self.lesson.goal = action_plan.goal

            self.lesson.lesson_type = action_plan.lesson_type

            self.lesson.target_skill = action_plan.target_skill

            self.lesson.current_phase = LessonPhase.CORRECTION

            self.lesson.expected_turns = action_plan.expected_turns

            self.lesson.total_steps = 5

            self.lesson.current_step = 1

            self.lesson.turns_elapsed = 0

            self.lesson.completed = False

            self.lesson.completion_condition = (
                action_plan.completion_condition
            )

            self.lesson.last_teacher_action = ""

        return self.lesson
    


    def __init__(self):

        self.lesson = LessonState()

    # ---------------------------------------------------------
    # Consulta
    # ---------------------------------------------------------

    def current(self) -> LessonState:

        return self.lesson

    # ---------------------------------------------------------
    # Atualização
    # ---------------------------------------------------------

    

    # ---------------------------------------------------------
    # Avança um passo da aula
    # ---------------------------------------------------------

    def advance(self):

        if not self.lesson.active:
            return

        self.lesson.turns_elapsed += 1

        if self.lesson.current_step < self.lesson.total_steps:
            self.lesson.current_step += 1

        self._advance_phase()

    # ---------------------------------------------------------
    # Atualiza a fase atual
    # ---------------------------------------------------------

    def _advance_phase(self):

        if not self.lesson.active:
            return

        next_phase = _PHASE_TRANSITIONS.get(
            self.lesson.current_phase,
        )

        if next_phase is None:
            return

        self.lesson.current_phase = next_phase

        if next_phase == LessonPhase.FINISHED:

            self.lesson.completed = True

            self.lesson.active = False
    # ---------------------------------------------------------
    # Última ação do professor
    # ---------------------------------------------------------

    def set_last_action(
        self,
        action: str,
    ):

        self.lesson.last_teacher_action = action

    # ---------------------------------------------------------
    # Finaliza
    # ---------------------------------------------------------

    def finish(self):

        self.lesson = LessonState()


lesson_manager = LessonManager()
