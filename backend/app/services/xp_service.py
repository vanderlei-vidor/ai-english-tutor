



def calculate_xp(score: int, had_error: bool, current_streak: int):

    xp = 5  # base por enviar mensagem

    if had_error:
        xp += 2
    else:
        xp += 10

    xp += current_streak  # bônus streak

    return xp

import math

def get_level_from_xp(total_xp: int):

    level = 1

    # Descobrir nível atual
    while total_xp >= xp_needed_for_level(level + 1):
        level += 1

    current_level_xp_floor = xp_needed_for_level(level)
    next_level_xp = xp_needed_for_level(level + 1)

    xp_into_level = total_xp - current_level_xp_floor
    xp_required_this_level = next_level_xp - current_level_xp_floor

    progress_percentage = int((xp_into_level / xp_required_this_level) * 100)

    return {
        "level": level,
        "current_xp": total_xp,
        "next_level_xp": next_level_xp,
        "progress_percentage": min(progress_percentage, 100)
    }


def xp_needed_for_level(level: int):
    if level == 1:
        return 0
    return 100 * ((level - 1) ** 2)