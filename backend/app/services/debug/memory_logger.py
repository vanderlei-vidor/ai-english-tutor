from __future__ import annotations


class MemoryLogger:
    def incoming(
        self,
        detected_skill,
        target_skill,
        had_error,
        target_skill_error,
    ):

        print("======== MEMORY SERVICE INCOMING ========")
        print(f"DETECTED: {detected_skill} | TARGET: {target_skill}")
        print(f"HAD_ERROR: {had_error} | TARGET_ERROR: {target_skill_error}")
        print("=========================================")


memory_logger = MemoryLogger()
