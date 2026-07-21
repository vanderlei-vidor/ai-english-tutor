from __future__ import annotations

from dataclasses import dataclass

from app.services.teacher.constants.interruption_levels import InterruptionLevel


@dataclass(slots=True)
class TeacherPerception:
    """
    Tudo o que o professor percebe nesta interação.

    Nenhuma decisão é tomada aqui.
    Apenas observações.
    """

    has_error: bool = False

    detected_skill: str | None = None

    target_skill: str | None = None

    current_focus: str | None = None

    estimated_level: str | None = None

    student_confident: bool = True

    needs_intervention: bool = False


@dataclass(slots=True)
class TeacherReflection:
    """
    Interpretação pedagógica da situação.

    Ainda não existe decisão.
    Apenas pensamento.
    """

    should_continue_lesson: bool = False

    should_start_new_lesson: bool = False

    should_review: bool = False

    should_praise: bool = False

    interruption_level: InterruptionLevel = InterruptionLevel.NONE

    teaching_reason: str = ""


@dataclass(slots=True)
class TeacherActionPlan:
    """
    Plano pedagógico criado pelo professor.

    O Teacher Brain responde apenas:

    "Qual é o próximo passo ideal para o aluno?"

    As demais camadas apenas executam este plano.
    """

    # ==========================================
    # Objetivo pedagógico
    # ==========================================

    goal: str = "conversation"

    lesson_type: str = "conversation"

    # phase: str = "conversation"

    phase: str = "conversation"

    # next_step: str = "chat"

    next_step: str = "chat"

    # ==========================================
    # Skill
    # ==========================================

    target_skill: str | None = None

    # ==========================================
    # Ensino
    # ==========================================

    explanation_level: str = "normal"

    requires_exercise: bool = False

    requires_review: bool = False

    # Tipo de exercicio a ser gerado quando a aula
    # entrar na fase de exercise (multiple_choice,
    # fill_blank, sentence_correction, etc.).
    exercise_type: str | None = None

    # ==========================================
    # Planejamento
    # ==========================================

    teaching_priority: int = 0

    expected_turns: int = 1

    completion_condition: str = ""

    interruption_level: str = "none"

    conversation_policy: str = "continue"

    review_policy: str = "none"

    exercise_policy: str = "none"

    # ==========================================
    # Resposta
    # ==========================================

    teaching_mode: str = "conversation"

    action: str = "chat"

    response_style: str = "natural"

    tone: str = "friendly"

    generate_example: bool = False

    generate_exercise: bool = False

    ask_question: bool = False

    wait_for_student: bool = True

    finish_lesson: bool = False

    # ==========================================
    # Decisao / conversa
    # ==========================================

    teacher_strategy: str = ""

    teacher_action: str = "chat"

    teacher_handler: str = ""

    teacher_purpose: str = ""

    teacher_reason: str = ""

    should_teach: bool = False

    should_review: bool = False

    should_exercise: bool = False

    confidence: float = 1.0

    # ==========================================
    # Motivação
    # ==========================================

    encouragement_required: bool = False

    celebrate_success: bool = False
