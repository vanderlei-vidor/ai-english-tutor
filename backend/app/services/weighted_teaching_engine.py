from app.services.skill_score_service import (
    calculate_skill_scores,
    get_highest_priority_skill,
)


def choose_teaching_skill(memory_data: dict) -> str:
    """
    Escolhe a skill pedagógica prioritária com base
    na pontuação normalizada entre:
    - dificuldade atual (skill_mastery)
    - histórico acumulado de erros (weak_skills)
    """

    skill_scores = calculate_skill_scores(memory_data)

    print("======== NORMALIZED SKILL SCORES ========")
    for skill, score in skill_scores.items():
        print(f"{skill}: {score}")
    print("=========================================")

    if not skill_scores:
        print("⚠️ NO SKILL SCORES FOUND - FALLBACK TO past_tense")
        return "past_tense"

    target_skill = get_highest_priority_skill(memory_data)

    print(f"🎯 NORMALIZED SKILL SELECTED: {target_skill}")

    return target_skill or "past_tense"
