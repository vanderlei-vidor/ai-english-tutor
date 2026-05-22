from datetime import date, timedelta
from app.models.weekly_xp import WeeklyXP
from app.models.weekly_results import WeeklyResult
from app.models.system_state import SystemState
from app.services.ranking_service import get_league_from_percentage
from app.models.user import User
from app.services.ranking_service import LEAGUE_ORDER

def check_and_close_week(db):

    today = date.today()
    current_week_start = today - timedelta(days=today.weekday())

    state = db.query(SystemState).first()

    if not state:
        return

    # Se já fechou essa semana → não faz nada
    if state.last_closed_week == current_week_start:
        return

    # Buscar ranking da semana anterior
    results = (
        db.query(WeeklyXP)
        .filter(WeeklyXP.week_start == state.last_closed_week)
        .order_by(WeeklyXP.total_xp.desc())
        .all()
    )

    total_users = len(results)
    position = 1

    for record in results:

        top_percentage = round((position / total_users) * 100)

        user = db.query(User).filter(User.id == record.user_id).first()
        current_league = user.current_league
        current_index = LEAGUE_ORDER.index(current_league)

        if top_percentage <= 20 and current_index < len(LEAGUE_ORDER) - 1:
            new_league = LEAGUE_ORDER[current_index + 1]

        elif top_percentage >= 80 and current_index > 0:
            new_league = LEAGUE_ORDER[current_index - 1]

        else:
            new_league = current_league

        user.current_league = new_league
        league = get_league_from_percentage(top_percentage)

        weekly_result = WeeklyResult(
            user_id=record.user_id,
            week_start=state.last_closed_week,
            final_position=position,
            final_xp=record.total_xp,
            league=league["name"]
        )

        db.add(weekly_result)

        position += 1

    # Atualiza controle
    state.last_closed_week = current_week_start
    db.commit()
