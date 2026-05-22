from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from app.core.database import Base
import uuid
from datetime import datetime


class XP(Base):
    __tablename__ = "xp"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    total_xp = Column(Integer, default=0)
    last_updated = Column(DateTime, default=datetime.utcnow)