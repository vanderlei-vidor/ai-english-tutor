from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class SkillFocus:
    """
    Representa todas as informações sobre
    o foco pedagógico do momento.

    Cada campo possui uma responsabilidade
    específica.
    """

    # Skill detectada pelo Grammar Engine
    detected: str | None = None

    # Skill que será ensinada nesta interação
    teaching: str | None = None

    # Skill sugerida pelo Backend Pedagógico
    recommended: str | None = None

    # Skill mais fraca do aluno
    weakest: str | None = None
