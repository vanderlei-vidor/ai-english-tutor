from __future__ import annotations

from app.services.pedagogical.analysis import PedagogicalAnalysis


class PedagogicalLogger:
    def advanced_level(
        self,
        structures,
        complexity_points,
        advanced_memory,
        level_score,
        estimated_level,
    ):

        print(f"🎓 ADVANCED STRUCTURES DETECTED: {structures}")
        print(f"🎓 COMPLEXITY POINTS: {complexity_points}")

        print(f"🎓 ADVANCED MEMORY: {advanced_memory}")
        print(f"🎓 LEVEL SCORE: {level_score}")
        print(f"🎓 ESTIMATED LEVEL: {estimated_level}")

    def analysis(
        self,
        pedagogical: PedagogicalAnalysis,
    ):

        print(f"🎓 ADVANCED STRUCTURES DETECTED: {pedagogical.structures}")
        print(f"🎓 COMPLEXITY POINTS: {pedagogical.complexity_points}")

        print(f"🎓 ADVANCED MEMORY: {pedagogical.advanced_structures}")
        print(f"🎓 LEVEL SCORE: {pedagogical.estimated_score}")
        print(f"🎓 ESTIMATED LEVEL: {pedagogical.estimated_level}")

    def normalized_skills(
        self,
        normalized_scores,
        selected_skill,
    ):

        print("======== NORMALIZED SKILL SCORES ========")

        for skill, score in normalized_scores.items():
            print(f"{skill}: {score}")

        print("=========================================")
        print(f"🎯 NORMALIZED SKILL SELECTED: {selected_skill}")

    def backend(
        self,
        turns,
        since_last_teaching,
        probability,
        chance_hit,
        routed_mode,
        weakness_score,
        target_skill,
        exercise_required,
        wants_teaching,
    ):

        print()
        print("=== DEBUG PEDAGOGICAL BACKEND ===")

        print(f"TURNS:            {turns} | SINCE LAST TEACHING: {since_last_teaching}")

        print(f"TEACH PROBABILITY: {probability:.1f}% | CHANCE HIT: {chance_hit}")

        print(f"ROUTED MODE:      {routed_mode}")
        print(f"SCORE DE FRAQUEZA: {weakness_score}")
        print(f"TARGET SKILL:     {target_skill}")
        print(f"EXERCISE REQUIRED:{exercise_required}")
        print(f"BACKEND WANTS TEACHING: {wants_teaching}")

        print("=================================")


pedagogical_logger = PedagogicalLogger()
