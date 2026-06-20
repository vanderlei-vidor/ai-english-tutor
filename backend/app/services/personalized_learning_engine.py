def get_weakest_skill(memory_data):

    mastery = memory_data.get("skill_mastery", {})

    print(f"🎯 CURRENT SKILL MASTERY: {mastery}")

    if not mastery:
        print("🎯 NO MASTERY FOUND -> past_tense")
        return "past_tense"

    weakest_skill = max(mastery, key=mastery.get)

    print(f"🎯 WEAKEST SKILL DETECTED: {weakest_skill}")

    return weakest_skill
