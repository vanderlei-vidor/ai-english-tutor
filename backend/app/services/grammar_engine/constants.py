from __future__ import annotations

from enum import Enum


# ==========================================================
# SKILLS
# ==========================================================


class Skill(str, Enum):
    PAST_TENSE = "past_tense"

    PRESENT_PERFECT = "present_perfect"

    FUTURE = "future"

    THIRD_PERSON = "third_person"

    ARTICLES = "articles"

    PREPOSITIONS = "prepositions"

    VERB_USAGE = "verb_usage"

    PRONOUNS = "pronouns"

    INFINITIVE = "infinitive"

    IRREGULAR_VERBS = "irregular_verbs"

    PLURAL_NOUNS = "plural_nouns"

    UNCOUNTABLE_NOUNS = "uncountable_nouns"

    OTHER = "other_skill"


# ==========================================================
# MARKERS
# ==========================================================


class Marker(str, Enum):
    TIME = "time"

    FREQUENCY = "frequency"

    LOCATION = "location"

    QUANTITY = "quantity"

    ARTICLE = "article"

    AUXILIARY = "auxiliary"


# ==========================================================
# TOKEN TYPES
# ==========================================================


class TokenType(str, Enum):
    VERB = "VERB"

    NOUN = "NOUN"

    PRONOUN = "PRONOUN"

    ARTICLE = "ARTICLE"

    ADJECTIVE = "ADJECTIVE"

    ADVERB = "ADVERB"

    PREPOSITION = "PREPOSITION"

    AUXILIARY = "AUXILIARY"

    CONJUNCTION = "CONJUNCTION"

    UNKNOWN = "UNKNOWN"


# ==========================================================
# ERROR SEVERITY
# ==========================================================


class Severity(int, Enum):
    LOW = 1

    MEDIUM = 5

    HIGH = 10


# ==========================================================
# MARKER CATEGORY
# ==========================================================


class MarkerCategory(str, Enum):
    PAST = "past"

    PRESENT = "present"

    FUTURE = "future"

    FREQUENCY = "frequency"

    DURATION = "duration"

    PERFECT = "perfect"

    LOCATION = "location"

    QUANTITY = "quantity"

    UNKNOWN = "unknown"