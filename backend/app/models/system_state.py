from sqlalchemy import Column, String
from app.core.database import Base


class SystemState(Base):
    __tablename__ = "system_state"

    key = Column(String, primary_key=True)
    value = Column(String)
