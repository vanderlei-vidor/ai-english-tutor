import profile
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
from app.services.correction_validator import (
    is_real_english_error,
    is_real_correction_by_skill,
    detect_non_target_skill,
    analyze_correction_validity,
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
        from app.services.grammar_engine.engine import grammar_engine
        analysis = grammar_engine.analyze(user_text)

        grammar_has_errors = bool(analysis.errors)

        print()

        print("=" * 60)

        print("🧠 ERROR DETECTION")

        print("=" * 60)

        print(f"Grammar Engine Errors : {grammar_has_errors}")

        print(f"Errors Count          : {len(analysis.errors)}")

        print("=" * 60)

        print()

        

        print()
        print("=" * 60)
        print("🧠 NEW GRAMMAR ENGINE (SHADOW MODE)")
        print("=" * 60)

        print(f"Sentence: {user_text}")

        print()

        print("Errors:")

        if analysis.has_errors:
            for skill in analysis.detected_skills:
                print(f" • {skill}")
        else:
            print(" None")

        print()

        print()

        print("Primary Error")

        if analysis.primary_error:
            print(analysis.primary_error.skill)
        else:
            print("None")

        print()
        print("Concepts")

        if analysis.has_concepts:
            for name in analysis.concept_names:
                print(f" • {name}")
        else:
            print(" None")

            print()

        print()

        print("Primary Concept")

        if analysis.primary_concept:
            print(analysis.primary_concept.name)
        else:
            print("None")

        profile = analysis.learning_profile

        if profile:

            print("Learning Profile")

            print(f" Current Focus : {profile.current_focus}")

            print(f" Accuracy      : {profile.overall_accuracy:.2f}%")

            print(f" Weak Skills   : {profile.weak_skills}")

            print(f" Mastered      : {profile.mastered_skills}")

        print("=" * 60)
        print()

        print()

        # ==========================================
        # NEW PEDAGOGICAL ENGINE
        # ==========================================

        new_target_skill = None

        if analysis.learning_profile:
            new_target_skill = analysis.learning_profile.current_focus

        

        had_error = False
        target_skill_error = False
        target_skill = None

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
            "english_level": estimated_level,
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

        # 1) Gerar resposta da IA
        ai_response_dict = generate_response(messages_for_ai, user_memory.data)
        if "error" in ai_response_dict:
            return ai_response_dict

        # 2) Rodar o Routing Sanitizer (FASE 12.8)
        #target_skill = ai_response_dict.get("target_skill")
        legacy_target_skill = ai_response_dict.get("target_skill")

        target_skill = new_target_skill or legacy_target_skill
        print()
        print("=" * 60)
        print("⚖️ TARGET SKILL MIGRATION")
        print("=" * 60)

        print(f"Legacy Target Skill : {legacy_target_skill}")
        print(f"New Current Focus   : {new_target_skill}")
        print(f"Using               : {target_skill}")

        print("=" * 60)
        print()
        correction_text = ai_response_dict.get("correction", "")
        teacher_action = ai_response_dict.get("teacher_action", "")
        needs_correction = ai_response_dict.get("needs_correction", False)
        detected_skill = ai_response_dict.get("detected_skill")

        # ----------------------------------------------------------
        # FASE 12.8 — separar:
        # A) erro real de inglês
        # B) erro da skill-alvo
        # C) erro real fora da skill-alvo + fallback de skill
        # ----------------------------------------------------------
        sanitizer_analysis = analyze_correction_validity(
            user_text=user_text,
            correction=correction_text,
            teacher_action=teacher_action,
            needs_correction=needs_correction,
            target_skill=target_skill,
            detected_skill=detected_skill,
        )

        has_any_real_error = sanitizer_analysis["is_real_error"]
        sanitizer_reason = sanitizer_analysis["reason"]

        initial_target_skill_error = is_real_correction_by_skill(
            correction=correction_text,
            target_skill=target_skill,
        )

        fallback_skill = None

        if has_any_real_error and not initial_target_skill_error and not detected_skill:
            fallback_skill = detect_non_target_skill(user_text, correction_text)

        if fallback_skill:
            ai_response_dict["detected_skill"] = fallback_skill

        if has_any_real_error and not initial_target_skill_error and fallback_skill:
            sanitizer_reason = f"real_non_target_error:{fallback_skill}"

        # 🔥 Sincroniza detected_skill com o estado final do dict
        detected_skill = ai_response_dict.get("detected_skill")

        print("======== ROUTING SANITIZER DEBUG ========")
        print(f"USER TEXT:               {user_text}")
        print(f"CORRECTION TEXT:         {correction_text}")
        print(f"TEACHER ACTION:          {teacher_action}")
        print(f"NEEDS CORRECTION:        {needs_correction}")
        print(f"TARGET SKILL:            {target_skill}")
        print(f"DETECTED SKILL:          {detected_skill}")
        print(f"FALLBACK SKILL:          {fallback_skill}")
        print(f"SANITIZER REASON:        {sanitizer_reason}")
        print("=========================================")

        # ==========================================================
        # CENÁRIO 1 — IA marcou correction, mas NÃO há erro real
        # ==========================================================
        if teacher_action == "correction" and not has_any_real_error:
            print(f"⚠️ SANITIZER CONVERTED TO SUCCESS -> reason={sanitizer_reason}")
            
            ai_response_dict["teacher_action"] = "chat"
            ai_response_dict["needs_correction"] = False
            ai_response_dict["correction"] = "Correct! ✨"
            ai_response_dict["conversation_reply"] = "Correct! ✨"
            ai_response_dict["detected_skill"] = None

        # ==========================================================
        # CENÁRIO 2 — existe erro real, mas NÃO é da skill-alvo
        # Usa o snapshot inicial estável pré-sanitização
        # ==========================================================
        elif (
            teacher_action == "correction"
            and has_any_real_error
            and not initial_target_skill_error
        ):
            print(
                f"🟡 REAL ERROR OUTSIDE TARGET SKILL -> keeping correction without contaminating target skill | reason={sanitizer_reason}"
            )
            ai_response_dict["teacher_action"] = "correction"
            ai_response_dict["needs_correction"] = True

            if not ai_response_dict.get("detected_skill"):
                ai_response_dict["detected_skill"] = "other_skill"

        # ==========================================================
        # CENÁRIO 3 — erro real da skill-alvo
        # ==========================================================
        else:
            print(f"✅ ROUTING KEPT AS-IS -> reason={sanitizer_reason}")

        # 3) Recalcular variáveis finais com base na decisão sanitizada
        teacher_action = ai_response_dict.get("teacher_action", "")
        needs_correction = ai_response_dict.get("needs_correction", False)
        correction_text = ai_response_dict.get("correction", "")
        detected_skill = ai_response_dict.get("detected_skill")

        # had_error = houve erro real de inglês
        had_error = is_real_english_error(
            user_text=user_text,
            correction=correction_text,
            teacher_action=teacher_action,
            needs_correction=needs_correction,
            target_skill=target_skill,
            detected_skill=detected_skill,
        )

        # ==========================================================
        # SHADOW MODE: Validação da Migração de Erros
        # ==========================================================
        legacy_had_error = had_error
        new_had_error = bool(analysis.errors)

        print()
        print("=" * 60)
        print("⚖️ ERROR MIGRATION")
        print("=" * 60)
        print(f"Legacy Error : {legacy_had_error}")
        print(f"Grammar      : {new_had_error}")
        print("=" * 60)

        # target_skill_error = erro real pertence à skill-alvo (recalculado pós-sanitizer)
        target_skill_error = (
            teacher_action == "correction"
            and needs_correction
            and is_real_correction_by_skill(
                correction=correction_text,
                target_skill=target_skill,
            )
        )


        print("========== TARGET SKILL CHECK ==========")
        print(f"TARGET SKILL: {target_skill}")
        print(f"DETECTED SKILL: {detected_skill}")
        print(f"CORRECTION: {correction_text}")
        print(f"TARGET SKILL ERROR: {target_skill_error}")
        print("========================================")

        print("======== FINAL SANITIZED STATE ========")
        print(f"FINAL TEACHER_ACTION:     {teacher_action}")
        print(f"FINAL NEEDS_CORRECTION:   {needs_correction}")
        print(f"FINAL CORRECTION:         {correction_text}")
        print(f"FINAL DETECTED_SKILL:     {detected_skill}")
        print(f"FINAL HAD_ERROR:          {had_error}")
        print(f"FINAL TARGET_SKILL_ERR:   {target_skill_error}")
        print(f"FINAL SANITIZER_REASON:   {sanitizer_reason}")
        print("=======================================")

        # 4) Só agora salvar a resposta da IA de forma segura no Banco de Dados
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
            user_message=request.message,
            correction=ai_response_dict.get("correction", ""),
            exercise=ai_response_dict.get("exercise", ""),
            teacher_action=ai_response_dict.get("teacher_action", "chat"),
            detected_skill=ai_response_dict.get("detected_skill"),
            target_skill=target_skill,
            had_error=had_error,
            target_skill_error=target_skill_error,
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
