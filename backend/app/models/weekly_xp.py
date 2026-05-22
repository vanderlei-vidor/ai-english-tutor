from sqlalchemy import Column, String, Integer, Date, ForeignKey
from app.core.database import Base
import uuid

class WeeklyXP(Base):
    __tablename__ = "weekly_xp"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    total_xp = Column(Integer, default=0)
    week_start = Column(Date, nullable=False)