from app.core.database import engine, Base

from app.models.user import User
from app.models.conversation import Conversation
from app.models.message import Message
from app.models.progress import Progress

# 🔥 IMPORT NOVO
from app.models.user_memory import UserMemory


def init():
    Base.metadata.create_all(bind=engine)
    print("🔥 Tabelas criadas com sucesso!")


if __name__ == "__main__":
    init()