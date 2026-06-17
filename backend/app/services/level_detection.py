import re

# BANCO DE PADRÕES AVANÇADOS - FASE 11.5
ADVANCED_PATTERNS = {
    "present_perfect": [
        r"\bhave\s+been\b",
        r"\bhas\s+been\b",
        r"\bhave\s+[a-z]+ed\b",
        r"\bhas\s+[a-z]+ed\b",
        r"\bhave\s+(?:gone|seen|done|written|known)\b",
        r"\bhas\s+(?:gone|seen|done|written|known)\b",
    ],
    "past_perfect": [
        # O (?:i\s+)? permite capturar tanto o formato normal (had known) quanto o invertido (had I known)
        r"\bhad\s+(?:i\s+)?(?:been|known|gone|seen|done|written|taken|made|[a-z]+ed)\b",
    ],
    "conditional": [
        r"\bwould\s+have\b",
        r"\bcould\s+have\b",
        r"\bshould\s+have\b",
    ],
    "inversion": [
        r"\bhad\s+i\b",
        r"\bwere\s+i\b",
        r"\bnot\s+only\s+had\b",
    ],
}


def detect_advanced_structures(text: str):
    text = text.lower()
    score = 0
    detected = []

    for skill, patterns in ADVANCED_PATTERNS.items():
        for pattern in patterns:
            # re.search procura o padrão regex respeitando os limites das palavras
            if re.search(pattern, text):
                score += 1
                detected.append(skill)
                break  # Evita duplicar a mesma skill se houver mais de um padrão correspondido

    return score, detected


def calculate_complexity_points(score: int):
    # Dicionário de mapeamento limpo (Clean Code)
    points_map = {0: 0, 1: 5, 2: 15}

    # Se o score for 3 ou mais, retorna 25. Caso contrário, busca no mapa.
    return 25 if score >= 3 else points_map.get(score, 0)
