import random


def choose_teaching_skill(memory_data):
    mastery = memory_data.get("skill_mastery", {})

    # Se não houver dados, retorna o fallback padrão
    if not mastery:
        return "past_tense"

    skills = list(mastery.keys())

    # 🧠 LÓGICA PEDAGÓGICA: Invertemos o peso.
    # Se a maestria é 90 (alta), o peso vira 10 (muda pouco).
    # Se a maestria é 10 (baixa), o peso vira 90 (muda muito, pratica mais!).
    weights = [max(1, 100 - score) for score in mastery.values()]

    # ⚡ PERFORMANCE: random.choices faz a seleção ponderada direto na matemática,
    # sem precisar criar listas gigantescas repetindo strings na memória.
    selected_skill = random.choices(skills, weights=weights, k=1)[0]

    # Dica: Substitua por logging em produção se puder, mas para o terminal ajuda
    print(f"🎯 WEIGHTED SKILL SELECTED: {selected_skill}")

    return selected_skill
