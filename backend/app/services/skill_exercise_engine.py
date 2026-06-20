import random

# BANCO DE DADOS ADAPTATIVO — FASE 11.8
SKILL_EXERCISES = {
    "past_tense": {
        "A1": {
            "multiple_choice": ["Yesterday I ____ to school. (a) go (b) went"],
            "fill_blank": [
                "Complete the sentence with the past of 'go': I _____ to the park yesterday."
            ],
        },
        "A2": {
            "multiple_choice": [
                "Yesterday I ____ a mobile application. (a) develop (b) developed"
            ],
            "fill_blank": [
                "Complete with the past of 'build': The team _____ an amazing open source tool last week."
            ],
        },
        "B1": {
            "multiple_choice": [
                "Identify the mistake: 'Yesterday I have went to school.' (a) have went (b) yesterday"
            ],
            "fill_blank": [
                "Change to Simple Past: 'I am watching Naruto' becomes 'Last night, I _____ Naruto'."
            ],
        },
        "B2": {
            "multiple_choice": [
                "Rewrite using Past Perfect: 'I finished the project before the meeting.' (a) I had finished the project... (b) I have finished the project..."
            ],
            "fill_blank": [
                "Complete using Past Perfect: By the time the server crashed, we _____ (save) the code."
            ],
        },
        "C1": {
            "multiple_choice": [
                "Analyze the inversion: 'Had I known about the bug, I would have fixed it.' Is it: (a) Formal and correct (b) Informal and incorrect"
            ],
            "fill_blank": [
                "Write a short paragraph describing a difficult decision you made last year using at least three past tense verbs."
            ],
        },
    },
    # Mantidos no formato antigo conforme Passo 2 (a engine aceita os dois dinamicamente)
    "articles": {
        "multiple_choice": [
            "I bought ____ computer yesterday. (a) a (b) an",
            "She is ____ software engineer. (a) a (b) an",
        ],
        "fill_blank": [
            "Fill with 'a' or 'an': This is _____ open source tool.",
        ],
    },
    "prepositions": {
        "multiple_choice": [
            "The project code is ____ GitHub. (a) on (b) in",
            "I love to watch anime ____ night. (a) at (b) on",
        ],
        "fill_blank": [
            "Complete with the correct preposition: The book is _____ the table.",
        ],
    },
}


def get_skill_specific_exercise(
    skill: str, level: str = "A1", exercise_type: str = "multiple_choice"
) -> str:
    """Engine estática adaptativa que entrega exercícios baseados na Skill, Nível e Formato da UI."""
    
    # Passo 3: Busca a Skill. Se não achar, fallback seguro para 'past_tense'
    skill_bank = SKILL_EXERCISES.get(skill, SKILL_EXERCISES["past_tense"])

    # 🛡️ Proteção de Transição: Verifica se a skill já possui subdivisão por níveis (ex: past_tense)
    # Pegamos o primeiro item interno para checar se ele é um dicionário (nível) ou uma lista (formato antigo)
    first_item = next(iter(skill_bank.values()))

    if isinstance(first_item, dict):
        # Modelo Novo: Navega por Nível e depois por Tipo de Exercício
        level_bank = skill_bank.get(level, skill_bank["A1"])
        exercises = level_bank.get(exercise_type, level_bank["multiple_choice"])
    else:
        # Modelo Antigo (Articles / Prepositions): Ignora o nível e busca o tipo direto
        exercises = skill_bank.get(exercise_type, skill_bank["multiple_choice"])

    # Fallback de segurança caso a lista específica esteja vazia por algum motivo bizarro
    if not exercises:
        return "Write a sentence in English about your favorite technology or anime."

    # Passo 4: Telemetria e Debug no Console
    print(f"🎓 ADAPTIVE LEVEL: {level}")
    print(f"🎓 ADAPTIVE SKILL: {skill}")
    print(f"🎓 EXERCISE TYPE: {exercise_type}")

    return random.choice(exercises)
