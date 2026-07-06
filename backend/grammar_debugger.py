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

    # --- CORRIGIDO: Agora tudo isso faz parte da função print_analysis ---
    print("\nLEARNING PROFILE")

    profile = analysis.learning_profile

    if profile is None:
        print("None")
    else:
        print("----------------------------------")
        print(f"Student ID      : {profile.student_id}")
        print(f"CEFR Level      : {profile.cefr_level}")
        print(f"Current Focus   : {profile.current_focus}")
        print(f"Accuracy        : {profile.overall_accuracy:.2f}%")

        print()

        print("Weak Skills")
        if profile.weak_skills:
            for skill in profile.weak_skills:
                print(f" • {skill}")
        else:
            print(" None")

        print()

        print("Mastered Skills")
        if profile.mastered_skills:
            for skill in profile.mastered_skills:
                print(f" • {skill}")
        else:
            print(" None")

        print()

        print("Review Queue")
        if profile.review_queue:
            for concept in profile.review_queue:
                print(f" • {concept}")
        else:
            print(" None")

        print("----------------------------------")


        print()


        print("SKILL PROGRESS")

        if not profile.skill_progress:
            print(" None")

        else:
            print("----------------------------------")

            for progress in profile.skill_progress.values():
                print(f"Skill      : {progress.skill}")
                print(f"Attempts   : {progress.attempts}")
                print(f"Correct    : {progress.correct}")
                print(f"Incorrect  : {progress.incorrect}")
                print(f"Mastery    : {progress.mastery:.2f}%")

                print("----------------------------------")

    show("TEACHING PLANS", analysis.teaching_plans)

    # --- Seção customizada para GRAMMAR CONCEPTS ---
    print("\nGRAMMAR CONCEPTS")

    if not analysis.concepts:
        print("None")
    else:
        for concept in analysis.concepts:
            # Se print_concept já der um print interno, mude para: print_concept(concept)
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

sentence = "I went yesterday."

analysis = grammar_engine.analyze(sentence)

print_analysis(analysis)
