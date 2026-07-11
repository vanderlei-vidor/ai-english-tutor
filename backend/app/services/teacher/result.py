from __future__ import annotations

from dataclasses import dataclass

from app.services.teacher.brain.state import (
    TeacherBrainState,
)


@dataclass(slots=True)
class TeacherResult:
    """
    Resultado produzido pelo Teacher Brain.

    Todo o restante do sistema deve consumir
    apenas o estado produzido pelo Brain.
    """

    brain: TeacherBrainState
