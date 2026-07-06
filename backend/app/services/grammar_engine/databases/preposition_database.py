from __future__ import annotations

# ============================================
# PLACE
# ============================================

PLACE_PREPOSITIONS = {
    "in",
    "on",
    "at",
    "under",
    "over",
    "behind",
    "between",
    "inside",
    "outside",
    "near",
}

# ============================================
# TIME
# ============================================

TIME_PREPOSITIONS = {
    "before",
    "after",
    "during",
    "since",
    "until",
    "from",
}

# ============================================
# MOVEMENT
# ============================================

MOVEMENT_PREPOSITIONS = {
    "to",
    "into",
    "onto",
    "towards",
    "through",
}

# ============================================
# GENERAL
# ============================================

GENERAL_PREPOSITIONS = {
    "with",
    "without",
    "for",
    "about",
    "of",
    "by",
    "against",
}

# ============================================
# UNION
# ============================================

ALL_PREPOSITIONS = (
    PLACE_PREPOSITIONS
    | TIME_PREPOSITIONS
    | MOVEMENT_PREPOSITIONS
    | GENERAL_PREPOSITIONS
)
