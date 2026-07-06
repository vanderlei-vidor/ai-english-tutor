from __future__ import annotations

import re


# ==========================================================
# NORMALIZATION
# ==========================================================


def normalize_text(text: str) -> str:
    """
    Normaliza uma frase para facilitar análises.

    - lowercase
    - remove espaços duplicados
    - remove espaços nas extremidades
    """

    if not text:
        return ""

    text = text.lower().strip()
    text = re.sub(r"\s+", " ", text)

    return text


# ==========================================================
# TOKENIZATION
# ==========================================================


def tokenize(text: str) -> list[str]:
    """
    Tokenização simples baseada em espaços.

    Exemplo:

    "She likes pizza."

    →

    ["she", "likes", "pizza"]
    """

    text = normalize_text(text)

    text = re.sub(r"[.,!?;:]", "", text)

    if not text:
        return []

    return text.split()


# ==========================================================
# WORD SEARCH
# ==========================================================


def contains_word(text: str, word: str) -> bool:
    """
    Procura uma palavra inteira.

    Evita falsos positivos usando limite de palavra.
    """

    text = normalize_text(text)
    word = normalize_text(word)

    return (
        re.search(
            rf"\b{re.escape(word)}\b",
            text,
        )
        is not None
    )


# ==========================================================
# SAFE GET TOKEN
# ==========================================================


def safe_token(tokens: list[str], index: int):
    """
    Retorna um token de forma segura.

    Evita IndexError.
    """

    if index < 0:
        return None

    if index >= len(tokens):
        return None

    return tokens[index]


# ==========================================================
# IS EMPTY
# ==========================================================


def is_empty(text: str | None) -> bool:

    return not text or not text.strip()
