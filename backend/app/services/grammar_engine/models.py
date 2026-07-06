from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional, TYPE_CHECKING

from app.services.grammar_engine.constants import MarkerCategory
from app.services.learning.models import LearningProfile



if TYPE_CHECKING:
    from app.services.grammar_engine.semantic.models import SemanticRelation

    from app.services.grammar_engine.concepts.models import GrammarConcept

    from app.services.pedagogical.models import TeachingPlan

    from app.services.pedagogical.lesson_models import TeachingLesson

    from app.services.learning.models import LearningProfile

    from app.services.learning.events import LearningEvent


# ==========================================================
# TOKEN
# Representa uma palavra da frase.
# ==========================================================


@dataclass(slots=True)
class GrammarToken:
    text: str
    lemma: Optional[str] = None
    pos: Optional[str] = None  # VERB / NOUN / ARTICLE ...
    position: int = 0


# ==========================================================
# MARKER
# Marcadores encontrados na frase.
# Ex.: yesterday, last week, since...
# ==========================================================


@dataclass(slots=True)
class GrammarMarker:
    """
    Representa um marcador linguístico encontrado na frase.

    Exemplos:

        GrammarMarker(
            name="TIME_MARKER",
            value="yesterday",
            category="past"
        )

        GrammarMarker(
            name="FREQUENCY_MARKER",
            value="always",
            category="frequency"
        )
    """

    name: str

    value: str

    category: MarkerCategory
    


# ==========================================================
# CONTEXT
# Tudo que os Detectores descobriram.
# Nenhuma decisão pedagógica existe aqui.
# ==========================================================


@dataclass(slots=True)
class GrammarContext:

    # ==========================================
    # Original sentence
    # ==========================================

    original_sentence: str = ""

    tokens: list[GrammarToken] = field(default_factory=list)

    # ==========================================
    # Main grammatical elements
    # ==========================================

    subject: Optional[GrammarToken] = None

    auxiliary: Optional[GrammarToken] = None

    verb: Optional[GrammarToken] = None

    article: Optional[GrammarToken] = None

    # ==========================================
    # Secondary grammatical elements
    # ==========================================

    object: Optional[GrammarToken] = None

    adverbs: list[GrammarToken] = field(default_factory=list)

    prepositions: list[GrammarToken] = field(default_factory=list)


    tense_marker: Optional[str] = None


    markers: list[GrammarMarker] = field(default_factory=list)

    


# ==========================================================
# GRAMMAR ERROR
# Um erro detectado pelas Rules.
# ==========================================================


@dataclass(slots=True)
class GrammarError:
    skill: str

    confidence: float

    severity: int

    explanation: str

    detected_by: Optional[str] = None


# ==========================================================
# GRAMMAR ANALYSIS
# Resultado final do Grammar Engine.
# ==========================================================


@dataclass(slots=True)
class GrammarAnalysis:
    # ==========================================
    # Structural Analysis
    # ==========================================

    context: GrammarContext = field(default_factory=GrammarContext)

    errors: list[GrammarError] = field(default_factory=list)

    # ==========================================
    # Semantic Layer
    # ==========================================

    semantic_relations: list["SemanticRelation"] = field(default_factory=list)

    # ==========================================
    # Knowledge Layer
    # ==========================================

    concepts: list["GrammarConcept"] = field(default_factory=list)


    # ==========================================
    # Learning Events
    # ==========================================

    learning_events: list["LearningEvent"] = field(default_factory=list)

    # ==========================================
    # Learning Layer
    # ==========================================

    
    learning_profile: Optional["LearningProfile"] = None

    # ==========================================
    # Pedagogical Layer
    # ==========================================

    teaching_plans: list["TeachingPlan"] = field(default_factory=list)

    presented_lessons: list["TeachingLesson"] = field(default_factory=list)

    # ==========================================
    # Compatibility Layer
    # ==========================================

    primary_skill: Optional[str] = None

    secondary_skills: list[str] = field(default_factory=list)


    # Confiança global da análise.
    confidence: float = 0.0

    matched_rules: list[str] = field(default_factory=list)

    detected_skills: list[str] = field(default_factory=list)

    metadata: dict[str, object] = field(default_factory=dict)
