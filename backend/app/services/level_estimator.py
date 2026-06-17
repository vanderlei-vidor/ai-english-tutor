# Configuração centralizada de pesos (Clean Code)
STRUCTURE_WEIGHTS = {
    "present_perfect": 2,
    "conditional": 4,
    "past_perfect": 3,
    "inversion": 5,
}


def calculate_level_score(advanced_structures: dict) -> int:
    """Calcula o score acumulado aplicando um teto para evitar 'farming' de pontos."""
    score = 0
    for structure, weight in STRUCTURE_WEIGHTS.items():
        count = advanced_structures.get(structure, 0)

        # 🛡️ Proteção: Conta no máximo até 15 repetições de cada estrutura.
        # Isso força o usuário a diversificar a gramática para continuar subindo.
        safe_count = min(count, 15)

        score += safe_count * weight
    return score


def estimate_level(advanced_structures: dict) -> str:
    """Estima o nível CEFR reaproveitando o cálculo de score unificado."""
    # Evita duplicação: usa a função parceira para pegar o score atualizado
    score = calculate_level_score(advanced_structures)

    # Validação dos limites de nível (Claro e escalável)
    if score <= 3:
        return "A1"

    elif score <= 8:
        return "A2"

    elif score <= 15:
        return "B1"

    elif score <= 25:
        return "B2"

    elif score <= 40:
        return "C1"

    return "C2"
