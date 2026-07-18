from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class StudentState:
    # ==========================================================
    # Identity
    # ==========================================================

    user_id: str = ""

    # ==========================================================
    # Learning Profile
    # ==========================================================

    estimated_level: str = ""

    current_skill: str = ""

    mastery: float = 0.0

    accuracy: float = 0.0

    # ==========================================================
    # Statistics
    # ==========================================================

    total_attempts: int = 0

    correct_answers: int = 0

    incorrect_answers: int = 0

    total_study_time: int = 0

    average_response_time: float = 0.0

    average_sentence_length: float = 0.0

    # ==========================================================
    # Preferences
    # ==========================================================

    learning_speed: float = 1.0

    learning_style: str = ""

    preferred_examples: bool = False

    # ==========================================================
    # Review
    # ==========================================================

    review_required: bool = False

    exercise_required: bool = False

    weak_skills: list[str] = field(default_factory=list)

    # ==========================================================
    # Progress
    # ==========================================================

    last_skill: str = ""

    last_error: str = ""

    consecutive_errors: int = 0

    consecutive_successes: int = 0

    
