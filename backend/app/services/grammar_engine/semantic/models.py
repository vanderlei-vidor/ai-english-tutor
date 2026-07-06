from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class SemanticRelation:
    name: str

    confidence: float

    description: str

    detected_by: str
