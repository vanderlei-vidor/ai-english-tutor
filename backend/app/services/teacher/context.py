from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

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

    # Memória de longo prazo do aluno — usada pelos
    # seletores adaptativos (ex.: StudentSkillSelector).
    memory_data: dict[str, Any] = field(default_factory=dict)

    # Opcionais
    known_error: dict | None = None

    conversation_id: str | None = None

    message: str | None = None
