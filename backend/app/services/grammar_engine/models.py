from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional, TYPE_CHECKING

from app.services.grammar_engine.constants import MarkerCategory




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

    

    metadata: dict[str, object] = field(default_factory=dict)

    # ==========================================================
    # Grammar Analysis API
    # ==========================================================


    @property
    def has_errors(self) -> bool:
        """
        Retorna True se existir pelo menos um erro gramatical.
        """
        return bool(self.errors)


    @property
    def primary_error(self):
        """
        Primeiro erro encontrado.
        """
        if not self.errors:
            return None

        return self.errors[0]


    @property
    def detected_skills(self) -> list[str]:
        """
        Lista de todas as habilidades detectadas.
        """
        return [error.skill for error in self.errors]

    # ==========================================================
    # Concept API
    # ==========================================================


    @property
    def has_concepts(self) -> bool:
        """
        True se algum conceito foi identificado.
        """
        return bool(self.concepts)


    @property
    def primary_concept(self):
        """
        Primeiro conceito identificado.
        """
        if not self.concepts:
            return None

        return self.concepts[0]


    @property
    def concept_names(self) -> list[str]:
        """
        Lista com os nomes dos conceitos encontrados.
        """
        return [concept.name for concept in self.concepts]

    # ==========================================================
    # Learning API
    # ==========================================================


    @property
    def has_learning_profile(self) -> bool:
        """
        Retorna True se existir um perfil de aprendizagem.
        """
        return self.learning_profile is not None


    @property
    def has_learning_focus(self) -> bool:
        """
        Retorna True se houver uma habilidade em foco.
        """
        return (
            self.learning_profile is not None
            and self.learning_profile.current_focus is not None
        )


    @property
    def current_focus(self) -> str | None:
        """
        Skill atualmente em foco.
        """
        if self.learning_profile is None:
            return None

        return self.learning_profile.current_focus
    
    @property
    def accuracy(self) -> float:
        """
        Accuracy geral do aluno.
        """
        if not self.has_learning_profile:
            return 0.0

        return self.learning_profile.overall_accuracy


    @property
    def weak_skills(self) -> list[str]:
        """
        Lista de habilidades fracas.
        """
        if not self.has_learning_profile:
            return []

        return self.learning_profile.weak_skills


    @property
    def mastered_skills(self) -> list[str]:
        """
        Lista de habilidades dominadas.
        """
        if not self.has_learning_profile:
            return []

        return self.learning_profile.mastered_skills


    @property
    def learning_summary(self) -> dict:
        """
        Resumo da aprendizagem do aluno.
        """
        return {
            "focus": self.current_focus,
            "accuracy": self.accuracy,
            "weak_skills": self.weak_skills,
            "mastered_skills": self.mastered_skills,
        }

    # ==========================================================
    # Lesson API
    # ==========================================================


    @property
    def has_lessons(self) -> bool:
        return bool(self.presented_lessons)


    @property
    def primary_lesson(self):
        if not self.presented_lessons:
            return None

        return self.presented_lessons[0]

    # ==========================================================
    # Teaching API
    # ==========================================================


    @property
    def has_teaching_plans(self) -> bool:
        return bool(self.teaching_plans)


    @property
    def primary_teaching_plan(self):
        if not self.teaching_plans:
            return None

        return self.teaching_plans[0]
    
    # ==========================================================
    # summary API
    # ==========================================================
    

    @property
    def summary(self) -> dict:
        """
        Resumo de alto nível da análise.
        """

        return {
            "has_errors": self.has_errors,
            "primary_skill": (self.primary_error.skill if self.primary_error else None),
            "has_concepts": self.has_concepts,
            "primary_concept": (
                self.primary_concept.name if self.primary_concept else None
            ),
            "current_focus": self.current_focus,
            "accuracy": (
                self.learning_profile.overall_accuracy
                if self.has_learning_profile
                else 0.0
            ),
        }