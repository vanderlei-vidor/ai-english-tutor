from __future__ import annotations
from app.services.grammar_engine.detectors.subject_detector import SubjectDetector
from app.services.grammar_engine.detectors.verb_detector import VerbDetector
from app.services.grammar_engine.detectors.marker_detector import MarkerDetector
from app.services.grammar_engine.rules.third_person_rule import ThirdPersonRule
from app.services.grammar_engine.rules.past_tense_rule import PastTenseRule
from app.services.grammar_engine.detectors.adverb_detector import AdverbDetector
from app.services.grammar_engine.detectors.auxiliary_detector import AuxiliaryDetector
from app.services.grammar_engine.detectors.object_detector import ObjectDetector
from app.services.grammar_engine.detectors.article_detector import ArticleDetector
from app.services.grammar_engine.detectors.preposition_detector import PrepositionDetector

# ==========================================================
# REGISTRY DO GRAMMAR ENGINE
#
# Este módulo registra todos os componentes do motor.
#
# O Engine nunca conhece diretamente Detectores,
# Rules ou Analyzers.
#
# Isso permite adicionar novos componentes
# sem modificar o Engine.
# ==========================================================


# ----------------------------------------------------------
# DETECTORS
# ----------------------------------------------------------

_DETECTORS = [
    SubjectDetector(),
    AuxiliaryDetector(),
    AdverbDetector(),
    VerbDetector(),
    ArticleDetector(),
    ObjectDetector(),
    PrepositionDetector(),
    MarkerDetector(),
]


def get_detectors():
    """
    Retorna todos os Detectores registrados.
    """
    return _DETECTORS


# ----------------------------------------------------------
# RULES
# ----------------------------------------------------------

_RULES = [
    ThirdPersonRule(),
    PastTenseRule(),
]


def get_rules():
    """
    Retorna todas as Rules registradas.
    """
    return _RULES


# ----------------------------------------------------------
# ANALYZERS
# ----------------------------------------------------------

_ANALYZERS = []


def get_analyzers():
    """
    Retorna todos os Analyzers registrados.
    """
    return _ANALYZERS
