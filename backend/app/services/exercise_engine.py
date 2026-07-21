import random

AVAILABLE_TYPES = [
    "multiple_choice",
    "fill_blank",
    "sentence_correction",
    "sentence_reordering",
    "verb_transformation",
]


def choose_exercise_type(memory_data):
    # Garante que puxa uma lista caso venha nulo do banco
    recent = memory_data.get("recent_exercise_types", [])
    if not isinstance(recent, list):
        recent = []

    # Evita repetir os últimos 3 tipos de exercícios aplicados
    allowed = [t for t in AVAILABLE_TYPES if t not in recent[-3:]]

    if not allowed:
        allowed = AVAILABLE_TYPES

    return random.choice(allowed)
