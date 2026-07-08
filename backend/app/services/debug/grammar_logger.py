from __future__ import annotations

from app.services.grammar_engine.models import GrammarAnalysis


class GrammarLogger:
    def log(self, analysis: GrammarAnalysis):

        print()
        print("=" * 60)
        print("🧠 NEW GRAMMAR ENGINE (SHADOW MODE)")
        print("=" * 60)

        print(f"Sentence: {analysis.context.original_sentence}")

        print()

        print("Errors")

        if analysis.has_errors:
            for skill in analysis.detected_skills:
                print(f" • {skill}")
        else:
            print(" None")

        print()

        print("Primary Error")

        if analysis.primary_error:
            print(analysis.primary_error.skill)
        else:
            print("None")

        print()

        print("Concepts")

        if analysis.has_concepts:
            for name in analysis.concept_names:
                print(f" • {name}")
        else:
            print(" None")

        print()

        print("Primary Concept")

        if analysis.primary_concept:
            print(analysis.primary_concept.name)
        else:
            print("None")

        print()

        if analysis.has_learning_profile:
            print("Learning Profile")

            print(f" Current Focus : {analysis.current_focus}")

            print(f" Accuracy      : {analysis.accuracy:.2f}%")

            print(f" Weak Skills   : {analysis.weak_skills}")

            print(f" Mastered      : {analysis.mastered_skills}")

        print("=" * 60)
        print()


grammar_logger = GrammarLogger()
