from __future__ import annotations

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