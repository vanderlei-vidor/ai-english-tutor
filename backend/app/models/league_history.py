from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from app.core.database import Base
import uuid
from datetime import datetime

class LeagueHistory(Base):
    __tablename__ = "league_history"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    season_month = Column(String, nullable=False)
    league = Column(String)
    final_position = Column(Integer)
    total_xp = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
