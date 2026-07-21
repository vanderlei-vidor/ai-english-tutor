import re


def detect_known_error(text: str) -> dict | None:
    """
    Detector de erros conhecidos — apenas identifica skill, confiança e regra.
    Não produz correções; quem decide ensinar é o TeacherBrain.
    """
    text = text.lower().strip()

    patterns = {
        # === 1. VERB USAGE ===
        r"\btalk\s+english\b": {
            "skill": "verb_usage",
            "confidence": 0.95,
            "rule": "Use 'speak' for languages, not 'talk'",
        },
        r"\bneed\s+learning\b": {
            "skill": "verb_usage",
            "confidence": 0.90,
            "rule": "After 'need', use infinitive with 'to' (need to learn)",
        },
        # === 2. THIRD PERSON ===
        r"\b(she|he|it)\s+don'?t\b": {
            "skill": "third_person",
            "confidence": 0.95,
            "rule": "Third person singular requires 'doesn't', not 'don't'",
        },
        # === 3. PAST TENSE ===
        r"\bgo.*\byesterday\b": {
            "skill": "past_tense",
            "confidence": 0.95,
            "rule": "Past time markers like 'yesterday' require past tense verb form",
        },
        r"\bbuyed\b": {
            "skill": "past_tense",
            "confidence": 0.98,
            "rule": "'buy' is irregular — past form is 'bought'",
        },
        r"\bgoed\b": {
            "skill": "past_tense",
            "confidence": 0.98,
            "rule": "'go' is irregular — past form is 'went'",
        },
        # === 4. ARTICLES ===
        r"\ba\s+(apple|orange|egg|hour|it)\b": {
            "skill": "articles",
            "confidence": 0.90,
            "rule": "Use 'an' before vowel sounds",
        },
        r"\ban\s+(car|computer|house|book|man)\b": {
            "skill": "articles",
            "confidence": 0.90,
            "rule": "Use 'a' before consonant sounds",
        },
        r"\bbought\s+computer\b": {
            "skill": "articles",
            "confidence": 0.92,
            "rule": "Countable singular nouns require an article (a/the)",
        },
        r"\bbought\s+car\b": {
            "skill": "articles",
            "confidence": 0.92,
            "rule": "Countable singular nouns require an article (a/the)",
        },
        r"\bhave\s+dog\b": {
            "skill": "articles",
            "confidence": 0.90,
            "rule": "Singular countable nouns need an article: 'have a dog'",
        },
        r"\bis\s+teacher\b": {
            "skill": "articles",
            "confidence": 0.90,
            "rule": "Professions in singular require an indefinite article (a/an)",
        },
        r"\bare\s+engineer\b": {
            "skill": "articles",
            "confidence": 0.90,
            "rule": "Professions require an article; 'engineer' takes 'an'",
        },
        # === 5. PREPOSITIONS ===
        r"\bdepend\s+of\b": {
            "skill": "prepositions",
            "confidence": 0.95,
            "rule": "Correct collocation is 'depend on', not 'depend of'",
        },
        r"\bmarried\s+with\b": {
            "skill": "prepositions",
            "confidence": 0.95,
            "rule": "Use 'married to', not 'married with'",
        },
        r"\bgood\s+in\s+english\b": {
            "skill": "prepositions",
            "confidence": 0.92,
            "rule": "Skills use 'good at', not 'good in'",
        },
        r"\barrived\s+in\s+the\s+airport\b": {
            "skill": "prepositions",
            "confidence": 0.90,
            "rule": "Specific points/locations use 'at', not 'in'",
        },
        r"\binterested\s+on\b": {
            "skill": "prepositions",
            "confidence": 0.95,
            "rule": "'Interested' collocates with 'in', not 'on'",
        },
        r"\blisten\s+music\b": {
            "skill": "prepositions",
            "confidence": 0.95,
            "rule": "'Listen' requires 'to' when followed by an object",
        },
        r"\bgo\s+to\s+home\b": {
            "skill": "prepositions",
            "confidence": 0.92,
            "rule": "With 'home' as destination, omit 'to' (go home)",
        },
        # === 6. NOUNS ===
        r"\binformations\b": {
            "skill": "nouns",
            "confidence": 0.98,
            "rule": "'Information' is uncountable — no plural with 's'",
        },
        r"\badvices\b": {
            "skill": "nouns",
            "confidence": 0.98,
            "rule": "'Advice' is uncountable — use 'advice' or 'pieces of advice'",
        },
        r"\bpeoples\b": {
            "skill": "nouns",
            "confidence": 0.95,
            "rule": "'People' is already plural — do not add 's'",
        },
    }

    for pattern, data in patterns.items():
        if re.search(pattern, text):
            return data

    return None
