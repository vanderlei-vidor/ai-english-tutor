import types

import app.services.chat_service as chat_service
from app.services.teacher.context import TeacherContext
from app.services.teacher.brain.perception import teacher_perception_engine


def test_prepare_pedagogical_context_returns_expected_keys(monkeypatch):
    memory_data = {
        "conversation_turns": 3,
        "messages_since_last_teaching": 1,
        "english_level": "B1",
        "favorite_topics": {"sports": 5, "tech": 3},
        "weak_skills": {"grammar": 15},
        "common_errors": {},
    }

    monkeypatch.setattr(chat_service, "get_top_topics", lambda topics: ["sports"])
    monkeypatch.setattr(chat_service, "get_top_errors", lambda data: [])
    monkeypatch.setattr(
        chat_service, "should_generate_exercise", lambda *_args, **_kwargs: False
    )
    monkeypatch.setattr(
        chat_service, "choose_exercise_type", lambda *_args, **_kwargs: "fill_blank"
    )
    monkeypatch.setattr(chat_service.random, "random", lambda: 0.95)

    weighted_module = types.SimpleNamespace(
        choose_teaching_skill=lambda _memory_data: "grammar"
    )
    monkeypatch.setitem(
        __import__("sys").modules,
        "app.services.weighted_teaching_engine",
        weighted_module,
    )

    pedagogical = chat_service._prepare_pedagogical_context(memory_data)

    assert pedagogical["allowed_mode"] == "chat"
    assert pedagogical["exercise_focus"] == "grammar"
    assert pedagogical["exercise_type"] == "fill_blank"
    assert pedagogical["theme"] == "sports"
    assert pedagogical["english_level"] == "B1"
    assert pedagogical["exercise_required"] is False
    assert pedagogical["backend_wants_teaching"] is False


def test_apply_correction_guardrails_sets_default_reply_and_correction():
    response_json = {
        "grammar_confidence": 0.99,
        "needs_correction": False,
        "correction": "",
        "conversation_reply": "",
        "example": "",
    }
    messages = [{"content": "I am good"}]
    pedagogical = {"theme": "technology"}

    result = chat_service._apply_correction_guardrails(
        response_json, messages, pedagogical
    )

    assert result["needs_correction"] is False
    assert result["correction"] == "Correct! ✨"
    assert (
        result["explanation_pt"]
        == "Sua frase está totalmente correta! Excelente trabalho. 🥳"
    )
    assert result["conversation_reply"] == "That sounds cool! Tell me more about that."


def test_teacher_perception_uses_known_error_when_grammar_has_no_error():
    grammar = types.SimpleNamespace(
        has_errors=False,
        primary_error=None,
        current_focus=None,
    )
    pedagogical = types.SimpleNamespace(target_skill="verb_usage", estimated_level="A2")
    context = TeacherContext(grammar=grammar, pedagogical=pedagogical)
    context.known_error = {"skill": "verb_usage"}

    perception = teacher_perception_engine.perceive(context)

    assert perception.has_error is True
    assert perception.detected_skill == "verb_usage"
    assert perception.target_skill == "verb_usage"
