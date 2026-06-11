from app.services.level_service import detect_english_level
from sqlalchemy import Column, Integer, String, JSON
from sqlalchemy.orm import Session
from app.core.database import Base

# 1. O MODELO
class UserMemory(Base):
    __tablename__ = "user_memory"

    id = Column(Integer, primary_key=True)
    user_id = Column(String, unique=True)
    data = Column(JSON)


# 🔹 DICIONÁRIO DE TÓPICOS (Declarado aqui fora para organizar)
TOPICS_DATABASE = {
    "technology": ["ai", "technology", "computer"],
    "games": ["game", "games", "minecraft"],
    "anime": ["anime", "naruto", "one piece"],
    "books": ["book", "reading", "author"]
    
}


# 2. FUNÇÃO QUE BUSCA OU CRIA A MEMÓRIA
def get_user_memory(db: Session, user_id: str):
    memory = db.query(UserMemory).filter(
        UserMemory.user_id == user_id
    ).first()

    if not memory:
        memory = UserMemory(
            user_id=user_id,
            data={
                "english_level": "A1",
                "common_errors": {},
                "favorite_topics": {},
                "conversation_style": "casual",
                "total_conversations": 0
            }
        )
        db.add(memory)
        db.commit()
        db.refresh(memory)

    return memory


# 3. FUNÇÃO QUE ATUALIZA A MEMÓRIA
def update_memory_from_message(
    db: Session,
    user_id: str,
    user_message: str,
    correction: str
):
    # Garante que a memória existe antes de alterar
    memory = get_user_memory(db, user_id)

    # Evita bugs de mutabilidade no SQLAlchemy criando uma cópia limpa
    data = dict(memory.data)

    if not isinstance(
        data.get("favorite_topics"),
        dict
    ):
        data["favorite_topics"] = {}

    # 🔥 TOTAL CONVERSATIONS
    data["total_conversations"] += 1

    # 🔥 DETECT ENGLISH LEVEL
    detected_level = detect_english_level(user_message)
    data["english_level"] = detected_level

    # 🔥 DETECT FAVORITE TOPICS (Sua lógica nova integrada aqui!)
    message_lower = user_message.lower()
    for topic, keywords in TOPICS_DATABASE.items():
        for keyword in keywords:
            if keyword in message_lower:
                # Se o tópico mapeado ainda não está na lista do usuário, adiciona
                if topic not in data["favorite_topics"]:
                    data["favorite_topics"] [topic] = 0
                data["favorite_topics"] [topic] +=1
                break # Para de checar outras palavras do mesmo tópico se já achou uma

    # 🔥 DETECT VERB TENSE ERROR
    if "went" in correction.lower():
        if "verb tense" not in data["common_errors"]:
            data["common_errors"]["verb tense"] = 0
        data["common_errors"]["verb tense"] += 1

    # 🔥 DETECT ARTICLES
    if "article" in correction.lower():
        if "articles" not in data["common_errors"]:
            data["common_errors"]["articles"] = 0
        data["common_errors"]["articles"] += 1

    # Atualiza o campo e commita no banco
    memory.data = data
    db.commit()

    return memory