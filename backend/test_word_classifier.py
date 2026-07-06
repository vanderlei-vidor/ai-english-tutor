from app.services.grammar_engine.classifiers.word_classifier import classify_word

WORDS = [
    "a",
    "has",
    "always",
    "you",
    "pizza",
]

for word in WORDS:
    result = classify_word(word)

    print("-" * 40)
    print(word)
    print(result)
