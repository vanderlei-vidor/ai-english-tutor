from __future__ import annotations

from app.services.grammar_engine.concepts.models import GrammarConcept


def concept_summary(concept: GrammarConcept) -> str:
    """
    Retorna um resumo amigável do conceito.
    """

    return f"{concept.name} (Level {concept.level}) [Skill: {concept.skill}]"


from app.services.grammar_engine.concepts.models import GrammarConcept


def print_concept(concept: GrammarConcept):

    print("----------------------------------")

    print(f"Name        : {concept.name}")

    print(f"Level       : {concept.level}")

    print(f"Skill       : {concept.skill}")

    print(f"Priority    : {concept.teaching_priority}")

    print(f"Difficulty  : {concept.exercise_difficulty}")

    print(f"Review      : {concept.review_after_days} days")

    print(f"Mastery     : {concept.mastery_threshold}%")

    print()

    print("Prerequisites")

    for item in concept.prerequisites:
        print(f" • {item}")

    print()

    print("Examples")

    for item in concept.examples:
        print(f" • {item}")

    print()

    print("Common Errors")

    for item in concept.common_errors:
        print(f" • {item}")

    print("----------------------------------")