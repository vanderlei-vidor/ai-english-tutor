def is_real_correction_by_skill(
    correction: str,
    teacher_action: str = "",
    needs_correction: bool = False,
    target_skill: str | None = None,
) -> bool:
    """
    Decide se a correction representa um erro real do aluno
    ou se é só uma resposta genérica / lixo do modelo.

    Regras:
    - Se needs_correction=False -> não houve erro
    - Se teacher_action != correction -> não houve erro
    - Se correction for "Correct! ✨" ou elogio genérico -> não houve erro
    - Se houver target_skill, a correction precisa combinar com a skill
    """

    if not correction or not isinstance(correction, str):
        return False

    text = correction.strip().lower()

    # 1) Se a IA disse que não precisa corrigir, então não houve erro
    if not needs_correction:
        return False

    # 2) Se a ação não é correction, também não tratamos como erro
    if teacher_action != "correction":
        return False

    # 3) Respostas genéricas que NÃO representam correção real
    generic_responses = {
        "correct! ✨",
        "correct!",
        "great!",
        "great job!",
        "excellent!",
        "well done!",
        "good job!",
        "very good!",
        "nice!",
        "perfect!",
    }

    if text in generic_responses:
        return False

    # 4) Se não temos target_skill, fazemos uma validação mínima
    #    (aceita porque ainda pode ser uma correção real)
    if not target_skill:
        return True

    # 5) Marcadores por skill
    skill_markers = {
        "past_tense": [
            "yesterday",
            "ago",
            "last",
            "went",
            "was",
            "were",
            "did",
            "had",
            "bought",
        ],
        "articles": [" a ", " an ", " the ", "article", "an apple", "a car"],
        "prepositions": [
            " at ",
            " on ",
            " in ",
            " to ",
            " for ",
            " with ",
            "depend on",
            "married to",
            "good at",
        ],
        "third_person": ["doesn't", "he", "she", "it"],
        "verb_usage": ["speak english", "need to", "use", "verb"],
        "pronouns": ["he", "she", "they", "his", "her", "them", "we", "our"],
        "infinitive": ["to learn", "to go", "to study", "infinitive"],
        "irregular_verbs": ["went", "bought", "saw", "ate", "had", "did"],
        "plural_nouns": ["people", "children", "men", "women"],
        "uncountable_nouns": ["information", "advice", "furniture", "money"],
    }

    markers = skill_markers.get(target_skill)

    # Se não conhecemos a skill, melhor aceitar do que bloquear tudo
    if not markers:
        return True

    # 6) A correction precisa ter pelo menos 1 marcador da skill-alvo
    if any(marker in text for marker in markers):
        return True

    # 7) Se não bate com a skill esperada, tratamos como lixo/erro do modelo
    return False
