from sqlalchemy import Column, String, Integer, Date, ForeignKey
from app.core.database import Base
import uuid


class WeeklyResult(Base):
    __tablename__ = "weekly_results"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False)

    week_start = Column(Date, nullable=False)
    final_position = Column(Integer)
    final_xp = Column(Integer)

    league = Column(String(50))
