import os
import json
import time
import re
import random
import requests
from dotenv import load_dotenv
from app.services.memory_utils import get_top_errors, get_top_topics
from app.services.exercise_engine import should_generate_exercise, choose_exercise_type
from app.services.error_pattern_engine import detect_known_error

# Importação da nova Skill Exercise Engine (Fase 9)
from app.services.skill_exercise_engine import get_skill_specific_exercise

# 🎓 MUDANÇA 3: Importe centralizado no topo para evitar duplicidade nos escopos locais
from app.services.level_estimator import estimate_level
from app.services.personalized_learning_engine import get_weakest_skill

from app.services.prompt_builder.static.builder import (
    static_prompt_builder,
)
from app.services.teacher.response.executor import (
    teacher_response_executor,
)

load_dotenv()

LM_STUDIO_URL = os.getenv("LM_STUDIO_URL", "http://localhost:1234/v1/chat/completions")
MODEL_NAME = os.getenv("LM_STUDIO_MODEL", "qwen2.5-7b-instruct")


static_prompt_builder.build()
# ==========================================
# VALIDATION ENGINE & GUARDRAILS
# ==========================================


def validate_correction(correction: str, needs_correction: bool) -> str:
    """Filtra correções inválidas ou vazias geradas por preguiça do modelo."""
    if not needs_correction:
        return correction

    invalid_feedbacks = [
        "good try",
        "you're close",
        "you are close",
        "almost",
        "nice try",
        "well done",
        "great job",
        "keep practicing",
        "excellent",
    ]

    correction_lower = correction.lower()

    for phrase in invalid_feedbacks:
        if phrase in correction_lower:
            return ""

    return correction


def _validate_multiple_choice(ex: str) -> bool:
    return "_____" in ex and ("(a)" in ex or "a)" in ex)


def _validate_fill_blank(ex: str) -> bool:
    return "_____" in ex and not any(opt in ex for opt in ["(a)", "a)", "b)"])


def _validate_verb_transformation(ex: str) -> bool:
    ex_low = ex.lower()
    return "(" in ex and ")" in ex and ("to " in ex_low or "verb" in ex_low)


def _validate_sentence_reordering(ex: str) -> bool:
    return "/" in ex and len(ex.split("/")) >= 3


def _validate_sentence_correction(ex: str) -> bool:
    return len(ex.split()) >= 3 and not "_____" in ex


def validate_and_fix_exercise(
    exercise: str, exercise_type: str, theme: str, target_skill: str
) -> str:
    """Guardrail do Backend com Validadores Granulares para o Modelo 7B."""
    ex_clean = exercise.strip()
    placeholders = ["word1", "word2", "[incorrect sentence]", "subject", "action"]

    if any(p in ex_clean.lower() for p in placeholders) or not ex_clean:
        print(
            f"⚠️ [Guardrail] Placeholder detectado ou vazio. Gerando fallback completo."
        )
        return _generate_backend_fallback(exercise_type, theme, target_skill)

    validators = {
        "multiple_choice": _validate_multiple_choice,
        "fill_blank": _validate_fill_blank,
        "verb_transformation": _validate_verb_transformation,
        "sentence_reordering": _validate_sentence_reordering,
        "sentence_correction": _validate_sentence_correction,
    }

    validator_func = validators.get(exercise_type)

    if validator_func and not validator_func(ex_clean):
        print(
            f"⚠️ [Guardrail] Falha estrutural no tipo '{exercise_type}'. Injetando fallback limpo."
        )
        return _generate_backend_fallback(exercise_type, theme, target_skill)

    return ex_clean


def _generate_backend_fallback(
    exercise_type: str, theme: str, target_skill: str
) -> str:
    is_anime = theme.lower() == "anime"
    subject = "Naruto" if is_anime else "He"
    action_past = "watched an anime" if is_anime else "bought a laptop"
    action_present = "watches anime" if is_anime else "studies English"

    fallbacks = {
        "multiple_choice": f"{subject} _____ {action_past} yesterday. (a) went (b) {'watched' if is_anime else 'bought'}",
        "fill_blank": f"Fill the blank ({target_skill}): {subject} _____ {action_present} every single day.",
        "sentence_reordering": f"Order the words about {theme}: {subject} / English / loves / studying"
        if not is_anime
        else "Naruto / become / wants / Hokage / to",
        "sentence_correction": f"Correct the error: {subject} do not like {'anime' if is_anime else 'studying'}.",
        "verb_transformation": f"Change the verb to {target_skill}: {subject} (to watch) a new episode last night."
        if is_anime
        else f"Change the verb to {target_skill}: {subject} (to buy) a computer yesterday.",
    }
    return fallbacks.get(
        exercise_type,
        f"Let's practice {target_skill}! Fill the blank: {subject} _____ happy. (is/are)",
    )


# ==========================================
# PASSO 1 — Criar o Resolver (Juiz Final)
# ==========================================
def resolve_final_teacher_action(
    response_json: dict,
    known_error: dict | None,
    allowed_mode: str,
    backend_wants_teaching: bool,
) -> str:
    """
    Juiz final do sistema pedagógico.
    Somente esta função decide a ação final.
    """
    if known_error:
        return "correction"

    if response_json.get("needs_correction"):
        return "correction"

    if allowed_mode == "chat":
        return "chat"

    if backend_wants_teaching:
        ai_action = response_json.get("teacher_action")
        if ai_action == "exercise":
            return "exercise"
        return "question"

    ai_action = response_json.get("teacher_action", "chat")
    if ai_action in ["question", "exercise"]:
        return ai_action

    return "chat"


# ==========================================
# MAIN RESPONSE ENGINE
# ==========================================
def generate_response(
    messages: list, prompt_context, teacher_result, memory_data: dict
) -> dict:
    conversation_turns = memory_data.get("conversation_turns", 0)
    messages_since_last_teaching = memory_data.get("messages_since_last_teaching", 5)

    english_level = memory_data.get("english_level", "A2")
    favorite_topics = memory_data.get("favorite_topics", {})

    top_topics = get_top_topics(
        favorite_topics if isinstance(favorite_topics, dict) else {}
    )
    theme = top_topics[0].lower() if top_topics else "technology"

    weak_skills = memory_data.get("weak_skills", {})

    from app.services.weighted_teaching_engine import (
    choose_teaching_skill
    )

    exercise_focus = choose_teaching_skill(
    memory_data
    )



    top_weak_skills = get_top_errors(
        weak_skills if isinstance(weak_skills, dict) else {}
    )
    top_errors = get_top_errors(memory_data.get("common_errors", {}))

    
    exercise_type = choose_exercise_type(memory_data)

    weakness_score = weak_skills.get(exercise_focus, 0)

    if weakness_score >= 20:
        teaching_probability = 0.90
    elif weakness_score >= 10:
        teaching_probability = 0.70
    elif weakness_score >= 5:
        teaching_probability = 0.50
    else:
        teaching_probability = 0.20

    hit_teaching_chance = random.random() < teaching_probability

    if messages_since_last_teaching < 2 and weakness_score < 10:
        allowed_mode = "chat"
    else:
        if hit_teaching_chance:
            allowed_mode = "full" if len(weak_skills) > 0 else "light"
        elif conversation_turns % 5 == 0 and conversation_turns > 0:
            allowed_mode = "light"
        else:
            allowed_mode = "chat"

    exercise_required = (
        len(weak_skills) > 0 or should_generate_exercise("", memory_data)
    ) and allowed_mode in ["light", "full"]

    backend_wants_teaching = allowed_mode == "full" and weakness_score >= 10

    print("\n=== DEBUG PEDAGOGICAL BACKEND ===")
    print(
        f"TURNS:            {conversation_turns} | SINCE LAST TEACHING: {messages_since_last_teaching}"
    )
    print(
        f"TEACH PROBABILITY: {teaching_probability * 100}% | CHANCE HIT: {hit_teaching_chance}"
    )
    print(
        f"ROUTED MODE:      {allowed_mode.upper()} | SCORE DE FRAQUEZA: {weakness_score}"
    )
    print(f"TARGET SKILL:     {exercise_focus}")
    print(f"EXERCISE REQUIRED:{exercise_required}")
    print(f"BACKEND WANTS TEACHING: {backend_wants_teaching}")
    print("=================================\n")

    memory_context = f"""
### DYNAMIC USER CONTEXT ###
ALLOWED TEACHING MODE FOR THIS TURN: {allowed_mode} (Strictly obey this directive!)
MANDATORY TARGET SKILL TO TRAIN: {exercise_focus}
Exercise Format Required: {exercise_type}
Exercise Theme: {theme}
User English Level: {english_level}
Conversation Style: {memory_data.get("conversation_style", "casual")}
Exercise Required Right Now: {"YES" if exercise_required else "NO"}
"""
    
    from app.services.prompt_builder.composer import (
        prompt_composer,
    )
    
    dynamic_prompt = prompt_composer.compose(
    prompt_context,
)

    system_prompt = (
        static_prompt_builder.build()
        + "\n\n"
        + dynamic_prompt
        + "\n\n"
        + memory_context
    )

    full_messages = [
        {
            "role": "system",
            "content": system_prompt,
        }
    ] + messages

    payload = {
        "model": MODEL_NAME,
        "messages": full_messages,
        "temperature": 0.2,
        "max_tokens": 600,
    }

    try:
        print("=== SENDING TO LM STUDIO ===")
        start_time = time.time()
        response = requests.post(LM_STUDIO_URL, json=payload, timeout=45)
        response.raise_for_status()
        print(f"LM STUDIO RESPONSE TIME: {time.time() - start_time:.2f}s")

        raw_text = response.json()["choices"][0]["message"]["content"].strip()

        # Remove vírgulas extras antes de fechar chaves ou colchetes, mesmo com espaços/quebras de linha
        cleaned_text = re.sub(r",\s*}", "}", raw_text)
        cleaned_text = re.sub(r",\s*]", "]", cleaned_text)

        if cleaned_text != raw_text:
            print("⚠️ JSON AUTO-REPAIRED (Regex Rule)")
            raw_text = cleaned_text

    except Exception as e:
        print(f"❌ Erro de requisição no LM Studio: {str(e)}")
        return _disaster_recovery_json()

    try:
        response_json = json.loads(raw_text)

        known_error = detect_known_error(messages[-1]["content"])
        print(f"KNOWN ERROR RESULT: {known_error}")

        if known_error:
            response_json["detected_skill"] = known_error["skill"]

        if known_error:
            print(f"🎯 ERROR PATTERN DETECTED -> {known_error['skill']}")
            response_json["needs_correction"] = True
            response_json["correction"] = known_error["correction"]
            response_json["explanation_pt"] = known_error["explanation"]

        VALID_ACTIONS = ["chat", "question", "exercise", "correction"]
        teacher_action = response_json.get("teacher_action", "chat")
        if teacher_action not in VALID_ACTIONS:
            print(f"⚠️ INVALID TEACHER ACTION DETECTED: {teacher_action}")
            teacher_action = "chat"
            response_json["teacher_action"] = "chat"

        confidence = response_json.get("grammar_confidence", 1.0)
        needs_correction = response_json.get("needs_correction", False)

        print("\n=== AI ORIGINAL DECISION ===")
        print(f"ACTION: {teacher_action} | CONFIDENCE: {confidence}")
        print("============================\n")

        # Guardrail de Correção
        original_correction = response_json.get("correction", "")

        response_json["correction"] = validate_correction(
            original_correction, needs_correction
        )

        validated_correction = response_json.get("correction", "")

        if is_invalid_correction(validated_correction):
            print("⚠️ INVALID CORRECTION FORMAT DETECTED")
            response_json["correction"] = ""

        if response_json.get("needs_correction") and not response_json.get(
            "correction"
        ):
            if response_json.get("example"):
                response_json["correction"] = response_json["example"]

        BAD_CORRECTIONS = [
            "you're close",
            "good try",
            "small mistake",
            "change",
            "past tense",
            "try again",
            "almost",
        ]
        correction_lower = response_json.get("correction", "").lower()
        if any(bad in correction_lower for bad in BAD_CORRECTIONS):
            print("⚠️ INVALID CORRECTION DETECTED")
            response_json["correction"] = ""

        user_msg_clean = messages[-1]["content"].strip().lower() if messages else ""
        SPECIAL_CORRECTIONS = {
            "talk english": "I speak English.",
            "talk english with": "I speak English.",
            "talk english at": "I speak English.",
        }
        for trigger, fixed_form in SPECIAL_CORRECTIONS.items():
            if trigger in user_msg_clean:
                print(f"🎯 SPECIAL CORRECTION TRIGGERED FOR SUBSTRING: '{trigger}'")
                response_json["needs_correction"] = True
                response_json["correction"] = fixed_form
                break

        SPECIAL_EXPLANATIONS = {
            "talk english": "Em inglês usamos 'speak English', não 'talk English'.",
            "she don't": "Na terceira pessoa usamos 'doesn't', não 'don't'.",
            "go yesterday": "Após marcadores de passado como 'yesterday', usamos o verbo no passado.",
        }
        for trigger, explanation in SPECIAL_EXPLANATIONS.items():
            if trigger in user_msg_clean:
                response_json["explanation_pt"] = explanation
                print(f"🎯 SPECIAL EXPLANATION TRIGGERED FOR SUBSTRING: '{trigger}'")
                break

        confidence = response_json.get("grammar_confidence", 1.0)
        needs_correction = response_json.get("needs_correction", False)

        if confidence > 0.95 and not needs_correction:
            response_json["needs_correction"] = False
            response_json["correction"] = "Correct! ✨"
            response_json["explanation_pt"] = (
                "Sua frase está totalmente correta! Excelente trabalho. 🥳"
            )
            response_json["example"] = ""

        if (
            not response_json.get("conversation_reply")
            or "keep practicing" in response_json.get("conversation_reply").lower()
        ):
            if theme == "anime":
                response_json["conversation_reply"] = (
                    "That's awesome! By the way, who is your favorite anime character?"
                )
            else:
                response_json["conversation_reply"] = (
                    "That sounds cool! Tell me more about that."
                )

        response_json = teacher_response_executor.execute(
            brain=teacher_result.brain,
            response_json=response_json,
        )

        

        final_action = resolve_final_teacher_action(
            response_json=response_json,
            known_error=known_error,
            allowed_mode=allowed_mode,
            backend_wants_teaching=backend_wants_teaching,
        )

        

        response_json["teacher_action"] = final_action

        print("\n=== FINAL BACKEND DECISION ===")
        print(f"FINAL ACTION DETERMINED: {final_action}")
        print("==============================\n")

        # ==========================================================
        # RESOLUÇÃO DE AÇÕES PEDAGÓGICAS — FASE 11.9 (REFATORADO)
        # ==========================================================
        if final_action == "chat":
            response_json["exercise"] = ""

        elif final_action == "correction":
            response_json["exercise"] = ""

        elif final_action == "exercise":
            print(
                f"🎯 SKILL EXERCISE ENGINE ACTIVATED FOR EXERCISE -> {exercise_focus}"
            )

            # 1. Extração unificada dos níveis para o log
            memory_level = memory_data.get("english_level", "A2")
            advanced_structures = memory_data.get("advanced_structures", {})
            estimated_level = estimate_level(advanced_structures)
            adaptive_level = estimated_level

            # 🎓 Prints de telemetria
            print(f"🎓 MEMORY LEVEL: {memory_level}")
            print(f"🎓 ESTIMATED LEVEL: {estimated_level}")
            print(f"🎓 ADAPTIVE LEVEL USED: {adaptive_level}")
            print("==================================================\n")

            # Invocação da engine com o nível dinâmico mapeado
            response_json["exercise"] = get_skill_specific_exercise(
                skill=exercise_focus, level=adaptive_level, exercise_type=exercise_type
            )
            print(f"🎯 ADAPTIVE EXERCISE GENERATED: {response_json['exercise']}")

        elif final_action == "question":
            # 🎓 MUDANÇA 1 & 3: Limpeza completa do bloco morto redundante e remoção de imports duplicados
            advanced_structures = memory_data.get("advanced_structures", {})
            adaptive_level = estimate_level(advanced_structures)

            # 🎓 MUDANÇA 2: Corrigido o motor adaptativo para passar 'adaptive_level' em vez de 'english_level'
            response_json["exercise"] = get_skill_specific_exercise(
                skill=exercise_focus,
                level=adaptive_level,
                exercise_type=exercise_type,
            )
            print(
                f"🎯 ADAPTIVE EXERCISE GENERATED (IN QUESTION MODE): {response_json['exercise']}"
            )

        print("\n=== AI SUMMARY DECISION ===")
        print(f"ACTION: {response_json.get('teacher_action')}")
        print(f"CORRECTION: {response_json.get('needs_correction')}")
        print(f"CONFIDENCE: {response_json.get('grammar_confidence')}")
        print("===================\n")
        print(f"🎯 RESPONSE SKILL: {response_json.get('detected_skill')}")

        response_json["target_skill"] = exercise_focus

        return response_json

    except json.JSONDecodeError:
        print(f"❌ Erro Crítico de Parse no JSON. Texto Bruto: {raw_text}")
        return _disaster_recovery_json()
    except Exception as e:
        print(f"❌ Erro inesperado: {str(e)}")
        return _disaster_recovery_json()


def _disaster_recovery_json() -> dict:
    return {
        "grammar_confidence": 0.0,
        "needs_correction": False,
        "teacher_action": "chat",
        "correction": "Correct! ✨",
        "explanation_pt": "Análise gramatical momentaneamente offline, mas prossiga!",
        "example": "",
        "exercise": "",
        "conversation_reply": "I'm having a little technical hiccup, but I'm still here! What are you up to today?",
    }


def is_invalid_correction(correction: str) -> bool:
    if not correction:
        return True

    correction = correction.lower().strip()

    bad_starts = [
        "you need",
        "you should",
        "try to",
        "remember to",
        "don't forget",
        "change",
        "add",
        "remove",
        "use",
        "put",
        "insert",
        "the correct sentence is",
        "the correct form is",
        "the sentence should be",
    ]

    return any(correction.startswith(prefix) for prefix in bad_starts)
