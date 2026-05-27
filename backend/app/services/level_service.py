def detect_english_level(user_message):

    text = user_message.lower()

    words = text.split()

    # 🔥 VERY BASIC
    if len(words) <= 3:
        return "A1"

    # 🔥 SIMPLE SENTENCES
    if len(words) <= 8:
        return "A2"

    # 🔥 INTERMEDIATE
    if len(words) <= 15:
        return "B1"

    # 🔥 ADVANCED
    return "B2"