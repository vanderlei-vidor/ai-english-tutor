from sqlalchemy import Column, String, Integer, Date, ForeignKey
from app.core.database import Base
import uuid


class Streak(Base):
    __tablename__ = "streaks"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    current_streak = Column(Integer, default=0)
    longest_streak = Column(Integer, default=0)
    last_study_date = Column(Date)