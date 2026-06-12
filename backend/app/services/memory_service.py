from app.models.user_memory import UserMemory


def get_or_create_memory(db, user_id):

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

                "weak_skills": {},

                "conversation_style": "casual",

                "total_conversations": 0
            }
        )

        db.add(memory)
        db.commit()
        db.refresh(memory)

    return memory