import uuid
from app.models.badge import Badge
from app.models.user_badge import UserBadge

def check_and_award_badges(db, user_id, score, streak, xp_total, cefr_code):

    earned_badges = []

    all_badges = db.query(Badge).all()

    for badge in all_badges:

        already_has = db.query(UserBadge).filter(
            UserBadge.user_id == user_id,
            UserBadge.badge_id == badge.id
        ).first()

        if already_has:
            continue

        if badge.category == "streak" and streak >= badge.requirement_value:
            earned_badges.append(badge)

        elif badge.category == "xp" and xp_total >= badge.requirement_value:
            earned_badges.append(badge)

        elif badge.category == "cefr" and cefr_code == badge.code:
            earned_badges.append(badge)

        elif badge.category == "perfect" and score == 100:
            earned_badges.append(badge)

    awarded = []

    for badge in earned_badges:
        new_user_badge = UserBadge(
            id=str(uuid.uuid4()),
            user_id=user_id,
            badge_id=badge.id
        )
        db.add(new_user_badge)
        awarded.append({
            "code": badge.code,
            "title": badge.title,
            "description": badge.description,
            "icon": badge.icon
        })

    db.commit()

    return awarded