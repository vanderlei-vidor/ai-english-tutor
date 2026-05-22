from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.user import User
from app.models.schemas import UserCreate
import uuid
from app.models.progress import Progress
from app.models.user_badge import UserBadge
from app.models.badge import Badge
from app.models.xp import XP
from app.models.user_badge import UserBadge
from app.models.badge import Badge
from app.models.xp import XP
from app.models.user import User
from app.services.ranking_service import get_league_from_percentage
from datetime import date, timedelta
from app.models.weekly_xp import WeeklyXP
from app.services.ranking_service import get_league_from_percentage
from app.models.streak import Streak
from app.services.season_service import close_season
from app.services.weekly_service import check_and_close_week


from app.services.score_service import (
    calculate_global_score,
    get_level,
    get_next_level
)


router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/users")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    new_user = User(
        id=str(uuid.uuid4()),
        email=user.email,
        password_hash=user.password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "Usuário criado com sucesso!", "user_id": new_user.id}

@router.post("/admin/close-week")
def close_week_endpoint(db: Session = Depends(get_db)):
    check_and_close_week(db)
    return {"message": "Semana encerrada com sucesso"}


@router.get("/progress/{user_id}")
def get_user_progress(user_id: str, db: Session = Depends(get_db)):

    records = db.query(Progress).filter(
        Progress.user_id == user_id
    ).all()

    global_score = calculate_global_score(records)
    level = get_level(global_score)
    meta = get_next_level(global_score)

    streak = db.query(Streak).filter(
        Streak.user_id == user_id
    ).first()

    return {
        "total_conversations": len(records),
        "global_score": global_score,
        "level": level,
        "meta": meta,
        "streak": {
            "current": streak.current_streak if streak else 0,
            "longest": streak.longest_streak if streak else 0
        }
    }


@router.get("/badges/{user_id}")
def get_user_badges(user_id: str, db: Session = Depends(get_db)):

    results = (
        db.query(Badge)
        .join(UserBadge, Badge.id == UserBadge.badge_id)
        .filter(UserBadge.user_id == user_id)
        .all()
    )

    badge_list = []

    for badge in results:
        badge_list.append({
            "code": badge.code,
            "title": badge.title,
            "description": badge.description,
            "icon": badge.icon,
            "category": badge.category
        })

    return {
        "total_badges": len(badge_list),
        "badges": badge_list
    }

@router.get("/profile/{user_id}")
def get_user_profile(user_id: str, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.id == user_id).first()

    records = db.query(Progress).filter(
        Progress.user_id == user_id
    ).all()

    global_score = calculate_global_score(records)
    level = get_level(global_score)
    meta = get_next_level(global_score)

    streak = db.query(Streak).filter(
        Streak.user_id == user_id
    ).first()

    xp_record = db.query(XP).filter(
        XP.user_id == user_id
    ).first()

    from app.services.xp_service import get_level_from_xp

    xp_data = {
        "total_xp": xp_record.total_xp if xp_record else 0,
        "level_data": get_level_from_xp(xp_record.total_xp if xp_record else 0)
    }

    return {
        "user_id": user_id,

        "user_league": user.current_league if user else "Bronze",

        "stats": {
            "total_conversations": len(records),
            "global_score": global_score
        },

        "level": level,
        "meta": meta,

        "streak": {
            "current": streak.current_streak if streak else 0,
            "longest": streak.longest_streak if streak else 0
        },

        "xp": xp_data
    }

@router.get("/ranking/weekly")
def get_weekly_ranking(db: Session = Depends(get_db)):

    today = date.today()
    week_start = today - timedelta(days=today.weekday())

    results = (
        db.query(User.id, User.email, WeeklyXP.total_xp)
        .join(WeeklyXP, WeeklyXP.user_id == User.id)
        .filter(WeeklyXP.week_start == week_start)
        .order_by(WeeklyXP.total_xp.desc())
        .limit(20)
        .all()
    )

    total_users = len(results)
    ranking = []
    position = 1

    for user in results:
        top_percentage = round((position / total_users) * 100) if total_users > 0 else 100
        league = get_league_from_percentage(top_percentage)

        ranking.append({
            "position": position,
            "user_id": user.id,
            "email": user.email,
            "weekly_xp": user.total_xp,
            "league": league
        })

        position += 1

    return {
        "week_start": str(week_start),
        "total_ranked": total_users,
        "ranking": ranking
    }

@router.get("/ranking/{user_id}")
def get_user_ranking_position(user_id: str, db: Session = Depends(get_db)):

    results = (
        db.query(XP.user_id, XP.total_xp)
        .order_by(XP.total_xp.desc())
        .all()
    )

    total_users = len(results)

    position = None
    user_xp = 0

    for index, record in enumerate(results):
        if record.user_id == user_id:
            position = index + 1
            user_xp = record.total_xp
            break

    if position is None:
        return {"error": "Usuário não encontrado no ranking"}

    top_percentage = round((position / total_users) * 100)
    league = get_league_from_percentage(top_percentage)

    return {
        "position": position,
        "total_users": total_users,
        "total_xp": user_xp,
        "top_percentage": top_percentage,
        "league": league
    }
@router.post("/admin/close-season")
def close_season_endpoint(db: Session = Depends(get_db)):
    close_season(db)
    return {"message": "Temporada encerrada com sucesso"}