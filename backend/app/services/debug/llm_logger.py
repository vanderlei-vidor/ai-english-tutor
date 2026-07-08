from __future__ import annotations


class LLMLogger:
    def request(self):

        print()
        print("=== SENDING TO LM STUDIO ===")

    def response(
        self,
        response_time,
        known_error,
    ):

        print(f"LM STUDIO RESPONSE TIME: {response_time:.2f}s")
        print(f"KNOWN ERROR RESULT: {known_error}")

    def ai_decision(
        self,
        action,
        confidence,
    ):

        print()
        print("=== AI ORIGINAL DECISION ===")
        print(f"ACTION: {action} | CONFIDENCE: {confidence}")
        print("============================")

    def final_decision(
        self,
        action,
    ):

        print()
        print("=== FINAL BACKEND DECISION ===")
        print(f"FINAL ACTION DETERMINED: {action}")
        print("==============================")

    def summary(
        self,
        action,
        correction,
        confidence,
    ):

        print()
        print("=== AI SUMMARY DECISION ===")
        print(f"ACTION: {action}")
        print(f"CORRECTION: {correction}")
        print(f"CONFIDENCE: {confidence}")
        print("===================")


llm_logger = LLMLogger()
