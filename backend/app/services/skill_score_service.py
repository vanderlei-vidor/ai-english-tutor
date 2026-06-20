VALID_SKILLS = {
    "past_tense",
    "articles",
    "prepositions",
    "verb_usage",
    "third_person",
    "pronouns",
}


def calculate_skill_scores(memory_data: dict) -> dict:
    """
    Combina dificuldade atual (skill_mastery)
    + histórico acumulado (weak_skills)
    em um score único por skill.
    """

    skill_mastery = memory_data.get("skill_mastery", {})
    weak_skills = memory_data.get("weak_skills", {})

    all_skills = set(skill_mastery.keys()) | set(weak_skills.keys())

    scores = {}

    for skill in all_skills:
        if skill not in VALID_SKILLS:
            continue

        mastery_value = skill_mastery.get(skill, 0)
        weak_value = weak_skills.get(skill, 0)

        # Peso maior para dificuldade atual
        final_score = (mastery_value * 0.7) + (weak_value * 0.3)

        scores[skill] = round(final_score, 2)

    return scores


def get_highest_priority_skill(memory_data: dict) -> str | None:
    """
    Retorna a skill com maior score pedagógico.
    """
    scores = calculate_skill_scores(memory_data)

    if not scores:
        return None

    return max(scores, key=scores.get)
