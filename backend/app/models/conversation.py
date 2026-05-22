from sqlalchemy import Column, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.core.database import Base
import uuid
from datetime import datetime

class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    started_at = Column(DateTime, default=datetime.utcnow)

    messages = relationship("Message", back_populates="conversation")