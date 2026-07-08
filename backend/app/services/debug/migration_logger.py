from __future__ import annotations


class MigrationLogger:
    def target_skill(
        self,
        legacy_target_skill,
        new_target_skill,
        final_target_skill,
    ):

        print()

        print("=" * 60)
        print("⚖️ TARGET SKILL MIGRATION")
        print("=" * 60)

        print(f"Legacy Target Skill : {legacy_target_skill}")
        print(f"New Current Focus   : {new_target_skill}")
        print(f"Using               : {final_target_skill}")

        print("=" * 60)

    def error(
        self,
        legacy_error,
        grammar_error,
    ):

        print()

        print("=" * 60)
        print("⚖️ ERROR MIGRATION")
        print("=" * 60)

        print(f"Legacy Error : {legacy_error}")
        print(f"Grammar      : {grammar_error}")

        print("=" * 60)


migration_logger = MigrationLogger()
