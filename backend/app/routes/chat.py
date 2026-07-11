
import uuid

from datetime import date, timedelta
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.models.chat_schemas import ChatRequest

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
from app.services.grammar_engine.engine import grammar_engine

from app.services.streak_service import update_streak
from app.services.xp_service import calculate_xp, get_level_from_xp
from app.services.pedagogical.sanitizer import (
    pedagogical_sanitizer,
)
from app.services.debug.manager import debug

from app.services.prompt_builder.builder import (
    prompt_builder,
)

from app.models.conversation import Conversation

from app.services.teacher.engine import (
    teacher_engine,
)


from app.services.teacher.context import (
    TeacherContext,
)

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

        

        analysis = grammar_engine.analyze(user_text)

        from app.services.pedagogical.analysis_engine import (
            pedagogical_analysis_engine,
        )

        debug.grammar.log(analysis)

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

        pedagogical = pedagogical_analysis_engine.analyze(
            grammar=analysis,
            text=user_text,
            user_memory=user_memory,
        )

        teacher_context = TeacherContext(
            grammar=analysis,
            pedagogical=pedagogical,
        )

        teacher_result = teacher_engine.decide(
            teacher_context,
        )

        brain_state = teacher_result.brain

        #conversation_analysis = teacher_result.conversation

        print()
        print("=" * 60)
        print("BRAIN FINAL ACTION")
        print("=" * 60)
        print(brain_state.planning.action)
        print("=" * 60)

        prompt_context = prompt_builder.build(
            teacher_result.brain,
            pedagogical,
        )

       # conversation_logger.analysis(
        #    teacher_result.brain,
        #)


        debug.pedagogical.analysis(pedagogical)

        
        

        user_memory.data = {
            **user_memory.data,
            "advanced_structures": pedagogical.advanced_structures,
            "english_level": pedagogical.estimated_level,
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
        

        ai_response_dict = generate_response(
            messages_for_ai,
            prompt_context,
            teacher_result,
            user_memory.data,
        )

        if "error" in ai_response_dict:
            return ai_response_dict

        # ----------------------------------------------------------
        # Sincroniza a resposta da IA com o objeto pedagógico
        # ----------------------------------------------------------

        pedagogical.load_ai_response(
            ai_response_dict,
        )

        # ----------------------------------------------------------
        # SANITIZER
        # ----------------------------------------------------------

        pedagogical_sanitizer.sanitize(
            pedagogical,
            user_text,
            ai_response_dict,
        )

        

        

        

        # ==========================================================
        # SHADOW MODE: Validação da Migração de Erros
        # ==========================================================
        debug.migration.error(
            legacy_error=pedagogical.had_error,
            grammar_error=analysis.has_errors,
        )

        # Logs simplificados consumindo diretamente o estado encapsulado do objeto
        debug.skill.resolution(
            pedagogical,
            )
        debug.sanitizer.final(
            pedagogical,
        )

        # 4) Só agora salvar a resposta da IA de forma segura no Banco de Dados
        ai_message = Message(
            conversation_id=conversation.id,
            sender="ai",
            content=ai_response_dict["conversation_reply"],
        )
        db.add(ai_message)
        db.commit()

        # Atualiza a memória de erros/skills tradicional do app usando o objeto unificado
        update_memory_from_message(
            db=db,
            user_id=request.user_id,
            user_message=request.message,
            correction=ai_response_dict.get("correction", ""),
            exercise=ai_response_dict.get("exercise", ""),
            teacher_action=ai_response_dict.get("teacher_action", "chat"),
            detected_skill=ai_response_dict.get("detected_skill"),
            target_skill=pedagogical.target_skill,
            had_error=pedagogical.had_error,
            target_skill_error=pedagogical.target_skill_error,
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
        had_error_xp = score < 100
        xp_record = db.query(XP).filter(XP.user_id == request.user_id).first()
        if not xp_record:
            xp_record = XP(user_id=request.user_id, total_xp=0)
            db.add(xp_record)
            db.commit()
            db.refresh(xp_record)

        earned_xp = calculate_xp(score, had_error_xp, streak.current_streak)
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
