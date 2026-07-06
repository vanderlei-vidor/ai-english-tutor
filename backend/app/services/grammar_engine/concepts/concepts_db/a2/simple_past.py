from __future__ import annotations

from app.services.grammar_engine.concepts.models import GrammarConcept


SIMPLE_PAST = GrammarConcept(
    id="simple_past",
    name="Simple Past",
    level="A2",
    skill="past_tense",
    description="Used to describe completed actions in the past.",
    prerequisites=[
        "verbs",
        "regular_verbs",
        "irregular_verbs",
    ],
    examples=[
        "I went yesterday.",
        "She studied English.",
        "We bought a car.",
    ],
    common_errors=[
        "I go yesterday.",
        "We buy it last week.",
    ],
    teaching_priority=10,
    exercise_difficulty="easy",
    estimated_study_minutes=25,
    review_after_days=7,
    mastery_threshold=90,
    related_concepts=[
        "regular_verbs",
        "irregular_verbs",
    ],
    next_concepts=[
        "past_continuous",
        "present_perfect",
    ],
)
