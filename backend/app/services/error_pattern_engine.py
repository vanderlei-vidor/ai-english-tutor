import re


def detect_known_error(text: str) -> dict | None:
    """
    Detecta erros clássicos de estudantes A1/A2 usando Regex
    alinhado perfeitamente com o motor de Adaptive Weakness Tracker.
    """
    text = text.lower().strip()

    # Mapeamento com suporte a Regex para flexibilidade espacial (.*)
    # e \b para garantir a correspondência de palavras exatas.
    patterns = {
        # === 1. VERB USAGE ===
        r"\btalk\s+english\b": {
            "skill": "verb_usage",
            "correction": "I speak English.",
            "explanation": "Em inglês usamos 'speak English' para idiomas, não 'talk'.",
        },
        r"\bneed\s+learning\b": {
            "skill": "verb_usage",
            "correction": "I need to learn English.",
            "explanation": "Após o verbo 'need', usamos o infinitivo com 'to' (need to learn).",
        },
        # === 2. THIRD PERSON ===
        r"\b(she|he|it)\s+don'?t\b": {
            "skill": "third_person",
            "correction": "He/She doesn't like it.",
            "explanation": "Para a terceira pessoa do singular (He, She, It), o correto é usar 'doesn't'.",
        },
        # === 3. PAST TENSE (Erros de estrutura e verbos irregulares) ===
        r"\bgo.*\byesterday\b": {
            "skill": "past_tense",
            "correction": "I went yesterday.",
            "explanation": "Marcadores de passado como 'yesterday' exigem o verbo no passado simples (went).",
        },
        r"\bbuyed\b": {
            "skill": "past_tense",
            "correction": "bought",
            "explanation": "O verbo 'buy' é irregular. O seu passado correto é 'bought'.",
        },
        r"\bgoed\b": {
            "skill": "past_tense",
            "correction": "went",
            "explanation": "O verbo 'go' é irregular. O seu passado correto é 'went'.",
        },
        # === 4. ARTICLES ===
        r"\ba\s+(apple|orange|egg|hour|it)\b": {
            "skill": "articles",
            "correction": "an apple / an hour",
            "explanation": "Usamos o artigo 'an' antes de palavras que começam com som de vogal.",
        },
        r"\ban\s+(car|computer|house|book|man)\b": {
            "skill": "articles",
            "correction": "a car / a house",
            "explanation": "Usamos o artigo 'a' antes de palavras que começam com som de consoante.",
        },
        r"\bbought\s+computer\b": {
            "skill": "articles",
            "correction": "bought a computer",
            "explanation": "Substantivos contáveis no singular (como computer) exigem um artigo antes (a/the).",
        },
        r"\bbought\s+car\b": {
            "skill": "articles",
            "correction": "bought a car",
            "explanation": "Substantivos contáveis no singular (como car) exigem um artigo antes (a/the).",
        },
        r"\bhave\s+dog\b": {
            "skill": "articles",
            "correction": "have a dog",
            "explanation": "Em inglês, precisamos usar o artigo antes do animal no singular: 'have a dog'.",
        },
        r"\bis\s+teacher\b": {
            "skill": "articles",
            "correction": "is a teacher",
            "explanation": "Sempre usamos artigos indefinidos (a/an) antes de profissões no singular em inglês.",
        },
        r"\bare\s+engineer\b": {
            "skill": "articles",
            "correction": "are an engineer",
            "explanation": "Usamos artigos antes de profissões. Como 'engineer' começa com som de vogal, o correto é 'an engineer'.",
        },
        # === 5. PREPOSITIONS ===
        r"\bdepend\s+of\b": {
            "skill": "prepositions",
            "correction": "depend on",
            "explanation": "Em inglês, a regência correta é 'depend on', e não 'of'.",
        },
        r"\bmarried\s+with\b": {
            "skill": "prepositions",
            "correction": "married to",
            "explanation": "Dizemos que alguém é casado 'to' outra pessoa em inglês (married to).",
        },
        r"\bgood\s+in\s+english\b": {
            "skill": "prepositions",
            "correction": "good at English",
            "explanation": "Para falar sobre habilidades em algo, usamos a preposição 'at' (good at / bad at).",
        },
        r"\barrived\s+in\s+the\s+airport\b": {
            "skill": "prepositions",
            "correction": "arrived at the airport",
            "explanation": "Para locais ou pontos específicos na cidade (como aeroportos), usamos a preposição 'at'.",
        },
        r"\binterested\s+on\b": {
            "skill": "prepositions",
            "correction": "interested in",
            "explanation": "O adjetivo 'interested' é sempre acompanhado pela preposição 'in'.",
        },
        r"\blisten\s+music\b": {
            "skill": "prepositions",
            "correction": "listen to music",
            "explanation": "O verbo 'listen' exige a preposição 'to' quando indicamos o que estamos ouvindo.",
        },
        r"\bgo\s+to\s+home\b": {
            "skill": "prepositions",
            "correction": "go home",
            "explanation": "Com a palavra 'home' não se usa a preposição 'to' quando combinada com verbos de movimento.",
        },
        # === 6. NOUNS ===
        r"\binformations\b": {
            "skill": "nouns",
            "correction": "information",
            "explanation": "A palavra 'information' é incontável em inglês e não tem plural com 's'.",
        },
        r"\badvices\b": {
            "skill": "nouns",
            "correction": "advice",
            "explanation": "A palavra 'advice' (conselho) é incontável, use apenas 'advice' ou 'pieces of advice'.",
        },
        r"\bpeoples\b": {
            "skill": "nouns",
            "correction": "people",
            "explanation": "A palavra 'people' já é o plural coletivo de pessoa. Não use 'peoples'.",
        },
    }

    # Varredura utilizando o motor de expressões regulares
    for pattern, data in patterns.items():
        if re.search(pattern, text):
            return data

    return None
