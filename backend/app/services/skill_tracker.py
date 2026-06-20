import re

# 🎯 Dicionário de mapeamento: Categoria -> Lista de padrões Regex com \b (fronteiras de palavra)
# A ordem das chaves aqui dita a PRIORIDADE de detecção caso a frase tenha mais de um elemento.
SKILL_PATTERNS = {
    "past_tense": [
        r"\b(did|went|was|were|had|yesterday|ago)\b",
        r"\w+ed\b",  # Captura qualquer verbo regular terminado em 'ed' (walked, played, watched)
    ],
    "articles": [r"\b(a|an|the)\b"],
    "prepositions": [r"\b(at|on|in|with|for|to|about|of|by)\b"],
    "pronouns": [r"\b(he|she|they|his|her|your|my|i|you|we|it|him|them|us|our)\b"],
}


def detect_skill(correction: str) -> str | None:
    """
    Analisa a frase corrigida e identifica qual habilidade (skill)
    ela provavelmente está testando ou corrigindo.
    """
    if not correction or not isinstance(correction, str):
        return None

    # Deixa tudo em minúsculo e limpa espaços nas pontas
    text = correction.lower().strip()

    # Percorre o mapa de habilidades usando o motor de busca Regex
    for skill, regex_list in SKILL_PATTERNS.items():
        for pattern in regex_list:
            if re.search(pattern, text):
                return skill

    return None
