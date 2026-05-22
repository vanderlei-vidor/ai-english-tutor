from datetime import date
from app.models.league_history import LeagueHistory
from app.models.xp import XP
from app.models.weekly_xp import WeeklyXP
from app.models.user import User

def close_season(db):

    today = date.today()
    season_month = today.strftime("%Y-%m")

    ranking = (
        db.query(User.id, XP.total_xp, User.current_league)
        .join(XP, XP.user_id == User.id)
        .order_by(XP.total_xp.desc())
        .all()
    )

    position = 1

    for user in ranking:

        # 🔹 1️⃣ Salvar histórico
        history = LeagueHistory(
            user_id=user.id,
            season_month=season_month,
            league=user.current_league,
            final_position=position,
            total_xp=user.total_xp
        )
        db.add(history)

        # 🔹 2️⃣ Resetar XP global
        xp_record = db.query(XP).filter(
            XP.user_id == user.id
        ).first()

        if xp_record:
            xp_record.total_xp = 0

        position += 1

    # 🔹 3️⃣ Limpar Weekly XP
    db.query(WeeklyXP).delete()

    db.commit()
