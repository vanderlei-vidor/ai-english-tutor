import random

# Banco de dados estruturado por Skill e por Formato esperado pela UI
SKILL_EXERCISES = {
    "past_tense": {
        "multiple_choice": [
            "Yesterday I ____ a mobile application. (a) develop (b) developed",
            "Last night she ____ a new episode of Naruto. (a) watch (b) watched",
            "The programmer ____ the bug 5 minutes ago. (a) fix (b) fixed",
        ],
        "fill_blank": [
            "Fill the blank with Past Tense: Yesterday I _____ (to go) to school.",
            "Complete the sentence: Naruto _____ (to want) to become Hokage in the past.",
        ],
        "sentence_correction": [
            "Correct the error in past tense: Yesterday I go to work.",
            "Fix the grammatical mistake: Last week we create a new layout.",
        ],
    },
    "articles": {
        "multiple_choice": [
            "I bought ____ computer yesterday. (a) a (b) an",
            "She is ____ software engineer. (a) a (b) an",
            "He wants to be ____ Hokage. (a) a (b) an",
        ],
        "fill_blank": [
            "Fill with 'a' or 'an': This is _____ open source tool.",
            "Complete the sentence: I found _____ bug in the application.",
        ],
        "sentence_correction": [
            "Correct the article error: I bought computer yesterday.",
            "Fix the missing article: She is engineer.",
        ],
    },
    "prepositions": {
        "multiple_choice": [
            "I arrived ____ the station. (a) at (b) in",
            "The project code is ____ GitHub. (a) on (b) in",
            "I love to watch anime ____ night. (a) at (b) on",
        ],
        "fill_blank": [
            "Complete with the correct preposition: The book is _____ the table.",
            "Fill the blank: I am working _____ a mobile app right now.",
        ],
        "sentence_correction": [
            "Correct the preposition: I arrived in the airport.",
            "Fix the mistake: The developer is sitting in his desk.",
        ],
    },
}


def get_skill_specific_exercise(
    skill: str, exercise_type: str = "multiple_choice"
) -> str:
    """Engine estática avançada que entrega exercícios baseados na Skill e no Formato correto para a UI."""

    # 1. Busca a Skill solicitada. Se não existir, usa 'past_tense' como padrão de segurança
    skill_bank = SKILL_EXERCISES.get(skill, SKILL_EXERCISES["past_tense"])

    # 2. Busca o Formato esperado pelo Flutter. Se não existir, usa 'multiple_choice' como padrão
    exercises = skill_bank.get(exercise_type, skill_bank["multiple_choice"])

    # 3. Se por algum motivo bizarro a lista estiver vazia, entrega um fallback universal de escrita
    if not exercises:
        return "Write a sentence in English about your favorite technology or anime."

    return random.choice(exercises)
