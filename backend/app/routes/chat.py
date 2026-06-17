import uuid
import json
from datetime import date, timedelta
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.models.chat_schemas import ChatRequest
from app.models.conversation import Conversation
from app.models.message import Message
from app.models.progress import Progress
from app.models.streak import Streak
from app.models.xp import XP
from app.models.weekly_xp import WeeklyXP

from app.services.memory_service import get_user_memory, update_memory_from_message
from app.services.chat_service import generate_response
from app.services.score_service import (
    calculate_score,
    get_level,
    calculate_global_score,
)
from app.services.streak_service import update_streak
from app.services.xp_service import calculate_xp, get_level_from_xp

# Importação da engine de detecção de nível avançado
from app.services.level_detection import (
    detect_advanced_structures,
    calculate_complexity_points,
)

# FASE 11.7: Importando tanto o estimador de nível quanto o calculador de score de nível
from app.services.level_estimator import estimate_level, calculate_level_score

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/chat")
def chat(request: ChatRequest, db: Session = Depends(get_db)):
    try:
        # 📝 Centraliza o texto do usuário para deixar o código limpo
        user_text = request.message

        # 1️⃣ Se já existe conversation_id → usar
        if request.conversation_id:
            conversation = (
                db.query(Conversation)
                .filter(
                    Conversation.id == request.conversation_id,
                    Conversation.user_id == request.user_id,
                )
                .first()
            )
            if not conversation:
                return {"error": "Conversation não encontrada"}
        else:
            conversation = Conversation(id=str(uuid.uuid4()), user_id=request.user_id)
            db.add(conversation)
            db.commit()
            db.refresh(conversation)

        # 3️⃣ Salvar mensagem do usuário (Usando user_text)
        user_message = Message(
            conversation_id=conversation.id, sender="user", content=user_text
        )
        db.add(user_message)
        db.commit()

        # 🧠 Carrega a memória ANTES para poder injetar e ler as estruturas acumuladas nela
        user_memory = get_user_memory(db, request.user_id)

        # 🎓 FASE EXPERIMENTAL — DETECÇÃO DE COMPLEXIDADE GRAMATICAL DA FRASE ATUAL
        complexity_score, structures = detect_advanced_structures(user_text)
        complexity_points = calculate_complexity_points(complexity_score)

        print(f"🎓 ADVANCED STRUCTURES DETECTED: {structures}")
        print(f"🎓 COMPLEXITY POINTS: {complexity_points}")

        # ==========================================================
        # FASE 11.7 - ADVANCED STRUCTURE TRACKER & LEVEL ESTIMATOR
        # ==========================================================
        advanced_structures = user_memory.data.get("advanced_structures", {})

        # 1️⃣ Alimenta a memória acumulada com as estruturas da frase atual
        for structure in structures:
            advanced_structures[structure] = advanced_structures.get(structure, 0) + 1

        # 2️⃣ Calcula o Score de Nível e o Nível Estimado baseando-se no histórico acumulado fresco
        estimated_score = calculate_level_score(advanced_structures)
        estimated_level = estimate_level(advanced_structures)

        # 3️⃣ Console Debug unificado padrão AAA
        print(f"🎓 ADVANCED MEMORY: {advanced_structures}")
        print(f"🎓 LEVEL SCORE: {estimated_score}")
        print(f"🎓 ESTIMATED LEVEL: {estimated_level}")

        # 4️⃣ Sobrescreve o dicionário para o SQLAlchemy disparar o update do JSON no PostgreSQL
        user_memory.data = {
            **user_memory.data,
            "advanced_structures": advanced_structures,
        }

        db.commit()
        db.refresh(user_memory)
        # ==========================================================

        # 4️⃣ Buscar histórico (últimas 8)
        history = (
            db.query(Message)
            .filter(Message.conversation_id == conversation.id)
            .order_by(Message.created_at.asc())
            .all()
        )
        messages_for_ai = [
            {
                "role": "assistant" if msg.sender == "ai" else "user",
                "content": msg.content,
            }
            for msg in history[-8:]
        ]

        # 5️⃣ Chamar IA (Passando a memória já salva com os novos níveis e contadores)
        ai_response_dict = generate_response(messages_for_ai, user_memory.data)
        if "error" in ai_response_dict:
            return ai_response_dict

        # 7️⃣ Salvar resposta da IA
        ai_message = Message(
            conversation_id=conversation.id,
            sender="ai",
            content=ai_response_dict["conversation_reply"],
        )
        db.add(ai_message)
        db.commit()

        # Atualiza a memória de erros/skills tradicional do app
        update_memory_from_message(
            db=db,
            user_id=request.user_id,
            user_message=user_text,
            correction=ai_response_dict.get("correction", ""),
            exercise=ai_response_dict.get("exercise", ""),
            teacher_action=ai_response_dict.get("teacher_action", "chat"),
        )

        # Sincroniza a memória final para o retorno da API
        user_memory = get_user_memory(db, request.user_id)

        # 8️⃣ Calcular score e salvar progresso
        conversation_messages = (
            db.query(Message).filter(Message.conversation_id == conversation.id).all()
        )
        score = calculate_score(conversation_messages)

        progress = Progress(
            user_id=request.user_id, conversation_id=conversation.id, score=score
        )
        db.add(progress)
        db.commit()

        # Score global e Nível CEFR
        all_progress = (
            db.query(Progress).filter(Progress.user_id == request.user_id).all()
        )
        global_score = calculate_global_score(all_progress)
        cefr_level = get_level(global_score)

        # 1️⃣0️⃣ Atualizar streak
        streak = db.query(Streak).filter(Streak.user_id == request.user_id).first()
        if not streak:
            box = Streak(user_id=request.user_id)
            db.add(box)
            db.commit()
            db.refresh(box)
            streak = box
        streak = update_streak(streak)
        db.commit()

        # 🔥 XP SYSTEM
        had_error = score < 100
        xp_record = db.query(XP).filter(XP.user_id == request.user_id).first()
        if not xp_record:
            xp_record = XP(user_id=request.user_id, total_xp=0)
            db.add(xp_record)
            db.commit()
            db.refresh(xp_record)

        earned_xp = calculate_xp(score, had_error, streak.current_streak)
        xp_record.total_xp += earned_xp
        db.commit()

        # 🔥 WEEKLY XP SYSTEM
        today = date.today()
        week_start = today - timedelta(days=today.weekday())
        weekly_record = (
            db.query(WeeklyXP)
            .filter(
                WeeklyXP.user_id == request.user_id, WeeklyXP.week_start == week_start
            )
            .first()
        )
        if not weekly_record:
            weekly_record = WeeklyXP(
                user_id=request.user_id, total_xp=0, week_start=week_start
            )
            db.add(weekly_record)
            db.commit()
            db.refresh(weekly_record)
        weekly_record.total_xp += earned_xp
        db.commit()

        level_data = get_level_from_xp(xp_record.total_xp)

        # Medalhas
        from app.services.badge_service import check_and_award_badges

        badges_earned = check_and_award_badges(
            db=db,
            user_id=request.user_id,
            score=score,
            streak=streak.current_streak,
            xp_total=xp_record.total_xp,
            cefr_code=cefr_level["code"],
        )

        return {
            "conversation_id": conversation.id,
            "ai_response": ai_response_dict,
            "score": score,
            "streak": {
                "current": streak.current_streak,
                "longest": streak.longest_streak,
            },
            "xp": {
                "earned": earned_xp,
                "total": xp_record.total_xp,
                "level": level_data,
            },
            "badges_earned": badges_earned,
            "user_memory": user_memory.data,
        }

    except Exception as e:
        return {"error": str(e)}
