import types



import app.services.chat_service as chat_service

from app.services.error_pattern_engine import detect_known_error

from app.services.teacher.context import TeacherContext

from app.services.teacher.brain.perception import teacher_perception_engine





def test_build_brain_memory_context_uses_brain_planning(monkeypatch):

    memory_data = {

        "english_level": "B1",

        "favorite_topics": {"sports": 5, "tech": 3},

        "conversation_style": "casual",

    }



    plan = types.SimpleNamespace(

        target_skill="grammar",

        teaching_mode="conversation",

        exercise_type="fill_blank",

        generate_exercise=False,

    )

    student = types.SimpleNamespace(estimated_level="B1")

    brain = types.SimpleNamespace(planning=plan, student=student)



    monkeypatch.setattr(chat_service, "get_top_topics", lambda topics: ["sports"])



    context = chat_service._build_brain_memory_context(brain, memory_data)



    assert "ALLOWED TEACHING MODE FOR THIS TURN: conversation" in context

    assert "MANDATORY TARGET SKILL TO TRAIN: grammar" in context

    assert "Exercise Format Required: fill_blank" in context

    assert "Exercise Theme: sports" in context

    assert "User English Level: B1" in context

    assert "Exercise Required Right Now: NO" in context





def test_validate_response_json_accepts_valid_response():

    response_json = {

        "grammar_confidence": 0.99,

        "needs_correction": False,

        "teacher_action": "chat",

        "correction": "Correct! ✨",

        "explanation_pt": "Sua frase está excelente!",

        "example": "",

        "exercise": "",

        "conversation_reply": "That sounds cool!",

    }



    result = chat_service._validate_response_json(response_json)



    assert result.is_valid is True





def test_validate_response_json_rejects_invalid_correction():

    response_json = {

        "grammar_confidence": 0.5,

        "needs_correction": True,

        "teacher_action": "correction",

        "correction": "you need to use past tense",

        "explanation_pt": "Use o passado.",

        "example": "",

        "exercise": "",

        "conversation_reply": "Try again.",

    }



    result = chat_service._validate_response_json(response_json)



    assert result.is_valid is False

    assert "correction" in result.reason.lower()





def test_detect_known_error_returns_detector_fields_only():

    result = detect_known_error("I go yesterday")



    assert result is not None

    assert result["skill"] == "past_tense"

    assert "confidence" in result

    assert "rule" in result

    assert "correction" not in result

    assert "explanation" not in result





def test_teacher_perception_uses_known_error_when_grammar_has_no_error():

    grammar = types.SimpleNamespace(

        has_errors=False,

        primary_error=None,

        current_focus=None,

    )

    pedagogical = types.SimpleNamespace(target_skill="verb_usage", estimated_level="A2")

    context = TeacherContext(

        user_id="test-user",

        grammar=grammar,

        pedagogical=pedagogical,

    )

    context.known_error = {

        "skill": "verb_usage",

        "confidence": 0.95,

        "rule": "Use 'speak' for languages",

    }



    perception = teacher_perception_engine.perceive(context)



    assert perception.has_error is True

    assert perception.detected_skill == "verb_usage"

    assert perception.target_skill == "verb_usage"

