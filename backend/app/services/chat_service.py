import os
import json
import time
import re
import requests
from dataclasses import dataclass
from dotenv import load_dotenv
from app.services.memory_utils import get_top_topics
from app.services.exercise_engine import choose_exercise_type

from app.services.skill_exercise_engine import get_skill_specific_exercise

from app.services.level_estimator import estimate_level

from app.services.prompt_builder.static.builder import (
    static_prompt_builder,
)
from app.services.teacher.response.executor import (
    teacher_output,
)

load_dotenv()

LM_STUDIO_URL = os.getenv("LM_STUDIO_URL", "http://localhost:1234/v1/chat/completions")
MODEL_NAME = os.getenv("LM_STUDIO_MODEL", "qwen2.5-7b-instruct")

MAX_REGENERATION_ATTEMPTS = 1

REQUIRED_JSON_FIELDS = [
    "grammar_confidence",
    "needs_correction",
    "teacher_action",
    "correction",
    "explanation_pt",
    "example",
    "exercise",
    "conversation_reply",
]

VALID_ACTIONS = ["chat", "question", "exercise", "correction"]

static_prompt_builder.build()


@dataclass
class ResponseValidation:
    is_valid: bool
    reason: str = ""


def validate_correction(correction: str, needs_correction: bool) -> str:
    """Filtra correções vagas geradas pelo modelo."""
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


def _validate_response_json(response_json: dict) -> ResponseValidation:
    """
    Valida a resposta do LLM sem modificar conteúdo pedagógico.
    Retorna inválido quando a resposta precisa ser regenerada.
    """
    for field in REQUIRED_JSON_FIELDS:
        if field not in response_json or response_json[field] is None:
            return ResponseValidation(
                is_valid=False,
                reason=f"Missing required field: {field}",
            )

    teacher_action = response_json.get("teacher_action", "chat")
    if teacher_action not in VALID_ACTIONS:
        return ResponseValidation(
            is_valid=False,
            reason=f"Invalid teacher_action: {teacher_action}",
        )

    handler = response_json.get(
        "teacher_handler",
    )


    needs_correction = response_json.get(
        "needs_correction",
        False,
    )

    correction = response_json.get(
        "correction",
        "",
    )

    if handler == "CorrectionHandler" and needs_correction:
        validated = validate_correction(
            correction,
            needs_correction=True,
        )

        if not validated or is_invalid_correction(validated):
            return ResponseValidation(
                is_valid=False,
                reason=("CorrectionHandler requires a valid correction."),
            )

    if not response_json.get("conversation_reply", "").strip():
        return ResponseValidation(
            is_valid=False,
            reason="Empty conversation_reply",
        )

    return ResponseValidation(is_valid=True)


def _build_brain_memory_context(
    brain,
    memory_data,
) -> str:
    plan = brain.planning

    target_skill = plan.target_skill or "conversation"

    english_level = brain.student.estimated_level or memory_data.get(
        "english_level", "A2"
    )

    exercise_type = plan.exercise_type or choose_exercise_type(memory_data)

    favorite_topics = memory_data.get("favorite_topics", {})
    top_topics = get_top_topics(
        favorite_topics if isinstance(favorite_topics, dict) else {}
    )
    theme = top_topics[0].lower() if top_topics else "technology"

    exercise_required = plan.generate_exercise

    return f"""
### DYNAMIC USER CONTEXT ###
ALLOWED TEACHING MODE FOR THIS TURN: {plan.teaching_mode} (Strictly obey this directive!)
MANDATORY TARGET SKILL TO TRAIN: {target_skill}
Exercise Format Required: {exercise_type}
Exercise Theme: {theme}
User English Level: {english_level}
Conversation Style: {memory_data.get("conversation_style", "casual")}
Exercise Required Right Now: {"YES" if exercise_required else "NO"}
"""


def _build_system_prompt(
    dynamic_prompt,
    memory_context,
) -> str:
    return (
        static_prompt_builder.build()
        + "\n\n"
        + dynamic_prompt
        + "\n\n"
        + memory_context
    )


def _call_llm(full_messages) -> str:
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

        return response.json()["choices"][0]["message"]["content"].strip()

    except Exception as e:
        print(f"❌ Erro de requisição no LM Studio: {str(e)}")
        raise


def _parse_response_json(raw_text) -> dict:
    cleaned_text = re.sub(r",\s*}", "}", raw_text)
    cleaned_text = re.sub(r",\s*]", "]", cleaned_text)

    if cleaned_text != raw_text:
        print("JSON AUTO-REPAIRED (Regex Rule)")

    return json.loads(cleaned_text)


def _apply_teacher_output(
    response_json,
    teacher_result,
) -> tuple[dict, str]:
    response_json = teacher_output.apply(
        brain=teacher_result.brain,
        llm_response=response_json,
    )

    teacher_action = teacher_result.brain.execution.handler

    print()
    print("=" * 60)
    print("TEACHER FINAL DECISION")
    print("=" * 60)

    print(f"ACTION: {teacher_result.brain.execution.handler}")
    print(f"MODE: {teacher_result.brain.planning.teaching_mode}")
    print(f"REASON: {teacher_result.brain.planning.teacher_reason}")

    print("=" * 60)

    return response_json, teacher_action


def _generate_exercise(
    response_json,
    teacher_action,
    brain,
    memory_data,
) -> dict:
    plan = brain.planning

    target_skill = plan.target_skill or "conversation"
    exercise_type = plan.exercise_type or choose_exercise_type(memory_data)

    execution_handler = brain.execution.handler

    if execution_handler in ("chat", "correction"):
        response_json["exercise"] = ""

    elif execution_handler in ("exercise", "question"):
        advanced_structures = memory_data.get("advanced_structures", {})
        adaptive_level = estimate_level(advanced_structures)

        print(
            f"🎯 SKILL EXERCISE ENGINE ACTIVATED -> {target_skill} (level: {adaptive_level})"
        )

        response_json["exercise"] = get_skill_specific_exercise(
            skill=target_skill,
            level=adaptive_level,
            exercise_type=exercise_type,
        )
        print(f"🎯 ADAPTIVE EXERCISE GENERATED: {response_json['exercise']}")

    return response_json


def generate_response(
    messages: list, prompt_context, teacher_result, memory_data: dict
) -> dict:

    brain = teacher_result.brain

    memory_context = _build_brain_memory_context(
        brain,
        memory_data,
    )

    from app.services.prompt_builder.composer import prompt_composer

    dynamic_prompt = prompt_composer.compose(
        prompt_context,
        teacher_prompt=brain.prompt,
    )

    system_prompt = _build_system_prompt(
        dynamic_prompt,
        memory_context,
    )

    print()
    print("=" * 60)
    print("FINAL SYSTEM PROMPT")
    print("=" * 60)
    print(system_prompt)
    print("=" * 60)

    full_messages = [
        {
            "role": "system",
            "content": system_prompt,
        }
    ] + messages

    response_json = None
    raw_text = ""

    for attempt in range(MAX_REGENERATION_ATTEMPTS + 1):
        try:
            raw_text = _call_llm(full_messages)
            print()

            print("=" * 60)
            print("RAW LLM RESPONSE")
            print("=" * 60)
            print(raw_text)
            print("=" * 60)
            response_json = _parse_response_json(raw_text)

        except Exception:
            if attempt >= MAX_REGENERATION_ATTEMPTS:
                return _disaster_recovery_json()
            continue

        validation = _validate_response_json(response_json)

        if validation.is_valid:
            break

        print(f"⚠️ INVALID LLM RESPONSE (attempt {attempt + 1}): {validation.reason}")

        if attempt < MAX_REGENERATION_ATTEMPTS:
            full_messages.append(
                {
                    "role": "assistant",
                    "content": raw_text,
                }
            )
            full_messages.append(
                {
                    "role": "system",
                    "content": (
                        f"Your previous response was invalid: {validation.reason}. "
                        "Regenerate a complete valid JSON response. "
                        "Obey all Teacher Instructions."
                    ),
                }
            )
    else:
        return _disaster_recovery_json()

    try:
        response_json, teacher_action = _apply_teacher_output(
            response_json,
            teacher_result,
        )

        response_json = _generate_exercise(
            response_json,
            teacher_action,
            brain,
            memory_data,
        )

        response_json["target_skill"] = brain.planning.target_skill

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
        "correction": "",
        "explanation_pt": "Análise gramatical momentaneamente offline, mas prossiga!",
        "example": "",
        "exercise": "",
        "conversation_reply": "I'm having a little technical hiccup, but I'm still here! What are you up to today?",
    }
