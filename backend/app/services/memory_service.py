import copy
from sqlalchemy.orm import Session
from sqlalchemy.orm.attributes import flag_modified

from app.models.user_memory import UserMemory, TOPICS_DATABASE
from app.services.exercise_tracker import detect_exercise_type
from app.services.level_service import detect_english_level
from app.services.skill_tracker import detect_skill


def get_user_memory(db: Session, user_id: str):
    memory = db.query(UserMemory).filter(UserMemory.user_id == user_id).first()

    if not memory:
        memory = UserMemory(
            user_id=user_id,
            data={
                "english_level": "A1",
                "common_errors": {},
                "favorite_topics": {},
                "weak_skills": {},
                "skill_mastery": {
                    "past_tense": 0,
                    "articles": 0,
                    "prepositions": 0,
                    "verb_usage": 0,
                    "third_person": 0,
                    "infinitive": 0,
                    "irregular_verbs": 0,
                    "plural_nouns": 0,
                    "uncountable_nouns": 0,
                    "other_skill": 0,
                },
                "recent_exercise_types": [],
                "conversation_style": "casual",
                "total_conversations": 0,
                "total_messages": 0,
                # 🔥 Pedagogical counters
                "conversation_turns": 0,
                "messages_since_last_teaching": 5,
                # 🔥 última skill treinada pelo motor
                "last_target_skill": None,
            },
        )
        db.add(memory)
        db.commit()
        db.refresh(memory)

    return memory


def update_skill_mastery(data, skill, had_error: bool):
    print("🔥 UPDATE_SKILL_MASTERY CALLED")
    print(f"🔥 SKILL = {skill} | HAD_ERROR = {had_error}")

    if not skill or skill in ["unknown", "null"]:
        print("⚠️ Skill inválida para mastery, ignorando.")
        return

    mastery = data.setdefault("skill_mastery", {})
    current = mastery.get(skill, 0)

    # Se houve erro -> aumenta o score de erro (fraqueza)
    if had_error:
        current += 1
    else:
        # Se acertou -> reduz score de erro (decay)
        current = max(0, current - 1)

    mastery[skill] = current
    print(f"🔥 UPDATED MASTERY VALUE FOR {skill} = {mastery[skill]}")


def update_memory_from_message(
    db: Session,
    user_id: str,
    user_message: str,
    correction: str,
    exercise: str,
    teacher_action: str = "chat",
    detected_skill=None,
    target_skill=None,
    had_error=False,
    target_skill_error=False,
):
    print("======== MEMORY SERVICE INCOMING ========")
    print(f"DETECTED: {detected_skill} | TARGET: {target_skill}")
    print(f"HAD_ERROR: {had_error} | TARGET_ERROR: {target_skill_error}")
    print("=========================================")

    memory = get_user_memory(db, user_id)
    data = copy.deepcopy(memory.data)

    # =========================
    # Inicializações de segurança
    # =========================
    for key, default_type in [
        ("favorite_topics", dict),
        ("weak_skills", dict),
        ("common_errors", dict),
        ("skill_mastery", dict),
    ]:
        if not isinstance(data.get(key), default_type):
            data[key] = default_type()

    if not isinstance(data.get("recent_exercise_types"), list):
        data["recent_exercise_types"] = []

    # Salva a última skill alvo do motor
    if target_skill:
        data["last_target_skill"] = target_skill

    # ==========================================================
    # 🎯 FASE 12.7/12.8 — RESOLUÇÃO DE SKILL SEM CONTAMINAR TARGET
    # ==========================================================
    skill = None

    # CASO 1 — não houve erro real (frase correta)
    if not had_error:
        skill = target_skill or data.get("last_target_skill")

    # CASO 2 — houve erro real NA SKILL-ALVO
    elif had_error and target_skill_error:
        skill = target_skill or detected_skill or detect_skill(correction)

    # CASO 3 — houve erro real, mas FORA da skill-alvo
    else:
        skill = detected_skill or detect_skill(correction)
        if not skill:
            skill = "other_skill"

    if not skill:
        skill = "unknown"

    print("======== SKILL RESOLUTION DEBUG ========")
    print(f"DETECTED SKILL:        {detected_skill}")
    print(f"TARGET SKILL:          {target_skill}")
    print(f"HAD ERROR:             {had_error}")
    print(f"TARGET SKILL ERROR:    {target_skill_error}")
    print(f"FINAL SKILL:           {skill}")
    print(f"CORRECTION:            {correction}")
    print("========================================")

    # ==========================================================
    # 🎯 WEAK SKILLS + SKILL MASTERY
    # ==========================================================
    if skill and skill not in ["null", "unknown"]:
        current_weak = data["weak_skills"].get(skill, 0)

        if had_error:
            data["weak_skills"][skill] = current_weak + 1
            print(f"🎯 WEAK SKILL INCREMENTED: {skill} -> {data['weak_skills'][skill]}")
        else:
            data["weak_skills"][skill] = max(0, current_weak - 1)
            print(f"🎯 WEAK SKILL DECREMENTED: {skill} -> {data['weak_skills'][skill]}")

        update_skill_mastery(
            data=data,
            skill=skill,
            had_error=had_error,
        )

    # ==========================================================
    # 🚀 Outros Motores e Métricas
    # ==========================================================
    exercise_type = detect_exercise_type(exercise)
    if exercise_type:
        data["recent_exercise_types"].append(exercise_type)
        data["recent_exercise_types"] = data["recent_exercise_types"][-5:]

    # Histórico geral + contador pedagógico
    data["total_conversations"] = data.get("total_conversations", 0) + 1
    data["total_messages"] = data.get("total_messages", 0) + 1
    data["conversation_turns"] = data.get("conversation_turns", 0) + 1

    # Nível de inglês baseado na mensagem atual
    detected_level = detect_english_level(user_message)
    levels = {"A1": 1, "A2": 2, "B1": 3, "B2": 4, "C1": 5, "C2": 6}
    current_level = data.get("english_level", "A1")
    if levels.get(detected_level, 1) > levels.get(current_level, 1):
        data["english_level"] = detected_level

    # Tópicos favoritos
    message_lower = user_message.lower()
    for topic, keywords in TOPICS_DATABASE.items():
        if any(keyword in message_lower for keyword in keywords):
            data["favorite_topics"][topic] = data["favorite_topics"].get(topic, 0) + 1

    # Heurísticos antigos de Common Errors
    correction_lower = correction.lower() if correction else ""
    if had_error:
        if "went" in correction_lower:
            data["common_errors"]["verb tense"] = (
                data["common_errors"].get("verb tense", 0) + 1
            )
        if "article" in correction_lower:
            data["common_errors"]["articles"] = (
                data["common_errors"].get("articles", 0) + 1
            )

    # Controle do intervalo de intervenção do professor
    if teacher_action in ["exercise", "correction", "question"]:
        data["messages_since_last_teaching"] = 0
    else:
        data["messages_since_last_teaching"] = (
            data.get("messages_since_last_teaching", 0) + 1
        )

    print(f"🎯 SKILL MASTERY: {data.get('skill_mastery', {})}")
    print(f"🎯 WEAK SKILLS: {data.get('weak_skills', {})}")

    print("======== BEFORE SAVE ========")
    print(data["skill_mastery"])
    print("============================")

    # Persistência no Postgres via SQLAlchemy
    memory.data = data
    flag_modified(memory, "data")
    db.commit()
    db.refresh(memory)

    print("======== AFTER SAVE ========")
    print(memory.data["skill_mastery"])
    print("===========================")

    return memory
