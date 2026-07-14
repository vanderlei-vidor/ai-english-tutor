from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class TeacherPrompt:
    mode: str = ""

    action: str = ""

    tone: str = ""

    style: str = ""

    goal: str = ""

    target_skill: str | None = None

    explanation_level: str = "normal"

    generate_example: bool = False

    generate_exercise: bool = False

    ask_question: bool = False

    wait_student: bool = True

    instructions: list[str] = field(default_factory=list)

    constraints: list[str] = field(default_factory=list)
