from __future__ import annotations

from dataclasses import dataclass

from app.services.grammar_engine.models import GrammarAnalysis
from app.services.pedagogical.analysis import PedagogicalAnalysis


@dataclass(slots=True)
class TeacherContext:
    """
    Tudo o que o Teacher sabe sobre
    esta interação.

    Novas camadas (memory, curriculum,
    personality...) serão adicionadas aqui.
    """

    user_id: str

    grammar: GrammarAnalysis

    pedagogical: PedagogicalAnalysis

    # Opcionais
    known_error: dict | None = None

    conversation_id: str | None = None

    message: str | None = None
