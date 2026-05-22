from sqlalchemy import Column, String, Integer
from app.core.database import Base

class Badge(Base):
    __tablename__ = "badges"

    id = Column(String, primary_key=True)
    code = Column(String, unique=True, nullable=False)
    title = Column(String, nullable=False)
    description = Column(String)
    icon = Column(String)
    category = Column(String)
    requirement_value = Column(Integer)