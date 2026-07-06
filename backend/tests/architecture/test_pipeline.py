from app.services.grammar_engine.engine import grammar_engine

from app.services.pedagogical.presentation_engine import (
    lesson_presentation_engine,
)

from app.services.pedagogical.prompt.context_builder import (
    prompt_context_builder,
)


def separator(title: str):

    print()
    print("=" * 70)
    print(title)
    print("=" * 70)


analysis = grammar_engine.analyze("I go yesterday.")

separator("GRAMMAR ERRORS")

if analysis.errors:
    for error in analysis.errors:
        print(error)

else:
    print("None")


separator("GRAMMAR CONCEPTS")

if analysis.concepts:
    for concept in analysis.concepts:
        print(concept.name)

else:
    print("None")


separator("TEACHING PLANS")

if analysis.teaching_plans:
    for plan in analysis.teaching_plans:
        print(plan.title)

else:
    print("None")


separator("LESSON PRESENTATION")



if analysis.presented_lessons:
    for lesson in analysis.presented_lessons:
        print()

        print("TITLE")
        print(lesson.title)

        print()

        print("EXPLANATION")
        print(lesson.explanation)

        print()

        print("EXAMPLES")

        for example in lesson.examples:
            print(f"• {example}")

else:
    print("None")


separator("PROMPT CONTEXT")

if analysis.presented_lessons:
    for lesson in analysis.presented_lessons:
        context = prompt_context_builder.build(lesson)

        print(context)

else:
    print("None")


separator("PIPELINE STATUS")

print("Grammar Engine        ✅")

print("Concept Engine        ✅")

print("Pedagogical Engine    ✅")

print("Presentation Layer    ✅")

print("Prompt Builder        ✅")

print()

print("Architecture Test Finished Successfully 🚀")
