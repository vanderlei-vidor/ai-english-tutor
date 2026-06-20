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
                },
                "recent_exercise_types": [],
                "conversation_style": "casual",
                "total_conversations": 0,
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
    print(f"🔥 SKILL = {skill}")
    print(f"🔥 HAD_ERROR = {had_error}")

    if not skill or skill in ["unknown", "null"]:
        print("⚠️ Skill inválida para mastery, ignorando.")
        return

    mastery = data.setdefault("skill_mastery", {})
    current = mastery.get(skill, 0)

    # Se houve erro -> aumenta fraqueza
    if had_error:
        current += 1
    else:
        # Se acertou -> reduz fraqueza (decay)
        current = max(0, current - 1)

    mastery[skill] = current

    print(f"🔥 UPDATED VALUE = {mastery[skill]}")
    print(f"🚀 MEMORY_SERVICE HAD_ERROR: {had_error}")


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
):
    print(f"🚀 MEMORY_SERVICE DETECTED SKILL: {detected_skill}")
    print(f"🚀 MEMORY_SERVICE TARGET SKILL: {target_skill}")
    print(f"🚀 MEMORY_SERVICE HAD_ERROR: {had_error}")

    memory = get_user_memory(db, user_id)

    # deepcopy para evitar mutação profunda silenciosa do JSON
    data = copy.deepcopy(memory.data)

    # =========================
    # Inicializações de segurança
    # =========================
    if not isinstance(data.get("favorite_topics"), dict):
        data["favorite_topics"] = {}

    if not isinstance(data.get("weak_skills"), dict):
        data["weak_skills"] = {}

    if not isinstance(data.get("common_errors"), dict):
        data["common_errors"] = {}

    if not isinstance(data.get("skill_mastery"), dict):
        data["skill_mastery"] = {}

    if not isinstance(data.get("recent_exercise_types"), list):
        data["recent_exercise_types"] = []

    # ==========================================================
    # 🔥 SALVA A ÚLTIMA SKILL ALVO DA RODADA
    # ==========================================================
    if target_skill:
        data["last_target_skill"] = target_skill
        print(f"🎯 LAST TARGET SKILL SAVED: {target_skill}")

    # ==========================================================
    # 🎯 RESOLUÇÃO DE SKILL (BUGFIX PRINCIPAL)
    # ==========================================================
    skill = None

    # CASO 1: houve erro real


    if had_error:
    # quando há erro real, a skill detectada pode vencer a target
        skill = detected_skill or target_skill or detect_skill(correction)

# CASO 2: não houve erro
    else:
    # se NÃO houve erro, nunca usar detected_skill
    # porque detected_skill pode vir de uma correction lixo / known_error atravessado
        skill = target_skill or data.get("last_target_skill")

    if not skill:
        skill = "unknown"

    print("======== SKILL RESOLUTION DEBUG ========")
    print(f"DETECTED SKILL: {detected_skill}")
    print(f"TARGET SKILL:   {target_skill}")
    print(f"HAD ERROR:      {had_error}")
    print(f"FINAL SKILL:    {skill}")
    print(f"CORRECTION:     {correction}")
    print("========================================")

    # ==========================================================
    # 🎯 WEAK SKILLS + SKILL MASTERY
    # ==========================================================
    if skill and skill not in ["null", "unknown"]:
        print(f"🎯 SKILL DETECTED FOR MASTERY: {skill}")
        print("🚀 BEFORE UPDATE_SKILL_MASTERY")

        # weak_skills só aumenta quando realmente houve erro
        if had_error:
            data["weak_skills"][skill] = data["weak_skills"].get(skill, 0) + 1
            print(f"🎯 WEAK SKILL INCREMENTED: {skill} -> {data['weak_skills'][skill]}")

        update_skill_mastery(
            data=data,
            skill=skill,
            had_error=had_error,
        )
    else:
        print("⚠️ Skill final inválida ou desconhecida. Nenhuma skill será atualizada.")

    # ==========================================================
    # 🚀 Histórico Recente de Exercícios
    # ==========================================================
    exercise_type = detect_exercise_type(exercise)
    if exercise_type:
        data["recent_exercise_types"].append(exercise_type)
        data["recent_exercise_types"] = data["recent_exercise_types"][-5:]

    # ==========================================================
    # 🔥 TOTAL CONVERSATIONS
    # ==========================================================
    data["total_conversations"] = data.get("total_conversations", 0) + 1

    # ==========================================================
    # 🔥 PEDAGOGICAL COUNTERS
    # ==========================================================
    data["conversation_turns"] = data.get("conversation_turns", 0) + 1

    # ==========================================================
    # 🔥 DETECT ENGLISH LEVEL
    # ==========================================================
    detected_level = detect_english_level(user_message)
    levels = {"A1": 1, "A2": 2, "B1": 3, "B2": 4, "C1": 5, "C2": 6}
    current_level = data.get("english_level", "A1")

    if levels.get(detected_level, 1) > levels.get(current_level, 1):
        data["english_level"] = detected_level

    # ==========================================================
    # 🔥 DETECT FAVORITE TOPICS
    # ==========================================================
    message_lower = user_message.lower()
    for topic, keywords in TOPICS_DATABASE.items():
        for keyword in keywords:
            if keyword in message_lower:
                data["favorite_topics"][topic] = (
                    data["favorite_topics"].get(topic, 0) + 1
                )
                break

    # ==========================================================
    # 🔥 COMMON ERRORS (heurísticos antigos)
    # ==========================================================
    correction_lower = correction.lower() if correction else ""

    if had_error and "went" in correction_lower:
        data["common_errors"]["verb tense"] = (
            data["common_errors"].get("verb tense", 0) + 1
        )

    if had_error and "article" in correction_lower:
        data["common_errors"]["articles"] = data["common_errors"].get("articles", 0) + 1

    # ==========================================================
    # 🔥 TEACHING INTERVAL ENGINE
    # ==========================================================
    if teacher_action in ["exercise", "correction", "question"]:
        data["messages_since_last_teaching"] = 0
    else:
        data["messages_since_last_teaching"] = (
            data.get("messages_since_last_teaching", 0) + 1
        )

    # ==========================================================
    # DEBUG FINAL
    # ==========================================================
    print(f"🎯 SKILL MASTERY: {data.get('skill_mastery', {})}")
    print(f"🎯 WEAK SKILLS: {data.get('weak_skills', {})}")

    print("======== BEFORE SAVE ========")
    print(data["skill_mastery"])
    print("============================")

    # ==========================================================
    # SALVAR JSON NO SQLALCHEMY
    # ==========================================================
    memory.data = data
    flag_modified(memory, "data")
    db.commit()
    db.refresh(memory)

    print("======== AFTER SAVE ========")
    print(memory.data["skill_mastery"])
    print("===========================")

    return memory
