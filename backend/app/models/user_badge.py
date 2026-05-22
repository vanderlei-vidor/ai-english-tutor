from sqlalchemy import Column, String, ForeignKey, DateTime
from app.core.database import Base
from datetime import datetime

class UserBadge(Base):
    __tablename__ = "user_badges"

    id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    badge_id = Column(String, ForeignKey("badges.id"), nullable=False)
    earned_at = Column(DateTime, default=datetime.utcnow)