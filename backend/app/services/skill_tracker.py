def detect_skill(correction: str):

    text = correction.lower()

    if "went" in text:
        return "past_tense"

    if " a " in text or " an " in text:
        return "articles"

    if " on " in text:
        return "prepositions"

    return None
