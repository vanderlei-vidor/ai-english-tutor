import json

def calculate_score(messages):

    total_user_messages = 0
    errors = 0

    for i in range(len(messages) - 1):

        current_msg = messages[i]
        next_msg = messages[i + 1]

        if current_msg.sender == "user" and next_msg.sender == "ai":
            total_user_messages += 1

            try:
                ai_json = json.loads(next_msg.content)

                if ai_json.get("correction"):
                    errors += 1

            except Exception:
                pass

    if total_user_messages == 0:
        return 100

    accuracy = 100 - int((errors / total_user_messages) * 100)

    return max(0, accuracy)


def calculate_global_score(progress_records):

    if not progress_records:
        return 0

    total = sum(p.score for p in progress_records)
    return int(total / len(progress_records))


def get_level(score: int):

    if score < 40:
        return {"code": "A1", "label": "Beginner"}
    elif score < 60:
        return {"code": "A2", "label": "Elementary"}
    elif score < 75:
        return {"code": "B1", "label": "Intermediate"}
    elif score < 85:
        return {"code": "B2", "label": "Upper Intermediate"}
    elif score < 95:
        return {"code": "C1", "label": "Advanced"}
    else:
        return {"code": "C2", "label": "Proficient"}


def get_next_level(current_score: int):

    levels = [
        (0, "A1", 40),
        (40, "A2", 60),
        (60, "B1", 75),
        (75, "B2", 85),
        (85, "C1", 95),
        (95, "C2", 100)
    ]

    for min_score, code, next_threshold in levels:
        if current_score < next_threshold:
            progress = int((current_score / next_threshold) * 100)

            return {
                "target_level": code,
                "required_score": next_threshold,
                "progress_percentage": min(progress, 100)
            }

    return {
        "target_level": "C2",
        "required_score": 100,
        "progress_percentage": 100
    }