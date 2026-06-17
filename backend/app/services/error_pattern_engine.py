def detect_known_error(text: str):
    """
    Detecta erros clássicos de estudantes A1/A2
    antes mesmo da IA decidir.
    """

    text = text.lower().strip()

    patterns = {
        "talk english": {
            "skill": "verb_usage",
            "correction": "I speak English.",
            "explanation": "Em inglês usamos 'speak English', não 'talk English'.",
        },
        "need learning": {
            "skill": "infinitive",
            "correction": "I need to learn English.",
            "explanation": "Após 'need' normalmente usamos infinitivo: need to learn.",
        },
        "she don't": {
            "skill": "third_person",
            "correction": "She doesn't.",
            "explanation": "Na terceira pessoa usamos doesn't.",
        },
        "he don't": {
            "skill": "third_person",
            "correction": "He doesn't.",
            "explanation": "Na terceira pessoa usamos doesn't.",
        },
        "go yesterday": {
            "skill": "past_tense",
            "correction": "went",
            "explanation": "Yesterday exige passado simples.",
        },
        "buyed": {
            "skill": "irregular_verbs",
            "correction": "bought",
            "explanation": "Buy é um verbo irregular.",
        },
        "goed": {
            "skill": "irregular_verbs",
            "correction": "went",
            "explanation": "Go é um verbo irregular.",
        },
        "informations": {
            "skill": "uncountable_nouns",
            "correction": "information",
            "explanation": "Information é incontável.",
        },
        "advices": {
            "skill": "uncountable_nouns",
            "correction": "advice",
            "explanation": "Advice é incontável.",
        },
        "peoples": {
            "skill": "plural_nouns",
            "correction": "people",
            "explanation": "People já é plural.",
        },
    }

    for pattern, data in patterns.items():
        if pattern in text:
            return data

    return None
