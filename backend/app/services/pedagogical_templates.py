import random

# Banco de dados estruturado. Perfeito para virar JSON e ser consumido pelo Flutter.
EXERCISE_BANK = {
    "past_tense": [
        {
            "question": "Yesterday I _____ a mobile application.",
            "options": ["develop", "developed"],
            "correct_index": 1,  # Corresponde a 'developed'
            "explanation": "Usamos 'developed' porque 'Yesterday' indica uma ação concluída no passado (Simple Past).",
        },
        {
            "question": "Last week we _____ a new feature.",
            "options": ["create", "created"],
            "correct_index": 1,
            "explanation": "O marcador de tempo 'Last week' exige o verbo no passado simples.",
        },
        {
            "question": "Last night I _____ three episodes of Naruto.",
            "options": ["watch", "watched"],
            "correct_index": 1,
            "explanation": "Ações finalizadas no passado como 'Last night' usam o Simple Past.",
        },
    ],
    "articles": [
        {
            "question": "I bought _____ new computer yesterday.",
            "options": ["a", "an"],
            "correct_index": 0,  # Corresponde a 'a'
            "explanation": "Usamos 'a' antes de palavras que começam com som de consoante (new).",
        },
        {
            "question": "She created _____ amazing application.",
            "options": ["a", "an"],
            "correct_index": 1,  # Corresponde a 'an'
            "explanation": "Usamos 'an' antes de palavras que começam com som de vogal (amazing).",
        },
        {
            "question": "This is _____ open source tool.",
            "options": ["a", "an"],
            "correct_index": 1,
            "explanation": "Palavras com som de vogal inicial como 'open' exigem o artigo 'an'.",
        },
    ],
    "prepositions": [
        {
            "question": "I am working _____ a mobile app.",
            "options": ["on", "at"],
            "correct_index": 0,
            "explanation": "Em inglês, você trabalha 'on a project' ou 'on an app'.",
        },
        {
            "question": "The project source code is _____ GitHub.",
            "options": ["on", "in"],
            "correct_index": 0,
            "explanation": "Para plataformas digitais e sites como GitHub, a preposição correta é 'on'.",
        },
    ],
}


def get_skill_specific_exercise(skill: str) -> dict:
    """Retorna um exercício estruturado (dict) focado na skill solicitada.

    Garante o funcionamento do app e validação local caso a IA falhe.
    """
    # Se a skill não existir no banco, usa 'past_tense' como fallback seguro
    exercises = EXERCISE_BANK.get(skill, EXERCISE_BANK["past_tense"])

    # Retorna o dicionário completo do exercício selecionado
    return random.choice(exercises)
