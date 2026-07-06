from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class SkillProgress:
    """
    Representa o progresso do aluno em uma habilidade específica.
    """

    # -----------------------------------------
    # Skill
    # -----------------------------------------

    skill: str

    # -----------------------------------------
    # Statistics
    # -----------------------------------------

    attempts: int = 0

    correct: int = 0

    incorrect: int = 0

    mastery: float = 0.0

    # -----------------------------------------
    # Spaced Review
    # -----------------------------------------

    last_review_day: int = 0

    next_review_day: int = 0

    # -----------------------------------------
    # Learning History
    # -----------------------------------------

    recent_errors: list[str] = field(default_factory=list)

    completed_lessons: int = 0

    completed_exercises: int = 0

    streak: int = 0


@dataclass(slots=True)
class LearningProfile:
    """
    Estado atual de aprendizado do aluno.
    """

    # -----------------------------------------
    # Identificação
    # -----------------------------------------

    student_id: str = "anonymous"

    cefr_level: str = "A1"

    # -----------------------------------------
    # Estatísticas gerais
    # -----------------------------------------

    total_sentences: int = 0

    total_lessons: int = 0

    total_exercises: int = 0

    overall_accuracy: float = 0.0

    # -----------------------------------------
    # Aprendizagem
    # -----------------------------------------

    mastered_skills: list[str] = field(default_factory=list)

    weak_skills: list[str] = field(default_factory=list)

    current_focus: str | None = None

    skill_progress: dict[str, SkillProgress] = field(default_factory=dict)

    # -----------------------------------------
    # Futuro
    # -----------------------------------------

    completed_concepts: list[str] = field(default_factory=list)

    recommended_concepts: list[str] = field(default_factory=list)

    review_queue: list[str] = field(default_factory=list)
