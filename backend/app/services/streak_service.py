from datetime import date, timedelta


def update_streak(streak_record):

    today = date.today()

    # Primeira vez
    if not streak_record.last_study_date:
        streak_record.current_streak = 1
        streak_record.longest_streak = 1
        streak_record.last_study_date = today
        return streak_record

    # Se já estudou hoje
    if streak_record.last_study_date == today:
        return streak_record

    # Se estudou ontem → continua streak
    if streak_record.last_study_date == today - timedelta(days=1):
        streak_record.current_streak += 1

        if streak_record.current_streak > streak_record.longest_streak:
            streak_record.longest_streak = streak_record.current_streak

    else:
        # Quebrou streak
        streak_record.current_streak = 1

    streak_record.last_study_date = today

    return streak_record