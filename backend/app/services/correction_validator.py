import difflib
import re

# Respostas/Elogios comuns que a IA envia e devem ser desconsiderados como erro
GENERIC_RESPONSES = {
    "correct! ✨",
    "correct!",
    "great!",
    "great job!",
    "excellent!",
    "well done!",
    "good job!",
    "very good!",
    "nice!",
    "perfect!",
}

SKILL_MARKERS = {
    "past_tense": [
        "yesterday",
        "ago",
        "last",
        "went",
        "was",
        "were",
        "did",
        "had",
        "bought",
    ],
    "articles": [" a ", " an ", " the ", "article", "an apple", "a car", "an hour"],
    "prepositions": [
        " at ",
        " on ",
        " in ",
        " to ",
        " for ",
        " with ",
        "depend on",
        "married to",
        "good at",
    ],
    "third_person": ["doesn't", "he", "she", "it", "likes", "works", "goes", "listens"],
    "verb_usage": ["speak english", "need to", "use", "verb", "learn english"],
    "pronouns": ["he", "she", "they", "his", "her", "them", "we", "our"],
    "infinitive": ["to learn", "to go", "to study", "infinitive"],
    "irregular_verbs": ["went", "bought", "saw", "ate", "had", "did"],
    "plural_nouns": ["people", "children", "men", "women"],
    "uncountable_nouns": ["information", "advice", "furniture", "money"],
}


def normalize_sentence(text: str) -> str:
    if not text:
        return ""
    text = text.lower().strip()
    text = text.strip(" .!?\"'")
    return re.sub(r"\s+", " ", text)


def tokenize(text: str) -> list[str]:
    """
    Tokenização simples e estável para comparar conteúdo sem pontuação.
    """
    text = normalize_sentence(text)
    if not text:
        return []
    return re.findall(r"\b[\w']+\b", text)

def is_small_morphological_fix(user_tokens: list[str], corr_tokens: list[str]) -> bool:
    """
    Detecta microcorreções legítimas como:
    listen -> listens
    go -> goes
    work -> works
    play -> plays
    """
    if len(user_tokens) != len(corr_tokens):
        return False

    diffs = []
    for u, c in zip(user_tokens, corr_tokens):
        if u != c:
            diffs.append((u, c))

    # só aceitamos 1 mudança pontual
    if len(diffs) != 1:
        return False

    old, new = diffs[0]

    # listen -> listens / work -> works / play -> plays
    if new == f"{old}s" or new == f"{old}es":
        return True

    # caso simples de remoção/adaptação de "y" -> "ies"
    # ex: study -> studies
    if old.endswith("y") and new == old[:-1] + "ies":
        return True

    return False


def is_real_third_person_fix(user_tokens: list[str], corr_tokens: list[str]) -> bool:
    """
    Detecta correções reais de 3rd person singular, por exemplo:
    she always listen to music -> she always listens to music
    he work every day -> he works every day
    """
    if len(user_tokens) != len(corr_tokens):
        return False

    if not user_tokens:
        return False

    # precisa começar com sujeito típico de 3rd person
    if user_tokens[0] not in {"he", "she", "it"}:
        return False

    diffs = []
    for u, c in zip(user_tokens, corr_tokens):
        if u != c:
            diffs.append((u, c))

    # queremos exatamente uma única mudança lexical
    if len(diffs) != 1:
        return False

    old, new = diffs[0]

    # listen -> listens / work -> works / go -> goes
    if new == f"{old}s" or new == f"{old}es":
        return True

    # study -> studies
    if old.endswith("y") and new == old[:-1] + "ies":
        return True

    return False


def is_rephrase_equivalent(user_text: str, correction: str) -> bool:
    """
    Detecta rephrases inocentes / equivalências aceitáveis
    que NÃO devem ser tratadas como erro real.
    """
    user = normalize_sentence(user_text)
    corr = normalize_sentence(correction)

    if not user or not corr:
        return False

    if user == corr:
        return True

    # playing -> to play (caso clássico da fase 12.8)
    user_simplified = user.replace(" likes playing ", " likes to play ")
    corr_simplified = corr.replace(" likes playing ", " likes to play ")

    if user_simplified == corr or corr_simplified == user:
        return True

    # Ajuste simples para gerúndio -> infinitivo
    user_alt = re.sub(r"\b(\w+)ing\b", r"to \1", user)
    corr_alt = re.sub(r"\b(\w+)ing\b", r"to \1", corr)

    if user_alt == corr or corr_alt == user:
        return True

    if user_alt.replace("to ", "") == corr_alt.replace("to ", ""):
        return True

    return False


def is_invalid_correction_rewrite(user_text: str, correction: str) -> bool:
    """
    FASE 12.9 — bloqueia 'correções' que na verdade são frases inventadas
    ou rewrites que mudam o conteúdo-base do enunciado.

    Exemplo:
    user:      I went yesterday.
    correction: Yesterday, I went to the store.

    Isso NÃO é correção. É uma frase nova com conteúdo extra.
    """
    user_tokens = tokenize(user_text)
    corr_tokens = tokenize(correction)

    if not user_tokens or not corr_tokens:
        return False

        # 🔥 Não bloquear microcorreções legítimas
    if is_small_morphological_fix(user_tokens, corr_tokens):
        return False

    # Se for idêntico ou rephrase equivalente, não é rewrite inválido
    if normalize_sentence(user_text) == normalize_sentence(correction):
        return False

    if is_rephrase_equivalent(user_text, correction):
        return False

    user_set = set(user_tokens)
    corr_set = set(corr_tokens)

    common_tokens = user_set.intersection(corr_set)

    # Se não compartilham quase nada, é praticamente outra frase
    if len(common_tokens) <= 1:
        return True

    added_tokens = corr_set - user_set
    removed_tokens = user_set - corr_set

    # ---------------------------------------------------------
    # Regra principal da FASE 12.9:
    # se a correção adiciona muito conteúdo novo e não parece
    # uma correção gramatical local, tratamos como rewrite inválido
    # ---------------------------------------------------------
    suspicious_added_threshold = 2

    # tokens que frequentemente aparecem em correções legítimas
    allowed_small_grammar_tokens = {
        "a",
        "an",
        "the",
        "to",
        "in",
        "on",
        "at",
        "for",
        "with",
        "of",
        "is",
        "are",
        "was",
        "were",
        "do",
        "does",
        "did",
        "has",
        "have",
        "had",
        "am",
    }

    suspicious_added = [
        token for token in added_tokens if token not in allowed_small_grammar_tokens
    ]

    # Ex.: "I went yesterday." -> "Yesterday, I went to the store."
    # added_tokens relevantes = {"store"}
    # ou até {"to", "the", "store"} dependendo do caso
    if len(suspicious_added) >= suspicious_added_threshold:
        return True

    # Heurística extra:
    # se a frase corrigida ficou muito maior e trouxe conteúdo novo,
    # isso é fortíssimo sinal de rewrite.
    if len(corr_tokens) >= len(user_tokens) + 3 and len(suspicious_added) >= 1:
        return True

    # Se removeu muita coisa da frase original e adicionou outra ideia,
    # também tratamos como rewrite inválido.
    if len(removed_tokens) >= 2 and len(suspicious_added) >= 1:
        return True

    return False


def is_real_correction_by_skill(
    correction: str,
    target_skill: str | None = None,
) -> bool:
    """
    Valida se o texto de correção/explicação da IA realmente aciona
    os gatilhos da skill alvo.
    """
    if not correction or not target_skill:
        return False

    text = correction.strip().lower()
    target_skill = target_skill.strip().lower()
    markers = SKILL_MARKERS.get(target_skill)

    print("====== is_real_correction_by_skill ======")
    print(f"TARGET: {target_skill}")
    print(f"TEXT: {correction}")

    if not markers:
        return False

    for marker in markers:
        print(f"Checking marker -> {marker}")
        if marker.startswith(" ") or marker.endswith(" "):
            if marker in f" {text} ":
                return True
        else:
            if re.search(rf"\b{re.escape(marker)}\b", text):
                return True

    return False



def is_real_english_error(
    user_text: str,
    correction: str,
    teacher_action: str,
    needs_correction: bool,
    detected_skill: str | None = None,
    target_skill: str | None = None,
) -> bool:
    result = analyze_correction_validity(
        user_text=user_text,
        correction=correction,
        teacher_action=teacher_action,
        needs_correction=needs_correction,
        detected_skill=detected_skill,
        target_skill=target_skill,
    )
    return result["is_real_error"]


def detect_non_target_skill(user_text: str, correction: str) -> str | None:
    """
    Detecta skill real fora da skill-alvo usando diff lexical.
    """
    user = normalize_sentence(user_text)
    corr = normalize_sentence(correction)

    if not user or not corr:
        return None

    user_tokens = user.split()
    corr_tokens = corr.split()

    diff = list(difflib.ndiff(user_tokens, corr_tokens))
    removed_words = [d[2:] for d in diff if d.startswith("- ")]
    added_words = [d[2:] for d in diff if d.startswith("+ ")]

    # ------------------------------------------------------
    # 1) THIRD PERSON
    # ------------------------------------------------------
    subjects_3rd = {"he", "she", "it"}
    if user_tokens and user_tokens[0] in subjects_3rd:
        for r_word in removed_words:
            for a_word in added_words:
                if a_word == f"{r_word}s" or a_word == f"{r_word}es":
                    return "third_person"

    # ------------------------------------------------------
    # 2) ARTICLES
    # ------------------------------------------------------
    articles = {"a", "an", "the"}
    if any(w in articles for w in removed_words) or any(
        w in articles for w in added_words
    ):
        return "articles"

    # ------------------------------------------------------
    # 3) PREPOSITIONS
    # ------------------------------------------------------
    prepositions = {"in", "on", "at", "to", "for", "with", "from", "about", "of", "by"}
    if any(w in prepositions for w in removed_words) or any(
        w in prepositions for w in added_words
    ):
        return "prepositions"

    # ------------------------------------------------------
    # 4) VERB USAGE / INFINITIVE
    # ------------------------------------------------------
    if "to" in removed_words and "to" not in added_words:
        return "verb_usage"

    if "to" not in removed_words and "to" in added_words:
        return "infinitive"

    return None


def analyze_correction_validity(
    user_text: str,
    correction: str,
    teacher_action: str,
    needs_correction: bool,
    detected_skill: str | None = None,
    target_skill: str | None = None,
) -> dict:
    """
    FASE 13.0
    Analisa a correction e devolve:
    - is_real_error: bool
    - reason: motivo explícito do sanitizer
    """
    if teacher_action != "correction" or not needs_correction:
        return {
            "is_real_error": False,
            "reason": "not_a_correction_action",
        }

    corr_norm = normalize_sentence(correction)
    user_norm = normalize_sentence(user_text)

    if not corr_norm:
        return {
            "is_real_error": False,
            "reason": "empty_correction",
        }

    if corr_norm in GENERIC_RESPONSES:
        return {
            "is_real_error": False,
            "reason": "generic_praise",
        }

    user_tokens = tokenize(user_text)
    corr_tokens = tokenize(correction)

    # 🔥 microcorreção real de 3rd person
    if is_real_third_person_fix(user_tokens, corr_tokens):
        return {
            "is_real_error": True,
            "reason": "real_third_person_fix",
        }

    # frase idêntica
    if user_norm == corr_norm:
        return {
            "is_real_error": False,
            "reason": "identical_text",
        }

    # rephrase equivalente
    if is_rephrase_equivalent(user_text, correction):
        return {
            "is_real_error": False,
            "reason": "rephrase_equivalent",
        }

    # rewrite inventado
    if is_invalid_correction_rewrite(user_text, correction):
        return {
            "is_real_error": False,
            "reason": "invalid_rewrite",
        }

    invalid_skills = {"", "unknown", "null", "none"}

    # skill detectada válida pela IA
    if detected_skill and detected_skill.strip().lower() not in invalid_skills:
        return {
            "is_real_error": True,
            "reason": "detected_skill_from_ai",
        }

    # bate com a target skill
    if target_skill and is_real_correction_by_skill(correction, target_skill):
        return {
            "is_real_error": True,
            "reason": "target_skill_marker_match",
        }

    # fallback conservador
    return {
        "is_real_error": True,
        "reason": "fallback_real_error",
    }