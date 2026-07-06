from app.services.grammar_engine.engine import grammar_engine
from app.services.grammar_engine.concepts.concept_loader import (
    print_concept,
)


def show(title, value):
    """
    Exibe qualquer componente da análise de forma padronizada.
    """

    print(f"\n{title}")

    if value is None:
        print("None")
        return

    if isinstance(value, list):
        if not value:
            print("[]")
            return

        for item in value:
            print(item)

        return

    print(value)


def print_analysis(analysis):
    """
    Imprime toda a análise produzida pelo Grammar Engine.
    """

    print("\n==========================================================")
    print("GRAMMAR ENGINE ANALYSIS")
    print("==========================================================")

    print("\nSentence")
    print(analysis.context.original_sentence)

    print("\n----------------------------------------------------------")

    show("TOKENS", analysis.context.tokens)

    show("SUBJECT", analysis.context.subject)

    show("AUXILIARY", analysis.context.auxiliary)

    show("VERB", analysis.context.verb)

    show("ARTICLE", analysis.context.article)

    show("OBJECT", analysis.context.object)

    show("ADVERBS", analysis.context.adverbs)

    show("PREPOSITIONS", analysis.context.prepositions)

    show("SEMANTIC RELATIONS", analysis.semantic_relations)

    show("TEACHING PLANS", analysis.teaching_plans)

    # --- Nova seção customizada para GRAMMAR CONCEPTS ---
    print()


    print("GRAMMAR CONCEPTS")

    if not analysis.concepts:
            print("None")

    else:
        for concept in analysis.concepts:
            print_concept(concept)
    # -----------------------------------------------------

    show("MARKERS", analysis.context.markers)

    print(f"\nGRAMMAR ERRORS ({len(analysis.errors)})")

    if not analysis.errors:
        print("None")
    else:
        for error in analysis.errors:
            print(error)

    print("\n==========================================================\n")


# ==========================================================
# TEST SENTENCE
# ==========================================================

sentence = "I go yesterday."

analysis = grammar_engine.analyze(sentence)

print_analysis(analysis)
